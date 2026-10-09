from typing import TYPE_CHECKING
from BaseClasses import MultiWorld, Region, LocationProgressType
from rule_builder.rules import True_
from .Enums import Ages, HostEvents, Items, Locations
from .Locations import SohLocation, location_data_table, scrubs_one_time_only
from .ship_data_gen import SHIP_LOCATIONS, ShipLocation, CheckType, DUNGEON_SMALL_KEYS
from .enums_gen import Regions
from .LogicHelpers import add_host_events, add_events, is_pruned
from .regions_gen import set_region_rules
from .SongShuffle import song_vanilla_locations, get_shuffled_songs
from .ShopItems import no_shop_shuffle

if TYPE_CHECKING:
    from . import SohWorld


class SohRegion(Region):
    game = "Ship of Harkinian"

    def __init__(self, name: str, player: int, multiworld: MultiWorld, hint: str | None = None):
        super().__init__(name, player, multiworld, hint)

    def can_reach(self, state) -> bool:
        if state._soh_stale[self.player]:
            stored_age = state._soh_age[self.player]
            state._soh_update_age_reachable_regions(self.player)
            state._soh_age[self.player] = stored_age

        if state._soh_age[self.player] == Ages.CHILD:
            return self in state._soh_child_reachable_regions[self.player]
        elif state._soh_age[self.player] == Ages.ADULT:
            return self in state._soh_adult_reachable_regions[self.player]
        else:
            return self in state._soh_child_reachable_regions[self.player] or self in state._soh_adult_reachable_regions[self.player]


def location_enabled(world: "SohWorld", location: Locations, data: ShipLocation) -> bool:
    """Whether this seed's options shuffle a location, decided by Ship's check type."""
    o = world.options

    def split(choice) -> bool:
        # Options offering overworld / dungeon / all, split by Ship's Location::IsDungeon.
        return choice in ("all", "dungeon" if data.dungeon else "overworld")

    # Checks with an option of their own, whatever their check type.
    if location in (Locations.RC_HC_MALON_EGG, Locations.RC_HC_ZELDAS_LETTER):
        return not o.skip_child_zelda
    if location == Locations.RC_KAK_100_GOLD_SKULLTULA_REWARD:
        return bool(o.shuffle_100_gs_reward)
    if location == Locations.RC_ZR_MAGIC_BEAN_SALESMAN:
        return o.shuffle_merchants in ("bean_merchant_only", "all")
    if location == Locations.RC_TH_FREED_CARPENTERS or data.type == CheckType.RCTYPE_GF_KEY:
        return o.fortress_carpenters == "normal" or (
            o.fortress_carpenters == "fast"
            and location in (Locations.RC_TH_FREED_CARPENTERS, Locations.RC_TH_1_TORCH_CARPENTER))

    match data.type:
        case CheckType.RCTYPE_SCRUB:
            return o.shuffle_scrubs == "all" or (o.shuffle_scrubs == "one_time_only"
                                                 and location in scrubs_one_time_only)
        case CheckType.RCTYPE_ADULT_TRADE:
            return bool(o.shuffle_adult_trade_items)
        case CheckType.RCTYPE_MERCHANT:
            return o.shuffle_merchants in ("all_but_beans", "all")
        case CheckType.RCTYPE_COW:
            return bool(o.shuffle_cows)
        case CheckType.RCTYPE_FROG_SONG:
            return bool(o.shuffle_frog_song_rupees)
        case CheckType.RCTYPE_BEEHIVE:
            return bool(o.shuffle_beehives)
        case CheckType.RCTYPE_POT:
            return split(o.shuffle_pots)
        case CheckType.RCTYPE_CRATE | CheckType.RCTYPE_SMALL_CRATE:
            return split(o.shuffle_crates)
        case CheckType.RCTYPE_NLCRATE:
            return bool(o.true_no_logic) and o.shuffle_crates in ("overworld", "all")
        case CheckType.RCTYPE_TREE:
            return bool(o.shuffle_trees)
        case CheckType.RCTYPE_BUSH:
            return bool(o.shuffle_bushes)
        case CheckType.RCTYPE_NLTREE:
            return bool(o.true_no_logic and o.shuffle_trees)
        case CheckType.RCTYPE_FREESTANDING:
            return split(o.shuffle_freestanding_items)
        case CheckType.RCTYPE_GRASS:
            return split(o.shuffle_grass)
        case CheckType.RCTYPE_FOUNTAIN_FAIRY:
            return bool(o.shuffle_fountain_fairies)
        case CheckType.RCTYPE_STONE_FAIRY:
            return bool(o.shuffle_stone_fairies)
        case CheckType.RCTYPE_BEAN_FAIRY:
            return bool(o.shuffle_bean_fairies)
        case CheckType.RCTYPE_SONG_FAIRY:
            return bool(o.shuffle_song_fairies)
        case CheckType.RCTYPE_FISH:
            return o.shuffle_fish in ("all", "pond" if data.scene == "SCENE_FISHING_POND" else "overworld")
        case CheckType.RCTYPE_LINKS_POCKET:
            return o.start_with_links_pocket != "nothing"
    return True


def materialize_locations(world: "SohWorld") -> list[str]:
    pending, world._soh_pending_locations = world._soh_pending_locations, {}
    dropped: list[str] = []

    events = _location_events(world)
    for location, claims in pending.items():
        name = str(location)
        if name not in world.included_locations:
            # Not a check this seed. Check if it still matters
            if event := events.get(location):
                for parent, rule in claims:
                    event_name = name if len(claims) == 1 else f"{name} ({parent})"
                    add_events(parent, world, [(event_name, event, rule)])
            continue

        if world.options.true_no_logic:
            edges = [(claims[0][0], True_())]
        else:
            edges = [(parent, built) for parent, rule in claims
                     if not is_pruned(built := rule((parent, world)), world)]

        if not edges:
            dropped.append(name)
            continue

        # Determine if location is in one more more regions
        if len(edges) == 1:
            parent, rule = edges[0]
            region = world.get_region(str(parent))
        else:
            rule = None
            region = SohRegion(f"{name} (Access)", world.player, world.multiworld)
            world.multiworld.regions.append(region)
            for parent, built in edges:
                world.create_entrance(world.get_region(str(parent)), region, built)

        region.add_locations({name: world.included_locations.pop(location).loc_id}, SohLocation)
        if rule is not None:
            world.set_rule(world.get_location(name), rule)

    return dropped


def _location_events(world: "SohWorld") -> dict:
    victory = Locations.RC_TRIFORCE_COMPLETED if world.options.triforce_hunt else Locations.RC_GANON
    return {
        victory: HostEvents.GAME_COMPLETED,
        Locations.RC_ZR_MAGIC_BEAN_SALESMAN: HostEvents.CAN_BUY_BEANS,  # sells beans unless shuffled
    }


def create_regions_and_locations(world: "SohWorld") -> None:
    for region_name in Regions:
        if region_name != Regions.RR_NONE:
            world.multiworld.regions.append(SohRegion(region_name, world.player, world.multiworld))

    world.included_locations.update({name: data for name, data in location_data_table.items()
                                     if location_enabled(world, name, SHIP_LOCATIONS[name])})

    # Set region rules and location rules after all locations are created
    set_region_rules(world)
    materialize_locations(world)
    add_host_events(world)


# Create a dictionary mapping blue warp rewards to their vanilla items
dungeon_reward_item_mapping = {
    Locations.RC_QUEEN_GOHMA: Items.RG_KOKIRI_EMERALD,
    Locations.RC_KING_DODONGO: Items.RG_GORON_RUBY,
    Locations.RC_BARINADE: Items.RG_ZORA_SAPPHIRE,
    Locations.RC_PHANTOM_GANON: Items.RG_FOREST_MEDALLION,
    Locations.RC_VOLVAGIA: Items.RG_FIRE_MEDALLION,
    Locations.RC_MORPHA: Items.RG_WATER_MEDALLION,
    Locations.RC_BONGO_BONGO: Items.RG_SHADOW_MEDALLION,
    Locations.RC_TWINROVA: Items.RG_SPIRIT_MEDALLION,
    Locations.RC_LINKS_POCKET: Items.RG_LIGHT_MEDALLION
}


dungeon_boss_keys = [Items.RG_FOREST_TEMPLE_BOSS_KEY, Items.RG_FIRE_TEMPLE_BOSS_KEY, Items.RG_WATER_TEMPLE_BOSS_KEY,
                     Items.RG_SPIRIT_TEMPLE_BOSS_KEY, Items.RG_SHADOW_TEMPLE_BOSS_KEY]

maps_and_compasses = [
    Items.RG_DEKU_TREE_MAP, Items.RG_DEKU_TREE_COMPASS,
    Items.RG_DODONGOS_CAVERN_MAP, Items.RG_DODONGOS_CAVERN_COMPASS,
    Items.RG_JABU_JABUS_BELLY_MAP, Items.RG_JABU_JABUS_BELLY_COMPASS,
    Items.RG_FOREST_TEMPLE_MAP, Items.RG_FOREST_TEMPLE_COMPASS,
    Items.RG_FIRE_TEMPLE_MAP, Items.RG_FIRE_TEMPLE_COMPASS,
    Items.RG_WATER_TEMPLE_MAP, Items.RG_WATER_TEMPLE_COMPASS,
    Items.RG_SPIRIT_TEMPLE_MAP, Items.RG_SPIRIT_TEMPLE_COMPASS,
    Items.RG_SHADOW_TEMPLE_MAP, Items.RG_SHADOW_TEMPLE_COMPASS,
    Items.RG_BOTTOM_OF_THE_WELL_MAP, Items.RG_BOTTOM_OF_THE_WELL_COMPASS,
    Items.RG_ICE_CAVERN_MAP, Items.RG_ICE_CAVERN_COMPASS,
]


SMALL_KEY_BY_AREA = {dungeon: key for key, (dungeon, _, _) in DUNGEON_SMALL_KEYS.items()}


def place_vanilla_items(world: "SohWorld", types: set[CheckType]) -> None:
    for location in world.get_locations():
        data = SHIP_LOCATIONS.get(location.name)
        if data and data.type in types and location.item is None:
            item = SMALL_KEY_BY_AREA[data.area] if data.type == CheckType.RCTYPE_SMALL_KEY else data.vanilla_item
            place_locked_item(location.name, item, world)


def place_locked_item(location: Locations, item: Items, world: "SohWorld") -> None:
    soh_item = world.create_item(item)
    world.get_location(location).place_locked_item(soh_item)
    world.preplaced_items.append(soh_item)

def place_locked_items(world: "SohWorld") -> None:
    if world.options.start_with_links_pocket == "advancement":
        world.get_location(Locations.RC_LINKS_POCKET).progress_type = LocationProgressType.PRIORITY

    # If skip_child_zelda, connect the locations to root and push items precollected
    if not world.options.skip_child_zelda:
        # Zeldas Letter gets placed to it's location
        place_locked_item(Locations.RC_HC_ZELDAS_LETTER, Items.RG_ZELDAS_LETTER, world)
        # If not skip_child_zelda and not shuffle_weird_egg, place the weird egg
        if not world.options.shuffle_weird_egg:
            place_locked_item(Locations.RC_HC_MALON_EGG, Items.RG_WEIRD_EGG, world)
    else:
        world.push_precollected(world.create_item(Items.RG_ZELDAS_LETTER, True))
        world.push_precollected(world.create_item(Items.RG_WEIRD_EGG, True))

        
    if world.options.shuffle_songs == "off":
        for location, song in song_vanilla_locations.items():
            included_songs = get_shuffled_songs(world)
            if song not in included_songs:
                continue
            place_locked_item(location, song, world)

    # Place Kokiri Sword on vanilla location if not shuffled
    if not world.options.shuffle_kokiri_sword and not world.options.start_with_kokiri_sword:
        place_locked_item(Locations.RC_KF_KOKIRI_SWORD_CHEST, Items.RG_KOKIRI_SWORD, world)

    # Place Master Sword on vanilla location if not shuffled
    if not world.options.shuffle_master_sword:
        if world.options.starting_age == "adult" or world.options.start_with_master_sword:
            # Start with the master sword in your starting inventory
            world.multiworld.push_precollected(world.create_item(Items.RG_MASTER_SWORD, create_as_event=True))

        # place locked mastersword so this location doesn't get counted as an empty location
        world.get_location(Locations.RC_TOT_MASTER_SWORD).place_locked_item(
            world.create_item(Items.RG_MASTER_SWORD, create_as_event=True))
        world.get_location(Locations.RC_TOT_MASTER_SWORD).address = None
        
    # Place the Ocarinas on their vanilla locations if not shuffled
    if not world.options.shuffle_ocarinas:
        if world.options.start_with_ocarina == "off":
            place_locked_item(Locations.RC_LW_GIFT_FROM_SARIA, Items.RG_PROGRESSIVE_OCARINA, world)
        if world.options.start_with_ocarina != "ocarina_of_time":
            place_locked_item(Locations.RC_HF_OCARINA_OF_TIME_ITEM, Items.RG_PROGRESSIVE_OCARINA, world)

        
    # place the gerudo membership card
    if not world.options.shuffle_gerudo_membership_card:
        if world.options.fortress_carpenters == "free":
            # start with the membership card
            world.multiworld.push_precollected(world.create_item(Items.RG_GERUDO_MEMBERSHIP_CARD, create_as_event=True))
        else:
            # Place the Gerudo Membership Card on vanilla location if not shuffled
            place_locked_item(Locations.RC_TH_FREED_CARPENTERS, Items.RG_GERUDO_MEMBERSHIP_CARD, world)

    # Preplace dungeon rewards in vanilla locations when not shuffled
    if world.options.shuffle_dungeon_rewards == "off":
        # Loop through dungeons rewards and set their items to the vanilla reward.
        for location_name, reward_name in zip(dungeon_reward_item_mapping.keys(), dungeon_reward_item_mapping.values()):
            place_locked_item(location_name, reward_name, world)
    elif world.options.shuffle_dungeon_rewards != "end_of_dungeons":
        if world.options.start_with_links_pocket == "dungeon_reward":
            dungeon_rewards = list(dungeon_reward_item_mapping.values())
            world.random.shuffle(dungeon_rewards)
            place_locked_item(Locations.RC_LINKS_POCKET, dungeon_rewards[0], world)

    # Place Ganons Boss Key
    if not world.options.ganons_castle_boss_key == "vanilla" and not world.options.ganons_castle_boss_key == "anywhere" and not world.options.triforce_hunt:
        place_locked_item(Locations.RC_TOT_LIGHT_ARROWS_CUTSCENE, Items.RG_GANONS_CASTLE_BOSS_KEY, world)

    if world.options.ganons_castle_boss_key == "vanilla" and not world.options.triforce_hunt:
        place_locked_item(Locations.RC_GANONS_TOWER_BOSS_KEY_CHEST, Items.RG_GANONS_CASTLE_BOSS_KEY, world)

    # Place vanilla shop items if they're not shuffled
    if not world.options.shuffle_shops:
        no_shop_shuffle(world)

    # Preplace tokens based on settings.
    token_overworld = world.options.shuffle_skull_tokens in ("off", "dungeon")
    token_dungeon = world.options.shuffle_skull_tokens in ("off", "overworld")
    for location in world.get_locations():
        data = SHIP_LOCATIONS.get(location.name)
        if data and data.type == CheckType.RCTYPE_SKULL_TOKEN and (token_dungeon if data.dungeon else token_overworld):
            location.place_locked_item(world.create_item(Items.RG_GOLD_SKULLTULA_TOKEN, True))
            location.address = None
            location.item.code = None

    vanilla: set[CheckType] = set()
    if world.options.boss_key_shuffle == "vanilla":
        vanilla.add(CheckType.RCTYPE_BOSS_KEY)
    if world.options.small_key_shuffle == "vanilla":
        vanilla.add(CheckType.RCTYPE_SMALL_KEY)
    if world.options.maps_and_compasses == "vanilla":
        vanilla |= {CheckType.RCTYPE_MAP, CheckType.RCTYPE_COMPASS}
    place_vanilla_items(world, vanilla)

    # Gerudo Fortress Keys
    if world.options.fortress_carpenters != "free" and world.options.gerudo_fortress_key_shuffle == "vanilla":
        if world.options.fortress_carpenters != "fast":
            for location in (Locations.RC_TH_1_TORCH_CARPENTER, Locations.RC_TH_DEAD_END_CARPENTER, Locations.RC_TH_DOUBLE_CELL_CARPENTER, Locations.RC_TH_STEEP_SLOPE_CARPENTER):
                place_locked_item(location, Items.RG_GERUDO_FORTRESS_SMALL_KEY, world)
        else:
            place_locked_item(Locations.RC_TH_1_TORCH_CARPENTER, Items.RG_GERUDO_FORTRESS_SMALL_KEY, world)
