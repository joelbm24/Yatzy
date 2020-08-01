import unittest
from dice import Dice
from scorecard import Scorecard

class Helpers():
    def makeDiceFromList(self, dice, values):
        for i in range(5):
            dice.dice[i].value = values[i]

        return dice
        
class TestDiceMethods(unittest.TestCase):
    def setUp(self):
        self.helpers = Helpers()
        self.dice = Dice()
    
    def test_three_of_a_kind(self):
        test_values = [1,2,1,3,1]
        self.dice = self.helpers.makeDiceFromList(self.dice, test_values)
        self.assertEqual(self.dice.checkThreeOfAKind(), True)
        
        test_values = [1,2,1,3,5]
        self.dice = self.helpers.makeDiceFromList(self.dice, test_values)
        self.assertEqual(self.dice.checkThreeOfAKind(), False)

    def test_four_of_a_kind(self):
        test_values = [1,2,2,2,2]
        self.dice = self.helpers.makeDiceFromList(self.dice, test_values)
        self.assertEqual(self.dice.checkFourOfAKind(), True)
        
        test_values = [1,6,2,2,2]
        self.dice = self.helpers.makeDiceFromList(self.dice, test_values)
        self.assertEqual(self.dice.checkFourOfAKind(), False)

    def test_full_house(self):
        test_values = [1,1,2,2,2]
        self.dice = self.helpers.makeDiceFromList(self.dice, test_values)
        self.assertEqual(self.dice.checkFullHouse(), True)
        
        test_values = [1,1,2,1,1]
        self.dice = self.helpers.makeDiceFromList(self.dice, test_values)
        self.assertEqual(self.dice.checkFullHouse(), False)

    def test_large_straight(self):
        test_values = [1,2,3,4,5]
        self.dice = self.helpers.makeDiceFromList(self.dice, test_values)
        self.assertEqual(self.dice.checkLargeStraight(), True)


    def test_small_straight(self):
        test_values = [1,2,3,4,6]
        self.dice = self.helpers.makeDiceFromList(self.dice, test_values)
        self.assertEqual(self.dice.checkSmallStraight(), True)


class TestScorecardMethods(unittest.TestCase):
    def setUp(self):
        self.helpers = Helpers()
        self.dice = Dice()
        self.scorecard = Scorecard()

    def test_lowercard(self):
        test_values = [1,2,3,4,2]
        self.dice = self.helpers.makeDiceFromList(self.dice, test_values)

        possible_card = self.scorecard.getPossibleLowerCard(self.dice)

        self.assertEqual(possible_card["aces"], 1)
        self.assertEqual(possible_card["twos"], 4)
        self.assertEqual(possible_card["threes"], 3)
        self.assertEqual(possible_card["fours"], 4)

if __name__ == "__main__":
    unittest.main()
