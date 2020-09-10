from lib.dice import Dice
from lib.scorecard import Scorecard

class Player():
  def __init__(self, name):
    self.name = name
    self.scorecard = Scorecard()
    self.dice = Dice()
    self.finished = False