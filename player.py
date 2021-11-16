import random
import math
import weapon

#class storing all the attributes of the player
class Player(object):
    def __init__(self, row, col, lives, weaponID):
        #row, col marks the position of the player
        self.ImageLocation = 0
        self.row = row
        self.col = col
        self.lives = lives
        self.weaponID = weapon
        self.bombCount = 1
        self.bombTimer = 10