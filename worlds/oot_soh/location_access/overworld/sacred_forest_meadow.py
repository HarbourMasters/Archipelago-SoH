from ...LogicHelpers import *

if TYPE_CHECKING:
    from ... import SohWorld


class EventLocations(StrEnum):
    SFM_GOSSIP_STONE_SONG_FAIRY = "SFM Gossip Stone Song Fairy"
    SFM_FAIRY_FOUNTAIN_FAIRY = "SFM Fairy Fountain Fairy"


def set_region_rules(world: "SohWorld") -> None:
    # SFM Entryway
    # Connections
    connect_regions(Regions.SFM_ENTRYWAY, world, [
        (Regions.LW_BEYOND_MIDO, lambda bundle: True_()),
        (Regions.SACRED_FOREST_MEADOW, lambda bundle: is_adult(
            bundle) | can_kill_enemy(bundle, Enemies.WOLFOS)),
        (Regions.SFM_WOLFOS_GROTTO, lambda bundle: can_open_bomb_grotto(bundle)),
    ])

    # Sacred Forest Meadow
    # Events
    add_events(Regions.SACRED_FOREST_MEADOW, world, [
        (EventLocations.SFM_GOSSIP_STONE_SONG_FAIRY, Events.CAN_ACCESS_FAIRIES,
         lambda bundle: call_gossip_fairy_except_suns(bundle)),
    ])
    # Location
    add_locations(Regions.SACRED_FOREST_MEADOW, world, [
        (Locations.SONG_FROM_SARIA, lambda bundle: is_child(
            bundle) & has_item(Items.ZELDAS_LETTER, bundle)),
        (Locations.SHEIK_IN_FOREST, lambda bundle: is_adult(bundle)),
        (Locations.SFM_GS, lambda bundle: is_adult(bundle)
         & hookshot_or_boomerang(bundle) & can_get_nighttime_gs(bundle)),
        (Locations.SFM_MAZE_LOWER_GOSSIP_STONE_FAIRY,
         lambda bundle: call_gossip_fairy_except_suns(bundle)),
        (Locations.SFM_MAZE_LOWER_GOSSIP_STONE_BIG_FAIRY,
         lambda bundle: can_play_song(Items.SONG_OF_STORMS, bundle)),
        (Locations.SFM_MAZE_UPPER_GOSSIP_STONE_FAIRY,
         lambda bundle: call_gossip_fairy_except_suns(bundle)),
        (Locations.SFM_MAZE_UPPER_GOSSIP_STONE_BIG_FAIRY,
         lambda bundle: can_play_song(Items.SONG_OF_STORMS, bundle)),
        (Locations.SFM_SARIA_GOSSIP_STONE_FAIRY,
         lambda bundle: call_gossip_fairy_except_suns(bundle)),
        (Locations.SFM_SARIA_GOSSIP_STONE_BIG_FAIRY,
         lambda bundle: can_play_song(Items.SONG_OF_STORMS, bundle)),
    ])
    # Connections
    connect_regions(Regions.SACRED_FOREST_MEADOW, world, [
        (Regions.SFM_ENTRYWAY, lambda bundle: True_()),
        (Regions.FOREST_TEMPLE_ENTRYWAY,
         lambda bundle: can_use(Items.HOOKSHOT, bundle)),
        (Regions.SFM_FAIRY_GROTTO, lambda bundle: True_()),
        (Regions.SFM_STORMS_GROTTO, lambda bundle: can_open_storms_grotto(bundle)),
    ])

    # SFM Fairy Grotto
    # Events
    add_events(Regions.SFM_FAIRY_GROTTO, world, [
        (EventLocations.SFM_FAIRY_FOUNTAIN_FAIRY,
         Events.CAN_ACCESS_FAIRIES, lambda bundle: True_()),
    ])
    # Locations
    add_locations(Regions.SFM_FAIRY_GROTTO, world, [
        (Locations.SFM_FAIRY_GROTTO_FAIRY1, lambda bundle: True_()),
        (Locations.SFM_FAIRY_GROTTO_FAIRY2, lambda bundle: True_()),
        (Locations.SFM_FAIRY_GROTTO_FAIRY3, lambda bundle: True_()),
        (Locations.SFM_FAIRY_GROTTO_FAIRY4, lambda bundle: True_()),
        (Locations.SFM_FAIRY_GROTTO_FAIRY5, lambda bundle: True_()),
        (Locations.SFM_FAIRY_GROTTO_FAIRY6, lambda bundle: True_()),
        (Locations.SFM_FAIRY_GROTTO_FAIRY7, lambda bundle: True_()),
        (Locations.SFM_FAIRY_GROTTO_FAIRY8, lambda bundle: True_()),
    ])
    # Connections
    connect_regions(Regions.SFM_FAIRY_GROTTO, world, [
        (Regions.SACRED_FOREST_MEADOW, lambda bundle: True_()),
    ])

    # SFM Wolfos Grotto
    # Locations
    add_locations(Regions.SFM_WOLFOS_GROTTO, world, [
        (Locations.SFM_WOLFOS_GROTTO_CHEST, lambda bundle: can_kill_enemy(
            bundle, Enemies.WOLFOS, EnemyDistance.CLOSE, True, 2)),
    ])
    # Connections
    connect_regions(Regions.SFM_WOLFOS_GROTTO, world, [
        (Regions.SFM_ENTRYWAY, lambda bundle: True_()),
    ])

    # SFM Storms Grotto
    # Locations
    add_locations(Regions.SFM_STORMS_GROTTO, world, [
        (Locations.SFM_DEKU_SCRUB_GROTTO_FRONT,
         lambda bundle: can_stun_deku(bundle) & can_afford_slot(Locations.SFM_DEKU_SCRUB_GROTTO_FRONT, bundle)),
        (Locations.SFM_DEKU_SCRUB_GROTTO_REAR,
         lambda bundle: can_stun_deku(bundle) & can_afford_slot(Locations.SFM_DEKU_SCRUB_GROTTO_REAR, bundle)),
        (Locations.SFM_DEKU_SCRUB_GROTTO_BEEHIVE,
         lambda bundle: can_break_upper_beehives(bundle)),
    ])
    # Connections
    connect_regions(Regions.SFM_STORMS_GROTTO, world, [
        (Regions.SACRED_FOREST_MEADOW, lambda bundle: True_()),
    ])
