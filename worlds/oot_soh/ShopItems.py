from typing import TYPE_CHECKING
from worlds.generic.Rules import add_rule
from worlds.AutoWorld import LogicMixin
from BaseClasses import CollectionState, MultiWorld

from .Locations import scrubs_location_table, merchants_items_location_table, scrubs_one_time_only
from .Enums import *
from . import SohItem

if TYPE_CHECKING:
    from . import SohWorld


vanilla_shop_prices: dict[Items, int] = {
    Items.BUY_ARROWS10: 20,
    Items.BUY_DEKU_NUTS5: 15,
    Items.BUY_ARROWS30: 60,
    Items.BUY_ARROWS50: 90,
    Items.BUY_BOMBS525: 25,
    Items.BUY_DEKU_NUTS10: 30,
    Items.BUY_DEKU_STICK1: 10,
    Items.BUY_BOMBS10: 50,
    Items.BUY_FISH: 200,
    Items.BUY_RED_POTION30: 30,
    Items.BUY_GREEN_POTION: 30,
    Items.BUY_BLUE_POTION: 100,
    Items.BUY_HYLIAN_SHIELD: 80,
    Items.BUY_DEKU_SHIELD: 40,
    Items.BUY_GORON_TUNIC: 200,
    Items.BUY_ZORA_TUNIC: 300,
    Items.BUY_HEART: 10,
    Items.BUY_BOMBCHUS10: 99,
    Items.BUY_BOMBCHUS20: 180,
    Items.BUY_DEKU_SEEDS30: 30,
    Items.BUY_BLUE_FIRE: 300,
    Items.BUY_BOTTLE_BUG: 50,
    Items.BUY_POE: 30,
    Items.BUY_FAIRYS_SPIRIT: 50,
    Items.BUY_BOMBS20: 80,
    Items.BUY_BOMBS30: 120,
    Items.BUY_BOMBS535: 35,
    Items.BUY_RED_POTION40: 40,
    Items.BUY_RED_POTION50: 50,
}


shop_locations_kf_shop: dict[Locations, Items] = {
    Locations.KF_SHOP_ITEM1: Items.BUY_DEKU_SHIELD,
    Locations.KF_SHOP_ITEM2: Items.BUY_DEKU_NUTS5,
    Locations.KF_SHOP_ITEM3: Items.BUY_DEKU_NUTS10,
    Locations.KF_SHOP_ITEM4: Items.BUY_DEKU_STICK1,
    Locations.KF_SHOP_ITEM5: Items.BUY_DEKU_SEEDS30,
    Locations.KF_SHOP_ITEM6: Items.BUY_ARROWS10,
    Locations.KF_SHOP_ITEM7: Items.BUY_ARROWS30,
    Locations.KF_SHOP_ITEM8: Items.BUY_HEART,
}

shop_locations_market_bazaar: dict[Locations, Items] = {
    Locations.MARKET_BAZAAR_ITEM1: Items.BUY_HYLIAN_SHIELD,
    Locations.MARKET_BAZAAR_ITEM2: Items.BUY_BOMBS535,
    Locations.MARKET_BAZAAR_ITEM3: Items.BUY_DEKU_NUTS5,
    Locations.MARKET_BAZAAR_ITEM4: Items.BUY_HEART,
    Locations.MARKET_BAZAAR_ITEM5: Items.BUY_ARROWS10,
    Locations.MARKET_BAZAAR_ITEM6: Items.BUY_ARROWS50,
    Locations.MARKET_BAZAAR_ITEM7: Items.BUY_DEKU_STICK1,
    Locations.MARKET_BAZAAR_ITEM8: Items.BUY_ARROWS30,
}

shop_locations_market_potion_shop: dict[Locations, Items] = {
    Locations.MARKET_POTION_SHOP_ITEM1: Items.BUY_GREEN_POTION,
    Locations.MARKET_POTION_SHOP_ITEM2: Items.BUY_BLUE_FIRE,
    Locations.MARKET_POTION_SHOP_ITEM3: Items.BUY_RED_POTION30,
    Locations.MARKET_POTION_SHOP_ITEM4: Items.BUY_FAIRYS_SPIRIT,
    Locations.MARKET_POTION_SHOP_ITEM5: Items.BUY_DEKU_NUTS5,
    Locations.MARKET_POTION_SHOP_ITEM6: Items.BUY_BOTTLE_BUG,
    Locations.MARKET_POTION_SHOP_ITEM7: Items.BUY_POE,
    Locations.MARKET_POTION_SHOP_ITEM8: Items.BUY_FISH,
}

shop_locations_market_bombchu_shop: dict[Locations, Items] = {
    Locations.MARKET_BOMBCHU_SHOP_ITEM1: Items.BUY_BOMBCHUS10,
    Locations.MARKET_BOMBCHU_SHOP_ITEM2: Items.BUY_BOMBCHUS10,
    Locations.MARKET_BOMBCHU_SHOP_ITEM3: Items.BUY_BOMBCHUS10,
    Locations.MARKET_BOMBCHU_SHOP_ITEM4: Items.BUY_BOMBCHUS10,
    Locations.MARKET_BOMBCHU_SHOP_ITEM5: Items.BUY_BOMBCHUS20,
    Locations.MARKET_BOMBCHU_SHOP_ITEM6: Items.BUY_BOMBCHUS20,
    Locations.MARKET_BOMBCHU_SHOP_ITEM7: Items.BUY_BOMBCHUS20,
    Locations.MARKET_BOMBCHU_SHOP_ITEM8: Items.BUY_BOMBCHUS20,
}

shop_locations_kak_bazaar: dict[Locations, Items] = {
    Locations.KAK_BAZAAR_ITEM1: Items.BUY_HYLIAN_SHIELD,
    Locations.KAK_BAZAAR_ITEM2: Items.BUY_BOMBS535,
    Locations.KAK_BAZAAR_ITEM3: Items.BUY_DEKU_NUTS5,
    Locations.KAK_BAZAAR_ITEM4: Items.BUY_HEART,
    Locations.KAK_BAZAAR_ITEM5: Items.BUY_ARROWS10,
    Locations.KAK_BAZAAR_ITEM6: Items.BUY_ARROWS50,
    Locations.KAK_BAZAAR_ITEM7: Items.BUY_DEKU_STICK1,
    Locations.KAK_BAZAAR_ITEM8: Items.BUY_ARROWS30,
}

shop_locations_kak_potion_shop: dict[Locations, Items] = {
    Locations.KAK_POTION_SHOP_ITEM1: Items.BUY_GREEN_POTION,
    Locations.KAK_POTION_SHOP_ITEM2: Items.BUY_BLUE_FIRE,
    Locations.KAK_POTION_SHOP_ITEM3: Items.BUY_RED_POTION30,
    Locations.KAK_POTION_SHOP_ITEM4: Items.BUY_FAIRYS_SPIRIT,
    Locations.KAK_POTION_SHOP_ITEM5: Items.BUY_DEKU_NUTS5,
    Locations.KAK_POTION_SHOP_ITEM6: Items.BUY_BOTTLE_BUG,
    Locations.KAK_POTION_SHOP_ITEM7: Items.BUY_POE,
    Locations.KAK_POTION_SHOP_ITEM8: Items.BUY_FISH,
}

shop_locations_gc_shop: dict[Locations, Items] = {
    Locations.GC_SHOP_ITEM1: Items.BUY_BOMBS525,
    Locations.GC_SHOP_ITEM2: Items.BUY_BOMBS10,
    Locations.GC_SHOP_ITEM3: Items.BUY_BOMBS20,
    Locations.GC_SHOP_ITEM4: Items.BUY_BOMBS30,
    Locations.GC_SHOP_ITEM5: Items.BUY_GORON_TUNIC,
    Locations.GC_SHOP_ITEM6: Items.BUY_HEART,
    Locations.GC_SHOP_ITEM7: Items.BUY_RED_POTION40,
    Locations.GC_SHOP_ITEM8: Items.BUY_HEART,
}

shop_locations_zd_shop: dict[Locations, Items] = {
    Locations.ZD_SHOP_ITEM1: Items.BUY_ZORA_TUNIC,
    Locations.ZD_SHOP_ITEM2: Items.BUY_ARROWS10,
    Locations.ZD_SHOP_ITEM3: Items.BUY_HEART,
    Locations.ZD_SHOP_ITEM4: Items.BUY_ARROWS30,
    Locations.ZD_SHOP_ITEM5: Items.BUY_DEKU_NUTS5,
    Locations.ZD_SHOP_ITEM6: Items.BUY_ARROWS50,
    Locations.ZD_SHOP_ITEM7: Items.BUY_FISH,
    Locations.ZD_SHOP_ITEM8: Items.BUY_RED_POTION30,
}

all_shop_locations: list[tuple[Regions, dict[Locations, Items]]] = [
    (Regions.KF_KOKIRI_SHOP, shop_locations_kf_shop),
    (Regions.MARKET_BAZAAR, shop_locations_market_bazaar),
    (Regions.MARKET_POTION_SHOP, shop_locations_market_potion_shop),
    (Regions.MARKET_BOMBCHU_SHOP, shop_locations_market_bombchu_shop),
    (Regions.KAK_BAZAAR, shop_locations_kak_bazaar),
    (Regions.KAK_POTION_SHOP_FRONT, shop_locations_kak_potion_shop),
    (Regions.GC_SHOP, shop_locations_gc_shop),
    (Regions.ZD_SHOP, shop_locations_zd_shop)
]

vanilla_items_to_add: list[list[Items]] = [
    [Items.BUY_DEKU_SHIELD, Items.BUY_HYLIAN_SHIELD, Items.BUY_GORON_TUNIC, Items.BUY_ZORA_TUNIC,
        Items.BUY_DEKU_NUTS5, Items.BUY_BOMBS20, Items.BUY_BOMBCHUS10, Items.BUY_DEKU_STICK1],
    [Items.BUY_FAIRYS_SPIRIT, Items.BUY_DEKU_SEEDS30, Items.BUY_ARROWS10, Items.BUY_BLUE_FIRE,
        Items.BUY_RED_POTION30, Items.BUY_GREEN_POTION, Items.BUY_DEKU_NUTS10, Items.BUY_BOMBCHUS10],
    [Items.BUY_BOMBCHUS10, Items.BUY_BOMBCHUS20, Items.BUY_BOMBS525, Items.BUY_BOMBS535,
        Items.BUY_BOMBS10, Items.BUY_DEKU_NUTS5, Items.BUY_ARROWS30, Items.BUY_ARROWS50],
    [Items.BUY_ARROWS10, Items.BUY_FAIRYS_SPIRIT, Items.BUY_BOTTLE_BUG, Items.BUY_FISH,
        Items.BUY_HYLIAN_SHIELD, Items.BUY_BOTTLE_BUG, Items.BUY_DEKU_STICK1, Items.BUY_DEKU_STICK1],
    [Items.BUY_BLUE_FIRE, Items.BUY_FISH, Items.BUY_BOMBCHUS10, Items.BUY_DEKU_NUTS5,
        Items.BUY_ARROWS10, Items.BUY_BOMBCHUS20, Items.BUY_BOMBS535, Items.BUY_RED_POTION30],
    [Items.BUY_BOMBS30, Items.BUY_BOMBCHUS20, Items.BUY_DEKU_NUTS5, Items.BUY_ARROWS10,
        Items.BUY_DEKU_NUTS5, Items.BUY_ARROWS30, Items.BUY_RED_POTION40, Items.BUY_FISH],
    [Items.BUY_BOMBCHUS20, Items.BUY_ARROWS30, Items.BUY_RED_POTION50, Items.BUY_ARROWS30,
        Items.BUY_DEKU_NUTS5, Items.BUY_ARROWS50, Items.BUY_ARROWS50, Items.BUY_GREEN_POTION],
    [Items.BUY_POE, Items.BUY_POE, Items.BUY_HEART, Items.BUY_HEART,
        Items.BUY_HEART, Items.BUY_HEART, Items.BUY_HEART, Items.BUY_HEART],
]

vanilla_merchant_prices: dict[Locations, int] = {
    Locations.KAK_GRANNYS_SHOP: 100,
    Locations.GC_MEDIGORON: 200,
    Locations.ZR_MAGIC_BEAN_SALESMAN: 60,
    Locations.WASTELAND_CARPET_SALESMAN: 200
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
        location.place_locked_item(world.create_item(Items.RESERVATION))

def remove_vanilla_shop_reservations(world: "SohWorld") -> None:
    vanilla_shop_slots = get_vanilla_shop_locations(world)
    for slot in vanilla_shop_slots:
        location = world.get_location(slot)
        if location.item == world.create_item(Items.RESERVATION):
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
            world.get_location(slot).place_locked_item(world.create_item(item))
            world.get_location(slot).address = None
            world.shop_vanilla_items[slot] = item.value
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
            prices[slot] = create_random_price(min_shop_price, max_shop_price, world)
    return prices


def generate_scrub_prices(world: "SohWorld") -> dict[Locations, int]:
    prices = dict[Locations, int]()
    if not world.options.shuffle_scrubs:
        return prices
    
    min_scrub_price = world.options.shuffle_scrubs_minimum_price.value
    max_scrub_price = world.options.shuffle_scrubs_maximum_price.value
    
    if world.options.shuffle_scrubs == "all":
        for slot in scrubs_location_table.keys():
            prices[slot] = create_random_price(
                min_scrub_price, max_scrub_price, world)
    else:
        for slot in scrubs_one_time_only:
            prices[slot] = create_random_price(
                min_scrub_price, max_scrub_price, world)

    return prices

def generate_merchant_prices(world: "SohWorld") -> dict[Locations, int]:
    prices = vanilla_merchant_prices.copy()

    if not world.options.shuffle_merchants:
        return prices
    
    min_merchant_price = world.options.shuffle_merchants_minimum_price.value
    max_merchant_price = world.options.shuffle_merchants_maximum_price.value

    for slot in merchants_items_location_table.keys():
        if world.options.shuffle_merchants == "bean_merchant_only" and slot != Locations.ZR_MAGIC_BEAN_SALESMAN:
            continue
        if world.options.shuffle_merchants == "all_but_beans" and slot == Locations.ZR_MAGIC_BEAN_SALESMAN:
            continue

        prices[slot] = create_random_price(min_merchant_price, max_merchant_price, world)

    return prices


def create_random_price(min_price: int, max_price: int, world: "SohWorld") -> int:
    # randrange needs an actual range to work, so just pick the price directly if min/max are the same.
    if min_price == max_price:
        price = min_price
    else:
        price = world.random.randrange(min_price, max_price)

    price = price - (price % 5)
    return price
