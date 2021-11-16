class Bomb(object):
    def __init__(self, timer, playernum):
        self.timer = timer
        self.playernum = playernum
        self.rangeX = 2
        self.rangeY = 2
        self.weaponID = 0

    def countDown(self):
        if self.timer > 0:
            self.timer -= 1


class Explosion(object):
    def __init__(self, centerRow, centerCol):
        self.centerRow = centerRow
        self.centerCol = centerCol
        #list of coordinates containing the radius
        self.radius = []
        self.timer = 2