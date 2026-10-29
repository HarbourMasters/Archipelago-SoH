from .bases import SohTestBase
from ..Enums import Items, Locations


class TestTime(SohTestBase):
    options = {"starting_age": "adult", "shuffle_grass": "all", "shuffle_kokiri_sword": 1}

    # test that you cannot cut the market grass if you do not have a grass cutter for child Link
    def test_wrong_age_grass(self):
        self.collect_all_but([Items.RG_GORONS_BRACELET, Items.RG_PROGRESSIVE_STRENGTH, Items.RG_BOOMERANG, Items.RG_KOKIRI_SWORD,
                              Items.RG_BOMB_BAG, Items.RG_PROGRESSIVE_BOMB_BAG, Items.RG_PROGRESSIVE_BOMBCHU_BAG])
        self.assertFalse(self.can_reach_location(Locations.RC_MARKET_GRASS_1),
                         "Can access child-exclusive grass without an item that child can use to break it.")
        self.collect_by_name([Items.RG_PROGRESSIVE_STRENGTH])
        self.assertTrue(self.can_reach_location(Locations.RC_MARKET_GRASS_1))
