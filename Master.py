#Initial Code for the term project

from cmu_112_graphics import *
import player
import random
import wall
import Maze
import weapon
import time
import AI

# Python Program to Convert seconds
# into hours, minutes and seconds
import time
#https://www.geeksforgeeks.org/python-program-to-convert-seconds-into-hours-minutes-and-seconds/
def convert(seconds):
    return time.strftime("%M:%S", time.gmtime(seconds))
      

#https://www.cs.cmu.edu/~112/schedule.html
def almostEqual(d1, d2, epsilon=10**-7):
    # note: use math.isclose() outside 15-112 with Python version 3.5 or later
    return (abs(d2 - d1) < epsilon)
#from HW3 from https://www.cs.cmu.edu/~112/schedule.html
def rgbString(red, green, blue):
     return f'#{red:02x}{green:02x}{blue:02x}'

def appStarted(app):
    gameparams(app)
    intializeTime(app)
    gamegraphics(app)
    initializeAI(app)

def gameparams(app):
    #fixed params for the game
    app.mode = 'gameMode'
    app.panel = app.width/5
    app.columns = 16
    app.rows = 16
    app.margin = 10
    #adjustment for the panel
    app.shift = app.panel + app.margin
    app.cellWidth = (app.width - app.panel - 2*app.margin)/app.columns
    app.cellHeight = (app.height - 2*app.margin)/app.rows
    #set timer for 5mins
    app.timer = 300
    app.gameover = False

    app.gamewin = False

    

def intializeTime(app):
    app.startTime = time.time()
    app.timeElasped = 0

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
    #for heart powerup
    intializeHeart(app)
   
    #modified from https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html

    # dictionary containing all the paths of the images of the walls
    initializePlayer(app)
    initializeWeaponPosition(app)
    initializeMaze(app)
    initalizeKleeForward(app)
    intializeWallImages(app)
    initializeFloorImage(app)
    initializeWeaponsImages(app)
    initializeExplosionSprite(app)
    intializeTraps(app)

    #other modes
    initializeGameoversprite(app)
    initializeGamewinsprite(app)
    
    
    

def initializePlayer(app):
    #player format is 
    #row, col, lives, weaponD, action
    player1 = player.Player(0, 0, 10, 1, 'forward')
    player2 = player.Player(0,app.columns - 1, 10, 1, 'forward')
    player3 = player.Player(app.rows - 1, 0, 10,1, 'forward')
    player4 = player.Player(app.rows - 1, app.columns -1, 10, 1, 'forward')
    #app.players is the dictionary containing instance of all the players
    app.players = {
        1 : player1,
        2 : player2,
        3 : player3,
        4 : player4

    }
    initializeAllPlayerModels(app)
    
    
####################################################################################
#player images
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
            app.kleesprite.append(ImageTk.PhotoImage(sprite))
        else:
            i = i % 5
            sprite = app.kleeSpriteSheet.crop((imageWidth/5*i, imageHeight/2, imageWidth/5*i + imageWidth/5, imageHeight))
            sprite = app.scaleImage(sprite, app.KleescaleHeightFactor*1.9)
            app.kleesprite.append(ImageTk.PhotoImage(sprite))


def initializeAllPlayerModels(app):
    initializePlayerModel1(app)
    initializePlayerModel2(app)
    initializePlayerModel3(app)
    initializePlayerModel4(app)
    app.playerModels = {
        1 : app.playerModel1Directions,
        2 : app.playerModel2Directions,
        3 : app.playerModel3Directions,
        4 : app.playerModel4Directions
    }

    app.playerColor = {
        1: 'green',
        2: 'red',
        3: 'orange',
        4: 'yellow'
    }


# Player Model 1 credits
# body/male/human/white.png	Stephen Challener (Redshrike), Johannes SjÃ¶lund (wulax)	CC-BY-SA 3.0, GPL 3.0	https://opengameart.org/content/liberated-pixel-cup-lpc-base-assets-sprites-map-tiles	https://opengameart.org/content/lpc-medieval-fantasy-character-sprites			
# facial/sunglasses.png	Michael Whitlock (bigbeargames), Thane Brimhall (pennomi)	CC-BY-SA 3.0, GPL 3.0	https://opengameart.org/content/lpc-base-character-expressions				
# feet/shoes/male/brown.png	Johannes SjÃ¶lund (wulax)	CC-BY-SA 3.0, GPL 3.0	https://opengameart.org/content/lpc-medieval-fantasy-character-sprites				
# legs/pantaloons/male/black.png	Nila122, Johannes Sj?lund (wulax), Stephen Challener (Redshrike)	CC-BY-SA 3.0, GPL 2.0, GPL 3.0	https://opengameart.org/content/lpc-pirates	https://opengameart.org/content/more-lpc-clothes-and-hair			
# torso/clothes/longsleeve_laced/male/black.png	bluecarrot16, David Conway Jr. (JaidynReiman), Johannes SjÃ¶lund (wulax)	CC-BY-SA 3.0, GPL 3.0	https://opengameart.org/content/lpc-medieval-fantasy-character-sprites	https://opengameart.org/content/lpc-pirates			
# hair/bangslong/male/black.png	Manuel Riecke (MrBeast)	CC-BY-SA 3.0, GPL 3.0	https://opengameart.org/content/lpc-medieval-fantasy-character-sprites				
# Note you can find an excel in the Images\Players folder for credits
def initializePlayerModel1(app):
    #dictionary that stores sprite sheets for different directions and actions
    app.playerModel1Directions = {
        'forward' : None,
        'backward' : None,
        'right' : None,
        'left' : None
    }
    
    app.playerModel1SpriteSheet = app.loadImage("Images\Players\player1.png")
    imageWidth, imageHeight = app.playerModel1SpriteSheet.size
    app.playerModelHeightfactor = app.cellHeight / imageHeight
    #max columns
    cols = 13
    #max rows
    rows = 21
    scalefactor = 23
    app.playerModel1Counter = 0

    #initializing forward sprite
    
    app.playerModel1forwardsprite = []
    forwardrow = 10
    for col in range(9):
        forwardsprite = app.playerModel1SpriteSheet.crop((imageWidth/cols*col, imageHeight/rows*forwardrow, imageWidth/cols*(col+1) , imageHeight/rows*(forwardrow+1)))
        forwardscaledsprite = app.scaleImage(forwardsprite, app.playerModelHeightfactor*scalefactor)
        app.playerModel1forwardsprite.append(ImageTk.PhotoImage(forwardscaledsprite))
    app.playerModel1Directions['forward'] = app.playerModel1forwardsprite

    #initializing backward sprite
    #app.playerModel1BackwardCounter = 0
    app.playerModel1backwardsprite = []
    backwardrow = 8
    for col in range(9):
        backwardsprite = app.playerModel1SpriteSheet.crop((imageWidth/cols*col, imageHeight/rows*backwardrow, imageWidth/cols*(col+1) , imageHeight/rows*(backwardrow+1)))
        backwardscaledsprite = app.scaleImage(backwardsprite, app.playerModelHeightfactor*scalefactor)
        app.playerModel1backwardsprite.append(ImageTk.PhotoImage(backwardscaledsprite))
    app.playerModel1Directions['backward'] = app.playerModel1backwardsprite

    #intializing left sprite
    #app.playerModel1LeftCounter = 0
    app.playerModel1leftsprite = []
    leftrow = 9
    for col in range(9):
        leftsprite = app.playerModel1SpriteSheet.crop((imageWidth/cols*col, imageHeight/rows*leftrow, imageWidth/cols*(col+1) , imageHeight/rows*(leftrow+1)))
        leftscaledsprite = app.scaleImage(leftsprite, app.playerModelHeightfactor*scalefactor)
        app.playerModel1leftsprite.append(ImageTk.PhotoImage(leftscaledsprite))
    app.playerModel1Directions['left'] = app.playerModel1leftsprite

    #intializing right sprite
    #app.playerModel1RightCounter = 0
    app.playerModel1rightsprite = []
    rightrow = 11
    for col in range(9):
        rightsprite = app.playerModel1SpriteSheet.crop((imageWidth/cols*col, imageHeight/rows*rightrow, imageWidth/cols*(col+1) , imageHeight/rows*(rightrow+1)))
        rightscaledsprite = app.scaleImage(rightsprite, app.playerModelHeightfactor*scalefactor)
        app.playerModel1rightsprite.append(ImageTk.PhotoImage(rightscaledsprite))
    app.playerModel1Directions['right'] = app.playerModel1rightsprite

#initalizing player2Model
#images from
# body/male/human/white.png		Stephen Challener (Redshrike), Johannes SjÃ¶lund (wulax)	CC-BY-SA 3.0, GPL 3.0	https://opengameart.org/content/liberated-pixel-cup-lpc-base-assets-sprites-map-tiles	https://opengameart.org/content/lpc-medieval-fantasy-character-sprites			
# feet/armor/male/9.png		Michael Whitlock (bigbeargames), Matthew Krohn (makrohn), Johannes SjÃ¶lund (wulax)	CC-BY-SA 3.0, GPL 3.0	https://opengameart.org/content/lpc-medieval-fantasy-character-sprites				
# legs/armour/male/9.png		Michael Whitlock (bigbeargames), Matthew Krohn (makrohn), Johannes SjÃ¶lund (wulax)	CC-BY-SA 3.0, GPL 3.0	https://opengameart.org/content/lpc-medieval-fantasy-character-sprites				
# torso/chainmail/male/gray.png		Johannes SjÃ¶lund (wulax)	CC-BY-SA 3.0, GPL 3.0	https://opengameart.org/content/lpc-medieval-fantasy-character-sprites				
# torso/armour/plate/male/16.png	recolor of torso/plate/chest_female.png	Michael Whitlock (bigbeargames), Matthew Krohn (makrohn), Johannes SjÃ¶lund (wulax)	CC-BY-SA 3.0, GPL 3.0	https://opengameart.org/content/lpc-medieval-fantasy-character-sprites	https://opengameart.org/content/lpc-combat-armor-for-women			
# shoulders/legion/male/bronze.png		Nila122, David Conway Jr. (JaidynReiman), Matthew Krohn (makrohn), Johannes SjÃ¶lund (wulax)	CC-BY-SA 3.0, GPL 2.0, GPL 3.0	https://opengameart.org/content/lpc-roman-armor				
# cape/solid/male/maroon.png		David Conway Jr. (JaidynReiman)	CC-BY-SA 3.0, GPL 3.0	https://opengameart.org/content/lpc-curly-hair-elven-ears-white-cape-with-blue-trim-and-more				
# cape/solid_behind/maroon.png		David Conway Jr. (JaidynReiman)	CC-BY-SA 3.0, GPL 3.0	https://opengameart.org/content/lpc-curly-hair-elven-ears-white-cape-with-blue-trim-and-more				
# hat/armour/3.png		Michael Whitlock (bigbeargames), Johannes SjÃ¶lund (wulax)	CC-BY-SA 3.0, GPL 3.0	https://opengameart.org/content/lpc-medieval-fantasy-character-sprites				
# Note you can find an excel in the Images\Players folder for credits
def initializePlayerModel2(app):
    #dictionary that stores sprite sheets for different directions and actions
    app.playerModel2Directions = {
        'forward' : None,
        'backward' : None,
        'right' : None,
        'left' : None
    }
    
    app.playerModel2SpriteSheet = app.loadImage("Images\Players\player2.png")
    imageWidth, imageHeight = app.playerModel2SpriteSheet.size
    app.playerModelHeightfactor = app.cellHeight / imageHeight
    #max columns
    cols = 13
    #max rows
    rows = 21
    scalefactor = 23
    app.playerModel2Counter = 0

    #initializing forward sprite
    
    app.playerModel2forwardsprite = []
    forwardrow = 10
    for col in range(9):
        forwardsprite = app.playerModel2SpriteSheet.crop((imageWidth/cols*col, imageHeight/rows*forwardrow, imageWidth/cols*(col+1) , imageHeight/rows*(forwardrow+1)))
        forwardscaledsprite = app.scaleImage(forwardsprite, app.playerModelHeightfactor*scalefactor)
        app.playerModel2forwardsprite.append(ImageTk.PhotoImage(forwardscaledsprite))
    app.playerModel2Directions['forward'] = app.playerModel2forwardsprite

    #initializing backward sprite
    #app.playerModel2BackwardCounter = 0
    app.playerModel2backwardsprite = []
    backwardrow = 8
    for col in range(9):
        backwardsprite = app.playerModel2SpriteSheet.crop((imageWidth/cols*col, imageHeight/rows*backwardrow, imageWidth/cols*(col+1) , imageHeight/rows*(backwardrow+1)))
        backwardscaledsprite = app.scaleImage(backwardsprite, app.playerModelHeightfactor*scalefactor)
        app.playerModel2backwardsprite.append(ImageTk.PhotoImage(backwardscaledsprite))
    app.playerModel2Directions['backward'] = app.playerModel2backwardsprite

    #intializing left sprite
    #app.playerModel2LeftCounter = 0
    app.playerModel2leftsprite = []
    leftrow = 9
    for col in range(9):
        leftsprite = app.playerModel2SpriteSheet.crop((imageWidth/cols*col, imageHeight/rows*leftrow, imageWidth/cols*(col+1) , imageHeight/rows*(leftrow+1)))
        leftscaledsprite = app.scaleImage(leftsprite, app.playerModelHeightfactor*scalefactor)
        app.playerModel2leftsprite.append(ImageTk.PhotoImage(leftscaledsprite))
    app.playerModel2Directions['left'] = app.playerModel2leftsprite

    #intializing right sprite
    #app.playerModel2RightCounter = 0
    app.playerModel2rightsprite = []
    rightrow = 11
    for col in range(9):
        rightsprite = app.playerModel2SpriteSheet.crop((imageWidth/cols*col, imageHeight/rows*rightrow, imageWidth/cols*(col+1) , imageHeight/rows*(rightrow+1)))
        rightscaledsprite = app.scaleImage(rightsprite, app.playerModelHeightfactor*scalefactor)
        app.playerModel2rightsprite.append(ImageTk.PhotoImage(rightscaledsprite))
    app.playerModel2Directions['right'] = app.playerModel2rightsprite


# body/male/human/white.png	Stephen Challener (Redshrike), Johannes SjÃ¶lund (wulax)	CC-BY-SA 3.0, GPL 3.0	https://opengameart.org/content/liberated-pixel-cup-lpc-base-assets-sprites-map-tiles	https://opengameart.org/content/lpc-medieval-fantasy-character-sprites			
# beards/male/beard/black.png	David Conway Jr. (JaidynReiman), Carlo Enrico Victoria (Nemisys)	CC-BY-SA 3.0, GPL 3.0	https://opengameart.org/content/lpc-brunet-mustache				
# facial/patch.png	Michael Whitlock (bigbeargames), Thane Brimhall (pennomi)	CC-BY-SA 3.0, GPL 3.0	https://opengameart.org/content/lpc-base-character-expressions				
# feet/shoes/male/maroon.png	Johannes SjÃ¶lund (wulax)	CC-BY-SA 3.0, GPL 3.0	https://opengameart.org/content/lpc-medieval-fantasy-character-sprites				
# legs/pants/male/sky.png	bluecarrot16, David Conway Jr. (JaidynReiman), Joe White, Matthew Krohn (makrohn), Johannes Sj?lund (wulax)	CC-BY-SA 3.0, GPL 3.0	https://opengameart.org/content/liberated-pixel-cup-lpc-base-assets-sprites-map-tiles	https://opengameart.org/content/lpc-medieval-fantasy-character-sprites			
# torso/clothes/vest_open/male/black.png	bluecarrot16, Thane Brimhall (pennomi), laetissima	CC-BY-SA 3.0, GPL 3.0	https://opengameart.org/content/lpc-2-characters	https://opengameart.org/content/lpc-gentleman	https://opengameart.org/content/lpc-pirates		
# hair/mohawk/male/black.png	Manuel Riecke (MrBeast)	CC-BY-SA 3.0, GPL 3.0	https://opengameart.org/content/liberated-pixel-cup-lpc-base-assets-sprites-map-tiles				
# hat/pirate/bandana_skull/male/blue.png	bluecarrot16, Fabzy	CC-BY-SA 3.0	https://opengameart.org/content/lpc-pirates				
# Note you can find an excel in the Images\Players folder for credits

def initializePlayerModel3(app):
    #dictionary that stores sprite sheets for different directions and actions
    app.playerModel3Directions = {
        'forward' : None,
        'backward' : None,
        'right' : None,
        'left' : None
    }
    
    app.playerModel3SpriteSheet = app.loadImage("Images\Players\player3.png")
    imageWidth, imageHeight = app.playerModel3SpriteSheet.size
    app.playerModelHeightfactor = app.cellHeight / imageHeight
    #max columns
    cols = 13
    #max rows
    rows = 21
    scalefactor = 23
    app.playerModel3Counter = 0

    #initializing forward sprite
    
    app.playerModel3forwardsprite = []
    forwardrow = 10
    for col in range(9):
        forwardsprite = app.playerModel3SpriteSheet.crop((imageWidth/cols*col, imageHeight/rows*forwardrow, imageWidth/cols*(col+1) , imageHeight/rows*(forwardrow+1)))
        forwardscaledsprite = app.scaleImage(forwardsprite, app.playerModelHeightfactor*scalefactor)
        app.playerModel3forwardsprite.append(ImageTk.PhotoImage(forwardscaledsprite))
    app.playerModel3Directions['forward'] = app.playerModel3forwardsprite

    #initializing backward sprite
    #app.playerModel3BackwardCounter = 0
    app.playerModel3backwardsprite = []
    backwardrow = 8
    for col in range(9):
        backwardsprite = app.playerModel3SpriteSheet.crop((imageWidth/cols*col, imageHeight/rows*backwardrow, imageWidth/cols*(col+1) , imageHeight/rows*(backwardrow+1)))
        backwardscaledsprite = app.scaleImage(backwardsprite, app.playerModelHeightfactor*scalefactor)
        app.playerModel3backwardsprite.append(ImageTk.PhotoImage(backwardscaledsprite))
    app.playerModel3Directions['backward'] = app.playerModel3backwardsprite

    #intializing left sprite
    #app.playerModel3LeftCounter = 0
    app.playerModel3leftsprite = []
    leftrow = 9
    for col in range(9):
        leftsprite = app.playerModel3SpriteSheet.crop((imageWidth/cols*col, imageHeight/rows*leftrow, imageWidth/cols*(col+1) , imageHeight/rows*(leftrow+1)))
        leftscaledsprite = app.scaleImage(leftsprite, app.playerModelHeightfactor*scalefactor)
        app.playerModel3leftsprite.append(ImageTk.PhotoImage(leftscaledsprite))
    app.playerModel3Directions['left'] = app.playerModel3leftsprite

    #intializing right sprite
    #app.playerModel3RightCounter = 0
    app.playerModel3rightsprite = []
    rightrow = 11
    for col in range(9):
        rightsprite = app.playerModel3SpriteSheet.crop((imageWidth/cols*col, imageHeight/rows*rightrow, imageWidth/cols*(col+1) , imageHeight/rows*(rightrow+1)))
        rightscaledsprite = app.scaleImage(rightsprite, app.playerModelHeightfactor*scalefactor)
        app.playerModel3rightsprite.append(ImageTk.PhotoImage(rightscaledsprite))
    app.playerModel3Directions['right'] = app.playerModel3rightsprite


# body/male/human/white.png		Stephen Challener (Redshrike), Johannes SjÃ¶lund (wulax)	CC-BY-SA 3.0, GPL 3.0	https://opengameart.org/content/liberated-pixel-cup-lpc-base-assets-sprites-map-tiles	https://opengameart.org/content/lpc-medieval-fantasy-character-sprites			
# facial/mask_white.png		Nila122	CC-BY-SA 3.0, GPL 2.0, GPL 3.0	https://opengameart.org/content/lpc-masks				
# facial/earring/male/gold.png		bluecarrot16	CC-BY-SA 3.0	https://opengameart.org/content/lpc-pirates				
# feet/shoes/male/black.png		Johannes SjÃ¶lund (wulax)	CC-BY-SA 3.0, GPL 3.0	https://opengameart.org/content/lpc-medieval-fantasy-character-sprites				
# torso/jacket/iverness/male/black.png		bluecarrot16	CC-BY-SA 3.0, GPL 3.0	https://opengameart.org/content/lpc-gentleman				
# hat/magic/male/moon.png		Michael Whitlock (bigbeargames), Tracy	OGA-BY 3.0	https://opengameart.org/content/lpc-celestial-wizard-hats	https://opengameart.org/content/merlins-hat			
# Note you can find an excel in the Images\Players folder for credits

def initializePlayerModel4(app):
    #dictionary that stores sprite sheets for different directions and actions
    app.playerModel4Directions = {
        'forward' : None,
        'backward' : None,
        'right' : None,
        'left' : None
    }
    
    app.playerModel4SpriteSheet = app.loadImage("Images\Players\player4.png")
    imageWidth, imageHeight = app.playerModel4SpriteSheet.size
    app.playerModelHeightfactor = app.cellHeight / imageHeight
    #max columns
    cols = 13
    #max rows
    rows = 21
    scalefactor = 23
    app.playerModel4Counter = 0

    #initializing forward sprite
    
    app.playerModel4forwardsprite = []
    forwardrow = 10
    for col in range(9):
        forwardsprite = app.playerModel4SpriteSheet.crop((imageWidth/cols*col, imageHeight/rows*forwardrow, imageWidth/cols*(col+1) , imageHeight/rows*(forwardrow+1)))
        forwardscaledsprite = app.scaleImage(forwardsprite, app.playerModelHeightfactor*scalefactor)
        app.playerModel4forwardsprite.append(ImageTk.PhotoImage(forwardscaledsprite))
    app.playerModel4Directions['forward'] = app.playerModel4forwardsprite

    #initializing backward sprite
    #app.playerModel4BackwardCounter = 0
    app.playerModel4backwardsprite = []
    backwardrow = 8
    for col in range(9):
        backwardsprite = app.playerModel4SpriteSheet.crop((imageWidth/cols*col, imageHeight/rows*backwardrow, imageWidth/cols*(col+1) , imageHeight/rows*(backwardrow+1)))
        backwardscaledsprite = app.scaleImage(backwardsprite, app.playerModelHeightfactor*scalefactor)
        app.playerModel4backwardsprite.append(ImageTk.PhotoImage(backwardscaledsprite))
    app.playerModel4Directions['backward'] = app.playerModel4backwardsprite

    #intializing left sprite
    #app.playerModel4LeftCounter = 0
    app.playerModel4leftsprite = []
    leftrow = 9
    for col in range(9):
        leftsprite = app.playerModel4SpriteSheet.crop((imageWidth/cols*col, imageHeight/rows*leftrow, imageWidth/cols*(col+1) , imageHeight/rows*(leftrow+1)))
        leftscaledsprite = app.scaleImage(leftsprite, app.playerModelHeightfactor*scalefactor)
        app.playerModel4leftsprite.append(ImageTk.PhotoImage(leftscaledsprite))
    app.playerModel4Directions['left'] = app.playerModel4leftsprite

    #intializing right sprite
    #app.playerModel4RightCounter = 0
    app.playerModel4rightsprite = []
    rightrow = 11
    for col in range(9):
        rightsprite = app.playerModel4SpriteSheet.crop((imageWidth/cols*col, imageHeight/rows*rightrow, imageWidth/cols*(col+1) , imageHeight/rows*(rightrow+1)))
        rightscaledsprite = app.scaleImage(rightsprite, app.playerModelHeightfactor*scalefactor)
        app.playerModel4rightsprite.append(ImageTk.PhotoImage(rightscaledsprite))
    app.playerModel4Directions['right'] = app.playerModel4rightsprite




#end of player images

###################################################################################################
#POWERUPS
def intializeHeart(app):
    app.heart = set([])
    intializeHeartSprite(app)



def intializeHeartSprite(app):
    #image from https://www.newgrounds.com/art/view/thediamondfinderyt/free-spinning-heart-sprite
    app.heartsprite = []
    app.heartspriteCounter = 0
    app.heartspritesheet = app.loadImage('Images\powerup\heart2.png')
    imageWidth, imageHeight = app.heartspritesheet.size
    app.heartHeightfactor = app.cellHeight / imageHeight
    rows = 2
    cols = 5
    for row in range(rows):
        for col in range(cols):
            sprite = app.heartspritesheet.crop((imageWidth/cols*col, imageHeight/rows*row, imageWidth/cols*(col+1) , imageHeight/rows*(row+1)))
            scaledsprite = app.scaleImage(sprite, app.heartHeightfactor*1.3)
            app.heartsprite.append(ImageTk.PhotoImage(scaledsprite))

def createHeart(app, coordinate):
    app.heart.add(coordinate)

def removeHeart(app, coordinate):
    app.heart.remove(coordinate)

#absorb the heart and gain a life
def absorbHeart(app, player):
    playerRow, playerCol = player.row, player.col
    if (playerRow, playerCol) in app.heart:
        player.lives += 1
        removeHeart(app, (playerRow, playerCol))
        


def randomlycreateHeart(app, coordinate):
    #we create a heart where when we destroy the wall
    #the probability of a heart appearing is only 20%
    rngheart = random.randint(1,5)
    if rngheart == 1:   
        createHeart(app, coordinate)

#trigger this once every second
def insertHeartatRandomCoordinate(app):
    #20 % trigger rate
    availablePositions = []
    randomActivation = random.randint(1,5)
    if randomActivation == 5:
        for row in range(app.rows):
            for col in range(app.columns):
                if ((row,col) not in app.MazeWalls) and (app.weaponPos[(row,col)] == []):
                    availablePositions.append((row,col))
        #print(availablePositions)
        randomChoice = random.randint(0, len(availablePositions) - 1)
        coordinate = availablePositions[randomChoice]
        createHeart(app, coordinate)
    else:
        pass

#####################################################################################
#Traps
#key set to int so can randomly generate later
def intializeTraps(app):
    app.trapImages = {}
    loadLavaTrap(app)



def loadLavaTrap(app):
    #image from https://lpc.opengameart.org/static/lpc-style-guide/assets.html
    lavaTrap = app.loadImage('Images\\traps\lava.png')
    lavaTrapCropped = lavaTrap.crop((8, 69, 90, 150))
    imageWidth, imageHeight = lavaTrapCropped.size
    Heightfactor = app.cellHeight / imageHeight
    scaledLava = app.scaleImage(lavaTrapCropped, Heightfactor)
    app.trapImages[0] = ImageTk.PhotoImage(scaledLava)

def generateTraps(app):
    forbiddenCoordinates = set([(0,0), (0, app.rows-1), (app.columns-1, 0), (app.rows-1, app.columns-1)])
    app.graph.traps = set([])
    for row in range(app.graph.rows):
        for col in range(app.graph.cols):
            if (row,col) not in app.MazeWalls and (row,col) not in forbiddenCoordinates:
                #10 % chance to generate a trap
                rngTrap = random.randint(1,10)
                if rngTrap == 1:
                    app.graph.traps.add((row,col))


def trapEffect(app, playernum):
    playerRow, playerCol = app.players[playernum].row, app.players[playernum].col
    if (playerRow, playerCol) in app.graph.traps:
        app.players[playernum].lives -= 1

#####################################################################################

def initializeExplosionSprite(app):
    app.explosion = []
    app.explosionspriteCounter = 0
    #https://www.pngitem.com/middle/hToJxb_preview-pixel-art-explosion-sprite-sheet-hd-png/
    app.explosionSpriteSheet = app.loadImage('Images\weapons\explosionSprite.png')
    imageWidth, imageHeight = app.explosionSpriteSheet.size
    app.explosionHeightfactor = app.cellHeight / imageHeight
    #list to store all the sprite images
    app.explosionsprite = []
    rows = 6
    cols = 10
    for row in range(rows):
        for col in range(cols):
            sprite = app.explosionSpriteSheet.crop((imageWidth/cols*col, imageHeight/rows*row, imageWidth/cols*(col+1) , imageHeight/rows*(row+1)))
            scaledsprite = app.scaleImage(sprite, app.explosionHeightfactor * 5)
            app.explosionsprite.append(ImageTk.PhotoImage(scaledsprite))


def intializeWallImages(app):
    # All tree images from 
    # https://stardewcommunitywiki.com/Category:Tree_images
    app.tree1 = app.loadImage('Images\\trees\\tree1.png')
    app.tree2 = app.loadImage('Images\\trees\\tree2.png')
    app.tree3 = app.loadImage('Images\\trees\\tree3.png')
    app.tree4 = app.loadImage('Images\\trees\\tree4.png')
    app.WallDict = {
        0 : app.tree1,
        1 : app.tree2,
        2 : app.tree3,
        3 : app.tree4
    }

    ScaleWallImage(app)

def initializeWeaponsImages(app):
    #Bomb from https://www.google.com/url?sa=i&url=http%3A%2F%2Fclipart-library.com%2Fbomb-cliparts.html&psig=AOvVaw0MGEiKDcFcUDWUnBx5BprH&ust=1637106597396000&source=images&cd=vfe&ved=0CAsQjRxqFwoTCOiBhtLHm_QCFQAAAAAdAAAAABAO
    app.bomb = app.loadImage('Images\\weapons\\bombnobg.png')
    app.weaponDict = {
        0 : app.bomb
    }

    ScaleWeaponImage(app)

def ScaleWeaponImage(app):
    app.WeaponImageDictScaled = {}
    for imageIndex in app.weaponDict:
        imageWidth, imageHeight = app.weaponDict[imageIndex].size
        scaleHeightFactor = app.cellHeight / imageHeight
        app.WeaponImageDictScaled[imageIndex] = ImageTk.PhotoImage(app.scaleImage(app.weaponDict[imageIndex], scaleHeightFactor))

#need to edit the image dimensions
def initializeFloorImage(app):
    #image from https://lpc.opengameart.org/static/lpc-style-guide/assets.html
    app.grass = app.loadImage("Images\\floor\grass.png")
    grasscropped = app.grass.crop((8, 69, 90, 150))
    #grasscropped = app.grass.crop((35,160,35 + 30, 160 + 30))
    #scalegrass = app.scaleImage(grasscropped, 10)
    #grasscroppedFit = scalegrass.crop((0,0, app.cellWidth, app.cellHeight))
    imageWidth, imageHeight = grasscropped.size
    scaleHeightFactor = app.cellHeight / imageHeight
    #scaleWidthFactor = app.cellWidth / imageWidth
    app.grassscaled = ImageTk.PhotoImage(app.scaleImage(grasscropped, scaleHeightFactor))


#function to hold all power ups and bombs currently on the floor
def initializeWeaponPosition(app):
    #dictionary containing coordinates of bombs as keys and instance of bomb as value
    #set value to None if there is no longer any weapon there
    app.weaponPos = {}
    for row in range(app.rows):
        for col in range(app.columns):
            app.weaponPos[(row,col)] = []
    
#used to make sure no wall is created at the position of any player
def checkplayerposition(app, coordinate):
    for player in app.players:
        if coordinate == (app.players[player].row,app.players[player].col):
            return False
    return True




#generate the maze walls
def initializeMaze(app):
    choice = random.randint(1,3)
    app.MazeWalls = {}
    if choice == 1:
        graph = Maze.PrimMazeGeneration(app.rows//2, app.columns//2)
    elif choice == 2:
        graph = Maze.recursiveBacktrackingMaze(app.rows//2, app.columns//2)
    
    elif choice == 3:
        graph = Maze.kruskalMazeGeneration(app.rows//2, app.columns//2)
    forbiddenCoordinates = set([(0,0), (0, app.rows-1), (app.columns-1, 0), (app.rows-1, app.columns-1)])
    for coordinate in graph.nodes:
        if len(graph.nodes[coordinate].edges) == 0:
            if ((coordinate not in forbiddenCoordinates) and 
                (checkplayerposition(app, coordinate))
                and (app.weaponPos[coordinate] == [])
                and (coordinate not in app.heart)):
                #boolean for whether wall is destructible or not
                newWall = wall.Wall(coordinate[0], coordinate[1], True)
                app.MazeWalls[coordinate] = newWall

    app.graph = graph
    generateTraps(app)

    app.MazeWallsOriLength = len(app.MazeWalls.keys())
        

def ScaleWallImage(app):
    app.WallImageDictScaled = {}
    for imageIndex in app.WallDict:
        imageWidth, imageHeight = app.WallDict[imageIndex].size
        #scaleWidthFactor = app.cellWidth / imageWidth
        scaleHeightFactor = app.cellHeight / imageHeight
        #print(f'{imageIndex} + {scaleHeightFactor}')
        #app.treescale = app.scaleImage(app.tree1, scaleHeightFactor)
        app.WallImageDictScaled[imageIndex] = ImageTk.PhotoImage(app.scaleImage(app.WallDict[imageIndex], scaleHeightFactor))
    # for imageIndex in app.WallImageDictScaled:
    #     width , height = app.WallImageDictScaled[imageIndex].size
    #     print(width, height)








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
    #change action to forward
    if (drow, dcol) == (1,0):
        app.players[playernum].action = 'forward'

    if (drow, dcol) == (-1,0):
        app.players[playernum].action = 'backward'

    if (drow, dcol) == (0,1):
        app.players[playernum].action = 'right'

    if (drow, dcol) == (0,-1):
        app.players[playernum].action = 'left'

    newRow, newCol = app.players[playernum].row + drow, app.players[playernum].col + dcol
    if checkCollison(app, newRow, newCol) and checkBounds(app, newRow, newCol):
        app.players[playernum].row = newRow
        app.players[playernum].col = newCol
        absorbHeart(app, app.players[playernum])
        trapEffect(app, playernum)
        #testing for player 2
        #finddfspath(app, 2)
        #findbfspath(app, 2)

    else:
        return

def createBomb(app, playernum):
    currentRow, currentCol = app.players[playernum].row, app.players[playernum].col
    if app.players[playernum].bombCount > 0:
        app.weaponPos[(currentRow, currentCol)].append(weapon.Bomb(app.players[playernum].bombTimer, playernum, 2))
        app.players[playernum].bombCount -= 1

def explodeBomb(app):
    for coordinate in app.weaponPos:
        if app.weaponPos[coordinate] != []:
            for weaponObj in app.weaponPos[coordinate]:
                #if the weapon is a bomb
                if isinstance(weaponObj, weapon.Bomb):
                    if weaponObj.timer > 0:
                        weaponObj.timer -= 1
                    #if bomb has exploded
                    if weaponObj.timer == 0:
                        playernum = weaponObj.playernum
                        app.players[playernum].bombCount += 1
                        explosionRadius(app, coordinate, playernum, weaponObj.bombradius)
                        explosionEffect(app, coordinate)
                        app.weaponPos[coordinate].remove(weaponObj)



#stores the explosion radius into a list
def explosionRadius(app, coordinate, playernum, bombradius):
    #center row, center col, playernumer, explosion radius
    explosion = weapon.Explosion(coordinate[0], coordinate[1], playernum, bombradius)
    explosion.createBombchangeRowCol()
    for drow, dcol in explosion.bombdcoordinate:
        newRow, newCol = coordinate[0] + drow, coordinate[1] + dcol
        if checkBounds(app, newRow, newCol):
            explosion.radius.append((newRow, newCol))
    #contains list of instances for explosion class        
    app.explosion.append(explosion)  




#performs the effect of the explosion which destroys the walls
#need to add in harming the player effect as well
def explosionEffect(app, coordinate):
    for explosion in app.explosion:
        #row,col in explosion.radius
        for coordinate in explosion.radius:
            if coordinate in app.MazeWalls and app.MazeWalls[coordinate].destructible == True:
                app.MazeWalls.pop(coordinate)
            
                #create the heart
                randomlycreateHeart(app, coordinate)

            for player in range(1,5):
                #player cannot be harmed by their own explosions
                if player == explosion.playernum:
                    continue
                else:
                    if coordinate == (app.players[player].row, app.players[player].col):
                        if app.players[player].lives > 0:
                            app.players[player].lives -= 1




#controls the explosion duration
def explosionDuration(app):
    if len(app.explosion) != 0:
        for explosion in app.explosion:
            if explosion.timer > 0:
                explosion.timer -= 1
            if explosion.timer == 0:
                app.explosion.remove(explosion)
        


#######################################################################################################################################
#AI CODE will be written here

def editAIAction(app, drow, dcol, Ainum):
    if (drow, dcol) == (1,0):
        app.players[Ainum].action = 'forward'

    if (drow, dcol) == (-1,0):
        app.players[Ainum].action = 'backward'

    if (drow, dcol) == (0,1):
        app.players[Ainum].action = 'right'

    if (drow, dcol) == (0,-1):
        app.players[Ainum].action = 'left'

def initializeAI(app):
    initializeplayerpath(app)

def initializeplayerpath(app):
    app.playerpath = {
        1 : None,
        2 : None,
        3 : None,
        4 : None
    }

    app.AiTarget = {
        2 : 4,
        3 : 1,
        4 : 2,
    }



def finddfspath(app, AiNum):
    path  = AI.dfs(app.graph, app.MazeWalls, app.players[1], app.players[AiNum])
    if path != None:
        app.playerpath[AiNum] = path

#shortest path
def findbfspath(app, AiNum):
    player1 = app.players[1]
    ai = app.players[AiNum]
    path = AI.getshortestpathbfs(app.graph, app.MazeWalls, player1, ai)
    if path != None:
        app.playerpath[AiNum] = path

def distance(x0 ,y0 ,x1, y1):
    return ((x1-x0)**2 + (y1-y0)**2)**0.5

#this function will never return a None path
def AstarPath(app, startplayernum, targetplayernum):
    path = AI.getshortestpathAstar(app, app.graph, app.MazeWalls, startplayernum, targetplayernum)
    return path

def findAstarpath(app, AiNum, targetNum):
    path = AstarPath(app, AiNum, targetNum)
    if path != None:
        app.playerpath[AiNum] = path

# find the shortest distance from a heart to the AI
def calculateDistancetoHeart(app, AiNum):
    AiRow, AiCol = app.players[AiNum].row, app.players[AiNum].col
    bestDist = 1000000
    bestCoord = None
    for coordinate in app.heart:
        compdist = distance(coordinate[0], coordinate[1], AiRow, AiCol)
        if compdist < bestDist:
            bestDist = compdist
            bestCoord = coordinate
    return bestCoord

#finite state AI
def AIfindpath(app, AiNum, targetNum):
    #finding path to heart if there is a heart present
    if len(app.heart) != 0:
        targetCoord = calculateDistancetoHeart(app, AiNum)
        path = AI.getAstarCoordinatePath(app, app.graph, app.MazeWalls, AiNum, targetCoord)
        app.playerpath[AiNum] = path
        app.players[AiNum].counter = 0
        app.players[AiNum].targetHeart = True

    else:
        #findbfspath(app, AiNum)
        findAstarpath(app, AiNum, targetNum)
        #controlling AI
        app.players[AiNum].counter = 0




#trigger this every 1 second
def moveAI(app, AiNum):
    if app.players[AiNum].lives > 0:
        currentRow, currentCol = app.players[AiNum].row, app.players[AiNum].col
        path = app.playerpath[AiNum]
        #print(path)
        #if we reach the end of the path we just stay there
        if app.players[AiNum].counter >= len(path):
            app.players[AiNum].counter = len(path) - 1


        #if there is a bomb right in front we want to create a bomb
        if path[0] in app.MazeWalls:
            createBomb(app, AiNum)
            app.players[AiNum].counter = app.players[AiNum].counter
        else:
            drow, dcol = path[app.players[AiNum].counter][0] - currentRow, path[app.players[AiNum].counter][1] - currentCol
            #changes ai animation action
            editAIAction(app, drow, dcol, AiNum)

            #actual moving
            app.players[AiNum].row, app.players[AiNum].col = currentRow + drow, currentCol + dcol
            trapEffect(app, AiNum)
            #absorb the heart
            absorbHeart(app, app.players[AiNum])
            #findbfspath(app, AiNum)

            targetRow, targetCol = app.players[app.AiTarget[AiNum]].row, app.players[app.AiTarget[AiNum]].col
            #player1Row, player1Col = app.players[1].row, app.players[1].col

            #change target once bomb is placed
            #creating a bomb if within 1 cross radius
            for move in [(0,1), (1,0), (-1,0), (0, -1), (0,0)]:
                if (targetRow, targetCol) == (app.players[AiNum].row + move[0], app.players[AiNum].col + move[1]):
                    if app.players[AiNum].bombCount > 0:
                        createBomb(app, AiNum)

                        if app.players[AiNum].targetSwitch > 0:
                            app.players[AiNum].targetSwitch -= 1
                        

                        #we switch target after placing down 2 bombs
                        if app.players[AiNum].targetSwitch <= 0:
                            app.players[AiNum].targetSwitch = 2
                            targetplayer = random.randint(0,2)
                            #33% to target the player to add bias so that the game is more challenging
                            if targetplayer == 0:
                                app.AiTarget[AiNum] = 1
                            else:
                                newTarget = random.randint(1,4)
                                #new target cannot be itself or the previous target
                                while newTarget == AiNum or newTarget == app.AiTarget[AiNum]:
                                    newTarget = random.randint(1,4)
                                app.AiTarget[AiNum] = newTarget
        



##################################################################################################
#timer functions
def kleeSpriteTimer(app):
    app.KleespriteCounter += 1
    if app.KleespriteCounter >= len(app.kleesprite):
        app.KleespriteCounter = 0

def explosionSpriteTimer(app):
    app.explosionspriteCounter += 1
    if app.explosionspriteCounter >= len(app.explosionsprite):
        app.explosionspriteCounter = 0

def playerModel1Counter(app):
    #since all directional images have the same no of frames we can just compare to one of the sheets
    app.playerModel1Counter += 1
    if app.playerModel1Counter >= len(app.playerModel1forwardsprite):
        app.playerModel1Counter = 0

def playerModel2Counter(app):
    #since all directional images have the same no of frames we can just compare to one of the sheets
    app.playerModel2Counter += 1
    if app.playerModel2Counter >= len(app.playerModel2forwardsprite):
        app.playerModel2Counter = 0

def playerModel3Counter(app):
    #since all directional images have the same no of frames we can just compare to one of the sheets
    app.playerModel3Counter += 1
    if app.playerModel3Counter >= len(app.playerModel3forwardsprite):
        app.playerModel3Counter = 0

def playerModel4Counter(app):
    #since all directional images have the same no of frames we can just compare to one of the sheets
    app.playerModel4Counter += 1
    if app.playerModel4Counter >= len(app.playerModel4forwardsprite):
        app.playerModel4Counter = 0

def heartCounter(app):
    app.heartspriteCounter += 1
    if app.heartspriteCounter >= len(app.heartsprite):
        app.heartspriteCounter = 0

def gameChangeConditions(app):
    if app.timer < 0:
        app.gameover = True
    if app.players[1].lives <= 0:
        app.gameover = True
    if app.gameover:
        app.mode = 'gameOverMode'

    if checkEnemyLives(app):
        app.gamewin = True

    if app.gamewin:
        app.mode = 'gameWinMode'


def checkEnemyLives(app):
    for i in range(2,5):
        if app.players[i].lives > 0 :
            return False
    return True

def gameMode_timerFired(app):
    app.timeElasped += app.timerDelay
    if app.timeElasped % 1000 == 0:
        explodeBomb(app)
        app.timer -= 1
        insertHeartatRandomCoordinate(app)
        

    #controls move speed of AI
    if app.timeElasped % 150 == 0:
        for playernum in range(2,5):
            if app.players[playernum].lives > 0:
                AIfindpath(app, playernum, app.AiTarget[playernum])
                moveAI(app, playernum)
                


        
        autoRegenWalls(app)
        

    if app.timeElasped % 200 == 0:
        explosionDuration(app)
    
    gameChangeConditions(app)
    #print(app.timeElasped)
    #currentTime = time.time()
    #timepassed = currentTime - app.startTime
    #print(timepassed)
    #https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html#spritesheetsWithCropping
    #if app.timeElasped % 1000 == 0:
        #kleeSpriteTimer(app)
    playerModel1Counter(app)
    playerModel2Counter(app)
    playerModel3Counter(app)
    playerModel4Counter(app)
    explosionSpriteTimer(app)
    heartCounter(app)
        






        
        
    

def gameMode_keyPressed(app, event):
    #press r to reset the maze
    if event.key == 'r':
        regenerateWalls(app)

    if event.key == 'd':
        movePlayer(app, 0, 1, 1)

    if event.key == 'a':
        movePlayer(app, 0, -1, 1)

    if event.key == 'w':
        movePlayer(app, -1, 0, 1)

    if event.key == 's':
        movePlayer(app, 1, 0, 1)

    if event.key == 'b':
        createBomb(app, 1)
    #for debugging
    if event.key == 'o':
        app.gameover = True

    if event.key == 'l':
        app.gamewin = True


def regenerateWalls(app):
    app.MazeWalls = {}
    initializeMaze(app)

def autoRegenWalls(app):
    if len(app.MazeWalls.keys())/app.MazeWallsOriLength < 0.85:
        regenerateWalls(app)


#######################################################################################################################################
#Drawing Functions
def drawWallImage(app, canvas):
    for wall in app.MazeWalls:
        image = app.MazeWalls[wall].imageIndex
        x0, y0, x1, y1 = getCellBounds(app, app.MazeWalls[wall].row, app.MazeWalls[wall].col)
        canvas.create_image((x1 + x0)/2 , (y1 + y0)/2, image = app.WallImageDictScaled[image])

#using this for debugging
def drawMaze(app, canvas):
    for wall in app.MazeWalls:
        x0, y0, x1, y1 = getCellBounds(app, app.MazeWalls[wall].row, app.MazeWalls[wall].col)
        canvas.create_rectangle(x0, y0, x1, y1, fill = 'black')
#draws bomb
def drawWeapon(app, canvas):
    for coordinate in app.weaponPos:
        if app.weaponPos[coordinate] != []:
            for bomb in app.weaponPos[coordinate]:
                #draw the bomb
                if isinstance(bomb, weapon.Bomb):
                    weaponID = bomb.weaponID
                    x0, y0, x1, y1 = getCellBounds(app, coordinate[0], coordinate[1])
                    #canvas.create_rectangle(x0, y0, x1, y1, fill = app.playerColor[bomb.playernum])
                    canvas.create_image((x0 + x1)/2, (y0 + y1)/2, image = app.WeaponImageDictScaled[weaponID])
##################################################################################
#drawing players
#playernum here is an int
def drawKlee(app, canvas, playernum):
    x0, y0, x1, y1 = getCellBounds(app, app.players[playernum].row, app.players[playernum].col)
    spriteimage = app.kleesprite[app.KleespriteCounter]
    canvas.create_image((x1 + x0)/2, (y1 + y0)/2, image= spriteimage)

#action controls which sprite sheet is being used
#action is a string: 'forward', 'backward', 'right', 'left'
def drawplayerModel1(app, canvas, playernum):
    #get where to draw the player
    x0, y0, x1, y1 = getCellBounds(app, app.players[playernum].row, app.players[playernum].col)
    spriteimage = app.playerModels[playernum][app.players[playernum].action][app.playerModel1Counter]
    canvas.create_rectangle(x0, y0, x1 ,y1 , fill = app.playerColor[playernum])
    canvas.create_image((x1 + x0)/2, (y1 + y0)/2 - 5, image= spriteimage)

def drawAIModel(app, canvas, AInum):
    if app.players[AInum].lives > 0:
        x0, y0, x1, y1 = getCellBounds(app, app.players[AInum].row , app.players[AInum].col)
        spriteimage = app.playerModels[AInum][app.players[AInum].action][app.playerModel2Counter]
        canvas.create_rectangle(x0, y0, x1 ,y1 , fill = app.playerColor[AInum])
        canvas.create_image((x1 + x0)/2, (y1 + y0)/2 - 5, image= spriteimage)


##################################################################################

def drawFloor(app, canvas):
    for row in range(app.graph.rows):
        for col in range(app.graph.cols):
            x0, y0, x1, y1 = getCellBounds(app, row, col)
            canvas.create_image((x1 + x0)/2, (y1 + y0)/2, image= app.grassscaled)


def drawExplosion(app, canvas):
    for explosion in app.explosion:
        for coordinate in explosion.radius:
            x0, y0, x1, y1 = getCellBounds(app, coordinate[0], coordinate[1])
            #hardcoding the explosion sprite for now due to lag
            spriteimage = app.explosionsprite[25]
            canvas.create_image((x1 + x0)/2, (y1 + y0)/2, image= spriteimage)
        
#debugging for dfs
def drawdfsPath(app, canvas, ainum):
    if app.playerpath[ainum] != None:
        for row, col in app.playerpath[ainum]:
            x0, y0, x1, y1 = getCellBounds(app, row, col)
            canvas.create_rectangle(x0, y0, x1, y1, fill = 'red')

#debugging for bfs
def drawbfsPath(app, canvas, ainum):
    if app.playerpath[ainum] != None:
        for row, col in app.playerpath[ainum]:
            x0, y0, x1, y1 = getCellBounds(app, row, col)
            canvas.create_rectangle(x0, y0, x1, y1, fill = 'green')



def drawAstarPath(app, canvas,  startnum, targetnum):
    path = AstarPath(app, startnum, targetnum)
    for coordinate in path:
        row, col = coordinate[0], coordinate[1]
        x0, y0, x1, y1 = getCellBounds(app, row, col)
        canvas.create_rectangle(x0, y0, x1, y1, fill = 'red')

def drawgrid(app, canvas):
    for row in range(app.rows):
        for col in range(app.columns):
            x0, y0, x1, y1 = getCellBounds(app, row, col)
            canvas.create_rectangle(x0 , y0 , x1 , y1)

def drawScoreBoard(app, canvas):
    #lime green
    backgroundcolor = rgbString(77, 237, 48)
    panels = 5
    scoreboardWidth = app.shift - 2*app.margin
    scoreboardstartx = app.margin
    scoreboardstarty = app.margin
    scoreboardHeight = app.height - 2*app.margin
    scoreboardpanelHeight = (app.height - 2*app.margin)/panels
    linewidth = 5
    #draw background
    canvas.create_rectangle(scoreboardstartx, scoreboardstarty, 
                            scoreboardWidth + scoreboardstartx, 
                            scoreboardHeight + scoreboardstarty , 
                            width = linewidth)

    for background in range(panels):
        if background == 0:
            #timer
            canvas.create_rectangle(scoreboardstartx, scoreboardstarty + scoreboardpanelHeight * background,
                                    scoreboardWidth + scoreboardstartx, 
                                    scoreboardpanelHeight* (background+1),
                                    fill = backgroundcolor)
        #players 1 2 3
        elif 0 < background < panels - 1:
            canvas.create_rectangle(scoreboardstartx, scoreboardpanelHeight * background,                        scoreboardWidth + scoreboardstartx, 
                        scoreboardpanelHeight* (background+1),
                        fill = app.playerColor[background])
        #player 4
        else:
            canvas.create_rectangle(scoreboardstartx, scoreboardpanelHeight * background,                        scoreboardWidth + scoreboardstartx, 
                        scoreboardpanelHeight* (background+1) + scoreboardstarty,
                        fill = app.playerColor[background])


    #draw timer
    canvas.create_text(scoreboardWidth//2 + scoreboardstartx, 
                        scoreboardpanelHeight//2 + scoreboardstarty, 
                        text = f"{convert(app.timer)}", font = "Arial 50 bold", fill = "red")
    #draw player panels                            
    for i in range(1, panels):
        canvas.create_line(app.margin, scoreboardpanelHeight * i, 
                            app.shift - app.margin, scoreboardpanelHeight * i, 
                            width = linewidth)
    #draw character image
    for image in range(1, panels):
        spriteimage = app.playerModels[image]['forward'][app.playerModel2Counter]
        canvas.create_image(scoreboardstartx + linewidth  + scoreboardWidth/8, 
                            scoreboardpanelHeight/2 +  
                            scoreboardpanelHeight* image , image= spriteimage)
    
    for word in range(1, panels):
        canvas.create_text(scoreboardstartx + scoreboardWidth/1.8, scoreboardpanelHeight/4 +  scoreboardpanelHeight* word, text = f'Player {word}', font = "Arial 25 bold", fill = "black")
        canvas.create_text(scoreboardstartx + scoreboardWidth/1.8, 
                            scoreboardpanelHeight/1.75 +  scoreboardpanelHeight* word, 
                            text = f'Lives: {app.players[word].lives}', 
                            font = "Arial 18 bold", fill = "black")
        canvas.create_text(scoreboardstartx + scoreboardWidth/1.8, 
                            scoreboardpanelHeight/1.2 +  scoreboardpanelHeight* word, 
                            text = f'Bombs: {app.players[word].bombCount}', 
                            font = "Arial 15 bold", fill = "black")
        


def drawHeart(app, canvas):
    if len(app.heart) != 0:
        for coordinate in app.heart:
            x0, y0, x1, y1 = getCellBounds(app, coordinate[0], coordinate[1])
            spriteimage = app.heartsprite[app.heartspriteCounter]
            canvas.create_image((x1 + x0)/2, (y1 + y0)/2 - 5, image= spriteimage)


def drawTrap(app ,canvas):
    for trapcoordinate in app.graph.traps:
        trapchoice = random.randint(0,0)
        x0, y0, x1, y1 = getCellBounds(app, trapcoordinate[0], trapcoordinate[1])
        canvas.create_image((x1 + x0)/2, (y1 + y0)/2, image = app.trapImages[trapchoice])
#######################################################################################################################################

def gameMode_redrawAll(app,canvas):
    #drawFloor(app, canvas)
    drawHeart(app, canvas)
    drawTrap(app ,canvas)
    
    #drawAstarPath(app, canvas,  3, 1)
    #drawAstarPath(app, canvas,  2, 1)
    #drawAstarPath(app, canvas,  4, 1)
    drawplayerModel1(app, canvas, 1)
    for i in range(2,5):
        drawAIModel(app, canvas, i)
    drawWeapon(app, canvas)
    drawScoreBoard(app, canvas)
    drawgrid(app, canvas)
    #drawMaze(app, canvas)
    drawWallImage(app, canvas)
    #drawdfsPath(app, canvas, 2)
    #drawbfsPath(app, canvas, 2)
    #drawKlee(app, canvas, 1)
    
    drawExplosion(app, canvas)
    


    

    
    

#########################################################
#game over mode 

####################################################################
#intialize gameOver sprite

def initializeGameoversprite(app):
    #https://cipater.tumblr.com/post/43655192566/super-bomberman-5-hudson-soft-super-nintendo
    app.gameOverspriteCounter = 0
    #https://www.pngitem.com/middle/hToJxb_preview-pixel-art-explosion-sprite-sheet-hd-png/
    app.gameOverSpriteSheet = app.loadImage('Images\gameover\gameoversprite.png')
    app.gameOverSpriteSheet.crop((0,444, 2000, 444))
    imageWidth, imageHeight = app.gameOverSpriteSheet.size
    app.gameOverHeightfactor = app.height / imageHeight
    #app.gameOverWidthfactor = app.width / imageWidth
    #list to store all the sprite images
    app.gameOversprite = []
    rows = 1
    cols = 5
    for row in range(rows):
        for col in range(cols):
            if col == 4: continue
            sprite = app.gameOverSpriteSheet.crop((imageWidth/cols*col, imageHeight/rows*row, imageWidth/cols*(col+1) , imageHeight/rows*(row+1)))
            scaledsprite = app.scaleImage(sprite, app.gameOverHeightfactor)
            app.gameOversprite.append(ImageTk.PhotoImage(scaledsprite))

####################################################################
#drawing functions for gameover

def drawgameOverSprite(app, canvas):
    spriteimage = app.gameOversprite[app.gameOverspriteCounter]
    canvas.create_image(app.width/2, app.height/2, image= spriteimage)

def gameOverMode_redrawAll(app,canvas):
    canvas.create_rectangle(0,0, app.width, app.height, fill = 'black')
    drawgameOverSprite(app, canvas)
    canvas.create_text(app.width/2, app.height - app.height/5 , text = "GAME OVER!", fill = "white", font = "Arial 50 bold")
    canvas.create_text(app.width/2, app.height - app.height/9 , text = "PRESS R TO RESTART", fill = "white", font = "Arial 30 bold")

def gameOverMode_keyPressed(app, event):
    if event.key == 'r':
        app.gameover = False        
        gameparams(app)
        intializeTime(app)
        gamegraphics(app)
        initializeAI(app)
        app.mode = 'gameMode'

def gameOverMode_timerFired(app):
    app.gameOverspriteCounter += 1
    if app.gameOverspriteCounter >= len(app.gameOversprite):
        app.gameOverspriteCounter = 0

#end of gameover mode
#########################################################


#########################################################
#game win mode


def initializeGamewinsprite(app):
    #https://wonder-doughnut.tumblr.com/post/189445852204/happy-20th-anniversary-to-the-best-bomberman-game
    app.gameWinspriteCounter = 0
    #https://www.pngitem.com/middle/hToJxb_preview-pixel-art-explosion-sprite-sheet-hd-png/
    app.gameWinSpriteSheet = app.loadImage("Images\gameWin\gamewinsprite.png")
    imageWidth, imageHeight = app.gameWinSpriteSheet.size
    #app.gameWinHeightfactor = app.height / imageHeight
    app.gameWinWidthfactor = app.width / imageWidth
    #list to store all the sprite images
    app.gameWinsprite = []
    rows = 14
    cols = 5
    for row in range(rows):
        for col in range(cols):
            if row == 13 and (col == 4 or col == 3): continue
            sprite = app.gameWinSpriteSheet.crop((imageWidth/cols*col, imageHeight/rows*row, imageWidth/cols*(col+1) , imageHeight/rows*(row+1)))
            scaledsprite = app.scaleImage(sprite, 3)
            app.gameWinsprite.append(ImageTk.PhotoImage(scaledsprite))


####################################################################
#drawing functions for gamewin
def drawgameWinSprite(app, canvas):
    canvas.create_rectangle(0,0, app.width, app.height, fill = 'black')
    spriteimage = app.gameWinsprite[app.gameWinspriteCounter]
    canvas.create_image(app.width/2, app.height/2, image= spriteimage)
    canvas.create_text(app.width/2, app.height/10 , text = "CONGRATULATIONS YOU WIN!", fill = "yellow", font = "Arial 50 bold")
    canvas.create_text(app.width/2, app.height/6 , text = "PRESS R TO RESTART", fill = "yellow", font = "Arial 20 bold")

def gameWinMode_redrawAll(app,canvas):
    drawgameWinSprite(app, canvas)

def gameWinMode_timerFired(app):
    app.gameWinspriteCounter += 1
    if app.gameWinspriteCounter >= len(app.gameWinsprite):
        app.gameWinspriteCounter = 0

def gameWinMode_keyPressed(app, event):
    if event.key == 'r':
        app.gamewin = False        
        gameparams(app)
        intializeTime(app)
        gamegraphics(app)
        initializeAI(app)
        app.mode = 'gameMode'
####################################################################
def runGame():
    runApp(width= 1500, height= 800)


runGame()