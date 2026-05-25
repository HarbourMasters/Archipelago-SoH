from .. import SohWorld
from ..Options import *
from ..Items import Items, SohItem
from ..Enums import Tricks
from .bases import SohTestBase
from ..LogicHelpers import fire_timer_at_least, water_timer_at_least
from itertools import combinations

class TestFireTimerWithoutTrick(SohTestBase):
    options = {"starting_hearts": 1}

    def test_tunic_requirement(self):
        self.sweep()
        self.assertFalse(fire_timer_at_least(self.get_bundle(), 255)._instantiate(self.world)._evaluate(self.multiworld.state), "The fire timer should be really low when you only have 1 heart and no tunic")
        self.collect(self.create_item(Items.GORON_TUNIC))
        self.assertTrue(fire_timer_at_least(self.get_bundle(), 255)._instantiate(self.world)._evaluate(self.multiworld.state), "The fire timer should be maxed out if you have the tunic")

    def test_heart_requirement(self):
        self.sweep()
        self.assertFalse(fire_timer_at_least(self.get_bundle(), 0)._instantiate(self.world)._evaluate(self.multiworld.state), "Without the fewer tunic requirement trick the fire timer is never True without a tunic")
        self.assertFalse(fire_timer_at_least(self.get_bundle(), 1)._instantiate(self.world)._evaluate(self.multiworld.state), "Without the fewer tunic requirement trick the fire timer is never True without a tunic")
        self.collect(self.create_item(Items.HEART_CONTAINER))
        self.assertFalse(fire_timer_at_least(self.get_bundle(), 0)._instantiate(self.world)._evaluate(self.multiworld.state), "Without the fewer tunic requirement trick the fire timer is never True without a tunic, even after collecting more hearts")
        self.assertFalse(fire_timer_at_least(self.get_bundle(), 1)._instantiate(self.world)._evaluate(self.multiworld.state), "Without the fewer tunic requirement trick the fire timer is never True without a tunic, even after collecting more hearts")

class TestFireTimerWithTrick(SohTestBase):
    options = {"starting_hearts": 1,
               "tricks_in_logic": {Tricks.FEWER_TUNIC_REQUIREMENTS}}
    
    def test_tunic_requirement(self):
        self.sweep()
        self.assertFalse(fire_timer_at_least(self.get_bundle(), 255)._instantiate(self.world)._evaluate(self.multiworld.state), "The fire timer should be really low when you only have 1 heart and no tunic")
        self.collect(self.create_item(Items.GORON_TUNIC))
        self.assertTrue(fire_timer_at_least(self.get_bundle(), 255)._instantiate(self.world)._evaluate(self.multiworld.state), "The fire timer should be maxed out if you have the tunic")

    def test_heart_requirement(self):
        self.sweep()
        self.assertTrue(fire_timer_at_least(self.get_bundle(), 0)._instantiate(self.world)._evaluate(self.multiworld.state), "With 1 heart fire timer should always be higher than 0")
        self.assertTrue(fire_timer_at_least(self.get_bundle(), 7)._instantiate(self.world)._evaluate(self.multiworld.state), "With 1 heart fire timer should at least be higher than 7")
        self.assertTrue(fire_timer_at_least(self.get_bundle(), 8)._instantiate(self.world)._evaluate(self.multiworld.state), "With 1 heart fire timer should be exaclty 8")
        self.assertFalse(fire_timer_at_least(self.get_bundle(), 9)._instantiate(self.world)._evaluate(self.multiworld.state), "With 1 heart fire timer should not be higher than 9")

        self.collect(self.create_item(Items.HEART_CONTAINER))
        self.assertTrue(fire_timer_at_least(self.get_bundle(), 0)._instantiate(self.world)._evaluate(self.multiworld.state), "With 2 hearts fire timer should always be higher than 0")
        self.assertTrue(fire_timer_at_least(self.get_bundle(), 15)._instantiate(self.world)._evaluate(self.multiworld.state), "With 2 hearts fire timer should at least be higher than 15")
        self.assertTrue(fire_timer_at_least(self.get_bundle(), 16)._instantiate(self.world)._evaluate(self.multiworld.state), "With 2 hearts fire timer should be exaclty 16")
        self.assertFalse(fire_timer_at_least(self.get_bundle(), 17)._instantiate(self.world)._evaluate(self.multiworld.state), "With 2 hearts fire timer should not be higher than 17")

        self.collect(self.create_item(Items.PIECE_OF_HEART))
        self.assertFalse(fire_timer_at_least(self.get_bundle(), 17)._instantiate(self.world)._evaluate(self.multiworld.state), "A heart container does not give you extra time")

class TestWaterTimerWithoutTrick(SohTestBase):
    options = {"starting_hearts": 1}

    def test_tunic_requirement(self):
        self.sweep()
        self.assertFalse(water_timer_at_least(self.get_bundle(), 255)._instantiate(self.world)._evaluate(self.multiworld.state), "The water timer should be really low when you only have 1 heart and no tunic")
        self.collect(self.create_item(Items.ZORA_TUNIC))
        self.assertTrue(water_timer_at_least(self.get_bundle(), 255)._instantiate(self.world)._evaluate(self.multiworld.state), "The water timer should be maxed out if you have the tunic")

    def test_heart_requirement(self):
        self.sweep()
        self.assertFalse(water_timer_at_least(self.get_bundle(), 0)._instantiate(self.world)._evaluate(self.multiworld.state), "Without the fewer tunic requirement trick the water timer is never True without a tunic")
        self.assertFalse(water_timer_at_least(self.get_bundle(), 1)._instantiate(self.world)._evaluate(self.multiworld.state), "Without the fewer tunic requirement trick the water timer is never True without a tunic")
        self.collect(self.create_item(Items.HEART_CONTAINER))
        self.assertFalse(water_timer_at_least(self.get_bundle(), 0)._instantiate(self.world)._evaluate(self.multiworld.state), "Without the fewer tunic requirement trick the water timer is never True without a tunic, even after collecting more hearts")
        self.assertFalse(water_timer_at_least(self.get_bundle(), 1)._instantiate(self.world)._evaluate(self.multiworld.state), "Without the fewer tunic requirement trick the water timer is never True without a tunic, even after collecting more hearts")

class TestWaterTimerWithTrick(SohTestBase):
    options = {"starting_hearts": 1,
               "tricks_in_logic": {Tricks.FEWER_TUNIC_REQUIREMENTS}}
    
    def test_tunic_requirement(self):
        self.sweep()
        self.assertFalse(water_timer_at_least(self.get_bundle(), 255)._instantiate(self.world)._evaluate(self.multiworld.state), "The water timer should be really low when you only have 1 heart and no tunic")
        self.collect(self.create_item(Items.ZORA_TUNIC))
        self.assertTrue(water_timer_at_least(self.get_bundle(), 255)._instantiate(self.world)._evaluate(self.multiworld.state), "The water timer should be maxed out if you have the tunic")

    def test_heart_requirement(self):
        self.sweep()
        self.assertTrue(water_timer_at_least(self.get_bundle(), 0)._instantiate(self.world)._evaluate(self.multiworld.state), "With 1 heart water timer should always be higher than 0")
        self.assertTrue(water_timer_at_least(self.get_bundle(), 7)._instantiate(self.world)._evaluate(self.multiworld.state), "With 1 heart water timer should at least be higher than 7")
        self.assertTrue(water_timer_at_least(self.get_bundle(), 8)._instantiate(self.world)._evaluate(self.multiworld.state), "With 1 heart water timer should be exaclty 8")
        self.assertFalse(water_timer_at_least(self.get_bundle(), 9)._instantiate(self.world)._evaluate(self.multiworld.state), "With 1 heart water timer should not be higher than 9")

        self.collect(self.create_item(Items.HEART_CONTAINER))
        self.assertTrue(water_timer_at_least(self.get_bundle(), 0)._instantiate(self.world)._evaluate(self.multiworld.state), "With 2 hearts water timer should always be higher than 0")
        self.assertTrue(water_timer_at_least(self.get_bundle(), 15)._instantiate(self.world)._evaluate(self.multiworld.state), "With 2 hearts water timer should at least be higher than 15")
        self.assertTrue(water_timer_at_least(self.get_bundle(), 16)._instantiate(self.world)._evaluate(self.multiworld.state), "With 2 hearts water timer should be exaclty 16")
        self.assertFalse(water_timer_at_least(self.get_bundle(), 17)._instantiate(self.world)._evaluate(self.multiworld.state), "With 2 hearts water timer should not be higher than 17")

        self.collect(self.create_item(Items.PIECE_OF_HEART))
        self.assertFalse(water_timer_at_least(self.get_bundle(), 17)._instantiate(self.world)._evaluate(self.multiworld.state), "A heart container does not give you extra time")
