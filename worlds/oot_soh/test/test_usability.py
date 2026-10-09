from .bases import SohTestBase
from ..Enums import Items, HostEvents
from ..enums_gen import Regions, Events
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
    
    def require_all(self, check: Items, items: list[Items | Events | HostEvents]) -> None:
        # ideally we run these as subtests, but those are currently broken 
        # and report as Success if any subtest succeeds
        # (https://github.com/microsoft/vscode-python/issues/25824)
        self.sweep()
        self.assertFalse(LogicHelpers.can_use(self.get_bundle(), check)._instantiate(self.world)._evaluate(self.multiworld.state))
        required_items = list(map(lambda i: self.create_item(i), items))
        for size in range(1, len(required_items)):
            for invalid_combo in itertools.combinations(required_items, size):
                self.collect(invalid_combo)
                self.assertFalse(LogicHelpers.can_use(self.get_bundle(), check)._instantiate(self.world)._evaluate(self.multiworld.state), f"{str(check)} should not be usable with only {invalid_combo}")
                self.remove(invalid_combo)
        self.collect(required_items)
        self.assertTrue(LogicHelpers.can_use(self.get_bundle(), check)._instantiate(self.world)._evaluate(self.multiworld.state))
        
        
    def require_any(self, check, items) -> None:
        # ideally we run these as subtests, but those are currently broken 
        # and report as Success if any subtest succeeds
        # (https://github.com/microsoft/vscode-python/issues/25824)
        self.sweep()
        self.assertFalse(LogicHelpers.can_use(self.get_bundle(), check)._instantiate(self.world)._evaluate(self.multiworld.state))
        required_items = list(map(lambda i: self.create_item(i), items))
        for size in range(1, len(required_items)):
            for invalid_combo in itertools.combinations(required_items, size):
                self.collect(invalid_combo)
                self.assertTrue(LogicHelpers.can_use(self.get_bundle(), check)._instantiate(self.world)._evaluate(self.multiworld.state), f"{str(check)} should be usable with {invalid_combo}")
                self.remove(invalid_combo)
        self.collect(required_items)
        self.assertTrue(LogicHelpers.can_use(self.get_bundle(), check)._instantiate(self.world)._evaluate(self.multiworld.state))


    def test_magic_item(self):
        self.require_all(Items.RG_DINS_FIRE, [Items.RG_DINS_FIRE, Items.RG_PROGRESSIVE_MAGIC_METER])

    def test_sticks(self):
        self.require_all(Items.RG_STICKS, [Items.RG_PROGRESSIVE_STICK_UPGRADE, Events.LOGIC_STICK_ACCESS])

    def test_explosives(self):
        self.sweep()
        bombchu_items = (Items.RG_PROGRESSIVE_BOMBCHU_BAG, Items.RG_PROGRESSIVE_BOMB_BAG)
        for item in bombchu_items:
            #with self.subTest(item=item):
            self.assertFalse(LogicHelpers.can_use(self.get_bundle(), item)._instantiate(self.world)._evaluate(self.multiworld.state), "You need to get Bags first before you can use them")

        bomb_bag = self.create_item(Items.RG_PROGRESSIVE_BOMB_BAG)
        self.collect(bomb_bag)
        self.assertTrue(LogicHelpers.can_use(self.get_bundle(), Items.RG_PROGRESSIVE_BOMB_BAG)._instantiate(self.world)._evaluate(self.multiworld.state), "With the bomb bag unlocked you should be able to use bombs")
        self.assertFalse(LogicHelpers.can_use(self.get_bundle(), Items.RG_PROGRESSIVE_BOMBCHU_BAG)._instantiate(self.world)._evaluate(self.multiworld.state), "With bombchu bags shuffled you explicitly need the bombchu bag to them")

        self.collect(self.create_item(Items.RG_PROGRESSIVE_BOMBCHU_BAG))
        self.remove(bomb_bag)
        self.assertTrue(LogicHelpers.can_use(self.get_bundle(), Items.RG_PROGRESSIVE_BOMBCHU_BAG)._instantiate(self.world)._evaluate(self.multiworld.state), "With bombchu bag shuffled and found you should be able to use it")
        self.assertFalse(LogicHelpers.can_use(self.get_bundle(), Items.RG_PROGRESSIVE_BOMB_BAG)._instantiate(self.world)._evaluate(self.multiworld.state), "The bombchu bag alone doesn't grant access to bombs")

    def test_nuts(self):
        self.require_all(Items.RG_NUTS, [Items.RG_PROGRESSIVE_NUT_UPGRADE, Events.LOGIC_NUT_ACCESS])

    def test_beans(self):
        self.require_any(Items.RG_MAGIC_BEAN, [Items.RG_MAGIC_BEAN_PACK, HostEvents.CAN_BUY_BEANS])
    
    def shield(self, shield: Items, buy: Items):
        self.sweep()
        self.assertFalse(LogicHelpers.can_use(self.get_bundle(), shield)._instantiate(self.world)._evaluate(self.multiworld.state), "You need to get the shield before you can use it")
        self.collect(self.create_item(shield))
        self.assertFalse(LogicHelpers.can_use(self.get_bundle(), shield)._instantiate(self.world)._evaluate(self.multiworld.state), "shields can be lost to fire or like-likes, thus found shields shouldn't be considered in logic")
        
        self.collect(self.create_item(buy))
        self.assertTrue(LogicHelpers.can_use(self.get_bundle(), shield)._instantiate(self.world)._evaluate(self.multiworld.state), "Deku shields are only considered in logic if you can buy them")

    def test_deku_shield(self):
        self.sweep()
        self.assertFalse(LogicHelpers.can_use(self.get_bundle(), Items.RG_DEKU_SHIELD)._instantiate(self.world)._evaluate(self.multiworld.state), "You need to get the shield before you can use it")
        self.collect(self.create_item(Items.RG_DEKU_SHIELD))
        self.assertFalse(LogicHelpers.can_use(self.get_bundle(), Items.RG_DEKU_SHIELD)._instantiate(self.world)._evaluate(self.multiworld.state), "shields can be lost to fire or like-likes, thus found shields shouldn't be considered in logic")
        
        self.collect(self.create_item(Items.RG_BUY_DEKU_SHIELD))
        self.assertTrue(LogicHelpers.can_use(self.get_bundle(), Items.RG_DEKU_SHIELD)._instantiate(self.world)._evaluate(self.multiworld.state), "Deku shields are only considered in logic if you can buy them")

    def test_hylian_shield(self):
        self.sweep()
        self.assertFalse(LogicHelpers.can_use(self.get_bundle(), Items.RG_HYLIAN_SHIELD)._instantiate(self.world)._evaluate(self.multiworld.state), "You need to get the shield before you can use it")
        self.collect(self.create_item(Items.RG_HYLIAN_SHIELD))
        self.assertFalse(LogicHelpers.can_use(self.get_bundle(), Items.RG_HYLIAN_SHIELD)._instantiate(self.world)._evaluate(self.multiworld.state), "shields can be lost to fire or like-likes, thus found shields shouldn't be considered in logic")
        
        self.collect(self.create_item(Items.RG_BUY_HYLIAN_SHIELD))
        self.assertTrue(LogicHelpers.can_use(self.get_bundle(), Items.RG_HYLIAN_SHIELD)._instantiate(self.world)._evaluate(self.multiworld.state), "Hylian shields are only considered in logic if you can buy them")

    def test_goron_tunic(self):
        self.require_any(Items.RG_GORON_TUNIC, [Items.RG_BUY_GORON_TUNIC, Items.RG_GORON_TUNIC])

    def test_zora_tunic(self):
        self.require_any(Items.RG_ZORA_TUNIC, [Items.RG_BUY_ZORA_TUNIC, Items.RG_ZORA_TUNIC])

    def test_scarecrow(self):
        self.require_all(Items.RG_SCARECROW, [Items.RG_PROGRESSIVE_OCARINA, Items.RG_PROGRESSIVE_HOOKSHOT])
        
    def test_scarecrow_distant(self):
        self.require_all(Items.RG_DISTANT_SCARECROW, [Items.RG_PROGRESSIVE_OCARINA, Items.RG_PROGRESSIVE_HOOKSHOT, Items.RG_PROGRESSIVE_HOOKSHOT])

    def test_fishing_pole(self):
        self.sweep()
        self.assertFalse(LogicHelpers.can_use(self.get_bundle(), Items.RG_FISHING_POLE)._instantiate(self.world)._evaluate(self.multiworld.state), "when pole isn't shuffled, you require only the child wallet")
        self.collect(self.create_item(Items.RG_PROGRESSIVE_WALLET))
        self.assertTrue(LogicHelpers.can_use(self.get_bundle(), Items.RG_FISHING_POLE)._instantiate(self.world)._evaluate(self.multiworld.state), "when pole isn't shuffled it should be usable with only the wallet")
        
    def test_fishing_pole_shuffled(self):
        self.world.options.shuffle_fishing_pole.value = Options.ShuffleFishingPole.option_true
        self.require_all(Items.RG_FISHING_POLE, [Items.RG_FISHING_POLE, Items.RG_PROGRESSIVE_WALLET])

    def test_epona(self):
        self.require_all(Items.RG_EPONA, [Items.RG_PROGRESSIVE_OCARINA, Items.RG_EPONAS_SONG])
    
    def test_trade_items(self):
        # when creating this test the shuffle_adult_trade_items option is turned on so trade items aren't pre-collected
        trade_items = [Items.RG_POCKET_EGG, Items.RG_COJIRO, Items.RG_ODD_MUSHROOM, Items.RG_ODD_POTION, Items.RG_POACHERS_SAW,
                       Items.RG_BROKEN_SWORD, Items.RG_PRESCRIPTION, Items.RG_EYEBALL_FROG, Items.RG_EYEDROPS]
        
        self.sweep()
        self.world.options.shuffle_adult_trade_items.value = Options.RSK_SHUFFLE_ADULT_TRADE.option_false
        for item in trade_items:
            self.assertTrue(LogicHelpers.can_use(self.get_bundle(), item)._instantiate(self.world)._evaluate(self.multiworld.state), f"Without trade items shuffled {item} should be seen as usable")

        self.world.options.shuffle_adult_trade_items.value = Options.RSK_SHUFFLE_ADULT_TRADE.option_true
        for item in trade_items:
            self.assertFalse(LogicHelpers.can_use(self.get_bundle(), item)._instantiate(self.world)._evaluate(self.multiworld.state), f"With trade items shuffled you shouldn't be able to use {item} untill you get it")
        
        as_items = list(map(lambda i: self.create_item(i), trade_items))
        for item in as_items:
            item_set = set(as_items)
            item_set.remove(item)
            self.collect(item_set)
            self.assertFalse(LogicHelpers.can_use(self.get_bundle(), Items(item.name))._instantiate(self.world)._evaluate(self.multiworld.state), f"the other trade items are not a substitute for {item.name}")
            self.remove(item_set)
            self.collect(item)
            self.assertTrue(LogicHelpers.can_use(self.get_bundle(), Items(item.name))._instantiate(self.world)._evaluate(self.multiworld.state), f"you need the trade item in order to use it")
            self.remove(item)

    def bottles(self, bottle: Items, event: list[Items | Events | HostEvents]):
        self.sweep()
        self.assertFalse(LogicHelpers.can_use(self.get_bundle(), bottle)._instantiate(self.world)._evaluate(self.multiworld.state), "Bottles can't be used of you don't have any bottles")
        self.collect(self.create_item(Items.RG_EMPTY_BOTTLE))
        self.assertFalse(LogicHelpers.can_use(self.get_bundle(), bottle)._instantiate(self.world)._evaluate(self.multiworld.state), f"{bottle} can't be used of you don't have access to {event} as well")        
        self.require_any(bottle, event)

    def no_requirement_bottle(self, bottle: Items):
        self.sweep()
        self.assertFalse(LogicHelpers.can_use(self.get_bundle(), bottle)._instantiate(self.world)._evaluate(self.multiworld.state), "Bottles can't be used of you don't have any bottles")
        self.collect(self.create_item(Items.RG_EMPTY_BOTTLE))
        self.assertTrue(LogicHelpers.can_use(self.get_bundle(), bottle)._instantiate(self.world)._evaluate(self.multiworld.state), f"current rules dictate you can use {bottle} if you just have an empty bottle")

    def test_bottle_blue_fire(self):
        self.bottles(Items.RG_BOTTLE_WITH_BLUE_FIRE, [Events.LOGIC_BLUE_FIRE_ACCESS, Items.RG_BUY_BLUE_FIRE])

    def test_bottle_blue_potion(self):
        self.bottles(Items.RG_BOTTLE_WITH_BLUE_POTION, [Items.RG_BUY_BLUE_POTION])

    def test_bottle_bugs(self):
        self.bottles(Items.RG_BOTTLE_WITH_BUGS, [Items.RG_BUY_BOTTLE_BUG, Events.LOGIC_BUG_ACCESS])
    
    def test_bottle_fairy(self):
        self.bottles(Items.RG_BOTTLE_WITH_FAIRY, [Items.RG_BUY_FAIRYS_SPIRIT, Events.LOGIC_FAIRY_ACCESS])
    
    def test_bottle_fish(self):
        self.bottles(Items.RG_BOTTLE_WITH_FISH, [Items.RG_BUY_FISH, Events.LOGIC_FISH_ACCESS])

    def test_bottle_green_potion(self):
        self.bottles(Items.RG_BOTTLE_WITH_GREEN_POTION, [Items.RG_BUY_GREEN_POTION])

    # these bottles might want some extra checks added to them if they ever start getting used in logic
    def test_bottle_milk(self):
        self.no_requirement_bottle(Items.RG_BOTTLE_WITH_MILK)

    def test_bottle_poe(self):
        self.no_requirement_bottle(Items.RG_BOTTLE_WITH_POE)

    def test_bottle_red_potion(self):
        self.no_requirement_bottle(Items.RG_BOTTLE_WITH_RED_POTION)

    def test_bottle_empty(self):
        self.no_requirement_bottle(Items.RG_EMPTY_BOTTLE)

    def test_fire_arrow(self):
        self.require_all(Items.RG_FIRE_ARROWS, [Items.RG_FIRE_ARROWS, Items.RG_PROGRESSIVE_BOW, Items.RG_PROGRESSIVE_MAGIC_METER])

    def test_ice_arrow(self):
        self.require_all(Items.RG_ICE_ARROWS, [Items.RG_ICE_ARROWS, Items.RG_PROGRESSIVE_BOW, Items.RG_PROGRESSIVE_MAGIC_METER])

    def test_light_arrow(self):
        self.require_all(Items.RG_LIGHT_ARROWS, [Items.RG_LIGHT_ARROWS, Items.RG_PROGRESSIVE_BOW, Items.RG_PROGRESSIVE_MAGIC_METER])

    def test_play_song_buttons_shuffled(self):
        self.world.options.shuffle_ocarina_buttons.value = Options.ShuffleOcarinaButtons.option_true
        self.require_all(Items.RG_EPONAS_SONG, [Items.RG_PROGRESSIVE_OCARINA, Items.RG_EPONAS_SONG, Items.RG_OCARINA_C_LEFT_BUTTON, Items.RG_OCARINA_C_RIGHT_BUTTON, Items.RG_OCARINA_C_UP_BUTTON])

    def test_play_song_no_button_substitutions(self):
        # other buttons aren't suitable replacements
        self.world.options.shuffle_ocarina_buttons.value = Options.ShuffleOcarinaButtons.option_true
        self.collect(self.create_item(Items.RG_OCARINA_A_BUTTON))
        self.collect(self.create_item(Items.RG_OCARINA_C_DOWN_BUTTON))
        self.require_all(Items.RG_EPONAS_SONG, [Items.RG_PROGRESSIVE_OCARINA, Items.RG_EPONAS_SONG, Items.RG_OCARINA_C_LEFT_BUTTON, Items.RG_OCARINA_C_RIGHT_BUTTON, Items.RG_OCARINA_C_UP_BUTTON])

    def test_play_song(self):
        self.world.options.shuffle_ocarina_buttons.value = Options.ShuffleOcarinaButtons.option_false
        self.require_all(Items.RG_EPONAS_SONG, [Items.RG_PROGRESSIVE_OCARINA, Items.RG_EPONAS_SONG])

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
        self.collect_by_name(Items.RG_MIRROR_SHIELD)
        self.assertTrue(LogicHelpers.can_use(self.get_reg_bundle(Regions.RR_ADULT_SPAWN), Items.RG_MIRROR_SHIELD)._instantiate(self.world)._evaluate(self.multiworld.state), "Should be able to use adult items in adult reachable locations from the start")

    def test_cant_use_child_items_as_adult(self):
        self.sweep()
        self.collect_by_name(Items.RG_BOOMERANG)
        self.assertFalse(LogicHelpers.can_use(self.get_reg_bundle(Regions.RR_ADULT_SPAWN), Items.RG_BOOMERANG)._instantiate(self.world)._evaluate(self.multiworld.state), "Shouldn't be able to use child restricted items area's unreachable by child")

    def test_child_items_after_timetravel(self):
        self.sweep()
        self.collect_by_name(Items.RG_BOOMERANG)
        self.assertFalse(LogicHelpers.can_use(self.get_reg_bundle(Regions.RR_CHILD_SPAWN), Items.RG_BOOMERANG)._instantiate(self.world)._evaluate(self.multiworld.state), "Shouldn't be able to use child restricted items area's unreachable by child")
        self.collect(self.create_item(HostEvents.TIME_TRAVEL))
        self.assertTrue(LogicHelpers.can_use(self.get_reg_bundle(Regions.RR_CHILD_SPAWN), Items.RG_BOOMERANG)._instantiate(self.world)._evaluate(self.multiworld.state), "Should be able to use child restricted items area's reachable by child")

class TestCanUseChildOnlyItems(SohTestBase):
    options = {"starting_age": "child", 
                "closed_forest": "off", 
                "shuffle_songs": "anywhere",
                "shuffle_dungeon_rewards": "anywhere",
                "door_of_time": "song_only",
                "links_pocket": "nothing"}
    
    def test_child_items_from_start(self):
        # can you use this item at an adult reachable location
        self.sweep()
        self.collect_by_name(Items.RG_BOOMERANG)
        self.assertTrue(LogicHelpers.can_use(self.get_reg_bundle(Regions.RR_CHILD_SPAWN), Items.RG_BOOMERANG)._instantiate(self.world)._evaluate(self.multiworld.state), "Should be able to use adult items in adult reachable locations from the start")

    def test_cant_use_child_items_as_adult(self):
        self.sweep()
        self.collect_by_name(Items.RG_MIRROR_SHIELD)
        self.assertFalse(LogicHelpers.can_use(self.get_reg_bundle(Regions.RR_CHILD_SPAWN), Items.RG_MIRROR_SHIELD)._instantiate(self.world)._evaluate(self.multiworld.state), "Shouldn't be able to use child restricted items area's unreachable by child")

    def test_child_items_after_timetravel(self):
        self.sweep()
        self.collect_by_name(Items.RG_MIRROR_SHIELD)
        self.assertFalse(LogicHelpers.can_use(self.get_reg_bundle(Regions.RR_ADULT_SPAWN), Items.RG_MIRROR_SHIELD)._instantiate(self.world)._evaluate(self.multiworld.state), "Shouldn't be able to use child restricted items area's unreachable by child")
        self.collect(self.create_item(HostEvents.TIME_TRAVEL))
        self.assertTrue(LogicHelpers.can_use(self.get_reg_bundle(Regions.RR_ADULT_SPAWN), Items.RG_MIRROR_SHIELD)._instantiate(self.world)._evaluate(self.multiworld.state), "Should be able to use child restricted items area's reachable by child")
        