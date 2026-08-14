from cmu_graphics import *
from PIL import Image
import os, pathlib
from classes import *

def onAppStart(app):
    app.startScreen = True
    resetApp(app)

def resetApp(app):
    app.stepsPerSecond = 30 # update in resetApp in case the promptscreen changes this


# initialize room and objects
    # Referenced CS Academy notes on how to draw 2d grids
    app.rows = 30
    app.cols = 55
    app.boardLeft = 0
    app.boardTop = 0
    app.boardWidth = 1555
    app.boardHeight = 900
    app.cellBorderWidth = 0.13

    # openImage function and scaling technique taken from the CMU_Graphics Demo VScode Folder https://piazza.com/class/li3k33dc9yl37f/post/424#:~:text=N23%2DCMUGraphicsDemos.zip
    app.startImage = openImage("images/i am toast.jpg")
    app.startImageWidth, app.startImageHeight = app.startImage.width, app.startImage.height
    app.startImage = CMUImage(app.startImage)

    
    
    app.backgroundX = 0
    app.backgroundY = -470
    #Kitchen background taken from https://www.freepik.com/free-vector/kitchen-interior-design-with-furniture_16860713.htm
    app.backgroundImage = openImage("images/kitchen.jpg") #
    app.backgroundImageWidth, app.backgroundImageHeight = app.backgroundImage.width, app.backgroundImage.height
    app.backgroundImage = CMUImage(app.backgroundImage)

    # Table image taken from https://www.kindpng.com/imgv/hmmoxRJ_club-penguin-rewritten-wiki-coffee-table-club-penguin/
    app.table = openImage("images/table.webp")
    app.tableX = 141
    app.tableY = 420
    app.tableWidth, app.tableHeight = app.table.width, app.table.height
    app.table = CMUImage(app.table)

    # Wall image taken from https://scribblenauts.fandom.com/wiki/Rectangle
    app.wall = openImage("images/kitchencounter.webp")
    app.wallX = 1500
    app.wallY = 680 - app.wall.height
    app.wallWidth, app.wallHeight = app.wall.width * 2, app.wall.height * 2
    app.wall = CMUImage(app.wall)

    app.tableSurface = Surface(app.tableX, app.tableY, app.tableWidth // 3, app.tableHeight // 3)
    app.counterSurface = Surface(app.wallX, app.wallY, app.wallWidth, app.wallHeight)

    #Ants Image taken from https://larc.unt.edu/code/topdownwithants/
    app.antsImage = openImage("images/ants.png")
    app.antsWidth, app.antsHeight = app.antsImage.width, app.antsImage.height
    app.antsImage = CMUImage(app.antsImage)
    app.ants = Obstacle(500, 750, app.antsWidth, app.antsHeight)


    # Skateboard image taken from https://www.vexels.com/png-svg/preview/256749/skateboard-side-view-color-stroke
    app.skateboard = Skateboard(848, 630)
    app.skateboardImage = openImage("images/skateboard2.png")
    app.skateboardWidth, app.skateboardHeight = app.skateboardImage.width, app.skateboardImage.height
    app.skateboardImage = CMUImage(app.skateboardImage)

    # Image taken from https://unturned.fandom.com/wiki/Toaster
    app.toasterImage = openImage("images/toaster.webp")
    app.toasterWidth, app.toasterHeight = app.toasterImage.width, app.toasterImage.height
    app.toasterImage = CMUImage(app.toasterImage)
    app.toaster = Toaster(1300, 580, app.toasterWidth, app.toasterHeight)




    # Bread image taken from Minecraft https://minecraft.fandom.com/wiki/Bread
    app.bread = Player()
    app.breadImage = openImage("images/bread.webp")
    app.breadWidth, app.breadHeight = app.breadImage.width, app.breadImage.height
    app.breadImage = CMUImage(app.breadImage)
    app.isFalling = False
    app.onFloor = False

    app.edibility = Edibility()

    # app.roomObjects = [RoomObjects(app.tableX, app.tableY, app.table)]

# initialize the different screens
    app.promptScreen = False
    app.mainScreen = True
    app.nextLevel = False
    app.gameOver = False

    app.toasting = False
    app.timeLeft = 3
    app.toastedAmount = 0
    app.score = None

def resetNextLevel(app):
    # resetfor the next level
    #Image taken from https://www.shutterstock.com/image-illustration/kitchen-game-background-bg-realistic-toon-1104012278
    app.backgroundImage = openImage("images/nextlevel.webp")
    app.backgroundImageWidth, app.backgroundImageHeight = app.backgroundImage.width, app.backgroundImage.height
    app.backgroundImage = CMUImage(app.backgroundImage)
    app.backgroundX = 0
    app.backgroundY = 0

    app.bread.x = 40
    app.bread.y = 690
    app.bread.angle = 0

def openImage(fileName):
                return Image.open(os.path.join(pathlib.Path(__file__).parent,fileName))


def onStep(app):
    # always check if edibility has run out
    if app.edibility.counter == 0:
        app.gameOver = True

    # gravity; update bread's position if its not on a surface
    if app.isFalling:
        app.bread.y += 30  

    # main part of the level
    if app.mainScreen:
        if app.tableSurface.isOnSurface(app.bread.x, app.bread.y):
            app.isFalling = False

        # edibility decreases when bread is on the floor
        if onFloor(app):
            app.isFalling = False
            app.bread.y = 690
            app.edibility.decrease()

        if onSkateboard(app):
            app.isFalling = False
            app.bread.y = app.skateboard.y + 45
            moveSkateboard(app)

        if hitWall(app):
            app.mainScreen = False
            app.promptScreen = True
            app.bread.x -= 30
            app.timeLeft = 3

    # prompt screen to climb wall
    if app.promptScreen:
        app.stepsPerSecond = 1
        app.timeLeft -= 1
    
    # game over if the user doesnt do the prompt in time]
    if app.timeLeft <= 0 and not app.nextLevel:
        app.promptScreen = False
        app.gameOver = True

    if app.nextLevel:
        app.stepsPerSecond = 30
        app.isFalling = False
        app.bread.y = 690

        # decrease edibility if the bread is on the ants
        if app.ants.collide(app.bread.x, app.bread.y):
            app.edibility.decrease()

        # update when the user has reached the toaster
        if app.toaster.onTop(app.bread.x, app.bread.y):
            app.toasting = True
        else:
            app.toasting = False        
    
    # update toasted amount when on toaster
    if app.toasting:
        app.bread.x = 120
        app.bread.y = app.toaster.y
        app.toastedAmount += 1

        # decrease edibility if toast is burning
        if app.toastedAmount >= 100:
            app.edibility.decrease()

        # scoring system
        if app.gameOver:
            if app.edibility.counter >= 95:
                app.score = "A"
            elif app.edibility.counter >= 85:
                app.score = "B"
            elif app.edibility.counter >= 85:
                app.score = "C"
            elif app.edibility.counter >= 75:
                app.score = "D"
            else:
                app.score = "F"


def onKeyPress(app, key):
    # to jump:
    if key == "space":
        app.bread.speed += 1
        app.bread.jump()

    # beginning the game
    if app.startScreen and key == "b":
        app.startScreen = False
        resetApp(app)

    if key == "r":
        resetApp(app)

    # move the correct objects when the user tries to move on the main screen
    if app.mainScreen:
        if key == "left":
            moveObjects(app, ["background", "skateboard", "table", "wall"], key)
            if app.backgroundX > 0:
                app.bread.move("left")
                app.bread.angle = 0
        elif key == "right":
            moveObjects(app, ["background", "skateboard", "table", "wall"], key)
            app.bread.move("right")

    # move the correct objects when the user tries to move on the next screen
    if not app.toasting and app.nextLevel: 
        if key == "right" or key == "left":
            moveObjects(app, ["background", "toaster", "ants"], key)
            if key == "left":
                if app.backgroundX > 0:
                    app.bread.move("left")
            else:
                app.bread.move("right")

    # gravity
    if not onTable(app):
        app.isFalling = True

    # check if user has successfully done the prompt in time
    if app.promptScreen:
        if app.timeLeft >= 0:
            if key == "f":
                app.promptScreen = False
                app.nextLevel = True
                resetNextLevel(app)

    # end the game when the user is done toasting
    if app.toasting:
        if key == "d":
            app.gameOver = True

def onKeyHold(app, keys):
    if app.mainScreen:
        if "right" in keys:
            moveObjects(app, ["background", "skateboard", "table", "wall"], "right")
            app.bread.move("right")
        elif "left" in keys and app.backgroundX < 0:
            moveObjects(app, ["background", "skateboard", "table", "wall"], "left")
            app.bread.move("left")

        if not onTable(app):
            app.isFalling = True

        if not app.tableSurface.isOnSurface(app.bread.x, app.bread.y):
            app.isFalling = True
    
    if not app.toasting and app.nextLevel:
        if "right" in keys:
            moveObjects(app, ["background", "toaster", "ants"], "right")
            app.bread.move("right")
        elif "left" in keys and app.backgroundX < 0:
            moveObjects(app, ["background", "toaster", "ants"], "left")
            app.bread.move("left")

def moveObjects(app, objectsList, direction):
    # function to move the correct objects when side scrolling
    if direction == "right":
        for obj in objectsList:
            if obj == "background":
                app.backgroundX -= 30
                app.boardLeft -= 30
            elif obj == "table":
                app.tableX -= 30
            elif obj == "skateboard":
                app.skateboard.x -= 30
            elif obj == "wall":
                app.wallX -= 30
            elif obj == "toaster":
                app.toaster.x -= 30
            elif obj == "ants":
                app.ants.x -= 30

    elif direction == "left":
        if app.backgroundX < 0:
            for obj in objectsList:
                if obj == "background":
                    app.boardLeft += 30
                    app.backgroundX += 30
                elif obj == "table":
                    app.tableX += 30
                elif obj == "skateboard":
                    app.skateboard.x += 30
                elif obj == "wall":
                    app.wallX += 30
                elif obj == "toaster":
                    app.toaster.x += 30
                elif obj == "ants":
                    app.ants.x += 30

def onFloor(app):
    # check collision between bread and floor
    if app.mainScreen:
        if app.bread.y >= 690 and not onSkateboard(app):
            return True
    return False

def onTable(app):
    # check collison between bread and table
    tableRight = app.tableX + app.tableWidth // 3

    if app.bread.x <= tableRight:
        return True
    else:
        return False

def onSkateboard(app):
    # check collision between bread and skateboard
    skateboardRight = app.skateboard.x + app.skateboardWidth // 2

    if app.skateboard.x - 10 <= app.bread.x + app.breadWidth // 4 <= skateboardRight + 10:
        return True
    else:
        return False

def moveSkateboard(app):
    # if the bread is on the edge of the skateboard, it starts rolling
    skateboardRight = app.skateboard.x + app.skateboardWidth // 2 - 60

    if app.skateboard.x + 15 == app.bread.x:
        moveObjects(app, ["background", "table", "wall"], "left")
    elif skateboardRight == app.bread.x:
        moveObjects(app, ["background", "table", "wall"], "right")
    

def hitWall(app):
    # if bread and wall collide, move on to prompt screen
    skateboardLeft = app.skateboard.x - app.skateboardWidth // 2 + 60
    skateboardRight = app.skateboard.x + app.skateboardWidth // 2 - 60
    if skateboardLeft <= app.wallX <= app.bread.x + app.breadWidth // 4:
        return True
    else:
        return False
        

def redrawAll(app):
    # drawing different screens
    if app.startScreen:
        drawRect(app.backgroundX, app.backgroundY, app.width, app.height * 4, fill = rgb(240, 192, 115))
        drawRect(424, 210, 622, 570, fill =rgb(254, 213, 145))
        drawLabel("Welcome to I am Toast!", 735, 355, font = "monospace", size = 22)
        drawLabel("Instructions:", 735, 375, font = "monospace")
        drawLabel("Use arrow keys to move", 735, 395, font = "monospace")
        drawLabel("Press space to jump", 735, 415, font = "monospace")
        drawLabel("Avoid touching the floor, ants, or other obstacles!", 735, 435, font = "monospace")
        drawLabel("Press 'b' to begin!", 735, 455, font = "monospace", size = 22)
        drawImage(app.startImage, 615, 490, width = app.startImageWidth//4, height = app.startImageHeight//4)


    elif app.mainScreen:
        drawBoard(app)
        drawBoardBorder(app)

        # Referenced the CMU_Graphics Demo for parameters of drawImage https://piazza.com/class/li3k33dc9yl37f/post/424#:~:text=N23%2DCMUGraphicsDemos.zip
        drawImage(app.backgroundImage, app.backgroundX, app.backgroundY, width = app.backgroundImageWidth*4, height = app.backgroundImageHeight*4)
        drawImage(app.table, app.tableX, app.tableY, width = app.tableWidth//3, height = app.tableHeight//3)
        drawImage(app.skateboardImage, app.skateboard.x, app.skateboard.y, width = app.skateboardWidth//2, height = app.skateboardHeight//2)
        drawImage(app.wall, app.wallX, app.wallY, width = app.wallWidth, height = app.wallHeight)

        drawImage(app.breadImage, app.bread.x, app.bread.y, width = app.breadWidth//2, height = app.breadHeight//2, rotateAngle = app.bread.angle)
        drawLabel(f"Edibility: {app.edibility.counter}%", 99, 60, font = "monspace", bold = True)

    elif app.promptScreen:
        drawRect(app.backgroundX, app.backgroundY, 80000, 80000, fill = rgb(240, 192, 115))
        drawRect(424, 210, 622, 570, fill =rgb(254, 213, 145))
        drawLabel(f"Quick! Hit the key 'f' to climb the counter before time runs out!", 735, 400, font = "monospace")
        drawLabel(f"Time left: {app.timeLeft}", 735, 450, font = "monospace")
    
    elif app.nextLevel:
        drawBoard(app)
        drawRect(0, 0, 80000, 8000, fill = rgb(255, 217, 153))
        drawImage(app.backgroundImage, app.backgroundX, app.backgroundY, width = app.backgroundImageWidth*7, height = app.backgroundImageHeight*7)
        drawImage(app.toasterImage, app.toaster.x, app.toaster.y, width = app.toasterWidth, height = app.toasterHeight)
        drawImage(app.breadImage, app.bread.x, app.bread.y, width = app.breadWidth//2, height = app.breadHeight//2, rotateAngle = app.bread.angle)
        drawLabel(f"Edibility: {app.edibility.counter}%", 99, 60)
        drawImage(app.antsImage, app.ants.x, app.ants.y, width = app.antsWidth//3, height = app.antsHeight//3)
        if app.toasting:
            drawLabel(f"Toasting... {app.toastedAmount}% done", 400, 400)
            drawLabel(f"Press 'd' when done or you'll burn!", 400, 430)

    # two different game over screens
    if app.gameOver and app.toasting:
        drawRect(app.backgroundX, app.backgroundY, 80000, 80000, fill = rgb(240, 192, 115))
        drawRect(424, 210, 622, 570, fill =rgb(254, 213, 145))
        drawLabel(f"I am Toast!", 735, 400, font = "monospace")
        drawLabel(f"Final score: {app.score}", 735, 450, font = "monospace")
    elif app.gameOver:
        drawRect(app.backgroundX, app.backgroundY, 80000, 80000, fill = rgb(240, 192, 115))
        drawRect(424, 210, 622, 570, fill =rgb(254, 213, 145))
        drawLabel("Game over! Press 'r' to restart", 735, 400, font = "monospace")


# drawing 2d grid for referencing locations:
def drawBoard(app):
    for row in range(app.rows):
        for col in range(app.cols):
            drawCell(app, row, col)

def drawBoardBorder(app):
  drawRect(app.boardLeft, app.boardTop, app.boardWidth, app.boardHeight,
           fill=None, border='red',
           borderWidth=2*app.cellBorderWidth)

def drawCell(app, row, col):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)
    drawRect(cellLeft, cellTop, cellWidth, cellHeight,
             fill=None, border='black',
             borderWidth=app.cellBorderWidth)

def getCellLeftTop(app, row, col):
    cellWidth, cellHeight = getCellSize(app)
    cellLeft = app.boardLeft + col * cellWidth
    cellTop = app.boardTop + row * cellHeight
    return (cellLeft, cellTop)

def getCellSize(app):
    cellWidth = app.boardWidth / app.cols
    cellHeight = app.boardHeight / app.rows
    return (cellWidth, cellHeight)




def main():
    runApp()

main()