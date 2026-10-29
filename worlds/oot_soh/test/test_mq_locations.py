from ..MasterQuest import MQ_DUNGEONS
from ..ship_data_gen import SHIP_LOCATIONS, CheckQuest, DUNGEON_SMALL_KEYS
from .bases import SohTestBase

ALL_MQ = {"mq_dungeons": "selection_only", **{field: "master_quest" for field, _ in MQ_DUNGEONS.values()}}


def quest_locations(test: SohTestBase, quest: CheckQuest) -> set[str]:
    names = {loc.name for loc in test.multiworld.get_locations(test.player)}
    return {str(loc) for loc, data in SHIP_LOCATIONS.items() if data.quest == quest} & names


class TestAllMasterQuest(SohTestBase):
    options = {**ALL_MQ, "small_key_shuffle": "anywhere"}

    def test_only_mq_dungeon_locations(self):
        self.assertFalse(quest_locations(self, CheckQuest.RCQUEST_VANILLA))
        self.assertTrue(quest_locations(self, CheckQuest.RCQUEST_MQ))

    def test_small_keys_follow_mq_counts(self):
        pool = [item.name for item in self.multiworld.itempool]
        for key, (dungeon, _, mq) in DUNGEON_SMALL_KEYS.items():
            self.assertEqual(pool.count(str(key)), mq, dungeon)


class TestAllVanilla(SohTestBase):
    options = {"mq_dungeons": "none", "small_key_shuffle": "anywhere"}

    def test_only_vanilla_dungeon_locations(self):
        self.assertFalse(quest_locations(self, CheckQuest.RCQUEST_MQ))

    def test_small_keys_follow_vanilla_counts(self):
        pool = [item.name for item in self.multiworld.itempool]
        for key, (dungeon, vanilla, _) in DUNGEON_SMALL_KEYS.items():
            self.assertEqual(pool.count(str(key)), vanilla, dungeon)


class TestMasterQuestVanillaKeys(SohTestBase):
    options = {**ALL_MQ, "small_key_shuffle": "vanilla"}

    def test_keys_placed_in_mq_key_locations(self):
        placed = [loc.item.name for loc in self.multiworld.get_locations(self.player)
                  if loc.item and loc.item.name.endswith("Small Key")]
        for key, (dungeon, _, mq) in DUNGEON_SMALL_KEYS.items():
            self.assertEqual(placed.count(str(key)), mq, dungeon)
