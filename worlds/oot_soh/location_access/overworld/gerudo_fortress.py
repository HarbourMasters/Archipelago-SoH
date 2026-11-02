from ...LogicHelpers import *

if TYPE_CHECKING:
    from ... import SohWorld


class EventLocations(StrEnum):
    GF_GATE = "GF Gate"
    GF_GATE_OUTSIDE = "GF Gate Outside"
    GTG_GATE = "GTG Gate"
    GF_STORMS_GROTTO_FAIRY = "GF Storms Grotto Fairy"


class LocalEvents(StrEnum):
    GF_GATE_OPEN = "GF Gate Open"
    GTG_GATE_OPEN = "GTG Gate Open"


def set_region_rules(world: "SohWorld") -> None:
    # Gerudo Fortress Outskirts
    # Events
    add_events(Regions.GERUDO_FORTRESS_OUTSKIRTS, world, [
        (EventLocations.GF_GATE, LocalEvents.GF_GATE_OPEN,
         lambda bundle: is_adult(bundle) & has_item(Items.GERUDO_MEMBERSHIP_CARD, bundle)),
    ])
    # Locations
    add_locations(Regions.GERUDO_FORTRESS_OUTSKIRTS, world, [
        (Locations.GF_OUTSKIRTS_NORTHEAST_CRATE,
         lambda bundle: (is_child(bundle) | can_pass_enemy(bundle, Enemies.GERUDO_GUARD)) & can_break_crates(
             bundle)),
        (Locations.GF_OUTSKIRTS_NORTHWEST_CRATE,
         lambda bundle: is_child(bundle) | can_pass_enemy(bundle, Enemies.GERUDO_GUARD)),
    ])
    # Connections
    connect_regions(Regions.GERUDO_FORTRESS_OUTSKIRTS, world, [
        (Regions.GV_FORTRESS_SIDE, lambda bundle: True_()),
        (Regions.THIEVES_HIDEOUT_1_TORCH_CELL, lambda bundle: True_()),
        (Regions.GF_OUTSIDE_GATE, lambda bundle: has_item(
            LocalEvents.GF_GATE_OPEN, bundle)),
        (Regions.GF_NEAR_GROTTO, lambda bundle: is_child(bundle)
         | can_pass_enemy(bundle, Enemies.GERUDO_GUARD)),
        (Regions.GF_OUTSIDE_GTG, lambda bundle: is_child(bundle)
         | can_pass_enemy(bundle, Enemies.GERUDO_GUARD)),
        (Regions.GF_JAIL_WINDOW, lambda bundle: can_use(Items.HOOKSHOT, bundle)),
    ])

    # GF Near Grotto
    # Locations
    add_locations(Regions.GF_NEAR_GROTTO, world, [
        (Locations.GF_SOUTHMOST_CENTER_CRATE,
         lambda bundle: can_break_crates(bundle)),
        (Locations.GF_MIDDLE_SOUTH_CENTER_CRATE,
         lambda bundle: can_break_crates(bundle)),
        (Locations.GF_MIDDLE_NORTH_CENTER_CRATE,
         lambda bundle: can_break_crates(bundle)),
        (Locations.GF_NORTHMOST_CENTER_CRATE,
         lambda bundle: can_break_crates(bundle)),
    ])
    # Connections
    connect_regions(Regions.GF_NEAR_GROTTO, world, [
        (Regions.THIEVES_HIDEOUT_1_TORCH_CELL, lambda bundle: True_()),
        (Regions.THIEVES_HIDEOUT_STEEP_SLOPE_CELL, lambda bundle: True_()),
        (Regions.THIEVES_HIDEOUT_KITCHEN_CORRIDOR, lambda bundle: True_()),
        (Regions.GERUDO_FORTRESS_OUTSKIRTS, lambda bundle: True_()),
        (Regions.GF_JAIL_WINDOW, lambda bundle: can_use(Items.HOOKSHOT, bundle)),
        (Regions.GF_OUTSIDE_GTG, lambda bundle: is_child(bundle)
         | can_pass_enemy(bundle, Enemies.GERUDO_GUARD)),
        (Regions.GF_TOP_OF_UPPER_VINES,
         lambda bundle: can_use(Items.LONGSHOT, bundle)),
        (Regions.GF_STORMS_GROTTO, lambda bundle: is_adult(
            bundle) & can_open_storms_grotto(bundle)),
    ])

    # GF Outside GTG
    # Events
    add_events(Regions.GF_OUTSIDE_GTG, world, [
        (EventLocations.GTG_GATE, LocalEvents.GTG_GATE_OPEN,
         lambda bundle: (is_adult(bundle) & has_item(Items.GERUDO_MEMBERSHIP_CARD, bundle)) & has_item(
             Items.CHILD_WALLET, bundle)),
    ])
    # Connections
    connect_regions(Regions.GF_OUTSIDE_GTG, world, [
        (Regions.GF_TO_GTG, lambda bundle: has_item(LocalEvents.GTG_GATE_OPEN, bundle)
            & (is_adult(bundle) | dungeon_entrances_shuffled(bundle))),
        (Regions.GF_JAIL_WINDOW, lambda bundle: can_use(Items.HOOKSHOT, bundle)),
        (Regions.GERUDO_FORTRESS_OUTSKIRTS, lambda bundle: True_()),
        (Regions.GF_NEAR_GROTTO, lambda bundle: is_child(bundle)
         | can_pass_enemy(bundle, Enemies.GERUDO_GUARD)),
        (Regions.GF_ABOVE_GTG, lambda bundle: is_child(bundle)
         | can_pass_enemy(bundle, Enemies.GERUDO_GUARD)),
        (Regions.GF_TOP_OF_UPPER_VINES,
         lambda bundle: has_item(Items.GERUDO_MEMBERSHIP_CARD, bundle) & can_use(Items.LONGSHOT, bundle)),
        (Regions.GF_HBA_RANGE, lambda bundle: is_child(bundle)
         | has_item(Items.GERUDO_MEMBERSHIP_CARD, bundle)),
    ])

    # GF to GTG
    # Connections
    connect_regions(Regions.GF_TO_GTG, world, [
        (Regions.GERUDO_TRAINING_GROUND_ENTRYWAY, lambda bundle: True_()),
    ])

    # GF Exiting GTG
    # Connections
    connect_regions(Regions.GF_EXITING_GTG, world, [
        (Regions.GF_OUTSIDE_GTG, lambda bundle: is_child(bundle)
         | has_item(Items.GERUDO_MEMBERSHIP_CARD, bundle)),
        (Regions.GF_JAIL_WINDOW, lambda bundle: can_use(Items.HOOKSHOT, bundle)),
        (Regions.GERUDO_FORTRESS_OUTSKIRTS, lambda bundle: True_()),
    ])

    # GF Above GTG
    # Connections
    connect_regions(Regions.GF_ABOVE_GTG, world, [
        (Regions.THIEVES_HIDEOUT_DOUBLE_CELL, lambda bundle: True_()),
        (Regions.THIEVES_HIDEOUT_KITCHEN_CORRIDOR, lambda bundle: True_()),
        (Regions.GF_JAIL_WINDOW, lambda bundle: can_use(Items.HOOKSHOT, bundle)),
        (Regions.GERUDO_FORTRESS_OUTSKIRTS, lambda bundle: True_()),
        (Regions.GF_NEAR_GROTTO, lambda bundle: True_()),
        (Regions.GF_OUTSIDE_GTG, lambda bundle: is_child(bundle)
         | can_pass_enemy(bundle, Enemies.GERUDO_GUARD)),
        (Regions.GF_BOTTOM_OF_LOWER_VINES,
         lambda bundle: can_do_trick(Tricks.GF_JUMP, bundle)),
    ])

    # GF Bottom of Lower Vines
    # Connections
    connect_regions(Regions.GF_BOTTOM_OF_LOWER_VINES, world, [
        (Regions.THIEVES_HIDEOUT_STEEP_SLOPE_CELL, lambda bundle: True_()),
        (Regions.GF_NEAR_GROTTO, lambda bundle: True_()),
        (Regions.GF_TOP_OF_LOWER_VINES, lambda bundle: True_()),
        (Regions.GF_ABOVE_GTG, lambda bundle: True_()),
        (Regions.GF_BELOW_GS, lambda bundle: is_adult(
            bundle) & can_ground_jump(bundle))
    ])

    # GF Top of Lower Vines
    # Connections
    connect_regions(Regions.GF_TOP_OF_LOWER_VINES, world, [
        (Regions.THIEVES_HIDEOUT_KITCHEN_TOP, lambda bundle: True_()),
        (Regions.THIEVES_HIDEOUT_DOUBLE_CELL, lambda bundle: True_()),
        (Regions.GF_ABOVE_GTG, lambda bundle: True_()),
        (Regions.GF_BOTTOM_OF_LOWER_VINES, lambda bundle: True_()),
        (Regions.GF_BOTTOM_OF_UPPER_VINES, lambda bundle: is_adult(
            bundle) & can_do_trick(Tricks.GF_JUMP, bundle)),
    ])

    # GF Near GS
    # Connections
    connect_regions(Regions.GF_NEAR_GS, world, [
        (Regions.THIEVES_HIDEOUT_KITCHEN_TOP, lambda bundle: True_()),
        (Regions.GF_BOTTOM_OF_LOWER_VINES, lambda bundle: True_()),
        (Regions.GF_TOP_OF_LOWER_VINES, lambda bundle: True_()),
        (Regions.GF_SLOPED_ROOF, lambda bundle: is_adult(
            bundle) | can_ground_jump(bundle)),
        (Regions.GF_LONG_ROOF,
         lambda bundle: can_use(Items.HOVER_BOOTS, bundle) | is_adult(bundle) & can_do_trick(Tricks.GF_JUMP,
                                                                                                bundle)),
        (Regions.GF_NEAR_CHEST, lambda bundle: can_use(Items.LONGSHOT, bundle)),
        (Regions.GF_BELOW_GS, lambda bundle: True_()),
        (Regions.GF_GS_KILL_ZONE,
         lambda bundle: is_adult(bundle) & can_get_enemy_drop(bundle, Enemies.GOLD_SKULLTULA,
                                                                EnemyDistance.BOMB_THROW) & can_get_nighttime_gs(
             bundle)),
    ])

    # GF GS Top Floor
    # Location
    add_locations(Regions.GF_GS_KILL_ZONE, world, [
        (Locations.GF_GS_TOP_FLOOR, lambda bundle: True_()),
    ])

    # GF Sloped Roof
    # Connection
    connect_regions(Regions.GF_SLOPED_ROOF, world, [
        (Regions.GF_TOP_OF_LOWER_VINES, lambda bundle: True_()),
        (Regions.GF_NEAR_GS, lambda bundle: True_()),
        (Regions.GF_BOTTOM_OF_UPPER_VINES, lambda bundle: True_()),
        (Regions.GF_TOP_OF_UPPER_VINES, lambda bundle: is_adult(
            bundle) & can_do_trick(Tricks.GF_JUMP, bundle)),
    ])

    # GF Bottom of Upper Vines
    # Connections
    connect_regions(Regions.GF_BOTTOM_OF_UPPER_VINES, world, [
        (Regions.GF_OUTSIDE_GTG, lambda bundle: True_()),
        (Regions.GF_TOP_OF_LOWER_VINES, lambda bundle: True_()),
        (Regions.GF_SLOPED_ROOF, lambda bundle: is_adult(bundle) & (
            can_use(Items.HOVER_BOOTS, bundle) | can_do_trick(Tricks.GF_JUMP, bundle))),
        (Regions.GF_TOP_OF_UPPER_VINES, lambda bundle: True_()),
        (Regions.GF_TO_GTG, lambda bundle: is_adult(bundle)
         & can_do_trick(Tricks.GF_LEDGE_CLIP_INTO_GTG, bundle))
    ])

    # GF Top of Upper Vines
    # Connections
    connect_regions(Regions.GF_TOP_OF_UPPER_VINES, world, [
        (Regions.GF_TOP_OF_LOWER_VINES, lambda bundle: True_()),
        (Regions.GF_SLOPED_ROOF, lambda bundle: True_()),
        (Regions.GF_BOTTOM_OF_UPPER_VINES, lambda bundle: True_()),
        (Regions.GF_NEAR_CHEST, lambda bundle: can_use(Items.HOVER_BOOTS, bundle) | (
            is_adult(bundle) & can_use(Items.SCARECROW, bundle) & can_use(Items.HOOKSHOT,
                                                                              bundle)) | can_use(
            Items.LONGSHOT, bundle)),
        (Regions.GF_GS_KILL_ZONE,
         lambda bundle: is_adult(bundle) & can_get_enemy_drop(bundle, Enemies.GOLD_SKULLTULA,
                                                                EnemyDistance.SHORT_JUMPSLASH) & can_get_nighttime_gs(
             bundle)),
    ])

    # GF Near Chest
    # Locations
    add_locations(Regions.GF_NEAR_CHEST, world, [
        (Locations.GF_CHEST, lambda bundle: True_()),
    ])
    # Connections
    connect_regions(Regions.GF_NEAR_CHEST, world, [
        (Regions.GF_NEAR_GS, lambda bundle: True_()),
        (Regions.GF_LONG_ROOF, lambda bundle: True_()),
        (Regions.GF_GS_KILL_ZONE,
         lambda bundle: is_adult(bundle) & can_get_enemy_drop(bundle, Enemies.GOLD_SKULLTULA,
                                                                EnemyDistance.BOOMERANG) & can_get_nighttime_gs(
             bundle)),
    ])

    # GF Long Roof
    # Connections
    connect_regions(Regions.GF_LONG_ROOF, world, [
        (Regions.GF_BOTTOM_OF_LOWER_VINES, lambda bundle: True_()),
        (Regions.GF_NEAR_GS,
         lambda bundle: (is_adult(bundle) & can_do_trick(Tricks.GF_JUMP, bundle)) | can_use(Items.HOVER_BOOTS,
                                                                                               bundle)),
        (Regions.GF_BELOW_GS, lambda bundle: True_()),
        (Regions.GF_NEAR_CHEST, lambda bundle: can_use(Items.LONGSHOT, bundle)),
        (Regions.GF_BELOW_CHEST, lambda bundle: True_()),
    ])

    # GF Below GS
    # Connections
    connect_regions(Regions.GF_BELOW_GS, world, [
        (Regions.THIEVES_HIDEOUT_DEAD_END_CELL, lambda bundle: True_()),
        (Regions.GF_BOTTOM_OF_LOWER_VINES, lambda bundle: True_()),
        (Regions.GF_GS_KILL_ZONE,
         lambda bundle: is_adult(bundle) & can_get_enemy_drop(bundle, Enemies.GOLD_SKULLTULA,
                                                                EnemyDistance.LONGSHOT) & can_get_nighttime_gs(
             bundle)),
    ])

    # GF Below Chest
    # Connections
    connect_regions(Regions.GF_BELOW_CHEST, world, [
        (Regions.THIEVES_HIDEOUT_BREAK_ROOM, lambda bundle: True_()),
        (Regions.GERUDO_FORTRESS_OUTSKIRTS, lambda bundle: True_()),
    ])

    # GF Above Jail
    # Locations
    add_locations(Regions.GF_ABOVE_JAIL, world, [
        (Locations.GF_ABOVE_JAIL_CRATE, lambda bundle: True_()),
    ])
    # Connection
    connect_regions(Regions.GF_ABOVE_JAIL, world, [
        (Regions.GERUDO_FORTRESS_OUTSKIRTS,
         lambda bundle: can_do_trick(Tricks.GF_JUMP, bundle)),
        (Regions.GF_NEAR_CHEST, lambda bundle: can_use(Items.LONGSHOT, bundle)),
        (Regions.GF_BELOW_CHEST, lambda bundle: take_damage(bundle)),
        (Regions.GF_JAIL_WINDOW, lambda bundle: can_use(Items.HOOKSHOT, bundle)),
        (Regions.THIEVES_HIDEOUT_BREAK_ROOM_CORRIDOR, lambda bundle: True_())
    ])

    # GF Jail Window
    # Connections
    connect_regions(Regions.GF_JAIL_WINDOW, world, [
        (Regions.GERUDO_FORTRESS_OUTSKIRTS, lambda bundle: True_()),
        (Regions.GF_BELOW_CHEST, lambda bundle: True_()),
    ])

    # GF HBA Range
    # Locations
    add_locations(Regions.GF_HBA_RANGE, world, [
        (Locations.GF_HBA_1000_POINTS,
         lambda bundle: is_adult(bundle) & has_item(Items.CHILD_WALLET, bundle) & has_item(
             Items.GERUDO_MEMBERSHIP_CARD, bundle) & can_use(Items.EPONA, bundle) & can_use(Items.FAIRY_BOW,
                                                                                                bundle) & at_day(
             bundle)),
        (Locations.GF_HBA_1500_POINTS,
         lambda bundle: is_adult(bundle) & has_item(Items.CHILD_WALLET, bundle) & has_item(
             Items.GERUDO_MEMBERSHIP_CARD, bundle) & can_use(Items.EPONA, bundle) & can_use(Items.FAIRY_BOW,
                                                                                                bundle) & at_day(
             bundle)),
        (Locations.GF_GS_ARCHERY_RANGE,
         lambda bundle: is_adult(bundle) & can_get_enemy_drop(bundle, Enemies.GOLD_SKULLTULA,
                                                                EnemyDistance.BOOMERANG) & can_get_nighttime_gs(
             bundle)),
        (Locations.GF_HBA_RANGE_CRATE_1, lambda bundle: can_break_crates(bundle)),
        (Locations.GF_HBA_RANGE_CRATE_2, lambda bundle: can_break_crates(bundle)),
        (Locations.GF_HBA_RANGE_CRATE_3, lambda bundle: can_break_crates(bundle)),
        (Locations.GF_HBA_RANGE_CRATE_4, lambda bundle: can_break_crates(bundle)),
        (Locations.GF_HBA_RANGE_CRATE_5, lambda bundle: can_break_crates(bundle)),
        (Locations.GF_HBA_RANGE_CRATE_6, lambda bundle: can_break_crates(bundle)),
        (Locations.GF_HBA_RANGE_CRATE_7, lambda bundle: can_break_crates(bundle)),
        (Locations.GF_HBA_CANOPY_EAST_CRATE,
         lambda bundle: can_break_crates(bundle)),
        (Locations.GF_HBA_CANOPY_WEST_CRATE,
         lambda bundle: can_break_crates(bundle)),
        (Locations.GF_NORTH_TARGET_EAST_CRATE,
         lambda bundle: can_break_crates(bundle)),
        (Locations.GF_NORTH_TARGET_WEST_CRATE, lambda bundle: is_adult(bundle) | (
            blast_or_smash(bundle) | hookshot_or_boomerang(bundle) | can_use(Items.HOVER_BOOTS, bundle))),
        (Locations.GF_NORTH_TARGET_CHILD_CRATE,
         lambda bundle: is_child(bundle) & blast_or_smash(bundle)),
        (Locations.GF_SOUTH_TARGET_EAST_CRATE,
         lambda bundle: can_break_crates(bundle)),
        (Locations.GF_SOUTH_TARGET_WEST_CRATE,
         lambda bundle: can_break_crates(bundle)),
    ])
    # Connections
    connect_regions(Regions.GF_HBA_RANGE, world, [
        (Regions.GF_OUTSIDE_GTG, lambda bundle: is_child(bundle)
         | has_item(Items.GERUDO_MEMBERSHIP_CARD, bundle)),
    ])

    # GF Outside Gate
    # Events
    add_events(Regions.GF_OUTSIDE_GATE, world, [
        (EventLocations.GF_GATE_OUTSIDE, LocalEvents.GF_GATE_OPEN,
         lambda bundle: is_adult(bundle) & has_item(Items.GERUDO_MEMBERSHIP_CARD, bundle)),
    ])
    # Connections
    connect_regions(Regions.GF_OUTSIDE_GATE, world, [
        (Regions.GERUDO_FORTRESS_OUTSKIRTS, lambda bundle: has_item(
            LocalEvents.GF_GATE_OPEN, bundle)),
        (Regions.WASTELAND_NEAR_FORTRESS, lambda bundle: True_()),
    ])

    # GF Storms Grotto
    # Events
    add_events(Regions.GF_STORMS_GROTTO, world, [
        (EventLocations.GF_STORMS_GROTTO_FAIRY,
         Events.CAN_ACCESS_FAIRIES, lambda bundle: True_()),
    ])
    # Locations
    add_locations(Regions.GF_STORMS_GROTTO, world, [
        (Locations.GF_FAIRY_GROTTO_FAIRY1, lambda bundle: True_()),
        (Locations.GF_FAIRY_GROTTO_FAIRY2, lambda bundle: True_()),
        (Locations.GF_FAIRY_GROTTO_FAIRY3, lambda bundle: True_()),
        (Locations.GF_FAIRY_GROTTO_FAIRY4, lambda bundle: True_()),
        (Locations.GF_FAIRY_GROTTO_FAIRY5, lambda bundle: True_()),
        (Locations.GF_FAIRY_GROTTO_FAIRY6, lambda bundle: True_()),
        (Locations.GF_FAIRY_GROTTO_FAIRY7, lambda bundle: True_()),
        (Locations.GF_FAIRY_GROTTO_FAIRY8, lambda bundle: True_()),
    ])
    # Connections
    connect_regions(Regions.GF_STORMS_GROTTO, world, [
        (Regions.GF_NEAR_GROTTO, lambda bundle: True_()),
    ])
