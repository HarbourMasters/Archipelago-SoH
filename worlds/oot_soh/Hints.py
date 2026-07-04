from collections import Counter
from typing import TYPE_CHECKING, Callable, Iterable, NamedTuple
from collections import Counter

from BaseClasses import MultiWorld, Options, Item
from .Locations import location_data_table
from worlds.generic.Rules import set_rule
from worlds.AutoWorld import LogicMixin
from .Enums import HintKeys as hk, Items, Locations
from .Items import SohItem, item_data_table, ItemType, no_rules_bottles

if TYPE_CHECKING:
    from . import SohWorld

import logging
logger = logging.getLogger("SOH_OOT.Logic")

class locationPair(NamedTuple):
    player: int
    location: int

class StaticHint(NamedTuple):
    key: hk
    locations: list[locationPair]
    def serialize(self):
        return {self.key.value: [[loc.player, loc.location] for loc in self.locations]}

class OptionItemMapping(NamedTuple):
    option: Options.NumericOption
    hint_items: list[Items]

def GetNonlocalHintOptionMapping(world: "SohWorld") -> dict[hk, OptionItemMapping]:
    return {
        hk.GANONDORF_HINT: OptionItemMapping(world.options.ganondorf_hint, [Items.LIGHT_ARROW, Items.MASTER_SWORD]),
        hk.SHEIK_HINT: OptionItemMapping(world.options.sheik_la_hint, [Items.LIGHT_ARROW]),
        hk.DAMPES_DIARY: OptionItemMapping(world.options.dampe_diary_hint, [Items.PROGRESSIVE_HOOKSHOT]),
        hk.GREG_RUPEE: OptionItemMapping(world.options.greg_hint, [Items.GREG_THE_GREEN_RUPEE]),
        hk.ALTAR_CHILD: OptionItemMapping(world.options.tot_altar_hint, [Items.KOKIRIS_EMERALD, Items.GORONS_RUBY, Items.ZORAS_SAPPHIRE]),
        hk.ALTAR_ADULT: OptionItemMapping(world.options.tot_altar_hint, [Items.LIGHT_MEDALLION, Items.FOREST_MEDALLION, Items.FIRE_MEDALLION, Items.WATER_MEDALLION, Items.SPIRIT_MEDALLION, Items.SHADOW_MEDALLION]),
        hk.FOREST_BOSS_KEY_HINT: OptionItemMapping(world.options.boss_key_hint, [Items.FOREST_TEMPLE_BOSS_KEY]),
        hk.FIRE_BOSS_KEY_HINT: OptionItemMapping(world.options.boss_key_hint, [Items.FIRE_TEMPLE_BOSS_KEY]),
        hk.WATER_BOSS_KEY_HINT: OptionItemMapping(world.options.boss_key_hint, [Items.WATER_TEMPLE_BOSS_KEY]),
        hk.SPIRIT_BOSS_KEY_HINT: OptionItemMapping(world.options.boss_key_hint, [Items.SPIRIT_TEMPLE_BOSS_KEY]),
        hk.SHADOW_BOSS_KEY_HINT: OptionItemMapping(world.options.boss_key_hint, [Items.SHADOW_TEMPLE_BOSS_KEY]),
        hk.GANONS_BOSS_KEY_HINT: OptionItemMapping(world.options.boss_key_hint, [Items.GANONS_CASTLE_BOSS_KEY]),
        hk.SARIA_HINT: OptionItemMapping(world.options.saria_hint, [Items.PROGRESSIVE_MAGIC_METER]),
        hk.MIDO_HINT: OptionItemMapping(world.options.mido_hint, [Items.KOKIRI_SWORD]),
        hk.FISHING_POLE: OptionItemMapping(world.options.fishing_pole_hint, [Items.FISHING_POLE])
    }

def CreateNonlocalHints(world: "SohWorld") -> list[StaticHint]:
    hints = list[StaticHint]()

    for hint_key, mapping in GetNonlocalHintOptionMapping(world).items():
        if not mapping.option.value:
            continue

        hint_locations = list[locationPair]()

        for hinted_item in mapping.hint_items:
            # find the item and create a hint
            # check if we start with the item first
            placed_item = FindHintedItemInPool(hinted_item, world.multiworld.precollected_items[world.player])
            if placed_item:
                hint_locations.append(locationPair(world.player, location_data_table[Locations.LINKS_POCKET].loc_id))
                continue

            # then check if it's placed somewhere in the multiworld
            placed_item = FindHintedItemInPool(hinted_item, world.item_pool)
            if not placed_item:
                placed_item = FindHintedItemInPool(hinted_item, world.preplaced_items)
            if placed_item:
                if placed_item.location.address == None:
                    # the item is in our world but has no location for some reason, this means it could be an item link
                    # search the entire world for the real items location
                    placed_item = FindHintedItemFromMultiWorld(hinted_item, world.multiworld)
                    if placed_item == None:
                        # I don't know anymore
                        continue
                if placed_item.location.address != None:
                    hint_locations.append(locationPair(placed_item.location.player, placed_item.location.address))
        hints.append(StaticHint(hint_key, hint_locations))

    return hints

def FindHintedItemInPool(hinted_item: Items, pool: Iterable[Item]) -> Item | None:
    for item in pool:
        if item.name != hinted_item:
            continue
        return item

    return None

def FindHintedItemFromMultiWorld(hinted_item: Items, multiworld: MultiWorld) -> Item | None:
    for location in multiworld.get_locations():
        if location.address == None:
            continue
        if location.item == None:
            continue

        if location.item.name == hinted_item:
            if location.item.location.address == None:
                continue
            return location.item
    return None
