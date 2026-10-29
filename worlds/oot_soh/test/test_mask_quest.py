from ..Enums import Items, Locations
from ..enums_gen import Events
from .bases import SohTestBase

MASKS = [Items.RG_KEATON_MASK, Items.RG_SKULL_MASK, Items.RG_SPOOKY_MASK, Items.RG_BUNNY_HOOD,
         Items.RG_GORON_MASK, Items.RG_ZORA_MASK, Items.RG_GERUDO_MASK, Items.RG_MASK_OF_TRUTH]

# Ship's trade chain (RLS has no "sold" steps: selling is a game flag, not a logic event).
CHAIN_EVENTS = [Events.LOGIC_CAN_BORROW_MASKS, Events.LOGIC_BORROW_SKULL_MASK, Events.LOGIC_BORROW_SPOOKY_MASK,
                Events.LOGIC_BORROW_BUNNY_HOOD, Events.LOGIC_BORROW_RIGHT_MASKS]

# The two masks the logic actually asks for, and the check each one gates.
MASK_CHECKS = ((Locations.RC_DEKU_THEATER_SKULL_MASK, Items.RG_SKULL_MASK),
               (Locations.RC_DEKU_THEATER_MASK_OF_TRUTH, Items.RG_MASK_OF_TRUTH))


def event_items(world) -> set[str]:
    return {loc.item.name for loc in world.multiworld.get_locations(world.player)
            if loc.address is None and loc.item is not None}


class MaskQuestBase(SohTestBase):
    def assert_masks_absent_from_pool(self):
        pool = [item.name for item in self.multiworld.itempool]
        for mask in MASKS:
            self.assertNotIn(str(mask), pool)

    def assert_chain_exists(self):
        events = event_items(self.world)
        for event in CHAIN_EVENTS:
            self.assertIn(str(event), events)


class TestMaskQuestCompleted(MaskQuestBase):
    options = {"complete_mask_quest": "completed"}

    def test_masks_are_not_in_the_pool(self):
        self.assert_masks_absent_from_pool()

    def test_the_chain_exists(self):
        self.assert_chain_exists()

    def test_the_checks_open_without_any_mask_item(self):
        """The masks are borrowed, so no item has to be found."""
        self.collect_all_but([str(mask) for mask in MASKS])
        for location, _ in MASK_CHECKS:
            with self.subTest(location=str(location)):
                self.assertTrue(self.can_reach_location(str(location)))


class TestMaskQuestVanilla(MaskQuestBase):
    options = {"complete_mask_quest": "vanilla"}

    def test_masks_are_not_in_the_pool(self):
        self.assert_masks_absent_from_pool()

    def test_the_chain_exists(self):
        self.assert_chain_exists()

    def test_the_checks_open_without_any_mask_item(self):
        self.collect_all_but([str(mask) for mask in MASKS])
        for location, _ in MASK_CHECKS:
            with self.subTest(location=str(location)):
                self.assertTrue(self.can_reach_location(str(location)))


class TestMaskQuestShuffle(MaskQuestBase):
    options = {"complete_mask_quest": "shuffle"}

    def test_every_mask_is_in_the_pool_once(self):
        pool = [item.name for item in self.multiworld.itempool]
        for mask in MASKS:
            self.assertEqual(pool.count(str(mask)), 1, f"{mask} should be shuffled exactly once")

    def test_the_borrow_events_cannot_stand_in_for_the_mask(self):
        """collect_all_but grants the borrow events outright -- the check must still want the item.

        This is the assertion that would fail if `has_item` dropped its option filter: the mask
        shop is closed under Shuffle, so nothing the chain grants may substitute for the item.
        """
        self.collect_all_but([str(mask) for mask in MASKS])
        for location, mask in MASK_CHECKS:
            with self.subTest(location=str(location)):
                self.assertFalse(self.can_reach_location(str(location)),
                                 f"{location} should need {mask} itself when the quest is shuffled")
                self.collect_by_name(str(mask))
                self.assertTrue(self.can_reach_location(str(location)))
                self.remove_by_name(str(mask))
