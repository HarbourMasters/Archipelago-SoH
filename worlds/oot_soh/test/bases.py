from test.bases import WorldTestBase
from ..Enums import Items, Regions
from .. Items import SohItem
from BaseClasses import ItemClassification as IC

class SohTestBase(WorldTestBase):
    game = "Ship of Harkinian"
    glitches_item_name = Items.GLITCHED

    def enable_glitched_item(self):
        """
        Enable the use of the glitched/sequence breaking item for unit test purposes.

        Also automatically award the item for convenience sake.
        """
        self.collect(self.world.create_item(Items.GLITCHED))

    def get_bundle(self) -> tuple:
        """
        Get a state, region and world bundle using ROOT as region.

        This will ignore age requirements on items because both ages can reach root.
        """
        return self.multiworld.state, Regions.ROOT, self.world
    
    def get_reg_bundle(self, region) -> tuple:
        """
        Get a state, region and world bundle using a specified region.

        This can be used to enfore age requirements by setting CHILD_SPAWN or ADULT_SPAWN as the required region
        """
        return self.multiworld.state, region, self.world
    
    def create_item(self, item) -> SohItem:
        """
        Create a SohItem by name to collect without having to have it shuffled first
        """
        return SohItem(item, IC.progression, None, self.world.player)
    
    def sweep(self) -> None:
        """
        Sweep multiworld state

        This is only necisery if you're running an assertion before collecting items
        """
        self.multiworld.state.sweep_for_advancements()
