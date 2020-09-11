from lib.yatzy.dice import Dice
from lib.yatzy.scorecard import Scorecard

class Player():
  def __init__(self, name):
    self.name = name
    self.scorecard = Scorecard()
    self.dice = Dice()
    self.finished = False