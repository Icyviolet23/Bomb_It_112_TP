#Initial Code for the term project


from cmu_112_graphics import *
import player
import random
import math
import wall
import Maze

def appStarted(app):
    app.mode = 'gameMode'
    app.panel = 480
    app.columns = 16
    app.rows = 16
    app.margin = 10
    #adjustment for the panel
    app.shift = app.panel + app.margin
    gamegraphics(app)

def getCellBounds(app, row, col):
    cellWidth = (app.width - app.panel - 2*app.margin)/app.columns
    cellHeight = (app.height - 2*app.margin)/app.rows
    x0 = col * cellWidth
    y0 = row* cellHeight
    x1 = (col + 1) * cellWidth
    y1 = (row + 1) * cellHeight
    return x0, y0, x1, y1
    
#########################################################
#GameMode
#Creating the Board
#15x15
#Margin on the left to place player information and score

def gamegraphics(app):
    #########################################################
    #Sample Klee model
    #https://www.deviantart.com/chiibits/art/Klee-Walking-Sprite-872586364
    app.klee = app.loadImage('Images\KleeSprite.png')
    app.kleesprite = []
    #modified from https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html
    # for i in range(32):
    #     sprite = app.klee.crop((30+26*i, 30, 230+26*i, 250))
    #     app.kleesprite.append(sprite)
    # app.spriteCounter = 0


def initializeMaze(app):
    graph = Maze.recursiveBacktrackingMaze()
    Maze.convertX(graph,2)
    for coordinate in graph.nodes:
        if len(graph.nodes[coordinate].edges) != 0:

def drawMaze(app, canvas):
    graph = Maze.recursiveBacktrackingMaze()
    Maze.convertX(graph,2)


def drawKlee(app, canvas):
    sprite = app.kleesprite[app.spriteCounter]
    #print(app.kleesprite)
    canvas.create_image(app.width/2, app.height/2, image=ImageTk.PhotoImage(sprite))

def drawgrid(app, canvas):
    for row in range(app.rows):
        for col in range(app.columns):
            x0, y0, x1, y1 = getCellBounds(app, row, col)
            canvas.create_rectangle(x0 + app.shift, y0 + app.margin, x1 + app.shift, y1 + app.margin)

def timerFired(app):
    app.spriteCounter = (1 + app.spriteCounter) % len(app.kleesprite)

def gameMode_keyPressed(app, event):
    pass

def gameMode_mousePressed(app, event):
    pass

def gameMode_redrawAll(app,canvas):
    drawgrid(app, canvas)
    #drawKlee(app, canvas)

#########################################################
def runGame():
    runApp(width= 1500, height= 1000)


runGame()