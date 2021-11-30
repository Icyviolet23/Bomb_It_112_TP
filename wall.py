#wall class

import random
class Wall(object):
    def __init__(self, row, col, destructible):
        self.imageIndex = random.randint(0,3)
        self.row = row
        self.col = col
        #this will be a boolean value
        #true if destructible, false if not
        self.destructible = destructible