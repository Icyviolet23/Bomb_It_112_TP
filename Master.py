#Initial Code for the term project


from cmu_112_graphics import *
import player
import random
import math
import wall
import Maze
import weapon

def appStarted(app):
    app.mode = 'gameMode'
    app.panel = app.width/5
    app.columns = 12
    app.rows = 12
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

    app.MazeWalls = {}
    #modified from https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html

    # dictionary containing all the paths of the images of the walls
    initializePlayer(app)
    initializeMaze(app)
    initalizeKleeForward(app)
    intializeTreeImages(app)
    initializeImage(app)

def initializePlayer(app):
    player1 = player.Player(0,0,10, weapon.Bomb(5))
    #app.players is the dictionary containing instance of all the players
    app.players = {
        1 : player1
    }
    

def initalizeKleeForward(app):
    app.KleespriteCounter = 0
    #Klee model (forward walking)
    #https://www.deviantart.com/chiibits/art/Klee-Walking-Sprite-872586364
    app.kleeSpriteSheet = app.loadImage('Images\Klee\kleeForwardAnimation.png')
    #modified from https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html
    imageWidth, imageHeight = app.kleeSpriteSheet.size
    #print(imageWidth, imageHeight)
    app.KleescaleWidthFactor = app.cellWidth / imageWidth
    app.KleescaleHeightFactor = app.cellHeight / imageHeight
    app.kleesprite = []
    for i in range(10):
        if i <= 4:
            sprite = app.kleeSpriteSheet.crop((imageWidth/5*i, 0, imageWidth/5*i + imageWidth/5, imageHeight/2))
            sprite = app.scaleImage(sprite, app.KleescaleHeightFactor*1.9)
            app.kleesprite.append(sprite)
        else:
            i = i % 5
            sprite = app.kleeSpriteSheet.crop((imageWidth/5*i, imageHeight/2, imageWidth/5*i + imageWidth/5, imageHeight))
            sprite = app.scaleImage(sprite, app.KleescaleHeightFactor*1.9)
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


def initializeWeapons(app):
    #Bomb from https://www.google.com/url?sa=i&url=http%3A%2F%2Fclipart-library.com%2Fbomb-cliparts.html&psig=AOvVaw0MGEiKDcFcUDWUnBx5BprH&ust=1637106597396000&source=images&cd=vfe&ved=0CAsQjRxqFwoTCOiBhtLHm_QCFQAAAAAdAAAAABAO
    app.bomb = app.loadImage('Images\\weapons\\bombnobg.png"')
    app.weaponDict = {
        0 : app.bomb
    }
def checkplayerposition(app, coordinate):
    for player in app.players:
        if coordinate == (app.players[player].row,app.players[player].col):
            return False
    return True

def initializeMaze(app):
    graph = Maze.recursiveBacktrackingMaze(app.rows//2, app.columns//2)
    forbiddenCoordinates = set([(0,0), (0, app.rows-1), (app.columns-1, 0), (app.rows-1, app.columns-1)])
    Maze.convertX(graph,2)
    for coordinate in graph.nodes:
        if len(graph.nodes[coordinate].edges) == 0:
            if coordinate not in forbiddenCoordinates and checkplayerposition(app, coordinate):
                newWall = wall.Wall(coordinate[0], coordinate[1], True)
                app.MazeWalls[coordinate] = newWall


def initializeImage(app):
    app.ImageDictScaled = {}
    for image in app.ImageDict:
        imageWidth, imageHeight = app.tree1.size
        #scaleWidthFactor = app.cellWidth / imageWidth
        scaleHeightFactor = app.cellHeight / imageHeight
        #app.treescale = app.scaleImage(app.tree1, scaleHeightFactor)
        app.ImageDictScaled[image] = app.scaleImage(app.ImageDict[image], scaleHeightFactor)
#end of initialization functions
#################################################################
#check if any move is out of bounds
def checkBounds(app, row, col):
    rows, cols = app.rows, app.columns
    if row < 0 or col < 0 or row >= rows or col >= cols:
        return False
    return True

#check if there is any collion with a wall
def checkCollison(app, row, col):
    for wall in app.MazeWalls:
        if (row, col) == wall:
            return False
    return True


def movePlayer(app, drow, dcol, playernum):
    newRow, newCol = app.players[playernum].row + drow, app.players[playernum].col + dcol
    if checkCollison(app, newRow, newCol) and checkBounds(app, newRow, newCol):
        app.players[playernum].row = newRow
        app.players[playernum].col = newCol
    else:
        pass



def gameMode_timerFired(app):
    #https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html#spritesheetsWithCropping


    app.timeElasped += app.timerDelay
    if app.timeElasped % 1000:
        app.KleespriteCounter += 1
        if app.KleespriteCounter >= len(app.kleesprite):
            app.KleespriteCounter = 0
    #app.KleespriteCounter = (1 + app.KleespriteCounter) % len(app.kleesprite)
    #movePlayer(app, drow, dcol, playernum)


def gameMode_keyPressed(app, event):
    #press r to reset the maze
    if event.key == 'r':
        regenerateWalls(app)

    if event.key == 'Right':
        movePlayer(app, 0, 1, 1)

    if event.key == 'Left':
        movePlayer(app, 0, -1, 1)

    if event.key == 'Up':
        movePlayer(app, -1, 0, 1)

    if event.key == 'Down':
        movePlayer(app, 1, 0, 1)

def regenerateWalls(app):
    app.MazeWalls = {}
    initializeMaze(app)

def gameMode_mousePressed(app, event):
    pass


#######################################################################################################################################
#Drawing Functions
def drawWallImage(app, canvas):
    for wall in app.MazeWalls:
        image = app.MazeWalls[wall].image
        #print(image)
        x0, y0, x1, y1 = getCellBounds(app, app.MazeWalls[wall].row, app.MazeWalls[wall].col)
        canvas.create_image((x1 + x0)/2 , (y1 + y0)/2, image=ImageTk.PhotoImage(app.ImageDictScaled[image]))

#using this for debugging
def drawMaze(app, canvas):
    for wall in app.MazeWalls:
        x0, y0, x1, y1 = getCellBounds(app, app.MazeWalls[wall].row, app.MazeWalls[wall].col)
        canvas.create_rectangle(x0, y0, x1, y1, fill = 'black')

#playernum here is an int
def drawKlee(app, canvas, playernum):
    x0, y0, x1, y1 = getCellBounds(app, app.players[playernum].row, app.players[playernum].col)
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
    drawKlee(app, canvas, 1)

#########################################################
def runGame():
    runApp(width= 1500, height= 800)


runGame()