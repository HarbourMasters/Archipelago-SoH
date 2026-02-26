from typing import TYPE_CHECKING

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

dungeon_reward_song_locations: list[Locations] = [
    Locations.DEKU_TREE_QUEEN_GOHMA_HEART_CONTAINER,
    Locations.DODONGOS_CAVERN_KING_DODONGO_HEART_CONTAINER,
    Locations.JABU_JABUS_BELLY_BARINADE_HEART_CONTAINER,
    Locations.FOREST_TEMPLE_PHANTOM_GANON_HEART_CONTAINER,
    Locations.FIRE_TEMPLE_VOLVAGIA_HEART_CONTAINER,
    Locations.WATER_TEMPLE_MORPHA_HEART_CONTAINER,
    Locations.SHADOW_TEMPLE_BONGO_BONGO_HEART_CONTAINER,
    Locations.SPIRIT_TEMPLE_TWINROVA_HEART_CONTAINER,
    Locations.SONG_FROM_IMPA,
    Locations.SHEIK_IN_ICE_CAVERN,
    Locations.BOTTOM_OF_THE_WELL_LENS_OF_TRUTH_CHEST,   # todo MQ lens of truth chest
    Locations.GERUDO_TRAINING_GROUND_MAZE_PATH_FINAL_CHEST # todo MQ ice arrow chest
]

def get_shuffled_songs(world: "SohWorld") -> set[Items]:
    included_songs = set[Items]()
    if not world.options.start_with_zeldas_lullaby:
        included_songs.add(Items.ZELDAS_LULLABY)
    if not world.options.start_with_eponas_song:
        included_songs.add(Items.EPONAS_SONG)
    if not world.options.start_with_sarias_song:
        included_songs.add(Items.SARIAS_SONG)
    if not world.options.start_with_suns_song:
        included_songs.add(Items.SUNS_SONG)
    if not world.options.start_with_song_of_time:
        included_songs.add(Items.SONG_OF_TIME)
    if not world.options.start_with_song_of_storms:
        included_songs.add(Items.SONG_OF_STORMS)
    if not world.options.start_with_minuet:
        included_songs.add(Items.MINUET_OF_FOREST)
    if not world.options.start_with_bolero:
        included_songs.add(Items.BOLERO_OF_FIRE)
    if not world.options.start_with_serenade:
        included_songs.add(Items.SERENADE_OF_WATER)
    if not world.options.start_with_requiem:
        included_songs.add(Items.REQUIEM_OF_SPIRIT)
    if not world.options.start_with_nocturne:
        included_songs.add(Items.NOCTURNE_OF_SHADOW)
    if not world.options.start_with_prelude:
        included_songs.add(Items.PRELUDE_OF_LIGHT)
    return included_songs

def get_prefill_songs(world: "SohWorld") -> list[Items]:
    # Do not prefill songs anywhere in particular
    if world.options.shuffle_songs in ("off", "anywhere"):
        return list()
    
    pre_fill_songs = list[Items]()
    included_songs = get_shuffled_songs(world)
    for song in song_vanilla_locations.values():
        if song not in included_songs:
            continue
        pre_fill_songs.append(song)

    return list(pre_fill_songs)

def reserve_song_locations(world: "SohWorld") -> None:
    if world.options.shuffle_songs in ("off", "anywhere"):
        return
    
    if world.options.shuffle_songs == "song_locations":
        world.reserved_pre_fill_locations += list(song_vanilla_locations.keys())
    if world.options.shuffle_songs == "dungeon_rewards":
        world.reserved_pre_fill_locations += dungeon_reward_song_locations

def remove_song_reservations(world: "SohWorld") -> None:
    song_locations = list(song_vanilla_locations.keys())
    song_locations += dungeon_reward_song_locations
    world.reserved_pre_fill_locations = [loc for loc in world.reserved_pre_fill_locations if loc not in song_locations]

def pre_fill_songs(world: "SohWorld") -> None:
    # Do not prefill songs anywhere in particular
    if world.options.shuffle_songs in ("off", "anywhere"):
        return
    
    remove_song_reservations(world)

    songs = get_prefill_songs(world)
    song_locations = list[Locations]()

    if world.options.shuffle_songs == "song_locations":
        song_locations.extend(song_vanilla_locations.keys())
    elif world.options.shuffle_songs == "dungeon_rewards":
        song_locations.extend(dungeon_reward_song_locations)
    
    world.run_prefill(songs, song_locations)
