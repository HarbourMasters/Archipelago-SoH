from typing import TYPE_CHECKING

from . import SohItem
from .Locations import Locations
from .Items import Items
from .ship_data_gen import SHIP_LOCATIONS, CheckType

if TYPE_CHECKING:
    from . import SohWorld

song_vanilla_locations: dict[Locations, Items] = {
    Locations.RC_SONG_FROM_IMPA: Items.RG_ZELDAS_LULLABY,
    Locations.RC_SONG_FROM_MALON: Items.RG_EPONAS_SONG,
    Locations.RC_SONG_FROM_SARIA: Items.RG_SARIAS_SONG,
    Locations.RC_SONG_FROM_ROYAL_FAMILYS_TOMB: Items.RG_SUNS_SONG,
    Locations.RC_SONG_FROM_OCARINA_OF_TIME: Items.RG_SONG_OF_TIME,
    Locations.RC_SONG_FROM_WINDMILL: Items.RG_SONG_OF_STORMS,
    Locations.RC_SHEIK_IN_FOREST: Items.RG_MINUET_OF_FOREST,
    Locations.RC_SHEIK_IN_CRATER: Items.RG_BOLERO_OF_FIRE,
    Locations.RC_SHEIK_IN_ICE_CAVERN: Items.RG_SERENADE_OF_WATER,
    Locations.RC_SHEIK_IN_KAKARIKO: Items.RG_NOCTURNE_OF_SHADOW,
    Locations.RC_SHEIK_AT_COLOSSUS: Items.RG_REQUIEM_OF_SPIRIT,
    Locations.RC_SHEIK_AT_TEMPLE: Items.RG_PRELUDE_OF_LIGHT
}

dungeon_reward_song_locations: list[Locations] = [Locations.RC_SONG_FROM_IMPA, Locations.RC_SHEIK_IN_ICE_CAVERN] + [
    loc for loc, data in SHIP_LOCATIONS.items() if data.type == CheckType.RCTYPE_BOSS_HEART_OR_OTHER_REWARD
]

def get_shuffled_songs(world: "SohWorld") -> set[Items]:
    included_songs = set[Items]()
    if not world.options.start_with_zeldas_lullaby:
        included_songs.add(Items.RG_ZELDAS_LULLABY)
    if not world.options.start_with_eponas_song:
        included_songs.add(Items.RG_EPONAS_SONG)
    if not world.options.start_with_sarias_song:
        included_songs.add(Items.RG_SARIAS_SONG)
    if not world.options.start_with_suns_song:
        included_songs.add(Items.RG_SUNS_SONG)
    if not world.options.start_with_song_of_time:
        included_songs.add(Items.RG_SONG_OF_TIME)
    if not world.options.start_with_song_of_storms:
        included_songs.add(Items.RG_SONG_OF_STORMS)
    if not world.options.start_with_minuet:
        included_songs.add(Items.RG_MINUET_OF_FOREST)
    if not world.options.start_with_bolero:
        included_songs.add(Items.RG_BOLERO_OF_FIRE)
    if not world.options.start_with_serenade:
        included_songs.add(Items.RG_SERENADE_OF_WATER)
    if not world.options.start_with_requiem:
        included_songs.add(Items.RG_REQUIEM_OF_SPIRIT)
    if not world.options.start_with_nocturne:
        included_songs.add(Items.RG_NOCTURNE_OF_SHADOW)
    if not world.options.start_with_prelude:
        included_songs.add(Items.RG_PRELUDE_OF_LIGHT)
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
