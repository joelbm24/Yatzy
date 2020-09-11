import curses
from curses.textpad import rectangle

class FinishScreen():
  def __init__(self, screen, winner):
    self.x = 0
    self.y = 0
    self.width = 47
    self.height = 11
    self.amount = 1
    self.selection = 0
    self.done = False
    self.quit = False
    self.winner = winner
    self.screen = screen
    self.window = curses.newwin(self.height-1,self.width-1,self.y+1,self.x+1)
    rectangle(screen,self.y,self.x,self.y+self.height,self.x+self.width)

  def start(self):
    self.draw()

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
    self.window.addstr(0,0, "FINISHED! " + self.winner.name + " Won")
    self.window.addstr(1,0, "Score: " + str(self.winner.scorecard.total))
    self.window.addstr(2,2, "REPLAY")
    self.window.addstr(3,2, "QUIT")
    
    self.writePointer()

    self.refresh()

  def writePointer(self):
    self.window.addstr(self.selection+2,0,">")

  def handleInput(self, key):
    if key == curses.KEY_UP and self.selection > 0:
      self.selection -= 1
    if key == curses.KEY_DOWN and self.selection < 2:
      self.selection += 1
    if key == 10:
      self.done = True
      if self.selection == 1:
        self.quit = True