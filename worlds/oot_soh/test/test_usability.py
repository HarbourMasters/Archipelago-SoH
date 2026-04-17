from .bases import SohTestBase
from ..Enums import Items, Regions, Events
from .. import LogicHelpers
from .. import Options
import itertools

class TestCanUseItems(SohTestBase):
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
                "shuffle_adult_trade_items": "true",
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


    def test_magic_item(self):
        self.require_all(Items.DINS_FIRE, [Items.DINS_FIRE, Items.PROGRESSIVE_MAGIC_METER])

    def test_sticks(self):
        self.require_all(Items.STICKS, [Items.DEKU_STICK_BAG, Events.CAN_FARM_STICKS])

    def test_explosives(self):
        self.sweep()
        bombchu_items = (Items.BOMBCHU_BAG, Items.BOMB_BAG)
        for item in bombchu_items:
            #with self.subTest(item=item):
            self.assertFalse(LogicHelpers.can_use(item, self.get_bundle()), "You need to get Bags first before you can use them")

        bomb_bag = self.create_item(Items.BOMB_BAG)
        self.collect(bomb_bag)
        self.assertTrue(LogicHelpers.can_use(Items.BOMB_BAG, self.get_bundle()), "With the bomb bag unlocked you should be able to use bombs")
        self.assertFalse(LogicHelpers.can_use(Items.BOMBCHU_BAG, self.get_bundle()), "With bombchu bags shuffled you explicitly need the bombchu bag to them")

        self.collect(self.create_item(Items.BOMBCHU_BAG))
        self.remove(bomb_bag)
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
    
    def test_trade_items(self):
        # when creating this test the shuffle_adult_trade_items option is turned on so trade items aren't pre-collected
        trade_items = [Items.POCKET_EGG, Items.COJIRO, Items.ODD_MUSHROOM, Items.ODD_POTION, Items.POACHERS_SAW,
                       Items.BROKEN_GORONS_SWORD, Items.PRESCRIPTION, Items.EYEBALL_FROG, Items.WORLDS_FINEST_EYEDROPS]
        
        self.sweep()
        self.world.options.shuffle_adult_trade_items.value = Options.ShuffleAdultTradeItems.option_false
        for item in trade_items:
            self.assertTrue(LogicHelpers.can_use(item, self.get_bundle()), f"Without trade items shuffled {item} should be seen as usable")

        self.world.options.shuffle_adult_trade_items.value = Options.ShuffleAdultTradeItems.option_true
        for item in trade_items:
            self.assertFalse(LogicHelpers.can_use(item, self.get_bundle()), f"With trade items shuffled you shouldn't be able to use {item} untill you get it")
        
        as_items = list(map(lambda i: self.create_item(i), trade_items))
        for item in as_items:
            item_set = set(as_items)
            item_set.remove(item)
            self.collect(item_set)
            self.assertFalse(LogicHelpers.can_use(Items(item.name), self.get_bundle()), f"the other trade items are not a substitute for {item.name}")
            self.remove(item_set)
            self.collect(item)
            self.assertTrue(LogicHelpers.can_use(Items(item.name), self.get_bundle()), f"you need the trade item in order to use it")
            self.remove(item)

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

    def test_fire_arrow(self):
        self.require_all(Items.FIRE_ARROW, [Items.FIRE_ARROW, Items.FAIRY_BOW, Items.PROGRESSIVE_MAGIC_METER])

    def test_ice_arrow(self):
        self.require_all(Items.ICE_ARROW, [Items.ICE_ARROW, Items.FAIRY_BOW, Items.PROGRESSIVE_MAGIC_METER])

    def test_light_arrow(self):
        self.require_all(Items.LIGHT_ARROW, [Items.LIGHT_ARROW, Items.FAIRY_BOW, Items.PROGRESSIVE_MAGIC_METER])

    def test_play_song_buttons_shuffled(self):
        self.world.options.shuffle_ocarina_buttons.value = Options.ShuffleOcarinaButtons.option_true
        self.require_all(Items.EPONAS_SONG, [Items.PROGRESSIVE_OCARINA, Items.EPONAS_SONG, Items.OCARINA_CLEFT_BUTTON, Items.OCARINA_CRIGHT_BUTTON, Items.OCARINA_CUP_BUTTON])

    def test_play_song_no_button_substitutions(self):
        # other buttons aren't suitable replacements
        self.world.options.shuffle_ocarina_buttons.value = Options.ShuffleOcarinaButtons.option_true
        self.collect(self.create_item(Items.OCARINA_A_BUTTON))
        self.collect(self.create_item(Items.OCARINA_CDOWN_BUTTON))
        self.require_all(Items.EPONAS_SONG, [Items.PROGRESSIVE_OCARINA, Items.EPONAS_SONG, Items.OCARINA_CLEFT_BUTTON, Items.OCARINA_CRIGHT_BUTTON, Items.OCARINA_CUP_BUTTON])

    def test_play_song(self):
        self.world.options.shuffle_ocarina_buttons.value = Options.ShuffleOcarinaButtons.option_false
        self.require_all(Items.EPONAS_SONG, [Items.PROGRESSIVE_OCARINA, Items.EPONAS_SONG])

class TestCanUseAdultOnlyItems(SohTestBase):
    options = {"starting_age": "adult", 
                "closed_forest": "off", 
                "shuffle_songs": "anywhere",
                "shuffle_dungeon_rewards": "anywhere",
                "door_of_time": "song_only",
                "links_pocket": "nothing"}
    
    def test_adult_items_from_start(self):
        # can you use this item at an adult reachable location
        self.sweep()
        self.collect_by_name(Items.MIRROR_SHIELD)
        self.assertTrue(LogicHelpers.can_use(Items.MIRROR_SHIELD, self.get_reg_bundle(Regions.ADULT_SPAWN)), "Should be able to use adult items in adult reachable locations from the start")

    def test_cant_use_child_items_as_adult(self):
        self.sweep()
        self.collect_by_name(Items.BOOMERANG)
        self.assertFalse(LogicHelpers.can_use(Items.BOOMERANG, self.get_reg_bundle(Regions.ADULT_SPAWN)), "Shouldn't be able to use child restricted items area's unreachable by child")

    def test_child_items_after_timetravel(self):
        self.sweep()
        self.collect_by_name(Items.BOOMERANG)
        self.assertFalse(LogicHelpers.can_use(Items.BOOMERANG, self.get_reg_bundle(Regions.CHILD_SPAWN)), "Shouldn't be able to use child restricted items area's unreachable by child")
        self.collect(self.create_item(Events.TIME_TRAVEL))
        self.assertTrue(LogicHelpers.can_use(Items.BOOMERANG, self.get_reg_bundle(Regions.CHILD_SPAWN)), "Should be able to use child restricted items area's reachable by child")

class TestCanUseChildOnlyItems(SohTestBase):
    options = {"starting_age": "child", 
                "closed_forest": "on", 
                "shuffle_songs": "anywhere",
                "shuffle_dungeon_rewards": "anywhere",
                "door_of_time": "song_only",
                "links_pocket": "nothing"}
    
    def test_child_items_from_start(self):
        # can you use this item at an adult reachable location
        self.sweep()
        self.collect_by_name(Items.BOOMERANG)
        self.assertTrue(LogicHelpers.can_use(Items.BOOMERANG, self.get_reg_bundle(Regions.CHILD_SPAWN)), "Should be able to use adult items in adult reachable locations from the start")

    def test_cant_use_child_items_as_adult(self):
        self.sweep()
        self.collect_by_name(Items.MIRROR_SHIELD)
        self.assertFalse(LogicHelpers.can_use(Items.MIRROR_SHIELD, self.get_reg_bundle(Regions.CHILD_SPAWN)), "Shouldn't be able to use child restricted items area's unreachable by child")

    def test_child_items_after_timetravel(self):
        self.sweep()
        self.collect_by_name(Items.MIRROR_SHIELD)
        self.assertFalse(LogicHelpers.can_use(Items.MIRROR_SHIELD, self.get_reg_bundle(Regions.ADULT_SPAWN)), "Shouldn't be able to use child restricted items area's unreachable by child")
        self.collect(self.create_item(Events.TIME_TRAVEL))
        self.assertTrue(LogicHelpers.can_use(Items.MIRROR_SHIELD, self.get_reg_bundle(Regions.ADULT_SPAWN)), "Should be able to use child restricted items area's reachable by child")
        