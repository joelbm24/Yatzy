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
            "yahtzee": None,
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
        is_yahtzee = self.upper_card["yahtzee"] == 50

        if is_repeat and is_yahtzee:
            return self._repeat_yahtzees.append(100)

    def scoreLower(self, dice):
        dice_values = dice.getValues()
        card = self.lower_card.copy()

        card["aces"] = dice_values.count(1) * 1
        card["twos"] = dice_values.count(2) * 2
        card["threes"] = dice_values.count(3) * 3
        card["fours"] = dice_values.count(4) * 4
        card["fives"] = dice_values.count(5) * 5
        card["sixes"] = dice_values.count(6) * 6

        return card

    def addLowerScore(self, category, dice):
        lower_scores = self.scoreLower(dice)
        self.addScore(category, lower_scores, self.lower_card)
        self.checkAddBonus()
        self.checkRepeatYahtzee(dice)
        self.updateTotals()

    def scoreUpper(self, dice):
        dice_values = dice.getValues()
        card = self.upper_card.copy()

        card["triples"] = (0, sum(dice_values))[dice.checkThreeOfAKind()]
        card["quads"] = (0, sum(dice_values))[dice.checkFourOfAKind()]
        card["full"] = (0, 25)[dice.checkFullHouse()]
        card["small"] = (0, 30)[dice.checkSmallStraight() or dice.checkLargeStraight()]
        card["large"] = (0, 40)[dice.checkLargeStraight()]
        card["yahtzee"] = (0, 50)[dice.checkYahtzee()]
        card["chance"] = sum(dice_values)

        return card

    def addUpperScore(self, category, dice):
        upper_scores = self.scoreUpper(dice)
        self.addScore(category, upper_scores, self.upper_card)
        self.checkRepeatYahtzee(dice)
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
    
    def printCard(self, card, with_option=False):
        categories = list(card.keys())

        for category in categories:
            index = categories.index(category)
            score = (card[category], "")[card[category] == None]
            if with_option:
                print(index, "->", category + ":", score)
            else:
                print(category + ":", score)

    def printUpperCard(self, with_option=False):
        print("UPPER:")
        self.printCard(self.upper_card)
        print("TOTAL:", self.total)

    def printLowerCard(self, with_option=False):
        print("LOWER:")
        self.printCard(self.lower_card)
        print("SUBTOTAL:", self.subtotal)

