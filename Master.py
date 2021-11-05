#Initial Code for the term project


from cmu_112_graphics import *
import random
import math

def appStarted(app):
    app.mode = 'gameMode'
    app.panel = 480
    app.columns = 15
    app.rows = 15
    app.margin = 10
    #adjustment for the panel
    app.shift = app.panel + app.margin

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
#########################################################

def drawgrid(app, canvas):
    for row in range(app.rows):
        for col in range(app.columns):
            x0, y0, x1, y1 = getCellBounds(app, row, col)
            canvas.create_rectangle(x0 + app.shift, y0 + app.margin, x1 + app.shift, y1 + app.margin)

def gameMode_keyPressed(app, event):
    pass

def gameMode_mousePressed(app, event):
    pass

def gameMode_redrawAll(app,canvas):
    drawgrid(app, canvas)


def runGame():
    runApp(width= 1500, height= 1000)


runGame()