class Scorecard():
    def __init__(self):
        self.total = 0
        self.subtotal = 0
        self.complete = False

        self._repeat_yahtzees = []

        self.lower_card = {
            "aces": None,
            "twos": None,
            "threes": None,
            "fours": None,
            "fives": None,
            "sixes": None,
            "bonus": None
        }

        self.upper_card = {
            "triples": None,
            "quads": None,
            "full": None,
            "small": None,
            "large": None,
            "yatzy": None,
            "chance": None
        }

    def addScore(self, category, scores, card):
        if scores[category] == None:
            self.card[category] = 0
        else:
            card[category] = scores[category]

    def checkAddBonus(self):
        values = list( self.lower_card.values() )[:-1]
        numbers = [value for value in values if value != None]
        if sum(numbers) >= 62:
            self.lower_card["bonus"] = 35
        
        if len(numbers) == 6 and sum(numbers) < 62:
            self.lower_card["bonus"] = 0

    def checkRepeatYahtzee(self, dice):
        is_repeat = dice.checkYahtzee()
        is_yahtzee = self.upper_card["yatzy"] == 50

        if is_repeat and is_yahtzee:
            return self._repeat_yahtzees.append(100)

    def scoreLower(self, dice):
        lower_card = self.lower_card.copy()
        values = dice.getValues()

        if lower_card["aces"] == None:
            lower_card["aces"] = values.count(1) * 1

        if lower_card["twos"] == None:
            lower_card["twos"] = values.count(2) * 2
        
        if lower_card["threes"] == None:
            lower_card["threes"] = values.count(3) * 3
        
        if lower_card["fours"] == None:
            lower_card["fours"] = values.count(4) * 4

        if lower_card["fives"] == None:
            lower_card["fives"] = values.count(5) * 5
         
        if lower_card["sixes"] == None:
            lower_card["sixes"] = values.count(6) * 6

        if lower_card["bonus"] == None:
            lower_card["bonus"] = 0

        return lower_card

    def addLowerScore(self, category, dice):
        lower_scores = self.scoreLower(dice)
        self.addScore(category, lower_scores, self.lower_card)
        self.checkAddBonus()
        self.checkRepeatYahtzee(dice)
        self.updateTotals()

    def scoreUpper(self, dice):
        upper_card = self.upper_card.copy()
        values = [die.value for die in dice.dice]

        if upper_card["triples"] == None:
            result = dice.checkThreeOfAKind()
            upper_card["triples"] = (0, sum(values))[result]

        if upper_card["quads"] == None:
            result = dice.checkFourOfAKind()
            upper_card["quads"] = (0, sum(values))[result]

        if upper_card["full"] == None:
            result = dice.checkFullHouse()
            upper_card["full"] = (0, 25)[result]

        if upper_card["small"] == None:
            result = dice.checkSmallStraight()
            upper_card["small"] = (0, 30)[result or dice.checkLargeStraight()]

        if upper_card["large"] == None:
            result = dice.checkLargeStraight()
            upper_card["large"] = (0, 40)[result]

        if upper_card["yatzy"] == None:
            result = dice.checkYahtzee()
            upper_card["yatzy"] = (0, 50)[result]

        if upper_card["chance"] == None:
            upper_card["chance"] = sum(values)
        
        return upper_card

    def addUpperScore(self, category, dice):
        upper_scores = self.scoreUpper(dice)
        self.checkRepeatYahtzee(dice)
        self.addScore(category, upper_scores, self.upper_card)
        self.updateTotals()
    
    def updateTotals(self):
        values = [value for value in self.lower_card.values() if value != None]
        self.subtotal = sum(values)
        values = [value for value in self.upper_card.values() if value != None]
        self.total = self.subtotal + sum(values) + (len(self._repeat_yahtzees) * 100)
    
    def checkComplete(self):
        lower_complete = list(self.lower_card.values()).count(None) == 0
        upper_complete = list(self.upper_card.values()).count(None) == 0
        self.complete = lower_complete and upper_complete
