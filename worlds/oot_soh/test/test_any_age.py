from .bases import SohTestBase
from ..Enums import Items, Ages
from ..enums_gen import Regions
from ..functions_gen import blast_or_smash
from ..LogicHelpers import any_age, is_adult
from ..Regions import SohRegion


class TestAnyAge(SohTestBase):
    """Ship's Region::AnyAgeTime widens the age flags to the parent region's own access, 
    so a condition only one age can satisfy opens the edge for both.
    """

    options = {"starting_age": "child"}

    def test_widens_pinned_age(self):
        # Everything except explosives: adult can blast_or_smash (hammer), child cannot.
        self.collect_all_but([Items.RG_BOMB_BAG, Items.RG_PROGRESSIVE_BOMB_BAG, Items.RG_PROGRESSIVE_BOMBCHU_BAG])
        self.sweep()
        state = self.multiworld.state
        player = self.world.player
        bundle = self.get_reg_bundle(Regions.RR_HYRULE_FIELD)

        plain = blast_or_smash(bundle).resolve(self.world)
        wrapped = any_age(bundle, blast_or_smash).resolve(self.world)

        self.assertTrue(all(state._soh_region_ages(Regions.RR_HYRULE_FIELD, player)),
                        "Hyrule Field should be reachable as both ages.")

        # Pin the CHILD context the way the reachability sweep does.
        state._soh_age[player] = Ages.CHILD
        try:
            self.assertFalse(plain(state),
                             "Unwrapped blast_or_smash should fail for pinned child with no explosives.")
            self.assertTrue(wrapped(state),
                            "any_age should widen to adult access and pass, matching Ship.")
        finally:
            state._soh_age[player] = Ages.null

        # The widening must not leak past evaluation.
        self.assertIsNone(state._soh_widen[player])

    def test_false_when_region_unreachable(self):
        """Ship's trailing `&& (IsAdult || IsChild)` no age access, no pass."""
        self.collect_by_name([Items.RG_MEGATON_HAMMER])
        self.sweep()
        state = self.multiworld.state
        region = Regions.RR_GANONS_TOWER_BEFORE_GANONDORF_LAIR
        bundle = self.get_reg_bundle(region)
        wrapped = any_age(bundle, blast_or_smash).resolve(self.world)
        self.assertFalse(any(state._soh_region_ages(region, self.world.player)),
                         "Ganon's Tower should be unreachable here.")
        self.assertFalse(wrapped(state))


class TestAnyAgeReachesFixpoint(SohTestBase):
    """
    Test that opening an edge with any_age as adult also opens the edge as child.
    """

    options = {"starting_age": "child"}

    def test_child_edge_opened_by_adult_access(self):
        world, player = self.world, self.world.player
        field = world.get_region(str(Regions.RR_HYRULE_FIELD))
        grotto = SohRegion("Test Widened Grotto", player, self.multiworld)
        self.multiworld.regions.append(grotto)
        world.create_entrance(field, grotto, any_age((Regions.RR_HYRULE_FIELD, world), is_adult))

        state = self.multiworld.get_all_state(False)
        state._soh_invalidate(player)
        grotto.can_reach(state)

        self.assertIn(field, state._soh_adult_reachable_regions[player],
                      "Adult should reach Hyrule Field.")
        self.assertIn(grotto, state._soh_child_reachable_regions[player],
                      "Child should get through once adult can reach Hyrule Field, matching Ship.")
