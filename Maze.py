#code for maze generation

import random
import math
import copy


# Note: I got inspired to create a graph class and node class after attending the graph mini TA lecture but all the code below
# is written personally by me unless otherwise stated
class Graph(object):
    def __init__(self, row, col):
        self.rows = row
        self.cols = col
        #dict containing of all the nodes
        #format is instance Node(x,y) : {set containing all nodes connected to this node}
        self.nodes = {}
        self.generateNodes()

        #place the traps here
        self.traps = set([])
                                                                    
    #initializing node dictionary where there are initially no edges
    def generateNodes(self):
        for row in range(self.rows):
            for col in range(self.cols):
                #each dictionary key is tagged to a Node instance
                #each Node instance contains a list of all the other points that this node is tagged to
                self.nodes[(row, col)] = Node(row,col)

    def __repr__(self):
        return f'{self.nodes}'

    def addEdge(self, row, col, addnode):
        self.nodes[(row, col)].edges.append(addnode)
    
    def removeEdge(self, row, col, removenode):
        self.nodes[(row, col)].edges.remove(removenode)
                
class Node(object):
    def __init__(self, row, col):
        self.row = row
        self.col = col
        #check whether the node has been visited
        self.visited = False
        #List containing all points that this node is connected to
        self.edges = []
        #this will be the weight used for Astar
        self.distance = 1

    def updateRow(self, num):
        self.row = self.row * num
    
    def updateCol(self, num):
        self.col = self.col * num

    #returns a copy of the node instance with scaled coordinates
    #also updates the edges list in that node instance
    def updatedCopy(self, num):
        result = copy.deepcopy(self)
        result.updateCol(num)
        result.updateRow(num)
        updatedEdgeList = []
        #.edges contains list of instances of nodes which are connected
        for edge in result.edges:
            new = copy.deepcopy(edge)
            new.updateCol(num)
            new.updateRow(num)
            updatedEdgeList.append(new)
        result.edges = updatedEdgeList
        return result

    #from https://www.cs.cmu.edu/~112/notes/notes-oop-part4.html
    def getHashables(self):
        return (self.row, self.col) # return a tuple of hashables
    #from https://www.cs.cmu.edu/~112/notes/notes-oop-part4.html
    def __hash__(self):
        return hash(self.getHashables())
    #from https://www.cs.cmu.edu/~112/notes/notes-oop-part4.html
    def __eq__(self, other):
        return (isinstance(other, Node) and (self.row == other.row) and (self.col == other.col))


##Recursive Backtracking Maze Generator
#Generates half of the graph dimensions
def recursiveBacktrackingMaze(row, col):
    #initialize graph
    graph = Graph(row, col)
    startRow = 0
    startCol = 0
    createMazeRecursively(graph, startRow, startCol)
    #print(graph.nodes)
    convertX(graph,2)
    return graph
    
def checkVisitedallNodes(graph):
    for coordinate in graph.nodes:
        if graph.nodes[coordinate].visited == False:
            return False
    return True

def checkOutofBounds(graph, row, col):
    rows = graph.rows
    cols = graph.cols
    if row < 0 or col < 0  or row >= rows or col >= cols:
        return False
    return True


def createMazeRecursively(graph, startRow, startCol):
    if checkVisitedallNodes(graph):
        return graph
    else:
        #set node to visited
        graph.nodes[(startRow, startCol)].visited = True
        dRow = random.randint(0,1)
        possibleMoves = [(0,1), (1,0), (-1,0), (0, -1)]
        random.shuffle(possibleMoves)
        for move in possibleMoves:
            dRow, dCol = move[0], move[1]
            newRow, newCol = startRow + dRow, startCol + dCol
            if checkOutofBounds(graph, newRow, newCol) and graph.nodes[(newRow, newCol)].visited != True:
                newNode = Node(newRow, newCol)
                #creating the edge
                graph.addEdge(startRow, startCol, newNode)
                solution = createMazeRecursively(graph, newRow, newCol)
                if solution != None:
                    return solution
                #backtracking
                #graph.nodes[(startRow, startCol)].visited = False
                #graph.removeEdge(startRow, startCol, newNode)
        return None
            
#recursiveBacktrackingMaze()    

#connects those nodes that have edges in between
def fillinEdges(newDict):
    for coordinate in newDict:
        if coordinate[0] % 2 == 0 and coordinate[1] % 2 == 0:
            baseRow = coordinate[0]
            baseCol = coordinate[1]
            if newDict[coordinate].edges != []:
                for edge in newDict[coordinate].edges:
                    dRow = (edge.row - baseRow) / 2
                    dCol = (edge.col - baseCol) / 2
                    newRow = dRow + baseRow
                    newCol = dCol + baseCol
                    newDict[(newRow, newCol)].edges.append(newDict[coordinate])

#convert nxn maze to 2nx2n maze
def convertX(graph, num):
    newDict = {}
    rows = 2*graph.rows
    cols = 2*graph.cols

    for coordinate in graph.nodes:
        newCoordinates = ((coordinate)[0] * num, (coordinate)[1] * num)
        UpdatedNode = graph.nodes[coordinate].updatedCopy(num)
        ##issue for code is here cause the method returns none
        newDict[(newCoordinates)] = UpdatedNode
    

    for row in range(rows):
        for col in range(cols):
            if (row,col) not in newDict:
                newDict[(row,col)] = Node(row, col)


    fillinEdges(newDict)

    #updating dimensions of the graph
    graph.rows = num*graph.rows
    graph.cols = num*graph.cols
    graph.nodes = newDict
    #reset the visited status for all the nodes in the graph
    resetVisitedStatusNode(graph)

def resetVisitedStatusNode(graph):
    for coordinate in graph.nodes:
        graph.nodes[coordinate].visited = False
        #print(f'{coordinate}, {graph.nodes[coordinate].visited}')




    #debugging
    '''
    for key in newDict:
        if key != (newDict[key].row, newDict[key].col):
            print('SAD')
        print(f'{key}: Row: {newDict[key].row} Col: {newDict[key].col} Edge = {len(newDict[key].edges)}')
        for edge in newDict[key].edges:
            if edge.row % 2 == 1 or edge.col % 2 == 1:
                print('SAD')
            #print(f'Key: {key} Edge Row: {edge.row}, Edge Col: {edge.col}')
    #for coordinate in graph.nodes:
        #print(f'{coordinate}: Row: {graph.nodes[coordinate].rows}, Col: {graph.nodes[coordinate].cols}')
    '''

def sampleDrawing():
    graph = recursiveBacktrackingMaze(8,8)
    convertX(graph,2)
    sampleboard = [[0] * 16 for _ in range(16)]
    for coordinate in graph.nodes:
        if len(graph.nodes[coordinate].edges) != 0:
            #print(f'coordinate = {coordinate}: Length: {len(graph.nodes[coordinate].edges)}, len(EdgeRow = {graph.nodes[coordinate].edges[0].row} : EdgeCol = {graph.nodes[coordinate].edges[0].col}' )
            row = coordinate[0]
            col = coordinate[1]
            #if row % 2 == 0:
            sampleboard[row][col] = 1
    print2dList(sampleboard)
    

#sampleDrawing()

#https://www.cs.cmu.edu/~112/notes/notes-2d-lists.html#printing
def repr2dList(L):
    if (L == []): return '[]'
    output = [ ]
    rows = len(L)
    cols = max([len(L[row]) for row in range(rows)])
    M = [['']*cols for row in range(rows)]
    for row in range(rows):
        for col in range(len(L[row])):
            M[row][col] = repr(L[row][col])
    colWidths = [0] * cols
    for col in range(cols):
        colWidths[col] = max([len(M[row][col]) for row in range(rows)])
    output.append('[\n')
    for row in range(rows):
        output.append(' [ ')
        for col in range(cols):
            if (col > 0):
                output.append(', ' if col < len(L[row]) else '  ')
            output.append(M[row][col].rjust(colWidths[col]))
        output.append((' ],' if row < rows-1 else ' ]') + '\n')
    output.append(']')
    return ''.join(output)

def print2dList(L):
    print(repr2dList(L))






#inspired from https://www.geeksforgeeks.org/union-find/
#inspired from https://weblog.jamisbuck.org/2011/1/3/maze-generation-kruskal-s-algorithm
#code is written by myself. Algorithm idea was inspired by above
#a little wonky for now need to edit

#note that this bag contains the borders which we do not use

#check if edge is on the border
def checkBorder(graph, node1, node2):
    row1, col1 = node1[0], node1[1]
    row2, col2 = node2[0], node2[1]
    if (row1 == 0 and row2 == 0) or (col1 == 0 and col2 == 0):
        return False
    if (row1 == graph.rows and row2 == graph.rows) or (col1 == graph.cols and col2 == graph.cols):
        return False
    return True

def createBagofEdges(graph):
    possibleMoves = [(0,1), (1,0), (-1,0), (0, -1)]
    #we represent the edges in form [(x0,y0), (x1,y1)]
    #need to check if the reverse is inside
    bagofEdges = []
    for row in range(graph.rows + 1):
        for col in range(graph.cols + 1):
            for move in possibleMoves:
                drow, dcol = move[0], move[1]
                newRow, newCol = drow + row, dcol + col
                if checkOutofBounds(graph, newRow, newCol):
                    node1 = (row,col)
                    node2 = (newRow, newCol)
                    if checkBorder(graph, node1, node2):
                        edge = [node1, node2]
                        reversededge = [node2, node1]
                        #avoid double counting
                        if reversededge not in bagofEdges:
                            bagofEdges.append(edge)

    return bagofEdges

#get the 2 nodes blocked by this edge
def get2Nodes(edge):
    row1, col1 = edge[0][0], edge[0][1]
    row2, col2 = edge[1][0], edge[1][1]
    minRow, minCol = min(row1, row2), min(col1, col2)
    maxRow, maxCol = max(row1, row2), max(col1, col2)
    #we flip to add
    dcol, drow = minRow - maxRow, minCol - maxCol
    finalrow, finalcol = minRow + drow, minCol + dcol
    return ((minRow, minCol), (finalrow, finalcol))


def testingget2Nodes():
    print(get2Nodes([(2,1),(3,1)]))
    print(get2Nodes([(3,1), (2,1)]))
    print(get2Nodes([(2,2), (2,3)]))
    pass

#testingget2Nodes()
#we want to define a bijection from [graph.cols] \right arrow {all vertexs in the graph}
#this function converts a coordinate into a natural number
def getIndex(graph, node):
    #number of rows
    width = graph.rows
    row, col = node.row, node.col
    return (row * width + col)

def initalizeParent(graph):
    parent = []
    for row in range(graph.rows):
        for col in range(graph.cols):
            parent.append((row,col))
    return parent

#check if have the same parent
#return True if they have different parents so we can merge

def checkParent(graph, parent, node1, node2):
    parent1 = returnParent(graph, parent, node1)
    parent2 = returnParent(graph, parent, node2)
    if parent1 == parent2:
        return False
    return True

def returnParent(graph, parent, node):
    parentNode = parent[getIndex(graph, node)]
    #if parent is itself
    if parentNode == (node.row, node.col):
        #return parent
        return node
    #recursive case
    else:
        return returnParent(graph, parent, graph.nodes[parentNode])

def kruskalMazeGeneration(row, col):
    graph = Graph(row,col)
    bagofEdges = createBagofEdges(graph)
    #print(bagofEdges)
    # for edge in bagofEdges:
    #     check = list(reversed(edge))
    #     if check in bagofEdges:
    #         print('error')
    #creating parent array
    parent = initalizeParent(graph)
    while len(bagofEdges) > 0:
        randomChoice = random.randint(0, len(bagofEdges) - 1)
        randomEdge = bagofEdges.pop(randomChoice)
        coordinate1, coordinate2 = get2Nodes(randomEdge)[0], get2Nodes(randomEdge)[1]
        node1, node2 = graph.nodes[coordinate1], graph.nodes[coordinate2]
        #print(f'{len(node1.edges)}, {len(node2.edges)}, {node2.edges[0].row, node2.edges[0].col}')
        if checkParent(graph, parent, node1, node2):
            #if they have different parents
            #we want to merge the parents together
            parent1 = returnParent(graph, parent, node1)
            parent2 = returnParent(graph, parent, node2)
            graph.addEdge(parent1.row, parent1.col, parent2)
            parent[getIndex(graph, parent1)] = (parent2.row, parent2.col)
        else:
            continue

    #print(set(parent))
    convertX(graph,2)
    return graph

    '''
    sorted = 0
    #we want to stop when sorted = nxm -1
    graph = Graph(row, col)
    #we initialize the graph with nodes using an 8x8 matrix
    #we only want to connect the nodes within a cross distance to ensure no funny wall combinations
    possibleMoves = [(0,1), (1,0), (-1,0), (0, -1)]
    #print(graph.nodes.keys())

    while sorted < graph.rows* graph.cols - 1:
        randRow1 = random.randint(0,graph.rows-1)
        randCol1 = random.randint(0,graph.cols-1)
        #random.shuffle(possibleMoves)
        #we bind the move within the cross
        randchoice = random.randint(0,3)
        move = possibleMoves[randchoice]
        randRow2 = randRow1 + move[0]
        randCol2 = randRow2 + move[1]
        #check if the 2nd row and col is within bounds of the graph
        if checkOutofBounds(graph, randRow2, randCol2):
            if (randRow1, randCol1) == (randRow2,randCol2):
                continue

            parent1 = checkParent(graph.nodes[(randRow1, randCol1)])
            #print(parent1.row, parent1.col)
            parent2 = checkParent(graph.nodes[(randRow2, randCol2)])
            #if the parents are the same we know that the edges are connected so we skip
            if parent1 == parent2:
                continue
            else:
                graph.addEdge(randRow1, randCol1, graph.nodes[(randRow2, randCol2)])
                sorted += 1

    convertX(graph,2)
    return graph
    '''
        
def testKruskal():
    graph = kruskalMazeGeneration(8,8)
    #convertX(graph,2)
    board = [[1]*graph.rows for _ in range(graph.cols)]
    for row in range(graph.rows):
        for col in range(graph.cols):
            if len(graph.nodes[(row,col)].edges) >= 1:
                board[row][col] = 0

    print2dList(board)


#testKruskal()

#pseudo code from 
# https://hurna.io/academy/algorithms/maze_generator/prim_s.html
# Choose a starting cell in the field and add it to the path set.
# While there is cell to be handled in the set:
# 1. Randomly connect to one of the already connected neighbor.
# 2. Add all unconnected neighbors to the set

def PrimMazeGeneration(row, col):
    graph = Graph(row, col)
    possibleMoves = [(0,1), (1,0), (-1,0), (0, -1)]
    startset = [(0,0)]

    #contains all the vertexes

    while len(startset) != 0:
        #randomchoice = random.randint(0, len(startset) - 1)
        chosenVertex = startset.pop()
        #print(chosenVertex)
        #mark as visited
        graph.nodes[chosenVertex].visited = True
        neighbours = []
        #finding neighbours
        for move in possibleMoves:
            newRow, newCol = chosenVertex[0] + move[0], chosenVertex[1] + move[1]

            if checkOutofBounds(graph, newRow, newCol) and graph.nodes[(newRow, newCol)].visited != True:

                neighbours.append((newRow, newCol))
        

        if neighbours != []:
            randomNeighbourChoice = random.randint(0, len(neighbours) - 1)
            randomNeighbour = neighbours[randomNeighbourChoice]
            #form the connections
            graph.addEdge(chosenVertex[0], chosenVertex[1], graph.nodes[(randomNeighbour)])

            for coordinate in neighbours:
                startset.append(coordinate)

        else:
            continue
    
    convertX(graph,2)
    return graph



def testPrim():
    graph = PrimMazeGeneration(8,8)
    convertX(graph,2)
    board = [[1]*graph.rows for _ in range(graph.cols)]
    for row in range(graph.rows):
        for col in range(graph.cols):
            if len(graph.nodes[(row,col)].edges) >= 1:
                board[row][col] = 0

    print2dList(board)


#testPrim()


        







