# Epoc Bomb Game Thing
# Version 0.001
# Developed by Turtlerock Industries led by @Commandline

#sys init
import pygame as game
import time
import random
from pygame import mixer

game.init()

#display init
screen = game.display.set_mode((800,600))
game.display.set_caption("Epoc Bomb Game Thing")

#icon init
icon_image = game.image.load("icon.png")
game.display.set_icon(icon_image)


#----game init----

#music init
game.mixer.init()
sound = game.mixer.Sound("sounds/theme.mp3")
hit = game.mixer.Sound("sounds/hit.wav")
sound.play(-1)

#var init
bombCooldown = 0
bombs = 3
bombsLeft = 3
bombX = []
bombY = []
score = 0
volume = True
targetsLeft = 0

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
        if game.sprite.spritecollideany(self, wall_group):
            self.kill()

class Wall(game.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = game.Surface([width, height])
        self.image.fill((92, 92, 92))  # Gray color (RGB)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        # No automatic movement, position is updated manually
        pass

    #there is no need to update position to a wall
#--end of class init--

#--function init--
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

def writeText(input, textfont, R, G, B, X, Y):
    font = game.font.SysFont(textfont, 30)
    textwrite = font.render(input, True, (R, G, B))
    textRectwrite = textwrite.get_rect()
    textRectwrite.center = (X, Y)
    screen.blit(textwrite, textRectwrite)
#--end of function init--

#--sprite init--
all_sprites = game.sprite.Group()
wall_group = game.sprite.Group()
shard_group = game.sprite.Group()
#Dynamic Sprites
player = Player(275, 275, 25, 25)
all_sprites.add(player)

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

#detail init
sidePanel = game.Rect(575,0,225,600)
infoBox = game.Rect(560,400,230,190)
#--end of sprite init--

#---end of game init---

#game loop
running = True
mainloop = False
while running:
    for event in game.event.get():
        if event.type == game.QUIT:
            running = False
    
    #sound controls
    if key[game.K_m]:
            if volume:
                sound.set_volume(0) 
                hit.set_volume(0)
                volume = False
            else:
                sound.set_volume(1) 
                hit.set_volume(1)
                volume = True
      
    #game code
    screen.fill("white")
    if mainloop == False:
        key = game.key.get_pressed()
        if key[game.K_b]:
            mainloop = True
        
        #text
        writeText("Press B To Begin", "Arial",0,0,0,400,550)
        writeText("Epoc Bomb Game Thing", "Arial",0,0,0,400,450)

        #image
        newimage = game.transform.scale(game.image.load('icon.png'), (300, 300))
        screen.blit(newimage,(250,100))
            

    if mainloop:
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
        game.draw.rect(screen, (92, 92, 92), sidePanel)
        game.draw.rect(screen, (70, 70, 70), infoBox)
        
        #info box text
        writeText("Score: " + str(score), "Arial",255,255,255,650,425)
        writeText("Targets: " + str(targetsLeft), "Arial",255,255,255,650,470)
        writeText("Round: " + "[null]", "Arial",255,255,255,650,515)

        #logo image
        newimage = game.transform.scale(game.image.load('icon.png'), (150, 150))
        screen.blit(newimage,(600,50))

        #logo text
        writeText("Epoc Bomb", "Arial",200,200,200,675,250)
        writeText("Game Thing", "Arial",200,200,200,675,300)

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
            bombsLeft = -1

        if bombCooldown > 0:
            bombCooldown -= 1

        #dev keys
        if key[game.K_k]:
            createTargets()
        if key[game.K_l]:
            for target in all_sprites.sprites():
                if isinstance(target, Target):
                    all_sprites.remove(target)

        if key[game.K_u]:
            directions = ["up", "down", "left", "right", "up_left", "up_right", "down_left", "down_right"]
            for direction in directions:
                shard = Shard(player.rect.x, player.rect.y, 25, 25, direction)
                all_sprites.add(shard)
                shard_group.add(shard)

        #checks for remaining shards
        shardLeft = len([s for s in shard_group if isinstance(s, Shard)])
        print(shardLeft)

    time.sleep(0.08333)
    game.display.update()
game.quit()