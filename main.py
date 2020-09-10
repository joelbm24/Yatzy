import curses
from curses import wrapper
from curses.textpad import rectangle
from game import Game

def main(screen):
  curses.curs_set(0)
  curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
  curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_RED)
  
  game = Game(screen)
  game.start()

  while not game.done:
    game.run()

wrapper(main)
