import random
import math
import copy

class Graph(object):
    def __init__(self, row, col):
        self.rows = row
        self.cols = col
        #dict containing of all the nodes
        #format is instance Node(x,y) : {set containing all nodes connected to this node}
        self.nodes = {}
        self.generateNodes()
                                                                    
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

    def updateRow(self, num):
        self.row = self.row * num
    
    def updateCol(self, num):
        self.col = self.col * num

    def updateEdge(self, num):
        result = []
        #returns new instance
        for edge in self.edges:
            new = copy.deepcopy(edge)
            new.updateCol(num)
            new.updateRow(num)
            result.append(new)
        self.edges = result
            


class Wall(object):
    def __init__(self, image, destructible):
        self.image = image
        #this will be a boolean value
        #true if destructible, false if not
        self.destructible = destructible

##Recursive Backtracking Maze Generator
#Generates half of the graph dimensions
def recursiveBacktrackingMaze():
    #initialize graph
    graph = Graph(8, 8)
    startRow = 0
    startCol = 0
    createMazeRecursively(graph, startRow, startCol)
    #print(graph.nodes)
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


def convert2X(graph):
    newDict = {}
    for coordinate in graph.nodes:
        newnode = ((coordinate)[0] * 2, (coordinate)[1] * 2)
        newDict[(newnode)] = graph.nodes[coordinate].updateEdge(2)
    #graph.nodes = newDict

def sampleDrawing():
    graph = recursiveBacktrackingMaze()
    convert2X(graph)
    sampleboard = [[-1] * 16 for _ in range(16)]
    for coordinate in graph.nodes:
        if len(graph.nodes[coordinate].edges) != 0:
            #print(f'coordinate = {coordinate}: Length: {len(graph.nodes[coordinate].edges)}, len(EdgeRow = {graph.nodes[coordinate].edges[0].row} : EdgeCol = {graph.nodes[coordinate].edges[0].col}' )
            row = graph.nodes[coordinate].edges[0].row
            col = graph.nodes[coordinate].edges[0].col
            #if row % 2 == 0:
            sampleboard[row][col] = 0
    print2dList(sampleboard)

sampleDrawing()


    




