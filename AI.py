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


#right now we are finding any path not the shortest path
def dfs(graph, wallDict, player1, AI):
    #destination
    player1Row, player1Col = player1.row, player1.col
    #AI position
    startRow, startCol = AI.row, AI.col
    result = findShortestPathdfs(graph, wallDict, startRow, startCol, player1Row, player1Col, [], set([(startRow, startCol)]))
    if result != None:
        return result
    #will return none if there is an obstruction
    return None

def findShortestPathdfs(graph, wallDict, startRow, startCol, player1Row, player1Col, path, visitedsofar):
    if (startRow,startCol) == (player1Row, player1Col):
        return path
    else:
        possibleMoves = [(0,1), (1,0), (-1,0), (0, -1)]
        print(f'start : {startRow}, {startCol}, goal : {player1Row}, {player1Col}')
        print(f'{path}')
        print(f'{graph.rows}, {graph.cols}')
        for move in possibleMoves:
            dRow, dCol = move[0], move[1]
            newRow, newCol = startRow + dRow, startCol + dCol
            #checks if out of bounds and if there is a wall there
            if ((checkOutofBounds(graph, newRow, newCol)) and 
                ((newRow, newCol) not in wallDict) and 
                ((newRow, newCol) not in visitedsofar)):
                #print('yay')
                path.append((newRow,newCol))
                visitedsofar.add((newRow,newCol))
                solution = findShortestPathdfs(graph, wallDict, newRow, newCol, player1Row, player1Col, path, visitedsofar)
                if solution != None:
                    return solution
                path.pop()
                visitedsofar.remove((newRow,newCol))