import curses
from curses import wrapper
from curses.textpad import rectangle
from lib.dice import Dice
from lib.scorecard import Scorecard
from display import Display

class CardMenuHandler:
  def __init__(self):
    pass

class DiceSelectHandler:
  def __init__(self):
    pass

class ActionSelectHandler:
  def __init__(self):
    pass

class ActionWindow():
  def __init__(self, screen, y, x):
    self.x = x
    self.y = y
    self.width = 13
    self.height = 11
    self.screen = screen
    self.action_selection = 0
    self.enabled = True
    self.actions = ["Roll", "Keep", "Score"]
    self.action = None
    self.has_rolled = False
    self.action_window = curses.newwin(self.height-1,self.width-1,self.y+1,self.x+1)
    rectangle(screen,y,x,y+self.height,x+self.width)
  
  def _getAvailableActions(self):
    actions = (self.actions[:1], self.actions)[self.has_rolled]
    return actions

  def drawActions(self, current_roll=0):
    self.action_window.addstr(0,0,"Actions")
    current_line = 2
    actions = self._getAvailableActions()
    for action in actions:
      self.action_window.addstr(current_line,2,action)
      current_line += 1
    
    self.action_window.addstr(9, 0, "Roll: "+str(current_roll))

  def clear(self):
    self.action_window.clear()
  
  def refresh(self):
    self.screen.refresh()
    self.action_window.refresh()

  def writePointer(self):
    self.action_window.addstr(self.action_selection+2,0,">")

  def handleInput(self, key):
    if key == curses.KEY_UP and self.action_selection > 0:
      self.action_selection -= 1
    if key == curses.KEY_DOWN and self.action_selection < len(self._getAvailableActions())-1:
      self.action_selection += 1
    if key == 10:
      actions = self._getAvailableActions()
      self.action = actions[self.action_selection]

# 12, 0
class DiceWindow:
  def __init__(self, screen, y, x):
    self.x = x
    self.y = y
    self.width = 47
    self.height = 8
    self.enabled = False
    self.screen = screen
    self.dice_selection = 0
    self.action = None
    self.roll_window = curses.newwin(self.height-1,self.width-1,self.y+1,self.x+1)
    rectangle(screen,y,x,y+self.height,self.width)

  def drawDie(self, window, y, x, value):
    dot = u'\u2219'
    hl = u'\u2500'
    vl = u'\u2502'
    ltc = u'\u250c'
    rtc = u'\u2510'
    lbc = u'\u2514'
    rbc = u'\u2518'
    faces = {
      0: [[0,0,0], [0,0,0], [0,0,0]],
      1: [[0,0,0], [0,1,0], [0,0,0]],
      2: [[0,0,1], [0,0,0], [1,0,0]],
      3: [[0,0,1], [0,1,0], [1,0,0]],
      4: [[1,0,1], [0,0,0], [1,0,1]],
      5: [[1,0,1], [0,1,0], [1,0,1]],
      6: [[1,0,1], [1,0,1], [1,0,1]]
    }
    face = faces[value]
    current_line = y+1
    window.addstr(y, x, ltc+(hl*5)+rtc)
    for row in face:
      srow = [str(i) for i in row]
      s = ''.join(srow).replace('1', dot).replace('0', ' ')
      window.addstr(current_line, x, vl+" "+s+" "+vl)
      current_line += 1
    
    window.addstr(current_line, x, lbc+(hl*5)+rbc)

  def drawDice(self, dice):
    current_x = 3
    for die in dice.dice:
      self.drawDie(self.roll_window,0,current_x, die.value)
      if die.kept:
        self.roll_window.addstr(5,current_x+2,"[X]")
      else:
        self.roll_window.addstr(5,current_x+2,"[ ]")
      current_x += 8

  def writePointer(self):
    self.roll_window.addstr(6,(self.dice_selection*8)+6,"^")

  def refresh(self):
    self.screen.refresh()
    self.roll_window.refresh()

  def clear(self):
    self.roll_window.clear()

  def handleInput(self, key):
    if key == 27: # ESC KEY
      self.refresh()
      self.action = "back"
    if key == curses.KEY_LEFT and self.dice_selection > 0:
      self.dice_selection -= 1
    if key == curses.KEY_RIGHT and self.dice_selection < 4:
      self.dice_selection += 1
    if key == 10:
      self.action = "selected"

# 0, 0
class CardsWindow:
  def __init__(self, screen, y, x):
    self.width = 16
    self.height = 11
    self.card_pointer = [0,0]
    self.enabled = False
    self.screen = screen
    self.action = None
    self.lower_card_window = curses.newwin(self.height-1,self.width-1,y+1,x+1)
    rectangle(screen,y,x,y+self.height,x+self.width)
    self.upper_card_window = curses.newwin(self.height-1,self.width-1,y+1,x+2+self.width)
    rectangle(screen,y,x+1+self.width,y+self.height,x+1+(self.width*2))

  def writeCardToWindow(self, window, card, possible_card={}):
    current_line = 1
    for entry in card:
      if entry in possible_card:
        value = str(possible_card[entry])
      else:
        value = ""

      if card[entry] != None:
        value = "[" + str(card[entry]) + "]"
      
      window.addstr(current_line,2, entry+": "+value)
      current_line += 1

  def writePointer(self):
    windows = [self.lower_card_window, self.upper_card_window]
    windows[self.card_pointer[0]].addstr(self.card_pointer[1]+1,0,">")

  def drawLowerCard(self, scorecard, possible_lower={}):
    self.lower_card_window.addstr(0,0,"Lower Card")
    self.writeCardToWindow(self.lower_card_window, scorecard.lower_card, possible_lower)
    self.lower_card_window.addstr(9,0, "Subtotal: "+str(scorecard.subtotal))
  
  def drawUpperCard(self, scorecard, possible_upper={}):
    self.upper_card_window.addstr(0,0,"Upper Card")
    self.writeCardToWindow(self.upper_card_window, scorecard.upper_card, possible_upper)
    self.upper_card_window.addstr(9,0, "Total: "+str(scorecard.total))

  def refresh(self):
    self.screen.refresh()
    self.lower_card_window.refresh()
    self.upper_card_window.refresh()

  def clear(self):
    self.lower_card_window.clear()
    self.upper_card_window.clear()

  def handleInput(self, key):
    if key == curses.KEY_UP and self.card_pointer[1] > 0:
      self.card_pointer[1] -= 1
    if key == curses.KEY_DOWN:
      if self.card_pointer[0] == 0 and self.card_pointer[1] < 5:
        self.card_pointer[1] += 1
      elif self.card_pointer[0] == 1 and self.card_pointer[1] < 6:
        self.card_pointer[1] += 1
    if key == curses.KEY_LEFT and self.card_pointer[0] == 1:
      if self.card_pointer[1] == 6:
        self.card_pointer[1] -= 1
      self.card_pointer[0] -= 1
    if key == curses.KEY_RIGHT and self.card_pointer[0] == 0:
      self.card_pointer[0] += 1
    if key == 10:
      self.action = "selected"

scorecard = Scorecard()
dice = Dice()

def drawActionMenu(action_menu, current_roll, with_pointer=False):
  action_menu.clear()
  action_menu.drawActions(current_roll)
  if with_pointer:
    action_menu.writePointer()
  action_menu.refresh()

def drawDiceMenu(dice_menu, dice, with_pointer=False):
  dice_menu.clear()
  if with_pointer:
    dice_menu.writePointer()
  dice_menu.drawDice(dice)
  dice_menu.refresh()

def drawCardsMenu(cards_menu, possible_lower, possible_upper, with_pointer=False):
  cards_menu.clear()
  if with_pointer:
    cards_menu.writePointer()
  cards_menu.drawLowerCard(scorecard, possible_lower)
  cards_menu.drawUpperCard(scorecard, possible_upper)
  cards_menu.refresh()

def main(screen):
  cards_menu = CardsWindow(screen, 1, 0)
  dice_menu = DiceWindow(screen, 13, 0)
  action_menu = ActionWindow(screen, 1, 34)
  current_roll = 0
  curses.curs_set(0)
  curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
  screen.addstr(0,22,"YAHTZEE")
  screen.addstr(22,0,"<q> Quit <ESC> Go Back")
  possible_lower = {}
  possible_upper = {}
  cards_menu.drawLowerCard(scorecard)
  cards_menu.drawUpperCard(scorecard)
  dice_menu.drawDice(dice)
  action_menu.drawActions()
  action_menu.writePointer()
  action_menu.refresh()
  cards_menu.refresh()
  dice_menu.refresh()

  while True:
    if scorecard.complete:
      action_menu.enabled = False
      screen.addstr(22,26,"Finished",curses.color_pair(1))
      screen.refresh()

    c = screen.getch()
    if c == ord('q'):
      break

    if action_menu.enabled:
      action_menu.handleInput(c)
      drawActionMenu(action_menu, current_roll, True)

    elif cards_menu.enabled:
      cards_menu.handleInput(c)
      drawCardsMenu(cards_menu, possible_lower, possible_upper, True)

    elif dice_menu.enabled:
      dice_menu.handleInput(c)
      drawDiceMenu(dice_menu, dice, True)

    if action_menu.action == "Roll" and action_menu.enabled:
      dice.roll()
      action_menu.has_rolled = True
      current_roll += 1
      possible_lower = scorecard.scoreLower(dice)
      possible_upper = scorecard.scoreUpper(dice)
      drawDiceMenu(dice_menu, dice)
      drawActionMenu(action_menu, current_roll, True)
      drawCardsMenu(cards_menu, possible_lower, possible_upper)
      action_menu.action = None

    if action_menu.action == "Keep":
      action_menu.enabled = False
      action_menu.action = None
      dice_menu.enabled = True
      dice_menu.dice_selection = 0
      drawActionMenu(action_menu, current_roll)
      drawDiceMenu(dice_menu,dice,True)

    if action_menu.action == "Score":
      action_menu.enabled = False
      action_menu.action = None
      cards_menu.enabled = True
      drawActionMenu(action_menu, current_roll)
      drawCardsMenu(cards_menu, possible_lower, possible_upper, True)
      current_roll = 0
      action_menu.has_rolled = False

    if current_roll == 3 and action_menu.enabled:
      action_menu.cannot_roll = True
      action_menu.enabled = False
      cards_menu.enabled = True
      cards_menu.card_pointer = [0,0]
      drawActionMenu(action_menu, current_roll)
      drawCardsMenu(cards_menu, possible_lower, possible_upper, True)
      current_roll = 0
      action_menu.has_rolled = False

    if cards_menu.action == "selected":
      card = [scorecard.lower_card, scorecard.upper_card][cards_menu.card_pointer[0]]
      addScore = [scorecard.addLowerScore, scorecard.addUpperScore][cards_menu.card_pointer[0]]
      entry = list(card.keys())[cards_menu.card_pointer[1]]
      addScore(entry, dice)
      cards_menu.enabled = False
      action_menu.enabled = True
      action_menu.action_selection = 0
      cards_menu.action = None
      dice.reset()
      possible_lower = {}
      possible_upper = {}
      drawCardsMenu(cards_menu, possible_lower, possible_upper)
      drawDiceMenu(dice_menu, dice)
      drawActionMenu(action_menu, current_roll, True)
      scorecard.checkComplete()

    if dice_menu.action == "selected":
      die = dice.dice[dice_menu.dice_selection]
      if die.kept:
        dice.unkeep(dice_menu.dice_selection)
      else:
        dice.keep(dice_menu.dice_selection)
      drawDiceMenu(dice_menu, dice, True)
      dice_menu.action = None
    
    if dice_menu.action == "back":
      dice_menu.enabled = False
      dice_menu.action = None
      action_menu.enabled = True
      action_menu.action_selection = 0
      drawDiceMenu(dice_menu, dice)
      drawActionMenu(action_menu, current_roll, True)

wrapper(main)
