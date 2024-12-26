#########################################
# File Name: froggyjump.py
# Description: platform game
# Author: Amanda Xi and Jenny Hu
# Date: 05/12/2022
# Due date⚠️: 06/10/2022
#########################################
import pygame
import time
from random import randint

pygame.init()
WIDTH = 500
HEIGHT = 800
gameWindow=pygame.display.set_mode((WIDTH,HEIGHT))


#---------------------------------------#
#BASIC OVERVIEW OF PARTS:               #
#---------------------------------------#
#all screens and navigation, score, scrolling background, hard mode, sound effects, and music done by jenny
#frogs, enemy, platforms, animations done and drawn by amanda


#---------------------------------------#
# functions                             #
#---------------------------------------#

#settings, Hint, Shop, Game Over, and Mode Select: Jenny
def setTitleScreen(): 
  gameWindow.blit(titleIMG, (0,0))
  gameWindow.blit(frogLog, (WIDTH//2-115, HEIGHT//2+110))
  gameWindow.blit(frogCroak[frogCroakPic], (frogCroakX, frogCroakY))
  pygame.display.update()

def setHint():
  gameWindow.blit(helpIMG,(0,0))
  pygame.display.update()

def setShop():
  gameWindow.blit(shopIMG,(0,0))
  pygame.display.update()

def setMode():
  gameWindow.blit(modeIMG,(0,0))
  pygame.display.update()
  
def setDisplay():
  setSky()
  displayPlats()
  setFrog()
  displayEnemies()
  gameWindow.blit(scoreBox,(-50,-72.5))
  displayScore()
  pygame.display.update()
  
def setGameOver():
  gameWindow.blit(overIMG, (0,0))
  scoreInplay = scoreFontBig.render(str(scoreRecent), 1, WHITE)
  gameWindow.blit(scoreInplay, (WIDTH/3+20, 490))
  highScore = scoreFontBig.render(str(scoreHigh), 1, WHITE)
  gameWindow.blit(highScore, (WIDTH/3+45, 555))
  gameWindow.blit(overFrog[frogOverPic], (dizzyX, dizzyY))
  pygame.display.update()

#background scrolling and score: Jenny
def setSky():
    gameWindow.blit(sky,(skyX,skyY))
    gameWindow.blit(sky2, (sky2X, sky2Y))

def displayScore():
  scoreInplay = scoreFont.render(str(scoreRecent), 1, BLACK)
  gameWindow.blit(scoreInplay, (20, 15))

#frog: Amanda
def setFrog(): 
  gameWindow.blit(frogPic[frogPicNum], (frogX, frogY))
  if attacking: 
      gameWindow.blit(tongue, (tongueX, tongueY))
      gameWindow.blit(tongueTip, (tongueX-5, tongueY-10))

#enemy display: Jenny
def displayEnemies():
  if enemyPresent:
    if enemyShift > 0:
      enemyIMG = currentEnemy[enemyPic]
    else:
      enemyIMG = pygame.transform.flip(currentEnemy[enemyPic], True, False) 
    gameWindow.blit(enemyIMG, (enemyX, enemyY))

#platform and mushroom: Amanda
def displayPlats():
  for i in range(len(plats)):
    gameWindow.blit(plats[i], (platsX[i], platsY[i]))
    if hasMushroom[i]:
        gameWindow.blit(mushroomIMG, (platsX[i], platsY[i]-mushroomH))


#collisions: Amanda

#used for platform collision
def collisionTest1(firstX,firstY,firstW, secondX, secondY, secondW, secondH):
    if firstX-secondW+5<=secondX<=firstX+firstW-5 and firstY<=secondY+secondH<=firstY+18:
        return True

#used for mushroom and enemies and tongue
def collisionTest2(firstX,firstY,firstW, firstH, secondX, secondY, secondW, secondH):
    firstRect = pygame.Rect(firstX,firstY,firstW,firstH)
    secondRect = pygame.Rect(secondX, secondY, secondW, secondH)
    if firstRect.colliderect(secondRect):
        return True

#screen navigation: Jenny
def checkClick(x1, x2, y1, y2):
    mousePos[0], mousePos[1] = pygame.mouse.get_pos()
    if x1<=mousePos[0]<=x2 and y1<=mousePos[1]<=y2:
        return True
    
    return False
            
#resetting variables: Jenny
def resetGame():
    clearPlats()
    createPlats()

    global BEGIN
    BEGIN = time.time()
    global platShiftSpeed
    platShiftSpeed = basePlatShift
    global enemyShift
    enemyShift = baseEnemyShift
    global frogY
    frogY = GROUND_LEVEL-200
    global frogX
    frogX = WIDTH//2
    global skyY
    skyY = -skyH+HEIGHT
    global sky2Y
    sky2Y = skyY-skyH
    global newPlat
    newPlat = -1
    global scoreRecent
    scoreRecent = 0
    global enemyPresent
    enemyPresent = False
    global snakeUp
    snakeUp = False
    global enemyUp
    enemyUp = False
    global falling
    falling = False
    global movingChance
    global movingPlats
    if hardMode:
        movingPlats = True
        movingChance = 1
    else:
        movingPlats = False
        movingChance = 15
        
    global inGame
    inGame = True

#creating, clearing, and moving platforms: Amanda
def createPlats():
  for i in range (-1,7):
    minVal = i*100+plat2H
    maxVal = (i+1)*100
    logType = randint(1,5)
    if logType==5:
        plats.append(log2)
    else:
        plats.append(log1)
        
    platsY.append(randint(minVal, maxVal))

    tempX = randint(sideMargin,WIDTH-sideMargin-platsW)
    if i == 6:
        tempX = WIDTH//2-30

    platsX.append(tempX)
    moving.append(False)
    platShift.append(platShiftSpeed)
    hasMushroom.append(False)

def clearPlats():
    for i in range(len(plats)):
        deletePlat()

def createNewPlat():
    logType = randint(1,5)
    if logType==5:
      plats.insert(0,log2)

    else:
      plats.insert(0,log1)

    if platsX[0] > WIDTH//2:
        tempX = randint(sideMargin, platsX[0]-sideMargin-platsW)
    else:
        tempX = randint(platsX[0] + platsW, WIDTH-sideMargin-platsW)

    randMoving = randint(1,movingChance)
    if movingPlats and randMoving == 1:
        moving.insert(0, True)
    else:
        moving.insert(0, False)

    randMushroom = randint(1,10)
    if randMushroom == 10:
        hasMushroom.insert(0,True)
    else:
        hasMushroom.insert(0,False)

    platsX.insert(0,tempX)
    platShift.insert(0,platShiftSpeed)

    if platsY[0] > 100: 
        platsY.insert(0,-plat1H+10)
    elif platsY[0] < 20:
        platsY.insert(0, -plat1H-10)
    else:
        platsY.insert(0, -plat1H)

def deletePlat():
    plats.pop()
    platsY.pop()
    platsX.pop()
    moving.pop()
    platShift.pop()
    hasMushroom.pop()

def movePlats():
  for i in range(len(platsY)):
    platsY[i] += platSpeed

def moveMovingPlats():
  platsX[i]+=platShift[i]
  if platsX[i]>=WIDTH-sideMargin-platsW:
    platShift[i] = -abs(platShiftSpeed)
  elif platsX[i]<=sideMargin:
    platShift[i] = abs(platShiftSpeed)
      
    
#---------------------------------------#
# import files                          #
#---------------------------------------#

#ALL SPRITES AND BACKGROUND DRAWN BY AMANDA (except bird and mossy log) ----------------------------------------------------------------------------------------------------------------------
#ALL GAME SCREENS CREATED BY JENNY -------------------------------------------------------------------------------------------------------------------------------------------------------------         

#screens
titleIMG = pygame.transform.scale(pygame.image.load("resources/new Title Page.png"), (500,800))
helpIMG = pygame.image.load("resources/help.png")
modeIMG = pygame.image.load("resources/Mode Selection.png")
overIMG = pygame.transform.scale(pygame.image.load("resources/Game Over Page.png"), (500,800))
scoreBox = pygame.image.load("resources/score rec.png")
shopIMG = pygame.image.load("resources/Apologies.png")
loadingIMG = pygame.image.load("resources/Loading Page.png")


#sound effects 
overSound = pygame.mixer.Sound("resources/gameOver.wav")
overSound.set_volume(0.5)

mushroomSound = pygame.mixer.Sound("resources/mushroomSound.wav")
mushroomSound.set_volume(0.5)

jumpingSound = pygame.mixer.Sound("resources/jumpSound.wav")
jumpingSound.set_volume(0.3)

screenSound = pygame.mixer.Sound("resources/screenSwitch.wav")
screenSound.set_volume(0.5)

selectSound = pygame.mixer.Sound("resources/selectSound.wav")
selectSound.set_volume(0.5)

hitSound = pygame.mixer.Sound("resources/enemyHit.wav")
hitSound.set_volume(0.5)

attackSound = pygame.mixer.Sound("resources/attack.wav")
attackSound.set_volume(0.5)

enemyHitSound = pygame.mixer.Sound("resources/ouch.wav")
enemyHitSound.set_volume(0.5)


#background
sky = pygame.image.load("resources/frogSky.png")

#enemies 
birdW, birdH = 80,70

bird1 = pygame.transform.scale(pygame.image.load("resources/bird1Transparent.png"), (birdW, birdH))
bird2 = pygame.transform.scale(pygame.image.load("resources/bird2Transparent.png"), (birdW, birdH))
bird3 = pygame.transform.scale(pygame.image.load("resources/bird3Transparent.png"), (birdW, birdH))
bird4 = pygame.transform.scale(pygame.image.load("resources/bird4Transparent.png"), (birdW, birdH))

devilW, devilH = 86, 70

devil1 = pygame.transform.scale(pygame.image.load("resources/devil1.png"), (devilW, devilH))
devil2 = pygame.transform.scale(pygame.image.load("resources/devil2.png"), (devilW, devilH))
devil3 = pygame.transform.scale(pygame.image.load("resources/devil3.png"), (devilW, devilH))

snakeW, snakeH = 76, 92

snake1 = pygame.transform.scale(pygame.image.load("resources/snake1.png"), (snakeW, snakeH))
snake2 = pygame.transform.scale(pygame.image.load("resources/snake2.png"), (snakeW, snakeH))
snake3 = pygame.transform.scale(pygame.image.load("resources/snake3.png"), (snakeW, snakeH))


#frog
frogH1 = 44
frogH2 = 54
frogW1 = 65
frogW2 = 62

frog1 = pygame.transform.scale(pygame.image.load("resources/frog1.png"), (frogW1, frogH1))
frog2 = pygame.transform.scale(pygame.image.load("resources/frog2.png"), (frogW1, frogH1))
frog3 = pygame.transform.scale(pygame.image.load("resources/frog3.png"), (frogW1, frogH1))
frog4 = pygame.transform.scale(pygame.image.load("resources/frog4.png"), (frogW2, frogH2))
frog5 = pygame.transform.scale(pygame.image.load("resources/frog5.png"), (frogW2, frogH2))
frog6 = pygame.transform.scale(pygame.image.load("resources/frog6.png"), (frogW2, frogH2))

frogL1 = pygame.transform.flip(frog1, True, False)
frogL2 = pygame.transform.flip(frog2, True, False)
frogL3 = pygame.transform.flip(frog3, True, False)
frogL4 = pygame.transform.flip(frog4, True, False)
frogL5 = pygame.transform.flip(frog5, True, False)
frogL6 = pygame.transform.flip(frog6, True, False)

frogCroak1 = pygame.image.load("resources/frogCroak1.png")
frogCroak2 = pygame.image.load("resources/frogCroak2.png")
frogCroak3 = pygame.image.load("resources/frogCroak3.png")
frogCroak4 = pygame.image.load("resources/frogCroak4.png")
frogCroak5 = pygame.image.load("resources/frogCroak5.png")

dizzy1 = pygame.image.load("resources/frogdizzy1.png")
dizzy2 = pygame.image.load("resources/frogdizzy2.png")
dizzy3 = pygame.image.load("resources/frogdizzy3.png")

tongue = pygame.image.load("resources/tongue2.png")
tongueTipWH = 10
tongueTip = pygame.transform.scale(pygame.image.load("resources/tongue1.png"), (tongueTipWH,tongueTipWH))


#platforms
platsW = 95
log1 = pygame.transform.scale(pygame.image.load("resources/logRegular.png"), (platsW,25))
frogLog = pygame.transform.scale(pygame.image.load("resources/frogLog.png"), (260,110))
logAlt = pygame.transform.flip(log1, True, False)
log2 = pygame.transform.scale(pygame.image.load("resources/prettyLog.png"), (platsW,43))

mushroomH = 30
mushroomW = 40
mushroom1 = pygame.transform.scale(pygame.image.load("resources/mushroom1.png"), (mushroomW, mushroomH))
mushroom2 = pygame.transform.scale(pygame.image.load("resources/mushroom2.png"), (mushroomW, mushroomH))
mushroomIMG = mushroom1

#fonts
scoreFont = pygame.font.Font("resources/ARCADECLASSIC.TTF", 25)
scoreFontBig = pygame.font.Font("resources/ARCADECLASSIC.TTF", 40)

#---------------------------------------#
# variable setup                        #
#---------------------------------------#

#colour properties
WHITE = (255,255,255)
BLACK = (  0,  0,  0)
BLUE = (102, 178, 255)
RED = (230, 50, 50)

#clock properties
clock = pygame.time.Clock()
titleFPS = 8
FPS = 35
overFPS = 5

#frog propoerties
GROUND_LEVEL = 650
newPlat = -1
RUN_SPEED = 9
JUMP_SPEED = -20
GRAVITY = 1
frogH = frogH1
frogW = frogW1
frogX = WIDTH/2
frogY = GROUND_LEVEL-200
frogVx = 0
frogVy = 0 
frogVyMAX = 16
frogPicNum = 3                        
frogDir = "right"                       
frogPic = [0, frog1, frog2, frog3, frog4, frog5, frog6, frogL1, frogL2, frogL3, frogL4, frogL5, frogL6]

frogCroak = [frogCroak1, frogCroak2, frogCroak3, frogCroak4, frogCroak5, frogCroak2]
frogCroakPic = 0
frogCroakX = WIDTH//2-50
frogCroakY = HEIGHT//2+40
frogLogX = frogCroakX-65
frogLogY = frogCroakY+70

overFrog = [dizzy1, dizzy2, dizzy3, dizzy2]
frogOverPic = 0
dizzyX = 190
dizzyY = 310


tongueX = 0
tongueY = 0
tongueStartH = 10
tongueH = tongueStartH
tongueMaxH = 200
tongueW = 5

#background properties
sky2 = sky
skyH = 12000
skyX = 0
skyY = -skyH+HEIGHT
sky2X = 0
sky2Y = skyY-skyH

#platforn properties
plats = []
platsX = []
platsY = []
plat1H = 25
plat2H = 43
platSpeed = 10
sideMargin = 40
moving = []
movingPlats = False
movingChance = 15
movingChanceMin = 5
movingPlatPeriod = 15
basePlatShift = 5
platShiftSpeed = basePlatShift
maxPlatShift = 9
platShift = []
hasMushroom = []

#enemy properties
enemyList = [[bird1]*10 + [bird2]*10 + [bird3]*10 + [bird4]*10, [devil1]*10 +[devil2]*10 + [devil3]*10, [snake1]*10+ [snake2]*10+ [snake3]*10]
enemyHList = [birdH, devilH, snakeH]
enemyWList =  [birdW, devilW, snakeW]
currentEnemy = None   
enemyPic = None
enemyH = None
enemyW = None
enemyX = None
enemyY = None
enemyPresent = False
snakeUp = False
enemyUp = False
lastScore = 0
baseEnemyShift = 4
enemyShift = baseEnemyShift
maxEnemyShift = 10

#time variables
canAttack = True
coolDownPeriod = 0.7
attackPeriod = 0.5

#frog variables
attacking = False
onPlatform = False
springing = False
falling = False

#score variables
scoreRecent = 0
scoreHigh = 0
lastDifficultyBoost = 0

#fun facts (these did not end up being used, but we spent time researching them and they are fun so please read some of them) 
funfacts = ["Frogs have been around for 200 million years!",
"The world’s biggest frog, the goliath frog, can grow up to 15 inches",
"The world’s smallest frog, the Cuban tree toad, grows to only half an inch",
"There are over 6,000 frog species in the world!",
"As amphibians frogs can breathe through their skin while underwater",
"A frog's call is unique to its species, and some frog calls can be heard up to a mile away",
"Frogs use their eyes to help them swallow, pushing them down to help food down their throat",
"Frogs have excellent night vision and with their bulging eyes, they can see almost fully around them",
"Frogs were the first land animals with vocal cords. Ribbit!",
"With their long and powerful legs, frogs can leap up to 20 times their body length",
"Frogs are freshwater creatures, although some frogs such as the Florida leopard frog are able to live in brackish or nearly completely salt waters"]

#loop variables
inPlay = True
titleScreen = True
hint = False
shop = False
modeSelect = False
inGame = False
gameOver = False

#settings variables
fromTitleClick = False
fromShopClick = False
fromHintClick = False
hardMode = False

#screens variables
mousePos = [0,0]

#---------------------------------------#
# main program                          #
#---------------------------------------#

while inPlay:

  #load title screen music: Jenny
  if titleScreen and not (fromShopClick or fromHintClick):
      pygame.mixer.music.load("resources/menuMusic.mp3")
      pygame.mixer.music.set_volume(0.4)
      pygame.mixer.music.play(-1)
      
  #TITLE SCREEN AND CONTROLS: JENNY -----------------------------------------------------------------------------------------------------------------------------------------
  while titleScreen:
    clock.tick(titleFPS)
    setTitleScreen()

    #get mouse position for pressing buttons
    for event in pygame.event.get():

        #make sure that the click event is not from the previous screen
        if fromShopClick and event.type == pygame.MOUSEBUTTONUP: 
          fromShopClick = False

        elif fromHintClick and event.type == pygame.MOUSEBUTTONUP: 
          fromHintClick = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            #hint button
            if checkClick(331, 391, 19, 79):
                titleScreen = False
                hint = True
                screenSound.play(0)
                pygame.event.clear()
        
            #shop button
            elif checkClick(409, 469, 19, 79) and not fromShopClick and not fromHintClick:
                fromTitleClick = True
                titleScreen = False
                shop = True
                screenSound.play(0)
                pygame.event.clear()

    #animate frog
    if frogCroakPic<5:
      frogCroakPic += 1
      
    else:
      frogCroakPic = 0
      
    keys = pygame.key.get_pressed()
    
    #quit
    if keys[pygame.K_ESCAPE]:
        titleScreen = False
        inPlay = False

    #start
    if keys[pygame.K_SPACE]:     
        pygame.mixer.music.fadeout(200)
        titleScreen = False
        modeSelect = True
        selectSound.play(0)
        
  #MODE SELECTION AND CONTROLS: JENNY -----------------------------------------------------------------------------------------------------------------------------------------
  while modeSelect:
    setMode()
    for event in pygame.event.get():
      if event.type == pygame.MOUSEBUTTONDOWN:
        #normal mode
        if checkClick(166, 332, 266, 348) or checkClick(166, 332, 432, 504):
          hardMode = False
          gameMusic1 = pygame.mixer.music.load("resources/gameMusicEasy.mp3")

          #hard mode
          if checkClick(166, 332, 432, 504):
            hardMode = True
            gameMusic2 = pygame.mixer.music.load("resources/gameMusicHard.mp3")

          #set game and music
          modeSelect = False
          resetGame()
          selectSound.play(0)
          pygame.mixer.music.set_volume(0.2)
          pygame.mixer.music.play(-1)
      
  #HINT SCREEN AND CONTROLS: JENNY -----------------------------------------------------------------------------------------------------------------------------------------
  while hint:
    setHint()
    for event in pygame.event.get():
      #exit button
      if event.type == pygame.MOUSEBUTTONDOWN :
        if checkClick(405, 465, 21, 81):
          hint = False
          titleScreen = True
          fromHintClick = True
          screenSound.play(0)
          pygame.event.clear()

  #SHOP SCREEN AND CONTROLS: JENNY -----------------------------------------------------------------------------------------------------------------------------------------
  while shop:
    setShop()
    for event in pygame.event.get():
      #make sure that the click event is not from the previous screen
      if fromTitleClick and event.type == pygame.MOUSEBUTTONUP:
        fromTitleClick = False

      #exit button
      if event.type == pygame.MOUSEBUTTONDOWN:
        if checkClick(405, 465, 21, 81):
          fromShopClick = True
          shop = False
          titleScreen = True
          screenSound.play(0)
          pygame.event.clear()

  #IN GAME LOOP ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------     
  while inGame:
    pygame.event.clear()
    clock.tick(FPS)
    setDisplay()
    keys = pygame.key.get_pressed()

    #setting background: Jenny
    if skyY >= skyH: 
        skyY = -skyH
        sky2Y = 0
    elif sky2Y >= skyH:
        sky2Y = -skyH
        skyY = 0

    #FROG MOTION AND PLATFORMS: AMANDA (unless stated otherwise) -----------------------------------------------------------------------------------------------------------------------------------------
    for i in range (len(plats)):
      #if frog hits platform
      if frogVy > 0 and collisionTest1(platsX[i], platsY[i], platsW,frogX,frogY,frogW,frogH) and not falling:
        onPlatform = True
        newPlat = i
        platSpeed = 10
        jumpingSound.play(0)
        springing = False
        break
      else:
        onPlatform = False

      #jump on mushroom
      if hasMushroom[i]:
          if frogVy > 0 and collisionTest2(frogX,frogY,frogW, frogH, platsX[i], platsY[i]-mushroomH, mushroomW, mushroomH) and not falling:
              mushroomIMG = mushroom2
              onPlatform = True
              newPlat = 1
              platSpeed = 20
              springing = True
              mushroomSound.play(0)
              break
          else:
              mushroomIMG = mushroom1
              onPlatform = False

      #move moving platforms
      if moving[i]:
        moveMovingPlats()

    #frog attack
    if keys[pygame.K_UP] and canAttack and not falling:
        attacking = True
        canAttack = False
        referenceTime = time.time()
        frogH = frogH2
        frogW = frogW2
        frogY -= 5
        tongueH = tongueStartH
        attackSound.play(0)

    #frog move left
    if keys[pygame.K_LEFT] and not falling:
        frogVx = -RUN_SPEED
        frogDir = "left"

    #frog move right
    elif keys[pygame.K_RIGHT] and not falling:
        frogVx = RUN_SPEED
        frogDir = "right"
        
    #frog not moving horizontally
    else:                              
        frogVx = 0                    

    #if frog is on platform
    if onPlatform:
        if frogDir == "right":
            if attacking:
                frogPicNum = 4
            else: 
                frogPicNum = 1 
        elif frogDir == "left":
            if attacking:
                frogPicNum = 10
            else: 
                frogPicNum = 7
        #make frog jump
        frogVy = JUMP_SPEED

    #move platforms, frog, and background:
    #every time the frog jumps on a new platform, that platform is moved to a set GROUND_LEVEL
    if platsY[newPlat]<GROUND_LEVEL and not falling:
        movePlats()
        scoreRecent += 1
        
        #if frog jumps on mushroom, reduce gravity on frog
        if not springing: 
            frogY+=platSpeed
        else:
            frogY += 2

        #move sky
        skyY += platSpeed//3
        sky2Y += platSpeed//3

        #move enemy
        if enemyPresent: 
          enemyY += platSpeed
          
    else:
        if springing:
            springing = False

    #edit frog picture based on distance to platform 
    if frogY+frogH<=platsY[newPlat]-50:
        if frogDir == "right":
            if attacking:
                frogPicNum = 5
            else: 
                frogPicNum = 2            
        elif frogDir == "left":
            if attacking:
                frogPicNum = 11
            else: 
                frogPicNum = 8

        if frogY+frogH<=platsY[newPlat]-120:
            if frogDir == "right":
                if attacking:
                    frogPicNum = 6
                else: 
                    frogPicNum = 3             
            elif frogDir == "left":
                if attacking:
                    frogPicNum = 12
                else: 
                    frogPicNum = 9

    #move frog in horizontal direction
    frogX = frogX + frogVx

    #if frog leaves screen, comes back on other side
    if frogX > WIDTH:
      frogX = 0-frogW
    elif frogX+frogW < 0:
      frogX = WIDTH
    
    #update frog's vertical velocity
    if frogVy<frogVyMAX:
        frogVy = frogVy + GRAVITY
        
    #move frog in vertical direction
    frogY = frogY + frogVy

    #timing for attack
    if attacking:
        attackTime = time.time() - referenceTime
        if attackTime > attackPeriod:
          attacking = False
          frogH = 48

        #move tongue
        elif attackTime < attackPeriod/2:
          tongueH += 27

        elif attackTime > attackPeriod/2:
          if tongueH > 27:
            tongueH -= 27

        if tongueH < 0:
          tongueH = 0
        
        tongue = pygame.transform.scale(tongue, (tongueW, tongueH))

        #position tongue: Jenny
        tongueY = frogY - tongueH + 27
        if frogDir == "right":
            tongueX = frogX + 40
        else:
            tongueX = frogX + 18

        #check tongue collision with enemy: Jenny
        if enemyPresent:
            if collisionTest2(tongueX, tongueY, tongueW, tongueH, enemyX+5, enemyY, enemyW-5, enemyH) or collisionTest2(tongueX-5, tongueY-10, tongueTipWH, tongueTipWH, enemyX+5, enemyY, enemyW-5, enemyH) and not falling:
                enemyPresent = False
                hitSound.play(0)
              
    #calculate time between attacks
    if not canAttack:
        elapsed = time.time() - referenceTime
        if elapsed>coolDownPeriod:
            canAttack = True


    #PLATFORMS: AMANDA --------------------------------------------------------------------------------------------------------------------------------------------------------------
            
    #creating new platforms:
    if platsY[-1] > HEIGHT:
      deletePlat()
      newPlat +=1
      createNewPlat()

      #spawning in enemies based on platform location, do not spawn if mushroom-jumping
      if snakeUp and not springing:
        #snakes don't spawn on moving logs
        if not moving[0]:
          enemyPresent = True
          enemyX = platsX[0] + 10
          #snake location changes based on log type
          if plats[0] == log2:
            enemyY = platsY[0] -10
          else:
            enemyY = platsY[0] - 14
          snakeUp = False
        else:
          snakeUp = False
          enemyPresent = False

      #spawn enemy at random x location
      elif enemyUp and not springing:
        enemyX = randint(sideMargin, WIDTH-sideMargin-enemyW)
        enemyY = platsY[0] - 10 - enemyH
        enemyPresent = True
        enemyUp = False
      
    #calculate time to start moving platforms 
    inGameTime = time.time()-BEGIN
    if not movingPlats and inGameTime > movingPlatPeriod:
        movingPlats = True

    #ENEMIES: JENNY AND AMANDA -------------------------------------------------------------------------------------------------------------------------------------------
    
    #spawning enemies: Amanda
        
    #uses the same variable as movingPlats: when moving platforms are introduced, enemies are as well
    if movingPlats:     
      #spawn enemy chance every 100 scores, scoreRecent variable set to make sure the same score isn't counted multiple times
      if scoreRecent%100 == 0 and scoreRecent!= 0 and scoreRecent!= lastScore and not enemyPresent:
        lastScore = scoreRecent
        
        #50% chance of enemy spawning
        chanceNum = randint(1,2)

        if chanceNum == 1:
          #generate random enemy
          randomEnemy = randint(0,2)
          currentEnemy = enemyList[randomEnemy]
          enemyPic = 0
          enemyW = enemyWList[randomEnemy]
          enemyH = enemyHList[randomEnemy]
          
          #different variable for snake because it is postiioned differently on log
          if randomEnemy == 2:
            snakeUp = True
          else:
            enemyUp = True
            
        else:
          enemyPresent = False

      #increasing difficult based on score: Amanda
      if scoreRecent%420 == 0 and scoreRecent!=0 and scoreRecent != lastDifficultyBoost:
          lastDifficultyBoost = scoreRecent

          #increase chance of moving platforms, speed of platforms and enemies
          if movingChance > movingChanceMin:
              movingChance -= 2
              
          if platShiftSpeed < maxPlatShift:
              platShiftSpeed += 1
              
          if abs(enemyShift) < maxEnemyShift:
              if enemyShift>0:
                  enemyShift += 1
              else:
                  enemyShift -= 1

    #despawning enemy: Jenny
    if enemyPresent:
      if enemyY >= HEIGHT:
        enemyPresent = False

      #animate enemy: Amanda
      enemyPic += 1
      if enemyPic == len(currentEnemy):
        enemyPic = 0

      #moving enemies left and right: Amanda
      if currentEnemy == enemyList[0] or currentEnemy == enemyList[1]:
        enemyX+=enemyShift
        if enemyX>=WIDTH-sideMargin-enemyW:
          enemyShift = -abs(enemyShift)
        elif enemyX<=sideMargin:
          enemyShift = abs(enemyShift)

      #check collision: Jenny
      if collisionTest2(frogX,frogY+5,frogW, frogH-5, enemyX+10, enemyY, enemyW-10, enemyH-10) and not falling:
          #if frog is moving up, game over
          if frogVy < 0: 
            falling = True
            frogVy = 10
            frogVx = 0
            newPlat = -1
            enemyHitSound.play(0)

          #if frog is moving down on enemy, enemy dies
          else:
            enemyPresent = False
            hitSound.play(0)
            
            #if frog hits flying enemies, jump back up
            if currentEnemy == enemyList[0] or currentEnemy == enemyList[1]: 
                frogVy = JUMP_SPEED           

    #ending the game
    if frogY>HEIGHT:
      inGame = False
      gameOver = True
      overSound.play(0)

#GAME OVER SCREEN: JENNY -------------------------------------------------------------------------------------------
  while gameOver:
    pygame.event.clear()
    clock.tick(overFPS)
    
    keys = pygame.key.get_pressed()

    #set high score                      
    if scoreRecent > scoreHigh:
      scoreHigh = scoreRecent

    #animate frog
    if frogOverPic<3:
      frogOverPic += 1
    else:
      frogOverPic = 0

    setGameOver()

    #restart game
    if keys[pygame.K_SPACE]:
      gameOver = False
      resetGame()

    #go to menu
    elif keys[pygame.K_m]:
      gameOver = False
      titleScreen = True
      pygame.mixer.music.fadeout(200)

    pygame.event.pump()

pygame.quit()
