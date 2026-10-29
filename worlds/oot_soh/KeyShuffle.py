from typing import TYPE_CHECKING
from collections import defaultdict, namedtuple

from .Items import Items, item_data_table
from .Locations import location_data_table
from .Regions import maps_and_compasses
from .Enums import Locations
from .ship_data_gen import CheckArea
from .LogicHelpers import key_to_ring
from .MasterQuest import small_key_count
from .DungeonRewardShuffle import dungeon_reward_item_mapping

if TYPE_CHECKING:
    from . import SohWorld

option_mapping = namedtuple('Key_Mapping', ['Dungeon', 'Option', 'Quantity'])

def get_own_dungeon_prefill_items(world: "SohWorld") -> dict[CheckArea, list[Items]]:
        key_shuffle_locations: dict[CheckArea, list[Items]] = defaultdict(list)

        # Boss Keys
        if world.options.boss_key_shuffle == "own_dungeon":
            key_shuffle_locations[CheckArea.RCAREA_FOREST_TEMPLE].append(Items.RG_FOREST_TEMPLE_BOSS_KEY)
            key_shuffle_locations[CheckArea.RCAREA_FIRE_TEMPLE].append(Items.RG_FIRE_TEMPLE_BOSS_KEY)
            key_shuffle_locations[CheckArea.RCAREA_WATER_TEMPLE].append(Items.RG_WATER_TEMPLE_BOSS_KEY)
            key_shuffle_locations[CheckArea.RCAREA_SPIRIT_TEMPLE].append(Items.RG_SPIRIT_TEMPLE_BOSS_KEY)
            key_shuffle_locations[CheckArea.RCAREA_SHADOW_TEMPLE].append(Items.RG_SHADOW_TEMPLE_BOSS_KEY)

        # Small Keys
        small_key_option_mapping = small_key_option_matching(world)
        
        if world.options.small_key_shuffle == "own_dungeon":
            # Put the small keys or keyrings in the appropriate pool
            for key, data in small_key_option_mapping.items():
                dungeon = data.Dungeon
                key_ring_option = data.Option

                if key_ring_option:
                    item = key_to_ring[key]
                    count = 1
                else:
                    item = key
                    count = data.Quantity

                for _ in range(count):
                    key_shuffle_locations[dungeon].append(item)

        # Maps and Compasses
        if world.options.maps_and_compasses == "own_dungeon":
            map_and_compass_dungeon_mapping: dict[CheckArea, list[Items]] = {
                CheckArea.RCAREA_DEKU_TREE : [Items.RG_DEKU_TREE_MAP, Items.RG_DEKU_TREE_COMPASS],
                CheckArea.RCAREA_DODONGOS_CAVERN : [Items.RG_DODONGOS_CAVERN_MAP, Items.RG_DODONGOS_CAVERN_COMPASS],
                CheckArea.RCAREA_JABU_JABUS_BELLY : [Items.RG_JABU_JABUS_BELLY_MAP, Items.RG_JABU_JABUS_BELLY_COMPASS],
                CheckArea.RCAREA_FOREST_TEMPLE : [Items.RG_FOREST_TEMPLE_MAP, Items.RG_FOREST_TEMPLE_COMPASS],
                CheckArea.RCAREA_FIRE_TEMPLE : [Items.RG_FIRE_TEMPLE_MAP, Items.RG_FIRE_TEMPLE_COMPASS],
                CheckArea.RCAREA_WATER_TEMPLE : [Items.RG_WATER_TEMPLE_MAP, Items.RG_WATER_TEMPLE_COMPASS],
                CheckArea.RCAREA_SPIRIT_TEMPLE : [Items.RG_SPIRIT_TEMPLE_MAP, Items.RG_SPIRIT_TEMPLE_COMPASS],
                CheckArea.RCAREA_SHADOW_TEMPLE : [Items.RG_SHADOW_TEMPLE_MAP, Items.RG_SHADOW_TEMPLE_COMPASS],
                CheckArea.RCAREA_BOTTOM_OF_THE_WELL : [Items.RG_BOTTOM_OF_THE_WELL_MAP, Items.RG_BOTTOM_OF_THE_WELL_COMPASS],
                CheckArea.RCAREA_ICE_CAVERN : [Items.RG_ICE_CAVERN_MAP, Items.RG_ICE_CAVERN_COMPASS]
            }

            for shuffle_location, items in map_and_compass_dungeon_mapping.items():
                key_shuffle_locations[shuffle_location] += items

        return key_shuffle_locations


def get_dungeon_item_prefill_items(world: "SohWorld", overworld_shuffle: bool) -> list[Items]:
        shuffle_items = list[Items]()

        shuffle_setting = "any_dungeon"
        if overworld_shuffle:
             shuffle_setting = "overworld"

        # Boss Keys
        if world.options.boss_key_shuffle == shuffle_setting:
            shuffle_items += [Items.RG_FOREST_TEMPLE_BOSS_KEY, Items.RG_FIRE_TEMPLE_BOSS_KEY, Items.RG_WATER_TEMPLE_BOSS_KEY, Items.RG_SPIRIT_TEMPLE_BOSS_KEY, Items.RG_SHADOW_TEMPLE_BOSS_KEY]

        # Small Keys
        small_key_option_mapping = small_key_option_matching(world)
        
        if world.options.small_key_shuffle == shuffle_setting:
            # Put the small keys or keyrings in the appropriate pool
            for key, data in small_key_option_mapping.items():
                key_ring_option = data.Option

                if key_ring_option:
                    item = key_to_ring[key]
                    count = 1
                else:
                    item = key
                    count = data.Quantity

                for _ in range(count):
                    shuffle_items.append(item)

        # Gerudo Fortress Keys
        if world.options.fortress_carpenters != "free":
            if world.options.gerudo_fortress_key_shuffle == shuffle_setting:
                if world.options.gerudo_fortress_key_ring and world.options.fortress_carpenters == "normal" and world.options.gerudo_fortress_key_shuffle != "vanilla":
                    shuffle_items.append(Items.RG_GERUDO_FORTRESS_KEY_RING)
                else:
                    for _ in range(item_data_table[Items.RG_GERUDO_FORTRESS_SMALL_KEY].quantity_in_item_pool if world.options.fortress_carpenters == "normal" else 1):
                        shuffle_items.append(Items.RG_GERUDO_FORTRESS_SMALL_KEY)

        # Maps and Compasses
        if world.options.maps_and_compasses == shuffle_setting:
            shuffle_items += maps_and_compasses

        # Dungeon Rewards
        if world.options.shuffle_dungeon_rewards == shuffle_setting:
            shuffle_items += list(dungeon_reward_item_mapping.values())

        return shuffle_items
        

def pre_fill_own_dungeon_items(world: "SohWorld") -> None:
        own_dungeon_items = get_own_dungeon_prefill_items(world)
        key_shuffle_locations = dict[CheckArea, list[Locations]]()
        for location in world.multiworld.get_unfilled_locations(world.player):
            name = location.name
            if name not in location_data_table:
                continue

            dungeon = location_data_table[name].dungeon_tag
            if dungeon == None:
                continue

            if dungeon not in key_shuffle_locations:
                key_shuffle_locations[dungeon] = list()
                
            key_shuffle_locations[dungeon].append(Locations(name))

        # remove the items from the pre-fill pool
        for items in own_dungeon_items.values():
            for item in items:
                world.pre_fill_pool.remove(item)
        
        # get a single pre-fill state, this state is shared between the different dungeons but that's fine
        prefill_state = world.get_pre_fill_state()

        # Resolve own_dungeon
        for dungeon, items in own_dungeon_items.items():
            if not items:
                continue

            world.run_prefill(items, key_shuffle_locations[dungeon], prefill_state)

def pre_fill_any_dungeon_keys(world: "SohWorld") -> None:
        any_dungeon_items = get_dungeon_item_prefill_items(world, False)
        all_dungeon_locations:list[Locations] = [Locations(loc.name) for loc in world.multiworld.get_unfilled_locations(world.player)
                                                if location_data_table[loc.name].dungeon_tag != None]

        world.run_prefill(any_dungeon_items, all_dungeon_locations)

def pre_fill_overworld_items(world: "SohWorld") -> None:
        overworld_items = get_dungeon_item_prefill_items(world, True)
        overworld_locations:list[Locations] = [Locations(loc.name) for loc in world.multiworld.get_unfilled_locations(world.player)
                                                if location_data_table[loc.name].dungeon_tag == None ]
        world.run_prefill(overworld_items, overworld_locations)

def small_key_option_matching(world: "SohWorld") -> dict[Items, option_mapping]:
    return {
            Items.RG_FOREST_TEMPLE_SMALL_KEY: option_mapping(CheckArea.RCAREA_FOREST_TEMPLE, world.options.forest_temple_key_ring, small_key_count(world, Items.RG_FOREST_TEMPLE_SMALL_KEY)),
            Items.RG_FIRE_TEMPLE_SMALL_KEY: option_mapping(CheckArea.RCAREA_FIRE_TEMPLE, world.options.fire_temple_key_ring, small_key_count(world, Items.RG_FIRE_TEMPLE_SMALL_KEY)),
            Items.RG_WATER_TEMPLE_SMALL_KEY: option_mapping(CheckArea.RCAREA_WATER_TEMPLE, world.options.water_temple_key_ring, small_key_count(world, Items.RG_WATER_TEMPLE_SMALL_KEY)),
            Items.RG_SPIRIT_TEMPLE_SMALL_KEY: option_mapping(CheckArea.RCAREA_SPIRIT_TEMPLE, world.options.spirit_temple_key_ring, small_key_count(world, Items.RG_SPIRIT_TEMPLE_SMALL_KEY)),
            Items.RG_SHADOW_TEMPLE_SMALL_KEY: option_mapping(CheckArea.RCAREA_SHADOW_TEMPLE, world.options.shadow_temple_key_ring, small_key_count(world, Items.RG_SHADOW_TEMPLE_SMALL_KEY)),
            Items.RG_BOTTOM_OF_THE_WELL_SMALL_KEY: option_mapping(CheckArea.RCAREA_BOTTOM_OF_THE_WELL, world.options.bottom_of_the_well_key_ring, small_key_count(world, Items.RG_BOTTOM_OF_THE_WELL_SMALL_KEY)),
            Items.RG_GANONS_CASTLE_SMALL_KEY: option_mapping(CheckArea.RCAREA_GANONS_CASTLE, world.options.ganons_castle_key_ring, small_key_count(world, Items.RG_GANONS_CASTLE_SMALL_KEY)),
            Items.RG_GERUDO_TRAINING_GROUND_SMALL_KEY: option_mapping(CheckArea.RCAREA_GERUDO_TRAINING_GROUND, world.options.gerudo_training_ground_key_ring, small_key_count(world, Items.RG_GERUDO_TRAINING_GROUND_SMALL_KEY))
        }