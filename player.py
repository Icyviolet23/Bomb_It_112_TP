#player class

import random
import math
import weapon

#class storing all the attributes of the player
#action is the action that the player is doing at the moment
#possible actions : 'forward', 'backward', 'right', 'left'
class Player(object):
    def __init__(self, row, col, lives, weaponID, action):
        #row, col marks the position of the player
        self.ImageLocation = 0
        self.row = row
        self.col = col
        self.lives = lives
        self.weaponID = weaponID
        self.bombCount = 2
        self.bombTimer = 2
        self.action = action
        #for AI use only
        self.counter = 0

        #only used for AIs
        self.targetSwitch = 2
