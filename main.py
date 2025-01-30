# Epoc Bomb Game Thing
# Version 0.001
# Developed by Turtlerock Industries led by @Commandline

#sys init
import pygame as game
import time
import random
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

#music init
game.mixer.init()
playTheme = game.mixer.Sound("sounds/theme.mp3")
playTitleTheme = game.mixer.Sound("sounds/titletheme.mp3")
hit = game.mixer.Sound("sounds/hit.wav")
playTitleTheme.play(-1)

#var init
bombCooldown = 0
bombs = 3
bombsLeft = 3
bombX = []
bombY = []
score = 0
volume = True
targetsLeft = 0
round = 1
maxRounds = 9
roundStarted = False
shardsLeft = -1
shardsLoaded = False
display = "title"
titlethemeon = True
buttonIndex = 1

#--class init--
class Player(game.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = game.Surface([width, height])
        self.image.fill((148, 3, 252))  # Purple color (RGB)
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
        self.image.fill((0, 0, 255))  # Purple color (RGB)
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

class Target(game.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = game.Surface([width, height])
        self.image.fill((255, 0, 0))  # Red color (RGB)
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
        self.image.fill((249, 147, 5))  # Orange color (RGB)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = direction  # Stores direction (up, down, left, right, etc.)
        self.speed = 25  # Adjust shard speed here

    def update(self):
        # Update movement based on direction
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
        # Add checks for walls or other objects to stop the shard movement
        if display == "game":
            if game.sprite.spritecollideany(self, wall_group):
                self.kill()
        if display == "title":
            if game.sprite.spritecollideany(self, wall_group_title):
                self.kill()

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

    #top target
    targets = Target(randomSquare[0], randomSquare[1], 25, 25)
    all_sprites.add(targets)
    for i in range(random.randint(1,20)):
        targets.move(0,-25)
        if game.sprite.collide_rect(targets, topBorder):
            targets.move(0,25)
    
    #bottom target
    targets = Target(randomSquare[0], randomSquare[1], 25, 25)
    all_sprites.add(targets)
    for i in range(random.randint(1,20)):
        targets.move(0,25)
        if game.sprite.collide_rect(targets, bottomBorder):
            targets.move(0,-25)
    
    #left target
    targets = Target(randomSquare[0], randomSquare[1], 25, 25)
    all_sprites.add(targets)
    for i in range(random.randint(1,20)):
        targets.move(-25, 0)
        if game.sprite.collide_rect(targets, leftBorder):
            targets.move(25, 0)
    
    #right target
    targets = Target(randomSquare[0], randomSquare[1], 25, 25)
    all_sprites.add(targets)
    for i in range(random.randint(1,20)):
        targets.move(25, 0)
        if game.sprite.collide_rect(targets, rightBorder):
            targets.move(-25, 0)
    
    #top-left target
    targets = Target(randomSquare[0], randomSquare[1], 25, 25)
    all_sprites.add(targets)
    for i in range(random.randint(1,20)):
        targets.move(0, -25)
        targets.move(-25, 0)
        if game.sprite.collide_rect(targets, topBorder) or game.sprite.collide_rect(targets, leftBorder):
            targets.move(0, 25)
            targets.move(25, 0)
    
    #top-right target
    targets = Target(randomSquare[0], randomSquare[1], 25, 25)
    all_sprites.add(targets)
    for i in range(random.randint(1,20)):
        targets.move(0, -25)
        targets.move(25, 0)
        if game.sprite.collide_rect(targets, topBorder) or game.sprite.collide_rect(targets, rightBorder):
            targets.move(0, 25)
            targets.move(-25, 0)
    
    #bottom-left target
    targets = Target(randomSquare[0], randomSquare[1], 25, 25)
    all_sprites.add(targets)
    for i in range(random.randint(1,20)):
        targets.move(0, 25)
        targets.move(-25, 0)
        if game.sprite.collide_rect(targets, bottomBorder) or game.sprite.collide_rect(targets, leftBorder):
            targets.move(0, -25)
            targets.move(25, 0)
    
    #bottom-right target
    targets = Target(randomSquare[0], randomSquare[1], 25, 25)
    all_sprites.add(targets)
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
#--end of function init--

#--sprite init--
all_sprites = game.sprite.Group()
title_sprites = game.sprite.Group()
wall_group = game.sprite.Group()
wall_group_title = game.sprite.Group()
shard_group = game.sprite.Group()
#Dynamic Sprites
player = Player(275, 275, 25, 25)
all_sprites.add(player)
title_sprites.add(player)

#Static Sprites
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

barW = 230
barH = 10
BarX = 25
BarY = 585

#game detail
sidePanel = game.Rect(575,0,225,600)
infoBox = game.Rect(560,400,230,190)
#--end of sprite init--

#---end of game init---

for i in range(10):
    createTargetsTitle()

#game loop
player.goto(400,100)
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
                volume = False
            else:
                if display == "title":
                    playTitleTheme.set_volume(1) 
                if display == "game":
                    playTitleTheme.set_volume(.25) 
                hit.set_volume(1)
                volume = True
      
    #game code
    if display == "title":
        screen.fill("white")

        key = game.key.get_pressed()
        if key[game.K_a] or key[game.K_LEFT]:
            player.move(-25,0)
            if game.sprite.collide_rect(player, leftBorderTitle):
                player.move(25,0)
        if key[game.K_d] or key[game.K_RIGHT]:
            player.move(25,0)
            if game.sprite.collide_rect(player, rightBorderTitle):
                player.move(-25,0)
        if key[game.K_s] or key[game.K_DOWN]:
            player.move(0,25)
            if game.sprite.collide_rect(player, bottomBorderTitle):
                player.move(0,-25)
        if key[game.K_w] or key[game.K_UP]:
            player.move(0,-25)
            if game.sprite.collide_rect(player, topBorderTitle):
                player.move(0,25)
        title_sprites.update()
        title_sprites.draw(screen)

        if key[game.K_k]:
            createTargetsTitle()
        if key[game.K_l]:
            for target in all_sprites.sprites():
                if isinstance(target, Target):
                    title_sprites.remove(target)
                    targetsLeft = 0
        

        if key[game.K_u]:
            directions = ["up", "down", "left", "right", "up_left", "up_right", "down_left", "down_right"]
            for direction in directions:
                shard = Shard(player.rect.x, player.rect.y, 25, 25, direction)
                title_sprites.add(shard)
                shard_group.add(shard)

        #image
        #newimage = game.transform.scale(game.image.load('images/gameplay.png'), (600, 600))
        #screen.blit(newimage,(200,0))

        for i in range(-1,32):
            game.draw.line(screen, (0, 0, 0), (i * 25,0),(i * 25,550))
        for i in range(-1,21):
            game.draw.line(screen, (0, 0, 0), (25,i * 25),(800,i * 25))

        game.draw.rect(screen, (56, 140, 70), coverbox1)
        game.draw.rect(screen, (56, 140, 70), coverbox2)
        game.draw.polygon(screen, (0, 0, 0), [(204, 0), (202, 398), (802, 398)])
        game.draw.polygon(screen, (56, 140, 70), [(200, 0), (200, 400), (800, 400)])
        game.draw.polygon(screen, (96, 180, 110), [(10, 105), (10, 325), (650, 325), (330, 105)])
        
        writeText("Epoc Bomb", "impact", 75,0,0,0,190,155)
        writeText("Epoc Bomb", "impact", 75,255,255,255,185,150)
        writeText("Game Thing", "impact", 100,0,0,0,260,265)
        writeText("Game Thing", "impact", 100,255,255,255,255,260)

        #boxes
        game.draw.rect(screen, (76, 160, 90), playButtonShadow, border_radius=10)
        game.draw.rect(screen, (96, 180, 110), playButton, border_radius=10)
        game.draw.rect(screen, (76, 160, 90), creditsButtonShadow, border_radius=10)
        game.draw.rect(screen, (96, 180, 110), creditsButton, border_radius=10)
        game.draw.rect(screen, (76, 160, 90), tutorialButtonShadow, border_radius=10)
        game.draw.rect(screen, (96, 180, 110), tutorialButton, border_radius=10)

        writeText("Play: B", "impact", 50,0,0,0,140,540)
        writeText("Play: B", "impact", 50,255,255,255,137,537)
        writeText("Credits: C", "impact", 50,0,0,0,390,540)
        writeText("Credits: C", "impact", 50,255,255,255,387,537)
        writeText("Tutorial: T", "impact", 50,0,0,0,640,540)
        writeText("Tutorial: T", "impact", 50,255,255,255,637,537)

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

        if buttonIndex == 1:
            BarX = 25
        elif buttonIndex == 2:
            BarX = 275
        elif buttonIndex == 3:
            BarX = 525
        game.draw.rect(screen, (255, 255, 255), (BarX, BarY, barW, barH), border_radius=10)

        if key[game.K_c] or (key[game.K_RETURN] and buttonIndex == 2):
            playTitleTheme.set_volume(.25)
            rect_surface = game.Surface((800, 600), game.SRCALPHA)
            rect_surface.fill((0, 0, 0, 128))
            screen.blit(rect_surface, (0, 0))
            game.draw.rect(screen, (76, 160, 90), creditsBoxShadow, border_radius=50)
            game.draw.rect(screen, (96, 180, 110), creditsBox, border_radius=50)
            writeText("Credits", "impact", 50,0,0,0,405,155)
            writeText("Credits", "impact", 50,255,255,255,400,150)
            writeText("Created by @Turtlerock0010", "Arial",30,255,255,255,400,175+50)
            writeText("Inspired by Build A Boat", "Arial",30,255,255,255,400,225+50)
            writeText("Epoc Bomb Game Thing, A", "Arial",30,255,255,255,400,300+50)
            writeText("Continuation of Epic Bomb", "Arial",30,255,255,255,400,350+50)
            writeText("Game On Scratch", "Arial",30,255,255,255,400,400+50)
            writeText("Hint: Did you know you can", "Arial",30,255,255,255,400,450+50)
            writeText("mess around in the title?", "Arial",30,255,255,255,400,475+50)
            writeText("Use WASD, U and K", "Arial",30,255,255,255,400,500+50)
        if not (key[game.K_c] or (key[game.K_RETURN] and buttonIndex == 2)):
            playTitleTheme.set_volume(1)
        
        if key[game.K_b] or (key[game.K_RETURN] and buttonIndex == 1):
            display = "game"
            playTitleTheme.set_volume(.25)
            player.goto(275,275)
            targetsLeft = 0
            for target in title_sprites.sprites():
                if isinstance(target, Target):
                    title_sprites.remove(target)
                    targetsLeft = 0
            shard_group.empty()


    if display == "game":
        screen.fill("white")
        #--detail draw--

        #grid lines
        for i in range(21):
            game.draw.line(screen, (0, 0, 0), (i * 25+25,25),(i * 25+25,550))
        for i in range(21):
            game.draw.line(screen, (0, 0, 0), (25,i * 25+25),(550,i * 25+25))

        #functional components
        all_sprites.update()
        all_sprites.draw(screen)

        #boxes
        game.draw.rect(screen, (56, 140, 70), sidePanel)
        game.draw.rect(screen, (96, 180, 110), infoBox, border_radius=10)

        
        #info box text
        writeText("Score: " + str(score), "Arial", 30,255,255,255,650,425)
        writeText("Targets: " + str(targetsLeft), "Arial", 30,255,255,255,650,470)
        writeText("Round: " + str(round), "Arial", 30,255,255,255,650,515)
        writeText("Bombs: " + str(bombsLeft), "Arial", 30,255,255,255,650,560)

        #logo image
        newimage = game.transform.scale(game.image.load('images/icon.png'), (150, 150))
        screen.blit(newimage,(600,25))

        #logo text
        writeText("Epoc Bomb", "impact", 40,0,0,0,678,203)
        writeText("Epoc Bomb", "impact", 40,255,255,255,675,200)
        writeText("Game Thing", "impact", 40,0,0,0,678,248)
        writeText("Game Thing", "impact", 40,255,255,255,675,245)

        #--End of Detail Draw--

        #player actions
        key = game.key.get_pressed()
        if key[game.K_a] or key[game.K_LEFT]:
            player.move(-25,0)
            if game.sprite.collide_rect(player, leftBorder):
                player.move(25,0)
        if key[game.K_d] or key[game.K_RIGHT]:
            player.move(25,0)
            if game.sprite.collide_rect(player, rightBorder):
                player.move(-25,0)
        if key[game.K_s] or key[game.K_DOWN]:
            player.move(0,25)
            if game.sprite.collide_rect(player, bottomBorder):
                player.move(0,-25)
        if key[game.K_w] or key[game.K_UP]:
            player.move(0,-25)
            if game.sprite.collide_rect(player, topBorder):
                player.move(0,25)
        
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
            #possibly important code: bombsLeft = -1

        if bombCooldown > 0:
            bombCooldown -= 1

        #dev keys
        if key[game.K_k]:
            createTargets()
        if key[game.K_l]:
            for target in all_sprites.sprites():
                if isinstance(target, Target):
                    all_sprites.remove(target)
                    targetsLeft = 0

        if key[game.K_u]:
            directions = ["up", "down", "left", "right", "up_left", "up_right", "down_left", "down_right"]
            for direction in directions:
                shard = Shard(player.rect.x, player.rect.y, 25, 25, direction)
                all_sprites.add(shard)
                shard_group.add(shard)

        #check shards
        shardsLeft = len([s for s in shard_group if isinstance(s, Shard)])

        #round system
        if round > maxRounds:
            pass
        else:
            if not roundStarted:
                roundStarted = True
                if round < 4:
                    createTargets()
                    bombsLeft = 1
                elif round < 7:
                    createTargets()
                    createTargets()
                    bombsLeft = 2
                else:
                    createTargets()
                    createTargets()
                    createTargets()
                    bombsLeft = 3

            if round < 4:
                if shardsLeft == 8:
                    shardsLoaded = True
            elif round < 7:
                if shardsLeft == 16:
                    shardsLoaded = True
            else:
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
                roundStarted = False
                shardsLoaded = False

    time.sleep(0.08333)
    game.display.update()
game.quit()