import curses, os
from curses import wrapper
from lib.ui.game import Game
from lib.ui.player_select import PlayerSelectScreen
from lib.ui.finish_screen import FinishScreen

def shorten_esc_delay():
  os.environ.setdefault("ESCDELAY", '25')

def main(screen):
  curses.curs_set(0)
  curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
  curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_RED)
  curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
  curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)

  game = None
  finish_screen = None
  player_select = PlayerSelectScreen(screen)
  player_select.start()

  current_screen = player_select

  while not current_screen.quit:
    if current_screen == player_select and player_select.done:
      screen.clear()
      game = Game(screen, player_select.amount)
      game.start()
      current_screen = game

    elif current_screen == game and game.done:
      screen.clear()
      winner = game.getWinner()
      finish_screen = FinishScreen(screen, winner)
      finish_screen.start()
      current_screen = finish_screen

    elif current_screen == finish_screen and finish_screen.done:
      screen.clear()
      player_select = PlayerSelectScreen(screen)
      player_select.start()
      current_screen = player_select

    current_screen.run()

shorten_esc_delay()
wrapper(main)
