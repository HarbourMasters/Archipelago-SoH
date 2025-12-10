from ...LogicHelpers import *
from ...Regions import SohRegion

if TYPE_CHECKING:
    from ... import SohWorld


vanilla_regions: list[Regions] = [
    Regions.DEKU_TREE_ENTRYWAY,
    Regions.DEKU_TREE_LOBBY,
    Regions.DEKU_TREE_2F_MIDDLE_ROOM,
    Regions.DEKU_TREE_SLINGSHOT_ROOM,
    Regions.DEKU_TREE_COMPASS_ROOM,
    Regions.DEKU_TREE_BASEMENT_LOWER,
    Regions.DEKU_TREE_BASEMENT_SCRUB_ROOM,
    Regions.DEKU_TREE_BASEMENT_WATER_ROOM_FRONT,
    Regions.DEKU_TREE_BASEMENT_WATER_ROOM_BACK,
    Regions.DEKU_TREE_BASEMENT_TORCH_ROOM,
    Regions.DEKU_TREE_BASEMENT_BACK_LOBBY,
    Regions.DEKU_TREE_BASEMENT_TORCH_ROOM,
    Regions.DEKU_TREE_BASEMENT_UPPER,
    Regions.DEKU_TREE_OUTSIDE_BOSS_ROOM,
    Regions.DEKU_TREE_BOSS_ENTRYWAY,
    Regions.DEKU_TREE_BOSS_EXIT,
    Regions.DEKU_TREE_BOSS_ROOM,
]

master_quest_regions: list[Regions] = [
    Regions.DEKU_TREE_ENTRYWAY,
    Regions.DEKU_TREE_MQ_1F,
    Regions.DEKU_TREE_MQ_2F,
    Regions.DEKU_TREE_MQ_3F,
    Regions.DEKU_TREE_MQ_EYE_TARGET_ROOM,
    Regions.DEKU_TREE_MQ_COMPASS_ROOM,
    Regions.DEKU_TREE_MQ_PAST_BOULDER_VINES,
    Regions.DEKU_TREE_MQ_BASEMENT,
    Regions.DEKU_TREE_MQ_SOUTHEAST_ROOM,
    Regions.DEKU_TREE_MQ_BASEMENT_WATER_ROOM_FRONT,
    Regions.DEKU_TREE_MQ_BASEMENT_WATER_ROOM_BACK,
    Regions.DEKU_TREE_MQ_BASEMENT_SOUTHWEST_ROOM,
    Regions.DEKU_TREE_MQ_BASEMENT_GRAVE_ROOM,
    Regions.DEKU_TREE_MQ_BASEMENT_BACK_ROOM,
    Regions.DEKU_TREE_MQ_BASEMENT_LEDGE,
    Regions.DEKU_TREE_MQ_OUTSIDE_BOSS_ROOM,
    Regions.DEKU_TREE_BOSS_ENTRYWAY,
    Regions.DEKU_TREE_BOSS_EXIT,
    Regions.DEKU_TREE_BOSS_ROOM,
]


class EventLocations(StrEnum):
    DEKU_TREE_LOBBY_BABA_STICKS = "Deku Tree Lobby Baba Sticks",
    DEKU_TREE_LOBBY_BABA_NUTS = "Deku Tree Lobby Baba Nuts",
    DEKU_TREE_COMPASS_BABA_STICKS = "Deku Tree Compass Room Baba Sticks",
    DEKU_TREE_COMPASS_BABA_NUTS = "Deku Tree Compass Room Baba Nuts",
    DEKU_TREE_BASEMENT_LOWER_BABA_STICKS = "Deku Tree Basement Lower Baba Sticks",
    DEKU_TREE_BASEMENT_LOWER_BABA_NUTS = "Deku Tree Basement Lower Baba Nuts",
    DEKU_TREE_BASEMENT_TORCH_ROOM_BABA_STICKS = "Deku Tree Basement Torch Room Baba Sticks",
    DEKU_TREE_BASEMENT_TORCH_ROOM_BABA_NUTS = "Deku Tree Torch Room Baba Nuts",
    DEKU_TREE_BASEMENT_BACK_LOBBY_BABA_STICKS = "Deku Tree Basement Back Lobby Baba Sticks",
    DEKU_TREE_BASEMENT_BACK_LOBBY_BABA_NUTS = "Deku Tree Basement Back Lobby Baba Nuts",
    DEKU_TREE_BASEMENT_UPPER_BABA_STICKS = "Deku Tree Basement Upper Baba Sticks",
    DEKU_TREE_BASEMENT_UPPER_BABA_NUTS = "Deku Tree Basement Upper Baba Nuts",
    DEKU_TREE_BASEMENT_UPPER_BLOCK = "Deku Tree Basement Upper Push Block",
    DEKU_TREE_MQ_1F_WEB = "Deku Tree MQ 1F Web",
    DEKU_TREE_MQ_1F_DEKU_BABA = "Deku Tree MQ 1F Deku Baba",
    DEKU_TREE_MQ_3F_DEKU_STICKS = "Deku Tree MQ 3F Deku Sticks",
    DEKU_TREE_MQ_3F_DEKU_NUTS = "Deku Tree MQ 3F Deku Nuts",
    DEKU_TREE_MQ_3F_WEB = "Deku Tree MQ 3F Web",
    DEKU_TREE_MQ_BASEMENT_DEKU_BABA_STICKS = "Deku Tree MQ Basement Baba Sticks",
    DEKU_TREE_MQ_BASEMENT_DEKU_BABA_NUTS = "Deku Tree MQ Basement Baba Nuts",
    DEKU_TREE_MQ_BASEMENT_SE_ROOM = "Deku Tree MQ Basement SE Room",
    DEKU_TREE_MQ_WATER_ROOM_TORCHES_FROM_FRONT = "Deku Tree MQ Water Room Torches From Front",
    DEKU_TREE_MQ_WATER_ROOM_TORCHES_FROM_BACK = "Deku Tree MQ Water Room Torches From Back",
    DEKU_TREE_MQ_WATER_ROOM_DEKU_BABA = "Deku Tree MQ Water Room Deku Baba",
    DEKU_TREE_MQ_GRAVE_ROOM_DEKU_BABA_STICKS = "Deku Tree MQ Grave Room Baba Sticks",
    DEKU_TREE_MQ_GRAVE_ROOM_DEKU_BABA_NUTS = "Deku Tree MQ Grave Room Baba Nuts",
    DEKU_TREE_QUEEN_GOHMA = "Deku Tree Queen Gohma"


class LocalEvents(StrEnum):
    DEKU_TREE_BASEMENT_UPPER_BLOCK_PUSHED = "Deku Tree Basement Upper Block Pushed"
    DEKU_TREE_MQ_1F_BROKE_WEB = "Deku Tree MQ 1F Broke Web"
    DEKU_TREE_MQ_CLEARED_SE_ROOM  = "Deku Tree MQ Cleared SE Room"
    DEKU_TREE_MQ_WATER_ROOM_TORCHES = "Deku Tree MQ Water Room Torches",


def set_region_rules(world: "SohWorld", dungeon_quest: DungeonQuest) -> None:
    if dungeon_quest == DungeonQuest.VANILLA:
        set_vanilla_rules(world)
    elif dungeon_quest.MASTER_QUEST:
        set_master_quest_rules(world)


def set_vanilla_rules(world: "SohWorld") -> None:
    # Deku Tree Entryway
    # Connections
    connect_regions(Regions.DEKU_TREE_ENTRYWAY, world, [
        (Regions.DEKU_TREE_LOBBY, lambda bundle: True),
        (Regions.KF_OUTSIDE_DEKU_TREE, lambda bundle: True)
    ])

    # Deku Lobby
    # Events
    add_events(Regions.DEKU_TREE_LOBBY, world, [
        (EventLocations.DEKU_TREE_LOBBY_BABA_STICKS, Events.CAN_FARM_STICKS,
         lambda bundle: can_get_deku_baba_sticks(bundle)),
        (EventLocations.DEKU_TREE_LOBBY_BABA_NUTS, Events.CAN_FARM_NUTS,
         lambda bundle: can_get_deku_baba_nuts(bundle))
    ])
    # Locations
    add_locations(Regions.DEKU_TREE_LOBBY, world, [
        (Locations.DEKU_TREE_MAP_CHEST, lambda bundle: True),
        (Locations.DEKU_TREE_LOBBY_LOWER_HEART, lambda bundle: True),
        (Locations.DEKU_TREE_LOBBY_UPPER_HEART,
         lambda bundle: can_pass_enemy(bundle, Enemies.BIG_SKULLTULA)),
        (Locations.DEKU_TREE_LOBBY_GRASS1, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.DEKU_TREE_LOBBY_GRASS2, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.DEKU_TREE_LOBBY_GRASS3, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.DEKU_TREE_LOBBY_GRASS4, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.DEKU_TREE_LOBBY_GRASS5, lambda bundle: can_cut_shrubs(bundle))
    ])
    # Connections
    connect_regions(Regions.DEKU_TREE_LOBBY, world, [
        (Regions.DEKU_TREE_ENTRYWAY, lambda bundle: True),
        (Regions.DEKU_TREE_2F_MIDDLE_ROOM, lambda bundle: True),
        (Regions.DEKU_TREE_COMPASS_ROOM, lambda bundle: True),
        (Regions.DEKU_TREE_BASEMENT_LOWER, lambda bundle: can_attack(
            bundle) or can_use(Items.NUTS, bundle))
    ])

    # Deku F2 middle room
    # Connections
    connect_regions(Regions.DEKU_TREE_2F_MIDDLE_ROOM, world, [
        (Regions.DEKU_TREE_LOBBY, lambda bundle: can_reflect_nuts(
            bundle) or can_use(Items.MEGATON_HAMMER, bundle)),
        (Regions.DEKU_TREE_SLINGSHOT_ROOM, lambda bundle: can_reflect_nuts(
            bundle) or can_use(Items.MEGATON_HAMMER, bundle))
    ])

    # Deku slingshot room
    # Locations
    add_locations(Regions.DEKU_TREE_SLINGSHOT_ROOM, world, [
        (Locations.DEKU_TREE_SLINGSHOT_CHEST, lambda bundle: True),
        (Locations.DEKU_TREE_SLINGSHOT_ROOM_SIDE_CHEST, lambda bundle: True),
        (Locations.DEKU_TREE_SLINGSHOT_GRASS1, lambda bundle: can_cut_shrubs(
            bundle) and can_reflect_nuts(bundle)),
        (Locations.DEKU_TREE_SLINGSHOT_GRASS2, lambda bundle: can_cut_shrubs(
            bundle) and can_reflect_nuts(bundle)),
        (Locations.DEKU_TREE_SLINGSHOT_GRASS3, lambda bundle: can_cut_shrubs(
            bundle) and can_reflect_nuts(bundle)),
        (Locations.DEKU_TREE_SLINGSHOT_GRASS4, lambda bundle: can_cut_shrubs(
            bundle) and can_reflect_nuts(bundle))
    ])
    # Connections
    connect_regions(Regions.DEKU_TREE_SLINGSHOT_ROOM, world, [
        (Regions.DEKU_TREE_2F_MIDDLE_ROOM, lambda bundle: can_use(
            Items.FAIRY_SLINGSHOT, bundle) or can_use(Items.HOVER_BOOTS, bundle))
    ])

    # Deku compass room
    # Events
    add_events(Regions.DEKU_TREE_COMPASS_ROOM, world, [
        (EventLocations.DEKU_TREE_COMPASS_BABA_STICKS, Events.CAN_FARM_STICKS,
         lambda bundle: can_get_deku_baba_sticks(bundle)),
        (EventLocations.DEKU_TREE_COMPASS_BABA_NUTS, Events.CAN_FARM_NUTS,
         lambda bundle: can_get_deku_baba_nuts(bundle))
    ])
    # Locations
    add_locations(Regions.DEKU_TREE_COMPASS_ROOM, world, [
        (Locations.DEKU_TREE_COMPASS_CHEST, lambda bundle: True),
        (Locations.DEKU_TREE_COMPASS_ROOM_SIDE_CHEST, lambda bundle: True),
        (Locations.DEKU_TREE_GS_COMPASS_ROOM,
         lambda bundle: can_kill_enemy(bundle, Enemies.GOLD_SKULLTULA)),
        (Locations.DEKU_TREE_COMPASS_GRASS1, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.DEKU_TREE_COMPASS_GRASS2, lambda bundle: can_cut_shrubs(bundle))
    ])
    # Connections
    connect_regions(Regions.DEKU_TREE_COMPASS_ROOM, world, [
        (Regions.DEKU_TREE_LOBBY, lambda bundle: has_fire_source_with_torch(bundle))
    ])

    # Deku Basement Lower
    # Events
    add_events(Regions.DEKU_TREE_BASEMENT_LOWER, world, [
        (EventLocations.DEKU_TREE_BASEMENT_LOWER_BABA_STICKS,
         Events.CAN_FARM_STICKS, lambda bundle: can_get_deku_baba_sticks(bundle)),
        (EventLocations.DEKU_TREE_BASEMENT_LOWER_BABA_NUTS,
         Events.CAN_FARM_NUTS, lambda bundle: can_get_deku_baba_nuts(bundle))
    ])
    # Locations
    add_locations(Regions.DEKU_TREE_BASEMENT_LOWER, world, [
        (Locations.DEKU_TREE_BASEMENT_CHEST, lambda bundle: True),
        (Locations.DEKU_TREE_GS_BASEMENT_GATE, lambda bundle: can_kill_enemy(
            bundle, Enemies.GOLD_SKULLTULA, EnemyDistance.SHORT_JUMPSLASH)),
        (Locations.DEKU_TREE_GS_BASEMENT_VINES, lambda bundle: can_kill_enemy(
            bundle, Enemies.GOLD_SKULLTULA, EnemyDistance.SHORT_JUMPSLASH)),
        (Locations.DEKU_TREE_BASEMENT_GRASS1,
         lambda bundle: can_cut_shrubs(bundle)),
        (Locations.DEKU_TREE_BASEMENT_GRASS2,
         lambda bundle: can_cut_shrubs(bundle))
    ])
    # Connections
    connect_regions(Regions.DEKU_TREE_BASEMENT_LOWER, world, [
        (Regions.DEKU_TREE_LOBBY, lambda bundle: True),
        (Regions.DEKU_TREE_BASEMENT_SCRUB_ROOM, lambda bundle: has_fire_source_with_torch(
            bundle) or can_use(Items.FAIRY_BOW, bundle)),
        (Regions.DEKU_TREE_BASEMENT_UPPER, lambda bundle: is_adult(bundle) or can_do_trick(Tricks.DEKU_B1_SKIP, bundle)
            or has_item(LocalEvents.DEKU_TREE_BASEMENT_UPPER_BLOCK_PUSHED, bundle) or can_ground_jump(bundle))
    ])

    # Deku basement shrub room
    # Locations
    add_locations(Regions.DEKU_TREE_BASEMENT_SCRUB_ROOM, world, [
        (Locations.DEKU_TREE_EYE_SWITCH_GRASS1,
         lambda bundle: can_cut_shrubs(bundle)),
        (Locations.DEKU_TREE_EYE_SWITCH_GRASS2,
         lambda bundle: can_cut_shrubs(bundle)),
        (Locations.DEKU_TREE_EYE_SWITCH_GRASS3,
         lambda bundle: can_cut_shrubs(bundle)),
        (Locations.DEKU_TREE_EYE_SWITCH_GRASS4,
         lambda bundle: can_cut_shrubs(bundle))
    ])
    # Connections
    connect_regions(Regions.DEKU_TREE_BASEMENT_SCRUB_ROOM, world, [
        (Regions.DEKU_TREE_BASEMENT_LOWER, lambda bundle: True),
        (Regions.DEKU_TREE_BASEMENT_WATER_ROOM_FRONT,
         lambda bundle: can_hit_eye_targets(bundle))
    ])

    # Deku basement water room front
    # Connections
    connect_regions(Regions.DEKU_TREE_BASEMENT_WATER_ROOM_FRONT, world, [
        (Regions.DEKU_TREE_BASEMENT_SCRUB_ROOM, lambda bundle: True),
        (Regions.DEKU_TREE_BASEMENT_WATER_ROOM_BACK, lambda bundle: has_item(
            Items.BRONZE_SCALE, bundle) or can_do_trick(Tricks.DEKU_B1_BACKFLIP_OVER_SPIKED_LOG, bundle)),
    ])

    # Deku basement water room back
    # Locations
    add_locations(Regions.DEKU_TREE_BASEMENT_WATER_ROOM_BACK, world, [
        (Locations.DEKU_TREE_SPIKE_ROLLER_GRASS1,
         lambda bundle: can_cut_shrubs(bundle)),
        (Locations.DEKU_TREE_SPIKE_ROLLER_GRASS2,
         lambda bundle: can_cut_shrubs(bundle))
    ])
    # Connections
    connect_regions(Regions.DEKU_TREE_BASEMENT_WATER_ROOM_BACK, world, [
        (Regions.DEKU_TREE_BASEMENT_WATER_ROOM_FRONT, lambda bundle: has_item(
            Items.BRONZE_SCALE, bundle) or can_do_trick(Tricks.DEKU_B1_BACKFLIP_OVER_SPIKED_LOG, bundle)),
        (Regions.DEKU_TREE_BASEMENT_TORCH_ROOM, lambda bundle: True)
    ])

    # Deku tree basement torch room
    # Events
    add_events(Regions.DEKU_TREE_BASEMENT_TORCH_ROOM, world, [
        (EventLocations.DEKU_TREE_BASEMENT_TORCH_ROOM_BABA_STICKS,
         Events.CAN_FARM_STICKS, lambda bundle: can_get_deku_baba_sticks(bundle)),
        (EventLocations.DEKU_TREE_BASEMENT_TORCH_ROOM_BABA_NUTS,
         Events.CAN_FARM_NUTS, lambda bundle: can_get_deku_baba_nuts(bundle))
    ])
    # Locations
    add_locations(Regions.DEKU_TREE_BASEMENT_TORCH_ROOM, world, [
        (Locations.DEKU_TREE_TORCHES_GRASS1, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.DEKU_TREE_TORCHES_GRASS2, lambda bundle: can_cut_shrubs(bundle))
    ])
    # Connections
    connect_regions(Regions.DEKU_TREE_BASEMENT_TORCH_ROOM, world, [
        (Regions.DEKU_TREE_BASEMENT_WATER_ROOM_BACK, lambda bundle: has_fire_source_with_torch(
            bundle) or can_use(Items.FAIRY_BOW, bundle)),
        (Regions.DEKU_TREE_BASEMENT_BACK_LOBBY, lambda bundle: has_fire_source_with_torch(
            bundle) or can_use(Items.FAIRY_BOW, bundle))
    ])

    # Deku basement back lobby
    # Events
    add_events(Regions.DEKU_TREE_BASEMENT_BACK_LOBBY, world, [
        (EventLocations.DEKU_TREE_BASEMENT_BACK_LOBBY_BABA_STICKS,
         Events.CAN_FARM_STICKS, lambda bundle: can_get_deku_baba_sticks(bundle)),
        (EventLocations.DEKU_TREE_BASEMENT_BACK_LOBBY_BABA_NUTS,
         Events.CAN_FARM_NUTS, lambda bundle: can_get_deku_baba_nuts(bundle))
    ])
    # Locations
    add_locations(Regions.DEKU_TREE_BASEMENT_BACK_LOBBY, world, [
        (Locations.DEKU_TREE_LARVAE_GRASS1, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.DEKU_TREE_LARVAE_GRASS2, lambda bundle: can_cut_shrubs(bundle))
    ])
    # Connections
    connect_regions(Regions.DEKU_TREE_BASEMENT_BACK_LOBBY, world, [
        (Regions.DEKU_TREE_BASEMENT_TORCH_ROOM, lambda bundle: True),
        (Regions.DEKU_TREE_BASEMENT_BACK_ROOM, lambda bundle: (
            has_fire_source_with_torch(bundle) or can_use(Items.FAIRY_BOW, bundle))),
        (Regions.DEKU_TREE_BASEMENT_UPPER, lambda bundle: (
            has_fire_source_with_torch(bundle) or can_use(Items.FAIRY_BOW, bundle))),
    ])

    # Deku basement back room
    # Locations
    add_locations(Regions.DEKU_TREE_BASEMENT_BACK_ROOM, world, [
        (Locations.DEKU_TREE_GS_BASEMENT_BACK_ROOM,
         lambda bundle: hookshot_or_boomerang(bundle)),

    ])
    # Connections
    connect_regions(Regions.DEKU_TREE_BASEMENT_BACK_ROOM, world, [
        (Regions.DEKU_TREE_BASEMENT_BACK_LOBBY, lambda bundle: True),
    ])

    # Deku basement upper
    # Events
    add_events(Regions.DEKU_TREE_BASEMENT_UPPER, world, [
        (EventLocations.DEKU_TREE_BASEMENT_UPPER_BABA_STICKS,
         Events.CAN_FARM_STICKS, lambda bundle: can_get_deku_baba_sticks(bundle)),
        (EventLocations.DEKU_TREE_BASEMENT_UPPER_BABA_NUTS,
         Events.CAN_FARM_NUTS, lambda bundle: can_get_deku_baba_nuts(bundle)),
        (EventLocations.DEKU_TREE_BASEMENT_UPPER_BLOCK,
         LocalEvents.DEKU_TREE_BASEMENT_UPPER_BLOCK_PUSHED, lambda bundle: True)
    ])
    # Connections
    connect_regions(Regions.DEKU_TREE_BASEMENT_UPPER, world, [
        (Regions.DEKU_TREE_BASEMENT_LOWER, lambda bundle: True),
        (Regions.DEKU_TREE_BASEMENT_BACK_LOBBY, lambda bundle: is_child(bundle)),
        (Regions.DEKU_TREE_OUTSIDE_BOSS_ROOM, lambda bundle: has_fire_source_with_torch(bundle) or
         (can_do_trick(Tricks.DEKU_B1_BOW_WEBS, bundle) and is_adult(bundle) and can_use(Items.FAIRY_BOW, bundle)))
    ])

    # Deku outside boss room
    # Locations
    add_locations(Regions.DEKU_TREE_OUTSIDE_BOSS_ROOM, world, [
        (Locations.DEKU_TREE_FINAL_ROOM_LEFT_FRONT_HEART, lambda bundle: has_item(Items.BRONZE_SCALE,
         bundle) or can_use(Items.IRON_BOOTS, bundle) or can_use(Items.IRON_BOOTS, bundle)),
        (Locations.DEKU_TREE_FINAL_ROOM_LEFT_BACK_HEART, lambda bundle: has_item(Items.BRONZE_SCALE,
         bundle) or can_use(Items.IRON_BOOTS, bundle) or can_use(Items.IRON_BOOTS, bundle)),
        (Locations.DEKU_TREE_FINAL_ROOM_RIGHT_HEART, lambda bundle: has_item(Items.BRONZE_SCALE,
         bundle) or can_use(Items.IRON_BOOTS, bundle) or can_use(Items.IRON_BOOTS, bundle)),
        (Locations.DEKU_TREE_BEFORE_BOSS_GRASS1, lambda bundle: can_cut_shrubs(
            bundle) and has_fire_source_with_torch(bundle)),
        (Locations.DEKU_TREE_BEFORE_BOSS_GRASS2, lambda bundle: can_cut_shrubs(
            bundle) and has_fire_source_with_torch(bundle)),
        (Locations.DEKU_TREE_BEFORE_BOSS_GRASS3, lambda bundle: can_cut_shrubs(
            bundle) and has_fire_source_with_torch(bundle))
    ])
    # Connections
    connect_regions(Regions.DEKU_TREE_OUTSIDE_BOSS_ROOM, world, [
        (Regions.DEKU_TREE_BASEMENT_UPPER, lambda bundle: True),
        (Regions.DEKU_TREE_BOSS_ENTRYWAY, lambda bundle: (has_item(Items.BRONZE_SCALE, bundle) or can_use(Items.IRON_BOOTS, bundle))
            and can_reflect_nuts(bundle))
    ])

    # Skipping master quest for now

    # Deku Boss room entryway
    # Connections
    connect_regions(Regions.DEKU_TREE_BOSS_ENTRYWAY, world, [
        (Regions.DEKU_TREE_BOSS_ROOM, lambda bundle: True)
    ])

    # Deku boss exit
    # Connections
    connect_regions(Regions.DEKU_TREE_BOSS_EXIT, world, [
        (Regions.DEKU_TREE_OUTSIDE_BOSS_ROOM, lambda bundle: True),
        # skipping mq connection
    ])

    # Deku Tree boss room
    # Events
    add_events(Regions.DEKU_TREE_BOSS_ROOM, world, [
        (EventLocations.DEKU_TREE_QUEEN_GOHMA, Events.DEKU_TREE_COMPLETED,
         lambda bundle: can_kill_enemy(bundle, Enemies.GOHMA))
    ])
    # Locations
    add_locations(Regions.DEKU_TREE_BOSS_ROOM, world, [
        (Locations.QUEEN_GOHMA, lambda bundle: has_item(
            Events.DEKU_TREE_COMPLETED, bundle)),
        (Locations.DEKU_TREE_QUEEN_GOHMA_HEART_CONTAINER,
         lambda bundle: has_item(Events.DEKU_TREE_COMPLETED, bundle)),
        (Locations.DEKU_TREE_QUEEN_GOHMA_GRASS1,
         lambda bundle: can_cut_shrubs(bundle)),
        (Locations.DEKU_TREE_QUEEN_GOHMA_GRASS2,
         lambda bundle: can_cut_shrubs(bundle)),
        (Locations.DEKU_TREE_QUEEN_GOHMA_GRASS3,
         lambda bundle: can_cut_shrubs(bundle)),
        (Locations.DEKU_TREE_QUEEN_GOHMA_GRASS4,
         lambda bundle: can_cut_shrubs(bundle)),
        (Locations.DEKU_TREE_QUEEN_GOHMA_GRASS5,
         lambda bundle: can_cut_shrubs(bundle)),
        (Locations.DEKU_TREE_QUEEN_GOHMA_GRASS6,
         lambda bundle: can_cut_shrubs(bundle)),
        (Locations.DEKU_TREE_QUEEN_GOHMA_GRASS7,
         lambda bundle: can_cut_shrubs(bundle)),
        (Locations.DEKU_TREE_QUEEN_GOHMA_GRASS8,
         lambda bundle: can_cut_shrubs(bundle))
    ])
    # Connections
    connect_regions(Regions.DEKU_TREE_BOSS_ROOM, world, [
        (Regions.DEKU_TREE_BOSS_EXIT, lambda bundle: True),
        (Regions.KF_OUTSIDE_DEKU_TREE, lambda bundle: has_item(
            Events.DEKU_TREE_COMPLETED, bundle))
    ])


def set_master_quest_rules(world: "SohWorld") -> None:
    # Deku Tree Entryway
    # Connections
    connect_regions(Regions.DEKU_TREE_ENTRYWAY, world, [
        (Regions.DEKU_TREE_MQ_1F, lambda bundle: True),
        (Regions.KF_OUTSIDE_DEKU_TREE, lambda bundle: True),
    ])

    # Deku Tree MQ 1F
    # Events
    add_events(Regions.DEKU_TREE_MQ_1F, world, [
        (EventLocations.DEKU_TREE_MQ_1F_DEKU_BABA, Events.CAN_FARM_STICKS, lambda bundle: can_kill_enemy(bundle, Enemies.WITHERED_DEKU_BABA)),
        (EventLocations.DEKU_TREE_MQ_1F_WEB, LocalEvents.DEKU_TREE_MQ_1F_BROKE_WEB, lambda bundle: has_fire_source(bundle)),
    ])
    # Locations
    add_locations(Regions.DEKU_TREE_MQ_1F, world, [
        (Locations.DEKU_TREE_MQ_LOBBY_GRASS1, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.DEKU_TREE_MQ_LOBBY_GRASS2, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.DEKU_TREE_MQ_LOBBY_GRASS3, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.DEKU_TREE_MQ_LOBBY_GRASS4, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.DEKU_TREE_MQ_LOBBY_GRASS5, lambda bundle: can_cut_shrubs(bundle)),
    ])
    # Connections
    connect_regions(Regions.DEKU_TREE_MQ_1F, world, [
        (Regions.DEKU_TREE_ENTRYWAY, lambda bundle: True),
        (Regions.DEKU_TREE_MQ_2F, lambda bundle: True),
        (Regions.DEKU_TREE_MQ_BASEMENT, lambda bundle: has_item(LocalEvents.DEKU_TREE_MQ_1F_BROKE_WEB, bundle)),
    ])

    # Deku Tree MQ 2F
    # Locations
    add_locations(Regions.DEKU_TREE_MQ_2F, world, [
        (Locations.DEKU_TREE_MQ_MAP_CHEST, lambda bundle: True),
        (Locations.DEKU_TREE_MQ_GS_LOBBY, lambda bundle: can_get_enemy_drop(bundle, Enemies.GOLD_SKULLTULA)),
        (Locations.DEKU_TREE_MQ_LOBBY_HEART, lambda bundle: True),
        (Locations.DEKU_TREE_MQ_LOBBY_GRASS6, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.DEKU_TREE_MQ_LOBBY_GRASS7, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.DEKU_TREE_MQ_LOBBY_HEART, lambda bundle: can_break_crates(bundle)),
    ])
    # Connections
    connect_regions(Regions.DEKU_TREE_MQ_2F, world, [
        (Regions.DEKU_TREE_MQ_1F, lambda bundle: True),
        (Regions.DEKU_TREE_MQ_3F, lambda bundle: True),
        (Regions.DEKU_TREE_MQ_EYE_TARGET_ROOM, lambda bundle: has_fire_source(bundle)),
    ])

    # Deku Tree MQ 3F
    # Events
    add_events(Regions.DEKU_TREE_MQ_3F, world, [
        (EventLocations.DEKU_TREE_MQ_3F_DEKU_STICKS, Events.CAN_FARM_STICKS, lambda bundle: can_get_deku_baba_sticks(bundle)),
        (EventLocations.DEKU_TREE_MQ_3F_DEKU_NUTS, Events.CAN_FARM_NUTS, lambda bundle: can_get_deku_baba_nuts(bundle)),
        (EventLocations.DEKU_TREE_MQ_3F_WEB, LocalEvents.DEKU_TREE_MQ_1F_BROKE_WEB, lambda bundle: True),
    ])
    # Locations
    add_locations(Regions.DEKU_TREE_MQ_3F, world, [
        (Locations.DEKU_TREE_MQ_SLINGSHOT_CHEST, lambda bundle: can_kill_enemy(bundle, Enemies.DEKU_BABA)),
        (Locations.DEKU_TREE_MQ_SLINGSHOT_ROOM_BACK_CHEST, lambda bundle: has_fire_source_with_torch(bundle) or (is_adult(bundle) and can_use(Items.FAIRY_BOW, bundle))),
        (Locations.DEKU_TREE_MQ_SLINGSHOT_ROOM_HEART, lambda bundle: True),
        (Locations.DEKU_TREE_MQ_SLINGSHOT_GRASS1, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.DEKU_TREE_MQ_SLINGSHOT_GRASS2, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.DEKU_TREE_MQ_SLINGSHOT_GRASS3, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.DEKU_TREE_MQ_SLINGSHOT_GRASS4, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.DEKU_TREE_MQ_SLINGSHOT_ROOM_CRATE1, lambda bundle: can_break_crates(bundle)),
        (Locations.DEKU_TREE_MQ_SLINGSHOT_ROOM_CRATE2, lambda bundle: can_break_crates(bundle)),
    ])
    # Connections
    connect_regions(Regions.DEKU_TREE_MQ_3F, world, [
        (Regions.DEKU_TREE_MQ_2F, lambda bundle: True),
        (Regions.DEKU_TREE_MQ_EYE_TARGET_ROOM, lambda bundle: can_use(Items.STICKS, bundle) or can_use(Items.FAIRY_BOW, bundle)),
        (Regions.DEKU_TREE_MQ_BASEMENT, lambda bundle: True),
    ])

    # Deku Tree MQ Eye Target Room
    # Locations
    add_locations(Regions.DEKU_TREE_MQ_EYE_TARGET_ROOM, world, [
        (Locations.DEKU_TREE_MQ_DEKU_BABA_HEART, lambda bundle: True),
        (Locations.DEKU_TREE_MQ_BEFORE_COMPASS_GRASS1, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.DEKU_TREE_MQ_BEFORE_COMPASS_GRASS2, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.DEKU_TREE_MQ_BEFORE_COMPASS_GRASS3, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.DEKU_TREE_MQ_BEFORE_COMPASS_GRASS4, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.DEKU_TREE_MQ_BEFORE_COMPASS_GRASS5, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.DEKU_TREE_MQ_BEFORE_COMPASS_GRASS6, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.DEKU_TREE_MQ_BEFORE_COMPASS_GRASS7, lambda bundle: can_cut_shrubs(bundle)),
    ])
    # Connections
    connect_regions(Regions.DEKU_TREE_MQ_EYE_TARGET_ROOM, world, [
        (Regions.DEKU_TREE_MQ_COMPASS_ROOM, lambda bundle: can_hit_eye_targets(bundle)),
        (Regions.DEKU_TREE_MQ_2F, lambda bundle: True),
    ])

    # Deku Tree MQ Compass Room
    # Locations
    add_locations(Regions.DEKU_TREE_MQ_COMPASS_ROOM, world, [
        (Locations.DEKU_TREE_MQ_COMPASS_CHEST, lambda bundle: True),
        (Locations.DEKU_TREE_MQ_COMPASS_GRASS1, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.DEKU_TREE_MQ_COMPASS_GRASS2, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.DEKU_TREE_MQ_COMPASS_GRASS3, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.DEKU_TREE_MQ_COMPASS_GRASS4, lambda bundle: can_cut_shrubs(bundle)),
    ])
    # Connections
    connect_regions(Regions.DEKU_TREE_MQ_COMPASS_ROOM, world, [
        (Regions.DEKU_TREE_MQ_EYE_TARGET_ROOM, lambda bundle: can_use(Items.FAIRY_SLINGSHOT, bundle) or can_use(Items.HOVER_BOOTS, bundle)),
        (Regions.DEKU_TREE_MQ_PAST_BOULDER_VINES, lambda bundle: can_use(Items.BOMBCHUS_5, bundle) or  (can_use(Items.BOMB_BAG, bundle) and (can_use(Items.SONG_OF_TIME, bundle) or is_adult(bundle) or can_use(Items.HOVER_BOOTS, bundle))) or (can_use(Items.MEGATON_HAMMER, bundle) and (can_use(Items.SONG_OF_TIME, bundle) or can_do_trick(Tricks.DEKU_MQ_COMPASS_GS, bundle)))),
    ])

    # Deku Tree MQ Past Boulder Vines
    # Locations
    add_locations(Regions.DEKU_TREE_MQ_PAST_BOULDER_VINES, world, [
        (Locations.DEKU_TREE_MQ_GS_PAST_BOULDER_VINES, lambda bundle: can_get_enemy_drop(bundle, Enemies.GOLD_SKULLTULA, EnemyDistance.BOOMERANG)),
        (Locations.DEKU_TREE_MQ_COMPASS_ROOM_HEART, lambda bundle: True),
    ])
    # Connections
    connect_regions(Regions.DEKU_TREE_MQ_PAST_BOULDER_VINES, world, [
        (Regions.DEKU_TREE_MQ_COMPASS_ROOM, lambda bundle: blast_or_smash(bundle)),
    ])

    # Deku Tree MQ Basement
    # Events
    add_events(Regions.DEKU_TREE_MQ_BASEMENT, world, [
        (EventLocations.DEKU_TREE_MQ_BASEMENT_DEKU_BABA_STICKS, Events.CAN_FARM_STICKS, lambda bundle: can_get_deku_baba_sticks(bundle)),
        (EventLocations.DEKU_TREE_MQ_BASEMENT_DEKU_BABA_NUTS, Events.CAN_FARM_NUTS, lambda bundle: can_get_deku_baba_nuts(bundle)),
    ])
    # Locations
    add_locations(Regions.DEKU_TREE_MQ_BASEMENT, world, [
        (Locations.DEKU_TREE_MQ_BASEMENT_CHEST, lambda bundle: has_fire_source_with_torch(bundle) or can_use(Items.FAIRY_BOW, bundle)),
        (Locations.DEKU_TREE_MQ_BASEMENT_LOWER_GRASS1, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.DEKU_TREE_MQ_BASEMENT_LOWER_GRASS2, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.DEKU_TREE_MQ_BASEMENT_LOWER_GRASS3, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.DEKU_TREE_MQ_BASEMENT_LOWER_GRASS4, lambda bundle: can_cut_shrubs(bundle)),
    ])
    # Connections
    connect_regions(Regions.DEKU_TREE_MQ_BASEMENT, world, [
        (Regions.DEKU_TREE_MQ_1F, lambda bundle: True),
        (Regions.DEKU_TREE_MQ_SOUTHEAST_ROOM, lambda bundle: can_hit_eye_targets(bundle)),
        (Regions.DEKU_TREE_MQ_BASEMENT_WATER_ROOM_FRONT, lambda bundle: can_hit_eye_targets(bundle) and has_item(LocalEvents.DEKU_TREE_MQ_CLEARED_SE_ROOM, bundle) and can_use(Items.STICKS, bundle)),
        (Regions.DEKU_TREE_MQ_BASEMENT_LEDGE, lambda bundle: is_adult(bundle) or can_do_trick(Tricks.DEKU_B1_SKIP, bundle) or can_ground_jump(bundle) or has_item(LocalEvents.DEKU_TREE_BASEMENT_UPPER_BLOCK_PUSHED, bundle) or can_use(Items.HOVER_BOOTS, bundle)),
    ])

    # Deku Tree MQ Southeast Room
    # Events
    add_events(Regions.DEKU_TREE_MQ_SOUTHEAST_ROOM, world, [
        (EventLocations.DEKU_TREE_MQ_BASEMENT_SE_ROOM, LocalEvents.DEKU_TREE_MQ_CLEARED_SE_ROOM, lambda bundle: can_kill_enemy(bundle, Enemies.MAD_SCRUB)),
    ])
    # Locations
    add_locations(Regions.DEKU_TREE_MQ_BASEMENT, world, [
        (Locations.DEKU_TREE_MQ_TORCHES_GRASS1, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.DEKU_TREE_MQ_TORCHES_GRASS2, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.DEKU_TREE_MQ_TORCHES_GRASS3, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.DEKU_TREE_MQ_TORCHES_GRASS4, lambda bundle: can_cut_shrubs(bundle)),
    ])
    # Connections
    connect_regions(Regions.DEKU_TREE_MQ_SOUTHEAST_ROOM, world, [
        (Regions.DEKU_TREE_MQ_BASEMENT_WATER_ROOM_FRONT, lambda bundle: has_fire_source(bundle)),
        (Regions.DEKU_TREE_MQ_BASEMENT, lambda bundle: has_item(LocalEvents.DEKU_TREE_MQ_CLEARED_SE_ROOM, bundle)),
    ])

    # Deku Tree MQ Basement Water Room Front
    # Events
    add_events(Regions.DEKU_TREE_MQ_BASEMENT_WATER_ROOM_FRONT, world, [
        (EventLocations.DEKU_TREE_MQ_WATER_ROOM_TORCHES_FROM_FRONT, LocalEvents.DEKU_TREE_MQ_WATER_ROOM_TORCHES, lambda bundle: can_use(Items.FIRE_ARROW, bundle) or (can_use(Items.STICKS, bundle) and (can_do_trick(Tricks.DEKU_MQ_LOG, bundle) or (is_child(bundle) and can_shield(bundle))))),
    ])
    # Locations
    add_locations(Regions.DEKU_TREE_MQ_BASEMENT_WATER_ROOM_FRONT, world, [
        (Locations.DEKU_TREE_MQ_AFTER_SPINNING_LOG_CHEST, lambda bundle: True),
        (Locations.DEKU_TREE_MQ_SPIKE_ROLLER_FRONT_GRASS1, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.DEKU_TREE_MQ_SPIKE_ROLLER_FRONT_GRASS2, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.DEKU_TREE_MQ_SPIKE_ROLLER_FRONT_GRASS3, lambda bundle: can_cut_shrubs(bundle)),
    ])
    # Connections
    connect_regions(Regions.DEKU_TREE_MQ_BASEMENT_WATER_ROOM_FRONT, world, [
        (Regions.DEKU_TREE_MQ_BASEMENT_WATER_ROOM_BACK, lambda bundle: can_do_trick(Tricks.DEKU_MQ_LOG, bundle) or (is_child(bundle) and can_shield(bundle)) or can_use(Items.LONGSHOT, bundle) or (can_use(Items.HOOKSHOT, bundle) and can_use(Items.IRON_BOOTS, bundle))),
        (Regions.DEKU_TREE_MQ_SOUTHEAST_ROOM, lambda bundle: True),
    ])

    # Deku Tree MQ Basement Water Room Back
    # Events
    add_events(Regions.DEKU_TREE_MQ_BASEMENT_WATER_ROOM_BACK, world, [
        (EventLocations.DEKU_TREE_MQ_WATER_ROOM_DEKU_BABA, Events.CAN_FARM_STICKS, lambda bundle: can_kill_enemy(bundle, Enemies.WITHERED_DEKU_BABA)),
        (EventLocations.DEKU_TREE_MQ_WATER_ROOM_TORCHES_FROM_BACK, LocalEvents.DEKU_TREE_MQ_WATER_ROOM_TORCHES, lambda bundle: has_fire_source(bundle)),
    ])
    # Locations
    add_locations(Regions.DEKU_TREE_MQ_BASEMENT_WATER_ROOM_BACK, world, [
        (Locations.DEKU_TREE_MQ_AFTER_SPINNING_LOG_CHEST, lambda bundle: can_use(Items.SONG_OF_STORMS, bundle) and can_pass_enemy(bundle, Enemies.BIG_SKULLTULA)),
        (Locations.DEKU_TREE_MQ_SPIKE_ROLLER_BACK_GRASS1, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.DEKU_TREE_MQ_SPIKE_ROLLER_BACK_GRASS2, lambda bundle: can_cut_shrubs(bundle)),
    ])
    # Connections
    connect_regions(Regions.DEKU_TREE_MQ_BASEMENT_WATER_ROOM_BACK, world, [
        (Regions.DEKU_TREE_MQ_BASEMENT_SOUTHWEST_ROOM, lambda bundle: has_item(LocalEvents.DEKU_TREE_MQ_WATER_ROOM_TORCHES, bundle) and can_pass_enemy(bundle, Enemies.BIG_SKULLTULA, EnemyDistance.CLOSE if can_use(Items.SONG_OF_TIME, bundle) else EnemyDistance.SHORT_JUMPSLASH)),
        (Regions.DEKU_TREE_MQ_BASEMENT_WATER_ROOM_FRONT, lambda bundle: can_do_trick(Tricks.DEKU_MQ_LOG, bundle) or (is_child(bundle) and can_shield(bundle)) or can_use(Items.LONGSHOT, bundle) or has_item(Items.BRONZE_SCALE, bundle) or (can_use(Items.IRON_BOOTS, bundle) and (is_adult(bundle) or can_use(Items.HOOKSHOT, bundle)))),
    ])

    # Deku Tree MQ Basement Southwest Room
    # Locations
    add_locations(Regions.DEKU_TREE_MQ_BASEMENT_SOUTHWEST_ROOM, world, [
        (Locations.DEKU_TREE_MQ_LARVAE_GRASS1, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.DEKU_TREE_MQ_LARVAE_GRASS2, lambda bundle: can_cut_shrubs(bundle)),
    ])
    # Connections
    connect_regions(Regions.DEKU_TREE_MQ_BASEMENT_SOUTHWEST_ROOM, world, [
        (Regions.DEKU_TREE_MQ_BASEMENT_GRAVE_ROOM, lambda bundle: can_kill_enemy(bundle, Enemies.MAD_SCRUB) and can_kill_enemy(bundle, Enemies.KEESE)),
        (Regions.DEKU_TREE_MQ_BASEMENT_WATER_ROOM_FRONT, lambda bundle: can_kill_enemy(bundle, Enemies.MAD_SCRUB) and can_kill_enemy(bundle, Enemies.KEESE)),
    ])

    # Deku Tree MQ Basement Grave Room
    # Events
    add_events(Regions.DEKU_TREE_MQ_BASEMENT_GRAVE_ROOM, world, [
        (EventLocations.DEKU_TREE_MQ_GRAVE_ROOM_DEKU_BABA_STICKS, Events.CAN_FARM_STICKS, lambda bundle: can_get_deku_baba_sticks(bundle)),
        (EventLocations.DEKU_TREE_MQ_GRAVE_ROOM_DEKU_BABA_NUTS, Events.CAN_FARM_NUTS, lambda bundle: can_get_deku_baba_nuts(bundle)),
    ])
    # Locations
    add_locations(Regions.DEKU_TREE_MQ_BASEMENT_GRAVE_ROOM, world, [
        (Locations.DEKU_TREE_MQ_GS_BASEMENT_GRAVES_ROOM, lambda bundle: can_use(Items.LONGSHOT, bundle) or (can_use(Items.SONG_OF_TIME, bundle) and can_get_enemy_drop(bundle, Enemies.GOLD_SKULLTULA, EnemyDistance.BOOMERANG))),
        (Locations.DEKU_TREE_MQ_GRAVES_GRASS1, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.DEKU_TREE_MQ_GRAVES_GRASS2, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.DEKU_TREE_MQ_GRAVES_GRASS3, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.DEKU_TREE_MQ_GRAVES_GRASS4, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.DEKU_TREE_MQ_GRAVES_GRASS5, lambda bundle: can_cut_shrubs(bundle)),
    ])
    # Connections
    connect_regions(Regions.DEKU_TREE_MQ_BASEMENT_GRAVE_ROOM, world, [
        (Regions.DEKU_TREE_MQ_BASEMENT_LEDGE, lambda bundle: is_child(bundle) and (has_fire_source_with_torch(bundle) or can_use(Items.FAIRY_BOW, bundle))),
        (Regions.DEKU_TREE_MQ_BASEMENT_SOUTHWEST_ROOM, lambda bundle: True),
        (Regions.DEKU_TREE_MQ_BASEMENT_BACK_ROOM, lambda bundle: has_fire_source_with_torch(bundle) or can_use(Items.FAIRY_BOW, bundle)),
    ])

    # Deku Tree MQ Basement Back Room
    # Locations
    add_locations(Regions.DEKU_TREE_MQ_BASEMENT_BACK_ROOM, world, [
        (Locations.DEKU_TREE_MQ_GS_BASEMENT_BACK_ROOM, lambda bundle: can_get_enemy_drop(bundle, Enemies.GOLD_SKULLTULA, EnemyDistance.BOOMERANG)),
        (Locations.DEKU_TREE_MQ_BACK_GRASS1, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.DEKU_TREE_MQ_BACK_GRASS2, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.DEKU_TREE_MQ_BACK_GRASS3, lambda bundle: can_cut_shrubs(bundle)),
    ])
    # Connections
    connect_regions(Regions.DEKU_TREE_MQ_BASEMENT_BACK_ROOM, world, [
        (Regions.DEKU_TREE_MQ_BASEMENT_GRAVE_ROOM, lambda bundle: True),
    ])

    # Deku Tree Basement Ledge
    # Events
    add_events(Regions.DEKU_TREE_MQ_BASEMENT_LEDGE, world, [
        (EventLocations.DEKU_TREE_BASEMENT_UPPER_BLOCK, LocalEvents.DEKU_TREE_BASEMENT_UPPER_BLOCK_PUSHED, lambda bundle: True),
    ])
    # Locations
    add_locations(Regions.DEKU_TREE_MQ_BASEMENT_LEDGE, world, [
        (Locations.DEKU_TREE_MQ_DEKU_SCRUB, lambda bundle: can_stun_deku(bundle)),
        (Locations.DEKU_TREE_MQ_BASEMENT_UPPER_GRASS1, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.DEKU_TREE_MQ_BASEMENT_UPPER_GRASS2, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.DEKU_TREE_MQ_BASEMENT_UPPER_GRASS3, lambda bundle: can_cut_shrubs(bundle)),
    ])
    connect_regions(Regions.DEKU_TREE_MQ_BASEMENT_LEDGE, world, [
        (Regions.DEKU_TREE_MQ_BASEMENT_GRAVE_ROOM, lambda bundle: is_child(bundle)),
        (Regions.DEKU_TREE_MQ_BASEMENT, lambda bundle: True),
        (Regions.DEKU_TREE_MQ_OUTSIDE_BOSS_ROOM, lambda bundle: (has_fire_source(bundle) or can_use(Items.STICKS, bundle)) and (has_item(Items.BRONZE_SCALE, bundle) or can_use(Items.IRON_BOOTS, bundle))),
    ])

    # Deku Tree MQ Outside Boss Room
    # Locations
    add_locations(Regions.DEKU_TREE_MQ_OUTSIDE_BOSS_ROOM, world, [
        (Locations.DEKU_TREE_MQ_FINAL_ROOM_LEFT_FRONT_HEART, lambda bundle: has_item(Items.BRONZE_SCALE, bundle) or can_use(Items.IRON_BOOTS, bundle) or can_use(Items.BOOMERANG, bundle)),
        (Locations.DEKU_TREE_MQ_FINAL_ROOM_LEFT_BACK_HEART,
         lambda bundle: has_item(Items.BRONZE_SCALE, bundle) or can_use(Items.IRON_BOOTS, bundle) or can_use(
             Items.BOOMERANG, bundle)),
        (Locations.DEKU_TREE_MQ_FINAL_ROOM_RIGHT_HEART, lambda bundle: has_item(Items.BRONZE_SCALE, bundle) or can_use(Items.IRON_BOOTS, bundle) or can_use(Items.BOOMERANG, bundle)),
        (Locations.DEKU_TREE_MQ_BEFORE_BOSS_GRASS1, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.DEKU_TREE_MQ_BEFORE_BOSS_GRASS2, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.DEKU_TREE_MQ_BEFORE_BOSS_GRASS3, lambda bundle: can_cut_shrubs(bundle)),
    ])
    # Connections
    connect_regions(Regions.DEKU_TREE_MQ_OUTSIDE_BOSS_ROOM, world, [
        (Regions.DEKU_TREE_MQ_BASEMENT_LEDGE, lambda bundle: has_item(Items.BRONZE_SCALE, bundle) or can_use(Items.HOOKSHOT, bundle)),
        (Regions.DEKU_TREE_BOSS_ENTRYWAY, lambda bundle: can_reflect_nuts(bundle)),
    ])

    # Deku Boss room entryway
    # Connections
    connect_regions(Regions.DEKU_TREE_BOSS_ENTRYWAY, world, [
        (Regions.DEKU_TREE_BOSS_ROOM, lambda bundle: True)
    ])

    # Deku boss exit
    # Connections
    connect_regions(Regions.DEKU_TREE_BOSS_EXIT, world, [
        (Regions.DEKU_TREE_MQ_OUTSIDE_BOSS_ROOM, lambda bundle: True),
        # skipping mq connection
    ])

    # Deku Tree boss room
    # Events
    add_events(Regions.DEKU_TREE_BOSS_ROOM, world, [
        (EventLocations.DEKU_TREE_QUEEN_GOHMA, Events.DEKU_TREE_COMPLETED,
         lambda bundle: can_kill_enemy(bundle, Enemies.GOHMA))
    ])
    # Locations
    add_locations(Regions.DEKU_TREE_BOSS_ROOM, world, [
        (Locations.QUEEN_GOHMA, lambda bundle: has_item(
            Events.DEKU_TREE_COMPLETED, bundle)),
        (Locations.DEKU_TREE_QUEEN_GOHMA_HEART_CONTAINER,
         lambda bundle: has_item(Events.DEKU_TREE_COMPLETED, bundle)),
        (Locations.DEKU_TREE_QUEEN_GOHMA_GRASS1,
         lambda bundle: can_cut_shrubs(bundle)),
        (Locations.DEKU_TREE_QUEEN_GOHMA_GRASS2,
         lambda bundle: can_cut_shrubs(bundle)),
        (Locations.DEKU_TREE_QUEEN_GOHMA_GRASS3,
         lambda bundle: can_cut_shrubs(bundle)),
        (Locations.DEKU_TREE_QUEEN_GOHMA_GRASS4,
         lambda bundle: can_cut_shrubs(bundle)),
        (Locations.DEKU_TREE_QUEEN_GOHMA_GRASS5,
         lambda bundle: can_cut_shrubs(bundle)),
        (Locations.DEKU_TREE_QUEEN_GOHMA_GRASS6,
         lambda bundle: can_cut_shrubs(bundle)),
        (Locations.DEKU_TREE_QUEEN_GOHMA_GRASS7,
         lambda bundle: can_cut_shrubs(bundle)),
        (Locations.DEKU_TREE_QUEEN_GOHMA_GRASS8,
         lambda bundle: can_cut_shrubs(bundle))
    ])
    # Connections
    connect_regions(Regions.DEKU_TREE_BOSS_ROOM, world, [
        (Regions.DEKU_TREE_BOSS_EXIT, lambda bundle: True),
        (Regions.KF_OUTSIDE_DEKU_TREE, lambda bundle: has_item(
            Events.DEKU_TREE_COMPLETED, bundle))
    ])





def init_regions(world: "SohWorld", dungeon_quest: DungeonQuest = DungeonQuest.VANILLA) -> None:
    regions = vanilla_regions if dungeon_quest == DungeonQuest.VANILLA else master_quest_regions
    for region_name in regions:
        region = SohRegion(str(region_name), world.player, world.multiworld)
        world.multiworld.regions.append(region)
