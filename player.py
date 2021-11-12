from cmu_112_graphics import *
import random
import math

#class storing all the attributes of the player
class Player(object):
    def __init__(self, ImageLocation, startRow, startCol, lives, weapon):
        self.ImageLocation = ImageLocation
        self.startRow = startRow
        self.startCol = startCol
        self.lives = lives
        self.weapon= weapon