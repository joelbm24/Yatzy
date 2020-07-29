import random

class Die():
    def __init__(self, min=1, max=6):
        self.value = 0
        self._min = min
        self._max = max

    def roll(self):
        self.value = random.randint(self._min, self._max)

