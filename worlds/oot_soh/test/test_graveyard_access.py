from .. import SohWorld
from ..Items import progressive_items, Items, Locations
from ..Enums import Regions
from .bases import SohTestBase
from BaseClasses import Item, ItemClassification


class TestCanReachGraveyardShieldChest(SohTestBase):
    options = {"door_of_time": 0}
    world: SohWorld

    def test_graveyard_shield_chest_no_day_control_means_glitched(self):
        """
        Checking if player can open the shield grave chest by just waiting until the sun sets
        """
        self.world.glitches_item_name = Items.GLITCHED
        # self.multiworld.push_precollected(Items.GLITCHED)
        self.world.push_precollected(self.world.create_item(Items.GLITCHED))
        self.multiworld.itempool.append(Item(Items.GLITCHED, ItemClassification.filler, None, 1))
        items = self.collect_by_name(Items.GLITCHED)
        self.assertTrue(len(items) == 1)

        self.multiworld.state.update_reachable_regions(1)        
        self.assertTrue(self.get_item_by_name(Items.GLITCHED).name == 'Glitched Item', f"Glitched Item was found.")
        self.assertTrue(self.can_reach_region(Regions.THE_GRAVEYARD), f"The Graveyard should be accessible.")
        self.assertTrue(self.can_reach_location(Locations.GRAVEYARD_SHIELD_GRAVE_CHEST),
                        f"Was able to reach the Graveyard Shield Grave Chest by just waiting around.")

    def test_graveyard_shield_chest_yes_day_control_means_normal(self):
        """
        Checking if player can open the shield grave chest by just waiting until the sun sets
        """
        self.collect_by_name(Items.FAIRY_OCARINA)
        self.collect_by_name(Items.SONG_OF_TIME)
        self.assertTrue(self.can_reach_location(Locations.GRAVEYARD_SHIELD_GRAVE_CHEST),
                        f"Was able to reach the Graveyard Shield Grave Chest by playing the Song of Time.")
