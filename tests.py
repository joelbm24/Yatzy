import unittest
from lib.dice import Dice
from lib.scorecard import Scorecard

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

        test_values = [1,2,1,1,1]
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

    def test_yahtzee(self):
        test_values = [1,1,1,1,1]
        self.dice = self.helpers.makeDiceFromList(self.dice, test_values)
        self.assertEqual(self.dice.checkYahtzee(), True)

class TestScorecardMethods(unittest.TestCase):
    def setUp(self):
        self.helpers = Helpers()
        self.dice = Dice()
        self.scorecard = Scorecard()
    
    def test_lower(self):
        test_values = [1,1,2,2,6]
        self.dice = self.helpers.makeDiceFromList(self.dice, test_values)
        lower_card = self.scorecard.scoreLower(self.dice)
        self.assertEqual(lower_card["aces"], 2)
        self.assertEqual(lower_card["twos"], 4)
        self.assertEqual(lower_card["sixes"], 6)

    def test_upper(self):
        test_values = [2,2,2,5,5]
        self.dice = self.helpers.makeDiceFromList(self.dice, test_values)
        upper_card = self.scorecard.scoreUpper(self.dice)
        self.assertEqual(upper_card["full"], 25)

        test_values = [1,2,3,4,5]
        self.dice = self.helpers.makeDiceFromList(self.dice, test_values)
        upper_card = self.scorecard.scoreUpper(self.dice)
        self.assertEqual(upper_card["large"], 40)

        test_values = [3,5,4,1,6]
        self.dice = self.helpers.makeDiceFromList(self.dice, test_values)
        upper_card = self.scorecard.scoreUpper(self.dice)
        self.assertEqual(upper_card["small"], 30)

        test_values = [3,3,2,1,4]
        self.dice = self.helpers.makeDiceFromList(self.dice, test_values)
        upper_card = self.scorecard.scoreUpper(self.dice)
        self.assertEqual(upper_card["small"], 30)

        test_values = [2,2,2,3,4]
        self.dice = self.helpers.makeDiceFromList(self.dice, test_values)
        upper_card = self.scorecard.scoreUpper(self.dice)
        self.assertEqual(upper_card["triples"], 13)

        test_values = [2,2,2,2,2]
        self.dice = self.helpers.makeDiceFromList(self.dice, test_values)
        upper_card = self.scorecard.scoreUpper(self.dice)
        self.assertEqual(upper_card["yatzy"], 50)

    def test_add_score(self):
        test_values = [1,1,1,1,2]
        self.dice = self.helpers.makeDiceFromList(self.dice, test_values)
        self.scorecard.addLowerScore("aces", self.dice)

        test_values = [2,2,2,2,3]
        self.dice = self.helpers.makeDiceFromList(self.dice, test_values)
        self.scorecard.addLowerScore("twos", self.dice)

        test_values = [3,3,3,3,4]
        self.dice = self.helpers.makeDiceFromList(self.dice, test_values)
        self.scorecard.addLowerScore("threes", self.dice)

        test_values = [4,4,4,4,5]
        self.dice = self.helpers.makeDiceFromList(self.dice, test_values)
        self.scorecard.addLowerScore("fours", self.dice)

        test_values = [5,5,5,5,6]
        self.dice = self.helpers.makeDiceFromList(self.dice, test_values)
        self.scorecard.addLowerScore("fives", self.dice)

        test_values = [6,6,6,6,1]
        self.dice = self.helpers.makeDiceFromList(self.dice, test_values)
        self.scorecard.addLowerScore("sixes", self.dice)

        self.assertEqual(self.scorecard.lower_card["bonus"], 35)

        self.scorecard.updateTotals()
        self.assertEqual(self.scorecard.subtotal, 119)

if __name__ == "__main__":
    unittest.main()
