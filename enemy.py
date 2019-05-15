import pygame
from config import WIDTH, HEIGHT, SIZE, PATH
import os
from random import choice, randint

pygame.init()

font = pygame.font.Font(PATH+os.path.join('data', 'font.ttf'), 56)

walkR = []
for i in range(12):
    img = pygame.image.load(PATH+os.path.join('data', 'enemy', str(i)+'.gif'))
    w, h = img.get_rect().size
    img = pygame.transform.scale(img, (int(w*SIZE*.8), int(h*SIZE*.8)))
    walkR.append(img)

walkL = []
for i in range(12):
    img = pygame.transform.flip(walkR[i], True, False)
    walkL.append(img)

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        dirs = ['left', 'right', '', '']
        self.dir = choice(dirs)
        self.vel = 2
        self.behavior = 'idle'
        self.cautionTimer = 0
        self.alertTimer = 0
        self.frameCounter = 0
        self.lastImg = walkR[0]
        self.seenLoc = 0
    def update(self, player, obstacles):
        #Detect player
        if (self.lastImg in walkL) and player.x < self.x:
            alerted = True
            for i in obstacles:
                if i.x > player.x and i.x < self.x:
                    alerted = False
                if i.x - 20 < player.x < i.x+20:
                    alerted = False
            if alerted:
                if self.cautionTimer > 25:
                    self.behavior = 'alerted'
                    self.vel = 4.5
                    self.alertTimer = 0
                else:
                    self.behavior = 'cautious'
                    self.seenLoc = player.x
        if (self.lastImg in walkR) and player.x > self.x:
            alerted = True
            for i in obstacles:
                if i.x < player.x and i.x > self.x:
                    alerted = False
                if i.x - 20 < player.x < i.x+20:
                    alerted = False
            if alerted:
                if self.cautionTimer > 25:
                    self.behavior = 'alerted'
                    self.vel = 4.5
                    self.alertTimer = 0
                else:
                    self.behavior = 'cautious'
                    self.seenLoc = player.x

        if self.behavior == 'idle':
            self.vel = 2
            self.cautionTimer = 0
            if randint(0,100) == 0:
                if self.dir == '':
                    if randint(0,1) == 0:
                        self.dir = 'right'
                    else:
                        self.dir = 'left'
                else:
                    self.dir = ''
            if self.x > WIDTH-10:
                self.dir = 'left'
            elif self.x < 10:
                self.dir = 'right'
        elif self.behavior == 'cautious':
            self.vel = 3
            self.cautionTimer += 1
            hidden = False
            for i in obstacles:
                if player.x < i.x+20 and player.x > i.x-20:
                    hidden = True
                    break
            if self.seenLoc != -100:
                if self.seenLoc < 0:
                    self.seenLoc = 0
                elif self.seenLoc > WIDTH:
                    self.seenLoc = WIDTH
                if abs(self.seenLoc - self.x) < 30:
                    self.seenLoc = -100
                elif self.seenLoc < self.x:
                    self.dir = 'left'
                elif self.seenLoc > self.x:
                    self.dir = 'right'
            else:
                if abs(player.x-self.x) < 20 and not hidden:
                    self.behavior = 'alerted'
                    self.vel = 4.5
                if randint(0,30) == 1:
                    if self.dir == 'right':
                        self.dir = 'left'
                    else:
                        self.dir = 'right'
                if self.cautionTimer > 200:
                    self.cautonTimer = 0
                    self.behavior = 'idle'
        elif self.behavior == 'alerted':
            hidden = False
            for i in obstacles:
                if player.x < i.x+20 and player.x > i.x-20:
                    hidden = True
                    break
            if hidden:
                self.behavior = 'cautious'
                if player.dir == 'right':
                    self.seenLoc = player.x + 100
                elif player.dir == 'left':
                    self.seenLoc = player.x - 100
                else:
                    self.seenLoc = player.x
                self.cautionTimer = 0
            if self.alertTimer > 200:
                self.behavior = 'idle'
                self.vel = 2
            if abs(self.x-player.x) < 30 and not hidden:
                player.health -= 1
                player.damageTimer = 0
            elif player.x < self.x:
                self.dir = 'left'
            elif player.x > self.x:
                self.dir = 'right'

        #actually moves the enemy
        if self.dir == 'right':
            self.x += self.vel
            if self.x > WIDTH:
                self.x = WIDTH
        elif self.dir == 'left':
            self.x -= self.vel
            if self.x < 0:
                self.x = 0
    def draw(self, win):
        self.frameCounter += 1
        if self.frameCounter > 11:
            self.frameCounter = 0
        img = self.lastImg
        if self.dir == 'right':
            img = walkR[self.frameCounter]
            self.lastImg = img
        elif self.dir == 'left':
            img = walkL[self.frameCounter]
            self.lastImg = img
        loc = img.get_rect()
        loc.midbottom = (self.x, self.y+5)
        win.blit(img, loc)
        #loc = pygame.Rect(0,0,25,50)
        #loc.midbottom = (self.x, self.y)
        #pygame.draw.rect(win, (60,0,0), loc)
        if self.behavior == 'cautious':
            text = font.render('?', True, (100,0,0))
            loc = text.get_rect()
            loc.center = (self.x+35, self.y-70)
            win.blit(text, loc)
        if self.behavior == 'alerted':
            text = font.render('!', True, (100,0,0))
            loc = text.get_rect()
            loc.center = (self.x+35, self.y-70)
            win.blit(text, loc)