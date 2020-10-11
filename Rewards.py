import random


class Rewards:
    def __init__(self):
        self._rolls = ["1 Coal", "2 Levels", "64 Dirt", "64 Cobblestone", "5 Levels",
                       "1 stack of building block of your choice", "8 Levels", "1 Wolf",
                       "1 Cat", "Luck of the Sea III", "Lure III", "Mending", "15 Levels", "64 Diamonds",
                       "64 Gunpowder", "1 Netherite ingot", "30 Levels", "Efficiency V",
                       "Silk Touch", "Unbreaking III", "Fortune III", "Totem of Undying", "Elytra"]

    def roll(self):
        return self._rolls[random.randint(0, len(self._rolls))]
