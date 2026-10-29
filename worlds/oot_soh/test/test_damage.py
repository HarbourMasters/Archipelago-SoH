from .. import SohWorld
from ..Items import Items, SohItem
from .bases import SohTestBase
from ..functions_gen import can_attack
from itertools import combinations

class TestCanAttack(SohTestBase):
    """
    Test can_attack helper
    """
    options = {"shuffle_deku_nut_bag": True, "shuffle_deku_stick_bag": True, "closed_forest": 2, "door_of_time": 2, "shuffle_kokiri_sword": 1, "shuffle_master_sword": 1, "bombchu_bag": 1, "bombchu_drops": 1}

    def require_any_to_damage(self, items: list[Items]) -> None:
        # ideally we run these as subtests, but those are currently broken 
        # and report as Success if any subtest succeeds
        # (https://github.com/microsoft/vscode-python/issues/25824)

        self.sweep()
        self.remove_by_name(items)

        for size in range(1, len(items)):
            for valid_combo in combinations(items, size):
                self.collect_by_name(valid_combo)
                self.assertTrue(can_attack(self.get_bundle())._instantiate(self.world)._evaluate(self.multiworld.state), f"Couldn't attack but should have been able to.")
                self.remove_by_name(valid_combo)
                

        self.collect_by_name(items)

        self.assertTrue(can_attack(self.get_bundle())._instantiate(self.world)._evaluate(self.multiworld.state), f"Couldn't attack but should have been able to.")
        
        self.remove_by_name(items)

    def test_can_attack(self):

        # Has Nothing
        self.assertFalse(can_attack(self.get_bundle())._instantiate(self.world)._evaluate(self.multiworld.state), f"Could attack but shouldn't have been able to.")

        # Attacking items
        items = [Items.RG_MEGATON_HAMMER, Items.RG_KOKIRI_SWORD, Items.RG_MASTER_SWORD, Items.RG_BIGGORON_SWORD, Items.RG_PROGRESSIVE_STICK_UPGRADE, 
            Items.RG_PROGRESSIVE_HOOKSHOT, Items.RG_PROGRESSIVE_SLINGSHOT, Items.RG_PROGRESSIVE_BOW, Items.RG_BOOMERANG, Items.RG_PROGRESSIVE_BOMB_BAG, Items.RG_PROGRESSIVE_BOMBCHU_BAG]
        self.require_any_to_damage(items)

        # Check Din's Fire
        items = [Items.RG_PROGRESSIVE_MAGIC_METER, Items.RG_DINS_FIRE]
        self.collect_by_name(items)

        self.assertTrue(can_attack(self.get_bundle())._instantiate(self.world)._evaluate(self.multiworld.state), f"Couldn't attack but should have been able to.")

        self.remove_by_name(items)