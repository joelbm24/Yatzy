from dice import Dice
from scorecard import Scorecard

dice = Dice()
scorecard = Scorecard()

def keep_unkeep_dice(dice, keep=True):
  done = False
  dice_change = (dice.unkeep, dice.keep)[keep]
  while not done:
    dice.printDice()
    print("q: QUIT")
    option = input("Which die? ")
    if option.isdigit():
      index = int(option)
      dice_change(index)
    elif option == "q":
      done = True
    else:
      print("Try again")

def addScore(upper_lower, dice):
  done = False
  is_lower = upper_lower == "lower"
  card = (scorecard.upper_card, scorecard.lower_card)[is_lower]
  get_scores = (scorecard.scoreUpper, scorecard.scoreLower)[is_lower]
  add_card_score = (scorecard.addUpperScore, scorecard.addLowerScore)[is_lower]

  categories = list( card.keys() )
  scores = get_scores(dice)
  while not done:
    scorecard.printCard(scores, with_option=True)
    option = int(input("Which Category? "))
    category = categories[option]
    if card[category] == None:
      add_card_score(category, dice)
      done = True
    else:
      print("Score already filled")

def score():
  upper_lower = input("Which Card (upper/lower)? ")
  if upper_lower in ["upper", "lower"]:
    addScore(upper_lower, dice)
  else:
    print("Not an option")

while not scorecard.complete:
  current_roll = 0
  have_rolled = False
  while current_roll < 3:
    print("Current Roll:", current_roll)
    scorecard.printLowerCard()
    scorecard.printUpperCard()
    dice.printDice()
    print("1: ROLL")
    if have_rolled:
      print("2: KEEP")
      print("3: UNKEEP")
      print("4: SCORE")
    option = input("Which Option? ")

    if option == "1":
      dice.roll()
      current_roll += 1
      have_rolled = True
    elif option == "2" and have_rolled:
      keep_unkeep_dice(dice)
    elif option == "3" and have_rolled:
      keep_unkeep_dice(dice, keep=False)
    elif option == "4" and have_rolled:
      current_roll = 3
    else:
      print("Try again")
  
  dice.printDice()
  score()
  dice.reset()


print("Final Score:", scorecard.total)
