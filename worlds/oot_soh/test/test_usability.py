from .bases import SohTestBase
from ..Enums import Items, Locations, Regions, Events
from .. import LogicHelpers
from .. Items import SohItem
from BaseClasses import ItemClassification as IC
from .. import Options
import itertools
import pytest

class HelperBase(SohTestBase):
    def get_bundle(self) -> tuple:
        return self.multiworld.state, Regions.ROOT, self.world
    
    def create_item(self, item) -> SohItem:
        return SohItem(item, IC.progression, None, self.world.player)
    
    def sweep(self) -> None:
        self.multiworld.state.sweep_for_advancements()

class TestCanUseItems(HelperBase):
    options = {"starting_age": "child", 
                "closed_forest": "on", 
                "shuffle_kokiri_sword": "on",
                "shuffle_childs_wallet": "on",
                "shuffle_deku_stick_bag": "true", 
                "shuffle_deku_nut_bag": "true",
                "bombchu_bag": "single_bag",
                "skip_scarecrows_song": "true",
                "shuffle_songs": "anywhere",
                "links_pocket": "nothing",
                "shuffle_fishing_pole": "false",
                "skip_epona_race": "true"}
    
    def require_all(self, check: Items, items: list[Items | Events]) -> None:
        # ideally we run these as subtests, but those are currently broken 
        # and report as Success if any subtest succeeds
        # (https://github.com/microsoft/vscode-python/issues/25824)
        self.sweep()
        self.assertFalse(LogicHelpers.can_use(check, self.get_bundle()))
        required_items = list(map(lambda i: self.create_item(i), items))
        for size in range(1, len(required_items)):
            for invalid_combo in itertools.combinations(required_items, size):
                self.collect(invalid_combo)
                self.assertFalse(LogicHelpers.can_use(check, self.get_bundle()), f"{str(check)} should not be usable with only {invalid_combo}")
                self.remove(invalid_combo)
        self.collect(required_items)
        self.assertTrue(LogicHelpers.can_use(check, self.get_bundle()))
        
        

    def require_any(self, check, items) -> None:
        # ideally we run these as subtests, but those are currently broken 
        # and report as Success if any subtest succeeds
        # (https://github.com/microsoft/vscode-python/issues/25824)
        self.sweep()
        self.assertFalse(LogicHelpers.can_use(check, self.get_bundle()))
        required_items = list(map(lambda i: self.create_item(i), items))
        for size in range(1, len(required_items)):
            for invalid_combo in itertools.combinations(required_items, size):
                self.collect(invalid_combo)
                self.assertTrue(LogicHelpers.can_use(check, self.get_bundle()), f"{str(check)} should be usable with {invalid_combo}")
                self.remove(invalid_combo)
        self.collect(required_items)
        self.assertTrue(LogicHelpers.can_use(check, self.get_bundle()))

    def test_sticks(self):
        self.require_all(Items.STICKS, [Items.DEKU_STICK_BAG, Events.CAN_FARM_STICKS])

    def test_explosives(self):
        self.sweep()
        bombchu_items = (Items.BOMBCHU_BAG, Items.BOMB_BAG)
        for item in bombchu_items:
            with self.subTest(item=item):
                self.assertFalse(LogicHelpers.can_use(item, self.get_bundle()), "You need to get Bags first before you can use them")

        self.collect(self.create_item(Items.BOMB_BAG))
        self.assertTrue(LogicHelpers.can_use(Items.BOMB_BAG, self.get_bundle()), "With the bomb bag unlocked you should be able to use bombs")
        self.assertFalse(LogicHelpers.can_use(Items.BOMBCHU_BAG, self.get_bundle()), "With bombchu bags shuffled you explicitly need the bombchu bag to them")

        self.collect(self.create_item(Items.BOMBCHU_BAG))
        self.remove_by_name(Items.BOMB_BAG)
        self.assertTrue(LogicHelpers.can_use(Items.BOMBCHU_BAG, self.get_bundle()), "With bombchu bag shuffled and found you should be able to use it")
        self.assertFalse(LogicHelpers.can_use(Items.BOMB_BAG, self.get_bundle()), "The bombchu bag alone doesn't grant access to bombs")

    def test_nuts(self):
        self.require_all(Items.NUTS, [Items.DEKU_NUT_BAG, Events.CAN_FARM_NUTS])

    def test_beans(self):
        self.require_any(Items.MAGIC_BEAN, [Items.MAGIC_BEAN_PACK, Events.CAN_BUY_BEANS])
    
    def shield(self, shield: Items, buy: Items):
        self.sweep()
        self.assertFalse(LogicHelpers.can_use(shield, self.get_bundle()), "You need to get the shield before you can use it")
        self.collect(self.create_item(shield))
        self.assertFalse(LogicHelpers.can_use(shield, self.get_bundle()), "shields can be lost to fire or like-likes, thus found shields shouldn't be considered in logic")
        
        self.collect(self.create_item(buy))
        self.assertTrue(LogicHelpers.can_use(shield, self.get_bundle()), "Deku shields are only considered in logic if you can buy them")

    def test_deku_shield(self):
        self.sweep()
        self.assertFalse(LogicHelpers.can_use(Items.DEKU_SHIELD, self.get_bundle()), "You need to get the shield before you can use it")
        self.collect(self.create_item(Items.DEKU_SHIELD))
        self.assertFalse(LogicHelpers.can_use(Items.DEKU_SHIELD, self.get_bundle()), "shields can be lost to fire or like-likes, thus found shields shouldn't be considered in logic")
        
        self.collect(self.create_item(Items.BUY_DEKU_SHIELD))
        self.assertTrue(LogicHelpers.can_use(Items.DEKU_SHIELD, self.get_bundle()), "Deku shields are only considered in logic if you can buy them")


    def test_hylian_shield(self):
        self.sweep()
        self.assertFalse(LogicHelpers.can_use(Items.HYLIAN_SHIELD, self.get_bundle()), "You need to get the shield before you can use it")
        self.collect(self.create_item(Items.HYLIAN_SHIELD))
        self.assertFalse(LogicHelpers.can_use(Items.HYLIAN_SHIELD, self.get_bundle()), "shields can be lost to fire or like-likes, thus found shields shouldn't be considered in logic")
        
        self.collect(self.create_item(Items.BUY_HYLIAN_SHIELD))
        self.assertTrue(LogicHelpers.can_use(Items.HYLIAN_SHIELD, self.get_bundle()), "Hylian shields are only considered in logic if you can buy them")


    def test_goron_tunic(self):
        self.require_any(Items.GORON_TUNIC, [Items.BUY_GORON_TUNIC, Items.GORON_TUNIC])

    def test_zora_tunic(self):
        self.require_any(Items.ZORA_TUNIC, [Items.BUY_ZORA_TUNIC, Items.ZORA_TUNIC])

    def test_scarecrow(self):
        self.require_all(Items.SCARECROW, [Items.PROGRESSIVE_OCARINA, Items.PROGRESSIVE_HOOKSHOT])
        
    def test_scarecrow_distant(self):
        self.require_all(Items.DISTANT_SCARECROW, [Items.PROGRESSIVE_OCARINA, Items.PROGRESSIVE_HOOKSHOT, Items.PROGRESSIVE_HOOKSHOT])

    def test_fishing_pole(self):
        self.sweep()
        self.assertFalse(LogicHelpers.can_use(Items.FISHING_POLE, self.get_bundle()), "when pole isn't shuffled, you require only the child wallet")
        self.collect(self.create_item(Items.CHILD_WALLET))
        self.assertTrue(LogicHelpers.can_use(Items.FISHING_POLE, self.get_bundle()), "when pole isn't shuffled it should be usable with only the wallet")
        
    def test_fishing_pole_shuffled(self):
        self.world.options.shuffle_fishing_pole.value = Options.ShuffleFishingPole.option_true
        self.require_all(Items.FISHING_POLE, [Items.FISHING_POLE, Items.CHILD_WALLET])

    def test_epona(self):
        self.require_all(Items.EPONA, [Items.PROGRESSIVE_OCARINA, Items.EPONAS_SONG, Events.FREED_EPONA])
    
    # Skipping has_item for adult trade items s

    def bottles(self, bottle: Items, event: list[Items | Events]):
        self.sweep()
        self.assertFalse(LogicHelpers.can_use(bottle, self.get_bundle()), "Bottles can't be used of you don't have any bottles")
        self.collect(self.create_item(Items.EMPTY_BOTTLE))
        self.assertFalse(LogicHelpers.can_use(bottle, self.get_bundle()), f"{bottle} can't be used of you don't have access to {event} as well")        
        self.require_any(bottle, event)

    def no_requirement_bottle(self, bottle: Items):
        self.sweep()
        self.assertFalse(LogicHelpers.can_use(bottle, self.get_bundle()), "Bottles can't be used of you don't have any bottles")
        self.collect(self.create_item(Items.EMPTY_BOTTLE))
        self.assertTrue(LogicHelpers.can_use(bottle, self.get_bundle()), f"current rules dictate you can use {bottle} if you just have an empty bottle")

    def test_bottle_blue_fire(self):
        self.bottles(Items.BOTTLE_WITH_BLUE_FIRE, [Events.CAN_ACCESS_BLUE_FIRE, Items.BUY_BLUE_FIRE])

    def test_bottle_blue_potion(self):
        self.bottles(Items.BOTTLE_WITH_BLUE_POTION, [Items.BUY_BLUE_POTION])

    def test_bottle_bugs(self):
        self.bottles(Items.BOTTLE_WITH_BUGS, [Items.BUY_BOTTLE_BUG, Events.CAN_ACCESS_BUGS])
    
    def test_bottle_fairy(self):
        self.bottles(Items.BOTTLE_WITH_FAIRY, [Items.BUY_FAIRYS_SPIRIT, Events.CAN_ACCESS_FAIRIES])
    
    def test_bottle_fish(self):
        self.bottles(Items.BOTTLE_WITH_FISH, [Items.BUY_FISH, Events.CAN_ACCESS_FISH])

    def test_bottle_green_potion(self):
        self.bottles(Items.BOTTLE_WITH_GREEN_POTION, [Items.BUY_GREEN_POTION])

    # these bottles might want some extra checks added to them if they ever start getting used in logic
    def test_bottle_milk(self):
        self.no_requirement_bottle(Items.BOTTLE_WITH_MILK)

    def test_bottle_poe(self):
        self.no_requirement_bottle(Items.BOTTLE_WITH_POE)

    def test_bottle_red_potion(self):
        self.no_requirement_bottle(Items.BOTTLE_WITH_RED_POTION)

    def test_bottle_empty(self):
        self.no_requirement_bottle(Items.EMPTY_BOTTLE)