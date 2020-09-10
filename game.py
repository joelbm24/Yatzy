import curses
from curses import wrapper
from curses.textpad import rectangle
from lib.dice import Dice
from lib.scorecard import Scorecard
from action_menu import *
from dice_menu import *
from cards_menu import *
from info_window import *

class Game():
  def __init__(self, screen):
    self.done = False
    self.screen = screen
    self.scorecard = Scorecard()
    self.dice = Dice()
    self.cards_menu = CardsMenu(screen, 1, 0)
    self.dice_menu = DiceMenu(screen, 13, 0)
    self.action_menu = ActionMenu(screen, 1, 34)
    self.info_window = InfoWindow(screen, 22, 0)

    self.current_window = self.action_menu
  
  def start(self):
    self.screen.addstr(0,22,"YAHTZEE")
    self.action_menu.focus()
    self.cards_menu.updateInfo(self.scorecard, self.dice)
    self.action_menu.updateInfo(self.dice)
    self.dice_menu.updateInfo(self.dice)

    self.cards_menu.draw()
    self.action_menu.draw()
    self.dice_menu.draw()
    self.info_window.draw()

  def run(self):
    key = self.screen.getch()
    if key == ord('q'):
      self.done = True

    if self.scorecard.complete:
      action_menu.enabled = False
      info_window.finished = True
    
    self.info_window.draw()

    self.current_window.handleInput(key)
    self.current_window.draw()
    self.handleAction()

  def handleAction(self):
    if self.current_window == self.action_menu:
      if self.action_menu.action == "Roll":
        self.actionRoll()
      elif self.action_menu.action == "Keep":
        self.actionKeep()
      elif self.action_menu.action == "Score":
        self.actionScore()
    elif self.current_window == self.cards_menu:
      if self.cards_menu.action == "error":
        self.cardEntryError()
      elif self.cards_menu.action == "selected":
        self.cardEntrySelect()
    elif self.current_window == self.dice_menu:
      if self.dice_menu.action == "back":
        self.diceBack()
      elif self.dice_menu.action == "selected":
        self.diceSelect()

  def actionRoll(self):
    self.action_menu.action = None
    self.dice.roll()

    self.action_menu.updateInfo(self.dice)
    self.cards_menu.updateInfo(self.scorecard, self.dice)
    self.dice_menu.updateInfo(self.dice)

    self.dice_menu.draw()
    self.action_menu.draw()

    if self.dice.roll_amount == 3:
      self.actionScore()
    else:
      self.cards_menu.draw()
  
  def actionKeep(self):
      self.action_menu.unfocus()
      self.dice_menu.focus()

      self.action_menu.draw()
      self.dice_menu.draw()

      self.current_window = self.dice_menu
  
  def actionScore(self):
      self.action_menu.unfocus()
      self.cards_menu.focus()

      self.action_menu.draw()
      self.cards_menu.draw()

      self.current_window = self.cards_menu
  
  def cardEntryError(self):
    self.info_window.error = True
    self.cards_menu.action = None

  def cardEntrySelect(self):
    card = [self.scorecard.lower_card,self.scorecard.upper_card][self.cards_menu.card_pointer[0]]
    addScore = [self.scorecard.addLowerScore, self.scorecard.addUpperScore][self.cards_menu.card_pointer[0]]
    entry = list(card.keys())[self.cards_menu.card_pointer[1]]
    addScore(entry, self.dice)
    self.dice.reset()
    self.scorecard.checkComplete()

    self.info_window.error = False
    self.cards_menu.unfocus()
    self.action_menu.focus()

    self.action_menu.updateInfo(self.dice)
    self.cards_menu.updateInfo(self.scorecard, self.dice)
    self.dice_menu.updateInfo(self.dice)

    self.cards_menu.draw()
    self.dice_menu.draw()
    self.action_menu.draw()

    self.current_window = self.action_menu
  
  def diceSelect(self):
    die = self.dice.dice[self.dice_menu.dice_selection]

    if die.kept:
      self.dice.unkeep(self.dice_menu.dice_selection)
    else:
      self.dice.keep(self.dice_menu.dice_selection)

    self.dice_menu.updateInfo(self.dice)
    self.dice_menu.draw()

    self.dice_menu.action = None

  def diceBack(self):
    self.dice_menu.unfocus()
    self.action_menu.focus()

    self.action_menu.draw()
    self.dice_menu.draw()

    self.current_window = self.action_menu