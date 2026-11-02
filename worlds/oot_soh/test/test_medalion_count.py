from .bases import SohTestBase
from ..Enums import Items, Regions, Events
from .. import LogicHelpers
from .. import Options
from ..Regions import dungeon_reward_item_mapping
import itertools

class TestStartWithoutRewardShuffleAnywhere(SohTestBase):
    options = {"rainbow_bridge": Options.RainbowBridge.option_dungeon_rewards,
               "rainbow_bridge_dungeon_rewards_required": 9,
               "shuffle_dungeon_rewards": Options.ShuffleDungeonRewards.option_anywhere,
               "start_with_links_pocket": Options.StartWithLinksPocket.option_nothing}
    def test_count(self):
        dungeon_rewards = [str(val) for val in dungeon_reward_item_mapping.values()]
        self.collect_by_name(dungeon_rewards)
        for reward in dungeon_rewards:
            count = 0
            for item in self.multiworld.get_items():
                if item.name == reward:
                    count += 1
            self.assertEqual(count, 1, f"We should have only 1 {reward} in the pool")

class TestStartWithRewardShuffleAnywhere(SohTestBase):
    options = {"rainbow_bridge": Options.RainbowBridge.option_dungeon_rewards,
               "rainbow_bridge_dungeon_rewards_required": 9,
               "shuffle_dungeon_rewards": Options.ShuffleDungeonRewards.option_anywhere,
               "start_with_links_pocket": Options.StartWithLinksPocket.option_dungeon_reward}
    def test_count(self):
        dungeon_rewards = [str(val) for val in dungeon_reward_item_mapping.values()]
        self.collect_by_name(dungeon_rewards)
        for reward in dungeon_rewards:
            count = 0
            for item in self.multiworld.get_items():
                if item.name == reward:
                    count += 1
            self.assertEqual(count, 1, f"We should have only 1 {reward} in the pool")

class TestStartWithRewardShuffleAnyDungeon(SohTestBase):
    options = {"rainbow_bridge": Options.RainbowBridge.option_dungeon_rewards,
               "rainbow_bridge_dungeon_rewards_required": 9,
               "shuffle_dungeon_rewards": Options.ShuffleDungeonRewards.option_any_dungeon,
               "start_with_links_pocket": Options.StartWithLinksPocket.option_dungeon_reward}
    def test_count(self):
        dungeon_rewards = [str(val) for val in dungeon_reward_item_mapping.values()]
        self.collect_by_name(dungeon_rewards)
        for reward in dungeon_rewards:
            count = 0
            for item in self.multiworld.get_items():
                if item.name == reward:
                    count += 1
            self.assertEqual(count, 1, f"We should have only 1 {reward} in the pool")

class TestStartWithRewardShuffleOverworld(SohTestBase):
    options = {"rainbow_bridge": Options.RainbowBridge.option_dungeon_rewards,
               "rainbow_bridge_dungeon_rewards_required": 9,
               "shuffle_dungeon_rewards": Options.ShuffleDungeonRewards.option_overworld,
               "start_with_links_pocket": Options.StartWithLinksPocket.option_dungeon_reward}
    def test_count(self):
        dungeon_rewards = [str(val) for val in dungeon_reward_item_mapping.values()]
        self.collect_by_name(dungeon_rewards)
        for reward in dungeon_rewards:
            count = 0
            for item in self.multiworld.get_items():
                if item.name == reward:
                    count += 1
            self.assertEqual(count, 1, f"We should have only 1 {reward} in the pool")


class TestStartWithRewardShuffleEndDungeon(SohTestBase):
    options = {"rainbow_bridge": Options.RainbowBridge.option_dungeon_rewards,
               "rainbow_bridge_dungeon_rewards_required": 9,
               "shuffle_dungeon_rewards": Options.ShuffleDungeonRewards.option_end_of_dungeons,
               "start_with_links_pocket": Options.StartWithLinksPocket.option_dungeon_reward}
    def test_count(self):
        dungeon_rewards = [str(val) for val in dungeon_reward_item_mapping.values()]
        self.collect_by_name(dungeon_rewards)
        for reward in dungeon_rewards:
            count = 0
            for item in self.multiworld.get_items():
                if item.name == reward:
                    count += 1
            self.assertEqual(count, 1, f"We should have only 1 {reward} in the pool")
