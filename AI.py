#This will be where I place the code for AI pathfinding


##########################################################
#dfs
#takes in the app.Mazewalls dictionary and finds the shortest path
#takes in the player1 instance and the AI which is another player instance


def checkOutofBounds(graph, row, col):
    rows = graph.rows
    cols = graph.cols
    if row < 0 or col < 0  or row >= rows or col >= cols:
        return False
    return True

def dfs(graph, player1, AI):
    player1Row, player1Col = player1.row, player1.col
    
    startRow, startCol = AI.row, AI.col
    result = findShortestPathdfs(graph, startRow, startCol, player1Row, player1Col)
    if result != None:
        return result
    return None

def findShortestPathdfs(graph, startRow, startCol, player1Row, player1Col):
    possibleMoves = [(0,1), (1,0), (-1,0), (0, -1)]
    pass