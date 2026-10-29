"""Locations declared by more than one region.

RLS lets several regions declare the same location, meaning "reachable from any of these". An AP
location has exactly one parent region, and AP only consults its rule when that parent is
reachable -- so `Regions.materialize_locations` gives such a location a region of its own and an
entrance from each declaring region, letting AP's own BFS compute the union.

52 of the 1543 generated locations have more than one parent today, up to 7.
"""
from BaseClasses import ItemClassification as IC

from .bases import SohTestBase
from ..Enums import Items
from ..enums_gen import Regions
from ..Items import SohItem
from ..Locations import SohLocData, location_data_table
from ..Regions import materialize_locations
from rule_builder.rules import False_, Has, True_

# Two regions that are always reachable, so the test measures the union rather than the fixture.
PARENT_A = Regions.RR_ROOT
PARENT_B = Regions.RR_KOKIRI_FOREST


class TestMultiRegionLocations(SohTestBase):
    options = {"starting_age": "child"}

    def setUp(self):
        super().setUp()
        created = {loc.name for loc in self.multiworld.get_locations(self.world.player)}
        self.spare = next(name for name, data in location_data_table.items()
                          if name not in created and data.loc_id is not None)
        self.world.included_locations[self.spare] = location_data_table[self.spare]
        self.world._soh_pending_locations = {}

        for region in (PARENT_A, PARENT_B):
            self.assertTrue(self.world.get_region(str(region)).can_reach(self.multiworld.state),
                            f"Fixture broken: {region} should be reachable from the start.")

    def claim(self, *claims):
        self.world._soh_pending_locations = {self.spare: list(claims)}
        return materialize_locations(self.world)

    def holder_name(self):
        return f"{self.spare} (Access)"

    def test_single_parent_creates_no_holder_region(self):
        self.claim((PARENT_A, lambda bundle: True_()))
        location = self.world.get_location(self.spare)
        self.assertEqual(location.parent_region.name, str(PARENT_A))
        self.assertNotIn(self.holder_name(),
                         {r.name for r in self.multiworld.get_regions(self.world.player)})

    def test_two_parents_create_one_holder_with_an_entrance_from_each(self):
        self.claim((PARENT_A, lambda bundle: True_()), (PARENT_B, lambda bundle: True_()))

        location = self.world.get_location(self.spare)
        self.assertEqual(location.parent_region.name, self.holder_name())

        holder = self.world.get_region(self.holder_name())
        sources = {e.parent_region.name for e in holder.entrances}
        self.assertEqual(sources, {str(PARENT_A), str(PARENT_B)})
        self.assertEqual(list(holder.exits), [])

    def test_either_parent_alone_grants_access(self):
        a_only, b_only = Items.RG_BOMB_BAG, Items.RG_MEGATON_HAMMER
        self.claim((PARENT_A, lambda bundle: Has(a_only)),
                   (PARENT_B, lambda bundle: Has(b_only)))
        location = self.world.get_location(self.spare)

        state = self.multiworld.get_all_state()
        for item in (a_only, b_only):
            state.remove(SohItem(item, IC.progression, None, self.world.player))
        self.assertFalse(location.can_reach(state), "reachable with neither key item")

        state.collect(SohItem(a_only, IC.progression, None, self.world.player), True)
        self.assertTrue(location.can_reach(state), "should be reachable via the first parent")

        state.remove(SohItem(a_only, IC.progression, None, self.world.player))
        state.collect(SohItem(b_only, IC.progression, None, self.world.player), True)
        self.assertTrue(location.can_reach(state), "should be reachable via the second parent")

    def test_pruned_parents_are_dropped_and_the_rest_still_count(self):
        self.claim((PARENT_A, lambda bundle: False_()), (PARENT_B, lambda bundle: True_()))
        self.assertEqual(self.world.get_location(self.spare).parent_region.name, str(PARENT_B))

    def test_location_with_every_parent_pruned_is_never_created(self):
        dropped = self.claim((PARENT_A, lambda bundle: False_()),
                             (PARENT_B, lambda bundle: False_()))
        self.assertEqual(dropped, [self.spare])
        self.assertNotIn(self.spare,
                         {loc.name for loc in self.multiworld.get_locations(self.world.player)})

    def test_a_location_the_seed_excludes_is_skipped_entirely(self):
        del self.world.included_locations[self.spare]
        self.assertEqual(self.claim((PARENT_A, lambda bundle: True_()),
                                    (PARENT_B, lambda bundle: True_())), [])
        self.assertNotIn(self.spare,
                         {loc.name for loc in self.multiworld.get_locations(self.world.player)})
