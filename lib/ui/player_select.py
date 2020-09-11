import curses
from curses.textpad import rectangle
from lib.ui.info_window import InfoWindow

class PlayerSelectScreen():
  def __init__(self, screen):
    self.x = 0
    self.y = 1
    self.width = 47
    self.height = 11
    self.amount = 1
    self.selection = 0
    self.done = False
    self.quit = False
    self.screen = screen
    self.window = curses.newwin(self.height-1,self.width-1,self.y+1,self.x+1)
    self.info_window = InfoWindow(screen, 13, 0)
    self.info_window.help_message = "<Q> Quit <ENTER> Select"
    rectangle(screen,self.y,self.x,self.y+self.height,self.x+self.width)

  def start(self):
    self.screen.addstr(0,22,"YATZY")
    self.draw()
    self.info_window.draw()

  def run(self):
    key = self.screen.getch()
    if key == ord('q'):
      self.quit = True

    self.handleInput(key)
    self.draw()

  def clear(self):
    self.window.erase()

  def refresh(self):
    self.screen.refresh()
    self.window.refresh()

  def draw(self):
    self.clear()
    self.window.addstr(0,0, "Select Player Amount:")
    current_line = 1

    for i in range(4):
      self.window.addstr(current_line,2, str(i+1)+" Player")
      current_line += 1
    
    self.writePointer()

    self.refresh()

  def writePointer(self):
    self.window.addstr(self.selection+1,0,">")

  def handleInput(self, key):
    if key == curses.KEY_UP and self.selection > 0:
      self.selection -= 1
    if key == curses.KEY_DOWN and self.selection < 3:
      self.selection += 1
    if key == 10:
      self.done = True
      self.amount = self.selection+1