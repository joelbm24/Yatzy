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

    def _checkForKind(self, kind):
        dice_values = [die.value for die in self.dice]
        dice_values.sort()
        for value in dice_values:
            if dice_values.count(value) == kind:
                return True
        return False

    def checkThreeOfAKind(self):
        return self._checkForKind(3)

    def checkFourOfAKind(self):
        return self._checkForKind(4)

    def checkFullHouse(self):
        return self._checkForKind(2) and self._checkForKind(3)

    def checkSmallStraight(self):
        pass

    def checkLargeStraight(self):
        pass

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


