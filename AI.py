#This will be where I place the code for AI pathfinding
import Maze
from queue import Queue

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
    result = findPathdfs(graph, wallDict, startRow, startCol, player1Row, player1Col, [], set([(startRow, startCol)]))
    if result != None:
        return result
    #will return none if there is an obstruction
    return None

def findPathdfs(graph, wallDict, startRow, startCol, player1Row, player1Col, path, visitedsofar):
    if (startRow,startCol) == (player1Row, player1Col):
        return path
    else:
        possibleMoves = [(0,1), (1,0), (-1,0), (0, -1)]
        #print(f'start : {startRow}, {startCol}, goal : {player1Row}, {player1Col}')
        #print(f'{path}')
        #print(f'{graph.rows}, {graph.cols}')
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
                solution = findPathdfs(graph, wallDict, newRow, newCol, player1Row, player1Col, path, visitedsofar)
                if solution != None:
                    return solution
                path.pop()
                visitedsofar.remove((newRow,newCol))


##########################################################
# bfs pseudo code from #https://docs.google.com/presentation/d/1Jcu_qIQDZLIhK71DdDagxv9ayCZgaHVqV5AmNhvXUGU/edit#slide=id.g9fef3b5456_0_236
# Keep a set of all vertices that are visited, initially empty
# Have a queue of unvisited neighbors (initially just the start node)
# Extract the current node from the front of the queue
# Skip if the current node has already been visited, otherwise mark it as visited
# Stop if the current node = the target node
# Loop over the neighbors of the current node
# If they are unvisited, add them to the end of the queue
# Repeat 3-7 until the queue is empty
# This is typically not done with recursion


def bfs(graph, wallDict, player1, AI):
    #print(f'{graph.rows}, {graph.cols}')
    player1Row, player1Col = player1.row, player1.col
    #print(f'{player1Row}, {player1Col}')
    startRow, startCol = AI.row, AI.col
    possibleMoves = [(0,1), (1,0), (-1,0), (0, -1)]
    nodeMap = {}
    for row in range(graph.rows):
        for col in range(graph.cols):
            nodeMap[(row,col)] = None
    #visitedNodes = set([])
    #infinite q
    unvisitedneighbours = Queue(maxsize = 0)
    unvisitedneighbours.put((startRow, startCol))
    #unvisitedneighbours = [(startRow, startCol)]
    while unvisitedneighbours.empty() != True:
        frontNodeCoordinate = unvisitedneighbours.get()
        #print(frontNodeCoordinate)
        #print(unvisitedneighbours.qsize())
        if frontNodeCoordinate == (player1Row, player1Col):
            #reset the visited status at the end
            #print(f'{nodeMap}')
            return nodeMap
        #skip if already visited
        elif graph.nodes[frontNodeCoordinate].visited == True:
            #print('triggered')
            continue
        else:
            #if not visited set the front node visited value to True
            graph.nodes[frontNodeCoordinate].visited = True
            for move in possibleMoves:
                dRow, dCol = move[0], move[1]
                newRow, newCol = frontNodeCoordinate[0] + dRow, frontNodeCoordinate[1] + dCol
                if ((checkOutofBounds(graph, newRow, newCol)) and 
                    ((newRow, newCol) not in wallDict)
                    and (graph.nodes[(newRow, newCol)].visited != True)):
                    #assigning path
                    nodeMap[(newRow, newCol)] = frontNodeCoordinate
                    unvisitedneighbours.put((newRow, newCol))

            


def getshortestpathbfs(graph, wallDict, player1, AI):
    Maze.resetVisitedStatusNode(graph)
    nodeMap = bfs(graph, wallDict, player1, AI)
    #There is a solution
    if nodeMap != None:
        shortestPath = []
        player1Row, player1Col = player1.row, player1.col
        coordinate = (player1Row, player1Col)
        #print(nodeMap)
        while nodeMap[coordinate] != None:
            shortestPath.insert(0, coordinate)
            coordinate = nodeMap[coordinate]
        shortestPath.append((player1.row, player1.col))
        return shortestPath
    #return None if no path
    else:
        return None

    
    