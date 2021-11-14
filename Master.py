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
    app.cellWidth = (app.width - app.panel - 2*app.margin)/app.columns
    app.cellHeight = (app.height - 2*app.margin)/app.rows
    gamegraphics(app)

def getCellBounds(app, row, col):
    x0 = col * app.cellWidth + app.shift
    y0 = row* app.cellHeight + app.margin
    x1 = (col + 1) * app.cellWidth + app.shift
    y1 = (row + 1) * app.cellHeight + app.margin
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
    app.MazeWalls = []
    initializeMaze(app)
    #modified from https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html
    # for i in range(32):
    #     sprite = app.klee.crop((30+26*i, 30, 230+26*i, 250))
    #     app.kleesprite.append(sprite)
    # app.spriteCounter = 0

    # dictionary containing all the paths of the images of the walls
    # All tree images from 
    # https://stardewcommunitywiki.com/Category:Tree_images
    app.tree1 = app.loadImage('Images\trees\tree2.png')
    
    app.ImageDict = {
        'tree1' : app.tree1
    }
    initializeImage(app)


def initializeMaze(app):
    graph = Maze.recursiveBacktrackingMaze(8, 8)
    Maze.convertX(graph,2)
    for coordinate in graph.nodes:
        if len(graph.nodes[coordinate].edges) == 0:
            newWall = wall.Wall(coordinate[0], coordinate[1], True)
            app.MazeWalls.append(newWall)

def initializeImage(app):
    app.ImageDictScaled = {}
    for image in app.ImageDict:
        imageWidth, imageHeight = app.ImageDict[image].size
        scaleWidthFactor = app.cellWidth / imageWidth
        scaleHeightFactor = app.cellHeight / imageHeight
        app.ImageDictScaled[image] = app.scaleImage(app.ImageDict[image], scaleHeightFactor)

def drawWallImage(app, canvas):
    for wall in app.MazeWalls:
        image = wall.image
        x0, y0, x1, y1 = getCellBounds(app, wall.row, wall.col)
        canvas.create_image((x1 + x0)/2 , (y1 + y0)/2, image=ImageTk.PhotoImage(app.ImageDictScaled[image]))

def drawMaze(app, canvas):
    for wall in app.MazeWalls:
        x0, y0, x1, y1 = getCellBounds(app, wall.row, wall.col)
        canvas.create_rectangle(x0, y0, x1, y1, fill = 'black')


def drawKlee(app, canvas):
    sprite = app.kleesprite[app.spriteCounter]
    #print(app.kleesprite)
    canvas.create_image(app.width/2, app.height/2, image=ImageTk.PhotoImage(sprite))

def drawgrid(app, canvas):
    for row in range(app.rows):
        for col in range(app.columns):
            x0, y0, x1, y1 = getCellBounds(app, row, col)
            canvas.create_rectangle(x0 , y0 , x1 , y1)

def timerFired(app):
    app.spriteCounter = (1 + app.spriteCounter) % len(app.kleesprite)

def gameMode_keyPressed(app, event):
    pass

def gameMode_mousePressed(app, event):
    pass

def gameMode_redrawAll(app,canvas):
    drawgrid(app, canvas)
    #drawKlee(app, canvas)
    drawMaze(app, canvas)
    drawWallImage(app, canvas)

#########################################################
def runGame():
    runApp(width= 1500, height= 1000)


runGame()