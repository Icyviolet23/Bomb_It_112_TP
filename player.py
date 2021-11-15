import random
import math

#class storing all the attributes of the player
class Player(object):
    def __init__(self, row, col, lives, weapon):
        #row, col marks the position of the player
        self.ImageLocation = 0
        self.row = row
        self.col = col
        self.lives = lives
        self.weapon = weapon