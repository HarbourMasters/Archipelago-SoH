from ...LogicHelpers import *

if TYPE_CHECKING:
    from ... import SohWorld


class EventLocations(StrEnum):
    DMC_GOSSIP_STONE_SONG_FAIRY = "DMC Gossip Stone Song Fairy"
    DMC_BEAN_PLANT_FAIRY = "DMC Bean Plant Fairy"
    DMC_UPPER_GROTTO_GOSSIP_STONE_SONG_FAIRY = "DMC Upper Grotto Gossip Stone Song Fairy"
    DMC_UPPER_GROTTO_BUTTERFLY_FAIRY = "DMC Upper Grotto Butterfly Fairy"
    DMC_UPPER_GROTTO_BUG_GRASS = "DMC Upper Grotto Bug Grass"
    DMC_UPPER_GROTTO_PUDDLE_FISH = "DMC Upper Grotto Puddle Fish"
    DMC_BEAN_PATCH = "DMC Bean Patch"


class LocalEvents(StrEnum):
    DMC_BEAN_PLANTED = "DMC Bean Planted"


def set_region_rules(world: "SohWorld") -> None:
    # Death Mountain Crater Upper Nearby
    # Connections
    connect_regions(Regions.DMC_UPPER_NEARBY, world, [
        (Regions.DMC_UPPER_LOCAL, lambda bundle: fire_timer_at_least(bundle, 48)),
        (Regions.DEATH_MOUNTAIN_SUMMIT, lambda bundle: True_()),
        (Regions.DMC_UPPER_GROTTO, lambda bundle: blast_or_smash(
            bundle) & (fire_timer_at_least(bundle, 8) | hearts_at_least(bundle, 3))),
    ])

    # Death Mountain Crater Upper Local
    # Events
    add_events(Regions.DMC_UPPER_LOCAL, world, [
        (EventLocations.DMC_GOSSIP_STONE_SONG_FAIRY, Events.CAN_ACCESS_FAIRIES, lambda bundle: has_explosives(
            bundle) & call_gossip_fairy_except_suns(bundle) & (fire_timer_at_least(bundle, 16) | hearts_at_least(bundle, 3)))
    ])
    # Locations
    add_locations(Regions.DMC_UPPER_LOCAL, world, [
        (Locations.DMC_WALL_FREESTANDING_POH, lambda bundle: fire_timer_at_least(bundle, 16) | hearts_at_least(bundle, 3)),
        (Locations.DMC_GS_CRATE, lambda bundle: (fire_timer_at_least(bundle, 8) | hearts_at_least(bundle, 3)) & is_child(bundle) & can_attack(bundle) & can_break_crates(bundle)),
        (Locations.DMC_GOSSIP_STONE_FAIRY, lambda bundle: call_gossip_fairy_except_suns(
            bundle) & has_explosives(bundle) & (fire_timer_at_least(bundle, 16) | hearts_at_least(bundle, 3))),
        (Locations.DMC_GOSSIP_STONE_BIG_FAIRY, lambda bundle: can_use(
            Items.SONG_OF_STORMS, bundle) & (fire_timer_at_least(bundle, 16) | hearts_at_least(bundle, 3))),
        (Locations.DMC_CRATE, lambda bundle: (fire_timer_at_least(bundle, 8) | hearts_at_least(bundle, 3)) & is_child(bundle) & can_break_crates(bundle))
    ])
    # Connections
    connect_regions(Regions.DMC_UPPER_LOCAL, world, [
        (Regions.DMC_UPPER_NEARBY, lambda bundle: True_()),
        (Regions.DMC_LADDER_REGION_NEARBY, lambda bundle: fire_timer_at_least(bundle, 16) | hearts_at_least(bundle, 3)),
        # TODO Implement Dungeon Shuffle Option to replace False
        (Regions.DMC_CENTRAL_NEARBY, lambda bundle: is_adult(bundle) & can_use(Items.GORON_TUNIC, bundle) & can_use(Items.DISTANT_SCARECROW, bundle) & (effective_health_at_least(bundle, 3) | (can_use(Items.BOTTLE_WITH_FAIRY, bundle) & False_() | can_use(Items.NAYRUS_LOVE, bundle)))),
        (Regions.DMC_LOWER_NEARBY, lambda bundle: False_()),
        (Regions.DMC_DISTANT_PLATFORM, lambda bundle: (fire_timer_at_least(bundle, 48) | hearts_at_least(bundle, 2)) | hearts_at_least(bundle, 3)),
    ])

    # Death Mountain Crater Ladder Area Nearby
    # Locations
    add_locations(Regions.DMC_LADDER_REGION_NEARBY, world, [
        (Locations.DMC_DEKU_SCRUB, lambda bundle: is_child(bundle) & can_stun_deku(bundle) & can_afford_slot(Locations.DMC_DEKU_SCRUB, bundle))

    ])
    # Connections
    connect_regions(Regions.DMC_LADDER_REGION_NEARBY, world, [
        (Regions.DMC_UPPER_NEARBY, lambda bundle: hearts_at_least(bundle, 3)),
        (Regions.DMC_LOWER_NEARBY, lambda bundle: hearts_at_least(bundle, 3) & (can_use(Items.HOVER_BOOTS, bundle) | (can_do_trick(Tricks.DMC_BOULDER_JS,
         bundle) & is_adult(bundle) & can_use(Items.MEGATON_HAMMER, bundle)) | (can_do_trick(Tricks.DMC_BOULDER_SKIP, bundle) & is_adult(bundle))))
    ])

    # Death Mountain Crater Lower Nearby
    # Locations
    add_locations(Regions.DMC_LOWER_NEARBY, world, [
        (Locations.DMC_NEAR_GCPOT1, lambda bundle: can_break_pots(bundle)),
        (Locations.DMC_NEAR_GCPOT2, lambda bundle: can_break_pots(bundle)),
        (Locations.DMC_NEAR_GCPOT3, lambda bundle: can_break_pots(bundle)),
        (Locations.DMC_NEAR_GCPOT4, lambda bundle: can_break_pots(bundle))
    ])
    # Connections
    connect_regions(Regions.DMC_LOWER_NEARBY, world, [
        (Regions.DMC_LOWER_LOCAL, lambda bundle: fire_timer_at_least(bundle, 48)),
        (Regions.GC_DARUNIAS_CHAMBER, lambda bundle: True_()),
        (Regions.DMC_GREAT_FAIRY_FOUNTAIN,
         lambda bundle: can_use(Items.MEGATON_HAMMER, bundle)),
        (Regions.DMC_HAMMER_GROTTO, lambda bundle: is_adult(
            bundle) & can_use(Items.MEGATON_HAMMER, bundle))
    ])

    # Death Mountain Crater Lower Local
    # Connections
    connect_regions(Regions.DMC_LOWER_LOCAL, world, [
        (Regions.DMC_LOWER_NEARBY, lambda bundle: True_()),
        (Regions.DMC_LADDER_REGION_NEARBY, lambda bundle: fire_timer_at_least(bundle, 8) | hearts_at_least(bundle, 3)),
        (Regions.DMC_CENTRAL_NEARBY, lambda bundle: (can_use(Items.HOVER_BOOTS, bundle) | can_use(
            Items.HOOKSHOT, bundle)) & (fire_timer_at_least(bundle, 8) | hearts_at_least(bundle, 3))),
        (Regions.DMC_CENTRAL_LOCAL, lambda bundle: (can_use(Items.HOVER_BOOTS, bundle) | can_use(Items.HOOKSHOT, bundle) | (
            is_adult(bundle) & can_shield(bundle) & can_do_trick(Tricks.DMC_BOLERO_JUMP, bundle))) & fire_timer_at_least(bundle, 24))
    ])

    # Death Mountain Crater Central Nearby
    # Locations
    add_locations(Regions.DMC_CENTRAL_NEARBY, world, [
        (Locations.SHEIK_IN_CRATER, lambda bundle: is_adult(bundle)
         & (fire_timer_at_least(bundle, 8) | hearts_at_least(bundle, 3))),
        (Locations.DMC_VOLCANO_FREESTANDING_POH, lambda bundle: is_adult(bundle) &
         hearts_at_least(bundle, 3) &
         (has_item(LocalEvents.DMC_BEAN_PLANTED, bundle) |
          (can_do_trick(Tricks.DMC_HOVER_BEAN_POH, bundle)
           &
           can_use(Items.HOVER_BOOTS, bundle)))),
    ])
    # Connections
    connect_regions(Regions.DMC_CENTRAL_NEARBY, world, [
        (Regions.DMC_CENTRAL_LOCAL, lambda bundle: fire_timer_at_least(bundle, 48)),
    ])

    # Death Mountain Crater Central Local
    # Events
    add_events(Regions.DMC_CENTRAL_LOCAL, world, [
        (EventLocations.DMC_BEAN_PLANT_FAIRY, Events.CAN_ACCESS_FAIRIES, lambda bundle: can_use(Items.MAGIC_BEAN,
         bundle) & can_use(Items.SONG_OF_STORMS, bundle) & (fire_timer_at_least(bundle, 8) | hearts_at_least(bundle, 3))),
        (EventLocations.DMC_BEAN_PATCH, LocalEvents.DMC_BEAN_PLANTED, lambda bundle: is_child(bundle)
         & can_use(Items.MAGIC_BEAN, bundle) & (fire_timer_at_least(bundle, 8) | hearts_at_least(bundle, 3))),
    ])
    # Locations
    add_locations(Regions.DMC_CENTRAL_LOCAL, world, [
        (Locations.DMC_GS_BEAN_PATCH, lambda bundle: (fire_timer_at_least(bundle, 8) | hearts_at_least(bundle, 3)) & can_spawn_soil_skull(bundle) & can_attack(bundle)),
        (Locations.DMC_NEAR_WARP_PLATFORM_RED_RUPEE,
         lambda bundle: is_child(bundle)),
        (Locations.DMC_MIDDLE_PLATFORM_RED_RUPEE, lambda bundle: is_child(
            bundle) & (fire_timer_at_least(bundle, 8) | hearts_at_least(bundle, 3))),
        (Locations.DMC_MIDDLE_PLATFORM_BLUE_RUPEE1, lambda bundle: is_child(
            bundle) & (fire_timer_at_least(bundle, 8) | hearts_at_least(bundle, 3))),
        (Locations.DMC_MIDDLE_PLATFORM_BLUE_RUPEE2, lambda bundle: is_child(
            bundle) & (fire_timer_at_least(bundle, 8) | hearts_at_least(bundle, 3))),
        (Locations.DMC_MIDDLE_PLATFORM_BLUE_RUPEE3, lambda bundle: is_child(
            bundle) & (fire_timer_at_least(bundle, 8) | hearts_at_least(bundle, 3))),
        (Locations.DMC_MIDDLE_PLATFORM_BLUE_RUPEE4, lambda bundle: is_child(
            bundle) & (fire_timer_at_least(bundle, 8) | hearts_at_least(bundle, 3))),
        (Locations.DMC_MIDDLE_PLATFORM_BLUE_RUPEE5, lambda bundle: is_child(
            bundle) & (fire_timer_at_least(bundle, 8) | hearts_at_least(bundle, 3))),
        (Locations.DMC_MIDDLE_PLATFORM_BLUE_RUPEE6, lambda bundle: is_child(
            bundle) & (fire_timer_at_least(bundle, 8) | hearts_at_least(bundle, 3))),
        (Locations.DMC_BEAN_SPROUT_FAIRY1, lambda bundle: is_child(bundle) & can_use(Items.MAGIC_BEAN, bundle)
         & can_use(Items.SONG_OF_STORMS, bundle) & (fire_timer_at_least(bundle, 8) | hearts_at_least(bundle, 3))),
        (Locations.DMC_BEAN_SPROUT_FAIRY2, lambda bundle: is_child(bundle) & can_use(Items.MAGIC_BEAN, bundle)
         & can_use(Items.SONG_OF_STORMS, bundle) & (fire_timer_at_least(bundle, 8) | hearts_at_least(bundle, 3))),
        (Locations.DMC_BEAN_SPROUT_FAIRY3, lambda bundle: is_child(bundle) & can_use(Items.MAGIC_BEAN, bundle)
         & can_use(Items.SONG_OF_STORMS, bundle) & (fire_timer_at_least(bundle, 8) | hearts_at_least(bundle, 3)))
    ])
    # Connections
    connect_regions(Regions.DMC_CENTRAL_LOCAL, world, [
        (Regions.DMC_CENTRAL_NEARBY, lambda bundle: True_()),
        (Regions.DMC_LOWER_NEARBY, lambda bundle: (is_adult(bundle) & has_item(LocalEvents.DMC_BEAN_PLANTED,
         bundle)) | can_use(Items.HOVER_BOOTS, bundle) | can_use(Items.HOOKSHOT, bundle)),
        (Regions.DMC_UPPER_NEARBY, lambda bundle: is_adult(bundle)
         & has_item(LocalEvents.DMC_BEAN_PLANTED, bundle)),
        (Regions.FIRE_TEMPLE_ENTRYWAY, lambda bundle: (is_child(bundle) & hearts_at_least(bundle, 3) & dungeon_entrances_shuffled(bundle)) | (is_adult(bundle) & fire_timer_at_least(bundle, 24))),
        (Regions.DMC_DISTANT_PLATFORM, lambda bundle: (fire_timer_at_least(bundle, 48) | hearts_at_least(bundle, 2)) & can_use(Items.DISTANT_SCARECROW, bundle)),
    ])

    # Death Mountain Crater Great Fairy Fountain
    # Locations
    add_locations(Regions.DMC_GREAT_FAIRY_FOUNTAIN, world, [
        (Locations.DMC_GREAT_FAIRY_REWARD,
         lambda bundle: can_use(Items.ZELDAS_LULLABY, bundle))
    ])
    # Connections
    connect_regions(Regions.DMC_GREAT_FAIRY_FOUNTAIN, world, [
        (Regions.DMC_LOWER_LOCAL, lambda bundle: True_())
    ])

    # Death Mountain Crater Upper Grotto
    # Events
    add_events(Regions.DMC_UPPER_GROTTO, world, [
        (EventLocations.DMC_UPPER_GROTTO_GOSSIP_STONE_SONG_FAIRY,
         Events.CAN_ACCESS_FAIRIES, lambda bundle: (call_gossip_fairy(bundle))),
        (EventLocations.DMC_UPPER_GROTTO_BUTTERFLY_FAIRY,
         Events.CAN_ACCESS_FAIRIES, lambda bundle: (can_use(Items.STICKS, bundle))),
        (EventLocations.DMC_UPPER_GROTTO_BUG_GRASS,
         Events.CAN_ACCESS_BUGS, lambda bundle: (can_cut_shrubs(bundle))),
        (EventLocations.DMC_UPPER_GROTTO_PUDDLE_FISH,
         Events.CAN_ACCESS_FISH, lambda bundle: True_())
    ])
    # Locations
    add_locations(Regions.DMC_UPPER_GROTTO, world, [
        (Locations.DMC_UPPER_GROTTO_CHEST, lambda bundle: True_()),
        (Locations.DMC_UPPER_GROTTO_FISH, lambda bundle: has_bottle(bundle)),
        (Locations.DMC_UPPER_GROTTO_GOSSIP_STONE_FAIRY,
         lambda bundle: call_gossip_fairy(bundle)),
        (Locations.DMC_UPPER_GROTTO_GOSSIP_STONE_BIG_FAIRY,
         lambda bundle: can_use(Items.SONG_OF_STORMS, bundle)),
        (Locations.DMC_UPPER_GROTTO_BEEHIVE_LEFT,
         lambda bundle: can_break_lower_hives(bundle)),
        (Locations.DMC_UPPER_GROTTO_BEEHIVE_RIGHT,
         lambda bundle: can_break_lower_hives(bundle)),
        (Locations.DMC_UPPER_GROTTO_GRASS1, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.DMC_UPPER_GROTTO_GRASS2, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.DMC_UPPER_GROTTO_GRASS3, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.DMC_UPPER_GROTTO_GRASS4, lambda bundle: can_cut_shrubs(bundle))
    ])
    # Connections
    connect_regions(Regions.DMC_UPPER_GROTTO, world, [
        (Regions.DMC_UPPER_LOCAL, lambda bundle: True_())
    ])

    # Death Mountain Crater Hammer Grotto
    # Locations
    add_locations(Regions.DMC_HAMMER_GROTTO, world, [
        (Locations.DMC_DEKU_SCRUB_GROTTO_LEFT,
         lambda bundle: can_stun_deku(bundle) & can_afford_slot(Locations.DMC_DEKU_SCRUB_GROTTO_LEFT, bundle)),
        (Locations.DMC_DEKU_SCRUB_GROTTO_RIGHT,
         lambda bundle: can_stun_deku(bundle) & can_afford_slot(Locations.DMC_DEKU_SCRUB_GROTTO_RIGHT, bundle)),
        (Locations.DMC_DEKU_SCRUB_GROTTO_CENTER,
         lambda bundle: can_stun_deku(bundle) & can_afford_slot(Locations.DMC_DEKU_SCRUB_GROTTO_CENTER, bundle)),
        (Locations.DMC_HAMMER_GROTTO_BEEHIVE,
         lambda bundle: can_break_upper_beehives(bundle))
    ])
    # Connections
    connect_regions(Regions.DMC_HAMMER_GROTTO, world, [
        (Regions.DMC_LOWER_LOCAL, lambda bundle: True_())
    ])

    # Death Mountain Crater Distant Platform
    # Locations
    add_locations(Regions.DMC_DISTANT_PLATFORM, world, [
        (Locations.DMC_DISTANT_PLATFORM_RUPEE1, lambda bundle: is_adult(bundle)),
        (Locations.DMC_DISTANT_PLATFORM_RUPEE2, lambda bundle: is_adult(bundle)),
        (Locations.DMC_DISTANT_PLATFORM_RUPEE3, lambda bundle: is_adult(bundle)),
        (Locations.DMC_DISTANT_PLATFORM_RUPEE4, lambda bundle: is_adult(bundle)),
        (Locations.DMC_DISTANT_PLATFORM_RUPEE5, lambda bundle: is_adult(bundle)),
        (Locations.DMC_DISTANT_PLATFORM_RUPEE6, lambda bundle: is_adult(bundle)),
        (Locations.DMC_DISTANT_PLATFORM_RED_RUPEE, lambda bundle: is_adult(bundle))
    ])
    # Connections
    connect_regions(Regions.DMC_DISTANT_PLATFORM, world, [
        (Regions.DMC_CENTRAL_LOCAL, lambda bundle: fire_timer_at_least(bundle, 48) & can_use(Items.DISTANT_SCARECROW, bundle))
    ])
