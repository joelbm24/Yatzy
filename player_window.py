import curses
from curses.textpad import rectangle

class PlayerWindow():
  def __init__(self, screen, y, x, players):
    self.x = x
    self.y = y
    self.width = 47
    self.height = 2
    self.screen = screen
    self.players = players
    self.current_player = 0
    self.window = curses.newwin(self.height-1,self.width-1,self.y+1,self.x+1)
    rectangle(screen,y,x,y+self.height,x+self.width)

  def draw(self):
    self.clear()
    current_x = 2

    for player in self.players:
      color = 0
      index = self.players.index(player)
      if index == self.current_player:
        color = 3
      elif player.finished:
        color = 4
      
      self.window.addstr(0, current_x, player.name, curses.color_pair(color))
      current_x += len(player.name) + 3

    self.refresh()
  
  def clear(self):
    self.window.clear()

  def refresh(self):
    self.screen.refresh()
    self.window.refresh()