class Wall(object):
    def __init__(self, row, col, destructible):
        self.image = 'tree1'
        self.row = row
        self.col = col
        #this will be a boolean value
        #true if destructible, false if not
        self.destructible = destructible