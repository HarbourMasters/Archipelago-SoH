from .. import SohWorld
from ..Items import Items
from .bases import SohTestBase
from BaseClasses import ItemClassification as IC


class TestHearts(SohTestBase):
    world: SohWorld

    def test_heart_counts(self):
        # note that tests don't care if something is progression, since we manually collect
        # it doesn't actually matter whether the heart pieces are useful or prog for this test
        self.assertTrue(self.multiworld.state.soh_heart_count[self.player] == 3)  # type: ignore

        self.collect(self.world.create_item(Items.HEART_CONTAINER))
        self.assertTrue(self.multiworld.state.soh_heart_count[self.player] == 4)  # type: ignore

        for _ in range(3):
            self.collect(self.world.create_item(Items.PIECE_OF_HEART))
        self.assertTrue(self.multiworld.state.soh_heart_count[self.player] == 4)  # type: ignore

        heart = self.world.create_item(Items.HEART_CONTAINER)
        self.collect(heart)
        self.assertTrue(self.multiworld.state.soh_heart_count[self.player] == 5)  # type: ignore

        heart_piece = self.world.create_item(Items.PIECE_OF_HEART)
        self.collect(heart_piece)
        self.assertTrue(self.multiworld.state.soh_heart_count[self.player] == 6)  # type: ignore

        self.remove(heart_piece)
        self.assertTrue(self.multiworld.state.soh_heart_count[self.player] == 5)  # type: ignore

        self.remove(heart)
        self.assertTrue(self.multiworld.state.soh_heart_count[self.player] == 4)  # type: ignore

class TestHeartsBalanced(SohTestBase):
    options = {"starting_hearts": 1, "item_pool": "balanced"}
    def test_collecting_all_hearts_count(self):
        self.assertEqual(self.multiworld.state.soh_heart_count[self.player], 1, "start with 1 heart") # type: ignore 
        self.collect_by_name([Items.PIECE_OF_HEART, Items.PIECE_OF_HEART_WINNER, Items.HEART_CONTAINER])
        self.assertEqual(self.multiworld.state.soh_heart_count[self.player], 20, "after collecting all heart pieces and containers we should have 20 hearts") # type: ignore 

    def test_count_hearts_progression(self):
        poh = list()
        winner = list()
        container = list()
        for item in self.multiworld.itempool:
            if item.name == Items.PIECE_OF_HEART and (item.classification & IC.progression) == IC.progression:
                poh.append(item)
            if item.name == Items.PIECE_OF_HEART_WINNER and (item.classification & IC.progression) == IC.progression:
                winner.append(item)    
            if item.name == Items.HEART_CONTAINER and (item.classification & IC.progression) == IC.progression:
                container.append(item)    
        self.assertEqual(len(poh), 0, "Should have been 0 PoH")
        self.assertEqual(len(winner), 0, "Should have been 0 Winner PoH")
        self.assertEqual(len(container), 2, "Should have been 2 Containers")

    def test_count_heart_total(self):
        poh = list()
        winner = list()
        container = list()
        for item in self.multiworld.itempool:
            if item.name == Items.PIECE_OF_HEART:
                poh.append(item)
            if item.name == Items.PIECE_OF_HEART_WINNER:
                winner.append(item)    
            if item.name == Items.HEART_CONTAINER:
                container.append(item)   
        self.assertEqual(len(poh), 39, "Should have been 39 PoH")
        self.assertEqual(len(winner), 1, "Should have been 1 Winner PoH")
        self.assertEqual(len(container), 9, "Should have been 9 Containers")

class TestHeartsMinimal(SohTestBase):
    options = {"starting_hearts": 1, "item_pool": "minimal"}
    def test_collecting_all_hearts_count(self):
        self.assertEqual(self.multiworld.state.soh_heart_count[self.player], 1, "start with 1 heart") # type: ignore 
        self.collect_by_name([Items.PIECE_OF_HEART, Items.PIECE_OF_HEART_WINNER, Items.HEART_CONTAINER])
        self.assertEqual(self.multiworld.state.soh_heart_count[self.player], 3, "after collecting all heart pieces and containers we should have 3 hearts") # type: ignore 

    def test_count_hearts_progression(self):
        poh = list()
        winner = list()
        container = list()
        for item in self.multiworld.itempool:
            if item.name == Items.PIECE_OF_HEART and (item.classification & IC.progression) == IC.progression:
                poh.append(item)
            if item.name == Items.PIECE_OF_HEART_WINNER and (item.classification & IC.progression) == IC.progression:
                winner.append(item)
            if item.name == Items.HEART_CONTAINER and (item.classification & IC.progression) == IC.progression:
                container.append(item)    
        self.assertEqual(len(poh), 3, "Should have been 3 PoH")
        self.assertEqual(len(winner), 1, "Should have been 1 Winner PoH")
        self.assertEqual(len(container), 1, "Should have been 1 Containers")


    def test_count_heart_total(self):
        poh = list()
        winner = list()
        container = list()
        for item in self.multiworld.itempool:
            if item.name == Items.PIECE_OF_HEART:
                poh.append(item)
            if item.name == Items.PIECE_OF_HEART_WINNER:
                winner.append(item)    
            if item.name == Items.HEART_CONTAINER:
                container.append(item)   
        self.assertEqual(len(container), 1, "Should have been 0 Containers")
        self.assertEqual(len(poh), 3, "Should have been 3 PoH")
        self.assertEqual(len(winner), 1, "Should have been 1 Winner PoH")

class TestHeartsScarce(SohTestBase):
    options = {"starting_hearts": 1, "item_pool": "scarce"}
    def test_collecting_all_hearts_count(self):
        self.assertEqual(self.multiworld.state.soh_heart_count[self.player], 1, "start with 1 heart") # type: ignore 
        self.collect_by_name([Items.PIECE_OF_HEART, Items.PIECE_OF_HEART_WINNER, Items.HEART_CONTAINER])
        self.assertEqual(self.multiworld.state.soh_heart_count[self.player], 12, "after collecting all heart pieces and containers we should have 12 hearts") # type: ignore 

    def test_count_hearts_progression(self):
        poh = list()
        winner = list()
        container = list()
        for item in self.multiworld.itempool:
            if item.name == Items.PIECE_OF_HEART and (item.classification & IC.progression) == IC.progression:
                poh.append(item)
            if item.name == Items.PIECE_OF_HEART_WINNER and (item.classification & IC.progression) == IC.progression:
                winner.append(item)    
            if item.name == Items.HEART_CONTAINER and (item.classification & IC.progression) == IC.progression:
                container.append(item)   
        self.assertEqual(len(poh), 8, "Should have been 8 PoH")
        self.assertEqual(len(winner), 0, "Should have been 0 Winner PoH")
        self.assertEqual(len(container), 0, "Should have been 0 Containers")

    def test_count_heart_total(self):
        poh = list()
        winner = list()
        container = list()
        for item in self.multiworld.itempool:
            if item.name == Items.PIECE_OF_HEART:
                poh.append(item)
            if item.name == Items.PIECE_OF_HEART_WINNER:
                winner.append(item)    
            if item.name == Items.HEART_CONTAINER:
                container.append(item)   
        self.assertEqual(len(container), 0, "Should have been 0 Containers")
        self.assertEqual(len(poh), 43, "Should have been 43 PoH")
        self.assertEqual(len(winner), 1, "Should have been 1 Winner PoH")

class TestHeartsPlentiful(SohTestBase):
    options = {"starting_hearts": 1, "item_pool": "plentiful"}
    def test_collecting_all_hearts_count(self):
        self.assertEqual(self.multiworld.state.soh_heart_count[self.player], 1, "start with 1 heart") # type: ignore 
        self.collect_by_name([Items.PIECE_OF_HEART, Items.PIECE_OF_HEART_WINNER, Items.HEART_CONTAINER])
        self.assertEqual(self.multiworld.state.soh_heart_count[self.player], 20, "after collecting all heart pieces and containers we should have 20 hearts") # type: ignore 

    def test_count_hearts_progression(self):
        poh = list()
        winner = list()
        container = list()
        for item in self.multiworld.itempool:
            if item.name == Items.PIECE_OF_HEART and (item.classification & IC.progression) == IC.progression:
                poh.append(item)
            if item.name == Items.PIECE_OF_HEART_WINNER and (item.classification & IC.progression) == IC.progression:
                winner.append(item)    
            if item.name == Items.HEART_CONTAINER and (item.classification & IC.progression) == IC.progression:
                container.append(item)    
        self.assertEqual(len(poh), 0, "Should have been 0 PoH")
        self.assertEqual(len(winner), 0, "Should have been 0 Winner PoH")
        self.assertEqual(len(container), 2, "Should have been 2 Containers")

    def test_count_heart_total(self):
        poh = list()
        winner = list()
        container = list()
        for item in self.multiworld.itempool:
            if item.name == Items.PIECE_OF_HEART:
                poh.append(item)
            if item.name == Items.PIECE_OF_HEART_WINNER:
                winner.append(item)    
            if item.name == Items.HEART_CONTAINER:
                container.append(item)   
        self.assertEqual(len(poh), 3, "Should have been 3 PoH")
        self.assertEqual(len(winner), 1, "Should have been 1 Winner PoH")
        self.assertEqual(len(container), 18, "Should have been 18 Containers")