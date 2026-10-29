from .bases import SohTestBase
from ..Enums import Items
from ..enums_gen import Regions

class TestAllTrialsOpen(SohTestBase):
    options = {"starting_age": "adult",
               "rainbow_bridge": "always_open",
               "medallion_locked_trials": "false",
               "shuffle_dungeon_rewards": "anywhere",
               "start_with_links_pocket": "nothing"}
    def test_require_none(self):
        self.sweep()
        self.assertTrue(self.can_reach_region(Regions.RR_GANONS_CASTLE_ENTRYWAY), "The entryway should be accessible")
        self.assertTrue(self.can_reach_region(Regions.RR_GANONS_CASTLE_FOREST_TRIAL_WOLFOS_ROOM), "The Forest Trial should be accessible when medallion locked trials are disabled")
        self.assertTrue(self.can_reach_region(Regions.RR_GANONS_CASTLE_FIRE_TRIAL_FROM_OPEN), "The Fire Trial should be accessible when medallion locked trials are disabled")
        self.assertTrue(self.can_reach_region(Regions.RR_GANONS_CASTLE_WATER_TRIAL_BLUE_FIRE_ROOM), "The Water Trial should be accessible when medallion locked trials are disabled")
        self.assertTrue(self.can_reach_region(Regions.RR_GANONS_CASTLE_SHADOW_TRIAL_START), "The Shadow Trial should be accessible when medallion locked trials are disabled")
        self.assertTrue(self.can_reach_region(Regions.RR_GANONS_CASTLE_SPIRIT_TRIAL_BEAMOS_ROOM), "The Spirit Trial should be accessible when medallion locked trials are disabled")
        self.assertFalse(self.can_reach_region(Regions.RR_GANONS_CASTLE_LIGHT_TRIAL_CHESTS_ROOM), "The Light Trial should be not be accessible when medallion locked trials are disabled, until the gold gauntlets are obtained")
        self.collect([self.create_item(Items.RG_PROGRESSIVE_STRENGTH)] * 3)
        self.assertTrue(self.can_reach_region(Regions.RR_GANONS_CASTLE_LIGHT_TRIAL_CHESTS_ROOM), "The Light Trial should be not be accessible when medallion locked trials are disabled, until the gold gauntlets are obtained")

class TestAllTrialsClosed(SohTestBase):
    options = {"starting_age": "adult",
               "rainbow_bridge": "always_open",
               "medallion_locked_trials": "true",
               "shuffle_dungeon_rewards": "anywhere",
               "start_with_links_pocket": "nothing"}

    def require_specific(self, check: Items, area: Regions):
        all_medallions = [Items.RG_FOREST_MEDALLION,
                          Items.RG_FIRE_MEDALLION,
                          Items.RG_WATER_MEDALLION,
                          Items.RG_SPIRIT_MEDALLION,
                          Items.RG_SHADOW_MEDALLION,
                          Items.RG_LIGHT_MEDALLION]
        all_medallions.remove(check)
        other_medallions = list(map(lambda i: self.create_item(i), all_medallions))

        self.sweep()
        self.assertFalse(self.can_reach_region(area), "The trial should not be reachable without the coresponding medallion")
        self.collect(other_medallions)
        self.assertFalse(self.can_reach_region(area), "The trial should not be reachable with only the other medallions")
        self.collect(self.create_item(check))
        self.assertTrue(self.can_reach_region(area), "The trial should be reachable with the medallion")
        self.remove(other_medallions)
        self.assertTrue(self.can_reach_region(area), "The trial should remain reachable without the other medallion")

    def test_forest_trial(self):
        self.require_specific(Items.RG_FOREST_MEDALLION, Regions.RR_GANONS_CASTLE_FOREST_TRIAL_WOLFOS_ROOM)

    def test_fire_trial(self):
        self.require_specific(Items.RG_FIRE_MEDALLION, Regions.RR_GANONS_CASTLE_FIRE_TRIAL_FROM_OPEN)

    def test_water_trial(self):
        self.require_specific(Items.RG_WATER_MEDALLION, Regions.RR_GANONS_CASTLE_WATER_TRIAL_BLUE_FIRE_ROOM)

    def test_shadow_trial(self):
        self.require_specific(Items.RG_SHADOW_MEDALLION, Regions.RR_GANONS_CASTLE_SHADOW_TRIAL_START)

    def test_spirit_trial(self):
        self.require_specific(Items.RG_SPIRIT_MEDALLION, Regions.RR_GANONS_CASTLE_SPIRIT_TRIAL_BEAMOS_ROOM)

    def test_light_trial(self):
        self.collect([self.create_item(Items.RG_PROGRESSIVE_STRENGTH)] * 3)
        self.require_specific(Items.RG_LIGHT_MEDALLION, Regions.RR_GANONS_CASTLE_LIGHT_TRIAL_CHESTS_ROOM)
