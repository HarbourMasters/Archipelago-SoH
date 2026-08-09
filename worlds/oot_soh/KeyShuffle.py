from typing import TYPE_CHECKING
from collections import namedtuple

from .Items import Items, item_data_table
from .Locations import location_data_table
from .Regions import map_and_compass_vanilla_mapping
from .Enums import DungeonLocations, Locations
from .LogicHelpers import key_to_ring
from .DungeonRewardShuffle import dungeon_reward_item_mapping

if TYPE_CHECKING:
    from . import SohWorld

option_mapping = namedtuple('Key_Mapping', ['Dungeon', 'Option', 'Quantity'])

def get_own_dungeon_prefill_items(world: "SohWorld") -> dict[DungeonLocations, list[Items]]:
        key_shuffle_locations = dict[DungeonLocations, list[Items]]()
        for location_type in DungeonLocations:
            key_shuffle_locations[location_type] = list[Items]()

        # Boss Keys
        if world.options.boss_key_shuffle == "own_dungeon":
            key_shuffle_locations[DungeonLocations.FOREST_TEMPLE].append(Items.FOREST_TEMPLE_BOSS_KEY)
            key_shuffle_locations[DungeonLocations.FIRE_TEMPLE].append(Items.FIRE_TEMPLE_BOSS_KEY)
            key_shuffle_locations[DungeonLocations.WATER_TEMPLE].append(Items.WATER_TEMPLE_BOSS_KEY)
            key_shuffle_locations[DungeonLocations.SPIRIT_TEMPLE].append(Items.SPIRIT_TEMPLE_BOSS_KEY)
            key_shuffle_locations[DungeonLocations.SHADOW_TEMPLE].append(Items.SHADOW_TEMPLE_BOSS_KEY)

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
            map_and_compass_dungeon_mapping: dict[DungeonLocations, list[Items]] = {
                DungeonLocations.DEKU_TREE : [Items.GREAT_DEKU_TREE_MAP, Items.GREAT_DEKU_TREE_COMPASS],
                DungeonLocations.DODONGOS_CAVERN : [Items.DODONGOS_CAVERN_MAP, Items.DODONGOS_CAVERN_COMPASS],
                DungeonLocations.JABU_JABUS_BELLY : [Items.JABU_JABUS_BELLY_MAP, Items.JABU_JABUS_BELLY_COMPASS],
                DungeonLocations.FOREST_TEMPLE : [Items.FOREST_TEMPLE_MAP, Items.FOREST_TEMPLE_COMPASS],
                DungeonLocations.FIRE_TEMPLE : [Items.FIRE_TEMPLE_MAP, Items.FIRE_TEMPLE_COMPASS],
                DungeonLocations.WATER_TEMPLE : [Items.WATER_TEMPLE_MAP, Items.WATER_TEMPLE_COMPASS],
                DungeonLocations.SPIRIT_TEMPLE : [Items.SPIRIT_TEMPLE_MAP, Items.SPIRIT_TEMPLE_COMPASS],
                DungeonLocations.SHADOW_TEMPLE : [Items.SHADOW_TEMPLE_MAP, Items.SHADOW_TEMPLE_COMPASS],
                DungeonLocations.BOTTOM_OF_THE_WELL : [Items.BOTTOM_OF_THE_WELL_MAP, Items.BOTTOM_OF_THE_WELL_COMPASS],
                DungeonLocations.ICE_CAVERN : [Items.ICE_CAVERN_MAP, Items.ICE_CAVERN_COMPASS]
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
            shuffle_items += [Items.FOREST_TEMPLE_BOSS_KEY, Items.FIRE_TEMPLE_BOSS_KEY, Items.WATER_TEMPLE_BOSS_KEY, Items.SPIRIT_TEMPLE_BOSS_KEY, Items.SHADOW_TEMPLE_BOSS_KEY]

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
                    shuffle_items.append(Items.GERUDO_FORTRESS_KEY_RING)
                else:
                    for _ in range(item_data_table[Items.GERUDO_FORTRESS_SMALL_KEY].quantity_in_item_pool if world.options.fortress_carpenters == "normal" else 1):
                        shuffle_items.append(Items.GERUDO_FORTRESS_SMALL_KEY)

        # Maps and Compasses
        if world.options.maps_and_compasses == shuffle_setting:
            shuffle_items += list(map_and_compass_vanilla_mapping.values())

        # Dungeon Rewards
        if world.options.shuffle_dungeon_rewards == shuffle_setting:
            shuffle_items += list(dungeon_reward_item_mapping.values())

        # Triforce pieces
        if world.options.triforce_hunt and world.options.triforce_hunt_pieces_location == shuffle_setting:
            for _ in range(world.options.triforce_hunt_pieces_total.value):
                shuffle_items.append(Items.TRIFORCE_PIECE)

        return shuffle_items
        

def pre_fill_own_dungeon_items(world: "SohWorld") -> None:
        own_dungeon_items = get_own_dungeon_prefill_items(world)
        key_shuffle_locations = dict[DungeonLocations, list[Locations]]()
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
            Items.FOREST_TEMPLE_SMALL_KEY: option_mapping(DungeonLocations.FOREST_TEMPLE, world.options.forest_temple_key_ring, item_data_table[Items.FOREST_TEMPLE_SMALL_KEY].quantity_in_item_pool),
            Items.FIRE_TEMPLE_SMALL_KEY: option_mapping(DungeonLocations.FIRE_TEMPLE, world.options.fire_temple_key_ring, item_data_table[Items.FIRE_TEMPLE_SMALL_KEY].quantity_in_item_pool),
            Items.WATER_TEMPLE_SMALL_KEY: option_mapping(DungeonLocations.WATER_TEMPLE, world.options.water_temple_key_ring, item_data_table[Items.WATER_TEMPLE_SMALL_KEY].quantity_in_item_pool),
            Items.SPIRIT_TEMPLE_SMALL_KEY: option_mapping(DungeonLocations.SPIRIT_TEMPLE, world.options.spirit_temple_key_ring, item_data_table[Items.SPIRIT_TEMPLE_SMALL_KEY].quantity_in_item_pool),
            Items.SHADOW_TEMPLE_SMALL_KEY: option_mapping(DungeonLocations.SHADOW_TEMPLE, world.options.shadow_temple_key_ring, item_data_table[Items.SHADOW_TEMPLE_SMALL_KEY].quantity_in_item_pool),
            Items.BOTTOM_OF_THE_WELL_SMALL_KEY: option_mapping(DungeonLocations.BOTTOM_OF_THE_WELL, world.options.bottom_of_the_well_key_ring, item_data_table[Items.BOTTOM_OF_THE_WELL_SMALL_KEY].quantity_in_item_pool),
            Items.GANONS_CASTLE_SMALL_KEY: option_mapping(DungeonLocations.GANONS_CASTLE, world.options.ganons_castle_key_ring, item_data_table[Items.GANONS_CASTLE_SMALL_KEY].quantity_in_item_pool),
            Items.TRAINING_GROUND_SMALL_KEY: option_mapping(DungeonLocations.GERUDO_TRAINING_GROUNDS, world.options.gerudo_training_ground_key_ring, item_data_table[Items.TRAINING_GROUND_SMALL_KEY].quantity_in_item_pool)
        }