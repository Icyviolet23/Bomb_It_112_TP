class Bomb(object):
    def __init__(self, timer):
        self.timer = timer
        self.rangeX = 2
        self.rangeY = 2
        self.weaponID = 1

    def countDown(self):
        if self.timer > 0:
            self.timer -= 1