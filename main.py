# Epoc Bomb Game Thing
# Version 27
# Developed by Turtlerock Industries led by @Commandline
# A grid-based strategy game

#sys init
import pygame as game
import time
import random
import math
import sys
from pygame import mixer
from pygame import gfxdraw

game.init()

#display init
screen = game.display.set_mode((800,600))
game.display.set_caption("Epoc Bomb Game Thing")

#icon init
icon_image = game.image.load("images/icon.png")
game.display.set_icon(icon_image)


#----game init----

#var init
os = sys.platform
clock = game.time.Clock()
lastMoveTime = 0.0
bombCooldown = 0
bombs = 3
bombsLeft = 3
bombX = []
bombY = []
score = 0
volume = True
targetsLeft = 0
round = 1
maxRounds = 37
roundStarted = False
shardsLeft = -1
shardsLoaded = False
display = "title"
titlethemeon = True
buttonIndex = 1
tutorialStage = 0
tutorialOnce = True
tutorial3pass = False
tutorialLoad = False
navigationButtonPressed = False
spacebarWait = False
targetList = []
shadowBoxStart = True
shadowBoxAlpha = 255
laserTimer = 0.0
laserOn = False
touchedByLaser = False
atTitleStart = True

#music init
game.mixer.init()
playTheme = game.mixer.Sound("sounds/theme.mp3")
playTitleTheme = game.mixer.Sound("sounds/titletheme.mp3")
hit = game.mixer.Sound("sounds/hit.wav")
explosion = game.mixer.Sound("sounds/explosion.wav")
laserSFX = game.mixer.Sound("sounds/spaceLaser.wav")
playTitleTheme.play(-1)

#--class init--
class Player(game.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = game.Surface([width, height])
        if os == "darwin":
            self.image = game.transform.scale(game.image.load("images/squareDesignsMac/playerSquare.svg").convert_alpha(), (25, 25))
        elif os == "win32":
            self.image = game.transform.scale(game.image.load("images/squareDesignsWin/playerSquare.svg").convert_alpha(), (25, 25))
        #self.image.fill((148, 3, 252))  # Purple color (RGB)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        # No automatic movement, position is updated manually
        pass

    def move(self, dx, dy):
        # Update the sprite's position and store it
        self.rect.x += dx
        self.rect.y += dy
    
    def goto(self, sx, sy):
        # Update the sprite's position and store it
        self.rect.x = sx
        self.rect.y = sy


class Bomb(game.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = game.Surface([width, height])
        if os == "darwin":
            self.image = game.transform.scale(game.image.load("images/squareDesignsMac/bombSquare.svg").convert_alpha(), (25, 25))
        elif os == "win32":
            self.image = game.transform.scale(game.image.load("images/squareDesignsWin/bombSquare.png").convert_alpha(), (25, 25))
        #self.image.fill((0, 0, 255))  # Purple color (RGB)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        # No automatic movement, position is updated manually
        pass

    def place(self, dx, dy):
        # Update the sprite's position and store it
        self.rect.x = dx
        self.rect.y = dy

    def explode(self):
        directions = ["up", "down", "left", "right", "up_left", "up_right", "down_left", "down_right"]
        for direction in directions:
            shard = Shard(self.rect.x, self.rect.y, 25, 25, direction)
            all_sprites.add(shard)
            shard_group.add(shard)
        self.kill()
        del self
        self = None


class Target(game.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = game.Surface([width, height])
        if os == "darwin":
            self.image = game.transform.scale(game.image.load("images/squareDesignsMac/targetSquare.svg").convert_alpha(), (25, 25))
        elif os == "win32":
            self.image = game.transform.scale(game.image.load("images/squareDesignsWin/targetSquare.png").convert_alpha(), (25, 25))
        #self.image.fill((255, 0, 0))  # Red color (RGB)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        global targetsLeft
        targetsLeft += 1

    def update(self):
        if game.sprite.spritecollideany(self, shard_group):
            self.kill()
            global score
            global targetsLeft
            if display == "game":
                score += 100
            targetsLeft -= 1
            global hit
            hit.play()

    def move(self, dx, dy):
        # Update the sprite's position and store it
        self.rect.x += dx
        self.rect.y += dy
        

class Shard(game.sprite.Sprite):
    def __init__(self, x, y, width, height, direction):
        super().__init__()
        self.image = game.Surface([width, height])
        if os == "darwin":
            self.image = game.transform.scale(game.image.load("images/squareDesignsMac/shardSquare.svg").convert_alpha(), (25, 25))
        elif os == "win32":
            self.image = game.transform.scale(game.image.load("images/squareDesignsWin/shardSquare.png").convert_alpha(), (25, 25))
        #self.image.fill((249, 147, 5))  # Orange color (RGB)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = direction  # Stores direction (up, down, left, right, etc.)
        self.speed = 25  # Adjust shard speed here
        self.lastMoveTime = 0.0

    def update(self):
        self.lastMoveTime += dt
        # Update movement based on direction
        if self.lastMoveTime >= 0.075:
            if self.direction == "up":
                self.rect.y -= self.speed
            elif self.direction == "down":
                self.rect.y += self.speed
            elif self.direction == "left":
                self.rect.x -= self.speed
            elif self.direction == "right":
                self.rect.x += self.speed
            # Add diagonal movement logic here
            elif self.direction == "up_left":
                self.rect.x -= self.speed
                self.rect.y -= self.speed
            elif self.direction == "up_right":
                self.rect.x += self.speed
                self.rect.y -= self.speed
            elif self.direction == "down_left":
                self.rect.x -= self.speed
                self.rect.y += self.speed
            elif self.direction == "down_right":
                self.rect.x += self.speed
                self.rect.y += self.speed
            self.lastMoveTime = 0.0
        # Add checks for walls or other objects to stop the shard movement
        if display == "game" or display == "tutorial":
            if game.sprite.spritecollideany(self, wall_group):
                self.kill()
                del self
                self = None
        if display == "title":
            if game.sprite.spritecollideany(self, wall_group_title):
                self.kill()
                del self
                self = None


class Wall(game.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = game.Surface([width, height])
        self.image.fill((56, 140, 70))  # Gray color RGB ( 92, 92, 92)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        # No automatic movement, position is updated manually
        pass

    #there is no need to update position to a wall


class Hole(game.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = game.Surface([width, height])
        if os == "darwin":
            self.image = game.transform.scale(game.image.load("images/squareDesignsMac/holeSquare.svg").convert_alpha(), (25, 25))
        elif os == "win32":
            self.image = game.transform.scale(game.image.load("images/squareDesignsWin/holeSquare.png").convert_alpha(), (25, 25))
        #self.image.fill((0, 0, 0))  # yellow color (RGB)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        # No automatic movement, position is updated manually
        pass

    def move(self, dx, dy):
        # Update the sprite's position and store it
        self.rect.x += dx
        self.rect.y += dy
    
    def goto(self, sx, sy):
        # Update the sprite's position and store it
        self.rect.x = sx
        self.rect.y = sy


class Diode(game.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = game.Surface([width, height])
        if os == "darwin":
            self.image = game.transform.scale(game.image.load("images/squareDesignsMac/diodeSquare.svg").convert_alpha(), (25, 25))
        elif os == "win32":
            self.image = game.transform.scale(game.image.load("images/squareDesignsWin/diodeSquare.png").convert_alpha(), (25, 25))
        #self.image.fill((0, 0, 0))  # yellow color (RGB)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        # No automatic movement, position is updated manually
        pass

    def move(self, dx, dy):
        # Update the sprite's position and store it
        self.rect.x += dx
        self.rect.y += dy
    
    def goto(self, sx, sy):
        # Update the sprite's position and store it
        self.rect.x = sx
        self.rect.y = sy

    def makeLasers(self):
        # creates horizontal and vertical lasers
        laserSFX.play()

        #positive X gen
        for i in range(1, 21):
            laser = Laser(self.rect.x + i * 25, self.rect.y, 25, 25, "horizontal")
            if laser.update() == True:
                break
            all_sprites.add(laser)
            laser_group.add(laser)
        
        #negative X gen
        for i in range(1, 21):
            laser = Laser(self.rect.x + -i * 25, self.rect.y, 25, 25, "horizontal")
            if laser.update() == True:
                break
            all_sprites.add(laser)
            laser_group.add(laser)

        #positive Y gen
        for i in range(1, 21):
            laser = Laser(self.rect.x, self.rect.y + i * 25, 25, 25, "vertical")
            if laser.update() == True:
                break
            all_sprites.add(laser)
            laser_group.add(laser)
        
        #negative Y gen
        for i in range(1, 21):
            laser = Laser(self.rect.x, self.rect.y + -i * 25, 25, 25, "vertical")
            if laser.update() == True:
                break
            all_sprites.add(laser)
            laser_group.add(laser)
    
    def destroyLasers(self):
        # removes all lasers in the map
        for laser in laser_group.sprites():
            if isinstance(laser,Laser):
                all_sprites.remove(laser)
                laser_group.remove(laser)
                laser.kill()
                del laser
                laser = None


class Laser(game.sprite.Sprite):
    def __init__(self, x, y, width, height, direction):
        super().__init__()
        self.image = game.Surface([width, height])
        self.direction = direction
        if os == "darwin":
            if self.direction == "vertical":
                self.image = game.transform.scale(game.image.load("images/squareDesignsMac/verticalLaser.svg").convert_alpha(), (25, 25))
            if self.direction == "horizontal":
                self.image = game.transform.scale(game.image.load("images/squareDesignsMac/horizontalLaser.svg").convert_alpha(), (25, 25))
        elif os == "Windows":
            if self.direction == "vertical":
                self.image = game.transform.scale(game.image.load("images/squareDesignsWin/verticalLaser.png").convert_alpha(), (25, 25))
            if self.direction == "horizontal":
                self.image = game.transform.scale(game.image.load("images/squareDesignsWin/horizontalLaser.png").convert_alpha(), (25, 25))
        #self.image.fill((0, 0, 0))  # yellow color (RGB)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        if game.sprite.spritecollideany(self, wall_group):
            self.kill()
            del self
            self = None

    def update(self):
        if game.sprite.spritecollideany(self, wall_group):
            self.kill()
            del self
            self = None
            return True

    def move(self, dx, dy):
        # Update the sprite's position and store it
        self.rect.x += dx
        self.rect.y += dy
    
    def goto(self, sx, sy):
        # Update the sprite's position and store it
        self.rect.x = sx
        self.rect.y = sy
#--end of class init--


#--function init--
def createTargetsTitle():
    randomSquare = [random.randint(5,21)*25,random.randint(0,16)*25]

    #top target
    targets = Target(randomSquare[0], randomSquare[1], 25, 25)
    title_sprites.add(targets)
    for i in range(random.randint(1,20)):
        targets.move(0,-25)
        if game.sprite.collide_rect(targets, topBorderTitle):
            targets.move(0,25)
    
    #bottom target
    targets = Target(randomSquare[0], randomSquare[1], 25, 25)
    title_sprites.add(targets)
    for i in range(random.randint(1,20)):
        targets.move(0,25)
        if game.sprite.collide_rect(targets, bottomBorderTitle):
            targets.move(0,-25)
    
    #left target
    targets = Target(randomSquare[0], randomSquare[1], 25, 25)
    title_sprites.add(targets)
    for i in range(random.randint(1,20)):
        targets.move(-25, 0)
        if game.sprite.collide_rect(targets, leftBorderTitle):
            targets.move(25, 0)
    
    #right target
    targets = Target(randomSquare[0], randomSquare[1], 25, 25)
    title_sprites.add(targets)
    for i in range(random.randint(1,20)):
        targets.move(25, 0)
        if game.sprite.collide_rect(targets, rightBorderTitle):
            targets.move(-25, 0)
    
    #top-left target
    targets = Target(randomSquare[0], randomSquare[1], 25, 25)
    title_sprites.add(targets)
    for i in range(random.randint(1,20)):
        targets.move(0, -25)
        targets.move(-25, 0)
        if game.sprite.collide_rect(targets, topBorderTitle) or game.sprite.collide_rect(targets, leftBorderTitle):
            targets.move(0, 25)
            targets.move(25, 0)
    
    #top-right target
    targets = Target(randomSquare[0], randomSquare[1], 25, 25)
    title_sprites.add(targets)
    for i in range(random.randint(1,20)):
        targets.move(0, -25)
        targets.move(25, 0)
        if game.sprite.collide_rect(targets, topBorderTitle) or game.sprite.collide_rect(targets, rightBorderTitle):
            targets.move(0, 25)
            targets.move(-25, 0)
    
    #bottom-left target
    targets = Target(randomSquare[0], randomSquare[1], 25, 25)
    title_sprites.add(targets)
    for i in range(random.randint(1,20)):
        targets.move(0, 25)
        targets.move(-25, 0)
        if game.sprite.collide_rect(targets, bottomBorderTitle) or game.sprite.collide_rect(targets, leftBorderTitle):
            targets.move(0, -25)
            targets.move(25, 0)
    
    #bottom-right target
    targets = Target(randomSquare[0], randomSquare[1], 25, 25)
    title_sprites.add(targets)
    for i in range(random.randint(1,20)):
        targets.move(0, 25)
        targets.move(25, 0)
        if game.sprite.collide_rect(targets, bottomBorderTitle) or game.sprite.collide_rect(targets, rightBorderTitle):
            targets.move(0, -25)
            targets.move(-25, 0)


def createTargets():
    randomSquare = [random.randint(1,21)*25,random.randint(1,21)*25]
    targetList.append(randomSquare)

    #top target
    targets = Target(randomSquare[0], randomSquare[1], 25, 25)
    all_sprites.add(targets)
    target_group.add(targets)
    for i in range(random.randint(1,20)):
        targets.move(0,-25)
        if game.sprite.collide_rect(targets, topBorder):
            targets.move(0,25)
    
    #bottom target
    targets = Target(randomSquare[0], randomSquare[1], 25, 25)
    all_sprites.add(targets)
    target_group.add(targets)
    for i in range(random.randint(1,20)):
        targets.move(0,25)
        if game.sprite.collide_rect(targets, bottomBorder):
            targets.move(0,-25)
    
    #left target
    targets = Target(randomSquare[0], randomSquare[1], 25, 25)
    all_sprites.add(targets)
    target_group.add(targets)
    for i in range(random.randint(1,20)):
        targets.move(-25, 0)
        if game.sprite.collide_rect(targets, leftBorder):
            targets.move(25, 0)
    
    #right target
    targets = Target(randomSquare[0], randomSquare[1], 25, 25)
    all_sprites.add(targets)
    target_group.add(targets)
    for i in range(random.randint(1,20)):
        targets.move(25, 0)
        if game.sprite.collide_rect(targets, rightBorder):
            targets.move(-25, 0)
    
    #top-left target
    targets = Target(randomSquare[0], randomSquare[1], 25, 25)
    all_sprites.add(targets)
    target_group.add(targets)
    for i in range(random.randint(1,20)):
        targets.move(0, -25)
        targets.move(-25, 0)
        if game.sprite.collide_rect(targets, topBorder) or game.sprite.collide_rect(targets, leftBorder):
            targets.move(0, 25)
            targets.move(25, 0)
    
    #top-right target
    targets = Target(randomSquare[0], randomSquare[1], 25, 25)
    all_sprites.add(targets)
    target_group.add(targets)
    for i in range(random.randint(1,20)):
        targets.move(0, -25)
        targets.move(25, 0)
        if game.sprite.collide_rect(targets, topBorder) or game.sprite.collide_rect(targets, rightBorder):
            targets.move(0, 25)
            targets.move(-25, 0)
    
    #bottom-left target
    targets = Target(randomSquare[0], randomSquare[1], 25, 25)
    all_sprites.add(targets)
    target_group.add(targets)
    for i in range(random.randint(1,20)):
        targets.move(0, 25)
        targets.move(-25, 0)
        if game.sprite.collide_rect(targets, bottomBorder) or game.sprite.collide_rect(targets, leftBorder):
            targets.move(0, -25)
            targets.move(25, 0)
    
    #bottom-right target
    targets = Target(randomSquare[0], randomSquare[1], 25, 25)
    all_sprites.add(targets)
    target_group.add(targets)
    for i in range(random.randint(1,20)):
        targets.move(0, 25)
        targets.move(25, 0)
        if game.sprite.collide_rect(targets, bottomBorder) or game.sprite.collide_rect(targets, rightBorder):
            targets.move(0, -25)
            targets.move(-25, 0)


def writeText(input, textfont, fontsize, R, G, B, X, Y):
    font = game.font.SysFont(textfont, fontsize)
    textwrite = font.render(input, True, (R, G, B))
    textRectwrite = textwrite.get_rect()
    textRectwrite.center = (X, Y)
    screen.blit(textwrite, textRectwrite)


def movement(collisionGroup):
    key = game.key.get_pressed()
    global lastMoveTime
    global touchedByLaser

    if key[game.K_a] or key[game.K_LEFT] or key[game.K_d] or key[game.K_RIGHT] or key[game.K_s] or key[game.K_DOWN] or key[game.K_w] or key[game.K_UP]:
        lastMoveTime += dt 
    
    if lastMoveTime >= .075:
        #movement checks with collision
        if key[game.K_a] or key[game.K_LEFT]:
            player.move(-25,0)
            if game.sprite.spritecollideany(player, collisionGroup) or game.sprite.spritecollideany(player, hole_group) or game.sprite.spritecollideany(player, diode_group):
                player.move(25,0)
        if key[game.K_d] or key[game.K_RIGHT]:
            player.move(25,0)
            if game.sprite.spritecollideany(player, collisionGroup) or game.sprite.spritecollideany(player, hole_group) or game.sprite.spritecollideany(player, diode_group):
                player.move(-25,0)
        if key[game.K_s] or key[game.K_DOWN]:
            player.move(0,25)
            if game.sprite.spritecollideany(player, collisionGroup) or game.sprite.spritecollideany(player, hole_group) or game.sprite.spritecollideany(player, diode_group):
                player.move(0,-25)
        if key[game.K_w] or key[game.K_UP]:
            player.move(0,-25)
            if game.sprite.spritecollideany(player, collisionGroup) or game.sprite.spritecollideany(player, hole_group) or game.sprite.spritecollideany(player, diode_group):
                player.move(0,25)
        lastMoveTime = 0.0
    
    if game.sprite.spritecollideany(player, laser_group) and not touchedByLaser:
        touchedByLaser = True
        global bombsLeft
        global bombCooldown
        global spacebarWait

        for i in range(bombsLeft):
            bombX.append(player.rect.x)
            bombY.append(player.rect.y)
            bomb = Bomb(player.rect.x, player.rect.y, 25, 25)
            all_sprites.add(bomb)
            bombCooldown = 3

        for i in range(len(bombX)):
            directions = ["up", "down", "left", "right", "up_left", "up_right", "down_left", "down_right"]
            for direction in directions:
                shard = Shard(bombX[i], bombY[i], 25, 25, direction)
                all_sprites.add(shard)
                shard_group.add(shard)
        for bomb in all_sprites.sprites():
            if isinstance(bomb, Bomb):
                all_sprites.remove(bomb)
                bombX.clear()
                bombY.clear()
                explosion.play()
            #possibly important code: bombsLeft = -1


def bombPlacement():
    #global variable definitization
    global bombsLeft
    global bombCooldown
    global spacebarWait

    #movement script
    if not spacebarWait:
        spacebarWait = True
        if key[game.K_SPACE] and bombCooldown == 0 and bombsLeft > 0:
            bombX.append(player.rect.x)
            bombY.append(player.rect.y)
            bomb = Bomb(player.rect.x, player.rect.y, 25, 25)
            all_sprites.add(bomb)
            bombCooldown = 3
            bombsLeft -= 1
        elif bombsLeft == 0:
            for i in range(len(bombX)):
                directions = ["up", "down", "left", "right", "up_left", "up_right", "down_left", "down_right"]
                for direction in directions:
                    shard = Shard(bombX[i], bombY[i], 25, 25, direction)
                    all_sprites.add(shard)
                    shard_group.add(shard)
            for bomb in all_sprites.sprites():
                if isinstance(bomb, Bomb):
                    all_sprites.remove(bomb)
                    bombX.clear()
                    bombY.clear()
                    explosion.play()
                #possibly important code: bombsLeft = -1
    if not key[game.K_SPACE]:
        spacebarWait = False
    

def generateGridLines(startX, endX, startY, endY):
    #grid lines generation
    for i in range(startX, endX):
        game.draw.line(screen, (0, 0, 0), (i * 25+25,25),(i * 25+25,550))
    for i in range(startY, endY):
        game.draw.line(screen, (0, 0, 0), (25,i * 25+25),(550,i * 25+25))


def createHole():
    #hole initialization
    holeX = random.randint(1,21) * 25
    holeY = random.randint(1,21) * 25
    hole = Hole(holeX,holeY, 25, 25)

    #generation checks
    while game.sprite.spritecollideany(hole, target_group) or ([holeX,holeY] in targetList):
        holeX = random.randint(1,21) * 25
        holeY = random.randint(1,21) * 25
        hole.goto(holeX,holeY)
    all_sprites.add(hole)
    hole_group.add(hole)


def createDiode():
    #hole initialization
    diodeX = random.randint(1,21) * 25
    diodeY = random.randint(1,21) * 25
    diode = Diode(diodeX,diodeY, 25, 25)

    #generation checks
    while game.sprite.spritecollideany(diode, target_group) or game.sprite.spritecollideany(diode, hole_group) or ([diodeX,diodeY] in targetList):
        diodeX = random.randint(1,21) * 25
        diodeY = random.randint(1,21) * 25
        diode.goto(diodeX,diodeY)
    all_sprites.add(diode)
    diode_group.add(diode)
#--end of function init--

#--sprite init--

#Sprite Groups
all_sprites = game.sprite.Group()
title_sprites = game.sprite.Group()
wall_group = game.sprite.Group()
wall_group_title = game.sprite.Group()
shard_group = game.sprite.Group()
hole_group = game.sprite.Group()
target_group = game.sprite.Group()
diode_group = game.sprite.Group()
laser_group = game.sprite.Group()

#Dynamic Sprites
player = Player(275, 275, 25, 25)
all_sprites.add(player)
title_sprites.add(player)

#Static Sprites

#--game walls
topBorder = Wall(0,0,600,25)
all_sprites.add(topBorder)
wall_group.add(topBorder)
bottomBorder = Wall(0,550,600,50)
all_sprites.add(bottomBorder)
wall_group.add(bottomBorder)
leftBorder = Wall(0,0,25,600)
all_sprites.add(leftBorder)
wall_group.add(leftBorder)
rightBorder = Wall(550,0,25,600)
all_sprites.add(rightBorder)
wall_group.add(rightBorder)

#--title walls
topBorderTitle = Wall(200,-25,600,25)
title_sprites.add(topBorderTitle)
wall_group_title.add(topBorderTitle)
bottomBorderTitle = Wall(200,400,600,25)
title_sprites.add(bottomBorderTitle)
wall_group_title.add(bottomBorderTitle)
leftBorderTitle = Wall(175,0,25,400)
title_sprites.add(leftBorderTitle)
wall_group_title.add(leftBorderTitle)
rightBorderTitle = Wall(800,0,25,400)
title_sprites.add(rightBorderTitle)
wall_group_title.add(rightBorderTitle)

#detail init

#start detail
playButton = game.Rect(25,500,225,75)
playButtonShadow = game.Rect(28,503,228,78)
creditsButton = game.Rect(275,500,225,75)
creditsButtonShadow = game.Rect(278,503,228,78)
tutorialButton = game.Rect(525,500,225,75)
tutorialButtonShadow = game.Rect(528,503,228,78)
creditsBox = game.Rect(100,100,600,600)
creditsBoxShadow = game.Rect(95,95,610,610)
coverbox1 = game.Rect(0,0,200,600)
coverbox2 = game.Rect(200,400,600,200)
shadowBox = game.Surface((800, 600))
shadowBox.fill((0,0,0))

barW = 230
barH = 10
BarX = 25
BarY = 585

#game detail
sidePanel = game.Rect(575,0,225,600)
infoBox = game.Rect(560,400,230,190)
infoBoxShadow = game.Rect(555,395,230,190)

#tutorial detail
tutorialBox = game.Rect(560,15,230,575)
guideSquare = game.Rect(25,25,25,25)
#--end of sprite init--

#---end of game init---

#adds test targets for player use

#game loop
running = True
while running:
    for event in game.event.get():
        if event.type == game.QUIT:
            running = False
    
    #sound controls
    key = game.key.get_pressed()
    if key[game.K_m]:
        if volume:
            playTitleTheme.set_volume(0) 
            hit.set_volume(0)
            explosion.set_volume(0)
            laserSFX.set_volume(0)
            volume = False
        else:
            if display == "title":
                playTitleTheme.set_volume(1) 
            if display == "game" or display == "tutorial":
                playTitleTheme.set_volume(.25) 
            hit.set_volume(1)
            explosion.set_volume(1)
            laserSFX.set_volume(1)
            volume = True
    
    #mouse checks
    mousePos = game.mouse.get_pos()
    mouseButtons = game.mouse.get_pressed()

    #game code
    if display == "title":
        screen.fill("white")

        movement(wall_group_title)

        title_sprites.update()
        title_sprites.draw(screen)

        if atTitleStart:
            atTitleStart = False
            for i in range(10):
                createTargetsTitle()
            player.goto(400,100)

        #dev keys

        #--creates a set of new targets
        if key[game.K_k]:
            createTargetsTitle()
        
        #--deletes all existing targets
        if key[game.K_l]:
            for target in all_sprites.sprites():
                if isinstance(target, Target):
                    title_sprites.remove(target)
                    targetsLeft = 0
                    target.kill()
                    del target
                    target = None
            targetList.clear()
        
        #--summons shards at the player's current position
        if key[game.K_u]:
            explosion.play()
            directions = ["up", "down", "left", "right", "up_left", "up_right", "down_left", "down_right"]
            for direction in directions:
                shard = Shard(player.rect.x, player.rect.y, 25, 25, direction)
                title_sprites.add(shard)
                shard_group.add(shard)

        #image
        #newimage = game.transform.scale(game.image.load('images/gameplay.png'), (600, 600))
        #screen.blit(newimage,(200,0))

        #draws title screen grid lines
        for i in range(-1,32):
            game.draw.line(screen, (0, 0, 0), (i * 25,0),(i * 25,550))
        for i in range(-1,21):
            game.draw.line(screen, (0, 0, 0), (25,i * 25),(800,i * 25))

        #draws the graphics of the title screen
        game.draw.rect(screen, (56, 140, 70), coverbox1)
        game.draw.rect(screen, (56, 140, 70), coverbox2)
        game.draw.polygon(screen, (0, 0, 0), [(204, 0), (202, 398), (802, 398)])
        gfxdraw.aapolygon(screen, [(205, 0), (203, 398), (803, 398)], (0, 0, 0))
        game.draw.polygon(screen, (56, 140, 70), [(200, 0), (200, 400), (800, 400)])
        gfxdraw.aapolygon(screen, [(201, 0), (201, 400), (800, 399)], (56, 140, 70)) 
        game.draw.polygon(screen, (96, 180, 110), [(10, 105), (10, 325), (650, 325), (330, 105)])
        gfxdraw.aapolygon(screen, [(10, 105), (10, 325), (650, 325), (330, 105)], (96, 180, 110)) 
        
        #draws the title
        writeText("Epoc Bomb", "impact", 75,0,0,0,190,155)
        writeText("Epoc Bomb", "impact", 75,255,255,255,185,150)
        writeText("Game Thing", "impact", 100,0,0,0,260,265)
        writeText("Game Thing", "impact", 100,255,255,255,255,260)

        #boxes
        if playButton.collidepoint(mousePos):
            game.draw.rect(screen, (96, 180, 110), playButtonShadow, border_radius=10)
            game.draw.rect(screen, (116, 200, 130), playButton, border_radius=10)
        else:
            game.draw.rect(screen, (76, 160, 90), playButtonShadow, border_radius=10)
            game.draw.rect(screen, (96, 180, 110), playButton, border_radius=10)

        if creditsButton.collidepoint(mousePos):
            game.draw.rect(screen, (96, 180, 110), creditsButtonShadow, border_radius=10)
            game.draw.rect(screen, (116, 200, 130), creditsButton, border_radius=10)
        else:
            game.draw.rect(screen, (76, 160, 90), creditsButtonShadow, border_radius=10)
            game.draw.rect(screen, (96, 180, 110), creditsButton, border_radius=10)

        if tutorialButton.collidepoint(mousePos):
            game.draw.rect(screen, (96, 180, 110), tutorialButtonShadow, border_radius=10)
            game.draw.rect(screen, (116, 200, 130), tutorialButton, border_radius=10)
        else:
            game.draw.rect(screen, (76, 160, 90), tutorialButtonShadow, border_radius=10)
            game.draw.rect(screen, (96, 180, 110), tutorialButton, border_radius=10)

        #draws button text
        writeText("Play: B", "impact", 50,0,0,0,140,540)
        writeText("Play: B", "impact", 50,255,255,255,137,537)
        writeText("Credits: C", "impact", 50,0,0,0,390,540)
        writeText("Credits: C", "impact", 50,255,255,255,387,537)
        writeText("Tutorial: T", "impact", 50,0,0,0,640,540)
        writeText("Tutorial: T", "impact", 50,255,255,255,637,537)

        #changes button index
        if not navigationButtonPressed:
            navigationButtonPressed = True
            if key[game.K_q]:
                if buttonIndex > 1:
                    buttonIndex -= 1
                else:
                    buttonIndex = 3
            if key[game.K_e]:
                if buttonIndex < 3:
                    buttonIndex += 1
                else:
                    buttonIndex = 1
        
        if not key[game.K_q] and not key[game.K_e]:
            navigationButtonPressed = False

        if buttonIndex == 1:
            BarX = 25
        elif buttonIndex == 2:
            BarX = 275
        elif buttonIndex == 3:
            BarX = 525
        
        game.draw.rect(screen, (255, 255, 255), (BarX, BarY, barW, barH), border_radius=10)

        if key[game.K_c] or (key[game.K_RETURN] and buttonIndex == 2) or (creditsButton.collidepoint(mousePos) and mouseButtons[0]):
            playTitleTheme.set_volume(.25)
            rect_surface = game.Surface((800, 600), game.SRCALPHA)
            rect_surface.fill((0, 0, 0, 128))
            screen.blit(rect_surface, (0, 0))
            game.draw.rect(screen, (76, 160, 90), creditsBoxShadow, border_radius=50)
            game.draw.rect(screen, (96, 180, 110), creditsBox, border_radius=50)
            writeText("Credits", "impact", 50,0,0,0,405,155)
            writeText("Credits", "impact", 50,255,255,255,400,150)
            writeText("Created by @Turtlerock0010", "Arial",30,255,255,255,400,225)
            writeText("Inspired by Build A Boat", "Arial",30,255,255,255,400,260)
            writeText("Epoc Bomb Game Thing, A", "Arial",30,255,255,255,400,335)
            writeText("Continuation of Epic Bomb", "Arial",30,255,255,255,400,370)
            writeText("Game On Scratch", "Arial",30,255,255,255,400,405)
            writeText("Hint: Did you know you can", "Arial",30,255,255,255,400,450+50)
            writeText("mess around in the title?", "Arial",30,255,255,255,400,475+50)
            writeText("Use WASD, U and K", "Arial",30,255,255,255,400,500+50)
        
        if shadowBoxStart:
            shadowBoxAlpha -= 10
            shadowBox.set_alpha(shadowBoxAlpha)
            screen.blit(shadowBox, (0, 0))
        if shadowBoxAlpha < 0:
            shadowBoxStart = False
        
        if not (key[game.K_c] or (key[game.K_RETURN] and buttonIndex == 2 or (creditsButton.collidepoint(mousePos) and mouseButtons[0]))):
            playTitleTheme.set_volume(1)
        
        if key[game.K_t] or (key[game.K_RETURN] and buttonIndex == 3) or (tutorialButton.collidepoint(mousePos) and mouseButtons[0]):
                    display = "tutorial"
                    playTitleTheme.set_volume(.25)
                    player.goto(275,275)
                    targetsLeft = 0
                    for target in title_sprites.sprites():
                        if isinstance(target, Target):
                            title_sprites.remove(target)
                            targetsLeft = 0
                            target.kill()
                            del target
                            target = None
                    targetList.clear()
                    shard_group.empty()

        if key[game.K_b] or (key[game.K_RETURN] and buttonIndex == 1 or (playButton.collidepoint(mousePos) and mouseButtons[0])):
            display = "game"
            playTitleTheme.set_volume(.25)
            player.goto(275,275)
            targetsLeft = 0
            for target in title_sprites.sprites():
                if isinstance(target, Target):
                    title_sprites.remove(target)
                    targetsLeft = 0
                    target.kill()
                    del target
                    target = None
            targetList.clear()
            shard_group.empty()

    
    if display == "tutorial":
        screen.fill("white")
        #--detail draw--

        #grid lines
        generateGridLines(0,21,0,21)

        #functional components
        all_sprites.update()
        all_sprites.draw(screen)

        #boxes
        game.draw.rect(screen, (56, 140, 70), sidePanel)
        game.draw.rect(screen, (96, 180, 110), tutorialBox, border_radius=10)
        game.draw.rect(screen, (239, 245, 66), guideSquare)



        #--End of Detail Draw--

        movement(wall_group)

        if bombCooldown > 0:
            bombCooldown -= 1

        #check shards
        shardsLeft = len([s for s in shard_group if isinstance(s, Shard)])

        if tutorialOnce:
            tutorialOnce = False
            guideSquare.left = random.randint(1,21) * 25
            guideSquare.top = random.randint(1,21) * 25
            shard_group.empty()
            if tutorialStage == 1:
                bombsLeft = 1
            if tutorialStage == 2:
                bombsLeft = 5
            if tutorialStage == 3:
                tutorialLoad = True
            if tutorialStage == 4:
                bombsLeft = 2
                createTargets()
                createTargets()
        
        if tutorialLoad:
            if tutorialStage == 3:
                bombsLeft = 1
                createTargets()
            if tutorialStage == 4:
                bombsLeft = 2
                createTargets()
                createTargets()
            tutorialLoad = False

        #tutorial system
        if tutorialStage <= 5:
            if tutorialStage == 0:
                writeText("Welcome To Epoc Bomb", "Arial", 20,255,255,255,675,30)
                writeText("Game Thing!", "Arial", 20,255,255,255,675,60)
                writeText("This is the tutorial for this", "Arial", 20,255,255,255,675,90)
                writeText("project. Start by going to", "Arial", 20,255,255,255,675,120) 
                writeText("the yellow guide square.", "Arial", 20,255,255,255,675,150)

            if tutorialStage == 1:
                writeText("First of all, lets talk about", "Arial", 20,255,255,255,675,30)
                writeText("Bombs and Shards.", "Arial", 20,255,255,255,675,60)
                writeText("Bombs are the way you", "Arial", 20,255,255,255,675,90)
                writeText("release shards. There are", "Arial", 20,255,255,255,675,120)
                writeText("8 shards per bomb which", "Arial", 20,255,255,255,675,150)
                writeText("move away from the", "Arial", 20,255,255,255,675,180)
                writeText("bomb(s) from the top,", "Arial", 20,255,255,255,675,210)
                writeText("bottom, left, right, top-left,", "Arial", 20,255,255,255,675,240)
                writeText("top-right, bottom-left,", "Arial", 20,255,255,255,675,270)
                writeText("and bottom-right.", "Arial", 20,255,255,255,675,300)
                writeText("To move on use the", "Arial", 20,255,255,255,675,360)
                writeText("[SPACE] key to place", "Arial", 20,255,255,255,675,390)
                writeText("one Bomb.", "Arial", 20,255,255,255,675,420)
                bombPlacement()

            if tutorialStage == 2:
                writeText("In some rounds there are", "Arial", 20,255,255,255,675,30)
                writeText("multiple bombs. The", "Arial", 20,255,255,255,675,60)
                writeText("bombs only explode once", "Arial", 20,255,255,255,675,90)
                writeText("you have placed ALL", "Arial", 20,255,255,255,675,120)
                writeText("bombs.", "Arial", 20,255,255,255,675,150)
                writeText("To move on use the", "Arial", 20,255,255,255,675,210)
                writeText("[SPACE] key to place", "Arial", 20,255,255,255,675,240)
                writeText("five bombs.", "Arial", 20,255,255,255,675,270)
                bombPlacement()

            if tutorialStage == 3:
                writeText("Now lets move on to", "Arial", 20,255,255,255,675,30)
                writeText("Targets. Targets are", "Arial", 20,255,255,255,675,60)
                writeText("well, targets that you", "Arial", 20,255,255,255,675,90)
                writeText("have to hit with the", "Arial", 20,255,255,255,675,120)
                writeText("shards from the bomb.", "Arial", 20,255,255,255,675,150)
                writeText("There are always 8", "Arial", 20,255,255,255,675,180)
                writeText("targets per bomb given", "Arial", 20,255,255,255,675,210)
                writeText("so you won't be given", "Arial", 20,255,255,255,675,240)
                writeText("any impossible rounds.", "Arial", 20,255,255,255,675,270)
                writeText("To move on hit all", "Arial", 20,255,255,255,675,330)
                writeText("targets shown on the", "Arial", 20,255,255,255,675,360)
                writeText("grid.", "Arial", 20,255,255,255,675,390)

                bombPlacement()

                if shardsLeft == 8:
                    shardsLoaded = True

                if targetsLeft == 0:
                    tutorial3pass = True
                    shardsLoaded = False
                
                if shardsLoaded and shardsLeft == 0:
                    shardsLoaded = False
                    for target in all_sprites.sprites():
                        if isinstance(target, Target):
                            all_sprites.remove(target)
                            targetsLeft = 0
                            target.kill()
                            del target
                            target = None
                    targetList.clear()
                    shardsLoaded = False
                    tutorialLoad = True
                
            if tutorialStage == 4:
                writeText("Like bombs there are", "Arial", 20,255,255,255,675,30)
                writeText("multiple targets on", "Arial", 20,255,255,255,675,60)
                writeText("the map.", "Arial", 20,255,255,255,675,90)
                writeText("To move on, hit all", "Arial", 20,255,255,255,675,150)
                writeText("targets on the map.", "Arial", 20,255,255,255,675,180)

                bombPlacement()
                
                if shardsLeft == 16:
                    shardsLoaded = True

                if targetsLeft == 0:
                    tutorial3pass = True
                    shardsLoaded = False
                
                if shardsLoaded and shardsLeft == 0:
                    shardsLoaded = False
                    for target in all_sprites.sprites():
                        if isinstance(target, Target):
                            all_sprites.remove(target)
                            targetsLeft = 0
                            target.kill()
                            del target
                            target = None
                    targetList.clear()
                    shardsLoaded = False
                    tutorialLoad = True
            if tutorialStage == 5:
                writeText("Now you are ready!", "Arial", 20,255,255,255,675,30)
                writeText("press space to", "Arial", 20,255,255,255,675,60)
                writeText("go back!", "Arial", 20,255,255,255,675,90)
                if key[game.K_SPACE]:
                    display = "title"
                    atTitleStart = True
                

        if player.rect.x == guideSquare.left and player.rect.y == guideSquare.top:
            if tutorialStage == 0:
                tutorialStage += 1
                tutorialOnce = True
            if tutorialStage == 1 and bombsLeft == 0:
                tutorialStage += 1
                tutorialOnce = True
                bombsLeft = -1
                shard_group.empty()
            if tutorialStage == 2 and bombsLeft == 0:
                tutorialStage += 1
                tutorialOnce = True
                bombsLeft = -1
                shard_group.empty()
            if tutorialStage == 3 and tutorial3pass:
                tutorialStage += 1
                tutorialOnce = True
                bombsLeft = -1
                shard_group.empty()
                tutorial3pass = False
            if tutorialStage == 4 and tutorial3pass:
                tutorialStage += 1
                tutorialOnce = True
                bombsLeft = -1
                shard_group.empty()
            if tutorialStage == 5:
                pass
            



    if display == "game":
        screen.fill("white")
        #--detail draw--

        #grid lines
        generateGridLines(0,21,0,21)

        #functional components
        all_sprites.update()
        all_sprites.draw(screen)

        #boxes
        game.draw.rect(screen, (56, 140, 70), sidePanel)
        game.draw.rect(screen, (36, 120, 50), infoBoxShadow, border_radius=10)
        game.draw.rect(screen, (96, 180, 110), infoBox, border_radius=10)

        #info box text
        writeText("SCORE: " + str(score), "Arial Black", 25,0,0,0,672,427)
        writeText("SCORE: " + str(score), "Arial Black", 25,255,255,255,670,425)
        writeText("TARGETS: " + str(targetsLeft), "Arial Black", 25,0,0,0,672,472)
        writeText("TARGETS: " + str(targetsLeft), "Arial Black", 25,255,255,255,670,470)
        writeText("ROUND: " + str(round), "Arial Black", 25,0,0,0,672,517)
        writeText("ROUND: " + str(round), "Arial Black", 25,255,255,255,670,515)
        writeText("BOMBS: " + str(bombsLeft), "Arial Black", 25,0,0,0,672,562)
        writeText("BOMBS: " + str(bombsLeft), "Arial Black", 25,255,255,255,670,560)

        #logo image
        newimage = game.transform.smoothscale(game.image.load('images/oldicon1.png'), (150, 150))
        screen.blit(newimage,(600,25))

        #logo text
        writeText("Epoc Bomb", "impact", 40,0,0,0,678,203)
        writeText("Epoc Bomb", "impact", 40,255,255,255,675,200)
        writeText("Game Thing", "impact", 40,0,0,0,678,248)
        writeText("Game Thing", "impact", 40,255,255,255,675,245)

        #--End of Detail Draw--

        #player actions
        movement(wall_group)
        bombPlacement()
        #dev keys
        if key[game.K_k]:
            createTargets()
        if key[game.K_l]:
            for target in all_sprites.sprites():
                if isinstance(target, Target):
                    all_sprites.remove(target)
                    targetsLeft = 0
                    target.kill()
                    del target
                    target = None
            targetList.clear()

        if key[game.K_u]:
            explosion.play()
            directions = ["up", "down", "left", "right", "up_left", "up_right", "down_left", "down_right"]
            for direction in directions:
                shard = Shard(player.rect.x, player.rect.y, 25, 25, direction)
                all_sprites.add(shard)
                shard_group.add(shard)
        
        if key[game.K_o]:
            for diode in diode_group.sprites():
                if isinstance(diode, Diode):
                    diode.makeLasers()
        if key[game.K_p]:
            for diode in diode_group.sprites():
                if isinstance(diode, Diode):
                    diode.destroyLasers()

        laserTimer += 1
        if not laserOn and laserTimer == 180:
            laserOn = True
            laserTimer = 0.0
            for diode in diode_group.sprites():
                if isinstance(diode, Diode):
                    diode.makeLasers()
        
        if laserOn and laserTimer == 180:
            laserOn = False
            laserTimer = 0.0
            for diode in diode_group.sprites():
                if isinstance(diode, Diode):
                    diode.destroyLasers()
        


        if bombCooldown > 0:
            bombCooldown -= 1


        #check shards
        shardsLeft = len([s for s in shard_group if isinstance(s, Shard)])

        #round system
        if round > maxRounds:
            pass
        else:
            if not roundStarted:
                touchedByLaser = False
                laserTimer = 0.0
                for hole in all_sprites.sprites():
                    if isinstance(hole, Hole):
                        all_sprites.remove(hole)
                        hole.kill()
                        del hole
                for diode in diode_group.sprites():
                    if isinstance(diode, Diode):
                        diode.destroyLasers()
                        all_sprites.remove(diode)
                        diode_group.remove(diode)
                        diode.kill()
                        del diode
                        diode = None
                roundStarted = True
                if round < 4:
                    createTargets()
                    bombsLeft = 1
                elif round < 7:
                    createTargets()
                    createTargets()
                    bombsLeft = 2
                elif round < 10:
                    createTargets()
                    createTargets()
                    createTargets()
                    bombsLeft = 3
                elif round < 13:
                    createTargets()
                    bombsLeft = 1
                    for i in range(10):
                        createHole()
                elif round < 16:
                    createTargets()
                    createTargets()
                    for i in range(20):
                        createHole()
                    bombsLeft = 2
                elif round < 19:
                    createTargets()
                    createTargets()
                    createTargets()
                    for i in range(30):
                        createHole()
                    bombsLeft = 3
                elif round < 22:
                    createTargets()
                    bombsLeft = 1
                    createDiode()
                elif round < 25:
                    createTargets()
                    createTargets()
                    bombsLeft = 2
                    for i in range(3):
                        createDiode()
                elif round < 28:
                    createTargets()
                    createTargets()
                    createTargets()
                    bombsLeft = 3
                    for i in range(5):
                        createDiode()
                elif round < 31:
                    createTargets()
                    bombsLeft = 1
                    createDiode()
                    for i in range(10):
                        createHole()
                elif round < 34:
                    createTargets()
                    createTargets()
                    bombsLeft = 2
                    for i in range(3):
                        createDiode()
                    for i in range(30):
                        createHole()
                elif round < 37:
                    createTargets()
                    createTargets()
                    createTargets()
                    bombsLeft = 3
                    for i in range(5):
                        createDiode()
                    for i in range(50):
                        createHole()

            if round < 4:
                if shardsLeft == 8:
                    shardsLoaded = True
            elif round < 7:
                if shardsLeft == 16:
                    shardsLoaded = True
            elif round < 10:
                if shardsLeft == 24:
                    shardsLoaded = True
            elif round < 13:
                if shardsLeft == 8:
                    shardsLoaded = True
            elif round < 16:
                if shardsLeft == 16:
                    shardsLoaded = True
            elif round < 19:
                if shardsLeft == 24:
                    shardsLoaded = True
            elif round < 22:
                if shardsLeft == 8:
                    shardsLoaded = True
            elif round < 25:
                if shardsLeft == 16:
                    shardsLoaded = True
            elif round < 28:
                if shardsLeft == 24:
                    shardsLoaded = True
            elif round < 31:
                if shardsLeft == 8:
                    shardsLoaded = True
            elif round < 34:
                if shardsLeft == 16:
                    shardsLoaded = True
            elif round < 37:
                if shardsLeft == 24:
                    shardsLoaded = True
    
            if targetsLeft == 0:
                if shardsLeft == 0:
                    round += 1
                    roundStarted = False
                    shardsLoaded = False
            
            if shardsLoaded and shardsLeft == 0:
                shardsLoaded = False
                for target in all_sprites.sprites():
                    if isinstance(target, Target):
                        all_sprites.remove(target)
                        targetsLeft = 0
                        target.kill()
                        del target
                        target = None
                
                targetList.clear()
                roundStarted = False
                shardsLoaded = False

    #time.sleep(0.08333)
    dt = clock.tick(60) / 1000.0
    game.display.update()
game.quit()