import curses
from curses.textpad import rectangle

class DiceSelectHandler:
  def __init__(self):
    pass

class DiceMenu():
  def __init__(self, screen, y, x):
    self.x = x
    self.y = y
    self.width = 47
    self.height = 8
    self.enabled = False
    self.screen = screen
    self.dice_selection = 0
    self.dice = []
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

  def drawDice(self):
    current_x = 3
    for die in self.dice:
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
    self.roll_window.erase()

  def handleInput(self, key):
    if key == 27: # ESC KEY
      self.action = "back"
    if key == curses.KEY_LEFT and self.dice_selection > 0:
      self.dice_selection -= 1
    if key == curses.KEY_RIGHT and self.dice_selection < 4:
      self.dice_selection += 1
    if key == 10:
      self.action = "selected"

  def unfocus(self):
    self.enabled = False
    self.action = None
    self.dice_selection = 0

  def focus(self):
    self.enabled = True

  def draw(self):
    self.clear()
    if self.enabled:
      self.writePointer()
    self.drawDice()
    self.refresh()

  def updateInfo(self, dice):
    self.dice = dice.dice