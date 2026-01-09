from typing import TYPE_CHECKING
from worlds.generic.Rules import add_rule
from Fill import fill_restrictive
from BaseClasses import CollectionState

from . import SohItem
from .Locations import Locations, location_name_groups
from .Items import Items

if TYPE_CHECKING:
    from . import SohWorld

song_vanilla_locations: dict[Locations, Items] = {
    Locations.SONG_FROM_IMPA: Items.ZELDAS_LULLABY,
    Locations.SONG_FROM_MALON: Items.EPONAS_SONG,
    Locations.SONG_FROM_SARIA: Items.SARIAS_SONG,
    Locations.SONG_FROM_ROYAL_FAMILYS_TOMB: Items.SUNS_SONG,
    Locations.SONG_FROM_OCARINA_OF_TIME: Items.SONG_OF_TIME,
    Locations.SONG_FROM_WINDMILL: Items.SONG_OF_STORMS,
    Locations.SHEIK_IN_FOREST: Items.MINUET_OF_FOREST,
    Locations.SHEIK_IN_CRATER: Items.BOLERO_OF_FIRE,
    Locations.SHEIK_IN_ICE_CAVERN: Items.SERENADE_OF_WATER,
    Locations.SHEIK_IN_KAKARIKO: Items.NOCTURNE_OF_SHADOW,
    Locations.SHEIK_AT_COLOSSUS: Items.REQUIEM_OF_SPIRIT,
    Locations.SHEIK_AT_TEMPLE: Items.PRELUDE_OF_LIGHT
}

def get_prefill_songs(world: "SohWorld") -> list[Items]:
    # Do not prefill songs anywhere in particular
    if world.options.shuffle_songs in ("off", "anywhere"):
        return list()
    
    return list(song_vanilla_locations.values())

def pre_fill_songs(world: "SohWorld") -> None:
    # Do not prefill songs anywhere in particular
    if world.options.shuffle_songs in ("off", "anywhere"):
        return

    songs = list[SohItem]()
    for item in get_prefill_songs(world):
        songs.append(world.create_item(item))
        world.pre_fill_pool.remove(item)

    prefill_state = world.get_pre_fill_state()
    reward_goal_locations = [world.get_location(loc) for loc in location_name_groups["Bosses"]]
    world.multiworld.completion_condition[world.player] = lambda state: all([state.can_reach(loc) for loc in reward_goal_locations])

    if world.options.shuffle_songs == "song_locations":
        song_locations = [world.get_location(loc) for loc in song_vanilla_locations.keys()]

        fill_restrictive(world.multiworld, prefill_state, song_locations, songs, single_player_placement=True, lock=True)
        return

    if world.options.shuffle_songs == "dungeon_rewards":
        reward_locations = list()
        reward_locations.append(world.get_location(Locations.DEKU_TREE_QUEEN_GOHMA_HEART_CONTAINER))
        reward_locations.append(world.get_location(Locations.DODONGOS_CAVERN_KING_DODONGO_HEART_CONTAINER))
        reward_locations.append(world.get_location(Locations.JABU_JABUS_BELLY_BARINADE_HEART_CONTAINER))
        reward_locations.append(world.get_location(Locations.FOREST_TEMPLE_PHANTOM_GANON_HEART_CONTAINER))
        reward_locations.append(world.get_location(Locations.FIRE_TEMPLE_VOLVAGIA_HEART_CONTAINER))
        reward_locations.append(world.get_location(Locations.WATER_TEMPLE_MORPHA_HEART_CONTAINER))
        reward_locations.append(world.get_location(Locations.SHADOW_TEMPLE_BONGO_BONGO_HEART_CONTAINER))
        reward_locations.append(world.get_location(Locations.SPIRIT_TEMPLE_TWINROVA_HEART_CONTAINER))
        reward_locations.append(world.get_location(Locations.SONG_FROM_IMPA))
        reward_locations.append(world.get_location(Locations.SHEIK_IN_ICE_CAVERN))
        reward_locations.append(world.get_location(Locations.BOTTOM_OF_THE_WELL_LENS_OF_TRUTH_CHEST))   # todo MQ lens of truth chest
        reward_locations.append(world.get_location(Locations.GERUDO_TRAINING_GROUND_MAZE_PATH_FINAL_CHEST)) # todo MQ ice arrow chest

        fill_restrictive(world.multiworld, prefill_state, reward_locations, songs, single_player_placement=True, lock=True)
        return
    


