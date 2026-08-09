from typing import TYPE_CHECKING

from .Enums import *
from .Items import item_data_table, filler_items, no_rules_bottles, SohItem
from .Regions import dungeon_reward_item_mapping, small_key_vanilla_mapping, dungeon_boss_key_vanilla_mapping
from .LogicHelpers import key_to_ring
from .KeyShuffle import small_key_option_matching
from BaseClasses import ItemClassification
from .SongShuffle import song_vanilla_locations, get_shuffled_songs
from .ShopItems import get_vanilla_shop_pool

if TYPE_CHECKING:
    from . import SohWorld


def create_item_pool(world: "SohWorld") -> None:
    items_to_create: dict[str, int] = {
        item: data.quantity_in_item_pool for item, data in item_data_table.items()}

    # King Zora
    if world.options.zoras_fountain == "open":
        items_to_create[Items.BOTTLE_WITH_RUTOS_LETTER] = 0

    # Overworld door keys
    if world.options.lock_overworld_doors:
        items_to_create[Items.GUARD_HOUSE_KEY] = 1
        items_to_create[Items.MARKET_BAZAAR_KEY] = 1
        items_to_create[Items.MARKET_POTION_SHOP_KEY] = 1
        items_to_create[Items.MASK_SHOP_KEY] = 1
        items_to_create[Items.MARKET_SHOOTING_GALLERY_KEY] = 1
        items_to_create[Items.BOMBCHU_BOWLING_KEY] = 1
        items_to_create[Items.TREASURE_CHEST_GAME_BUILDING_KEY] = 1
        items_to_create[Items.BOMBCHU_SHOP_KEY] = 1
        items_to_create[Items.RICHARDS_HOUSE_KEY] = 1
        items_to_create[Items.ALLEY_HOUSE_KEY] = 1
        items_to_create[Items.KAK_BAZAAR_KEY] = 1
        items_to_create[Items.KAK_POTION_SHOP_KEY] = 1
        items_to_create[Items.BOSS_HOUSE_KEY] = 1
        items_to_create[Items.GRANNYS_POTION_SHOP_KEY] = 1
        items_to_create[Items.SKULLTULA_HOUSE_KEY] = 1
        items_to_create[Items.IMPAS_HOUSE_KEY] = 1
        items_to_create[Items.WINDMILL_KEY] = 1
        items_to_create[Items.KAK_SHOOTING_GALLERY_KEY] = 1
        items_to_create[Items.DAMPES_HUT_KEY] = 1
        items_to_create[Items.TALONS_HOUSE_KEY] = 1
        items_to_create[Items.STABLES_KEY] = 1
        items_to_create[Items.BACK_TOWER_KEY] = 1
        items_to_create[Items.HYLIA_LAB_KEY] = 1
        items_to_create[Items.FISHING_HOLE_KEY] = 1

    # Gerudo Fortress Keys
    if world.options.fortress_carpenters == "fast":
        items_to_create[Items.GERUDO_FORTRESS_SMALL_KEY] = 1

    if world.options.fortress_carpenters == "free":
        items_to_create[Items.GERUDO_FORTRESS_SMALL_KEY] = 0

    # Overworld Skull Tokens
    if world.options.shuffle_skull_tokens == "overworld" or world.options.shuffle_skull_tokens == "all":
        items_to_create[Items.GOLD_SKULLTULA_TOKEN] += int(
            TokenCounts.OVERWORLD)

    # Dungeon Skull Tokens
    if world.options.shuffle_skull_tokens == "dungeon" or world.options.shuffle_skull_tokens == "all":
        items_to_create[Items.GOLD_SKULLTULA_TOKEN] += int(TokenCounts.DUNGEON)

    # Kokiri Sword
    if world.options.shuffle_kokiri_sword and not world.options.start_with_kokiri_sword:
        items_to_create[Items.KOKIRI_SWORD] = 1

    # Master Sword
    if world.options.shuffle_master_sword and not world.options.start_with_master_sword:
        items_to_create[Items.MASTER_SWORD] = 1

    # Child's Wallet
    if world.options.shuffle_childs_wallet:
        items_to_create[Items.PROGRESSIVE_WALLET] += 1

    # Tycoon Wallet
    if world.options.shuffle_tycoon_wallet:
        items_to_create[Items.PROGRESSIVE_WALLET] += 1

    # Fiary Ocarina and Ocarina of time
    if world.options.shuffle_ocarinas:
        if world.options.start_with_ocarina == "off":
            items_to_create[Items.PROGRESSIVE_OCARINA] = 2
        if world.options.start_with_ocarina == "fairy_ocarina":
            items_to_create[Items.PROGRESSIVE_OCARINA] = 1

    # Songs
    if world.options.shuffle_songs == "anywhere":
        for song in get_shuffled_songs(world):
            items_to_create[song] = 1

    # Ocarina Buttons
    if world.options.shuffle_ocarina_buttons:
        items_to_create[Items.OCARINA_A_BUTTON] = 1
        items_to_create[Items.OCARINA_CDOWN_BUTTON] = 1
        items_to_create[Items.OCARINA_CLEFT_BUTTON] = 1
        items_to_create[Items.OCARINA_CRIGHT_BUTTON] = 1
        items_to_create[Items.OCARINA_CUP_BUTTON] = 1

    # Swim
    if world.options.shuffle_swim:
        items_to_create[Items.PROGRESSIVE_SCALE] += 1

    # Weird Egg
    if not world.options.skip_child_zelda and world.options.shuffle_weird_egg:
        items_to_create[Items.WEIRD_EGG] = 1

    # Gerudo Membership Card
    if world.options.shuffle_gerudo_membership_card:
        items_to_create[Items.GERUDO_MEMBERSHIP_CARD] = 1

    # Fishing Pole
    if world.options.shuffle_fishing_pole:
        items_to_create[Items.FISHING_POLE] = 1

    # Deku Stick Bag
    if world.options.shuffle_deku_stick_bag:
        items_to_create[Items.PROGRESSIVE_STICK_CAPACITY] += 1

    # Deku Nut Bag
    if world.options.shuffle_deku_nut_bag:
        items_to_create[Items.PROGRESSIVE_NUT_CAPACITY] += 1

    # Merchants
    if world.options.shuffle_merchants in ("all", "bean_merchant_only") and not world.options.start_with_magic_beans:
        items_to_create[Items.MAGIC_BEAN_PACK] = 1

    if world.options.shuffle_merchants in ("all", "all_but_beans"):
        items_to_create[Items.GIANTS_KNIFE] = 1

    # Adult Trade Items
    if world.options.shuffle_adult_trade_items:
        items_to_create[Items.POCKET_EGG] = 1
        items_to_create[Items.COJIRO] = 1
        items_to_create[Items.ODD_MUSHROOM] = 1
        items_to_create[Items.ODD_POTION] = 1
        items_to_create[Items.POACHERS_SAW] = 1
        items_to_create[Items.BROKEN_GORONS_SWORD] = 1
        items_to_create[Items.PRESCRIPTION] = 1
        items_to_create[Items.EYEBALL_FROG] = 1
        items_to_create[Items.WORLDS_FINEST_EYEDROPS] = 1

    # Boss Souls
    if world.options.shuffle_boss_souls:
        items_to_create[Items.GOHMAS_SOUL] = 1
        items_to_create[Items.KING_DODONGOS_SOUL] = 1
        items_to_create[Items.BARINADES_SOUL] = 1
        items_to_create[Items.PHANTOM_GANONS_SOUL] = 1
        items_to_create[Items.VOLVAGIAS_SOUL] = 1
        items_to_create[Items.MORPHAS_SOUL] = 1
        items_to_create[Items.BONGO_BONGOS_SOUL] = 1
        items_to_create[Items.TWINROVAS_SOUL] = 1

    if world.options.shuffle_boss_souls == "on_plus_ganons":
        items_to_create[Items.GANONS_SOUL] = 1

    # Dungeon Rewards
    if world.options.shuffle_dungeon_rewards == "anywhere":
        # remove potentially pre-placed pocket item
        pocket_item = None
        if world.options.start_with_links_pocket != "nothing":
            placed_item = world.get_location(Locations.LINKS_POCKET).item
            if placed_item:
                pocket_item = Items(placed_item.name)
        for reward in dungeon_reward_item_mapping.values():
            if reward == pocket_item:
                continue
            items_to_create[reward] = 1

    # Maps and Compasses
    if world.options.maps_and_compasses == "anywhere":
        items_to_create[Items.GREAT_DEKU_TREE_MAP] = 1
        items_to_create[Items.DODONGOS_CAVERN_MAP] = 1
        items_to_create[Items.JABU_JABUS_BELLY_MAP] = 1
        items_to_create[Items.FOREST_TEMPLE_MAP] = 1
        items_to_create[Items.FIRE_TEMPLE_MAP] = 1
        items_to_create[Items.WATER_TEMPLE_MAP] = 1
        items_to_create[Items.SPIRIT_TEMPLE_MAP] = 1
        items_to_create[Items.SHADOW_TEMPLE_MAP] = 1
        items_to_create[Items.BOTTOM_OF_THE_WELL_MAP] = 1
        items_to_create[Items.ICE_CAVERN_MAP] = 1
        items_to_create[Items.GREAT_DEKU_TREE_COMPASS] = 1
        items_to_create[Items.DODONGOS_CAVERN_COMPASS] = 1
        items_to_create[Items.JABU_JABUS_BELLY_COMPASS] = 1
        items_to_create[Items.FOREST_TEMPLE_COMPASS] = 1
        items_to_create[Items.FIRE_TEMPLE_COMPASS] = 1
        items_to_create[Items.WATER_TEMPLE_COMPASS] = 1
        items_to_create[Items.SPIRIT_TEMPLE_COMPASS] = 1
        items_to_create[Items.SHADOW_TEMPLE_COMPASS] = 1
        items_to_create[Items.BOTTOM_OF_THE_WELL_COMPASS] = 1
        items_to_create[Items.ICE_CAVERN_COMPASS] = 1

    # Ganon's Castle Boss Key
    if world.options.ganons_castle_boss_key == "anywhere" and not world.options.triforce_hunt:
        items_to_create[Items.GANONS_CASTLE_BOSS_KEY] = 1

    # Keys
    if world.options.small_key_shuffle == "anywhere":
        if world.options.forest_temple_key_ring:
            items_to_create[Items.FOREST_TEMPLE_SMALL_KEY] = 0
            items_to_create[Items.FOREST_TEMPLE_KEY_RING] = 1

        if world.options.fire_temple_key_ring:
            items_to_create[Items.FIRE_TEMPLE_SMALL_KEY] = 0
            items_to_create[Items.FIRE_TEMPLE_KEY_RING] = 1

        if world.options.water_temple_key_ring:
            items_to_create[Items.WATER_TEMPLE_SMALL_KEY] = 0
            items_to_create[Items.WATER_TEMPLE_KEY_RING] = 1

        if world.options.spirit_temple_key_ring:
            items_to_create[Items.SPIRIT_TEMPLE_SMALL_KEY] = 0
            items_to_create[Items.SPIRIT_TEMPLE_KEY_RING] = 1

        if world.options.shadow_temple_key_ring:
            items_to_create[Items.SHADOW_TEMPLE_SMALL_KEY] = 0
            items_to_create[Items.SHADOW_TEMPLE_KEY_RING] = 1

        if world.options.bottom_of_the_well_key_ring:
            items_to_create[Items.BOTTOM_OF_THE_WELL_SMALL_KEY] = 0
            items_to_create[Items.BOTTOM_OF_THE_WELL_KEY_RING] = 1

        if world.options.gerudo_training_ground_key_ring:
            items_to_create[Items.TRAINING_GROUND_SMALL_KEY] = 0
            items_to_create[Items.TRAINING_GROUND_KEY_RING] = 1

        if world.options.ganons_castle_key_ring:
            items_to_create[Items.GANONS_CASTLE_SMALL_KEY] = 0
            items_to_create[Items.GANONS_CASTLE_KEY_RING] = 1

    else:
        items_to_create[Items.FOREST_TEMPLE_SMALL_KEY] = 0
        items_to_create[Items.FIRE_TEMPLE_SMALL_KEY] = 0
        items_to_create[Items.WATER_TEMPLE_SMALL_KEY] = 0
        items_to_create[Items.SPIRIT_TEMPLE_SMALL_KEY] = 0
        items_to_create[Items.SHADOW_TEMPLE_SMALL_KEY] = 0
        items_to_create[Items.BOTTOM_OF_THE_WELL_SMALL_KEY] = 0
        items_to_create[Items.TRAINING_GROUND_SMALL_KEY] = 0
        items_to_create[Items.GANONS_CASTLE_SMALL_KEY] = 0

    # Gerudo Fortress Keys
    if world.options.gerudo_fortress_key_shuffle == "anywhere":
        if world.options.gerudo_fortress_key_ring:
            items_to_create[Items.GERUDO_FORTRESS_SMALL_KEY] = 0
            items_to_create[Items.GERUDO_FORTRESS_KEY_RING] = 1
    else:
        items_to_create[Items.GERUDO_FORTRESS_SMALL_KEY] = 0

    # Boss Keys
    if world.options.boss_key_shuffle != "anywhere":
        items_to_create[Items.FOREST_TEMPLE_BOSS_KEY] = 0
        items_to_create[Items.FIRE_TEMPLE_BOSS_KEY] = 0
        items_to_create[Items.WATER_TEMPLE_BOSS_KEY] = 0
        items_to_create[Items.SPIRIT_TEMPLE_BOSS_KEY] = 0
        items_to_create[Items.SHADOW_TEMPLE_BOSS_KEY] = 0

    # Big Poe Bottle
    if world.options.big_poe_target_count == 0:
        items_to_create[Items.BOTTLE_WITH_BIG_POE] = 0

    # Bombchu bag
    if world.options.bombchu_bag == "single_bag":
        items_to_create[Items.BOMBCHUS_5] = 0
        items_to_create[Items.BOMBCHUS_10] = 0
        items_to_create[Items.BOMBCHUS_20] = 0
        if world.options.shuffle_merchants in ("all_but_beans", "all"):
            items_to_create[Items.BOMBCHU_BAG] = 6
        else:
            items_to_create[Items.BOMBCHU_BAG] = 5
    elif world.options.bombchu_bag == "progressive_bags":
        items_to_create[Items.BOMBCHU_BAG] = 3

    # Infinite Upgrades
    if world.options.infinite_upgrades == "progressive":
        items_to_create[Items.PROGRESSIVE_BOMB_BAG] += 1
        items_to_create[Items.PROGRESSIVE_BOW] += 1
        items_to_create[Items.PROGRESSIVE_NUT_CAPACITY] += 1
        items_to_create[Items.PROGRESSIVE_SLINGSHOT] += 1
        items_to_create[Items.PROGRESSIVE_STICK_CAPACITY] += 1
        items_to_create[Items.PROGRESSIVE_MAGIC_METER] += 1
        items_to_create[Items.PROGRESSIVE_WALLET] += 1
        if world.options.bombchu_bag == "progressive_bags":
            items_to_create[Items.BOMBCHU_BAG] += 1

    # Skeleton Key
    if world.options.skeleton_key:
        items_to_create[Items.SKELETON_KEY] = 1

    # Roc's Feather
    if world.options.rocs_feather:
        items_to_create[Items.ROCS_FEATHER] = 1

    # Max Hearts logic for Item Pool
    max_hearts: int = 20
    if world.options.item_pool == "scarce":
        max_hearts = 12
    elif world.options.item_pool == "minimal":
        max_hearts = 3

    starting_hearts: int = world.multiworld.state.soh_heart_count[world.player]
    if starting_hearts < max_hearts:
        items_to_create[Items.PIECE_OF_HEART_WINNER] = 1
        items_to_create[Items.PIECE_OF_HEART] = 3
        starting_hearts += 1
        if starting_hearts < max_hearts:
            hearts_to_place: int = max_hearts - starting_hearts
            if world.options.item_pool in ("plentiful", "minimal"):
                items_to_create[Items.HEART_CONTAINER] = hearts_to_place
            elif world.options.item_pool == "balanced":
                half_hearts: int = int(hearts_to_place / 2)
                items_to_create[Items.HEART_CONTAINER] = hearts_to_place - half_hearts
                items_to_create[Items.PIECE_OF_HEART] += half_hearts * 4
            elif world.options.item_pool == "scarce":
                items_to_create[Items.PIECE_OF_HEART] += hearts_to_place * 4

    # Item Pool Modifications
    if world.options.item_pool.value:
        if world.options.item_pool == "plentiful":
            # This plentiful stuff we might want to add to when we check these above. For simplicity I'll recheck stuff here for now
            if world.options.shuffle_ocarinas and not world.options.start_with_ocarina == "ocarina_of_time":
                items_to_create[Items.PROGRESSIVE_OCARINA] += 1

            if world.options.shuffle_merchants in ("all", "bean_merchant_only") and not world.options.start_with_magic_beans:
                items_to_create[Items.MAGIC_BEAN_PACK] += 1

            if world.options.shuffle_skull_tokens:
                items_to_create[Items.GOLD_SKULLTULA_TOKEN] += 10

            if world.options.gerudo_fortress_key_ring and world.options.fortress_carpenters == "normal":
                items_to_create[Items.GERUDO_FORTRESS_KEY_RING] += 1
            else:
                items_to_create[Items.GERUDO_FORTRESS_SMALL_KEY] += 1

            if world.options.shuffle_gerudo_membership_card:
                items_to_create[Items.GERUDO_MEMBERSHIP_CARD] += 1

            if world.options.bombchu_bag in ("single_bag", "progressive_bags"):
                items_to_create[Items.BOMBCHU_BAG] += 1

            items_to_create[Items.BOOMERANG] += 1
            items_to_create[Items.LENS_OF_TRUTH] += 1
            items_to_create[Items.MEGATON_HAMMER] += 1
            items_to_create[Items.IRON_BOOTS] += 1
            items_to_create[Items.GORON_TUNIC] += 1
            items_to_create[Items.ZORA_TUNIC] += 1
            items_to_create[Items.HOVER_BOOTS] += 1
            items_to_create[Items.MIRROR_SHIELD] += 1
            items_to_create[Items.STONE_OF_AGONY] += 1
            items_to_create[Items.FIRE_ARROW] += 1
            items_to_create[Items.ICE_ARROW] += 1
            items_to_create[Items.LIGHT_ARROW] += 1
            items_to_create[Items.DINS_FIRE] += 1
            items_to_create[Items.NAYRUS_LOVE] += 1
            items_to_create[Items.STRENGTH_UPGRADE] += 1
            items_to_create[Items.DOUBLE_DEFENSE] += 1
            items_to_create[Items.PROGRESSIVE_BOW] += 1
            items_to_create[Items.PROGRESSIVE_SLINGSHOT] += 1
            items_to_create[Items.PROGRESSIVE_BOMB_BAG] += 1
            items_to_create[Items.PROGRESSIVE_MAGIC_METER] += 1
            items_to_create[Items.PROGRESSIVE_WALLET] += 1
            items_to_create[Items.PROGRESSIVE_STICK_CAPACITY] += 1
            items_to_create[Items.PROGRESSIVE_NUT_CAPACITY] += 1

            if world.options.shuffle_kokiri_sword and not world.options.start_with_kokiri_sword:
                items_to_create[Items.KOKIRI_SWORD] += 1

            if world.options.shuffle_master_sword and not world.options.start_with_master_sword:
                items_to_create[Items.MASTER_SWORD] += 1

            if world.options.shuffle_weird_egg:
                items_to_create[Items.WEIRD_EGG] += 1

            if world.options.shuffle_ocarina_buttons:
                items_to_create[Items.OCARINA_A_BUTTON] += 1
                items_to_create[Items.OCARINA_CUP_BUTTON] += 1
                items_to_create[Items.OCARINA_CDOWN_BUTTON] += 1
                items_to_create[Items.OCARINA_CLEFT_BUTTON] += 1
                items_to_create[Items.OCARINA_CRIGHT_BUTTON] += 1

            items_to_create[Items.PROGRESSIVE_SCALE] += 1

            if world.options.shuffle_fishing_pole:
                items_to_create[Items.FISHING_POLE] += 1

            if world.options.shuffle_adult_trade_items:
                items_to_create[Items.POCKET_EGG] += 1
                items_to_create[Items.COJIRO] += 1
                items_to_create[Items.ODD_MUSHROOM] += 1
                items_to_create[Items.POACHERS_SAW] += 1
                items_to_create[Items.BROKEN_GORONS_SWORD] += 1
                items_to_create[Items.PRESCRIPTION] += 1
                items_to_create[Items.EYEBALL_FROG] += 1
                items_to_create[Items.WORLDS_FINEST_EYEDROPS] += 1

            items_to_create[Items.CLAIM_CHECK] += 1

            # TODO Bean Souls

            if world.options.shuffle_boss_souls:
                items_to_create[Items.GOHMAS_SOUL] += 1
                items_to_create[Items.KING_DODONGOS_SOUL] += 1
                items_to_create[Items.BARINADES_SOUL] += 1
                items_to_create[Items.PHANTOM_GANONS_SOUL] += 1
                items_to_create[Items.VOLVAGIAS_SOUL] += 1
                items_to_create[Items.MORPHAS_SOUL] += 1
                items_to_create[Items.BONGO_BONGOS_SOUL] += 1
                items_to_create[Items.TWINROVAS_SOUL] += 1
                if world.options.shuffle_boss_souls == "on_plus_ganons":
                    items_to_create[Items.GANONS_SOUL] += 1

            if world.options.lock_overworld_doors:
                items_to_create[Items.GUARD_HOUSE_KEY] += 1
                items_to_create[Items.MARKET_BAZAAR_KEY] += 1
                items_to_create[Items.MARKET_POTION_SHOP_KEY] += 1
                items_to_create[Items.MASK_SHOP_KEY] += 1
                items_to_create[Items.MARKET_SHOOTING_GALLERY_KEY] += 1
                items_to_create[Items.BOMBCHU_BOWLING_KEY] += 1
                items_to_create[Items.TREASURE_CHEST_GAME_BUILDING_KEY] += 1
                items_to_create[Items.BOMBCHU_SHOP_KEY] += 1
                items_to_create[Items.RICHARDS_HOUSE_KEY] += 1
                items_to_create[Items.ALLEY_HOUSE_KEY] += 1
                items_to_create[Items.KAK_BAZAAR_KEY] += 1
                items_to_create[Items.KAK_POTION_SHOP_KEY] += 1
                items_to_create[Items.BOSS_HOUSE_KEY] += 1
                items_to_create[Items.GRANNYS_POTION_SHOP_KEY] += 1
                items_to_create[Items.SKULLTULA_HOUSE_KEY] += 1
                items_to_create[Items.IMPAS_HOUSE_KEY] += 1
                items_to_create[Items.WINDMILL_KEY] += 1
                items_to_create[Items.KAK_SHOOTING_GALLERY_KEY] += 1
                items_to_create[Items.DAMPES_HUT_KEY] += 1
                items_to_create[Items.TALONS_HOUSE_KEY] += 1
                items_to_create[Items.STABLES_KEY] += 1
                items_to_create[Items.BACK_TOWER_KEY] += 1
                items_to_create[Items.HYLIA_LAB_KEY] += 1
                items_to_create[Items.FISHING_HOLE_KEY] += 1

            if world.options.small_key_shuffle == "anywhere":
                small_key_mapping = small_key_option_matching(world)
                for key in small_key_vanilla_mapping.keys():
                    if small_key_mapping[key].Option:
                        items_to_create[key_to_ring[key]] += 1
                    else:
                        items_to_create[key] += 1

            if world.options.boss_key_shuffle == "anywhere":
                for key in dungeon_boss_key_vanilla_mapping.values():
                    items_to_create[key] += 1

            if world.options.ganons_castle_boss_key == "anywhere":
                items_to_create[Items.GANONS_CASTLE_BOSS_KEY] += 1

            if world.options.shuffle_songs == "anywhere":
                for song in get_shuffled_songs(world):
                    items_to_create[song] += 1

        elif world.options.item_pool == "scarce":
            if world.options.bombchu_bag == "single_bag":
                items_to_create[Items.BOMBCHU_BAG] = 3
            elif world.options.bombchu_bag == "progressive_bags":
                items_to_create[Items.BOMBCHU_BAG] -= 1

            items_to_create[Items.BOMBCHUS_5] = 1
            items_to_create[Items.BOMBCHUS_10] = 2
            items_to_create[Items.BOMBCHUS_20] = 0
            items_to_create[Items.NAYRUS_LOVE] = 0
            items_to_create[Items.DOUBLE_DEFENSE] = 0

            items_to_create[Items.PROGRESSIVE_BOW] -= 1
            items_to_create[Items.PROGRESSIVE_SLINGSHOT] -= 1
            items_to_create[Items.PROGRESSIVE_BOMB_BAG] -= 1
            items_to_create[Items.PROGRESSIVE_MAGIC_METER] -= 1
            items_to_create[Items.PROGRESSIVE_STICK_CAPACITY] -= 1
            items_to_create[Items.PROGRESSIVE_NUT_CAPACITY] -= 1

        elif world.options.item_pool == "minimal":
            if world.options.bombchu_bag == "single_bag":
                items_to_create[Items.BOMBCHU_BAG] = 1
            elif world.options.bombchu_bag == "progressive_bags":
                items_to_create[Items.BOMBCHU_BAG] -= 2
            items_to_create[Items.BOMBCHUS_5] = 1
            items_to_create[Items.BOMBCHUS_10] = 0
            items_to_create[Items.BOMBCHUS_20] = 0
            items_to_create[Items.NAYRUS_LOVE] = 0
            items_to_create[Items.DOUBLE_DEFENSE] = 0

            items_to_create[Items.PROGRESSIVE_BOW] -= 2
            items_to_create[Items.PROGRESSIVE_SLINGSHOT] -= 2
            items_to_create[Items.PROGRESSIVE_BOMB_BAG] -= 2
            items_to_create[Items.PROGRESSIVE_MAGIC_METER] -= 1
            items_to_create[Items.PROGRESSIVE_STICK_CAPACITY] -= 2
            items_to_create[Items.PROGRESSIVE_NUT_CAPACITY] -= 2

    # If you start with enough hearts to do everything and tricks aren't enabled make the rest of them useful
    if not (world.options.enable_all_tricks or str(Tricks.FEWER_TUNIC_REQUIREMENTS) in world.options.tricks_in_logic.value):
        min_hearts_needed: int = 3
        if world.multiworld.state.soh_heart_count[world.player] >= min_hearts_needed:
            items_to_create[Items.PIECE_OF_HEART] -= create_special_progression_item(world, Items.PIECE_OF_HEART, ItemClassification.useful, items_to_create[Items.PIECE_OF_HEART])
            items_to_create[Items.PIECE_OF_HEART_WINNER] -= create_special_progression_item(world, Items.PIECE_OF_HEART_WINNER, ItemClassification.useful, items_to_create[Items.PIECE_OF_HEART_WINNER])
            items_to_create[Items.HEART_CONTAINER] -= create_special_progression_item(world, Items.HEART_CONTAINER, ItemClassification.useful, items_to_create[Items.HEART_CONTAINER])
        else:
             # starting health is less than min_hearts_needed
            # Get the total number of heart classifications we have to work with
            total_non_progression_hearts: int = max_hearts - min_hearts_needed

            if total_non_progression_hearts > 0:
                # Heart Piece amount to make useful. Convert to actual hearts, then convert back later
                non_progression_piece_amount: int = int((items_to_create[Items.PIECE_OF_HEART] + items_to_create[Items.PIECE_OF_HEART_WINNER]) / 4)
            
                if total_non_progression_hearts >= non_progression_piece_amount: 
                    items_to_create[Items.PIECE_OF_HEART] -= create_special_progression_item(world, Items.PIECE_OF_HEART, ItemClassification.useful, ((non_progression_piece_amount * 4) - 1))
                    items_to_create[Items.PIECE_OF_HEART_WINNER] -= create_special_progression_item(world, Items.PIECE_OF_HEART_WINNER, ItemClassification.useful, 1)

                    total_non_progression_hearts -= non_progression_piece_amount
                elif world.options.item_pool not in ("plentiful", "minimal"):
                    non_progression_piece_amount = total_non_progression_hearts
                    
                    items_to_create[Items.PIECE_OF_HEART] -= create_special_progression_item(world, Items.PIECE_OF_HEART, ItemClassification.useful, ((non_progression_piece_amount * 4) - 1))
                    items_to_create[Items.PIECE_OF_HEART_WINNER] -= create_special_progression_item(world, Items.PIECE_OF_HEART_WINNER, ItemClassification.useful, 1)

                    total_non_progression_hearts = 0

                # Container amount to make useful
                if total_non_progression_hearts >= items_to_create[Items.HEART_CONTAINER]:
                    items_to_create[Items.HEART_CONTAINER] -= create_special_progression_item(world, Items.HEART_CONTAINER, ItemClassification.useful, items_to_create[Items.HEART_CONTAINER])
                else:
                    items_to_create[Items.HEART_CONTAINER] -= create_special_progression_item(world, Items.HEART_CONTAINER, ItemClassification.useful, total_non_progression_hearts)

    # if Greg isn't necessary to win, make him filler
    if not (world.options.rainbow_bridge == "greg" or (world.options.rainbow_bridge and world.options.rainbow_bridge_greg_modifier) or (world.options.ganons_castle_boss_key and world.options.ganons_castle_boss_key_greg_modifier)):
        items_to_create[Items.GREG_THE_GREEN_RUPEE] -= create_special_progression_item(
            world, Items.GREG_THE_GREEN_RUPEE, ItemClassification.filler)

    # Stone of Agony is Progression unless not required for Grottos
    if world.options.enable_all_tricks or str(Tricks.GROTTOS_WITHOUT_AGONY) in world.options.tricks_in_logic:
        items_to_create[Items.STONE_OF_AGONY] -= create_special_progression_item(
            world, Items.STONE_OF_AGONY, ItemClassification.filler)

    # Ice Arrows set to filler if not useful (blue fire arrows enabled)
    if not world.options.blue_fire_arrows:
        items_to_create[Items.ICE_ARROW] -= create_special_progression_item(
            world, Items.ICE_ARROW, ItemClassification.filler)

    items: list[SohItem] = list()
    # Add regular item pool
    for item, quantity in items_to_create.items():
        items.extend([world.create_item(item) for _ in range(quantity)])

    filler_bottle_amount: int = 2
    if world.options.zoras_fountain == "open":
        filler_bottle_amount += 1
    if world.options.big_poe_target_count == 0:
        filler_bottle_amount += 1

    # Add random filler bottles
    items.extend([world.create_item(get_filler_bottle(world)) for _ in range(filler_bottle_amount)])

    world.add_items_to_item_pool_list(items)


def create_special_progression_item(world: "SohWorld", item: Items, classification: ItemClassification, amount: int = 1) -> int:
    if amount < 1:
        return 0

    items = [world.create_item(item, classification=classification)
             for _ in range(amount)]

    world.add_items_to_item_pool_list(items)

    return amount


def create_triforce_pieces(world: "SohWorld") -> None:
    total_triforce_pieces: int = min(
        get_open_location_count(world), world.options.triforce_hunt_pieces_total.value)

    triforce_pieces_to_win: int = max(1, round(
        total_triforce_pieces * (world.options.triforce_hunt_pieces_required_percentage.value * .01)))

    triforce_pieces_made = [world.create_item(Items.TRIFORCE_PIECE) 
                            for _ in range(triforce_pieces_to_win)]
    triforce_pieces_made += [world.create_item(Items.TRIFORCE_PIECE, classification=ItemClassification.useful | ItemClassification.skip_balancing) 
                             for _ in range(total_triforce_pieces - triforce_pieces_to_win)]

    world.add_items_to_item_pool_list(triforce_pieces_made)

    world.options.triforce_hunt_pieces_total.value = total_triforce_pieces
    world.triforce_pieces_required = triforce_pieces_to_win

    if world.using_ut:
        world.triforce_pieces_required = world.passthrough["triforce_hunt_pieces_required"]


def create_filler_item_pool(world: "SohWorld") -> None:
    filler_item_count = get_open_location_count(world)

    # Ice Trap Count
    ice_trap_count = min(filler_item_count, world.options.ice_trap_count.value)
    world.multiworld.itempool += [world.create_item(
        Items.ICE_TRAP) for _ in range(ice_trap_count)]

    filler_item_count -= ice_trap_count

    # Ice Trap Filler Replacement
    ice_traps_to_place: int = int(
        filler_item_count * (world.options.ice_trap_filler_replacement.value * .01))
    world.multiworld.itempool += [world.create_item(
        Items.ICE_TRAP) for _ in range(ice_traps_to_place)]

    filler_item_count -= ice_traps_to_place

    # Add junk items to fill remaining locations
    world.multiworld.itempool += [world.create_item(
        get_filler_item(world)) for _ in range(filler_item_count)]


def get_open_location_count(world: "SohWorld") -> int:
    open_location_count = len(world.multiworld.get_unfilled_locations(
        world.player)) - len(world.item_pool) - len(world.pre_fill_pool) + len(get_vanilla_shop_pool(world))

    return open_location_count


def get_filler_item(world: "SohWorld") -> str:
    return world.random.choice(filler_items)


def get_filler_bottle(world: "SohWorld") -> str:
    return world.random.choice(no_rules_bottles)


def give_starting_items(world: "SohWorld") -> None:
    if world.options.start_with_kokiri_sword:
        world.push_precollected(world.create_item(Items.KOKIRI_SWORD, True))

    if world.options.start_with_master_sword and world.options.shuffle_master_sword:
        world.push_precollected(world.create_item(Items.MASTER_SWORD, True))

    # doesn't actually do anything logically since deku shields can be lost
    if world.options.start_with_deku_shield:
        world.push_precollected(world.create_item(Items.DEKU_SHIELD, True))

    if world.options.start_with_ocarina == "fairy_ocarina":
        world.push_precollected(world.create_item(Items.PROGRESSIVE_OCARINA, True))

    if world.options.start_with_ocarina == "ocarina_of_time":
        world.push_precollected(world.create_item(Items.PROGRESSIVE_OCARINA, True))
        world.push_precollected(world.create_item(Items.PROGRESSIVE_OCARINA, True))
    
    if world.options.start_with_magic_beans:
        world.push_precollected(world.create_item(Items.MAGIC_BEAN_PACK, True))
    
        # Songs
    # Iterate over the ordered mapping (not the set) so precollected order is
    # deterministic; set iteration order of item-name strings varies with
    # PYTHONHASHSEED and breaks generation determinism / UT.
    shuffled_songs = get_shuffled_songs(world)
    for song in song_vanilla_locations.values():
        if song not in shuffled_songs:
            world.push_precollected(world.create_item(song, True))

    if world.options.small_key_shuffle == "start_with":
        for key_ring in key_to_ring.values():
            world.push_precollected(world.create_item(key_ring, True))
        
    if world.options.boss_key_shuffle == "start_with":
        for boss_key in dungeon_boss_key_vanilla_mapping.values():
            world.push_precollected(world.create_item(boss_key, True))
