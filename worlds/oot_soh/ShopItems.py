from typing import TYPE_CHECKING
from worlds.generic.Rules import add_rule
from worlds.AutoWorld import LogicMixin
from BaseClasses import CollectionState, MultiWorld

from .Locations import scrubs_location_table, merchants_items_location_table, scrubs_one_time_only
from .Enums import Items, Locations
from .enums_gen import Regions
from . import SohItem

if TYPE_CHECKING:
    from . import SohWorld


vanilla_shop_prices: dict[Items, int] = {
    Items.RG_BUY_ARROWS_10: 20,
    Items.RG_BUY_DEKU_NUTS_5: 15,
    Items.RG_BUY_ARROWS_30: 60,
    Items.RG_BUY_ARROWS_50: 90,
    Items.RG_BUY_BOMBS_525: 25,
    Items.RG_BUY_DEKU_NUTS_10: 30,
    Items.RG_BUY_DEKU_STICK_1: 10,
    Items.RG_BUY_BOMBS_10: 50,
    Items.RG_BUY_FISH: 200,
    Items.RG_BUY_RED_POTION_30: 30,
    Items.RG_BUY_GREEN_POTION: 30,
    Items.RG_BUY_BLUE_POTION: 100,
    Items.RG_BUY_HYLIAN_SHIELD: 80,
    Items.RG_BUY_DEKU_SHIELD: 40,
    Items.RG_BUY_GORON_TUNIC: 200,
    Items.RG_BUY_ZORA_TUNIC: 300,
    Items.RG_BUY_HEART: 10,
    Items.RG_BUY_BOMBCHUS_10: 99,
    Items.RG_BUY_BOMBCHUS_20: 180,
    Items.RG_BUY_DEKU_SEEDS_30: 30,
    Items.RG_BUY_BLUE_FIRE: 300,
    Items.RG_BUY_BOTTLE_BUG: 50,
    Items.RG_BUY_POE: 30,
    Items.RG_BUY_FAIRYS_SPIRIT: 50,
    Items.RG_BUY_BOMBS_20: 80,
    Items.RG_BUY_BOMBS_30: 120,
    Items.RG_BUY_BOMBS_535: 35,
    Items.RG_BUY_RED_POTION_40: 40,
    Items.RG_BUY_RED_POTION_50: 50,
}


shop_locations_kf_shop: dict[Locations, Items] = {
    Locations.RC_KF_SHOP_ITEM_1: Items.RG_BUY_DEKU_SHIELD,
    Locations.RC_KF_SHOP_ITEM_2: Items.RG_BUY_DEKU_NUTS_5,
    Locations.RC_KF_SHOP_ITEM_3: Items.RG_BUY_DEKU_NUTS_10,
    Locations.RC_KF_SHOP_ITEM_4: Items.RG_BUY_DEKU_STICK_1,
    Locations.RC_KF_SHOP_ITEM_5: Items.RG_BUY_DEKU_SEEDS_30,
    Locations.RC_KF_SHOP_ITEM_6: Items.RG_BUY_ARROWS_10,
    Locations.RC_KF_SHOP_ITEM_7: Items.RG_BUY_ARROWS_30,
    Locations.RC_KF_SHOP_ITEM_8: Items.RG_BUY_HEART,
}

shop_locations_market_bazaar: dict[Locations, Items] = {
    Locations.RC_MARKET_BAZAAR_ITEM_1: Items.RG_BUY_HYLIAN_SHIELD,
    Locations.RC_MARKET_BAZAAR_ITEM_2: Items.RG_BUY_BOMBS_535,
    Locations.RC_MARKET_BAZAAR_ITEM_3: Items.RG_BUY_DEKU_NUTS_5,
    Locations.RC_MARKET_BAZAAR_ITEM_4: Items.RG_BUY_HEART,
    Locations.RC_MARKET_BAZAAR_ITEM_5: Items.RG_BUY_ARROWS_10,
    Locations.RC_MARKET_BAZAAR_ITEM_6: Items.RG_BUY_ARROWS_50,
    Locations.RC_MARKET_BAZAAR_ITEM_7: Items.RG_BUY_DEKU_STICK_1,
    Locations.RC_MARKET_BAZAAR_ITEM_8: Items.RG_BUY_ARROWS_30,
}

shop_locations_market_potion_shop: dict[Locations, Items] = {
    Locations.RC_MARKET_POTION_SHOP_ITEM_1: Items.RG_BUY_GREEN_POTION,
    Locations.RC_MARKET_POTION_SHOP_ITEM_2: Items.RG_BUY_BLUE_FIRE,
    Locations.RC_MARKET_POTION_SHOP_ITEM_3: Items.RG_BUY_RED_POTION_30,
    Locations.RC_MARKET_POTION_SHOP_ITEM_4: Items.RG_BUY_FAIRYS_SPIRIT,
    Locations.RC_MARKET_POTION_SHOP_ITEM_5: Items.RG_BUY_DEKU_NUTS_5,
    Locations.RC_MARKET_POTION_SHOP_ITEM_6: Items.RG_BUY_BOTTLE_BUG,
    Locations.RC_MARKET_POTION_SHOP_ITEM_7: Items.RG_BUY_POE,
    Locations.RC_MARKET_POTION_SHOP_ITEM_8: Items.RG_BUY_FISH,
}

shop_locations_market_bombchu_shop: dict[Locations, Items] = {
    Locations.RC_MARKET_BOMBCHU_SHOP_ITEM_1: Items.RG_BUY_BOMBCHUS_10,
    Locations.RC_MARKET_BOMBCHU_SHOP_ITEM_2: Items.RG_BUY_BOMBCHUS_10,
    Locations.RC_MARKET_BOMBCHU_SHOP_ITEM_3: Items.RG_BUY_BOMBCHUS_10,
    Locations.RC_MARKET_BOMBCHU_SHOP_ITEM_4: Items.RG_BUY_BOMBCHUS_10,
    Locations.RC_MARKET_BOMBCHU_SHOP_ITEM_5: Items.RG_BUY_BOMBCHUS_20,
    Locations.RC_MARKET_BOMBCHU_SHOP_ITEM_6: Items.RG_BUY_BOMBCHUS_20,
    Locations.RC_MARKET_BOMBCHU_SHOP_ITEM_7: Items.RG_BUY_BOMBCHUS_20,
    Locations.RC_MARKET_BOMBCHU_SHOP_ITEM_8: Items.RG_BUY_BOMBCHUS_20,
}

shop_locations_kak_bazaar: dict[Locations, Items] = {
    Locations.RC_KAK_BAZAAR_ITEM_1: Items.RG_BUY_HYLIAN_SHIELD,
    Locations.RC_KAK_BAZAAR_ITEM_2: Items.RG_BUY_BOMBS_535,
    Locations.RC_KAK_BAZAAR_ITEM_3: Items.RG_BUY_DEKU_NUTS_5,
    Locations.RC_KAK_BAZAAR_ITEM_4: Items.RG_BUY_HEART,
    Locations.RC_KAK_BAZAAR_ITEM_5: Items.RG_BUY_ARROWS_10,
    Locations.RC_KAK_BAZAAR_ITEM_6: Items.RG_BUY_ARROWS_50,
    Locations.RC_KAK_BAZAAR_ITEM_7: Items.RG_BUY_DEKU_STICK_1,
    Locations.RC_KAK_BAZAAR_ITEM_8: Items.RG_BUY_ARROWS_30,
}

shop_locations_kak_potion_shop: dict[Locations, Items] = {
    Locations.RC_KAK_POTION_SHOP_ITEM_1: Items.RG_BUY_GREEN_POTION,
    Locations.RC_KAK_POTION_SHOP_ITEM_2: Items.RG_BUY_BLUE_FIRE,
    Locations.RC_KAK_POTION_SHOP_ITEM_3: Items.RG_BUY_RED_POTION_30,
    Locations.RC_KAK_POTION_SHOP_ITEM_4: Items.RG_BUY_FAIRYS_SPIRIT,
    Locations.RC_KAK_POTION_SHOP_ITEM_5: Items.RG_BUY_DEKU_NUTS_5,
    Locations.RC_KAK_POTION_SHOP_ITEM_6: Items.RG_BUY_BOTTLE_BUG,
    Locations.RC_KAK_POTION_SHOP_ITEM_7: Items.RG_BUY_POE,
    Locations.RC_KAK_POTION_SHOP_ITEM_8: Items.RG_BUY_FISH,
}

shop_locations_gc_shop: dict[Locations, Items] = {
    Locations.RC_GC_SHOP_ITEM_1: Items.RG_BUY_BOMBS_525,
    Locations.RC_GC_SHOP_ITEM_2: Items.RG_BUY_BOMBS_10,
    Locations.RC_GC_SHOP_ITEM_3: Items.RG_BUY_BOMBS_20,
    Locations.RC_GC_SHOP_ITEM_4: Items.RG_BUY_BOMBS_30,
    Locations.RC_GC_SHOP_ITEM_5: Items.RG_BUY_GORON_TUNIC,
    Locations.RC_GC_SHOP_ITEM_6: Items.RG_BUY_HEART,
    Locations.RC_GC_SHOP_ITEM_7: Items.RG_BUY_RED_POTION_40,
    Locations.RC_GC_SHOP_ITEM_8: Items.RG_BUY_HEART,
}

shop_locations_zd_shop: dict[Locations, Items] = {
    Locations.RC_ZD_SHOP_ITEM_1: Items.RG_BUY_ZORA_TUNIC,
    Locations.RC_ZD_SHOP_ITEM_2: Items.RG_BUY_ARROWS_10,
    Locations.RC_ZD_SHOP_ITEM_3: Items.RG_BUY_HEART,
    Locations.RC_ZD_SHOP_ITEM_4: Items.RG_BUY_ARROWS_30,
    Locations.RC_ZD_SHOP_ITEM_5: Items.RG_BUY_DEKU_NUTS_5,
    Locations.RC_ZD_SHOP_ITEM_6: Items.RG_BUY_ARROWS_50,
    Locations.RC_ZD_SHOP_ITEM_7: Items.RG_BUY_FISH,
    Locations.RC_ZD_SHOP_ITEM_8: Items.RG_BUY_RED_POTION_30,
}

all_shop_locations: list[tuple[Regions, dict[Locations, Items]]] = [
    (Regions.RR_KF_KOKIRI_SHOP, shop_locations_kf_shop),
    (Regions.RR_MARKET_BAZAAR, shop_locations_market_bazaar),
    (Regions.RR_MARKET_POTION_SHOP, shop_locations_market_potion_shop),
    (Regions.RR_MARKET_BOMBCHU_SHOP, shop_locations_market_bombchu_shop),
    (Regions.RR_KAK_BAZAAR, shop_locations_kak_bazaar),
    (Regions.RR_KAK_POTION_SHOP, shop_locations_kak_potion_shop),
    (Regions.RR_GC_SHOP, shop_locations_gc_shop),
    (Regions.RR_ZD_SHOP, shop_locations_zd_shop)
]

vanilla_items_to_add: list[list[Items]] = [
    [Items.RG_BUY_DEKU_SHIELD, Items.RG_BUY_HYLIAN_SHIELD, Items.RG_BUY_GORON_TUNIC, Items.RG_BUY_ZORA_TUNIC,
        Items.RG_BUY_DEKU_NUTS_5, Items.RG_BUY_BOMBS_20, Items.RG_BUY_BOMBCHUS_10, Items.RG_BUY_DEKU_STICK_1],
    [Items.RG_BUY_FAIRYS_SPIRIT, Items.RG_BUY_DEKU_SEEDS_30, Items.RG_BUY_ARROWS_10, Items.RG_BUY_BLUE_FIRE,
        Items.RG_BUY_RED_POTION_30, Items.RG_BUY_GREEN_POTION, Items.RG_BUY_DEKU_NUTS_10, Items.RG_BUY_BOMBCHUS_10],
    [Items.RG_BUY_BOMBCHUS_10, Items.RG_BUY_BOMBCHUS_20, Items.RG_BUY_BOMBS_525, Items.RG_BUY_BOMBS_535,
        Items.RG_BUY_BOMBS_10, Items.RG_BUY_DEKU_NUTS_5, Items.RG_BUY_ARROWS_30, Items.RG_BUY_ARROWS_50],
    [Items.RG_BUY_ARROWS_10, Items.RG_BUY_FAIRYS_SPIRIT, Items.RG_BUY_BOTTLE_BUG, Items.RG_BUY_FISH,
        Items.RG_BUY_HYLIAN_SHIELD, Items.RG_BUY_BOTTLE_BUG, Items.RG_BUY_DEKU_STICK_1, Items.RG_BUY_DEKU_STICK_1],
    [Items.RG_BUY_BLUE_FIRE, Items.RG_BUY_FISH, Items.RG_BUY_BOMBCHUS_10, Items.RG_BUY_DEKU_NUTS_5,
        Items.RG_BUY_ARROWS_10, Items.RG_BUY_BOMBCHUS_20, Items.RG_BUY_BOMBS_535, Items.RG_BUY_RED_POTION_30],
    [Items.RG_BUY_BOMBS_30, Items.RG_BUY_BOMBCHUS_20, Items.RG_BUY_DEKU_NUTS_5, Items.RG_BUY_ARROWS_10,
        Items.RG_BUY_DEKU_NUTS_5, Items.RG_BUY_ARROWS_30, Items.RG_BUY_RED_POTION_40, Items.RG_BUY_FISH],
    [Items.RG_BUY_BOMBCHUS_20, Items.RG_BUY_ARROWS_30, Items.RG_BUY_RED_POTION_50, Items.RG_BUY_ARROWS_30,
        Items.RG_BUY_DEKU_NUTS_5, Items.RG_BUY_ARROWS_50, Items.RG_BUY_ARROWS_50, Items.RG_BUY_GREEN_POTION],
    [Items.RG_BUY_POE, Items.RG_BUY_POE, Items.RG_BUY_HEART, Items.RG_BUY_HEART,
        Items.RG_BUY_HEART, Items.RG_BUY_HEART, Items.RG_BUY_HEART, Items.RG_BUY_HEART],
]

vanilla_merchant_prices: dict[Locations, int] = {
    Locations.RC_KAK_GRANNYS_SHOP: 100,
    Locations.RC_GC_MEDIGORON: 200,
    Locations.RC_ZR_MAGIC_BEAN_SALESMAN: 60,
    Locations.RC_WASTELAND_BOMBCHU_SALESMAN: 200
}

def get_vanilla_shop_pool(world: "SohWorld") -> list[Items]:
    vanilla_shop_pool = list[Items]()
    if not world.options.shuffle_shops:
        for region, shop in all_shop_locations:
            for item in shop.values():
                vanilla_shop_pool.append(item)
        return vanilla_shop_pool

    num_vanilla = 8 - world.options.shuffle_shops_item_amount
    for i in range(0, num_vanilla):
        vanilla_shop_pool += vanilla_items_to_add[i]
    return vanilla_shop_pool

def get_vanilla_shop_locations(world: "SohWorld") -> list[str]:
    vanilla_shop_slots = list[str]()
    if not world.options.shuffle_shops:
        for region, shop in all_shop_locations:
            for slot in shop.keys():
                vanilla_shop_slots.append(slot)
        return vanilla_shop_slots

    # select what shop slots to and vanilla items to shuffle
    num_vanilla = 8 - world.options.shuffle_shops_item_amount
    for region, shop in all_shop_locations:
        vanilla_shop_slots += list(shop.keys())[0: num_vanilla]
    return vanilla_shop_slots


def reserve_vanilla_shop_locations(world: "SohWorld") -> None:
    if not world.options.shuffle_shops:
        return
    vanilla_shop_slots = get_vanilla_shop_locations(world)
    for slot in vanilla_shop_slots:
        location = world.get_location(slot)
        location.place_locked_item(world.create_item(Items.RG_RESERVATION))

def remove_vanilla_shop_reservations(world: "SohWorld") -> None:
    vanilla_shop_slots = get_vanilla_shop_locations(world)
    for slot in vanilla_shop_slots:
        location = world.get_location(slot)
        if location.item == world.create_item(Items.RG_RESERVATION):
            location.item = None
            location.locked = False

def fill_shop_items(world: "SohWorld") -> None:
    if not world.options.shuffle_shops:
        return
    
    remove_vanilla_shop_reservations(world)
    
    # if we're using UT, we just want to place the event shop items in their proper spots
    if world.using_ut:
        world.shop_vanilla_items = world.passthrough["shop_vanilla_items"]
        for slot, item in world.shop_vanilla_items.items():
            location = world.get_location(slot)
            location.address = None
            location.place_locked_item(world.create_item(item, create_as_event=True))
        return
    
    # select what shop slots to and vanilla items to shuffle
    vanilla_pool = get_vanilla_shop_pool(world)
    vanilla_shop_slots = [Locations(slot) for slot in get_vanilla_shop_locations(world)]
    
    world.run_prefill(vanilla_pool, vanilla_shop_slots)
    
    # set the prices for our shuffled slots
    for slot in vanilla_shop_slots:
        location = world.get_location(slot)
        location.address = None
        world.shop_prices[slot] = vanilla_shop_prices[Items(location.item.name)]
        world.shop_vanilla_items[slot] = location.item.name


def no_shop_shuffle(world: "SohWorld") -> None:
    # put everything in its place as plain vanilla
    new_shop_prices = dict[Locations, int]()
    for region, shop in all_shop_locations:
        for slot, item in shop.items():
            new_shop_prices[slot] = vanilla_shop_prices[item]
            shop_item = world.create_item(item)
            world.get_location(slot).place_locked_item(shop_item)
            world.get_location(slot).address = None
            world.shop_vanilla_items[slot] = item.value
            world.preplaced_items.append(shop_item)
    update_shop_prices(world, new_shop_prices)

def update_shop_prices(world: "SohWorld", new_prices: dict[Locations, int]) -> None:
    world.shop_prices.update(new_prices)
    world.multiworld.state._soh_invalidate(world.player)

def generate_prices(world: "SohWorld") -> None:
    if world.using_ut:
        world.shop_prices = world.passthrough.get("shop_prices", dict())
        return

    all_prices = dict[Locations, int]()
    all_prices.update(generate_shop_prices(world))
    all_prices.update(generate_scrub_prices(world))
    all_prices.update(generate_merchant_prices(world))
    update_shop_prices(world, all_prices)

def generate_shop_prices(world: "SohWorld") -> dict[Locations, int]:
    prices = dict[Locations, int]()
    if not world.options.shuffle_shops:
        return prices

    min_shop_price = world.options.shuffle_shops_minimum_price.value
    max_shop_price = world.options.shuffle_shops_maximum_price.value

    for region, shop in all_shop_locations:
        for slot in shop.keys():
            prices[slot] = create_random_price(min_shop_price, max_shop_price, world.options.shop_affordable_prices, world)
    return prices


def generate_scrub_prices(world: "SohWorld") -> dict[Locations, int]:
    prices = dict[Locations, int]()
    if not world.options.shuffle_scrubs:
        return prices
    
    min_scrub_price = world.options.shuffle_scrubs_minimum_price.value
    max_scrub_price = world.options.shuffle_scrubs_maximum_price.value
    
    if world.options.shuffle_scrubs == "all":
        for slot in scrubs_location_table.keys():
            prices[slot] = create_random_price(min_scrub_price, max_scrub_price, world.options.scrub_affordable_prices, world)
    else:
        for slot in scrubs_one_time_only:
            prices[slot] = create_random_price(min_scrub_price, max_scrub_price, world.options.scrub_affordable_prices, world)

    return prices

def generate_merchant_prices(world: "SohWorld") -> dict[Locations, int]:
    prices = vanilla_merchant_prices.copy()

    if not world.options.shuffle_merchants:
        return prices
    
    min_merchant_price = world.options.shuffle_merchants_minimum_price.value
    max_merchant_price = world.options.shuffle_merchants_maximum_price.value

    for slot in merchants_items_location_table.keys():
        if world.options.shuffle_merchants == "bean_merchant_only" and slot != Locations.RC_ZR_MAGIC_BEAN_SALESMAN:
            continue
        if world.options.shuffle_merchants == "all_but_beans" and slot == Locations.RC_ZR_MAGIC_BEAN_SALESMAN:
            continue

        prices[slot] = create_random_price(min_merchant_price, max_merchant_price, world.options.merchant_affordable_prices, world)

    return prices


affordable_prices: list[int] = [0,1,100,201,501]

def create_random_price(min_price: int, max_price: int, affordable: bool, world: "SohWorld") -> int:
    if affordable:
        # Try to adhere to their min/max
        start: int = 0
        end: int = 0
        for index, value in enumerate(affordable_prices):
            if min_price >= value and min_price != 0:
                start = index
            if max_price >= value:
                if not world.options.shuffle_tycoon_wallet and index == len(affordable_prices):
                    end = 4
                    break
                # Need to add one because randrange stop in exclusive
                end = index + 1

        if start == end:
            price_tier = start
        else:
            price_tier = world.random.randrange(start, end)

        price = affordable_prices[price_tier]
    else:
        # randrange needs an actual range to work, so just pick the price directly if min/max are the same.
        if min_price == max_price:
            price = min_price
        else:
            price = world.random.randrange(min_price, max_price)

        # otherwise round down to the nearest multiple of 5
        price = price - (price % 5)

    return price
