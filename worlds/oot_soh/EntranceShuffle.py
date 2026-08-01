"""Dungeon entrance randomization for Ship of Harkinian.

The layout is computed here during generation (so item fill respects it) using
Archipelago's generic entrance randomizer, then shipped to the game client via slot_data
as canonical entryway-to-entryway name pairs (see fill_slot_data).

Each dungeon boundary in the region graph looks like:

    overworld_source --(forward)--> DUNGEON_ENTRYWAY --(interior, fixed)--> lobby
    overworld_return <--(return)-- DUNGEON_ENTRYWAY

We shuffle the coupled (forward, return) boundary edges among all dungeons while leaving
the fixed ENTRYWAY->interior edge untouched. Two randomization groups keep overworld-side
exits connecting only to entryway-side targets (and vice versa), so a dungeon mouth can
never connect straight to another mouth's overworld side (which would orphan dungeons).

oot_soh reachability note: this world does not use the standard reachable_regions graph.
It keeps its own dual-age reachable sets (RegionAgeAccess) cached behind a ``_soh_stale``
flag that is only invalidated on item collect/remove -- never on entrance graph changes.
The generic randomizer mutates the graph as it connects entrances, so we invalidate that
cache from the ``on_connect`` hook and request an extra sweep, keeping the randomizer's
reachability analysis in sync with the age BFS.
"""

from collections import deque
from enum import IntEnum
from typing import TYPE_CHECKING

from BaseClasses import Entrance, EntranceType, Region

from entrance_rando import (randomize_entrances, disconnect_entrance_for_randomization,
                            EntranceRandomizationError)
from .Enums import Ages, Regions
from .Options import ShuffleDungeonEntrances

if TYPE_CHECKING:
    from . import SohWorld


class ERGroup(IntEnum):
    # Overworld-side half-edges (overworld -> entryway, and their reverse targets).
    DUNGEON_OVERWORLD = 1
    # Entryway-side half-edges (entryway -> overworld, and their reverse targets).
    DUNGEON_ENTRYWAY = 2


class SohEntrance(Entrance):
    """Dungeon boundary edge with two custom behaviors versus the base Entrance:

    1. Permits a dungeon to map to itself (stay vanilla). The base ``can_connect_to``
       forbids same-name connections in coupled mode to avoid a degenerate self-loop.
       In our two-group design the overworld and entryway halves of a dungeon are
       distinct edges that merely share a name, so a dungeon-to-itself placement couples
       correctly; forbidding it deadlocks whenever the final placement must be a self-map.

    2. Enforces age-complete dungeon placement. Every dungeon must land at an overworld
       spot reachable by each age it requires (``world.dungeon_age_requirements``, derived
       by _compute_age_requirements). Because the vanilla world is fully accessible,
       preserving a dungeon's age access preserves reachability of all its locations --
       e.g. Spirit Temple has both child- and adult-only content and so must stay reachable
       by both. ``self`` is the overworld-side door, and the check verifies its edge is
       actually traversable at the required age (adult-only items like the Hookshot/Iron
       Boots gate some spots)."""

    def _traversable_as(self, cs, player: int, age) -> bool:
        if cs._soh_stale[player]:
            cs._soh_update_age_reachable_regions(player)
        reachable = (cs._soh_child_reachable_regions[player] if age == Ages.CHILD
                     else cs._soh_adult_reachable_regions[player])
        if self.parent_region not in reachable:
            return False
        saved_age = cs._soh_age[player]
        cs._soh_age[player] = age
        try:
            return bool(self.access_rule(cs))
        finally:
            cs._soh_age[player] = saved_age

    def can_connect_to(self, other: Entrance, dead_end: bool, er_state) -> bool:
        if self.randomization_type != other.randomization_type:
            return False
        dest = other.connected_region
        if dest is not None:
            cs = er_state.collection_state
            requirements = cs.multiworld.worlds[self.player].dungeon_age_requirements
            for age in requirements.get(dest.name, ()):
                if not self._traversable_as(cs, self.player, age):
                    return False
        return True


TARGET_GROUP_LOOKUP: dict[int, list[int]] = {
    ERGroup.DUNGEON_OVERWORLD: [ERGroup.DUNGEON_ENTRYWAY],
    ERGroup.DUNGEON_ENTRYWAY: [ERGroup.DUNGEON_OVERWORLD],
}


# (dungeon display name, entryway region, overworld region the entryway returns to).
# The overworld *source* of the forward edge is discovered from the graph (it is not
# always the same region as the return target, e.g. Gerudo Training Ground).
STANDARD_DUNGEONS: list[tuple[str, Regions, Regions]] = [
    ("Deku Tree", Regions.DEKU_TREE_ENTRYWAY, Regions.KF_OUTSIDE_DEKU_TREE),
    ("Dodongos Cavern", Regions.DODONGOS_CAVERN_ENTRYWAY, Regions.DEATH_MOUNTAIN_TRAIL),
    ("Jabu Jabus Belly", Regions.JABU_JABUS_BELLY_ENTRYWAY, Regions.ZORAS_FOUNTAIN),
    ("Forest Temple", Regions.FOREST_TEMPLE_ENTRYWAY, Regions.SACRED_FOREST_MEADOW),
    ("Fire Temple", Regions.FIRE_TEMPLE_ENTRYWAY, Regions.DMC_CENTRAL_LOCAL),
    ("Water Temple", Regions.WATER_TEMPLE_ENTRYWAY, Regions.LH_FROM_WATER_TEMPLE),
    ("Spirit Temple", Regions.SPIRIT_TEMPLE_ENTRYWAY, Regions.DESERT_COLOSSUS_OUTSIDE_TEMPLE),
    ("Shadow Temple", Regions.SHADOW_TEMPLE_ENTRYWAY, Regions.GRAVEYARD_WARP_PAD_REGION),
    ("Bottom of the Well", Regions.BOTTOM_OF_THE_WELL_ENTRYWAY, Regions.KAK_WELL),
    ("Ice Cavern", Regions.ICE_CAVERN_ENTRYWAY, Regions.ZF_LEDGE),
    ("Gerudo Training Ground", Regions.GERUDO_TRAINING_GROUND_ENTRYWAY, Regions.GF_EXITING_GTG),
]
GANON_DUNGEON: tuple[str, Regions, Regions] = (
    "Ganons Castle", Regions.GANONS_CASTLE_ENTRYWAY, Regions.CASTLE_GROUNDS_FROM_GANONS_CASTLE,
)

# Coupled placement with age-locked dungeons can deadlock; retry with fresh randomness.
MAX_SHUFFLE_ATTEMPTS = 50

def _reachable_regions(world: "SohWorld", skip: Region | None = None) -> set[Region]:
    """Regions reachable from ROOT by graph connectivity alone (ignoring rules and age).
    With ``skip`` set, that region is treated as removed from the graph."""
    root = world.multiworld.get_region(str(Regions.ROOT), world.player)
    seen = {root}
    queue = deque([root])
    while queue:
        region = queue.popleft()
        for ex in region.exits:
            nxt = ex.connected_region
            if nxt is None or nxt in seen or nxt is skip:
                continue
            seen.add(nxt)
            queue.append(nxt)
    return seen


def _compute_age_requirements(world: "SohWorld") -> dict[str, set]:
    """Derive, per dungeon, the age(s) that must be able to reach its entryway for the
    world to stay fully accessible and beatable, replacing a hand-maintained table.

    A dungeon's interior is the set of regions reachable *only* through its entryway
    (remove the entryway and they fall off the graph). With every entryway temporarily made
    reachable as both ages, we ask of each interior location -- item checks *and* events,
    matching the full-accessibility invariant that every get_locations() entry stay
    reachable -- whether it is doable as only one age. Those single-age locations pin the
    dungeon's placement: a child-only item/event means child must reach the dungeon; the
    Ganon-defeat event (adult-only) means adult must; a dungeon whose every location is
    doable by either age imposes no constraint."""
    mw, player = world.multiworld, world.player
    entryways = [str(entryway) for _name, entryway, _return in _dungeons_for(world)]

    reachable_all = _reachable_regions(world)
    interior = {name: reachable_all - _reachable_regions(world, skip=mw.get_region(name, player))
                for name in entryways}

    state = mw.get_all_state(False)
    root = mw.get_region(str(Regions.ROOT), player)
    probes = []
    for name in entryways:
        entryway = mw.get_region(name, player)
        probe = Entrance(player, f"_age probe {name}", root)
        probe.connected_region = entryway
        root.exits.append(probe)
        entryway.entrances.append(probe)
        probes.append((probe, entryway))

    # Recompute both age-reachable sets to a fixpoint: a single pass leaves edges whose
    # dependencies were not yet reachable parked in the blocked set, re-tried next pass.
    state._soh_invalidate(player)
    child_regions = state._soh_child_reachable_regions[player]
    adult_regions = state._soh_adult_reachable_regions[player]
    prev = None
    while True:
        state._soh_update_age_reachable_regions(player)
        size = (len(child_regions), len(adult_regions))
        if size == prev:
            break
        prev = size
        state._soh_stale[player] = True

    def _doable_as(location, age, reachable) -> bool:
        if location.parent_region not in reachable:
            return False
        saved_age = state._soh_age[player]
        state._soh_age[player] = age
        try:
            return bool(location.access_rule(state))
        finally:
            state._soh_age[player] = saved_age

    requirements: dict[str, set] = {}
    for name in entryways:
        ages: set = set()
        for region in interior[name]:
            for location in region.locations:
                child_ok = _doable_as(location, Ages.CHILD, child_regions)
                adult_ok = _doable_as(location, Ages.ADULT, adult_regions)
                if child_ok and not adult_ok:
                    ages.add(Ages.CHILD)
                elif adult_ok and not child_ok:
                    ages.add(Ages.ADULT)
            if len(ages) == 2:
                break
        requirements[name] = ages

    for probe, entryway in probes:
        root.exits.remove(probe)
        entryway.entrances.remove(probe)
    return requirements


def _dungeons_for(world: "SohWorld") -> list[tuple[str, Regions, Regions]]:
    dungeons = list(STANDARD_DUNGEONS)
    if world.options.shuffle_dungeon_entrances == ShuffleDungeonEntrances.option_all:
        dungeons.append(GANON_DUNGEON)
    return dungeons


def _find_return_exit(entryway: Region, return_target_name: str) -> Entrance:
    """The entryway's exit back to the overworld (as opposed to the fixed interior edge)."""
    candidates = [ex for ex in entryway.exits
                  if ex.connected_region is not None and ex.connected_region.name == return_target_name]
    if len(candidates) != 1:
        raise Exception(f"[oot_soh ER] expected exactly one return exit from {entryway.name} "
                        f"to {return_target_name}, found {len(candidates)}")
    return candidates[0]


def _find_forward_exit(world: "SohWorld", entryway: Region, interior_target: Region) -> Entrance:
    """The overworld exit that leads into this entryway. Each entryway also has an
    interior "leave the dungeon" back-edge (parent == the interior target region); that
    one is excluded so only the shufflable overworld door is returned."""
    candidates = [ex for region in world.multiworld.get_regions(world.player)
                  for ex in region.exits
                  if ex.connected_region is entryway and ex.parent_region is not interior_target]
    if len(candidates) != 1:
        raise Exception(f"[oot_soh ER] expected exactly one forward entrance to "
                        f"{entryway.name}, found {len(candidates)}")
    return candidates[0]


# Dungeons with a boss, and thus a blue warp (boss room -> overworld on completion).
# entryway name -> (boss room region, vanilla blue-warp destination region).
DUNGEON_BLUE_WARPS: dict[str, tuple[Regions, Regions]] = {
    str(Regions.DEKU_TREE_ENTRYWAY): (Regions.DEKU_TREE_BOSS_ROOM, Regions.KF_OUTSIDE_DEKU_TREE),
    str(Regions.DODONGOS_CAVERN_ENTRYWAY): (Regions.DODONGOS_CAVERN_BOSS_ROOM, Regions.DEATH_MOUNTAIN_TRAIL),
    str(Regions.JABU_JABUS_BELLY_ENTRYWAY): (Regions.JABU_JABUS_BELLY_BOSS_ROOM, Regions.ZORAS_FOUNTAIN),
    str(Regions.FOREST_TEMPLE_ENTRYWAY): (Regions.FOREST_TEMPLE_BOSS_ROOM, Regions.SACRED_FOREST_MEADOW),
    str(Regions.FIRE_TEMPLE_ENTRYWAY): (Regions.FIRE_TEMPLE_BOSS_ROOM, Regions.DMC_CENTRAL_LOCAL),
    str(Regions.WATER_TEMPLE_ENTRYWAY): (Regions.WATER_TEMPLE_BOSS_ROOM, Regions.LAKE_HYLIA),
    str(Regions.SPIRIT_TEMPLE_ENTRYWAY): (Regions.SPIRIT_TEMPLE_BOSS_ROOM, Regions.DESERT_COLOSSUS),
    str(Regions.SHADOW_TEMPLE_ENTRYWAY): (Regions.SHADOW_TEMPLE_BOSS_ROOM, Regions.GRAVEYARD_WARP_PAD_REGION),
}


def _reroute_blue_warps(world: "SohWorld", layout: list[list[str]],
                        exit_region_by_entryway: dict[str, Region]) -> None:
    """Point each dungeon's blue warp at the overworld destination of the slot it now
    occupies, matching the client."""
    for orig_name, new_name in layout:
        blue_warp = DUNGEON_BLUE_WARPS.get(new_name)
        if blue_warp is None:
            continue  # dungeon has no boss / blue warp (Bottom of the Well, Ice, GTG, Ganon)
        boss_room_enum, vanilla_bw_enum = blue_warp
        boss_room = world.multiworld.get_region(str(boss_room_enum), world.player)
        # Match the client's SetBlueWarps(): a dungeon at a boss slot warps to that slot's
        # blue-warp region (for Spirit/Water that is the main overworld region, not the
        # temple-exit sub-region the front door returns to); otherwise to the exit region.
        slot_blue_warp = DUNGEON_BLUE_WARPS.get(orig_name)
        if slot_blue_warp is not None:
            target_region = world.multiworld.get_region(str(slot_blue_warp[1]), world.player)
        else:
            target_region = exit_region_by_entryway[orig_name]
        for ex in boss_room.exits:
            if ex.connected_region is not None and ex.connected_region.name == str(vanilla_bw_enum):
                _reconnect(ex, target_region)
                break


def _reconnect(exit_entrance: Entrance, new_region: Region) -> None:
    if exit_entrance.connected_region is not None and exit_entrance in exit_entrance.connected_region.entrances:
        exit_entrance.connected_region.entrances.remove(exit_entrance)
    exit_entrance.connected_region = new_region
    new_region.entrances.append(exit_entrance)


def apply_dungeon_entrance_layout(world: "SohWorld", layout: list[list[str]]) -> None:
    """Deterministically wire a known [original_entryway, new_entryway] layout instead of
    randomizing (used by Universal Tracker)."""
    # entryway name -> (forward exit, return exit, entry region, exit region)
    boundaries: dict[str, tuple[Entrance, Entrance, Region, Region]] = {}
    for _name, entryway_enum, return_enum in _dungeons_for(world):
        entryway = world.multiworld.get_region(str(entryway_enum), world.player)
        ret = _find_return_exit(entryway, str(return_enum))
        interior_target = next(ex.connected_region for ex in entryway.exits if ex is not ret)
        forward = _find_forward_exit(world, entryway, interior_target)
        boundaries[str(entryway_enum)] = (forward, ret, forward.parent_region, ret.connected_region)

    for orig_name, new_name in layout:
        forward, _ret, _entry_region, exit_region = boundaries[orig_name]
        _new_forward, new_ret, _new_entry, _new_exit = boundaries[new_name]
        new_entryway = world.multiworld.get_region(new_name, world.player)
        # The door at orig's overworld spot now leads to new dungeon's entryway...
        _reconnect(forward, new_entryway)
        # ...and exiting the new dungeon returns to orig's overworld exit region (coupled).
        _reconnect(new_ret, exit_region)

    _reroute_blue_warps(world, layout, {name: b[3] for name, b in boundaries.items()})


def shuffle_dungeon_entrances(world: "SohWorld") -> list[list[str]]:
    """Randomize the dungeon boundary edges (coupled) and return the layout as
    [original_entryway, new_entryway] name pairs (one per shuffled overworld door)."""
    # Derived here (on the still-vanilla graph) and read by SohEntrance.can_connect_to.
    world.dungeon_age_requirements = _compute_age_requirements(world)

    original_entryway: dict[Entrance, str] = {}
    exits: list[Entrance] = []
    exit_region_by_entryway: dict[str, Region] = {}
    # forward exit -> (entry region, exit region) for slots where they differ (Spirit,
    # Gerudo Training Ground, Ganon). Generic ER's coupling drops a dungeon's exit back at
    # the entry region, so we redirect it to the true exit region afterwards, otherwise the
    # exit region (and its locations, e.g. Sheik at Colossus) is orphaned.
    asymmetric_slots: list[tuple[Entrance, Region, Region]] = []

    for name, entryway_enum, _return_enum in _dungeons_for(world):
        entryway = world.multiworld.get_region(str(entryway_enum), world.player)
        if len(entryway.exits) != 2:
            raise Exception(f"[oot_soh ER] expected {entryway.name} to have exactly 2 exits "
                            f"(interior + return), found {len(entryway.exits)}")
        ret = _find_return_exit(entryway, str(_return_enum))
        interior_target = next(ex.connected_region for ex in entryway.exits if ex is not ret)
        forward = _find_forward_exit(world, entryway, interior_target)

        entry_region = forward.parent_region
        exit_region = ret.connected_region
        exit_region_by_entryway[str(entryway_enum)] = exit_region
        if exit_region is not entry_region:
            asymmetric_slots.append((forward, entry_region, exit_region))

        entrance_name = f"{name} Entrance"
        forward.__class__ = SohEntrance
        forward.name = entrance_name
        forward.randomization_type = EntranceType.TWO_WAY
        forward.randomization_group = ERGroup.DUNGEON_OVERWORLD
        ret.__class__ = SohEntrance
        ret.name = entrance_name
        ret.randomization_type = EntranceType.TWO_WAY
        ret.randomization_group = ERGroup.DUNGEON_ENTRYWAY

        original_entryway[forward] = str(entryway_enum)
        exits.append(forward)
        exits.append(ret)

    for ex in exits:
        disconnect_entrance_for_randomization(ex)

    # Deterministic exit/target ordering (randomize_entrances shuffles internally).
    exits.sort(key=lambda e: (e.parent_region.name, e.name))
    er_targets = sorted(
        [en for region in world.multiworld.get_regions(world.player) for en in region.entrances
         if en.parent_region is None
         and en.randomization_group in (ERGroup.DUNGEON_OVERWORLD, ERGroup.DUNGEON_ENTRYWAY)],
        key=lambda en: (en.connected_region.name, en.name))

    def reset_to_disconnected() -> None:
        # Restore the clean "all boundary edges disconnected" state so randomize_entrances
        # can be retried after a constraint-induced deadlock (see entrance_rando: "retries
        # may be implemented if early deadlocking is a frequent issue").
        for ex in exits:
            if ex.connected_region is not None:
                if ex in ex.connected_region.entrances:
                    ex.connected_region.entrances.remove(ex)
                ex.connected_region = None
        for target in er_targets:
            home = target.connected_region
            if target not in home.entrances:
                home.entrances.append(target)

    def on_connect(er_state, _placed_exits, _paired_entrances) -> bool:
        # See the module docstring: invalidate the age cache and force a full standard
        # recompute after each placement so both stay in sync with the mutated graph.
        cs = er_state.collection_state
        cs._soh_stale[world.player] = True
        cs.reachable_regions[world.player].clear()
        cs.blocked_connections[world.player].clear()
        cs.stale[world.player] = True
        return True

    result = None
    for attempt in range(MAX_SHUFFLE_ATTEMPTS):
        try:
            result = randomize_entrances(world, coupled=True, target_group_lookup=TARGET_GROUP_LOOKUP,
                                         exits=exits, er_targets=er_targets, on_connect=on_connect)
            break
        except EntranceRandomizationError:
            reset_to_disconnected()
    if result is None:
        raise EntranceRandomizationError(
            f"[oot_soh ER] could not place dungeon entrances after {MAX_SHUFFLE_ATTEMPTS} attempts")

    # Non-symmetric slot fixup: a dungeon placed at a slot whose entry and exit regions
    # differ should drop the player at the exit region on the way out (coupled ER connected
    # it to the entry region). Redirect the resident dungeon's return edge accordingly so
    # the exit region and its locations stay reachable.
    for forward, entry_region, exit_region in asymmetric_slots:
        resident_entryway = forward.connected_region
        for ex in resident_entryway.exits:
            if isinstance(ex, SohEntrance) and ex.connected_region is entry_region:
                entry_region.entrances.remove(ex)
                ex.connected_region = exit_region
                exit_region.entrances.append(ex)
                break

    # Only the overworld-side (forward) placements describe "which dungeon is now here".
    layout: list[list[str]] = []
    for placed in result.placements:
        if placed in original_entryway:
            layout.append([original_entryway[placed], placed.connected_region.name])
    layout.sort()

    _reroute_blue_warps(world, layout, exit_region_by_entryway)
    return layout
