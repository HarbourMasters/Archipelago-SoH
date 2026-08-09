from ..Items import Items
from .bases import SohTestBase

Options = {
    "bombchu_bag": "none",
    "infinite_upgrades": "off",
    "shuffle_childs_wallet": "false",
    "shuffle_tycoon_wallet": "false",
    "shuffle_deku_stick_bag": "false",
    "shuffle_deku_nut_bag": "false",
    "shuffle_swim": "false",
    "shuffle_kokiri_sword": "true",
    "shuffle_master_sword": "true",
    "shuffle_adult_trade_items": "true",
    "shuffle_boss_souls": "on_plus_ganons",
    "shuffle_ocarina_buttons": "true",
    "shuffle_fishing_pole": "true",
    "shuffle_gerudo_membership_card": "true",
    "lock_overworld_doors": "true",
    "boss_key_shuffle": "anywhere",
    "small_key_shuffle": "anywhere",
    "ganons_castle_boss_key": "anywhere",
    "shuffle_songs": "anywhere",
    "fortress_carpenters": "normal",
    "gerudo_fortress_key_shuffle": "anywhere",
}

Tier = {"balanced": 0, "plentiful": 1, "scarce": 2, "minimal": 3}

# item -> (balanced, plentiful, scarce, minimal) expected copies in the pool.
ExpectedCounts: dict[Items, tuple[int, int, int, int]] = {
    # Unconditional single-copy items
    Items.BOOMERANG: (1, 2, 1, 1),
    Items.CLAIM_CHECK: (1, 2, 1, 1),
    Items.PROGRESSIVE_HOOKSHOT: (2, 2, 2, 2),
    Items.NAYRUS_LOVE: (1, 2, 1, 0),        
    Items.FARORES_WIND: (1, 2, 1, 0),
    Items.BIGGORONS_SWORD: (1, 2, 1, 0),
    Items.DOUBLE_DEFENSE: (1, 2, 0, 0),
    Items.STRENGTH_UPGRADE: (3, 4, 3, 3),
    Items.PROGRESSIVE_BOW: (3, 4, 2, 1),
    Items.PROGRESSIVE_SLINGSHOT: (3, 4, 2, 1),
    Items.PROGRESSIVE_BOMB_BAG: (3, 4, 2, 1),
    Items.PROGRESSIVE_MAGIC_METER: (2, 3, 1, 1),
    Items.PROGRESSIVE_STICK_CAPACITY: (2, 3, 1, 0),
    Items.PROGRESSIVE_NUT_CAPACITY: (2, 3, 1, 0),
    Items.PROGRESSIVE_WALLET: (2, 3, 2, 2),
    Items.PROGRESSIVE_SCALE: (2, 3, 2, 2),
    Items.BOMBCHUS_5: (1, 1, 1, 1),
    Items.BOMBCHUS_10: (3, 3, 2, 0),
    Items.BOMBCHUS_20: (1, 2, 0, 0),
    Items.KOKIRI_SWORD: (1, 2, 1, 1),
    Items.MASTER_SWORD: (1, 2, 1, 1),
    Items.POCKET_EGG: (1, 2, 1, 1),
    Items.ODD_POTION: (1, 2, 1, 1),
    Items.GOHMAS_SOUL: (1, 2, 1, 1),
    Items.GANONS_SOUL: (1, 2, 1, 1),
    Items.OCARINA_A_BUTTON: (1, 2, 1, 1),
    Items.GUARD_HOUSE_KEY: (1, 2, 1, 1),
    Items.FISHING_POLE: (1, 2, 1, 1),
    Items.GERUDO_MEMBERSHIP_CARD: (1, 2, 1, 1),
    Items.ZELDAS_LULLABY: (1, 2, 1, 1),
    Items.FOREST_TEMPLE_SMALL_KEY: (5, 6, 5, 5),
    Items.FIRE_TEMPLE_SMALL_KEY: (8, 9, 8, 8),
    Items.GANONS_CASTLE_SMALL_KEY: (2, 3, 2, 2),
    Items.FOREST_TEMPLE_BOSS_KEY: (1, 2, 1, 1),
    Items.GANONS_CASTLE_BOSS_KEY: (1, 2, 1, 1),
    Items.GERUDO_FORTRESS_SMALL_KEY: (4, 5, 4, 4),
}


def count_in_pool(test: SohTestBase, item: Items) -> int:
    return sum(1 for i in test.multiworld.itempool if i.player == test.player and i.name == item)


def assert_pool_tier(test: SohTestBase, tier: str) -> None:
    idx = Tier[tier]
    for item, counts in ExpectedCounts.items():
        expected = counts[idx]
        actual = count_in_pool(test, item)
        test.assertEqual(actual, expected, f"{item}: expected {expected} in the {tier} pool, got {actual}")


class TestItemPoolBalanced(SohTestBase):
    run_default_tests = False
    options = {**Options, "item_pool": "balanced"}

    def test_item_pool_counts(self):
        assert_pool_tier(self, "balanced")


class TestItemPoolPlentiful(SohTestBase):
    run_default_tests = False
    options = {**Options, "item_pool": "plentiful"}

    def test_item_pool_counts(self):
        assert_pool_tier(self, "plentiful")


class TestItemPoolScarce(SohTestBase):
    run_default_tests = False
    options = {**Options, "item_pool": "scarce"}

    def test_item_pool_counts(self):
        assert_pool_tier(self, "scarce")


class TestItemPoolMinimal(SohTestBase):
    run_default_tests = False
    options = {**Options, "item_pool": "minimal"}

    def test_item_pool_counts(self):
        assert_pool_tier(self, "minimal")


class TestItemPoolProgressiveDeltas(SohTestBase):
    """Options that add extra copies (infinite upgrades, extra wallets, deku bags, swim) should stack on top of the per-option base amount."""
    run_default_tests = False
    options = {
        "item_pool": "balanced",
        "bombchu_bag": "none",
        "infinite_upgrades": "progressive",
        "shuffle_childs_wallet": "true",
        "shuffle_tycoon_wallet": "true",
        "shuffle_deku_stick_bag": "true",
        "shuffle_deku_nut_bag": "true",
        "shuffle_swim": "true",
    }

    def test_progressive_deltas(self):
        # base balanced amount + infinite upgrade copy
        self.assertEqual(count_in_pool(self, Items.PROGRESSIVE_BOW), 4)          # 3 + 1
        self.assertEqual(count_in_pool(self, Items.PROGRESSIVE_SLINGSHOT), 4)    # 3 + 1
        self.assertEqual(count_in_pool(self, Items.PROGRESSIVE_BOMB_BAG), 4)     # 3 + 1
        self.assertEqual(count_in_pool(self, Items.PROGRESSIVE_MAGIC_METER), 3)  # 2 + 1
        # base + infinite + both wallets
        self.assertEqual(count_in_pool(self, Items.PROGRESSIVE_WALLET), 5)       # 2 + 1 + 2
        # base + infinite + deku bag
        self.assertEqual(count_in_pool(self, Items.PROGRESSIVE_STICK_CAPACITY), 4)  # 2 + 1 + 1
        self.assertEqual(count_in_pool(self, Items.PROGRESSIVE_NUT_CAPACITY), 4)    # 2 + 1 + 1
        # scale gets the swim copy but not an infinite-upgrade copy
        self.assertEqual(count_in_pool(self, Items.PROGRESSIVE_SCALE), 3)        # 2 + 1
        # strength gets neither
        self.assertEqual(count_in_pool(self, Items.STRENGTH_UPGRADE), 3)


class TestItemPoolBombchuBagProgressive(SohTestBase):
    run_default_tests = False
    options = {"item_pool": "balanced", "bombchu_bag": "progressive_bags", "infinite_upgrades": "progressive"}

    def test_bombchu_bag(self):
        # progressive bombchu bag: balanced 3 + infinite upgrade copy, and no loose bombchus
        self.assertEqual(count_in_pool(self, Items.BOMBCHU_BAG), 4)
        self.assertEqual(count_in_pool(self, Items.BOMBCHUS_5), 0)
        self.assertEqual(count_in_pool(self, Items.BOMBCHUS_10), 0)
        self.assertEqual(count_in_pool(self, Items.BOMBCHUS_20), 0)


class TestItemPoolBombchuBagSingle(SohTestBase):
    run_default_tests = False
    options = {"item_pool": "plentiful", "bombchu_bag": "single_bag"}

    def test_bombchu_bag(self):
        # single bombchu bag: plentiful amount 6, and no loose bombchus
        self.assertEqual(count_in_pool(self, Items.BOMBCHU_BAG), 6)
        self.assertEqual(count_in_pool(self, Items.BOMBCHUS_5), 0)
        self.assertEqual(count_in_pool(self, Items.BOMBCHUS_10), 0)
        self.assertEqual(count_in_pool(self, Items.BOMBCHUS_20), 0)


class TestItemPoolKeyRing(SohTestBase):
    run_default_tests = False
    options = {
        "item_pool": "balanced",
        "small_key_shuffle": "anywhere",
        "key_rings": "selection",
        "forest_temple_key_ring": "true",
    }

    def test_key_ring_replaces_small_keys(self):
        self.assertEqual(count_in_pool(self, Items.FOREST_TEMPLE_KEY_RING), 1)
        self.assertEqual(count_in_pool(self, Items.FOREST_TEMPLE_SMALL_KEY), 0)


class TestItemPoolKeyRingPlentiful(SohTestBase):
    run_default_tests = False
    options = {
        "item_pool": "plentiful",
        "small_key_shuffle": "anywhere",
        "key_rings": "selection",
        "forest_temple_key_ring": "true",
    }

    def test_key_ring_plentiful(self):
        self.assertEqual(count_in_pool(self, Items.FOREST_TEMPLE_KEY_RING), 2)
        self.assertEqual(count_in_pool(self, Items.FOREST_TEMPLE_SMALL_KEY), 0)


class TestItemPoolGerudoFortressFast(SohTestBase):
    run_default_tests = False
    options = {"item_pool": "plentiful", "gerudo_fortress_key_shuffle": "anywhere", "fortress_carpenters": "fast"}

    def test_fast_carpenters_single_key(self):
        # Fast carpenters only need one key; plentiful adds one more
        self.assertEqual(count_in_pool(self, Items.GERUDO_FORTRESS_SMALL_KEY), 2)


class TestItemPoolOcarina(SohTestBase):
    run_default_tests = False
    options = {"item_pool": "plentiful", "shuffle_ocarinas": "true", "start_with_ocarina": "off"}

    def test_ocarina_plentiful(self):
        # Starting without an ocarina puts 2 in the pool; plentiful adds one more
        self.assertEqual(count_in_pool(self, Items.PROGRESSIVE_OCARINA), 3)
