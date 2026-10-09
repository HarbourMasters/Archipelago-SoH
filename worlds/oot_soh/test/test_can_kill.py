from .. import SohWorld
from ..Enums import Items, Enemies, EnemyDistance
from ..enums_gen import Events
from .bases import SohTestBase
from ..functions_gen import can_kill
from itertools import combinations

class KillBase(SohTestBase):
    __Test__ = False

    def require_all_to_beat(self, items: list[Items | Events], enemy: Enemies, distance: EnemyDistance = EnemyDistance.ED_CLOSE,
                   wall_or_floor: bool = True, quantity: int = 1, timer: bool = False, in_water: bool = False) -> None:
        # ideally we run these as subtests, but those are currently broken 
        # and report as Success if any subtest succeeds
        # (https://github.com/microsoft/vscode-python/issues/25824)

        self.sweep()
        self.remove_by_name(items)

        for size in range(1, len(items)):
            for invalid_combo in combinations(items, size):
                self.collect_by_name(invalid_combo)
                self.assertFalse(can_kill(self.get_bundle(), enemy, distance, wall_or_floor, quantity, timer, in_water)._instantiate(self.world)._evaluate(self.multiworld.state), f"Was able to kill {quantity} {str(enemy)}, but shouldn't have been able to with only {invalid_combo} at distance {str(distance.name)} {"on wall or floor" if wall_or_floor else "not on wall or floor"}")
                self.remove_by_name(invalid_combo)
                

        self.collect_by_name(items)

        self.assertTrue(can_kill(self.get_bundle(), enemy, distance, wall_or_floor, quantity, timer, in_water)._instantiate(self.world)._evaluate(self.multiworld.state), f"Wasn't able to kill {quantity} {str(enemy)}, but should have been able to at distance {str(distance.name)} {"on wall or floor" if wall_or_floor else "not on wall or floor"}")

        self.remove_by_name(items)

    def require_any_to_beat(self, items: list[Items | Events], enemy: Enemies, distance: EnemyDistance = EnemyDistance.ED_CLOSE,
                   wall_or_floor: bool = True, quantity: int = 1, timer: bool = False, in_water: bool = False) -> None:
        # ideally we run these as subtests, but those are currently broken 
        # and report as Success if any subtest succeeds
        # (https://github.com/microsoft/vscode-python/issues/25824)

        self.sweep()
        self.remove_by_name(items)

        for size in range(1, len(items)):
            for valid_combo in combinations(items, size):
                self.collect_by_name(valid_combo)
                self.assertTrue(can_kill(self.get_bundle(), enemy, distance, wall_or_floor, quantity, timer, in_water)._instantiate(self.world)._evaluate(self.multiworld.state), f"Wasn't able to kill {quantity} {str(enemy)}, but should have been able to with only {valid_combo} at distance {str(distance.name)} {"on wall or floor" if wall_or_floor else "not on wall or floor"}")
                self.remove_by_name(valid_combo)
                

        self.collect_by_name(items)

        self.assertTrue(can_kill(self.get_bundle(), enemy, distance, wall_or_floor, quantity, timer, in_water)._instantiate(self.world)._evaluate(self.multiworld.state), f"Wasn't able to kill {quantity} {str(enemy)}, but should have been able to at distance {str(distance.name)} {"on wall or floor" if wall_or_floor else "not on wall or floor"}")
        
        self.remove_by_name(items)

    def cannot_beat_with_any(self, items: list[Items], enemy: Enemies) -> None:
        """Each of these items, held alone, is not enough to kill the enemy."""
        self.sweep()
        self.remove_by_name(items)
        for item in items:
            self.collect_by_name([item])
            self.assertFalse(can_kill(self.get_bundle(), enemy)._instantiate(self.world)._evaluate(self.multiworld.state),
                             f"Was able to kill {str(enemy)} with only {item}")
            self.remove_by_name([item])

# Can Kill Regular Enemies
class TestCanKillEnemy(KillBase):
    options = {"shuffle_deku_nut_bag": True, "shuffle_deku_stick_bag": True, "closed_forest": 2, "door_of_time": 2, "shuffle_kokiri_sword": 1, "shuffle_master_sword": 1}

    """
    Testing to see if we can kill regular enemies. 
    This only checks for special cases, not other helper functions
    """
    def test_gerudo_guard(self):
        """
        Checking if player can kill Gerudo Guard
        """
        for enemy in (Enemies.RE_GERUDO_GUARD, Enemies.RE_BREAK_ROOM_GUARD):
            self.assertFalse(can_kill(self.get_bundle(), enemy)._instantiate(self.world)._evaluate(self.multiworld.state), f'Could kill {str(enemy)}. This should be impossible.')

    def test_gold_skulltula(self):
        """
        Checking if player can kill Gold Skulltula
        """
        enemy = Enemies.RE_GOLD_SKULLTULA
        items = [Items.RG_BOOMERANG]
        # Boomerang and Hookshot overlapping distances
        for distance in (EnemyDistance.ED_CLOSE, EnemyDistance.ED_SHORT_JUMPSLASH, EnemyDistance.ED_MASTER_SWORD_JUMPSLASH, 
                         EnemyDistance.ED_LONG_JUMPSLASH, EnemyDistance.ED_BOMB_THROW, EnemyDistance.ED_BOOMERANG):
            self.require_all_to_beat(items, enemy, distance)

        # Dins Fire
        items = [Items.RG_PROGRESSIVE_MAGIC_METER, Items.RG_DINS_FIRE]
        for distance in (EnemyDistance.ED_CLOSE, EnemyDistance.ED_SHORT_JUMPSLASH, EnemyDistance.ED_MASTER_SWORD_JUMPSLASH, 
                         EnemyDistance.ED_LONG_JUMPSLASH, EnemyDistance.ED_BOMB_THROW, EnemyDistance.ED_BOOMERANG):
            self.require_all_to_beat(items, enemy, distance)

        # Bombchus
        items = [Items.RG_PROGRESSIVE_BOMB_BAG]
        for distance in (EnemyDistance.ED_CLOSE, EnemyDistance.ED_SHORT_JUMPSLASH, EnemyDistance.ED_MASTER_SWORD_JUMPSLASH, 
                         EnemyDistance.ED_LONG_JUMPSLASH, EnemyDistance.ED_BOMB_THROW, EnemyDistance.ED_BOOMERANG, 
                         EnemyDistance.ED_HOOKSHOT, EnemyDistance.ED_LONGSHOT):
            self.require_all_to_beat(items, enemy, distance)

    def test_big_skulltula(self):
        """
        Checking if player can kill Big Skulltula
        """
        enemy = Enemies.RE_BIG_SKULLTULA

        # Dins Fire (Ship: reaches ED_BOMB_THROW, not ED_BOOMERANG, unlike gold skulltulas)
        items = [Items.RG_PROGRESSIVE_MAGIC_METER, Items.RG_DINS_FIRE]
        for distance in (EnemyDistance.ED_CLOSE, EnemyDistance.ED_SHORT_JUMPSLASH, EnemyDistance.ED_MASTER_SWORD_JUMPSLASH, 
                         EnemyDistance.ED_LONG_JUMPSLASH, EnemyDistance.ED_BOMB_THROW):
            self.require_all_to_beat(items, enemy, distance)

    def test_dodongo(self):
        """
        Checking if player can kill Dodongo
        """
        enemy = Enemies.RE_DODONGO
     
 
        items = [Items.RG_MEGATON_HAMMER, Items.RG_PROGRESSIVE_SLINGSHOT, Items.RG_PROGRESSIVE_BOW]
        self.require_any_to_beat(items, enemy)

        # Sticks
        items = [Items.RG_PROGRESSIVE_STICK_UPGRADE]
        for i in range(1,6):
            self.require_any_to_beat(items, enemy, quantity=i)

    def test_lizalfos(self):
        """
        Checking if player can kill Lizalfos
        """
        enemy = Enemies.RE_LIZALFOS

        items = [Items.RG_MEGATON_HAMMER, Items.RG_KOKIRI_SWORD, Items.RG_MASTER_SWORD, 
                 Items.RG_BIGGORON_SWORD, Items.RG_PROGRESSIVE_BOW, Items.RG_PROGRESSIVE_SLINGSHOT, Items.RG_PROGRESSIVE_BOMB_BAG]
        self.require_any_to_beat(items, enemy)

    def test_keese(self):
        for enemy in (Enemies.RE_KEESE, Enemies.RE_FIRE_KEESE):
            # Close
            self.require_all_to_beat([Items.RG_KOKIRI_SWORD], enemy)

            # <= Boomerang
            for distance in (EnemyDistance.ED_CLOSE, EnemyDistance.ED_SHORT_JUMPSLASH, EnemyDistance.ED_MASTER_SWORD_JUMPSLASH, 
                             EnemyDistance.ED_LONG_JUMPSLASH, EnemyDistance.ED_BOMB_THROW, EnemyDistance.ED_BOOMERANG):
                self.require_all_to_beat([Items.RG_BOOMERANG], enemy, distance)

            # Short Jumpslash
            self.require_all_to_beat([Items.RG_MEGATON_HAMMER], enemy, EnemyDistance.ED_SHORT_JUMPSLASH)

    def test_gohma_larva(self):
        """
        Checking if player can kill Gohma Larva
        """
        items = [Items.RG_KOKIRI_SWORD, Items.RG_MASTER_SWORD, Items.RG_BIGGORON_SWORD, Items.RG_PROGRESSIVE_STICK_UPGRADE, Items.RG_MEGATON_HAMMER, Items.RG_PROGRESSIVE_BOMB_BAG, Items.RG_PROGRESSIVE_SLINGSHOT, Items.RG_PROGRESSIVE_BOW, Items.RG_BOOMERANG, Items.RG_PROGRESSIVE_HOOKSHOT]
        self.require_any_to_beat(items, Enemies.RE_GOHMA_LARVA)
        self.require_all_to_beat([Items.RG_PROGRESSIVE_MAGIC_METER, Items.RG_DINS_FIRE], Enemies.RE_GOHMA_LARVA)

    def test_mad_scrub(self):
        """
        Checking if player can kill Mad Scrub
        """
        items = [Items.RG_KOKIRI_SWORD, Items.RG_MASTER_SWORD, Items.RG_BIGGORON_SWORD, Items.RG_PROGRESSIVE_STICK_UPGRADE, Items.RG_MEGATON_HAMMER, Items.RG_PROGRESSIVE_BOMB_BAG, Items.RG_PROGRESSIVE_SLINGSHOT, Items.RG_PROGRESSIVE_BOW, Items.RG_BOOMERANG, Items.RG_PROGRESSIVE_HOOKSHOT]
        self.require_any_to_beat(items, Enemies.RE_MAD_SCRUB)
        self.require_all_to_beat([Items.RG_PROGRESSIVE_MAGIC_METER, Items.RG_DINS_FIRE], Enemies.RE_MAD_SCRUB)

    def test_deku_baba(self):
        """
        Checking if player can kill Deku Baba
        """
        items = [Items.RG_KOKIRI_SWORD, Items.RG_MASTER_SWORD, Items.RG_BIGGORON_SWORD, Items.RG_PROGRESSIVE_STICK_UPGRADE, Items.RG_MEGATON_HAMMER, Items.RG_PROGRESSIVE_BOMB_BAG, Items.RG_PROGRESSIVE_SLINGSHOT, Items.RG_PROGRESSIVE_BOW, Items.RG_BOOMERANG, Items.RG_PROGRESSIVE_HOOKSHOT]
        self.require_any_to_beat(items, Enemies.RE_DEKU_BABA)
        self.require_all_to_beat([Items.RG_PROGRESSIVE_MAGIC_METER, Items.RG_DINS_FIRE], Enemies.RE_DEKU_BABA)

    def test_blue_bubble(self):
        """
        Checking if player can kill Blue Bubble
        """
        items = [Items.RG_MEGATON_HAMMER, Items.RG_KOKIRI_SWORD, Items.RG_MASTER_SWORD, 
                 Items.RG_PROGRESSIVE_BOMB_BAG, Items.RG_PROGRESSIVE_BOW, Items.RG_PROGRESSIVE_SLINGSHOT]
        self.require_any_to_beat(items, Enemies.RE_BLUE_BUBBLE)

    def test_dead_hand(self):
        """
        Checking if player can kill Dead Hand
        """
        items = [Items.RG_KOKIRI_SWORD, Items.RG_MASTER_SWORD, Items.RG_BIGGORON_SWORD]
        self.require_any_to_beat(items, Enemies.RE_DEAD_HAND)

    def test_withered_deku_baba(self):
        """
        Checking if player can kill Withered Deku Baba
        """
        self.require_any_to_beat([Items.RG_KOKIRI_SWORD, Items.RG_MASTER_SWORD, Items.RG_BIGGORON_SWORD, Items.RG_BOOMERANG], Enemies.RE_WITHERED_DEKU_BABA)
        self.cannot_beat_with_any([Items.RG_PROGRESSIVE_STICK_UPGRADE, Items.RG_MEGATON_HAMMER, Items.RG_PROGRESSIVE_BOMB_BAG,
                                   Items.RG_PROGRESSIVE_SLINGSHOT, Items.RG_PROGRESSIVE_BOW, Items.RG_PROGRESSIVE_HOOKSHOT],
                                  Enemies.RE_WITHERED_DEKU_BABA)

    def test_like_like(self):
        """
        Checking if player can kill Like Like
        """
        items = [Items.RG_KOKIRI_SWORD, Items.RG_MASTER_SWORD, Items.RG_BIGGORON_SWORD, Items.RG_PROGRESSIVE_STICK_UPGRADE, Items.RG_MEGATON_HAMMER, Items.RG_PROGRESSIVE_BOMB_BAG, Items.RG_PROGRESSIVE_SLINGSHOT, Items.RG_PROGRESSIVE_BOW]
        self.require_any_to_beat(items, Enemies.RE_LIKE_LIKE)
        self.require_all_to_beat([Items.RG_PROGRESSIVE_MAGIC_METER, Items.RG_DINS_FIRE], Enemies.RE_LIKE_LIKE)
        self.cannot_beat_with_any([Items.RG_BOOMERANG, Items.RG_PROGRESSIVE_HOOKSHOT], Enemies.RE_LIKE_LIKE)

    def test_floormaster(self):
        """
        Checking if player can kill Floormaster
        """
        items = [Items.RG_KOKIRI_SWORD, Items.RG_MASTER_SWORD, Items.RG_BIGGORON_SWORD, Items.RG_PROGRESSIVE_STICK_UPGRADE, Items.RG_MEGATON_HAMMER, Items.RG_PROGRESSIVE_BOMB_BAG, Items.RG_PROGRESSIVE_SLINGSHOT, Items.RG_PROGRESSIVE_BOW]
        self.require_any_to_beat(items, Enemies.RE_FLOORMASTER)
        self.require_all_to_beat([Items.RG_PROGRESSIVE_MAGIC_METER, Items.RG_DINS_FIRE], Enemies.RE_FLOORMASTER)
        self.cannot_beat_with_any([Items.RG_BOOMERANG, Items.RG_PROGRESSIVE_HOOKSHOT], Enemies.RE_FLOORMASTER)

    def test_stalfos(self):
        """
        Checking if player can kill Stalfos
        """
        items = [Items.RG_KOKIRI_SWORD, Items.RG_MEGATON_HAMMER]
        self.require_any_to_beat(items, Enemies.RE_STALFOS, EnemyDistance.ED_SHORT_JUMPSLASH)
        self.require_all_to_beat([Items.RG_MASTER_SWORD], Enemies.RE_STALFOS, EnemyDistance.ED_MASTER_SWORD_JUMPSLASH)
        items = [Items.RG_BIGGORON_SWORD, Items.RG_PROGRESSIVE_STICK_UPGRADE]
        self.require_any_to_beat(items, Enemies.RE_STALFOS, EnemyDistance.ED_LONG_JUMPSLASH)
        self.require_all_to_beat([Items.RG_PROGRESSIVE_BOMB_BAG], Enemies.RE_STALFOS, EnemyDistance.ED_BOMB_THROW)
        self.require_all_to_beat([Items.RG_PROGRESSIVE_BOW], Enemies.RE_STALFOS, EnemyDistance.ED_FAR)

    def test_iron_knuckle(self):
        """
        Checking if player can kill Iron Knuckle
        """
        items = [Items.RG_KOKIRI_SWORD, Items.RG_MASTER_SWORD, Items.RG_BIGGORON_SWORD, Items.RG_MEGATON_HAMMER, Items.RG_PROGRESSIVE_BOMB_BAG]
        self.require_any_to_beat(items, Enemies.RE_IRON_KNUCKLE)

    def test_flare_dancer(self):
        """
        Checking if player can kill Flare Dancer
        """
        items = [Items.RG_MEGATON_HAMMER, Items.RG_PROGRESSIVE_HOOKSHOT]
        self.require_any_to_beat(items, Enemies.RE_FLARE_DANCER)
        self.require_all_to_beat([Items.RG_PROGRESSIVE_BOMB_BAG, Items.RG_KOKIRI_SWORD], Enemies.RE_FLARE_DANCER)
        self.require_all_to_beat([Items.RG_PROGRESSIVE_BOMB_BAG, Items.RG_PROGRESSIVE_BOW], Enemies.RE_FLARE_DANCER)
        self.require_all_to_beat([Items.RG_PROGRESSIVE_BOMB_BAG, Items.RG_PROGRESSIVE_SLINGSHOT], Enemies.RE_FLARE_DANCER)
        self.require_all_to_beat([Items.RG_PROGRESSIVE_BOMB_BAG, Items.RG_BOOMERANG], Enemies.RE_FLARE_DANCER)

    def test_wolfos(self):
        """
        Checking if player can kill Wolfos
        """
        items = [Items.RG_KOKIRI_SWORD, Items.RG_MASTER_SWORD, Items.RG_BIGGORON_SWORD, Items.RG_PROGRESSIVE_STICK_UPGRADE, 
                 Items.RG_MEGATON_HAMMER, Items.RG_PROGRESSIVE_BOW, Items.RG_PROGRESSIVE_SLINGSHOT, Items.RG_PROGRESSIVE_BOMB_BAG]
        self.require_any_to_beat(items, Enemies.RE_WOLFOS)
        self.require_all_to_beat([Items.RG_PROGRESSIVE_MAGIC_METER, Items.RG_DINS_FIRE], Enemies.RE_WOLFOS)

    def test_white_wolfos(self):
        """
        Checking if player can kill White Wolfos
        """
        items = [Items.RG_KOKIRI_SWORD, Items.RG_MASTER_SWORD, Items.RG_BIGGORON_SWORD, Items.RG_PROGRESSIVE_STICK_UPGRADE, 
                 Items.RG_MEGATON_HAMMER, Items.RG_PROGRESSIVE_BOW, Items.RG_PROGRESSIVE_SLINGSHOT, Items.RG_PROGRESSIVE_BOMB_BAG]
        self.require_any_to_beat(items, Enemies.RE_WHITE_WOLFOS)
        self.require_all_to_beat([Items.RG_PROGRESSIVE_MAGIC_METER, Items.RG_DINS_FIRE], Enemies.RE_WHITE_WOLFOS)

    def test_wallmaster(self):
        """
        Checking if player can kill Wallmaster
        """
        items = [Items.RG_KOKIRI_SWORD, Items.RG_MASTER_SWORD, Items.RG_BIGGORON_SWORD, Items.RG_PROGRESSIVE_STICK_UPGRADE, 
                 Items.RG_MEGATON_HAMMER, Items.RG_PROGRESSIVE_BOW, Items.RG_PROGRESSIVE_SLINGSHOT, Items.RG_PROGRESSIVE_BOMB_BAG]
        self.require_any_to_beat(items, Enemies.RE_WALLMASTER)
        self.require_all_to_beat([Items.RG_PROGRESSIVE_MAGIC_METER, Items.RG_DINS_FIRE], Enemies.RE_WALLMASTER)

    def test_armos(self):
        """
        Checking if player can kill Armos
        """
        items = [Items.RG_MASTER_SWORD, Items.RG_BIGGORON_SWORD, Items.RG_PROGRESSIVE_STICK_UPGRADE, Items.RG_MEGATON_HAMMER, 
                 Items.RG_PROGRESSIVE_BOMB_BAG, Items.RG_PROGRESSIVE_BOW]
        self.require_any_to_beat(items, Enemies.RE_ARMOS)

    def test_dinolfos(self):
        """
        Checking if player can kill Dinolfos
        """
        items = [Items.RG_KOKIRI_SWORD, Items.RG_MASTER_SWORD, Items.RG_BIGGORON_SWORD, Items.RG_PROGRESSIVE_SLINGSHOT, Items.RG_PROGRESSIVE_BOW]
        self.require_any_to_beat(items, Enemies.RE_DINOLFOS)

    def test_torch_slug(self):
        """
        Checking if player can kill Torch Slug
        """
        items = [Items.RG_KOKIRI_SWORD, Items.RG_MASTER_SWORD, Items.RG_BIGGORON_SWORD, Items.RG_PROGRESSIVE_STICK_UPGRADE, Items.RG_MEGATON_HAMMER, 
                 Items.RG_PROGRESSIVE_BOW]
        self.require_any_to_beat(items, Enemies.RE_TORCH_SLUG)
        self.require_all_to_beat([Items.RG_PROGRESSIVE_BOMB_BAG], Enemies.RE_TORCH_SLUG)

    def test_freezard(self):
        """
        Checking if player can kill Freezard
        """
        items = [Items.RG_MASTER_SWORD, Items.RG_BIGGORON_SWORD, Items.RG_MEGATON_HAMMER, Items.RG_PROGRESSIVE_STICK_UPGRADE, 
                 Items.RG_PROGRESSIVE_HOOKSHOT, Items.RG_PROGRESSIVE_BOMB_BAG]
        self.require_any_to_beat(items, Enemies.RE_FREEZARD)
        self.require_all_to_beat([Items.RG_PROGRESSIVE_MAGIC_METER, Items.RG_DINS_FIRE], Enemies.RE_FREEZARD)
        self.require_all_to_beat([Items.RG_PROGRESSIVE_BOW, Items.RG_PROGRESSIVE_MAGIC_METER, Items.RG_FIRE_ARROWS], Enemies.RE_FREEZARD)

    def test_shell_blade(self):
        """
        Checking if player can kill Shell Blade
        """
        items = [Items.RG_KOKIRI_SWORD, Items.RG_MASTER_SWORD, Items.RG_BIGGORON_SWORD, Items.RG_PROGRESSIVE_STICK_UPGRADE, 
                 Items.RG_MEGATON_HAMMER, Items.RG_PROGRESSIVE_BOMB_BAG]
        self.require_any_to_beat(items, Enemies.RE_SHELL_BLADE)
        self.require_all_to_beat([Items.RG_PROGRESSIVE_MAGIC_METER, Items.RG_DINS_FIRE], Enemies.RE_FREEZARD)
        self.require_all_to_beat([Items.RG_PROGRESSIVE_BOW, Items.RG_PROGRESSIVE_MAGIC_METER, Items.RG_FIRE_ARROWS], Enemies.RE_FREEZARD)

    def test_spike(self):
        """
        Checking if player can kill Spike
        """
        items = [Items.RG_MASTER_SWORD, Items.RG_BIGGORON_SWORD, Items.RG_MEGATON_HAMMER, Items.RG_PROGRESSIVE_STICK_UPGRADE, 
                 Items.RG_PROGRESSIVE_HOOKSHOT, Items.RG_PROGRESSIVE_BOW, Items.RG_PROGRESSIVE_BOMB_BAG]
        self.require_any_to_beat(items, Enemies.RE_SPIKE)
        self.require_all_to_beat([Items.RG_PROGRESSIVE_MAGIC_METER, Items.RG_DINS_FIRE], Enemies.RE_SPIKE)

    def test_stinger(self):
        """
        Checking if player can kill Stinger
        """
        items = [Items.RG_KOKIRI_SWORD, Items.RG_MASTER_SWORD, Items.RG_BIGGORON_SWORD, Items.RG_PROGRESSIVE_STICK_UPGRADE, 
                 Items.RG_MEGATON_HAMMER, Items.RG_PROGRESSIVE_SLINGSHOT, Items.RG_PROGRESSIVE_BOW, Items.RG_PROGRESSIVE_BOMB_BAG, 
                 Items.RG_PROGRESSIVE_HOOKSHOT]
        self.require_any_to_beat(items, Enemies.RE_STINGER)

    def test_big_octo(self):
        """
        Checking if player can kill Big Octo
        """
        items = [Items.RG_KOKIRI_SWORD, Items.RG_MASTER_SWORD, Items.RG_PROGRESSIVE_STICK_UPGRADE]
        self.require_any_to_beat(items, Enemies.RE_BIG_OCTO)

    def test_dark_link(self):
        """
        Checking if player can kill Dark Link
        """
        items = [Items.RG_KOKIRI_SWORD, Items.RG_MASTER_SWORD, Items.RG_BIGGORON_SWORD]
        self.require_any_to_beat(items, Enemies.RE_DARK_LINK)
        self.require_all_to_beat([Items.RG_BOOMERANG, Items.RG_PROGRESSIVE_BOW], Enemies.RE_DARK_LINK)

    def test_anubis(self):
        """
        Checking if player can kill Anubis
        """
        self.require_all_to_beat([Items.RG_PROGRESSIVE_MAGIC_METER, Items.RG_DINS_FIRE], Enemies.RE_ANUBIS)
        self.require_all_to_beat([Items.RG_PROGRESSIVE_BOW, Items.RG_PROGRESSIVE_MAGIC_METER, Items.RG_FIRE_ARROWS], Enemies.RE_ANUBIS)

    def test_beamos(self):
        """
        Checking if player can kill Beamos
        """
        items = [Items.RG_PROGRESSIVE_BOMB_BAG]
        self.require_any_to_beat(items, Enemies.RE_BEAMOS)

    def test_purple_leever(self):
        """
        Checking if player can kill Purple Leever
        """
        items = [Items.RG_MASTER_SWORD, Items.RG_BIGGORON_SWORD]
        self.require_any_to_beat(items, Enemies.RE_PURPLE_LEEVER)

    def test_tentacle(self):
        """
        Checking if player can kill Tentacle
        """
        self.require_all_to_beat([Items.RG_BOOMERANG], Enemies.RE_TENTACLE)

    def test_bari(self):
        """
        Checking if player can kill Bari
        """
        items = [Items.RG_PROGRESSIVE_HOOKSHOT, Items.RG_BOOMERANG, Items.RG_PROGRESSIVE_BOW, Items.RG_PROGRESSIVE_STICK_UPGRADE, 
                 Items.RG_MEGATON_HAMMER, Items.RG_PROGRESSIVE_BOMB_BAG]
        self.require_any_to_beat(items, Enemies.RE_BARI)
        self.require_all_to_beat([Items.RG_PROGRESSIVE_MAGIC_METER, Items.RG_DINS_FIRE], Enemies.RE_BARI)

    def test_shabom(self):
        """
        Checking if player can kill Shabom
        """
        items = [Items.RG_BOOMERANG, Items.RG_PROGRESSIVE_NUT_UPGRADE, Items.RG_KOKIRI_SWORD, Items.RG_MASTER_SWORD, Items.RG_BIGGORON_SWORD, Items.RG_PROGRESSIVE_STICK_UPGRADE, Items.RG_MEGATON_HAMMER]
        self.require_any_to_beat(items, Enemies.RE_SHABOM, quantity=4)
        self.require_all_to_beat([Items.RG_PROGRESSIVE_MAGIC_METER, Items.RG_DINS_FIRE], Enemies.RE_SHABOM, quantity=4)
        self.require_all_to_beat([Items.RG_PROGRESSIVE_BOW, Items.RG_PROGRESSIVE_MAGIC_METER, Items.RG_ICE_ARROWS], Enemies.RE_SHABOM, quantity=4)

    def test_octorok(self):
        """
        Checking if player can kill Octorok
        """
        items = [Items.RG_DEKU_SHIELD, Items.RG_HYLIAN_SHIELD, Items.RG_PROGRESSIVE_HOOKSHOT, Items.RG_BOOMERANG, Items.RG_PROGRESSIVE_BOW, Items.RG_PROGRESSIVE_SLINGSHOT, Items.RG_PROGRESSIVE_BOMB_BAG, Items.RG_BOMBCHU_5]
        self.require_any_to_beat(items, Enemies.RE_OCTOROK)

    def test_redead(self):
        """
        Checking if player can kill ReDead
        """
        items = [Items.RG_KOKIRI_SWORD, Items.RG_MASTER_SWORD, Items.RG_BIGGORON_SWORD]
        self.require_any_to_beat(items, Enemies.RE_REDEAD)
        self.require_all_to_beat([Items.RG_PROGRESSIVE_MAGIC_METER, Items.RG_DINS_FIRE], Enemies.RE_REDEAD)

    def test_meg(self):
        """
        Checking if player can kill Meg
        """
        items = [Items.RG_PROGRESSIVE_BOW, Items.RG_PROGRESSIVE_HOOKSHOT, Items.RG_PROGRESSIVE_BOMB_BAG]
        self.require_any_to_beat(items, Enemies.RE_MEG)

    def test_green_bubble(self):
        """
        Checking if player can kill Green Bubble (Ship: jumpslash, bow, slingshot or explosives)
        """
        items = [Items.RG_KOKIRI_SWORD, Items.RG_MASTER_SWORD, Items.RG_BIGGORON_SWORD, Items.RG_PROGRESSIVE_STICK_UPGRADE, Items.RG_MEGATON_HAMMER, Items.RG_PROGRESSIVE_BOMB_BAG, Items.RG_PROGRESSIVE_BOW, Items.RG_PROGRESSIVE_SLINGSHOT]
        self.require_any_to_beat(items, Enemies.RE_GREEN_BUBBLE)
        self.cannot_beat_with_any([Items.RG_BOOMERANG, Items.RG_PROGRESSIVE_HOOKSHOT], Enemies.RE_GREEN_BUBBLE)

    def test_gerudo_warrior(self):
        """
        Checking if player can kill Gerudo Warrior
        """
        items = [Items.RG_KOKIRI_SWORD, Items.RG_MASTER_SWORD, Items.RG_BIGGORON_SWORD, Items.RG_PROGRESSIVE_BOW]
        self.require_any_to_beat(items, Enemies.RE_GERUDO_WARRIOR)

    def test_gibdo(self):
        """
        Checking if player can kill Gibdo
        """
        items = [Items.RG_KOKIRI_SWORD, Items.RG_MASTER_SWORD, Items.RG_BIGGORON_SWORD]
        self.require_any_to_beat(items, Enemies.RE_GIBDO)
        self.require_all_to_beat([Items.RG_PROGRESSIVE_MAGIC_METER, Items.RG_DINS_FIRE], Enemies.RE_GIBDO)


# Can Kill Bosses
class TestCanKillBoss(KillBase):
    """
    Testing to see if we can kill all the bosses without boss souls on
    """
    options = {"shuffle_boss_souls": 0, "closed_forest": 2, "door_of_time": 2}
    world: SohWorld

    def test_queen_gohma(self):
        """
        Checking if player can kill Queen Ghoma
        """
        items = []

        if self.options["shuffle_boss_souls"]  >= 1:
            items.append(Items.RG_GOHMA_SOUL)

        self.require_all_to_beat(items, Enemies.RE_GOHMA)

    def test_king_dodongo(self):
        """
        Checking if player can kill King Dodongo
        """
        items = [Items.RG_PROGRESSIVE_BOMB_BAG]

        if self.options["shuffle_boss_souls"]  >= 1:
            items.append(Items.RG_KING_DODONGO_SOUL)

        self.require_all_to_beat(items, Enemies.RE_KING_DODONGO)

    def test_barinade(self):
        """
        Checking if player can kill Barinade
        """
        items = [Items.RG_BOOMERANG]

        if self.options["shuffle_boss_souls"]  >= 1:
            items.append(Items.RG_BARINADE_SOUL)

        self.require_all_to_beat(items, Enemies.RE_BARINADE)

    def test_phantom_ganon(self):
        """
        Checking if player can kill Phantom Ganon
        """
        items = [Items.RG_PROGRESSIVE_HOOKSHOT]

        if self.options["shuffle_boss_souls"]  >= 1:
            items.append(Items.RG_PHANTOM_GANON_SOUL)

        self.require_all_to_beat(items, Enemies.RE_PHANTOM_GANON)

    def test_volvagia(self):
        """
        Checking if player can kill Volvagia
        """
        items = [Items.RG_MEGATON_HAMMER]

        if self.options["shuffle_boss_souls"]  >= 1:
            items.append(Items.RG_VOLVAGIA_SOUL)

        self.require_all_to_beat(items, Enemies.RE_VOLVAGIA)

    def test_morpha(self):
        """
        Checking if player can kill Morpha
        """
        items = [Items.RG_PROGRESSIVE_HOOKSHOT]

        if self.options["shuffle_boss_souls"]  >= 1:
            items.append(Items.RG_MORPHA_SOUL)

        self.require_all_to_beat(items, Enemies.RE_MORPHA)

    def test_bongo_bongo(self):
        """
        Checking if player can kill Bongo Bongo
        """
        items = [Items.RG_PROGRESSIVE_HOOKSHOT, Items.RG_LENS_OF_TRUTH, Items.RG_PROGRESSIVE_MAGIC_METER]

        if self.options["shuffle_boss_souls"]  >= 1:
            items.append(Items.RG_BONGO_BONGO_SOUL)

        self.require_all_to_beat(items, Enemies.RE_BONGO_BONGO)

    def test_twinrova(self):
        """
        Checking if player can kill Twinrova
        """
        items = [Items.RG_MIRROR_SHIELD]

        if self.options["shuffle_boss_souls"]  >= 1:
            items.append(Items.RG_TWINROVA_SOUL)

        self.require_all_to_beat(items, Enemies.RE_TWINROVA)

    def test_ganondorf(self):
        """
        Checking if player can kill Ganondorf
        """
        items = [Items.RG_PROGRESSIVE_MAGIC_METER, Items.RG_LIGHT_ARROWS, Items.RG_PROGRESSIVE_BOW]

        if self.options["shuffle_boss_souls"] == 2:
            items.append(Items.RG_GANON_SOUL)

        self.require_all_to_beat(items, Enemies.RE_GANONDORF)

    def test_ganon(self):
        """
        Checking if player can kill Ganon
        """
        items = []

        if self.options["shuffle_boss_souls"] == 2:
            items.append(Items.RG_GANON_SOUL)

        self.require_all_to_beat(items, Enemies.RE_GANON)        
        
# Derivative of without boss soul test
class TestAccessCanKillBossWithSoul(TestCanKillBoss):
    """
    Testing to see if we can kill all the bosses with boss souls on
    """
    options = {"shuffle_boss_souls": 1, "closed_forest": 2, "door_of_time": 2, "jabu_jabu": 1, "zoras_fountain": 2, "sleeping_waterfall": 1,"small_key_shuffle": 5, "boss_key_shuffle": 5, "key_rings": 1, "key_rings_count": 9,
               "shuffle_songs": 3}
    world: SohWorld

# Derivative of without boss soul test with ganons soul
class TestAccessCanKillBossWithSoulPlus(TestCanKillBoss):
    """
    Testing to see if we can kill all the bosses with boss souls on
    """
    options = {"shuffle_boss_souls": 2, "closed_forest": 2, "door_of_time": 2, "jabu_jabu": 1, "zoras_fountain": 2, "sleeping_waterfall": 1,"small_key_shuffle": 5, "boss_key_shuffle": 5, "key_rings": 1, "key_rings_count": 9,
               "shuffle_songs": 3}
    world: SohWorld