import curses

class InfoWindow():
  def __init__(self, screen, x, y):
    self.x = x
    self.y = y
    self.width = 48
    self.height = 1
    self.screen = screen
    self.error = False
    self.window = curses.newwin(self.height, self.width, self.x, self.y)

    self.help_message = "<q> Quit <ESC> Back <ENTER> Select"

  def draw(self):
    self.clear()

    self.window.addstr(0,0,self.help_message)
    if self.error:
      self.window.addstr(0,42,"ERROR", curses.color_pair(2))
    
    self.refresh()
  
  def clear(self):
    self.window.clear()

  def refresh(self):
    self.screen.refresh()
    self.window.refresh()