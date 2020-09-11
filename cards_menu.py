import curses
from curses.textpad import rectangle

class CardsSelectHandler:
  def __init__(self):
    pass

class CardsMenu():
  def __init__(self, screen, y, x):
    self.width = 16
    self.height = 11
    self.card_pointer = [0,0]
    self.enabled = False
    self.screen = screen
    self.action = None
    self.dice = None
    self.scorecard = None
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

  def drawLowerCard(self, possible_lower={}):
    self.lower_card_window.addstr(0,0,"Lower Card")
    self.writeCardToWindow(self.lower_card_window, self.scorecard.lower_card, possible_lower)
    self.lower_card_window.addstr(9,0, "Subtotal: "+str(self.scorecard.subtotal))
  
  def drawUpperCard(self, possible_upper={}):
    self.upper_card_window.addstr(0,0,"Upper Card")
    self.writeCardToWindow(self.upper_card_window, self.scorecard.upper_card, possible_upper)
    self.upper_card_window.addstr(9,0, "Total: "+str(self.scorecard.total))

  def refresh(self):
    self.screen.refresh()
    self.lower_card_window.refresh()
    self.upper_card_window.refresh()

  def clear(self):
    self.lower_card_window.erase()
    self.upper_card_window.erase()

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
      card = [self.scorecard.lower_card,self.scorecard.upper_card][self.card_pointer[0]]
      entry = list(card.keys())[self.card_pointer[1]]

      if card[entry] != None:
        self.action = "error"
      else:
        self.action = "selected"
  
  def unfocus(self):
    self.enabled = False
    self.action = None
    self.card_pointer = [0,0]

  def focus(self):
    self.enabled = True

  def draw(self):
    if self.dice.has_rolled == False:
      possible_lower = {}
      possible_upper = {}
    else:
      possible_lower = self.scorecard.scoreLower(self.dice)
      possible_upper = self.scorecard.scoreUpper(self.dice)
    
    self.clear()
    if self.enabled:
      self.writePointer()

    self.drawLowerCard(possible_lower)
    self.drawUpperCard(possible_upper)
    self.refresh()

  def updateInfo(self, scorecard, dice):
    self.dice = dice
    self.scorecard = scorecard