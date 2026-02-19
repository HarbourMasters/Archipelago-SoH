from typing import TYPE_CHECKING
from Fill import fill_restrictive

from .Regions import dungeon_reward_item_mapping
from .Items import SohItem, Items

if TYPE_CHECKING:
    from . import SohWorld

def get_pre_fill_rewards(world: "SohWorld") -> list[Items]:
    if world.options.shuffle_dungeon_rewards != "dungeons":
        return list()
    return list(dungeon_reward_item_mapping.values())

def reserve_dungeon_reward_locations(world: "SohWorld"):
    if world.options.shuffle_dungeon_rewards != "dungeons":
         return

    world.reserved_pre_fill_locations += list(dungeon_reward_item_mapping.keys())

def remove_dungeon_reward_reservations(world: "SohWorld"):
    world.reserved_pre_fill_locations = [loc for loc in world.reserved_pre_fill_locations if loc not in dungeon_reward_item_mapping.keys()]

def pre_fill_dungeon_rewards(world: "SohWorld") -> None:
    if world.options.shuffle_dungeon_rewards != "dungeons":
         return

    remove_dungeon_reward_reservations(world)

    dungeon_reward_locations = world.get_empty_locations_from_list_shuffled(dungeon_reward_item_mapping.keys())
    
    dungeon_reward_items = list[SohItem]()
    for item in get_pre_fill_rewards(world):
        world.pre_fill_pool.remove(item)
        dungeon_reward_items.append(world.create_item(item))

    completion_items = [c.name for c in dungeon_reward_items]
    world.multiworld.completion_condition[world.player] = lambda state: state.has_all(completion_items, world.player)

    prefill_state = world.get_pre_fill_state()

    # Place dungeon rewards
    fill_restrictive(world.multiworld, prefill_state, dungeon_reward_locations,
                     dungeon_reward_items, single_player_placement=True, lock=True)
