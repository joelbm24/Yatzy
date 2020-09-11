import curses
from curses.textpad import rectangle

class ActionSelectHandler:
  def __init__(self):
    pass

class ActionMenu():
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
    self.current_roll = 0
    self.action_window = curses.newwin(self.height-1,self.width-1,self.y+1,self.x+1)
    rectangle(self.screen,y,x,y+self.height,x+self.width)
  
  def _getAvailableActions(self):
    actions = (self.actions[:1], self.actions)[self.has_rolled]
    return actions

  def drawActions(self):
    self.action_window.addstr(0,0,"Actions")
    current_line = 2
    actions = self._getAvailableActions()
    for action in actions:
      self.action_window.addstr(current_line,2,action)
      current_line += 1
    
    self.action_window.addstr(9, 0, "Roll: "+str(self.current_roll))

  def clear(self):
    self.action_window.erase()
  
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

  def unfocus(self):
    self.enabled = False
    self.action = None
    self.action_selection = 0

  def focus(self):
    self.enabled = True

  def draw(self):
    self.clear()
    if self.enabled:
      self.writePointer()
    
    self.drawActions()
    self.refresh()

  def updateInfo(self, dice):
    self.has_rolled = dice.has_rolled
    self.current_roll = dice.roll_amount