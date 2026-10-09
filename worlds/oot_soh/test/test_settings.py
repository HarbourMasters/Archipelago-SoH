from .. import SohWorld
from ..Options import *
from ..Items import Items, SohItem
from ..enums_gen import Events
from .bases import SohTestBase
from ..functions_gen import bombchu_refill, is_fire_loop_locked, scarecrows_song, trade_quest_step
from ..LogicHelpers import can_build_rainbow_bridge, can_trigger_lacs
from itertools import combinations

# Fire Loop
class FireLoopLockedAnywhere(SohTestBase):
    options = {"small_key_shuffle": RSK_KEYSANITY.option_anywhere}
    def test_fire_loop_locked(self):
        self.assertTrue(is_fire_loop_locked(self.get_bundle()).resolve(self.world)._evaluate(self.multiworld.state), f"Fire Loop was unlocked but should have been locked.")

class FireLoopLockedAnyDungeon(SohTestBase):
    options = {"small_key_shuffle": RSK_KEYSANITY.option_any_dungeon}
    def test_fire_loop_locked(self):
        self.assertTrue(is_fire_loop_locked(self.get_bundle()).resolve(self.world)._evaluate(self.multiworld.state), f"Fire Loop was unlocked but should have been locked.")

class FireLoopLockedOverworld(SohTestBase):
    options = {"small_key_shuffle": RSK_KEYSANITY.option_overworld}
    def test_fire_loop_locked(self):
        self.assertTrue(is_fire_loop_locked(self.get_bundle()).resolve(self.world)._evaluate(self.multiworld.state), f"Fire Loop was unlocked but should have been locked.")

class FireLoopUnlockedOwnDungeon(SohTestBase):
    options = {"small_key_shuffle": RSK_KEYSANITY.option_own_dungeon}
    def test_fire_loop_unlocked(self):
        self.assertFalse(is_fire_loop_locked(self.get_bundle()).resolve(self.world)._evaluate(self.multiworld.state), f"Fire Loop was locked but should not have been.")

class FireLoopUnlockedVanilla(SohTestBase):
    options = {"small_key_shuffle": RSK_KEYSANITY.option_vanilla}
    def test_fire_loop_unlocked(self):
        self.assertFalse(is_fire_loop_locked(self.get_bundle()).resolve(self.world)._evaluate(self.multiworld.state), f"Fire Loop was locked but should not have been.")


# LACS
class LACSBase(SohTestBase):
    __Test__ = False

    def require_all_lacs(self, items: list[Items | Events]) -> None:
        # ideally we run these as subtests, but those are currently broken 
        # and report as Success if any subtest succeeds
        # (https://github.com/microsoft/vscode-python/issues/25824)
        self.sweep()
        self.assertFalse(can_trigger_lacs(self.get_bundle())._instantiate(self.world)._evaluate(self.multiworld.state), f"Could trigger LACS but shouldn't have been able to.")
        required_items = list(map(lambda i: self.create_item(i), items))
        for size in range(1, len(required_items)):
            for invalid_combo in combinations(required_items, size):
                self.collect(invalid_combo)
                self.assertFalse(can_trigger_lacs(self.get_bundle())._instantiate(self.world)._evaluate(self.multiworld.state), f"Should not be able to trigger LACS with only {invalid_combo}")
                self.remove(invalid_combo)
        self.collect(required_items)
        self.assertTrue(can_trigger_lacs(self.get_bundle())._instantiate(self.world)._evaluate(self.multiworld.state), f"Wasn't able to trigger LACS, but should have been able to.")
        
        
    def require_some_lacs(self, items: list[Items | Events], required_amount: int) -> None:
        # ideally we run these as subtests, but those are currently broken 
        # and report as Success if any subtest succeeds
        # (https://github.com/microsoft/vscode-python/issues/25824)
        self.sweep()
        self.assertFalse(can_trigger_lacs(self.get_bundle())._instantiate(self.world)._evaluate(self.multiworld.state), f"Could trigger LACS but shouldn't have been able to.")
        required_items = list(map(lambda i: self.create_item(i), items))
        for size in range(1, len(required_items)):
            for invalid_combo in combinations(required_items, size):
                self.collect(invalid_combo)
                if required_amount <= len(invalid_combo) and not (Items.RG_GREG_RUPEE in invalid_combo and self.options["ganons_castle_boss_key_greg_modifier"] != GanonsCastleBossKeyGregModifier.option_reward):
                    self.assertTrue(can_trigger_lacs(self.get_bundle())._instantiate(self.world)._evaluate(self.multiworld.state), f"Wasn't able to trigger LACS, but should have been able to with count {required_amount}, {invalid_combo}")
                else:
                    self.assertFalse(can_trigger_lacs(self.get_bundle())._instantiate(self.world)._evaluate(self.multiworld.state), f"Should not be able to trigger LACS with only {invalid_combo}. Required amount:{required_amount}")

                self.remove(invalid_combo)
        self.collect(required_items)
        self.assertTrue(can_trigger_lacs(self.get_bundle())._instantiate(self.world)._evaluate(self.multiworld.state), f"Wasn't able to trigger LACS, but should have been able to.")

# Greg Specific
class TestCanTriggerLacsTestGregSoloReward(LACSBase):
    """
    Test can_trigger_lacs greg solo reward
    """
    options = {"ganons_castle_boss_key": GanonsCastleBossKey.option_lacs_stones, 
               "ganons_castle_boss_key_stones_required": 1,
               "ganons_castle_boss_key_greg_modifier": GanonsCastleBossKeyGregModifier.option_reward}

    def test_greg_solo_reward(self):
        self.require_all_lacs([Items.RG_GREG_RUPEE])

class TestCanTriggerLacsGregSoloNonReward(LACSBase):
    """
    Test can_trigger_lacs stones greg solo non reward
    """
    options = {"ganons_castle_boss_key": GanonsCastleBossKey.option_lacs_stones, 
               "ganons_castle_boss_key_stones_required": 1,
               "ganons_castle_boss_key_greg_modifier": GanonsCastleBossKeyGregModifier.option_off}

    def test_stones_greg_solo_nonreward(self):
        self.assertFalse(can_trigger_lacs(self.get_bundle())._instantiate(self.world)._evaluate(self.multiworld.state), f"Could trigger LACS but shouldn't have been able to.")
        self.collect(self.create_item(Items.RG_GREG_RUPEE))
        self.assertFalse(can_trigger_lacs(self.get_bundle())._instantiate(self.world)._evaluate(self.multiworld.state), f"Could trigger LACS but shouldn't have been able to.")


# Vanilla
class TestCanTriggerLacsVanilla(LACSBase):
    """
    Test can_trigger_lacs vanilla
    """
    options = {"ganons_castle_boss_key": GanonsCastleBossKey.option_vanilla,
               "door_of_time": RSK_DOOR_OF_TIME.option_closed, 
               "start_with_links_pocket": StartWithLinksPocket.option_nothing,
               "shuffle_dungeon_rewards": ShuffleDungeonRewards.option_anywhere,}

    def test_vanilla_setting(self):
        self.require_all_lacs([Items.RG_SHADOW_MEDALLION, Items.RG_SPIRIT_MEDALLION])

class TestCanTriggerLacsAnywhere(LACSBase):
    """
    Test can_trigger_lacs anywhere
    """
    options = {"ganons_castle_boss_key": GanonsCastleBossKey.option_anywhere,
               "door_of_time": RSK_DOOR_OF_TIME.option_closed, 
               "start_with_links_pocket": StartWithLinksPocket.option_nothing,
               "shuffle_dungeon_rewards": ShuffleDungeonRewards.option_anywhere,}

    def test_anywhere_setting(self):
        self.require_all_lacs([Items.RG_SHADOW_MEDALLION, Items.RG_SPIRIT_MEDALLION])

class TestCanTriggerLacsLACSVanilla(LACSBase):
    """
    Test can_trigger_lacs anywhere
    """
    options = {"ganons_castle_boss_key": GanonsCastleBossKey.option_lacs_vanilla,
               "door_of_time": RSK_DOOR_OF_TIME.option_closed, 
               "start_with_links_pocket": StartWithLinksPocket.option_nothing,
               "shuffle_dungeon_rewards": ShuffleDungeonRewards.option_anywhere,}

    def test_lacs_vanilla_setting(self):
        self.require_all_lacs([Items.RG_SHADOW_MEDALLION, Items.RG_SPIRIT_MEDALLION])

# Stones
class TestCanTriggerLacsStonesAll(LACSBase):
    """
    Test can_trigger_lacs all stones
    """
    options = {"ganons_castle_boss_key": GanonsCastleBossKey.option_lacs_stones, 
               "door_of_time": RSK_DOOR_OF_TIME.option_closed, 
               "start_with_links_pocket": StartWithLinksPocket.option_nothing,
               "shuffle_dungeon_rewards": ShuffleDungeonRewards.option_anywhere,
               "ganons_castle_boss_key_stones_required": 3}

    def test_stones_all(self):
        self.require_all_lacs([Items.RG_KOKIRI_EMERALD, Items.RG_GORON_RUBY, Items.RG_ZORA_SAPPHIRE])

class TestCanTriggerLacsStonesFew(LACSBase):
    """
    Test can_trigger_lacs a few stones
    """
    options = {"ganons_castle_boss_key": GanonsCastleBossKey.option_lacs_stones, 
               "door_of_time": RSK_DOOR_OF_TIME.option_closed, 
               "start_with_links_pocket": StartWithLinksPocket.option_nothing,
               "shuffle_dungeon_rewards": ShuffleDungeonRewards.option_anywhere,
               "ganons_castle_boss_key_stones_required": 2}

    def test_stones_few(self):
        self.require_some_lacs([Items.RG_KOKIRI_EMERALD, Items.RG_GORON_RUBY, Items.RG_ZORA_SAPPHIRE], 
                               self.options["ganons_castle_boss_key_stones_required"])

class TestCanTriggerLacsStonesGregReward(LACSBase):
    """
    Test can_trigger_lacs stones greg reward
    """
    options = {"ganons_castle_boss_key": GanonsCastleBossKey.option_lacs_stones, 
                "door_of_time": RSK_DOOR_OF_TIME.option_closed, 
               "start_with_links_pocket": StartWithLinksPocket.option_nothing,
               "shuffle_dungeon_rewards": ShuffleDungeonRewards.option_anywhere,
               # Needs to be updated when Greg Reward fixes get merged
               "ganons_castle_boss_key_stones_required": 3,
               "ganons_castle_boss_key_greg_modifier": GanonsCastleBossKeyGregModifier.option_reward}

    def test_stones_greg_all(self):
        # Needs to be updated when Greg Reward fixes get merged
        self.require_some_lacs([Items.RG_KOKIRI_EMERALD, Items.RG_GORON_RUBY, Items.RG_ZORA_SAPPHIRE, 
                                Items.RG_GREG_RUPEE], self.options["ganons_castle_boss_key_stones_required"])

# Medallions
class TestCanTriggerLacsMedallionsAll(LACSBase):
    """
    Test can_trigger_lacs all medallions
    """
    options = {"ganons_castle_boss_key": GanonsCastleBossKey.option_lacs_medallions, 
               "ganons_castle_boss_key_medallions_required": 6, 
               "door_of_time": RSK_DOOR_OF_TIME.option_closed, 
               "start_with_links_pocket": StartWithLinksPocket.option_nothing,
               "shuffle_dungeon_rewards": ShuffleDungeonRewards.option_anywhere}

    def test_medallions_all(self):
        self.require_all_lacs([Items.RG_FOREST_MEDALLION, Items.RG_FIRE_MEDALLION, Items.RG_WATER_MEDALLION, 
                               Items.RG_SPIRIT_MEDALLION, Items.RG_SHADOW_MEDALLION, Items.RG_LIGHT_MEDALLION])

class TestCanTriggerLacsMedallionsFew(LACSBase):
    """
    Test can_trigger_lacs a few medallions
    """
    options = {"ganons_castle_boss_key": GanonsCastleBossKey.option_lacs_medallions, 
               "ganons_castle_boss_key_medallions_required": 5,
               "door_of_time": RSK_DOOR_OF_TIME.option_closed, 
               "start_with_links_pocket": StartWithLinksPocket.option_nothing,
               "shuffle_dungeon_rewards": ShuffleDungeonRewards.option_anywhere,}

    def test_medallions_few(self):
        self.require_some_lacs([Items.RG_FOREST_MEDALLION, Items.RG_FIRE_MEDALLION, Items.RG_WATER_MEDALLION, 
                               Items.RG_SPIRIT_MEDALLION, Items.RG_SHADOW_MEDALLION, Items.RG_LIGHT_MEDALLION], self.options["ganons_castle_boss_key_medallions_required"])

class TestCanTriggerLacsMedallionsGregReward(LACSBase):
    """
    Test can_trigger_lacs medallions greg reward
    """
    options = {"ganons_castle_boss_key": GanonsCastleBossKey.option_lacs_medallions, 
               # Needs to be updated when Greg Reward fixes get merged
               "ganons_castle_boss_key_medallions_required": 6,
               "ganons_castle_boss_key_greg_modifier": GanonsCastleBossKeyGregModifier.option_reward,
               "door_of_time": RSK_DOOR_OF_TIME.option_closed, 
               "start_with_links_pocket": StartWithLinksPocket.option_nothing,
               "shuffle_dungeon_rewards": ShuffleDungeonRewards.option_anywhere,}

    def test_medallions_greg_all(self):
        # Needs to be updated when Greg Reward fixes get merged
        self.require_some_lacs([Items.RG_FOREST_MEDALLION, Items.RG_FIRE_MEDALLION, Items.RG_WATER_MEDALLION, 
                               Items.RG_SPIRIT_MEDALLION, Items.RG_SHADOW_MEDALLION, Items.RG_LIGHT_MEDALLION,
                                Items.RG_GREG_RUPEE], self.options["ganons_castle_boss_key_medallions_required"])

# Dungeon Rewards
class TestCanTriggerLacsDungeonRewardsAll(LACSBase):
    """
    Test can_trigger_lacs all dungeonrewards
    """
    options = {"ganons_castle_boss_key": GanonsCastleBossKey.option_lacs_dungeon_rewards, 
               "door_of_time": RSK_DOOR_OF_TIME.option_closed, 
               "start_with_links_pocket": StartWithLinksPocket.option_nothing,
               "shuffle_dungeon_rewards": ShuffleDungeonRewards.option_anywhere,
               "ganons_castle_boss_key_dungeon_rewards_required": 9}

    def test_dungeon_rewards_all(self):
        self.require_all_lacs([Items.RG_KOKIRI_EMERALD, Items.RG_GORON_RUBY, Items.RG_ZORA_SAPPHIRE,
                                Items.RG_FOREST_MEDALLION, Items.RG_FIRE_MEDALLION, Items.RG_WATER_MEDALLION, 
                                Items.RG_SPIRIT_MEDALLION, Items.RG_SHADOW_MEDALLION, Items.RG_LIGHT_MEDALLION])

class TestCanTriggerLacsDungeonRewardsFew(LACSBase):
    """
    Test can_trigger_lacs a few dungeonrewards
    """
    options = {"ganons_castle_boss_key": GanonsCastleBossKey.option_lacs_dungeon_rewards, 
               "door_of_time": RSK_DOOR_OF_TIME.option_closed, 
               "start_with_links_pocket": StartWithLinksPocket.option_nothing,
               "shuffle_dungeon_rewards": ShuffleDungeonRewards.option_anywhere,
               "ganons_castle_boss_key_dungeon_rewards_required": 8}

    def test_dungeon_rewards_few(self):
        self.require_some_lacs([Items.RG_KOKIRI_EMERALD, Items.RG_GORON_RUBY, Items.RG_ZORA_SAPPHIRE,
                                Items.RG_FOREST_MEDALLION, Items.RG_FIRE_MEDALLION, Items.RG_WATER_MEDALLION, 
                                Items.RG_SPIRIT_MEDALLION, Items.RG_SHADOW_MEDALLION, Items.RG_LIGHT_MEDALLION], 
                               self.options["ganons_castle_boss_key_dungeon_rewards_required"])

class TestCanTriggerLacsDungeonRewardsGregReward(LACSBase):
    """
    Test can_trigger_lacs dungeonrewards greg reward
    """
    options = {"ganons_castle_boss_key": GanonsCastleBossKey.option_lacs_dungeon_rewards, 
                "door_of_time": RSK_DOOR_OF_TIME.option_closed, 
               "start_with_links_pocket": StartWithLinksPocket.option_nothing,
               "shuffle_dungeon_rewards": ShuffleDungeonRewards.option_anywhere,
               # Needs to be updated when Greg Reward fixes get merged
               "ganons_castle_boss_key_dungeon_rewards_required": 9,
               "ganons_castle_boss_key_greg_modifier": GanonsCastleBossKeyGregModifier.option_reward}

    def test_dungeon_rewards_greg_all(self):
        # Needs to be updated when Greg Reward fixes get merged
        self.require_some_lacs([Items.RG_KOKIRI_EMERALD, Items.RG_GORON_RUBY, Items.RG_ZORA_SAPPHIRE,
                                Items.RG_FOREST_MEDALLION, Items.RG_FIRE_MEDALLION, Items.RG_WATER_MEDALLION, 
                                Items.RG_SPIRIT_MEDALLION, Items.RG_SHADOW_MEDALLION, Items.RG_LIGHT_MEDALLION, 
                                Items.RG_GREG_RUPEE], self.options["ganons_castle_boss_key_dungeon_rewards_required"])

# Dungeons
class TestCanTriggerLacsDungeonsAll(LACSBase):
    """
    Test can_trigger_lacs all dungeons
    """
    options = {"ganons_castle_boss_key": GanonsCastleBossKey.option_lacs_dungeons, 
               "door_of_time": RSK_DOOR_OF_TIME.option_closed, 
               "start_with_links_pocket": StartWithLinksPocket.option_nothing,
               "shuffle_dungeon_rewards": ShuffleDungeonRewards.option_anywhere,
               "ganons_castle_boss_key_dungeons_required": 8}

    def test_dungeons_all(self):
        self.require_all_lacs([Events.LOGIC_DEKU_TREE_CLEAR, Events.LOGIC_DODONGOS_CAVERN_CLEAR, Events.LOGIC_JABU_JABUS_BELLY_CLEAR,
                               Events.LOGIC_FOREST_TEMPLE_CLEAR, Events.LOGIC_FIRE_TEMPLE_CLEAR, Events.LOGIC_WATER_TEMPLE_CLEAR,
                               Events.LOGIC_SHADOW_TEMPLE_CLEAR, Events.LOGIC_SPIRIT_TEMPLE_CLEAR])

class TestCanTriggerLacsDungeonsFew(LACSBase):
    """
    Test can_trigger_lacs a few dungeons
    """
    options = {"ganons_castle_boss_key": GanonsCastleBossKey.option_lacs_dungeons, 
               "door_of_time": RSK_DOOR_OF_TIME.option_closed, 
               "start_with_links_pocket": StartWithLinksPocket.option_nothing,
               "shuffle_dungeon_rewards": ShuffleDungeonRewards.option_anywhere,
               "ganons_castle_boss_key_dungeons_required": 7}

    def test_dungeons_few(self):
        self.require_some_lacs([Events.LOGIC_DEKU_TREE_CLEAR, Events.LOGIC_DODONGOS_CAVERN_CLEAR, Events.LOGIC_JABU_JABUS_BELLY_CLEAR,
                               Events.LOGIC_FOREST_TEMPLE_CLEAR, Events.LOGIC_FIRE_TEMPLE_CLEAR, Events.LOGIC_WATER_TEMPLE_CLEAR,
                               Events.LOGIC_SHADOW_TEMPLE_CLEAR, Events.LOGIC_SPIRIT_TEMPLE_CLEAR], 
                               self.options["ganons_castle_boss_key_dungeons_required"])

class TestCanTriggerLacsDungeonsGregReward(LACSBase):
    """
    Test can_trigger_lacs dungeons greg reward
    """
    options = {"ganons_castle_boss_key": GanonsCastleBossKey.option_lacs_dungeons, 
                "door_of_time": RSK_DOOR_OF_TIME.option_closed, 
               "start_with_links_pocket": StartWithLinksPocket.option_nothing,
               "shuffle_dungeon_rewards": ShuffleDungeonRewards.option_anywhere,
               # Needs to be updated when Greg Reward fixes get merged
               "ganons_castle_boss_key_dungeons_required": 8,
               "ganons_castle_boss_key_greg_modifier": GanonsCastleBossKeyGregModifier.option_reward}

    def test_dungeons_greg_all(self):
        # Needs to be updated when Greg Reward fixes get merged
        self.require_some_lacs([Events.LOGIC_DEKU_TREE_CLEAR, Events.LOGIC_DODONGOS_CAVERN_CLEAR, Events.LOGIC_JABU_JABUS_BELLY_CLEAR,
                                Events.LOGIC_FOREST_TEMPLE_CLEAR, Events.LOGIC_FIRE_TEMPLE_CLEAR, Events.LOGIC_WATER_TEMPLE_CLEAR,
                                Events.LOGIC_SHADOW_TEMPLE_CLEAR, Events.LOGIC_SPIRIT_TEMPLE_CLEAR, 
                                Items.RG_GREG_RUPEE], self.options["ganons_castle_boss_key_dungeons_required"])

# Tokens
class TestCanTriggerLacsTokensAll(LACSBase):
    """
    Test can_trigger_lacs all tokens
    """
    options = {"ganons_castle_boss_key": GanonsCastleBossKey.option_lacs_skull_tokens,
               "shuffle_skull_tokens": ShuffleTokens.option_all, 
               "ganons_castle_boss_key_skull_tokens_required": 100}

    def test_tokens_all(self):
        self.assertFalse(can_trigger_lacs(self.get_bundle())._instantiate(self.world)._evaluate(self.multiworld.state), f"Could trigger LACS but shouldn't have been able to.")
        self.collect(self.create_item(Items.RG_GOLD_SKULLTULA_TOKEN) for _ in range(99))
        self.assertFalse(can_trigger_lacs(self.get_bundle())._instantiate(self.world)._evaluate(self.multiworld.state), f"Could trigger LACS but shouldn't have been able to.")
        self.collect(self.create_item(Items.RG_GOLD_SKULLTULA_TOKEN))
        self.assertTrue(can_trigger_lacs(self.get_bundle())._instantiate(self.world)._evaluate(self.multiworld.state), f"Couldn't trigger LACS but should have been able to.")

# Rainbow Bridge
class RainbowBase(SohTestBase):
    __Test__ = False

    def require_all_rainbow(self, items: list[Items | Events]) -> None:
        # ideally we run these as subtests, but those are currently broken 
        # and report as Success if any subtest succeeds
        # (https://github.com/microsoft/vscode-python/issues/25824)
        self.sweep()
        self.assertFalse(can_build_rainbow_bridge(self.get_bundle())._instantiate(self.world)._evaluate(self.multiworld.state), f"Could trigger Rainbow Bridge but shouldn't have been able to.")
        required_items = list(map(lambda i: self.create_item(i), items))
        for size in range(1, len(required_items)):
            for invalid_combo in combinations(required_items, size):
                self.collect(invalid_combo)
                self.assertFalse(can_build_rainbow_bridge(self.get_bundle())._instantiate(self.world)._evaluate(self.multiworld.state), f"Should not be able to trigger Rainbow Bridge with only {invalid_combo}")
                self.remove(invalid_combo)
        self.collect(required_items)
        self.assertTrue(can_build_rainbow_bridge(self.get_bundle())._instantiate(self.world)._evaluate(self.multiworld.state), f"Wasn't able to trigger Rainbow Bridge, but should have been able to.")
        
        
    def require_some_rainbow(self, items: list[Items | Events], required_amount: int) -> None:
        # ideally we run these as subtests, but those are currently broken 
        # and report as Success if any subtest succeeds
        # (https://github.com/microsoft/vscode-python/issues/25824)
        self.sweep()
        self.assertFalse(can_build_rainbow_bridge(self.get_bundle())._instantiate(self.world)._evaluate(self.multiworld.state), f"Could trigger Rainbow Bridge but shouldn't have been able to.")
        required_items = list(map(lambda i: self.create_item(i), items))
        for size in range(1, len(required_items)):
            for invalid_combo in combinations(required_items, size):
                self.collect(invalid_combo)
                if required_amount <= len(invalid_combo) and not (Items.RG_GREG_RUPEE in invalid_combo and self.options["rainbow_bridge_greg_modifier"] != RainbowBridgeGregModifier.option_reward):
                    self.assertTrue(can_build_rainbow_bridge(self.get_bundle())._instantiate(self.world)._evaluate(self.multiworld.state), f"Wasn't able to trigger Rainbow Bridge, but should have been able to with count {required_amount}, {invalid_combo}")
                else:
                    self.assertFalse(can_build_rainbow_bridge(self.get_bundle())._instantiate(self.world)._evaluate(self.multiworld.state), f"Should not be able to trigger Rainbow Bridge with only {invalid_combo}. Required amount:{required_amount}")

                self.remove(invalid_combo)
        self.collect(required_items)
        self.assertTrue(can_build_rainbow_bridge(self.get_bundle())._instantiate(self.world)._evaluate(self.multiworld.state), f"Wasn't able to trigger Rainbow Bridge, but should have been able to.")

# Greg Specific
class TestCanTriggerRainbowTestGreg(RainbowBase):
    """
    Test can_build_rainbow_bridge greg
    """
    options = {"rainbow_bridge": RainbowBridge.option_greg}

    def test_greg_solo_reward(self):
        self.require_all_rainbow([Items.RG_GREG_RUPEE])

class TestCanTriggerRainbowTestGregSoloReward(RainbowBase):
    """
    Test can_build_rainbow_bridge greg solo reward
    """
    options = {"rainbow_bridge": RainbowBridge.option_stones, 
               "rainbow_bridge_stones_required": 1,
               "rainbow_bridge_greg_modifier": RainbowBridgeGregModifier.option_reward}

    def test_greg_solo_reward(self):
        self.require_all_rainbow([Items.RG_GREG_RUPEE])

class TestCanTriggerRwinbowGregSoloNonReward(RainbowBase):
    """
    Test can_build_rainbow_bridge stones greg solo non reward
    """
    options = {"rainbow_bridge": RainbowBridge.option_stones, 
               "rainbow_bridge_stones_required": 1,
               "rainbow_bridge_greg_modifier": RainbowBridgeGregModifier.option_off}

    def test_stones_greg_solo_nonreward(self):
        self.assertFalse(can_build_rainbow_bridge(self.get_bundle())._instantiate(self.world)._evaluate(self.multiworld.state), f"Could trigger Rainbow Bridge but shouldn't have been able to.")
        self.collect(self.create_item(Items.RG_GREG_RUPEE))
        self.assertFalse(can_build_rainbow_bridge(self.get_bundle())._instantiate(self.world)._evaluate(self.multiworld.state), f"Could trigger Rainbow Bridge but shouldn't have been able to.")


# Vanilla
class TestCanTriggerRainbowVanilla(RainbowBase):
    """
    Test can_build_rainbow_bridge vanilla
    """
    options = {"rainbow_bridge": RainbowBridge.option_vanilla,
               "door_of_time": RSK_DOOR_OF_TIME.option_closed, 
               "start_with_links_pocket": StartWithLinksPocket.option_nothing,
               "shuffle_dungeon_rewards": ShuffleDungeonRewards.option_anywhere,}

    def test_vanilla_setting(self):
        self.require_all_rainbow([Items.RG_SHADOW_MEDALLION, Items.RG_SPIRIT_MEDALLION, 
                                  Items.RG_LIGHT_ARROWS, Items.RG_PROGRESSIVE_BOW, Items.RG_PROGRESSIVE_MAGIC_METER])

class TestCanTriggerRainbowAlwaysOpen(RainbowBase):
    """
    Test can_build_rainbow_bridge always open
    """
    options = {"rainbow_bridge": RainbowBridge.option_always_open,
               "door_of_time": RSK_DOOR_OF_TIME.option_closed, 
               "start_with_links_pocket": StartWithLinksPocket.option_nothing,
               "shuffle_dungeon_rewards": ShuffleDungeonRewards.option_anywhere,}

    def test_always_setting(self):
        self.assertTrue(can_build_rainbow_bridge(self.get_bundle())._instantiate(self.world)._evaluate(self.multiworld.state), f"Wasn't able to trigger Rainbow Bridge, but should have been able to.")

# Stones
class TestCanTriggerRainbowStonesAll(RainbowBase):
    """
    Test can_build_rainbow_bridge all stones
    """
    options = {"rainbow_bridge": RainbowBridge.option_stones, 
               "door_of_time": RSK_DOOR_OF_TIME.option_closed, 
               "start_with_links_pocket": StartWithLinksPocket.option_nothing,
               "shuffle_dungeon_rewards": ShuffleDungeonRewards.option_anywhere,
               "rainbow_bridge_stones_required": 3}

    def test_stones_all(self):
        self.require_all_rainbow([Items.RG_KOKIRI_EMERALD, Items.RG_GORON_RUBY, Items.RG_ZORA_SAPPHIRE])

class TestCanTriggerRainbowStonesFew(RainbowBase):
    """
    Test can_build_rainbow_bridge a few stones
    """
    options = {"rainbow_bridge": RainbowBridge.option_stones, 
               "door_of_time": RSK_DOOR_OF_TIME.option_closed, 
               "start_with_links_pocket": StartWithLinksPocket.option_nothing,
               "shuffle_dungeon_rewards": ShuffleDungeonRewards.option_anywhere,
               "rainbow_bridge_stones_required": 2}

    def test_stones_few(self):
        self.require_some_rainbow([Items.RG_KOKIRI_EMERALD, Items.RG_GORON_RUBY, Items.RG_ZORA_SAPPHIRE], 
                               self.options["rainbow_bridge_stones_required"])

class TestCanTriggerRainbowStonesGregReward(RainbowBase):
    """
    Test can_build_rainbow_bridge stones greg reward
    """
    options = {"rainbow_bridge": RainbowBridge.option_stones, 
                "door_of_time": RSK_DOOR_OF_TIME.option_closed, 
               "start_with_links_pocket": StartWithLinksPocket.option_nothing,
               "shuffle_dungeon_rewards": ShuffleDungeonRewards.option_anywhere,
               # Needs to be updated when Greg Reward fixes get merged
               "rainbow_bridge_stones_required": 3,
               "rainbow_bridge_greg_modifier": RainbowBridgeGregModifier.option_reward}

    def test_stones_greg_all(self):
        # Needs to be updated when Greg Reward fixes get merged
        self.require_some_rainbow([Items.RG_KOKIRI_EMERALD, Items.RG_GORON_RUBY, Items.RG_ZORA_SAPPHIRE, 
                                Items.RG_GREG_RUPEE], self.options["rainbow_bridge_stones_required"])

# Medallions
class TestCanTriggerRainbowMedallionsAll(RainbowBase):
    """
    Test can_build_rainbow_bridge all medallions
    """
    options = {"rainbow_bridge": RainbowBridge.option_medallions, 
               "rainbow_bridge_medallions_required": 6, 
               "door_of_time": RSK_DOOR_OF_TIME.option_closed, 
               "start_with_links_pocket": StartWithLinksPocket.option_nothing,
               "shuffle_dungeon_rewards": ShuffleDungeonRewards.option_anywhere}

    def test_medallions_all(self):
        self.require_all_rainbow([Items.RG_FOREST_MEDALLION, Items.RG_FIRE_MEDALLION, Items.RG_WATER_MEDALLION, 
                               Items.RG_SPIRIT_MEDALLION, Items.RG_SHADOW_MEDALLION, Items.RG_LIGHT_MEDALLION])

class TestCanTriggerRainbowMedallionsFew(RainbowBase):
    """
    Test can_build_rainbow_bridge a few medallions
    """
    options = {"rainbow_bridge": RainbowBridge.option_medallions, 
               "rainbow_bridge_medallions_required": 5,
               "door_of_time": RSK_DOOR_OF_TIME.option_closed, 
               "start_with_links_pocket": StartWithLinksPocket.option_nothing,
               "shuffle_dungeon_rewards": ShuffleDungeonRewards.option_anywhere,}

    def test_medallions_few(self):
        self.require_some_rainbow([Items.RG_FOREST_MEDALLION, Items.RG_FIRE_MEDALLION, Items.RG_WATER_MEDALLION, 
                               Items.RG_SPIRIT_MEDALLION, Items.RG_SHADOW_MEDALLION, Items.RG_LIGHT_MEDALLION], self.options["rainbow_bridge_medallions_required"])

class TestCanTriggerRainbowMedallionsGregReward(RainbowBase):
    """
    Test can_build_rainbow_bridge medallions greg reward
    """
    options = {"rainbow_bridge": RainbowBridge.option_medallions, 
               # Needs to be updated when Greg Reward fixes get merged
               "rainbow_bridge_medallions_required": 6,
               "rainbow_bridge_greg_modifier": RainbowBridgeGregModifier.option_reward,
               "door_of_time": RSK_DOOR_OF_TIME.option_closed, 
               "start_with_links_pocket": StartWithLinksPocket.option_nothing,
               "shuffle_dungeon_rewards": ShuffleDungeonRewards.option_anywhere,}

    def test_medallions_greg_all(self):
        # Needs to be updated when Greg Reward fixes get merged
        self.require_some_rainbow([Items.RG_FOREST_MEDALLION, Items.RG_FIRE_MEDALLION, Items.RG_WATER_MEDALLION, 
                               Items.RG_SPIRIT_MEDALLION, Items.RG_SHADOW_MEDALLION, Items.RG_LIGHT_MEDALLION,
                                Items.RG_GREG_RUPEE], self.options["rainbow_bridge_medallions_required"])

# Dungeon Rewards
class TestCanTriggerRainbowDungeonRewardsAll(RainbowBase):
    """
    Test can_build_rainbow_bridge all dungeonrewards
    """
    options = {"rainbow_bridge": RainbowBridge.option_dungeon_rewards, 
               "door_of_time": RSK_DOOR_OF_TIME.option_closed, 
               "start_with_links_pocket": StartWithLinksPocket.option_nothing,
               "shuffle_dungeon_rewards": ShuffleDungeonRewards.option_anywhere,
               "rainbow_bridge_dungeon_rewards_required": 9}

    def test_dungeon_rewards_all(self):
        self.require_all_rainbow([Items.RG_KOKIRI_EMERALD, Items.RG_GORON_RUBY, Items.RG_ZORA_SAPPHIRE,
                                Items.RG_FOREST_MEDALLION, Items.RG_FIRE_MEDALLION, Items.RG_WATER_MEDALLION, 
                                Items.RG_SPIRIT_MEDALLION, Items.RG_SHADOW_MEDALLION, Items.RG_LIGHT_MEDALLION])

class TestCanTriggerRainbowDungeonRewardsFew(RainbowBase):
    """
    Test can_build_rainbow_bridge a few dungeonrewards
    """
    options = {"rainbow_bridge": RainbowBridge.option_dungeon_rewards, 
               "door_of_time": RSK_DOOR_OF_TIME.option_closed, 
               "start_with_links_pocket": StartWithLinksPocket.option_nothing,
               "shuffle_dungeon_rewards": ShuffleDungeonRewards.option_anywhere,
               "rainbow_bridge_dungeon_rewards_required": 8}

    def test_dungeon_rewards_few(self):
        self.require_some_rainbow([Items.RG_KOKIRI_EMERALD, Items.RG_GORON_RUBY, Items.RG_ZORA_SAPPHIRE,
                                Items.RG_FOREST_MEDALLION, Items.RG_FIRE_MEDALLION, Items.RG_WATER_MEDALLION, 
                                Items.RG_SPIRIT_MEDALLION, Items.RG_SHADOW_MEDALLION, Items.RG_LIGHT_MEDALLION], 
                               self.options["rainbow_bridge_dungeon_rewards_required"])

class TestCanTriggerRainbowDungeonRewardsGregReward(RainbowBase):
    """
    Test can_build_rainbow_bridge dungeonrewards greg reward
    """
    options = {"rainbow_bridge": RainbowBridge.option_dungeon_rewards, 
                "door_of_time": RSK_DOOR_OF_TIME.option_closed, 
               "start_with_links_pocket": StartWithLinksPocket.option_nothing,
               "shuffle_dungeon_rewards": ShuffleDungeonRewards.option_anywhere,
               # Needs to be updated when Greg Reward fixes get merged
               "rainbow_bridge_dungeon_rewards_required": 9,
               "rainbow_bridge_greg_modifier": RainbowBridgeGregModifier.option_reward}

    def test_dungeon_rewards_greg_all(self):
        # Needs to be updated when Greg Reward fixes get merged
        self.require_some_rainbow([Items.RG_KOKIRI_EMERALD, Items.RG_GORON_RUBY, Items.RG_ZORA_SAPPHIRE,
                                Items.RG_FOREST_MEDALLION, Items.RG_FIRE_MEDALLION, Items.RG_WATER_MEDALLION, 
                                Items.RG_SPIRIT_MEDALLION, Items.RG_SHADOW_MEDALLION, Items.RG_LIGHT_MEDALLION, 
                                Items.RG_GREG_RUPEE], self.options["rainbow_bridge_dungeon_rewards_required"])

# Dungeons
class TestCanTriggerRainbowDungeonsAll(RainbowBase):
    """
    Test can_build_rainbow_bridge all dungeons
    """
    options = {"rainbow_bridge": RainbowBridge.option_dungeons, 
               "door_of_time": RSK_DOOR_OF_TIME.option_closed, 
               "start_with_links_pocket": StartWithLinksPocket.option_nothing,
               "shuffle_dungeon_rewards": ShuffleDungeonRewards.option_anywhere,
               "rainbow_bridge_dungeons_required": 8}

    def test_dungeons_all(self):
        self.require_all_rainbow([Events.LOGIC_DEKU_TREE_CLEAR, Events.LOGIC_DODONGOS_CAVERN_CLEAR, Events.LOGIC_JABU_JABUS_BELLY_CLEAR,
                               Events.LOGIC_FOREST_TEMPLE_CLEAR, Events.LOGIC_FIRE_TEMPLE_CLEAR, Events.LOGIC_WATER_TEMPLE_CLEAR,
                               Events.LOGIC_SHADOW_TEMPLE_CLEAR, Events.LOGIC_SPIRIT_TEMPLE_CLEAR])

class TestCanTriggerRainbowDungeonsFew(RainbowBase):
    """
    Test can_build_rainbow_bridge a few dungeons
    """
    options = {"rainbow_bridge": RainbowBridge.option_dungeons, 
               "door_of_time": RSK_DOOR_OF_TIME.option_closed, 
               "start_with_links_pocket": StartWithLinksPocket.option_nothing,
               "shuffle_dungeon_rewards": ShuffleDungeonRewards.option_anywhere,
               "rainbow_bridge_dungeons_required": 7}

    def test_dungeons_few(self):
        self.require_some_rainbow([Events.LOGIC_DEKU_TREE_CLEAR, Events.LOGIC_DODONGOS_CAVERN_CLEAR, Events.LOGIC_JABU_JABUS_BELLY_CLEAR,
                               Events.LOGIC_FOREST_TEMPLE_CLEAR, Events.LOGIC_FIRE_TEMPLE_CLEAR, Events.LOGIC_WATER_TEMPLE_CLEAR,
                               Events.LOGIC_SHADOW_TEMPLE_CLEAR, Events.LOGIC_SPIRIT_TEMPLE_CLEAR], 
                               self.options["rainbow_bridge_dungeons_required"])

class TestCanTriggerRainbowDungeonsGregReward(RainbowBase):
    """
    Test can_build_rainbow_bridge dungeons greg reward
    """
    options = {"rainbow_bridge": RainbowBridge.option_dungeons, 
                "door_of_time": RSK_DOOR_OF_TIME.option_closed, 
               "start_with_links_pocket": StartWithLinksPocket.option_nothing,
               "shuffle_dungeon_rewards": ShuffleDungeonRewards.option_anywhere,
               # Needs to be updated when Greg Reward fixes get merged
               "rainbow_bridge_dungeons_required": 8,
               "rainbow_bridge_greg_modifier": RainbowBridgeGregModifier.option_reward}

    def test_dungeons_greg_all(self):
        # Needs to be updated when Greg Reward fixes get merged
        self.require_some_rainbow([Events.LOGIC_DEKU_TREE_CLEAR, Events.LOGIC_DODONGOS_CAVERN_CLEAR, Events.LOGIC_JABU_JABUS_BELLY_CLEAR,
                                Events.LOGIC_FOREST_TEMPLE_CLEAR, Events.LOGIC_FIRE_TEMPLE_CLEAR, Events.LOGIC_WATER_TEMPLE_CLEAR,
                                Events.LOGIC_SHADOW_TEMPLE_CLEAR, Events.LOGIC_SPIRIT_TEMPLE_CLEAR, 
                                Items.RG_GREG_RUPEE], self.options["rainbow_bridge_dungeons_required"])

# Tokens
class TestCanTriggerRainbowTokensAll(RainbowBase):
    """
    Test can_build_rainbow_bridge all tokens
    """
    options = {"rainbow_bridge": RainbowBridge.option_tokens,
               "shuffle_skull_tokens": ShuffleTokens.option_all, 
               "rainbow_bridge_skull_tokens_required": 100}

    def test_tokens_all(self):
        self.assertFalse(can_build_rainbow_bridge(self.get_bundle())._instantiate(self.world)._evaluate(self.multiworld.state), f"Could trigger Rainbow Bridge but shouldn't have been able to.")
        self.collect(self.create_item(Items.RG_GOLD_SKULLTULA_TOKEN) for _ in range(99))
        self.assertFalse(can_build_rainbow_bridge(self.get_bundle())._instantiate(self.world)._evaluate(self.multiworld.state), f"Could trigger Rainbow Bridge but shouldn't have been able to.")
        self.collect(self.create_item(Items.RG_GOLD_SKULLTULA_TOKEN))
        self.assertTrue(can_build_rainbow_bridge(self.get_bundle())._instantiate(self.world)._evaluate(self.multiworld.state), f"Couldn't trigger Rainbow Bridge but should have been able to.")


# Scarecrow Song
class ScarecrowBase(SohTestBase):
    __Test__ = False

    def require_all_scarecrow(self, items: list[Items | Events]) -> None:
        # ideally we run these as subtests, but those are currently broken 
        # and report as Success if any subtest succeeds
        # (https://github.com/microsoft/vscode-python/issues/25824)
        self.sweep()
        self.assertFalse(scarecrows_song(self.get_bundle())._instantiate(self.world)._evaluate(self.multiworld.state), f"Could use Scarecrows Song but shouldn't have been able to.")
        required_items = list(map(lambda i: self.create_item(i), items))
        for size in range(1, len(required_items)):
            for invalid_combo in combinations(required_items, size):
                self.collect(invalid_combo)
                self.assertFalse(scarecrows_song(self.get_bundle())._instantiate(self.world)._evaluate(self.multiworld.state), f"Should not be able to use Scarecrows Song with only {invalid_combo}")
                self.remove(invalid_combo)
        self.collect(required_items)
        self.assertTrue(scarecrows_song(self.get_bundle())._instantiate(self.world)._evaluate(self.multiworld.state), f"Wasn't able to use Scarecrows Song, but should have been able to.")

    def scarecrow_button_check(self, items: list[Items | Events]) -> None:
        # ideally we run these as subtests, but those are currently broken 
        # and report as Success if any subtest succeeds
        # (https://github.com/microsoft/vscode-python/issues/25824)
        self.sweep()
        self.assertFalse(scarecrows_song(self.get_bundle())._instantiate(self.world)._evaluate(self.multiworld.state), f"Could use Scarecrows Song but shouldn't have been able to.")
        required_items = list(map(lambda i: self.create_item(i), items))
        for size in range(1, len(required_items)):
            for invalid_combo in combinations(required_items, size):
                self.collect(invalid_combo)
                if len(invalid_combo) < 2:
                    self.assertFalse(scarecrows_song(self.get_bundle())._instantiate(self.world)._evaluate(self.multiworld.state), f"Should not be able to use Scarecrows Song with only {invalid_combo}")
                else:
                    self.assertTrue(scarecrows_song(self.get_bundle())._instantiate(self.world)._evaluate(self.multiworld.state), f"Wasn't able to use Scarecrows Song, but should have been able to.")
                self.remove(invalid_combo)
        self.collect(required_items)
        self.assertTrue(scarecrows_song(self.get_bundle())._instantiate(self.world)._evaluate(self.multiworld.state), f"Wasn't able to use Scarecrows Song, but should have been able to.")

class TestScarecrowsSongNoSkip(ScarecrowBase):
    """
    Test if Scarecrows Song function works with no skip
    """
    options = {"skip_scarecrows_song": False, "shuffle_ocarinas": True, "shuffle_ocarina_buttons": True}
    def test_scarecrows_song(self):
        self.require_all_scarecrow([Events.LOGIC_CHILD_SCARECROW, Events.LOGIC_ADULT_SCARECROW])

class TestScarecrowsSongSkip(ScarecrowBase):
    """
    Test if Scarecrows Song function works with skip enabled
    """
    options = {"skip_scarecrows_song": True, "shuffle_ocarinas": True, "shuffle_ocarina_buttons": True}
    def test_scarecrows_song_skip(self):
        self.assertFalse(scarecrows_song(self.get_bundle())._instantiate(self.world)._evaluate(self.multiworld.state), f"Could use Scarecrows Song but shouldn't have been able to with nothing.")

        self.collect(self.create_item(Items.RG_PROGRESSIVE_OCARINA))

        self.assertFalse(scarecrows_song(self.get_bundle())._instantiate(self.world)._evaluate(self.multiworld.state), f"Could use Scarecrows Song but shouldn't have been able to with just ocarina.")

        self.scarecrow_button_check([Items.RG_OCARINA_A_BUTTON, Items.RG_OCARINA_C_DOWN_BUTTON, Items.RG_OCARINA_C_LEFT_BUTTON, Items.RG_OCARINA_C_RIGHT_BUTTON, Items.RG_OCARINA_C_UP_BUTTON])

# Bombchu Drops
class BombchuBase(SohTestBase):
    __Test__ = False

    def require_some_bomchu(self, items: list[Items | Events], required_amount: int) -> None:
        # ideally we run these as subtests, but those are currently broken 
        # and report as Success if any subtest succeeds
        # (https://github.com/microsoft/vscode-python/issues/25824)
        self.sweep()
        self.assertFalse(bombchu_refill(self.get_bundle())._instantiate(self.world)._evaluate(self.multiworld.state), f"Had bombchu drops but shouldn't have.")
        required_items = list(map(lambda i: self.create_item(i), items))
        for size in range(1, len(required_items)):
            for invalid_combo in combinations(required_items, size):
                self.collect(invalid_combo)
                self.assertTrue(bombchu_refill(self.get_bundle())._instantiate(self.world)._evaluate(self.multiworld.state), f"Didn't have bombchu drops, but should have with {required_amount}, {invalid_combo}")
                self.remove(invalid_combo)
        self.collect(required_items)
        self.assertTrue(bombchu_refill(self.get_bundle())._instantiate(self.world)._evaluate(self.multiworld.state), f"Didn't have bombchu drops, but should have.")

class TestBombchuNoDrops(BombchuBase):
    """
    Test if player can get bombchus if the drops setting is disabled.
    """
    options = {"bombchu_drops": False, "shuffle_childs_wallet": True}
    def test_bombchu_no_drops(self):
        self.require_some_bomchu([Items.RG_BUY_BOMBCHUS_10, Items.RG_BUY_BOMBCHUS_20, Events.LOGIC_COULD_PLAY_BOWLING, Events.LOGIC_CARPET_MERCHANT], 1)

class TestBombchuDropsOn(BombchuBase):
    """
    Test if player can get bombchus if the drops setting is enabled.
    """
    options = {"bombchu_drops": True, "shuffle_childs_wallet": True}
    def test_bombchu_drops_on(self):
        self.assertTrue(bombchu_refill(self.get_bundle())._instantiate(self.world)._evaluate(self.multiworld.state), f"Had bombchu drops setting enabled, but didn't have drops.")

# Trade Quest Step
TRADE_CHAIN = [Items.RG_POCKET_EGG, Items.RG_COJIRO, Items.RG_ODD_MUSHROOM, Items.RG_ODD_POTION, Items.RG_POACHERS_SAW,
               Items.RG_BROKEN_SWORD, Items.RG_PRESCRIPTION, Items.RG_EYEDROPS, Items.RG_CLAIM_CHECK]

class TestTradeQuestStepShuffleDisabled(SohTestBase):
    """
    Test Trade Quest Step Helper when adult trade quest items shuffle setting is disabled.

    Unshuffled trade items (everything but the Claim Check) aren't in the pool and has_item treats them as
    held (LogicHelpers.has_item), so every step before the Claim Check is satisfied from the start; the
    Claim Check step needs the Claim Check itself.
    """
    options = {"shuffle_adult_trade_items": False}

    def at_step(self, step: Items) -> bool:
        return trade_quest_step(self.get_bundle(), step)._instantiate(self.world)._evaluate(self.multiworld.state)

    def test_trade_quest_steps_before_claim_check(self):
        for step in TRADE_CHAIN[:-1]:
            self.assertTrue(self.at_step(step), f"Wasn't at {step} step, but unshuffled trade items count as held.")

    def test_trade_quest_step_claim_check(self):
        self.assertFalse(self.at_step(Items.RG_CLAIM_CHECK), f"Was at claim check step, but shouldn't have been.")
        self.collect(self.create_item(Items.RG_CLAIM_CHECK))
        self.assertTrue(self.at_step(Items.RG_CLAIM_CHECK), f"Should have been at claim check step, but wasn't.")

    def test_trade_quest_step_other(self):
        self.assertFalse(self.at_step(Items.RG_TRIFORCE_PIECE), f"An item that wasn't supposed to be checked was and returned true.")

class TestTradeQuestStepShuffleEnabled(SohTestBase):
    """
    Test Trade Quest Step Helper when adult trade quest items shuffle setting is enabled
    """
    options = {"shuffle_adult_trade_items": True}

    def test_trade_quest_steps_never(self):
        for step in TRADE_CHAIN:
            self.collect(self.create_item(step))
        for step in TRADE_CHAIN + [Items.RG_TRIFORCE_PIECE]:
            self.assertFalse(trade_quest_step(self.get_bundle(), step)._instantiate(self.world)._evaluate(self.multiworld.state), f"Was at {step} step, but trade steps never apply with shuffle on.")
