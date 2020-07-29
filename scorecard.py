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

    def score(self, dice):
       pass 


