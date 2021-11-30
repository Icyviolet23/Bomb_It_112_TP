#weapon class
class Bomb(object):
    def __init__(self, timer, playernum, bombradius):
        self.timer = timer
        #records down number by player
        self.playernum = playernum
        self.bombradius = bombradius
        self.weaponID = 0

    def countDown(self):
        if self.timer > 0:
            self.timer -= 1


class Explosion(object):
    def __init__(self, centerRow, centerCol, playernum, bombRadius):
        self.centerRow = centerRow
        self.centerCol = centerCol
        #list of coordinates containing the radius
        self.radius = []
        self.timer = 2
        #controls whose explosion belongs to whom
        self.playernum = playernum
        self.bombRadius = bombRadius
        self.bombdcoordinate = [(0,0)]

    def createBombchangeRowCol(self):
        baseRadius = [(0,1), (1,0), (-1,0), (0, -1)]
        for i in range(1, self.bombRadius + 1):
            for row, col in baseRadius:
                self.bombdcoordinate.append((row*i, col*i))
