from lib.die import Die

class Dice():
    def __init__(self):
        self.dice = [Die() for i in range(5)]
        self.has_rolled = False
        self.roll_amount = 0

    def roll(self):
        dice = [die for die in self.dice if die.kept == False]
        self.has_rolled = True
        self.roll_amount += 1
        for die in dice:
            die.roll()
    
    def reset(self):
        self.dice = [Die() for i in range(5)]
        self.has_rolled = False
        self.roll_amount = 0

    def keep(self, index):
        self.dice[index].kept = True

    def unkeep(self, index):
        self.dice[index].kept = False

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
        values = []
        for die in self.dice:
            if die.value not in values:
                values.append(die.value)

        values.sort()
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
        values.sort()
        
        return values == large_straight1 or values == large_straight2

    def checkYahtzee(self):
        values = self.getValues()
        return values.count(values[0]) == 5

    def getValues(self):
        return list( map(lambda die: die.value, self.dice) )


