#! /usr/bin/python
# Filename: game.py
###########################
# The Feeble Player
#   By T. Nelson Downs
#
# Music: Kevin MacLeod
###########################

# Import modules and raise an error if it can't
try:
    from sys import exit
    import pygame
    import time
    from levels import *
    import random
    from pygame.locals import *
    import vector2
    import os
    
except:
    print("Can't load module.")
    exit()

class Levels:

    def __init__(self, levelNum):
        global player
        global lavas
        global walls
        global disappears
        global keys
        global badGuys1
        global badGuys2
        global power
        global sensitives
        global world
        global moveables
        global health
        global next_levels
        global previous_levels
        global levelSelects
        levelSelects = []
        lavas = []
        sensitives = []
        disappears = []
        moveables = []
        badGuys1 = []
        badGuys2 = []
        walls = []
        power = []
        health = []
        next_levels = []
        previous_levels = []
        self.levelNum = levelNum
        if self.levelNum == "level1_1":
            world.background = pygame.image.load("data/background3.jpg").convert()
        if self.levelNum == "levelSelect":
            world.background = pygame.image.load("data/backgroundLevelSelect.jpg").convert()
# Reset the world
        world.background_x = 0 # Background Scrolling
        world.background_y = 0
        
        self.x = 0
        self.y = 0
        for line in self.levelNum.split("\n"):
            for char in line:
                if char == "+":
                    walls.append(GameObject(world, 'block', 'brick.png', (self.x, self.y), 0))
                if char == "*":
                    walls.append(GameObject(world, 'block1', 'brick0.png', (self.x, self.y), 0))
                if char == "-":
                    walls.append(GameObject(world, 'block21', 'brick21.png', (self.x, self.y), 0))
                if char == "^":
                    walls.append(GameObject(world, 'block3', 'brick3.png', (self.x, self.y), 0))
                if char == "=":
                    walls.append(GameObject(world, 'block2', 'brick2.png', (self.x, self.y), 0))
                if char == "[":
                    walls.append(GameObject(world, 'block4', 'brick4.png', (self.x, self.y), 0))
                if char == "]":
                    walls.append(GameObject(world, 'block5', 'brick5.png', (self.x, self.y), 0))
                if char == "{":
                    disappears.append(GameObject(world, 'block5', 'locked.png', (self.x, self.y), 0))
                if char == "#":
                    walls.append(GameObject(world, 'block5', 'woodenBlock.png', (self.x, self.y), 0))
                if char == "%":
                    moveables.append(MoveableObject(world, 'block5', 'key.png', (self.x, self.y), 0))
                    keys.append(moveables[-1])
                if char == "m":
                    moveables.append(MoveableObject(world, 'block5', 'woodenBlock.png', (self.x, self.y), 0))
                if char == "$":
                    sensitives.append(SensitiveObject(world, 'block5', 'keyhole.png', (self.x, self.y), 0))
                if char == "D":
                    player.rect.left = self.x
                    player.rect.top = self.y
                    player.health = player.health_size
                    player.alive = True
                    player.location = [self.x, self.y]
                    player.robotsKilled = 0
                    player.jump = 0
                    player.jumpPrep = 0
                    player.gravity = 0
                    world.scroll = player.rect.move(-150, -90)
                if char == ">":
                    next_levels.append(GameObject(world, 'next_level', 'next_level.png', (self.x, self.y), 0))                  
                if char == ")":
                    next_levels.append(InvisibleObject(world, 'next_level', 'next_level.png', (self.x, self.y), 0))
                if char == "<":
                    previous_levels.append(GameObject(world, 'previous_level', 'previous_level.png', (self.x, self.y), 0))                  
                if char == "'":
                    badGuys1.append(BadGuy1(world, 'badguy', 'robo1.png', (self.x, self.y), 1))
                if char == "\"":
                    badGuys2.append(BadGuy2(world, 'badguy', 'robo2-1.png', (self.x, self.y), 1))
                if char == "o":
                    power.append(Fortune(world, 'power', 'power2.png', (self.x, self.y), 0, 1))
                if char == "0":
                    health.append(Fortune(world, 'health', 'health2.png', (self.x, self.y), 0, 0))
                if char == "L":
                    lavas.append(Death(world, 'Lava', 'lava.png', (self.x, self.y), 0))
                if char == "1":
                    levelSelects.append(GotoLevel((self.x, self.y), level1_1, 1, 2))
                if char == "2":
                    levelSelects.append(GotoLevel((self.x, self.y), level2_1, 2, 3))
                if char == "3":
                    levelSelects.append(GotoLevel((self.x, self.y), level3_1, 3, 4))
                if char == "S":
                    levelSelects.append(GotoLevel((self.x, self.y), levelSelect, "S", 1))
                
                self.x += 16
            self.y += 16
            self.x = 0
        LoadingBlockController(self.levelNum)
        if self.levelNum == level1_1:
            if player.intro1 == False:
                intro = OnScreen(["I am the Great Giant.", "To move use the arrow keys",    "to jump, hold the up arrow key and keep holding it",
                "and you will bounce higher.", "To get to the Great Mountain go right.","Watch out for robots!"])
                intro.display(screen)
        if self.levelNum == level1_2:
            if player.intro2 == False:
                if player.robotsKilled >= 15:
                    intro = OnScreen(["Congratulations", "Here you go.", "It's the ability to fall faster,", "If you hold the down arrow you will fall faster.", "To be able to bounce higher,", "hold the down arrow while falling and release it", "when jumping."])
                    intro.display(screen)
                    player.increaseGravity = True
                    player.intro2 = True

class LoadingBlockController:

    def __init__(self, levelNum):
        global world
        global loadBlocks
        global walls
        global moveables
        global disappears
        global lavas
        loadBlocks = []
        self.levelNum = levelNum
        self.x = 0
        self.y = 0
        for line in self.levelNum.split("\n"):
            for char in line:
                if self.x % 240 == 0:
                    if self.y % 240 == 0:
                        loadBlocks.append(LoadingBlock((self.x-240, self.y-240)))
                        for wall in walls:
                            if wall.location[0] >= self.x-240 and wall.location[0] < self.x:
                                if wall.location[1] >= self.y-240 and wall.location[1] < self.y:
                                    loadBlocks[-1].blocks.append(wall)
                        for lava in lavas:
                            if lava.location[0] >= self.x-240 and lava.location[0] < self.x:
                                if lava.location[1] >= self.y-240 and lava.location[1] < self.y:
                                    loadBlocks[-1].lavas.append(lava)
                        for disappear in disappears:
                            if disappear.location[0] >= self.x-240 and disappear.location[0] < self.x:
                                if disappear.location[1] >= self.y-240 and disappear.location[1] < self.y:
                                    loadBlocks[-1].disappears.append(disappear)
                        for sensitive in sensitives:
                            if sensitive.location[0] >= self.x-240 and sensitive.location[0] < self.x:
                                if sensitive.location[1] >= self.y-240 and sensitive.location[1] < self.y:
                                    loadBlocks[-1].sensitives.append(sensitive)
                        for moveable in moveables:
                            if moveable.location[0] >= self.x-240 and moveable.location[0] < self.x:
                                if moveable.location[1] >= self.y-240 and moveable.location[1] < self.y:
                                    loadBlocks[-1].moveables.append(moveable)
                        
                self.x += 16
            self.y += 16
            self.x = 0

class World(object):
    """ All objects will be placed in the world """
    def __init__(self, screen, background_image_filename):
        # Load the background and give it a rect for scrolling
        self.background = pygame.image.load(background_image_filename).convert()
        # Scrolling
        self.scroll = vector2.Vector2(0,0) # For scrolling the screen, this will be applied to each object
        self.rect = screen.get_rect().inflate(480, 480)
                
    def process(self, player):
        # This allows the world to iterate over all objects
        global loadBlocks
        for object in loadBlocks:
            if self.rect.colliderect(object.rect):
                for sensitive in object.sensitives:
                    sensitive.process()
                for moveable in object.moveables:
                    moveable.process()
        for object in badGuys1:
            if self.rect.colliderect(object.rect):
                if object.alive == True:
                    object.process()
        for object in badGuys2:
            if self.rect.colliderect(object.rect):
                if object.alive == True:
                    object.process()
        player.process(self, player)
        self.rect.left = self.scroll.x -240
        self.rect.top = self.scroll.y -240
            
    def render(self, surface):
        # Renders all the objects the world contains
        global loadBlocks
        surface.blit(self.background, (-self.scroll.x/2 % -400, -self.scroll.y/2 % -300)) # Creates a background scrolling effect
        player.render(surface)
        for object in loadBlocks:
            if self.rect.colliderect(object.rect):
                for wall in object.blocks:
                    wall.render(surface)
                for lava in object.lavas:
                    lava.render(surface)
                for disappear in object.disappears:
                    if disappear.alive == True:
                        disappear.render(surface)
                for sensitive in object.sensitives:
                    sensitive.render(surface)
                for moveable in object.moveables:
                    moveable.render(surface)
        for object in levelSelects:
            if self.rect.colliderect(object.rect):
                object.render(surface)
        for object in next_levels:
            if self.rect.colliderect(object.rect):
                object.render(surface)
        for object in previous_levels:
            if self.rect.colliderect(object.rect):
                object.render(surface)
        for object in badGuys1:
            if self.rect.colliderect(object.rect):
                if object.alive == True:
                    object.render(surface)
        for object in badGuys2:
            if self.rect.colliderect(object.rect):
                if object.alive == True:
                    object.render(surface)
        for object in health:
            if self.rect.colliderect(object.rect):
                if object.alive == True:
                    object.render(surface)
        for object in power:
            if self.rect.colliderect(object.rect):
                if object.alive == True:
                    object.render(surface)

class GotoLevel(object):
    def __init__(self, location, level, levelNum, levelNumForBeaten):
        global world
        self.level = level
        self.levelNumForBeaten = levelNumForBeaten
        self.font = pygame.font.SysFont('sans', 16)
        self.levelNum = self.font.render(str(levelNum), 1, (155, 155, 0))
        self.location = location
        self.rect = pygame.Rect(location[0], location[1], 16, 16)
        self.relative = self.rect.move((-world.scroll.x, -world.scroll.y)) # The relative allows for the object to move the same way the screen does.
        
    def render(self, surface):
        global world
        if player.levelsBeaten[self.levelNumForBeaten] == True:
            pygame.draw.polygon(screen, (155, 0, 10), ((self.location[0] - world.scroll.x - 5, self.location[1] - world.scroll.y),(self.location[0] - world.scroll.x + 11, self.location[1] - world.scroll.y),(self.location[0] - world.scroll.x +11, self.location[1] - world.scroll.y + 16),(self.location[0] - world.scroll.x - 5, self.location[1] - world.scroll.y + 16)))
        else:
            pygame.draw.polygon(screen, (0, 0, 0), ((self.location[0] - world.scroll.x - 5, self.location[1] - world.scroll.y),(self.location[0] - world.scroll.x + 11, self.location[1] - world.scroll.y),(self.location[0] - world.scroll.x +11, self.location[1] - world.scroll.y + 16),(self.location[0] - world.scroll.x - 5, self.location[1] - world.scroll.y + 16)))
        screen.blit(self.levelNum, (self.rect.move((-world.scroll.x, -world.scroll.y))))    
        
class GameObject(object):
    """ Will be used for every object in the game. Even the player will use a form of it."""
    def __init__(self, world, name, image_filename, location, gravity):
        self.world = world
        self.name = name
        self.alive = True
        self.sprite2, self.rect = load_image(image_filename)
        self.sprite = self.sprite2
        self.location = location
        self.rect = self.rect.move(location)
        self.destination = vector2.Vector2(0, 0)
        self.relative = self.rect
        self.gravity = gravity
        
    def render(self, surface):
        surface.blit(self.sprite, self.rect.move(-world.scroll.x, -world.scroll.y))

class SensitiveObject(GameObject):
    def __init__(self, world, name, image_filename, location, gravity):
        GameObject.__init__(self, world, name, image_filename, location, gravity)
        
    def process(self):
        global moveables
        global loadBlocks
        global keys
        global disappears
        for key in keys:
            if self.rect.colliderect(key.rect):
                for disappear in disappears:
                    disappear.alive = False
                    
    def render(self, surface):
        surface.blit(self.sprite, self.rect.move(-world.scroll.x, -world.scroll.y))

class MoveableObject(GameObject):
    def __init__(self, world, name, image_filename, location, gravity):
        GameObject.__init__(self, world, name, image_filename, location, gravity)
        self.timing = 0
        self.moved = False
    def process(self):
        if self.moved == True:
            if self.timing > 200:
                if self.rect.x > self.location[0]:
                    self.rect.x -= 2
                    if self.rect.colliderect(player.rect):
                        self.rect.x += 2
                if self.rect.x < self.location[0]:
                    self.rect.x += 2
                    if self.rect.colliderect(player.rect):
                        self.rect.x -= 2
                if self.rect.y > self.location[1]:
                    self.rect.y -= 2
                    if self.rect.colliderect(player.rect):
                        self.rect.y += 2
                if self.rect.y < self.location[1]:
                    self.rect.y += 2
                    if self.rect.colliderect(player.rect):
                        self.rect.y -= 2
        if self.location[0] == self.rect.x and self.location[1] == self.rect.y:
            self.timing = 0
            self.moved = False
        self.timing += 1
    def render(self, surface):
        surface.blit(self.sprite, self.rect.move(-world.scroll.x, -world.scroll.y))

        
class LoadingBlock(object):
    """ Will be used for loading different parts of levels"""
    def __init__(self, location):
        self.rect = pygame.Rect(location[0], location[1], 32, 32)
        self.blocks = []
        self.lavas = []
        self.disappears = []
        self.sensitives = []
        self.moveables = []
        
    def render(self, surface):
        surface.blit(self.sprite, self.rect.move(-world.scroll.x, -world.scroll.y))

class Death(GameObject):
    def __init__(self, world, name, image_filename, location, gravity):
        GameObject.__init__(self, world, name, image_filename, location, gravity)
        self.sprite2 = pygame.image.load("data/lava.png").convert_alpha()

class InvisibleObject(GameObject):
    def __init__(self, world, name, image_filename, location, gravity):
        GameObject.__init__(self, world, name, image_filename, location, gravity)
    def render(self, screen):
        pass

                
class Fortune(GameObject):
    def __init__(self, world, name, image_filename, location, gravity, power):
        GameObject.__init__(self, world, name, image_filename, location, gravity)
        self.power = power
                            
class Player(GameObject):
    
    def __init__(self, world, name, image_filename, location, gravity):
        GameObject.__init__(self, world, name, image_filename, location, gravity)
        #Health and power
        self.jumping = False
        self.health_size = 10 #Maximum size of health
        self.power_size = 0
        self.power = 0
        self.health = 10
        #Destination and speed stuff
        self.destination.x
        self.destination.y
        self.ufoSpeed = False
        #Frames
        self.frameSpeed = 0
        self.frameDirection = 0
        self.spriteNumber = 1
        self.frame = 0
        self.location = location
        #Jumping
        self.jumpPrep = 0
        self.jumpStrength = 1
        self.bounce = .5
        self.onRightWall = False
        self.onLeftWall = False
        self.onGround = False
        self.onRoof = False
        self.jump = 0
        #States
        self.state = "ball"
        #Sprites
        # Ball Sprites  
        self.spriteBall1 = self.sprite
        self.spriteBallSquash = pygame.image.load("data/diddleSquash.png").convert_alpha()
        self.spriteBallSquashR = pygame.image.load("data/RdiddleSquash.png").convert_alpha()
        self.spriteBallSquashL = pygame.image.load("data/LdiddleSquash.png").convert_alpha()
        self.spriteBallSquashU = pygame.image.load("data/UdiddleSquash.png").convert_alpha()
        self.spriteBallJump = pygame.image.load("data/diddleJump.png").convert_alpha()
        self.spriteBall2 = pygame.image.load("data/diddle1.png").convert_alpha()
        self.spriteBall3 = pygame.image.load("data/diddle2.png").convert_alpha()
        self.spriteBall4 = pygame.image.load("data/diddle3.png").convert_alpha()
        self.spriteBall5 = pygame.image.load("data/diddle4.png").convert_alpha()
        # Ufo Sprites
        self.spriteUfo1 = pygame.image.load("data/diddleUfo1.png").convert_alpha()
        self.spriteUfoSquash = pygame.image.load("data/diddleUfoSquash.png").convert_alpha()
        self.spriteUfoJump = pygame.image.load("data/diddleUfoJump.png").convert_alpha()
        self.spriteUfo2 = pygame.image.load("data/diddleUfo2.png").convert_alpha()
        self.spriteUfo3 = pygame.image.load("data/diddleUfo3.png").convert_alpha()
        self.spriteUfo4 = self.spriteUfo2
        self.spriteUfo5 = self.spriteUfo1
        # Spider Sprites
        self.spriteSpider1 = pygame.image.load("data/diddleSpider1.png").convert_alpha()
        self.spriteSpiderSquash = pygame.image.load("data/diddleSpiderSquash.png").convert_alpha()
        self.spriteSpiderJump = pygame.image.load("data/diddleSpiderJump.png").convert_alpha()
        self.spriteSpider2 = pygame.image.load("data/diddleSpider2.png").convert_alpha()
        self.spriteSpider3 = pygame.image.load("data/diddleSpider3.png").convert_alpha()
        self.spriteSpider4 = self.spriteSpider2
        self.spriteSpider5 = self.spriteSpider1
        # Spider Sprites Sideways
        self.spriteSpiderR = pygame.image.load("data/RdiddleSpider.png").convert_alpha()
        self.spriteSpiderR1 = pygame.image.load("data/RdiddleSpider1.png").convert_alpha()
        self.spriteSpiderR2 = pygame.image.load("data/RdiddleSpider2.png").convert_alpha()
        self.spriteSpiderL = pygame.image.load("data/LdiddleSpider.png").convert_alpha()
        self.spriteSpiderL1 = pygame.image.load("data/LdiddleSpider1.png").convert_alpha()
        self.spriteSpiderL2 = pygame.image.load("data/LdiddleSpider2.png").convert_alpha()
        self.spriteSpiderU = pygame.image.load("data/UdiddleSpider.png").convert_alpha()
        self.spriteSpiderU1 = pygame.image.load("data/UdiddleSpider1.png").convert_alpha()
        self.spriteSpiderU2 = pygame.image.load("data/UdiddleSpider2.png").convert_alpha()
        
        # Default Sprites
        self.sprite1 = self.spriteBall1
        self.spriteSquash = self.spriteBallSquash
        self.spriteJump = self.spriteBallJump
        self.sprite2 = self.spriteBall2
        self.sprite3 = self.spriteBall3
        self.sprite4 = self.spriteBall4
        self.sprite5 = self.spriteBall5
        # Glowing Sprites
        self.spriteGlow1 = pygame.image.load("data/diddleGlow1.png").convert_alpha()
        self.spriteGlow2 = pygame.image.load("data/diddleGlow2.png").convert_alpha()
        self.spriteGlow3 = pygame.image.load("data/diddleGlow3.png").convert_alpha()
        self.spritePlayerSpiderHurt = pygame.image.load("data/diddlePlayerSpiderHurt.png").convert_alpha()
        self.spritePlayerHurt = pygame.image.load("data/diddleOnFire.png").convert_alpha()
        self.spriteHover1 = pygame.image.load("data/hover1.png").convert_alpha()
        self.spriteHover2 = pygame.image.load("data/hover2.png").convert_alpha()
        self.spriteHover3 = pygame.image.load("data/hover3.png").convert_alpha()
        self.spriteHover4 = pygame.image.load("data/hover4.png").convert_alpha()
        self.spriteHover5 = pygame.image.load("data/hover5.png").convert_alpha()
        self.spriteHover = self.spriteHover1
        self.flightBeams = []
        self.time = 0
        self.flightBeamShoot = True
        self.intro1 = False
        self.intro2 = False
        
        self.increaseGravity = False
        self.spiderCrawl = False
        self.spiderUnlocked = False
        self.ufoUnlocked = False
        self.robotsKilled = 0
        
        #Levels Beaten
        self.levelsBeaten = [True, True, False, False, False, False]
    
    def restart(self):
        global screen
        global clock
        global world
        self.GreatSpriteList = [pygame.image.load("data/giant2.png").convert_alpha(),pygame.image.load("data/giant3.png").convert_alpha(), pygame.image.load("data/giant4.png").convert_alpha(), pygame.image.load("data/giant5.png").convert_alpha(), pygame.image.load("data/giant6.png").convert_alpha(), pygame.image.load("data/giant7.png").convert_alpha(), pygame.image.load("data/giant8.png").convert_alpha(), pygame.image.load("data/giant9.png").convert_alpha(), pygame.image.load("data/giant10.png").convert_alpha() ,pygame.image.load("data/giant11.png").convert_alpha() ,pygame.image.load("data/giant12.png").convert_alpha() ,pygame.image.load("data/giant13.png").convert_alpha(), pygame.image.load("data/giant14.png").convert_alpha(), pygame.image.load("data/giant15.png").convert_alpha(), pygame.image.load("data/giant16.png").convert_alpha(), pygame.image.load("data/giant17.png").convert_alpha(), pygame.image.load("data/giant18.png").convert_alpha()]
        self.GLocation_x = self.rect.left - 16
        self.GLocation_y = self.rect.top + 150
        self.GreatSprite = pygame.image.load("data/giant2.png").convert_alpha()
        for i in range(40):
            clock.tick(30)
            world.render(screen)
            screen.blit(self.GreatSprite, (self.GLocation_x - world.scroll.x, self.GLocation_y - world.scroll.y))
            self.GLocation_y -= 7.5
            pygame.display.flip()
        for i in range(0, 16):
            clock.tick(7)
            if i == 7:
                self.sprite = pygame.image.load("data/blank.png").convert_alpha()
            world.render(screen)
            screen.blit(self.GreatSpriteList[i], (self.GLocation_x - world.scroll.x, self.GLocation_y - world.scroll.y))
            self.render(screen)
            pygame.display.flip()
        for i in range(15):
            if self.rect.left > self.location[0]:
                self.rect.left -= 3
            if self.rect.left < self.location[0]:
                self.rect.left += 3
            if self.rect.top < self.location[1]:
                self.rect.top += 3
            if self.rect.top > self.location[1]:
                self.rect.top -= 3
            world.rect.left = world.scroll.x -240
            world.rect.top = world.scroll.y -240
            world.scroll = self.rect.move(-150, -90)
            world.background_x = -world.scroll.x/2 % -400
            world.background_y = -world.scroll.y/2 % -300
            world.render(screen)
            screen.blit(self.GreatSpriteList[-i], (self.GLocation_x - world.scroll.x, self.GLocation_y - world.scroll.y))
            if i > 6:
                self.GLocation_y += 10
            if i == 6:
                player.rect.top -= 16
                player.sprite = self.spriteBallSquash
            pygame.display.flip()
        exit = False
        while exit != True:
            self.frameSpeed += 1
            clock.tick(28)
            for x in range(15):
                if self.rect.left > self.location[0]:
                    self.rect.left -= 1
                if self.rect.left < self.location[0]:
                    self.rect.left += 1
                if self.rect.top < self.location[1]:
                    self.rect.top += 1
                if self.rect.top > self.location[1]:
                    self.rect.top -= 1
                if self.rect.top == self.location[1]:
                    if self.rect.left == self.location[0]:
                        exit = True
            if self.frameSpeed %3 == 0:
                # Add power every 6th frame
                self.power += .1
                self.frameSpeed = 1
                self.frame += 1
                if self.frame > 4:
                    self.frame = 1
                    self.sprite = self.sprite2
                if self.frame < 1:
                    self.frame = 4
                    self.sprite = self.sprite4
                if self.frame == 2:
                    self.sprite = self.sprite3
                if self.frame == 3:
                    self.sprite = self.sprite4
                if self.frame == 4:
                    self.sprite = self.sprite5
            world.rect.left = world.scroll.x -240
            world.rect.top = world.scroll.y -240
            world.scroll = self.rect.move(-150, -90)
            world.background_x = -world.scroll.x/2 % -400
            world.background_y = -world.scroll.y/2 % -300
            world.render(screen)
            pygame.display.flip()
            
        
    def changeState(self, state):
        #States change what mode he is whether ball, spider or UFO
        if state == "ball":
            self.state = "ball"
            self.jumpStrength = 1
            self.bounce = 1
            self.sprite1 = self.spriteBall1
            self.spriteSquash = self.spriteBallSquash
            self.spriteJump = self.spriteBallJump
            self.sprite2 = self.spriteBall2
            self.sprite3 = self.spriteBall3
            self.sprite4 = self.spriteBall4
            self.sprite5 = self.spriteBall5
        if state == "spider":
            self.state = "spider"
            self.jumpStrength = 1.5
            self.bounce = 0
            self.spriteSquash = self.spriteSpiderSquash
            self.spriteJump = self.spriteSpiderJump
            self.sprite1 = self.spriteSpider1
            self.sprite2 = self.spriteSpider2
            self.sprite3 = self.spriteSpider3
            self.sprite4 = self.spriteSpider4
            self.sprite5 = self.spriteSpider5
        if state == "ufo":
            self.state = "ufo"
            self.jumpStrength = 1
            self.bounce = 0
            self.spriteSquash = self.spriteUfoSquash
            self.spriteJump = self.spriteUfoJump
            self.sprite1 = self.spriteUfo1
            self.sprite2 = self.spriteUfo2
            self.sprite3 = self.spriteUfo3
            self.sprite4 = self.spriteUfo4
            self.sprite5 = self.spriteUfo5
        self.rect = self.sprite1.get_rect().move(self.rect.left, self.rect.top)
        
    def move(self, dx, dy):
        
        # Call __move() for the x axis, then the y axis.
        if dx != 0:
            self.__move(dx, 0)
        if dy != 0:
            self.__move(0, dy)
    
    def __move(self, dx, dy):
        global Level
        global moveables
        global world        
        # Move the rect
        self.rect.x += dx
        self.rect.y += dy

        # If you collide with a wall, move out based on velocity
        for object in loadBlocks:
            if world.rect.colliderect(object.rect):
                for wall in object.blocks:
                    if self.rect.colliderect(wall.rect):
                        if dx > 0: # Moving right; Hit the left side of the wall
                            self.rect.right = wall.rect.left
                            self.onRightWall = True
                            if self.state == "ball":
                                self.sprite = self.spriteBallSquashR
                        if dx < 0: # Moving left; Hit the right side of the wall
                            self.rect.left = wall.rect.right
                            self.onLeftWall = True
                            if self.state == "ball":
                                self.sprite = self.spriteBallSquashL
                        if dy > 0: # Moving down; Hit the top side of the wall
                            self.rect.bottom = wall.rect.top
                            self.onGround = True
                            if self.state == "ball":
                                if self.jumping == True:
                                    self.jump = -self.gravity -1 - self.jumpPrep
                                    self.jumpPrep = 0
                                else:
                                    self.jump = -self.gravity + 2
                                    if self.jump >= 0:
                                        self.jump = 0
                                    self.jumpPrep = 0
                                if self.gravity > 1:
                                    self.sprite = self.spriteBallSquash
                        if dy < 0: # Moving up; Hit the bottom side of the wall
                            self.rect.top = wall.rect.bottom
                            self.onRoof = True
                            if self.state == "ball":
                                self.sprite = self.spriteBallSquashU
                
                for moveable in moveables:
                    if self.rect.colliderect(moveable.rect):
                        moveable.moved = True
                        if dx > 0: # Moving right; Hit the left side of the wall
                            moveable.rect.left = self.rect.right
                            if self.state == "ball":
                                self.sprite = self.spriteBallSquashR
                        if dx < 0: # Moving left; Hit the right side of the wall
                            moveable.rect.right = self.rect.left
                            if self.state == "ball":
                                self.sprite = self.spriteBallSquashL
                        if dy > 0: # Moving down; Hit the top side of the wall
                            moveable.rect.top = self.rect.bottom
                            self.onGround = True
                            if self.state == "ball":
                                if self.jumping == True:
                                    self.jump = -self.gravity -1 - self.jumpPrep
                                    self.jumpPrep = 0
                                else:
                                    self.jump = -self.gravity + 2
                                    if self.jump >= 0:
                                        self.jump = 0
                                    self.jumpPrep = 0
                                if self.gravity > 1:
                                    self.sprite = self.spriteBallSquash
                        if dy < 0: # Moving up; Hit the bottom side of the wall
                            moveable.rect.bottom = self.rect.top
                            if self.state == "ball":
                                self.sprite = self.spriteBallSquashU
                        
                for wall in object.disappears:
                    if wall.alive == True:
                        if self.rect.colliderect(wall.rect):
                            if dx > 0: # Moving right; Hit the left side of the wall
                                self.rect.right = wall.rect.left
                                self.onRightWall = True
                                if self.state == "ball":
                                    self.sprite = self.spriteBallSquashR
                            if dx < 0: # Moving left; Hit the right side of the wall
                                self.rect.left = wall.rect.right
                                self.onLeftWall = True
                                if self.state == "ball":
                                    self.sprite = self.spriteBallSquashL
                            if dy > 0: # Moving down; Hit the top side of the wall
                                self.rect.bottom = wall.rect.top
                                self.onGround = True
                                if self.state == "ball":
                                    if self.jumping == True:
                                        self.jump = -self.gravity -1 - self.jumpPrep
                                        self.jumpPrep = 0
                                    else:
                                        self.jump = -self.gravity + 2
                                        if self.jump >= 0:
                                            self.jump = 0
                                        self.jumpPrep = 0
                                    if self.gravity > 1:
                                        self.sprite = self.spriteBallSquash
                            if dy < 0: # Moving up; Hit the bottom side of the wall
                                self.rect.top = wall.rect.bottom
                                self.onRoof = True
                                if self.state == "ball":
                                    self.sprite = self.spriteBallSquashU

                for lava in object.lavas:
                    if self.rect.colliderect(lava.rect):
                        if dx > 0: # Moving right; Hit the left side of the lava
                            self.rect.right = lava.rect.left
                            self.onRightWall = True
                            if self.state == "ball":
                                self.sprite = self.spriteBallSquashR
                            if self.state != "spider":
                                self.health -= 5
                                self.sprite = self.sprite = self.spritePlayerHurt
                            else:
                                self.sprite = self.spritePlayerSpiderHurt
                                self.health -= 2
                        if dx < 0: # Moving left; Hit the right side of the lava
                            self.rect.left = lava.rect.right
                            self.onLeftWall = True
                            if self.state == "ball":
                                self.sprite = self.spriteBallSquashL
                            if self.state != "spider":
                                self.health -= 5
                                self.sprite = self.spritePlayerHurt
                            else:
                                self.sprite = self.spritePlayerSpiderHurt
                                self.health -= 2
                        if dy > 0: # Moving down; Hit the top side of the lava
                            self.rect.bottom = lava.rect.top
                            self.onGround = True
                            self.jump = -self.gravity
                            if self.state == "ball":
                                if self.jumping == True:
                                    self.jump = -self.gravity -1 - self.jumpPrep
                                    self.jumpPrep = 0
                                else:
                                    self.jump = -self.gravity + 2
                                    if self.jump >= 0:
                                        self.jump = 0
                                    self.jumpPrep = 0
                                if self.gravity > 1:
                                    self.sprite = self.spriteBallSquash
                            if self.state != "spider":
                                self.health -= 5
                                self.sprite = self.spritePlayerHurt
                            else:
                                self.sprite = self.spritePlayerSpiderHurt
                                self.health -= 2
                        if dy < 0: # Moving up; Hit the bottom side of the lava
                            self.rect.top = lava.rect.bottom
                            self.onRoof = True
                            if self.state == "ball":
                                self.sprite = self.spriteBallSquashU
                            if self.state != "spider":
                                self.health -= 5
                                self.sprite = self.spritePlayerHurt
                            else:
                                self.sprite = self.spritePlayerSpiderHurt
                                self.health -= 2
                        pygame.mixer.Sound.play(ouch)
                
        for healths in health:
            if healths.alive == True:
                if self.rect.colliderect(healths.rect):
                    healths.alive = False
                    self.health += 10
                    
        for powers in power:
            if powers.alive == True:
                if self.rect.colliderect(powers.rect):
                    powers.alive = False
                    self.power += 10
                    
        for next_level in next_levels:
            if self.rect.colliderect(next_level.rect):
                if levelNumber == 1:
                    intro = OnScreen(["Congratulations!", "You made it to the top!"])
                    intro.display(screen)
                    cutscene = Cutscene(600, 2)
                    cutscene.display(screen)
                Level = Levels(level1_2)
        
        for levelSelect in levelSelects:
            if self.rect.colliderect(levelSelect.rect):
                if self.levelsBeaten[levelSelect.levelNumForBeaten - 1] == True: 
                    self.levelsBeaten[levelSelect.levelNumForBeaten] = True
                    Level = Levels(levelSelect.level)
                
        for previous_level in previous_levels:
            if self.rect.colliderect(previous_level.rect):
                Level = Levels(level1_1)
                
        for badguy in badGuys1:
            if badguy.alive == True:
                if self.rect.colliderect(badguy.rect):
                    if dx > 0: # Moving right; Hit the left side of the wall
                        self.rect.right = badguy.rect.left
                        if self.state != "spider":
                            self.sprite = self.spritePlayerHurt
                        else:
                            self.sprite = self.spritePlayerSpiderHurt
                        self.health -= .25  
                        pygame.mixer.Sound.play(ouch)
                    if dx < 0: # Moving left; Hit the right side of the wall
                        self.rect.left = badguy.rect.right
                        if self.state != "spider":
                            self.sprite = self.spritePlayerHurt
                        else:
                            self.sprite = self.spritePlayerSpiderHurt
                        self.health -= .25
                        pygame.mixer.Sound.play(ouch)
                    if dy > 0: # Moving down; Hit the top side of the wall
                        self.rect.bottom = badguy.rect.top
                        self.onGround = True
                        if self.state == "ball":
                            if self.jumping == True:
                                self.jump = -self.gravity -1 - self.jumpPrep
                                self.jumpPrep = 0
                            else:
                                self.jump = -self.gravity + 2
                                if self.jump >= 0:
                                    self.jump = 0
                                self.jumpPrep = 0
                            if self.gravity > 1:
                                self.sprite = self.spriteBallSquash
                        if self.gravity > 2:
                            pygame.mixer.Sound.play(clink)
                            badguy.health -= self.gravity*self.gravity
                            badguy.sprite = badguy.spriteHurt
                    if dy < 0: # Moving up; Hit the bottom side of the wall
                        badguy.rect.bottom = self.rect.top
                        if self.state != "spider":
                            self.sprite = self.spritePlayerHurt
                        else:
                            self.sprite = self.spritePlayerSpiderHurt
                        self.health -= .25      
                        pygame.mixer.Sound.play(ouch)
                

        for badguy in badGuys2:
            if badguy.alive == True:
                if self.rect.colliderect(badguy.rect):
                    if dx > 0: # Moving right; Hit the left side of the wall
                        self.rect.right = badguy.rect.left
                        if self.state != "spider":
                            self.sprite = self.spritePlayerHurt
                        else:
                            self.sprite = self.spritePlayerSpiderHurt
                        self.health -= .25  
                        pygame.mixer.Sound.play(ouch)
                    if dx < 0: # Moving left; Hit the right side of the wall
                        self.rect.left = badguy.rect.right
                        if self.state != "spider":
                            self.sprite = self.spritePlayerHurt
                        else:
                            self.sprite = self.spritePlayerSpiderHurt
                        self.health -= .25
                        pygame.mixer.Sound.play(ouch)
                    if dy > 0: # Moving down; Hit the top side of the wall
                        badguy.rect.top = self.rect.bottom
                        self.onGround = True
                        for wall in walls:
                            if badguy.rect.colliderect(wall.rect):
                                badguy.rect.bottom = wall.rect.top
                                self.rect.bottom = badguy.rect.top
                        self.onGround = True
                        self.health -= .25
                        pygame.mixer.Sound.play(ouch)
                    if dy < 0: # Moving up; Hit the bottom side of the wall
                        self.rect.top = badguy.rect.bottom
                        badguy.onGround = True
                        badguy.gravity = 0
                        badguy.sprite = badguy.spriteHurt
                        badguy.health += self.jump/4
                        pygame.mixer.Sound.play(clink)
                        
        
    
    def process(self, world, player):
        #Reset the destinations
        self.destination.x = 0
        self.destination.y = 0
        if self.state == "ufo":
            for beam in self.flightBeams:
                screen.blit(self.spriteHover, (beam[0]-world.scroll.x +10 -2*self.time, beam[1]-world.scroll.y + 10 + self.time*5))
                if len(self.flightBeams) > 0:
                    del self.flightBeams[0]
            if self.time > 5:
                self.time = 1
            if self.time == 1:
                self.spriteHover = self.spriteHover1
            if self.time == 2:
                self.spriteHover = self.spriteHover2
            if self.time == 3:
                self.spriteHover = self.spriteHover3
            if self.time == 4:
                self.spriteHover = self.spriteHover4
            if self.time == 5:
                self.spriteHover = self.spriteHover5
            self.time += 1
            self.flightBeamShoot = True
        if self.health < 0:
            self.alive = False
        if self.health > self.health_size:
            self.health = self.health_size
        if self.power < 0:
            self.power = 0
        if self.power > self.power_size:
            self.power = self.power_size
        self.frameSpeed += 1
        # Apply Gravity
        if self.onGround == False:
            if self.frameSpeed > 7:
                self.sprite = self.sprite1
            self.gravity += .1
        else:
        # Turn Gravity off when touching the ground
            if self.state != "ball":
                self.jump = 0
            self.gravity = 0
            self.onGround = False
        if self.ufoSpeed == True:
            self.gravity -= .2
            if self.gravity < 0:
                self.gravity = 0
        if self.jump < -25:
            self.jump = -25
        if self.spiderCrawl == True:
            if self.onRoof == True or self.onRightWall == True or self.onLeftWall == True:
                self.gravity = 0
        if self.state == "ball":
            self.destination.y = self.gravity * self.gravity + (self.jump * self.bounce * self.jumpStrength)
        else:
            self.destination.y = self.gravity * self.gravity
        if self.destination.y > 15:
            self.destination.y = 15
        if self.destination.y < -15:
            self.destination.y = -15
        self.move(0, self.destination.y)
        #Reset the bounce to it's usuall value
        self.bounce = .5
        #Make the world move as player does
        world.scroll = self.rect.move(-150, -90)
        # Animated Sprites
        if self.frameSpeed %6 == 0:
            # Add power every 6th frame
            self.power += .1
            if abs(self.frameDirection) == 1:
                self.frameSpeed = 1
                self.frame += self.frameDirection
                if self.frame > 4:
                    self.frame = 1
                    self.sprite = self.sprite2
                if self.frame < 1:
                    self.frame = 4
                    self.sprite = self.sprite4
                if self.frame == 2:
                    self.sprite = self.sprite3
                if self.frame == 3:
                    self.sprite = self.sprite4
                if self.frame == 4:
                    self.sprite = self.sprite5
        self.frameDirection = 0
        self.onRightWall = False
        self.onLeftWall = False
        self.onRoof = False
        self.spiderCrawl = False

    def getKey(self):
        pressed_keys = pygame.key.get_pressed()
        for keys in pressed_keys:
            if pressed_keys[K_RIGHT]:
                self.destination.x = 3
                if self.ufoSpeed == True:
                    self.destination.x = 9
                self.frameDirection = 1
            if pressed_keys[K_LEFT]:
                self.destination.x = -3
                if self.ufoSpeed == True:
                    self.destination.x = -9
                self.frameDirection = -1
        if self.destination.x > 15:
            self.destination.x = 15
        self.move(self.destination.x, 0)    
        self.ufoSpeed = False
        for keys in pressed_keys:
            if pressed_keys[K_UP]:
                if self.state == "ball":
                    self.jumpPrep = self.gravity/2
                    self.jumping = True
                else:
                    self.jump = -3
                    self.destination.y = -3
            if pressed_keys[K_SPACE]:
                # The Special Key
                if self.state == "ufo":
                    if self.power > 1:
                        if self.flightBeamShoot == True:
                            pygame.mixer.Sound.play(fly)
                            self.flightBeams.append((self.rect.x, self.rect.y))
                            self.flightBeamShoot = False
                        self.power -= .001  
                        self.ufoSpeed = True
                elif self.state == "spider":
                    if self.onGround == False:
                        if self.onRightWall == True:
                            if random.randint(0, 15) == 1:
                                self.sprite = self.spriteSpiderR1
                            if random.randint(0, 15) == 1:
                                self.sprite = self.spriteSpiderR
                            if random.randint(0, 15) == 1:
                                self.sprite = self.spriteSpiderR2
                            self.spiderCrawl = True
                        if self.onLeftWall == True:
                            if random.randint(0, 15) == 1:
                                self.sprite = self.spriteSpiderL1
                            if random.randint(0, 15) == 1:
                                self.sprite = self.spriteSpiderL
                            if random.randint(0, 15) == 1:
                                self.sprite = self.spriteSpiderL2
                            self.spiderCrawl = True
                        if self.onRoof == True:
                            if random.randint(0, 15) == 1:
                                self.sprite = self.spriteSpiderU1
                            if random.randint(0, 15) == 1:
                                self.sprite = self.spriteSpiderU
                            if random.randint(0, 15) == 1:
                                self.sprite = self.spriteSpiderU2
                            self.spiderCrawl = True
                elif self.state == "ball":
                    if self.power > 1:
                        if self.onGround == True:
                            self.jump = self.gravity*2
                            self.power -= .001
            if pressed_keys[K_DOWN]:
                if self.increaseGravity == True:
                    if self.onGround == False:
                        self.gravity += .001
                        
        if self.destination.y > 15:
            self.destination.y = 15
        self.move(0, self.destination.y)
        self.jumping = False
                            

class OnScreen():
    def __init__(self, message):
        self.messageList = message                      
        self.font = pygame.font.SysFont('sans', 13)
        self.textbox = pygame.image.load("data/textbox.png").convert_alpha()
        self.next = False
        self.line = 1
        self.messagePrinted = []
        
    def display(self, screen):
        for line in self.messageList:
            self.messagePrinted.append(self.font.render(line, 1, (255, 255, 255)))
        while self.next == False:
            self.get_key(screen)
            world.render(screen)
            screen.blit(self.textbox, (10, 10))
            for line in self.messagePrinted:
                screen.blit(line, (15, 15*self.line))
                self.line += 1
            pygame.display.flip()
            self.line = 1
                
        player.intro1 = True
                
    def get_key(self, screen):
        global fullscreen
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    exit()
                if event.key == K_f:
                    if fullscreen:
                        screen = pygame.display.set_mode((320, 240),0)
                        fullscreen = False
                    else:
                        screen = pygame.display.set_mode((320, 240),FULLSCREEN)
                        fullscreen = True
                if event.key == K_SPACE:
                    self.next = True
        
        
class Cutscene():
    def __init__(self, time, sceneNum):                     
        self.timeBase = time
        self.sceneNum = sceneNum
        self.sceneList = []
        if self.sceneNum == 1:
            self.sceneList.append(pygame.image.load("data/cutscene1-1.png").convert())
            self.sceneList.append(pygame.image.load("data/cutscene1-2.png").convert())
            self.sceneList.append(pygame.image.load("data/cutscene1-3.png").convert())
            self.sceneList.append(pygame.image.load("data/cutscene1-4.png").convert())
        if self.sceneNum == 2:
            self.sceneList.append(pygame.image.load("data/cutscene2-1.png").convert())
    
    def display(self, screen):
        black = pygame.Surface((320, 240))
        black.fill((0, 0, 0))
        blackalpha = 255
        imagealpha = 0
        for x in self.sceneList:
            self.time = self.timeBase
            while blackalpha > 0:
                clock.tick(28)
                self.get_key(screen)
                blackalpha -= 20
                black.set_alpha(blackalpha)
                screen.blit(x, (0, 0))
                screen.blit(black, (0, 0))
                pygame.display.flip()
            while self.time > 0:
                self.get_key(screen)
                screen.blit(x, (0,0))
                pygame.display.flip()
                clock.tick(28)
                self.time -= 1
            blackalpha = 0
            while blackalpha < 255:
                clock.tick(28)
                self.get_key(screen)
                blackalpha += 20
                black.set_alpha(blackalpha)
                screen.blit(x, (0, 0))
                screen.blit(black, (0, 0))
                pygame.display.flip()
    
    def get_key(self, screen):
        global fullscreen
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    exit()
                if event.key == K_f:
                    if fullscreen:
                        screen = pygame.display.set_mode((320, 240),0)
                        fullscreen = False
                    else:
                        screen = pygame.display.set_mode((320, 240),FULLSCREEN)
                        fullscreen = True
                if event.key == K_SPACE:
                    self.time = 0
                        
class BadGuy1(GameObject):
    
    def __init__(self, world, name, image_filename, location, gravity):
        GameObject.__init__(self, world, name, image_filename, location, gravity)
        #Health and power
        self.sprite1 = self.sprite
        self.spriteHurt = pygame.image.load("data/robo1Hurt.png").convert_alpha()
        self.spriteEx1 = pygame.image.load("data/robo1ex1.png").convert_alpha()
        self.spriteEx2 = pygame.image.load("data/robo1ex2.png").convert_alpha()
        self.spriteEx3 = pygame.image.load("data/robo1ex3.png").convert_alpha()
        self.health = 10
        #Gravity
        self.gravityConstant = 1
        self.rect = pygame.Rect(location[0], location[1], 32, 20)
        
        self.dead = False
        self.spriteNumber = 1
        #Climbing
        self.onRightWall = False
        self.onLeftWall = False
        #Jumping
        self.jumpStrength = 1
        self.bounce = 1
        self.onGround = False
        self.onRoof = False
        self.jump = -1
        self.jumpPrep = 0 #Prep gives you more jump when you land instead of during
        self.gravity = 0
        self.timeB4Die = 0
        self.directionChange = 1
        self.destination.x = random.randint(-2, 2)
        
    def process(self):
        global power
        global health
        self.directionChange += 1
        if self.directionChange %10 == 0:
            self.sprite = self.sprite1
        if self.directionChange > random.randint(10, 600):
            self.destination.x = random.randint(-2, 2)
            self.directionChange = 0
        if self.health < 1:
            self.timeB4Die += 1
            if self.timeB4Die %2 == 0:
                self.sprite = self.spriteEx1
            if self.timeB4Die %3 == 0:
                self.sprite = self.spriteEx2
            else:
                self.sprite = self.spriteEx3
            pygame.mixer.Sound.play(explode)            
            if self.timeB4Die > 10:
                self.alive = False
                if random.randint(0, 10) == 1:
                    power.append(Fortune(world, 'power', 'power2.png', (self.rect.left, self.rect.top), 0, 1))
                elif random.randint(0, 8) == 1:
                    health.append(Fortune(world, 'health', 'health2.png', (self.rect.left, self.rect.top), 0, 0))
                player.robotsKilled += 1
            
        self.destination.y = self.gravity*self.gravity
        self.move(self.destination.x, 0)
        self.move(0, self.destination.y)
        if self.onGround == False:
            self.gravity += .1
            if self.gravity > 15:
                self.gravity = 15
        else:
            self.onGround = False
                
    def move(self, dx, dy):
        
        # Call __move() for the x axis, then the y axis.
        if dx != 0:
            self.__move(dx, 0)
        if dy != 0:
            self.__move(0, dy)
    
    def __move(self, dx, dy):
        global world
        global loadBlocks
        # Move the rect
        self.rect.x += dx
        self.rect.y += dy
        # If you collide with a wall, move out based on velocity
        for object in loadBlocks:
            if world.rect.colliderect(object.rect):
                for wall in object.blocks:
                    if self.rect.colliderect(wall.rect):
                        if dx > 0: # Moving right; Hit the left side of the wall
                            self.rect.right = wall.rect.left
                            self.directionChange += 37
                        if dx < 0: # Moving left; Hit the right side of the wall
                            self.rect.left = wall.rect.right
                            self.directionChange += 37
                        if dy > 0: # Moving down; Hit the top side of the wall
                            self.rect.bottom = wall.rect.top
                            self.onGround = True
                            self.gravity = 0
                        if dy < 0: # Moving up; Hit the bottom side of the wall
                            self.rect.top = wall.rect.bottom
        for wall in lavas:
            if self.rect.colliderect(wall.rect):
                if dx > 0: # Moving right; Hit the left side of the wall
                    self.rect.right = wall.rect.left
                    self.directionChange += 37
                if dx < 0: # Moving left; Hit the right side of the wall
                    self.rect.left = wall.rect.right
                    self.directionChange += 37
                if dy > 0: # Moving down; Hit the top side of the wall
                    self.rect.bottom = wall.rect.top
                    self.onGround = True
                    self.gravity = 0
                if dy < 0: # Moving up; Hit the bottom side of the wall
                    self.rect.top = wall.rect.bottom
                        
        if self.rect.colliderect(player.rect):
            if dx > 0: # Moving right; Hit the left side of the wall
                player.rect.left = self.rect.right
                for wall in walls:
                    if player.rect.colliderect(wall.rect):
                        player.rect.right = wall.rect.left
                        self.rect.right = player.rect.left
                if player.state != "spider":
                    player.sprite = player.spritePlayerHurt
                else:
                    player.sprite = player.spritePlayerSpiderHurt
                player.health -= .25        
                pygame.mixer.Sound.play(ouch)
            if dx < 0: # player moves left; Hit the right side of the wall
                player.rect.right = self.rect.left
                for wall in walls:
                    if player.rect.colliderect(wall.rect):
                        player.rect.left = wall.rect.right
                        self.rect.left = player.rect.right
                if player.state != "spider":
                    player.sprite = player.spritePlayerHurt
                else:
                    player.sprite = player.spritePlayerSpiderHurt
                player.health -= .25
                pygame.mixer.Sound.play(ouch)
            if dy > 0: # Moving down; Hit the top side of the wall
                self.rect.bottom = player.rect.top
                player.onGround = True
                if player.gravity > 2:
                    pygame.mixer.Sound.play(clink)
                    self.health -= player.gravity*player.gravity - self.gravity*self.gravity
                    self.sprite = self.spriteHurt
            if dy < 0: # Moving up; Hit the bottom side of the wall
                player.rect.bottom = self.rect.top
                self.onGround = True
                if player.state != "spider":
                    player.sprite = player.spritePlayerHurt
                else:
                    player.sprite = player.spritePlayerSpiderHurt
                player.health -= .25        
                pygame.mixer.Sound.play(ouch)
def load_image(name):
    """ Load image and return image object"""
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
        if image.get_alpha() is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
    except pygame.error:
        print(("Can't load image: ", fullname))
        raise SystemExit
    return image, image.get_rect()
    
class BadGuy2(GameObject):
    
    def __init__(self, world, name, image_filename, location, gravity):
        GameObject.__init__(self, world, name, image_filename, location, gravity)
        #Health and power
        self.sprite1 = self.sprite
        self.sprite2 = pygame.image.load("data/robo2-2.png").convert_alpha()
        self.spriteHurt = pygame.image.load("data/robo2Hurt.png").convert_alpha()
        self.spriteSquashed = pygame.image.load("data/robo2Squashed.png").convert_alpha()
        self.spriteEx1 = pygame.image.load("data/robo2ex1.png").convert_alpha()
        self.spriteEx2 = pygame.image.load("data/robo2ex2.png").convert_alpha()
        self.spriteEx3 = pygame.image.load("data/robo2ex3.png").convert_alpha()
        self.health = 2
        #Gravity
        self.gravityConstant = 1
        self.rect = pygame.Rect(location[0], location[1], 28, 32)
        
        self.dead = False
        #Frames
        self.frameSpeed = 0
        self.frameDirection = 0
        self.spriteNumber = 1
        #Climbing
        self.onRightWall = False
        self.onLeftWall = False
        #Jumping
        self.jumpStrength = 1
        self.bounce = 1
        self.onGround = False
        self.onRoof = False
        self.jump = -1
        self.jumpPrep = 0 #Prep gives you more jump when you land instead of during
        self.gravity = 0
        self.timeB4Die = 0
        self.directionChange = 1
        self.destination.x = 0
        
    def process(self):
        self.frameSpeed += 1
        if self.frameSpeed % 15 == 0:
            if self.sprite == self.sprite2:
                self.sprite = self.sprite1
            elif self.sprite == self.sprite1:
                self.sprite = self.sprite2
            else:
                self.sprite = self.sprite1
        self.directionChange += 1
        if self.directionChange > random.randint(10, 600):
            self.destination.x *= -1
            self.directionChange = 0
        if self.health < 1:
            self.timeB4Die += 1
            if self.timeB4Die %2 == 0:
                self.sprite = self.spriteEx1
            if self.timeB4Die %3 == 0:
                self.sprite = self.spriteEx2
            else:
                self.sprite = self.spriteEx3
            pygame.mixer.Sound.play(explode)            
            if self.timeB4Die > 10:
                self.alive = False
                
                player.robotsKilled += 1
            
        self.destination.y = self.gravity * self.gravity -4
        if self.destination.y > 7:
            self.destination.y = 7
        self.move(self.destination.x, 0)
        self.move(0, self.destination.y)
        if self.onGround == False:
            self.gravity += .1
            if self.gravity > 15:
                self.gravity = 15
        else:
            self.onGround = False
        
                
    def move(self, dx, dy):
        
        # Call __move() for the x axis, then the y axis.
        if dx != 0:
            self.__move(dx, 0)
        if dy != 0:
            self.__move(0, dy)
    
    def __move(self, dx, dy):
        global world
        global loadBlocks
        # Move the rect
        self.rect.x += dx
        self.rect.y += dy

        # If you collide with a wall, move out based on velocity
        for object in loadBlocks:
            if world.rect.colliderect(object.rect):
                for wall in object.blocks:
                    if self.rect.colliderect(wall.rect):
                        if dx > 0: # Moving right; Hit the left side of the wall
                            self.rect.right = wall.rect.left
                            self.directionChange += 37
                        if dx < 0: # Moving left; Hit the right side of the wall
                            self.rect.left = wall.rect.right
                            self.directionChange += 37
                        if dy > 0: # Moving down; Hit the top side of the wall
                            self.rect.bottom = wall.rect.top
                            self.onGround = True
                            self.gravity = 0
                            self.sprite = self.spriteSquashed
                        if dy < 0: # Moving up; Hit the bottom side of the wall
                            self.rect.top = wall.rect.bottom
                for wall in object.lavas:
                    if self.rect.colliderect(wall.rect):
                        if dx > 0: # Moving right; Hit the left side of the wall
                            self.rect.right = wall.rect.left
                            self.directionChange += 37
                        if dx < 0: # Moving left; Hit the right side of the wall
                            self.rect.left = wall.rect.right
                            self.directionChange += 37
                        if dy > 0: # Moving down; Hit the top side of the wall
                            self.rect.bottom = wall.rect.top
                            self.onGround = True
                            self.gravity = 0
                        if dy < 0: # Moving up; Hit the bottom side of the wall
                            self.rect.top = wall.rect.bottom
                    
        if self.rect.colliderect(player.rect):
            if dx < 0: # Moving right; Hit the left side of the wall
                player.rect.right = self.rect.left
                for wall in walls:
                    if player.rect.colliderect(wall.rect):
                        player.rect.right = wall.rect.left
                        self.rect.right = player.rect.left
                if player.state != "spider":
                    player.sprite = player.spritePlayerHurt
                else:
                    player.sprite = player.spritePlayerSpiderHurt
                player.health -= .25    
                pygame.mixer.Sound.play(ouch)
            if dx > 0: # Moving left; Hit the right side of the wall
                player.rect.left = self.rect.right
                for wall in walls:
                    if player.rect.colliderect(wall.rect):
                        player.rect.left = wall.rect.right
                        self.rect.left = player.rect.right
                if player.state != "spider":
                    player.sprite = player.spritePlayerHurt
                else:
                    player.sprite = player.spritePlayerSpiderHurt
                player.health -= .25
                pygame.mixer.Sound.play(ouch)
            if dy < 0: # Moving down; Hit the top side of the wall
                self.rect.top = player.rect.bottom
                for wall in walls:
                    if self.rect.colliderect(wall.rect):
                        self.rect.bottom = wall.rect.top
                        player.rect.bottom = self.rect.top
                player.onGround = True
                player.health -= 1
                pygame.mixer.Sound.play(ouch)
            if dy > 0: # Moving Down; Hit the top side of the wall
                self.rect.bottom = player.rect.top
                self.onGround = True
                self.onGround = True
                self.gravity = 0
                self.sprite = self.spriteHurt
                self.health += player.jump/4
                pygame.mixer.Sound.play(clink)

    #Create a list for different objects
pygame.init()
lavas = []
badGuys1 = []
badGuys2 = []
walls = []
moveables = []
power = []
sensitives = []
levelSelects = []
loadBlocks = []
disappears = []
health = []
keys = []
next_levels = []
previous_levels = []
screen = pygame.display.set_mode((320, 240))
world = World(screen, 'data/background3.jpg')
player = Player(world, 'diddle', 'diddle.png', (0, 0), 1)
pygame.mouse.set_visible(False)
pygame.display.set_caption("The Feeble Diddle \"Alpha\"")
pygame.mixer.init()
boing = pygame.mixer.Sound("data/boing.ogg")
ouch = pygame.mixer.Sound("data/ouch.ogg")
clink = pygame.mixer.Sound("data/clink.ogg")
explode = pygame.mixer.Sound("data/explode.ogg")
fly = pygame.mixer.Sound("data/fly.ogg")
music = pygame.mixer.music.load("data/Killing Time.ogg")
pygame.mixer.music.play(-1)
clock = pygame.time.Clock()
fullscreen = False
Level = Levels(levelSelect)
levelNumber = 1
quit = False

def run():
    global Level
    global screen   
    global fullscreen

    font = pygame.font.SysFont('sans', 15)
    health_image = pygame.image.load("data/health.png").convert_alpha()
    power_image = pygame.image.load("data/power.png").convert_alpha()
    time.sleep(2)
    world.process(player)
    if player.intro1 == False:
        cutscene1 = Cutscene(500, 1)
        cutscene1.display(screen)
        intro = OnScreen(["This is the level selection screen.", "To select a level just bounce into it.", "To bounce higher hold the up button."])
        intro.display(screen)
# The loop that the game runs in
    while quit == False:
        if player.alive == False:
            player.restart()
            Level = Levels(Level.levelNum)
        clock.tick(30) #Make the game run at no more than 28 Frames Per Second
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    exit()
                if event.key == K_f:
                    if fullscreen:
                        screen = pygame.display.set_mode((320, 240),0)
                        fullscreen = False
                    else:
                        screen = pygame.display.set_mode((320, 240),FULLSCREEN)
                        fullscreen = True
                if event.key == K_s:
                    # The state/mode switching button
                    if player.spiderUnlocked == True:
                        if player.power > 10:
                            player.power -= 10
                            player.changeState("spider")
                            for i in range(10):
                                clock.tick(10)
                                if i % 2:
                                    player.sprite = player.spriteGlow1
                                else:
                                    player.sprite = player.spriteGlow2
                                world.render(screen)
                                pygame.display.update()
                if event.key == K_t:
                    player.increaseGravity = True
                    player.spiderUnlocked = True
                    player.ufoUnlocked = True
                    player.health = 100
                    player.health_size = 100
                    player.power = 100
                    player.power_size = 100
                    player.levelsBeaten = [True, True, True, True, True, True, True, True, True]

                if event.key == K_a:
                    # The state/mode switching button
                    if player.power > 10:
                        player.power -= 10
                        player.changeState("ball")
                        for i in range(10):
                            clock.tick(10)
                            if i % 2:
                                player.sprite = player.spriteGlow1
                            if i % 3:
                                player.sprite = player.spriteGlow3
                            else:
                                player.sprite = player.spriteGlow2
                            world.render(screen)
                            pygame.display.update()
                            
                if event.key == K_d:
                    # The state/mode switching button
                    if player.ufoUnlocked == True:
                        if player.power > 10:
                            player.power -= 10
                            player.changeState("ufo")
                            for i in range(10):
                                clock.tick(10)
                                if i % 2:
                                    player.sprite = player.spriteGlow1
                                else:
                                    player.sprite = player.spriteGlow2
                                world.render(screen)
                                pygame.display.update()
                            
        world.render(screen)
        world.process(player)
        player.getKey()
        #Details labels
        fps = font.render("FPS: %s" %int(clock.get_fps()), 1, (0, 0, 100))
        jump = font.render("Jump: %s" %player.jump, 1, (0, 100, 100))
        gravity = font.render("Gravity: %s" %player.gravity, 1, (100, 0, 10))
        robotsKilled = font.render("Robots Killed: %s" %player.robotsKilled, 1, (10, 10, 90))
        screen.blit(fps, (160, 10))
        screen.blit(jump, (160, 25))
        screen.blit(gravity, (160, 40))
        screen.blit(robotsKilled, (160, 55))
        # Draw the health and power bars
        pygame.draw.polygon(screen, (189, 0, 0), ((10,5),(10,24),(player.health +13, 24),(player.health +13,5)))
        screen.blit(health_image, (5, 5))
        pygame.draw.line(screen, (0, 0, 100), (player.health_size +13, 23),(player.health_size +13, 6), 1)
        if player.power_size > 0:
            pygame.draw.polygon(screen, (0, 189, 0), ((10,28),(10,45),(player.power +13,45),(player.power +13, 28)))
            screen.blit(power_image, (5, 27))
            pygame.draw.line(screen, (0, 0, 100), (player.power_size +13, 46),(player.power_size +13, 28), 1)
        pygame.display.flip()
        
if __name__ == '__main__':
    run()
