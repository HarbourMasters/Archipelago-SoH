import random
import unittest

from ..MasterQuest import MQ_DUNGEONS, MQ_SCENES, mq_scenes, resolve_mq_dungeons
from ..Options import (BottomOfTheWellQuest, DekuTreeQuest, DodongosCavernQuest,
                       GanonsCastleQuest, IceCavernQuest, MQDungeonCount, MQDungeons,
                       SpiritTempleQuest)


class StubOptions:
    def __init__(self, mode, count=0, **quests):
        self.mq_dungeons = MQDungeons(mode)
        self.mq_dungeon_count = MQDungeonCount(count)
        for field, _scene in MQ_DUNGEONS.values():
            setattr(self, field, DekuTreeQuest(DekuTreeQuest.option_random_quest))
        for field, value in quests.items():
            setattr(self, field, DekuTreeQuest(value))


class StubWorld:
    def __init__(self, options, seed=0):
        self.options = options
        self.random = random.Random(seed)


def resolve(mode, count=0, seed=0, **quests):
    return resolve_mq_dungeons(StubWorld(StubOptions(mode, count, **quests), seed))


class TestResolveMQDungeons(unittest.TestCase):
    def test_none_is_all_vanilla(self):
        # Even a dungeon explicitly set to Master Quest stays vanilla: None means none.
        self.assertEqual(
            resolve(MQDungeons.option_none,
                    deku_tree_quest=DekuTreeQuest.option_master_quest),
            [])

    def test_set_number_picks_exactly_that_many(self):
        for count in (0, 1, 5, 12):
            self.assertEqual(len(resolve(MQDungeons.option_set_number, count)), count,
                             f"count={count}")

    def test_forced_dungeons_count_towards_the_total(self):
        # Ship: "the dungeons chosen to be Master Quest here will count towards that total".
        chosen = resolve(MQDungeons.option_set_number, 3,
                         deku_tree_quest=DekuTreeQuest.option_master_quest,
                         ice_cavern_quest=IceCavernQuest.option_master_quest)
        self.assertEqual(len(chosen), 3)
        self.assertIn("Deku Tree", chosen)
        self.assertIn("Ice Cavern", chosen)

    def test_vanilla_dungeons_are_never_chosen(self):
        vanilla = {field: DekuTreeQuest.option_vanilla for field, _ in MQ_DUNGEONS.values()}
        vanilla["deku_tree_quest"] = DekuTreeQuest.option_random_quest
        chosen = resolve(MQDungeons.option_set_number, 12, **vanilla)
        # Only one dungeon was available, so Ship's "you will have fewer MQ Dungeons than the
        # number you set" applies rather than an error.
        self.assertEqual(chosen, ["Deku Tree"])

    def test_count_above_available_yields_fewer(self):
        chosen = resolve(MQDungeons.option_set_number, 12,
                         **{field: DekuTreeQuest.option_vanilla
                            for field, _ in MQ_DUNGEONS.values()})
        self.assertEqual(chosen, [])

    def test_selection_only_keeps_forced_and_rolls_the_rest(self):
        chosen = resolve(MQDungeons.option_selection_only,
                         deku_tree_quest=DekuTreeQuest.option_master_quest,
                         ice_cavern_quest=IceCavernQuest.option_vanilla)
        self.assertIn("Deku Tree", chosen)
        self.assertNotIn("Ice Cavern", chosen)

    def test_set_number_is_exact_only_because_random_quest_defers(self):
        deferred = {field: DekuTreeQuest.option_random_quest for field, _ in MQ_DUNGEONS.values()}
        for seed in range(30):
            self.assertEqual(len(resolve(MQDungeons.option_set_number, 3, seed=seed, **deferred)), 3)

        # Pre-committing them instead makes the count unenforceable -- not an error, just no
        # longer the number the player chose.
        committed = dict(deferred)
        for i, field in enumerate(f for f, _ in MQ_DUNGEONS.values()):
            committed[field] = (DekuTreeQuest.option_master_quest if i % 2
                                else DekuTreeQuest.option_vanilla)
        self.assertGreater(len(resolve(MQDungeons.option_set_number, 3, **committed)), 3)

    def test_selection_only_ignores_the_count(self):
        # The count slider belongs to Set Number; under Selection Only each dungeon is its own
        # roll, which is what makes the total a bell curve rather than a chosen number.
        everything_forced = {field: DekuTreeQuest.option_master_quest
                             for field, _ in MQ_DUNGEONS.values()}
        chosen = resolve(MQDungeons.option_selection_only, 1, **everything_forced)
        self.assertEqual(len(chosen), len(MQ_DUNGEONS))

    def test_random_number_stays_in_range(self):
        for seed in range(25):
            self.assertLessEqual(len(resolve(MQDungeons.option_random_number, seed=seed)),
                                 len(MQ_DUNGEONS))

    def test_result_is_deterministic_for_a_seed(self):
        self.assertEqual(resolve(MQDungeons.option_set_number, 4, seed=7),
                         resolve(MQDungeons.option_set_number, 4, seed=7))

    def test_scenes_map_back(self):
        self.assertEqual(mq_scenes(["Deku Tree", "Ice Cavern"]),
                         frozenset({"SCENE_DEKU_TREE", "SCENE_ICE_CAVERN"}))
        self.assertTrue(mq_scenes(list(MQ_DUNGEONS)) == MQ_SCENES)


class TestRegionGating(unittest.TestCase):
    """A region belongs to a quest variant; only the rolled one is built."""

    def setUp(self):
        from ..LogicHelpers import REGION_SCENE, Regions, region_is_active
        self.REGION_SCENE, self.Regions, self.active = REGION_SCENE, Regions, region_is_active

    @staticmethod
    def world(*dungeons):
        """region_is_active only reads world.mq_scenes."""
        return type("StubMQWorld", (), {"mq_scenes": mq_scenes(list(dungeons))})()

    def test_mq_regions_only_when_that_dungeon_is_mq(self):
        mq_region = self.Regions.RR_DEKU_TREE_MQ_1F
        van_region = self.Regions.RR_DEKU_TREE_LOBBY

        self.assertTrue(self.active(mq_region, self.world("Deku Tree")))
        self.assertFalse(self.active(van_region, self.world("Deku Tree")))

        self.assertFalse(self.active(mq_region, self.world()))
        self.assertTrue(self.active(van_region, self.world()))

    def test_other_dungeons_are_unaffected(self):
        # Ice Cavern being MQ says nothing about the Deku Tree.
        self.assertTrue(self.active(self.Regions.RR_DEKU_TREE_LOBBY, self.world("Ice Cavern")))

    def test_non_dungeon_regions_are_always_active(self):
        self.assertTrue(self.active(self.Regions.RR_KOKIRI_FOREST, self.world()))
        self.assertTrue(self.active(self.Regions.RR_KOKIRI_FOREST, self.world("Deku Tree")))

    def test_dungeon_comes_from_the_scene_not_the_name(self):
        # RR_GANONS_CASTLE_* regions sit in SCENE_INSIDE_GANONS_CASTLE, and it is the scene that
        # ties them to the "Ganon's Castle" dungeon option -- the same scene Ganon's Tower uses,
        # which is why the tower correctly follows the castle's quest rather than its own name.
        vanilla_only = self.Regions.RR_GANONS_CASTLE_DEKU_SCRUBS
        self.assertEqual(self.REGION_SCENE[vanilla_only], "SCENE_INSIDE_GANONS_CASTLE")
        self.assertTrue(self.active(vanilla_only, self.world()))
        self.assertFalse(self.active(vanilla_only, self.world("Ganon's Castle")))
        # Another dungeon being MQ must not disturb it.
        self.assertTrue(self.active(vanilla_only, self.world("Deku Tree")))

    def test_shared_regions_stay_active_in_both_quests(self):
        from ..LogicHelpers import REGION_QUEST
        entryway = self.Regions.RR_DEKU_TREE_ENTRYWAY
        self.assertEqual(REGION_QUEST[entryway], "")
        self.assertTrue(self.active(entryway, self.world()))
        self.assertTrue(self.active(entryway, self.world("Deku Tree")))

    def test_every_dungeon_region_is_reachable_in_exactly_one_configuration(self):
        """No region may be dropped by both quests, and every variant-specific scene must be a
        dungeon MasterQuest.py knows about -- otherwise it could never be switched on."""
        from ..LogicHelpers import REGION_QUEST
        vanilla, all_mq = self.world(), self.world(*MQ_DUNGEONS)
        orphans = [r.name for r in self.REGION_SCENE
                   if not self.active(r, vanilla) and not self.active(r, all_mq)]
        self.assertEqual(orphans, [], "regions no configuration can reach")

        variant_scenes = {self.REGION_SCENE[r] for r, q in REGION_QUEST.items() if q}
        self.assertTrue(variant_scenes <= MQ_SCENES,
                        f"quest-specific regions in unknown scenes: {variant_scenes - MQ_SCENES}")


if __name__ == "__main__":
    unittest.main()
