from die import Die

class Dice():
    def __init__(self):
        self.dice = [Die() for i in range(5)]
        self.kept_dice = []

    def roll(self):
        for die in self.dice:
            die.roll()

    def keep(self, index):
        die = self.dice.pop(index)
        self.kept_dice.append(die)

    def unkeep(self, index):
        die = self.kept_dice.pop(index)
        self.dice.append(die)

    def _checkForKind(self, kind, strict=False):
        dice_values = [die.value for die in self.dice]
        dice_values.sort()
        for value in dice_values:
            if strict:
                if dice_values.count(value) == kind:
                    return True
            else:
                if dice_values.count(value) >= kind:
                    return True
        return False

    def checkThreeOfAKind(self):
        return self._checkForKind(3)

    def checkFourOfAKind(self):
        return self._checkForKind(4)

    def checkFullHouse(self):
        return self._checkForKind(2, strict=True) and self._checkForKind(3, strict=True)

    def checkSmallStraight(self):
        small_straight1 = [1,2,3,4]
        small_straight2 = [2,3,4,5]
        small_straight3 = [3,4,5,6]
        values = [die.value for die in self.dice]
        values1 = values[:4]
        values2 = values[1:5]

        result1 = values1 == small_straight1 or values2 == small_straight1
        result2 = values1 == small_straight2 or values2 == small_straight2
        result3 = values1 == small_straight3 or values2 == small_straight3

        return result1 or result2 or result3

    def checkLargeStraight(self):
        large_straight1 = [1,2,3,4,5]
        large_straight2 = [2,3,4,5,6]
        values = [die.value for die in self.dice]
        
        return values == large_straight1 or values == large_straight2

    def checkYahtzee(self):
        return self.dice.count(self.dice[0]) == 5

    def _printDice(self, dice):
        for die in dice:
            index = dice.index(die)
            print(index, "->", die.value)

    def printDice(self):
        self._printDice(self.dice)

    def printKeptDice(self):
        self._printDice(self.kept_dice)


