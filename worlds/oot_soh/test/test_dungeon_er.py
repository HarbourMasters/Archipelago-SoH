import sys
from typing import ClassVar

from .. import SohWorld
from ..EntranceShuffle import STANDARD_DUNGEONS
from .bases import SohTestBase

# Number of seeds each multi-seed test sweeps. Kept modest so the suite stays fast.
SEEDS = 25


def _build(option: str, seed: int) -> SohWorld:
    class _T(SohTestBase):
        options: ClassVar[dict[str, str]] = {"shuffle_dungeon_entrances": option}

        def runTest(self):  # noqa: N802 - satisfies TestCase construction
            pass

    t = _T()
    t.world_setup(seed=seed)
    return t.world, t.multiworld


def _age_reachable(multiworld, world):
    state = multiworld.get_all_state(False)
    player = world.player
    state._soh_stale[player] = True
    state._soh_update_age_reachable_regions(player)
    child = {r.name for r in state._soh_child_reachable_regions[player]}
    adult = {r.name for r in state._soh_adult_reachable_regions[player]}
    return child, adult


class SeedReportMixin:
    """SoH tests generate on a random seed (WorldTestBase.setUp -> world_setup() with no
    seed). Mixed into a test class, this prints that seed whenever the test fails, so a
    random-seed failure can be reproduced with ``world_setup(seed=<printed value>)``.

    It is a plain mixin (not a TestCase) so unittest never collects it on its own."""

    def setUp(self) -> None:
        super().setUp()
        # Capture the seed now: the memory-leak tearDown deletes self.multiworld before
        # addCleanup callbacks run, so we can't read it later.
        self._captured_seed = getattr(getattr(self, "multiworld", None), "seed", None)
        self.addCleanup(self._report_seed_on_failure)

    def _report_seed_on_failure(self) -> None:
        outcome = getattr(self, "_outcome", None)
        result = getattr(outcome, "result", None) if outcome else None
        if (result is not None and self._captured_seed is not None
                and any(tc is self for tc, _ in result.errors + result.failures)):
            sys.stderr.write(
                f"\n[oot_soh dungeon ER] reproduce this failure with seed: {self._captured_seed}\n")


class TestDungeonEROff(SeedReportMixin, SohTestBase):
    options: ClassVar[dict[str, str]] = {"shuffle_dungeon_entrances": "off"}
    world: SohWorld

    def test_no_shuffle_no_pairings(self):
        self.assertEqual(self.world.entrance_pairings, [])

    def test_vanilla_still_beatable(self):
        state = self.multiworld.get_all_state(False)
        self.assertTrue(self.multiworld.has_beaten_game(state, self.world.player))


class TestDungeonERStructure(SeedReportMixin, SohTestBase):
    options: ClassVar[dict[str, str]] = {"shuffle_dungeon_entrances": "simple"}
    world: SohWorld

    def test_pairing_count_and_permutation(self):
        layout = self.world.entrance_pairings
        self.assertEqual(len(layout), len(STANDARD_DUNGEONS))
        sources = [a for a, _ in layout]
        dests = [b for _, b in layout]
        self.assertEqual(len(set(sources)), len(sources), "an entryway was shuffled twice")
        self.assertEqual(set(sources), set(dests), "layout is not a permutation of entryways")

    def test_interior_edges_preserved(self):
        # The fixed ENTRYWAY -> interior edges must never be shuffled away.
        deku = self.world.get_region("Deku Tree Entryway")
        self.assertTrue(any(e.connected_region and e.connected_region.name == "Deku Tree Lobby"
                            for e in deku.exits))

    def test_blue_warps_follow_the_dungeon(self):
        # A dungeon's blue warp must land at the slot it now occupies, never its vanilla
        # overworld region (unless it stayed vanilla). Otherwise the apworld would grant
        # that region on boss completion when the game would not.
        from ..EntranceShuffle import DUNGEON_BLUE_WARPS
        slot_of = {new: orig for orig, new in self.world.entrance_pairings}
        for entryway, (boss_room, vanilla_bw) in DUNGEON_BLUE_WARPS.items():
            self.assertIn(entryway, slot_of, f"{entryway} missing from simple pool")
            boss = self.world.get_region(str(boss_room))
            warp_targets = [e.connected_region.name for e in boss.exits
                            if e.connected_region and "Boss" not in e.connected_region.name]
            if slot_of[entryway] == entryway:  # dungeon stayed vanilla
                self.assertIn(str(vanilla_bw), warp_targets)
            else:
                self.assertNotIn(str(vanilla_bw), warp_targets,
                                 f"{entryway} moved but its blue warp still points to vanilla {vanilla_bw}")

    def test_slot_data_layout_valid(self):
        from ..Enums import Regions
        region_names = {str(r) for r in Regions}
        layout = self.world.fill_slot_data()["dungeon_entrance_layout"]
        self.assertEqual(len(layout), len(STANDARD_DUNGEONS))
        for src, dst in layout:
            self.assertIn(src, region_names)
            self.assertIn(dst, region_names)


class TestDungeonERRobustness(SohTestBase):
    """Multi-seed sweeps asserting generation always succeeds and stays beatable, and that
    age-locked dungeons land where their required age can reach them."""

    options: ClassVar[dict[str, str]] = {"shuffle_dungeon_entrances": "simple"}
    world: SohWorld

    def test_simple_beatable_across_seeds(self):
        for seed in range(SEEDS):
            world, multiworld = _build("simple", seed)
            state = multiworld.get_all_state(False)
            self.assertTrue(multiworld.has_beaten_game(state, world.player),
                            f"simple seed {seed} not beatable")

    def test_all_beatable_and_ganon_adult_reachable(self):
        for seed in range(SEEDS):
            world, multiworld = _build("all", seed)
            self.assertEqual(len(world.entrance_pairings), len(STANDARD_DUNGEONS) + 1)
            state = multiworld.get_all_state(False)
            self.assertTrue(multiworld.has_beaten_game(state, world.player),
                            f"all seed {seed} not beatable")
            child, adult = _age_reachable(multiworld, world)
            # Ganon's Castle is adult-only; its interior must be adult-reachable.
            self.assertIn("Ganon's Castle Lobby", adult, f"all seed {seed}: Ganon unreachable as adult")
            # Jabu-Jabu is child-only; its interior must be child-reachable.
            self.assertIn("Jabu Jabus Belly Beginning", child, f"all seed {seed}: Jabu unreachable as child")

    def test_deterministic(self):
        for option in ("simple", "all"):
            first, _ = _build(option, 12345)
            second, _ = _build(option, 12345)
            self.assertEqual(first.entrance_pairings, second.entrance_pairings)


def _region_graph(multiworld, player):
    return {r.name: sorted(e.connected_region.name for e in r.exits if e.connected_region)
            for r in multiworld.get_regions(player)}


class TestDungeonERUniversalTracker(SeedReportMixin, SohTestBase):
    """Universal Tracker re-generates from slot_data; it must reproduce the seed's exact
    entrance graph rather than re-rolling a new one."""

    options: ClassVar[dict[str, str]] = {"shuffle_dungeon_entrances": "all"}
    world: SohWorld

    def test_ut_reproduces_exact_layout_and_graph(self):
        from test.general import gen_steps, setup_multiworld
        from worlds.AutoWorld import call_all
        slot_data = self.world.fill_slot_data()
        layout = [list(pair) for pair in self.world.entrance_pairings]
        original_graph = _region_graph(self.multiworld, self.world.player)

        # Re-generate the way UT does: feed the slot_data back in via re_gen_passthrough,
        # using a *different* seed so a re-roll would produce a different layout.
        mw = setup_multiworld(SohWorld, steps=(), seed=987654, options={})
        mw.re_gen_passthrough = {"Ship of Harkinian": slot_data}
        for step in gen_steps:
            call_all(mw, step)
        tracked = mw.worlds[mw.player_ids[0]]

        self.assertTrue(tracked.using_ut)
        self.assertEqual([list(p) for p in tracked.entrance_pairings], layout)
        self.assertEqual(_region_graph(mw, tracked.player), original_graph,
                         "UT reconstructed a different entrance graph")
