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
    app.timeElasped = 0
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

    app.MazeWalls = []
    initializeMaze(app)
    #modified from https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html

    # dictionary containing all the paths of the images of the walls
    
    initalizeKleeForward(app)
    intializeTreeImages(app)
    initializeImage(app)
    app.player1pos = [(0,0)]

def initalizeKleeForward(app):
    app.KleespriteCounter = 0
    #Klee model (forward walking)
    #https://www.deviantart.com/chiibits/art/Klee-Walking-Sprite-872586364
    app.kleeSpriteSheet = app.loadImage('Images\Klee\kleeForwardAnimation.png')
    #modified from https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html
    imageWidth, imageHeight = app.kleeSpriteSheet.size
    print(imageWidth, imageHeight)
    app.KleescaleWidthFactor = app.cellWidth / imageWidth
    app.KleescaleHeightFactor = app.cellHeight / imageHeight
    app.kleesprite = []
    for i in range(10):
        if i <= 4:
            sprite = app.kleeSpriteSheet.crop((imageWidth/5*i, 0, imageWidth/5*i + imageWidth/5, imageHeight/2))
            sprite = app.scaleImage(sprite, app.KleescaleHeightFactor*1.7)
            app.kleesprite.append(sprite)
        else:
            i = i % 5
            sprite = app.kleeSpriteSheet.crop((imageWidth/5*i, imageHeight/2, imageWidth/5*i + imageWidth/5, imageHeight))
            sprite = app.scaleImage(sprite, app.KleescaleHeightFactor*1.7)
            app.kleesprite.append(sprite)

    



def intializeTreeImages(app):
    # All tree images from 
    # https://stardewcommunitywiki.com/Category:Tree_images
    app.tree1 = app.loadImage('Images\\trees\\tree1.png')
    app.tree2 = app.loadImage('Images\\trees\\tree2.png')
    app.tree3 = app.loadImage('Images\\trees\\tree3.png')
    app.tree4 = app.loadImage('Images\\trees\\tree4.png')
    app.ImageDict = {
        0 : app.tree1,
        1 : app.tree2,
        2 : app.tree3,
        3 : app.tree4
    }


def initializeMaze(app):
    graph = Maze.recursiveBacktrackingMaze(8, 8)
    forbiddenCoordinates = set([(0,0), (0, app.rows-1), (app.columns-1, 0), (app.rows-1, app.columns-1)])
    Maze.convertX(graph,2)
    for coordinate in graph.nodes:
        if len(graph.nodes[coordinate].edges) == 0:
            if coordinate not in forbiddenCoordinates:
                newWall = wall.Wall(coordinate[0], coordinate[1], True)
                app.MazeWalls.append(newWall)

def initializeImage(app):
    app.ImageDictScaled = {}
    for image in app.ImageDict:
        imageWidth, imageHeight = app.tree1.size
        scaleWidthFactor = app.cellWidth / imageWidth
        scaleHeightFactor = app.cellHeight / imageHeight
        #app.treescale = app.scaleImage(app.tree1, scaleHeightFactor)
        app.ImageDictScaled[image] = app.scaleImage(app.ImageDict[image], scaleHeightFactor)


def gameMode_timerFired(app):
    #https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html#spritesheetsWithCropping


    app.timeElasped += app.timerDelay
    if app.timeElasped % 1000:
        app.KleespriteCounter += 1
        if app.KleespriteCounter >= len(app.kleesprite):
            app.KleespriteCounter = 0
    #app.KleespriteCounter = (1 + app.KleespriteCounter) % len(app.kleesprite)


def gameMode_keyPressed(app, event):
    #press r to reset the maze
    if event.key == 'r':
        regenerateWalls(app)

def regenerateWalls(app):
    app.MazeWalls = []
    initializeMaze(app)

def gameMode_mousePressed(app, event):
    pass


#######################################################################################################################################
#Drawing Functions
def drawWallImage(app, canvas):
    for wall in app.MazeWalls:
        image = wall.image
        #print(image)
        x0, y0, x1, y1 = getCellBounds(app, wall.row, wall.col)
        canvas.create_image((x1 + x0)/2 , (y1 + y0)/2, image=ImageTk.PhotoImage(app.ImageDictScaled[image]))

#using this for debugging
def drawMaze(app, canvas):
    for wall in app.MazeWalls:
        x0, y0, x1, y1 = getCellBounds(app, wall.row, wall.col)
        canvas.create_rectangle(x0, y0, x1, y1, fill = 'black')


def drawKlee(app, canvas):
    x0, y0, x1, y1 = getCellBounds(app, app.player1pos[0][0], app.player1pos[0][1])
    spriteimage = app.kleesprite[app.KleespriteCounter]
    canvas.create_image((x1 + x0)/2, (y1 + y0)/2, image=ImageTk.PhotoImage(spriteimage))

def drawgrid(app, canvas):
    for row in range(app.rows):
        for col in range(app.columns):
            x0, y0, x1, y1 = getCellBounds(app, row, col)
            canvas.create_rectangle(x0 , y0 , x1 , y1)
#######################################################################################################################################

def gameMode_redrawAll(app,canvas):
    drawgrid(app, canvas)
    #drawMaze(app, canvas)
    drawWallImage(app, canvas)
    drawKlee(app, canvas)

#########################################################
def runGame():
    runApp(width= 1500, height= 1000)


runGame()