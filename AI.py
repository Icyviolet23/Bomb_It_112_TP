#This will be where I place the code for AI pathfinding
import Maze
from queue import Queue

##########################################################
#dfs
#takes in the app.Mazewalls dictionary and finds the shortest path
#takes in the player1 instance and the AI which is another player instance
# dfs code is fully written by me

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
# bfs pseudo code from https://docs.google.com/presentation/d/1Jcu_qIQDZLIhK71DdDagxv9ayCZgaHVqV5AmNhvXUGU/edit#slide=id.g9fef3b5456_0_236
# Keep a set of all vertices that are visited, initially empty
# Have a queue of unvisited neighbors (initially just the start node)
# Extract the current node from the front of the queue
# Skip if the current node has already been visited, otherwise mark it as visited
# Stop if the current node = the target node
# Loop over the neighbors of the current node
# If they are unvisited, add them to the end of the queue
# Repeat 3-7 until the queue is empty
# This is typically not done with recursion

#bfs code is written by me
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

            

#idea for storing and retriving the node path is obtained from https://docs.google.com/presentation/d/1Jcu_qIQDZLIhK71DdDagxv9ayCZgaHVqV5AmNhvXUGU/edit#slide=id.g9fef3b5456_0_236
#however, all the code below is written solely by me
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






# https://docs.google.com/presentation/d/1Jcu_qIQDZLIhK71DdDagxv9ayCZgaHVqV5AmNhvXUGU/edit#slide=id.g9fef3b5456_0_247
# Have a set of unvisited nodes (all nodes)
# Have a dictionary mapping each node to its distance from the start node (0 for the start node, ∞ for everything else)
# Repeat the following until the current node is the target node:
# Pick the unvisited node with the minimum distance
# Remove it from the unvisited nodes
# For each neighbor of the current node, if its distance is greater than the current node + the weight of the edge connecting them, update the distance
# Use the same idea as from BFS/DFS to reconstruct the path
# code is written by me but algorithm design is inspired from the mini ta lecture slides



#Astar
#use this euclidean distance for the heuristic
def distance(x0 ,y0 ,x1, y1):
    return ((x1-x0)**2 + (y1-y0)**2)**0.5

def resetalldist(graph):
    for coordinate in graph.nodes:
        graph.nodes[coordinate].distance = 1

#we need to prepare the graph for use for Astar
#we need to reset all nodes.visited to False
#we need to update the distance to 3 for walls
#mazewalls is a dictionary mapping coordinate to wall instance
def initializeGraphforAstar(app, graph, Mazewalls):
    Maze.resetVisitedStatusNode(graph)
    resetalldist(graph)
    for coordinate in graph.nodes:
        #wall set to 5
        if coordinate in Mazewalls:
            graph.nodes[coordinate].distance = 5
        elif coordinate in graph.traps:
        #we want the AI to avoid traps as much as possible
            graph.nodes[coordinate].distance = 10**3
        #we want the AI to avoid bombs as much as possible
        elif len(app.weaponPos[coordinate]) > 0:
            graph.nodes[coordinate].distance = 10**3
        else:
            graph.nodes[coordinate].distance = 1
    return graph


#this is where i implement the Astar searching
def pickshortestDistance(graph, dict, targetplayerRow, targetplayerCol):
    shortestDist = 10**15
    bestCoordinate = None
    for coordinate in dict:
        row, col = coordinate[0], coordinate[1]
        AstarDist = dict[coordinate] + distance(row, col, targetplayerRow, targetplayerCol)


        if AstarDist < shortestDist and graph.nodes[coordinate].visited != True:
            shortestDist = dict[coordinate]
            bestCoordinate = coordinate
        else:
            continue

    return bestCoordinate

    
#tracks players only
#graph, wall dict, start instance of player, target instance of player
def Astar(app, graph, Mazewalls, startplayernum, targetplayernum):
    startplayer = app.players[startplayernum]
    targetplayer = app.players[targetplayernum]
    startRow, startCol = startplayer.row, startplayer.col
    targetRow, targetCol = targetplayer.row, targetplayer.col

    graph = initializeGraphforAstar(app, graph, Mazewalls)
    #initalizing the distance dictionary
    distanceDict = {}

    possibleMoves = [(0,1), (1,0), (-1,0), (0, -1)]
    
    for coordinate in graph.nodes:
        if coordinate == (startRow, startCol):
            distanceDict[coordinate] = 0
        else:
            #set to huge ass number
            distanceDict[coordinate] = 10**9


    previousDict = {}
    for coordinate in graph.nodes:
        #set all to None first
        previousDict[coordinate] = None

    while previousDict[(targetRow, targetCol)] == None:
        #Pick the unvisited node with the minimum distance
        bestcoordinate = pickshortestDistance(graph, distanceDict, targetRow, targetCol)
        

        #account for overlapping of character
        if bestcoordinate == None:
            return previousDict

        
        currentRow, currentCol = bestcoordinate[0], bestcoordinate[1]
        #we set the visited attribute to True
        graph.nodes[(currentRow, currentCol)].visited = True

        for move in possibleMoves:
            drow, dcol = move[0], move[1]
            newRow, newCol = currentRow + drow, currentCol + dcol
            if checkOutofBounds(graph, newRow, newCol):
                neighbourDist = distanceDict[(newRow, newCol)]
                compDist = distanceDict[(currentRow, currentCol)]  + graph.nodes[(newRow, newCol)].distance
                #update the distance
                if neighbourDist > compDist:
                    distanceDict[(newRow, newCol)] = compDist
                    previousDict[(newRow, newCol)] = (currentRow, currentCol)
                else:
                    continue

    return previousDict


def getshortestpathAstar(app, graph, Mazewalls, startplayernum, targetplayernum):
    pathDict = Astar(app, graph, Mazewalls, startplayernum, targetplayernum)
    targetplayer = app.players[targetplayernum]
    targetRow, targetCol = targetplayer.row, targetplayer.col
    path = []

    currentRow, currentCol = targetRow, targetCol

    while pathDict[(currentRow, currentCol)] != None:
        path.insert(0, (currentRow, currentCol))
        coordinate = pathDict[(currentRow, currentCol)]
        currentRow, currentCol = coordinate[0], coordinate[1]
    
    #only happens it overlap
    if path == []:
        return [(targetRow, targetCol)]
    return path

#tracks path to specific coordinate instead of a player
def AstarCoordinate(app, graph, Mazewalls, startplayernum, targetcoordinate):
    startplayer = app.players[startplayernum]
    startRow, startCol = startplayer.row, startplayer.col
    targetRow, targetCol = targetcoordinate[0], targetcoordinate[1]

    graph = initializeGraphforAstar(app, graph, Mazewalls)
    #initalizing the distance dictionary
    distanceDict = {}

    possibleMoves = [(0,1), (1,0), (-1,0), (0, -1)]
    
    for coordinate in graph.nodes:
        if coordinate == (startRow, startCol):
            distanceDict[coordinate] = 0
        else:
            #set to huge ass number
            distanceDict[coordinate] = 10**6


    previousDict = {}
    for coordinate in graph.nodes:
        #set all to None first
        previousDict[coordinate] = None

    while previousDict[(targetRow, targetCol)] == None:
        #Pick the unvisited node with the minimum distance
        bestcoordinate = pickshortestDistance(graph, distanceDict, targetRow, targetCol)
        

        #account for overlapping of character
        if bestcoordinate == None:
            return previousDict

        
        currentRow, currentCol = bestcoordinate[0], bestcoordinate[1]
        #we set the visited attribute to True
        graph.nodes[(currentRow, currentCol)].visited = True

        for move in possibleMoves:
            drow, dcol = move[0], move[1]
            newRow, newCol = currentRow + drow, currentCol + dcol
            if checkOutofBounds(graph, newRow, newCol):
                neighbourDist = distanceDict[(newRow, newCol)]
                compDist = distanceDict[(currentRow, currentCol)]  + graph.nodes[(newRow, newCol)].distance
                #update the distance
                if neighbourDist > compDist:
                    distanceDict[(newRow, newCol)] = compDist
                    previousDict[(newRow, newCol)] = (currentRow, currentCol)
                else:
                    continue

    return previousDict


#gets path to a specific coordinate instead of a player
def getAstarCoordinatePath(app, graph, Mazewalls, startplayernum, targetcoordinate):
    pathDict = AstarCoordinate(app, graph, Mazewalls, startplayernum, targetcoordinate)
    targetRow, targetCol = targetcoordinate[0], targetcoordinate[1]
    path = []

    currentRow, currentCol = targetRow, targetCol

    while pathDict[(currentRow, currentCol)] != None:
        path.insert(0, (currentRow, currentCol))
        coordinate = pathDict[(currentRow, currentCol)]
        currentRow, currentCol = coordinate[0], coordinate[1]
    return path



    

                




    
    