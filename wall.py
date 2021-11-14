import math

class Wall(object):
    def __init__(self, image, destructible):
        self.image = image
        #this will be a boolean value
        #true if destructible, false if not
        self.destructible = destructible