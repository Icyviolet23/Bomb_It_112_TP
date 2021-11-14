import random
import math

#class storing all the attributes of the player
class Player(object):
    def __init__(self, startRow, startCol, lives, weapon):
        self.ImageLocation = 0
        self.startRow = startRow
        self.startCol = startCol
        self.lives = lives
        self.weapon= weapon