class Scorecard():
    def __init__(self):
        self.total = 0
        self.subtotal = 0

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

    def getPossibleLowerCard(self, dice):
        lower_card = self.lower_card
        values = [die.value for die in dice]
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

        return lower_card

    def getPossibleUpperCard(self, dice):
        upper_card = self.upper_card
        values = [die.value for die in dice]

        if upper_card["triples"] == None:
            result = dice.checkThreeOfAKind()
            upper_card["triples"] = (0, sum(values))[result]

        if upper_card["quads"] == None:
            result = dice.checkFourOfAKind()
            upper_card["quads"] = (0, sum(valuez))[result]

        if upper_card["full"] == None:
            result = dice.checkFullHouse()
            upper_card["full"] = (0, 25)[result]

        if upper_card["small"] == None:
            result = dice.checkSmallStraight()
            upper_card["small"] = (0, 30)[result]

        if upper_card["large"] == None:
            result = dice.checkLargeStraight()
            upper_card["large"] = (0, 40)[result]

        if upper_card["yahtzee"] == None:
            result = dice.checkYahtzee()
            upper_card["yahtzee"] = (0, 50)[result]

        if upper_card["chance"] == None:
            upper_card["chance"] = sum(values)
        
        return upper_card
