from BaseClasses import CollectionState
from ..Enums import Items
from .bases import SohTestBase

ABILITY_ITEMS = {
    "shuffle_climb": [Items.RG_CLIMB],
    "shuffle_crawl": [Items.RG_CRAWL],
    "shuffle_open_chest": [Items.RG_OPEN_CHEST],
    "shuffle_jabber_nuts": [Items.RG_SPEAK_DEKU, Items.RG_SPEAK_GERUDO, Items.RG_SPEAK_GORON,
                            Items.RG_SPEAK_HYLIAN, Items.RG_SPEAK_KOKIRI, Items.RG_SPEAK_ZORA],
    "shuffle_bean_souls": [Items.RG_DEATH_MOUNTAIN_CRATER_BEAN_SOUL,
                           Items.RG_DEATH_MOUNTAIN_TRAIL_BEAN_SOUL, Items.RG_DESERT_COLOSSUS_BEAN_SOUL,
                           Items.RG_GERUDO_VALLEY_BEAN_SOUL, Items.RG_GRAVEYARD_BEAN_SOUL,
                           Items.RG_KOKIRI_FOREST_BEAN_SOUL, Items.RG_LAKE_HYLIA_BEAN_SOUL,
                           Items.RG_LOST_WOODS_BEAN_SOUL, Items.RG_LOST_WOODS_BRIDGE_BEAN_SOUL,
                           Items.RG_ZORAS_RIVER_BEAN_SOUL],
}
ALL_ABILITY_ITEMS = [item for items in ABILITY_ITEMS.values() for item in items]


def shuffled_items(test: SohTestBase):
    """The pool plus what pre_fill already placed (Open Chests goes early)."""
    return [*test.multiworld.itempool,
            *(loc.item for loc in test.multiworld.get_filled_locations(test.player) if loc.item.code is not None)]


class TestAbilitiesOff(SohTestBase):
    options = {name: "false" for name in [*ABILITY_ITEMS, "shuffle_grab"]}

    def test_no_ability_items_in_the_pool(self):
        pool = [item.name for item in self.multiworld.itempool]
        for item in ALL_ABILITY_ITEMS:
            self.assertNotIn(str(item), pool, f"{item} should not be shuffled when its option is off")

    def test_grab_is_granted(self):
        self.assertTrue(self.multiworld.state.has(str(Items.RG_PROGRESSIVE_STRENGTH), self.player, 1),
                        "the hidden starting strength stands in for the Power Bracelet")


class TestAbilitiesOn(SohTestBase):
    options = {name: "true" for name in [*ABILITY_ITEMS, "shuffle_grab"]}

    def test_every_ability_item_is_in_the_pool_exactly_once(self):
        pool = [item.name for item in shuffled_items(self)]
        for item in ALL_ABILITY_ITEMS:
            self.assertEqual(pool.count(str(item)), 1, f"{item} should be shuffled exactly once")

    def test_pool_still_matches_the_location_count(self):
        """16 extra progression items must displace filler, not overflow the world."""
        unfilled = len([loc for loc in self.multiworld.get_unfilled_locations(self.world.player)])
        self.assertEqual(len(self.multiworld.itempool), unfilled,
                         "item pool and unfilled location count disagree")

    def test_abilities_are_progression(self):
        by_name = {item.name: item for item in shuffled_items(self)}
        for item in ALL_ABILITY_ITEMS:
            self.assertTrue(by_name[str(item)].advancement, f"{item} should be progression")

    def test_grab_adds_a_strength_upgrade(self):
        pool = [item.name for item in self.multiworld.itempool]
        self.assertEqual(pool.count(str(Items.RG_PROGRESSIVE_STRENGTH)), 4)
        self.assertNotIn(str(Items.RG_POWER_BRACELET), pool)


class TestAbilitiesPlentiful(SohTestBase):
    """Ship pools each ability twice on plentiful (item_pool.cpp:409-425, 553-564)."""
    run_default_tests = False
    options = {**{name: "true" for name in ABILITY_ITEMS}, "item_pool": "plentiful"}

    def test_two_of_each(self):
        pool = [item.name for item in shuffled_items(self)]
        for item in ALL_ABILITY_ITEMS:
            self.assertEqual(pool.count(str(item)), 2, f"{item} should be shuffled twice on plentiful")


def assert_obtainable_at_start(test: SohTestBase, item: Items) -> None:
    """The item is held from the start, or sits on a location reachable by collecting what is
    reachable from the start (so one early item can open the spot for the next)."""
    if str(item) in [i.name for i in test.multiworld.precollected_items[test.player]]:
        return
    state = CollectionState(test.multiworld)
    state.sweep_for_advancements()
    location = next(loc for loc in test.multiworld.get_locations(test.player) if loc.item and loc.item.name == item)
    test.assertTrue(location.can_reach(state), f"{item} landed on {location.name}")


class TestStartItemsWithNothingAtStart(SohTestBase):
    """Test items are correctly placed in sphere 1"""
    options = {"shuffle_open_chest": "true", "shuffle_climb": "true", "shuffle_crawl": "true",
               "starting_age": "child", "closed_forest": "on", "start_with_links_pocket": "nothing"}

    def test_starts_with_open_chests(self):
        self.assertIn(str(Items.RG_OPEN_CHEST), [i.name for i in self.multiworld.precollected_items[self.player]])

    def test_climb_is_obtainable_at_start(self):
        assert_obtainable_at_start(self, Items.RG_CLIMB)


class TestStartItemsPlacedAtStart(SohTestBase):
    """Same start, but Link's Pocket is free: Open Chests goes there instead of being given."""
    options = {**TestStartItemsWithNothingAtStart.options, "start_with_links_pocket": "advancement",
               "shuffle_dungeon_rewards": "anywhere"}

    def test_both_are_taken_out_of_the_pool_and_obtainable_at_start(self):
        pool = [item.name for item in self.multiworld.itempool]
        for item in (Items.RG_OPEN_CHEST, Items.RG_CLIMB):
            self.assertNotIn(str(item), pool, f"{item} should have been taken out of the pool")
            assert_obtainable_at_start(self, item)


class TestStartItemsStayInPoolWithOpenForest(SohTestBase):
    """Without a closed forest the start is not tight, so the items are left to the normal fill
    instead of being pinned to the first spots, which would make seeds look alike."""
    options = {"shuffle_open_chest": "true", "shuffle_climb": "true", "starting_age": "adult",
               "closed_forest": "off"}

    def test_items_stay_in_the_pool(self):
        pool = [item.name for item in self.multiworld.itempool]
        precollected = [item.name for item in self.multiworld.precollected_items[self.player]]
        for item in (Items.RG_OPEN_CHEST, Items.RG_CLIMB):
            self.assertIn(str(item), pool)
            self.assertNotIn(str(item), precollected)


class TestStartItemsStayInPoolWithFreeLocations(SohTestBase):
    """A closed forest is only a problem while the start has nothing to check. 
    With every freestanding item shuffled there are plenty of free locations in Kokiri Forest."""
    options = {"shuffle_open_chest": "true", "shuffle_climb": "true", "starting_age": "child",
               "closed_forest": "on", "shuffle_freestanding_items": "all"}

    def test_items_stay_in_the_pool(self):
        pool = [item.name for item in self.multiworld.itempool]
        for item in (Items.RG_OPEN_CHEST, Items.RG_CLIMB):
            self.assertIn(str(item), pool)


class TestStartItemsPlacedWithFewFreeLocations(SohTestBase):
    """Pots add only five free locations, which is not enough to leave the fill alone."""
    options = {**TestStartItemsStayInPoolWithFreeLocations.options, "shuffle_freestanding_items": "off",
               "shuffle_pots": "all"}

    def test_items_are_taken_out_of_the_pool(self):
        pool = [item.name for item in self.multiworld.itempool]
        for item in (Items.RG_OPEN_CHEST, Items.RG_CLIMB):
            self.assertNotIn(str(item), pool)
            assert_obtainable_at_start(self, item)
