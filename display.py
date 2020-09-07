import curses
from curses.textpad import rectangle

class Display:
  def __init__(self, screen):
    self.screen = screen