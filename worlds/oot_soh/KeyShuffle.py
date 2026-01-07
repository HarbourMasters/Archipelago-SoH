from typing import TYPE_CHECKING
from collections import namedtuple
from Fill import fill_restrictive

from .Items import Items, item_data_table
from .Locations import Location, location_data_table
from .Regions import dungeon_reward_item_mapping
from .Enums import KeyShuffleLocations, Locations
from .ShopItems import all_shop_locations
from .LogicHelpers import key_to_ring

if TYPE_CHECKING:
    from . import SohWorld

def get_pre_fill_keys(world: "SohWorld") -> dict[KeyShuffleLocations, list[Items]]:
        key_shuffle_locations = dict[KeyShuffleLocations, list[Items]]()
        for location_type in KeyShuffleLocations:
            key_shuffle_locations[location_type] = list[Items]()

        # Boss Keys
        if world.options.boss_key_shuffle == "own_dungeon":
            key_shuffle_locations[KeyShuffleLocations.FOREST_TEMPLE].append(Items.FOREST_TEMPLE_BOSS_KEY)
            key_shuffle_locations[KeyShuffleLocations.FIRE_TEMPLE].append(Items.FIRE_TEMPLE_BOSS_KEY)
            key_shuffle_locations[KeyShuffleLocations.WATER_TEMPLE].append(Items.WATER_TEMPLE_BOSS_KEY)
            key_shuffle_locations[KeyShuffleLocations.SPIRIT_TEMPLE].append(Items.SPIRIT_TEMPLE_BOSS_KEY)
            key_shuffle_locations[KeyShuffleLocations.SHADOW_TEMPLE].append(Items.SHADOW_TEMPLE_BOSS_KEY)
        elif world.options.boss_key_shuffle == "any_dungeon":
            key_shuffle_locations[KeyShuffleLocations.ANY_DUNGEON] += [Items.FOREST_TEMPLE_BOSS_KEY, Items.FIRE_TEMPLE_BOSS_KEY, Items.WATER_TEMPLE_BOSS_KEY, Items.SPIRIT_TEMPLE_BOSS_KEY, Items.SHADOW_TEMPLE_BOSS_KEY]
        elif world.options.boss_key_shuffle == "overworld":
            key_shuffle_locations[KeyShuffleLocations.OVERWORLD] += [Items.FOREST_TEMPLE_BOSS_KEY, Items.FIRE_TEMPLE_BOSS_KEY, Items.WATER_TEMPLE_BOSS_KEY, Items.SPIRIT_TEMPLE_BOSS_KEY, Items.SHADOW_TEMPLE_BOSS_KEY]

        # Small Keys
        option_mapping = namedtuple('Key_Mapping', ['Dungeon', 'Option', 'Quantity'])
        small_key_option_mapping = {
            Items.FOREST_TEMPLE_SMALL_KEY: option_mapping(KeyShuffleLocations.FOREST_TEMPLE, world.options.forest_temple_key_ring, item_data_table[Items.FOREST_TEMPLE_SMALL_KEY].quantity_in_item_pool),
            Items.FIRE_TEMPLE_SMALL_KEY: option_mapping(KeyShuffleLocations.FIRE_TEMPLE, world.options.fire_temple_key_ring, item_data_table[Items.FIRE_TEMPLE_SMALL_KEY].quantity_in_item_pool),
            Items.WATER_TEMPLE_SMALL_KEY: option_mapping(KeyShuffleLocations.WATER_TEMPLE, world.options.water_temple_key_ring, item_data_table[Items.WATER_TEMPLE_SMALL_KEY].quantity_in_item_pool),
            Items.SPIRIT_TEMPLE_SMALL_KEY: option_mapping(KeyShuffleLocations.SPIRIT_TEMPLE, world.options.spirit_temple_key_ring, item_data_table[Items.SPIRIT_TEMPLE_SMALL_KEY].quantity_in_item_pool),
            Items.SHADOW_TEMPLE_SMALL_KEY: option_mapping(KeyShuffleLocations.SHADOW_TEMPLE, world.options.shadow_temple_key_ring, item_data_table[Items.SHADOW_TEMPLE_SMALL_KEY].quantity_in_item_pool),
            Items.BOTTOM_OF_THE_WELL_SMALL_KEY: option_mapping(KeyShuffleLocations.BOTTOM_OF_THE_WELL, world.options.bottom_of_the_well_key_ring, item_data_table[Items.BOTTOM_OF_THE_WELL_SMALL_KEY].quantity_in_item_pool),
            Items.GANONS_CASTLE_SMALL_KEY: option_mapping(KeyShuffleLocations.GANONS_CASTLE, world.options.ganons_castle_key_ring, item_data_table[Items.GANONS_CASTLE_SMALL_KEY].quantity_in_item_pool),
            Items.TRAINING_GROUND_SMALL_KEY: option_mapping(KeyShuffleLocations.GERUDO_TRAINING_GROUNDS, world.options.gerudo_training_ground_key_ring, item_data_table[Items.TRAINING_GROUND_SMALL_KEY].quantity_in_item_pool)
        }
        
        if world.options.small_key_shuffle in ("own_dungeon", "any_dungeon", "overworld"):
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

                if world.options.small_key_shuffle == "own_dungeon":
                    for _ in range(count):
                        key_shuffle_locations[dungeon].append(item)
                elif world.options.small_key_shuffle == "any_dungeon":
                    for _ in range(count):
                        key_shuffle_locations[KeyShuffleLocations.ANY_DUNGEON].append(item)
                elif world.options.small_key_shuffle == "overworld":
                    for _ in range(count):
                        key_shuffle_locations[KeyShuffleLocations.OVERWORLD].append(item)

        # Gerudo Fortress Keys
        if world.options.fortress_carpenters != "free":
            if world.options.gerudo_fortress_key_shuffle == "any_dungeon":
                if world.options.gerudo_fortress_key_ring and world.options.fortress_carpenters == "normal" and world.options.gerudo_fortress_key_shuffle != "vanilla":
                    key_shuffle_locations[KeyShuffleLocations.ANY_DUNGEON].append(Items.GERUDO_FORTRESS_KEY_RING)
                else:
                    for _ in range(item_data_table[Items.GERUDO_FORTRESS_SMALL_KEY].quantity_in_item_pool if world.options.fortress_carpenters == "normal" else 1):
                        key_shuffle_locations[KeyShuffleLocations.ANY_DUNGEON].append(Items.GERUDO_FORTRESS_SMALL_KEY)

            elif world.options.gerudo_fortress_key_shuffle == "overworld":
                if world.options.gerudo_fortress_key_ring and world.options.fortress_carpenters == "normal" and world.options.gerudo_fortress_key_shuffle != "vanilla":
                    key_shuffle_locations[KeyShuffleLocations.OVERWORLD].append(Items.GERUDO_FORTRESS_KEY_RING)
                else:
                    for _ in range(item_data_table[Items.GERUDO_FORTRESS_SMALL_KEY].quantity_in_item_pool if world.options.fortress_carpenters == "normal" else 1):
                        key_shuffle_locations[KeyShuffleLocations.OVERWORLD].append(Items.GERUDO_FORTRESS_SMALL_KEY)

        return key_shuffle_locations

    

def pre_fill_keys(world: "SohWorld") -> None:
        all_locations: list[str] = [location.name for location in world.multiworld.get_unfilled_locations(world.player)]
        reserved_locations: list[Locations] = []

        # Reserve dungeon reward locations if a dungeon reward should be there
        if world.options.shuffle_dungeon_rewards != "anywhere":
            reserved_locations += [location for location in dungeon_reward_item_mapping.keys()]

        # Reserve Shop Locations       # todo, only reserve vanilla shop slots
        for data in all_shop_locations:
            for location in data[1].keys():
                reserved_locations.append(location)

        key_shuffle_keys = get_pre_fill_keys(world)
        key_shuffle_locations = dict[KeyShuffleLocations, list[Locations]]()
        for location_type in KeyShuffleLocations:
            key_shuffle_locations[location_type] = list[Location]()

        # This loops through all unfilled locations in the players world, removes any from our reserved list (Shops and Dungeon Rewards if applicable), then sorts them into three categories: Overworld, Any Dungeon, and Own Dungeon
        for name, data in location_data_table.items():
            if name in all_locations and name not in reserved_locations:
                if data.key_suffle_location == None:
                    key_shuffle_locations[KeyShuffleLocations.OVERWORLD].append(Locations(name))
                else:
                    key_shuffle_locations[KeyShuffleLocations.ANY_DUNGEON].append(Locations(name))
                    key_shuffle_locations[data.key_suffle_location].append(Locations(name))

        # use full dungeon accessability as the goal for filling
        all_dungeon_location_goal = [world.get_location(loc) for loc in key_shuffle_locations[KeyShuffleLocations.ANY_DUNGEON]]
        world.multiworld.completion_condition[world.player] = lambda state: all([state.can_reach(loc) for loc in all_dungeon_location_goal])

        # Resolve own_dungeon, any_dungeon and overworld options
        for shuffle_location, keys in key_shuffle_keys.items():
            if not keys:
                continue

            for key in keys:
                world.pre_fill_pool.remove(key)

            prefill_state = world.get_pre_fill_state()
            found = False
            for other_location, other_keys in key_shuffle_keys.items():
                if shuffle_location == other_location:
                    found = True
                    continue
                if found:
                    for other_key in other_keys:
                        prefill_state.collect(world.create_item(other_key), True)
            prefill_state.sweep_for_advancements()

            empty_locations = world.get_empty_locations_from_list_shuffled(key_shuffle_locations[shuffle_location])
            key_items = [world.create_item(str(key)) for key in keys]

            fill_restrictive(world.multiworld, prefill_state, empty_locations, key_items, single_player_placement=True, lock=True)
