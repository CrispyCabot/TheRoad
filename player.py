import pygame
from pygame.locals import K_UP, K_LEFT, K_DOWN, K_RIGHT, K_w, K_a, \
    K_s, K_d, K_SPACE
from config import SIZE, WIDTH, HEIGHT, PATH
import os

walkR = []
for i in range(9):
    img = pygame.image.load(PATH+os.path.join('data', 'walking', str(i)+'.gif'))
    w, h = img.get_rect().size
    img = pygame.transform.scale(img, (int(w*SIZE*.3), int(h*SIZE*.3)))
    walkR.append(img)

walkL = []
for i in range(9):
    img = pygame.transform.flip(walkR[i], True, False)
    walkL.append(img)

bullet = pygame.image.load(PATH+os.path.join('data', 'bullet.png'))
w, h = bullet.get_rect().size
bulletR = pygame.transform.scale(bullet, (int(w*SIZE*.3), int(h*SIZE*.3)))
bulletL = pygame.transform.flip(bulletR, True, False)

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel = 4
        self.numShots = 5
        self.frameCounter = 0
        self.dir = 'right'
        self.moving = False
        self.shots = []
        self.shotDelay = 0
        self.health = 100
        self.damageTimer = 0

    def update(self, keys):
        self.shotDelay += 1
        self.moving = True
        if keys[K_RIGHT] or keys[K_d]:
            self.x += self.vel
            self.dir = 'right'
        elif keys[K_LEFT] or keys[K_a]:
            self.x -= self.vel
            self.dir = 'left'
        else:
            self.moving = False
        if keys[K_SPACE] and self.shotDelay > 20 and self.numShots > 0:
            self.shots.append(Shot(self.x, self.y-50, self.dir))
            self.shotDelay = 0
            self.numShots -= 1

    def draw(self, win):
        img = ''
        if self.moving:
            self.frameCounter += 1
            if self.frameCounter > 8:
                self.frameCounter = 0
        if self.dir == 'right':
            img = walkR[self.frameCounter]
        elif self.dir == 'left':
            img = walkL[self.frameCounter]
        loc = img.get_rect()
        loc.midbottom = (self.x, self.y)
        win.blit(img, loc)
        if self.health < 100 and self.damageTimer < 300:
            self.damageTimer += 1
            pygame.draw.rect(win, (0,0,0), pygame.Rect(self.x-50,self.y-100,self.health,10))
            pygame.draw.rect(win, (0,0,0), pygame.Rect(self.x-50,self.y-100,100, 10), 1)
        for i in self.shots:
            i.draw(win)

        #Rectangle player
        #loc = pygame.Rect(0,0,25,50)
        #loc.midbottom = (self.x, self.y)
        #pygame.draw.rect(win, (0,0,0), loc)

class Shot:
    def __init__(self, x, y, dirr):
        self.x = x
        self.y = y
        if dirr == 'right':
            self.vel = 15
        elif dirr == 'left':
            self.vel = -15
    def draw(self, win):
        self.x += self.vel
        img = None
        if self.vel < 0:
            img = bulletL
        else:
            img = bulletR
        loc = img.get_rect()
        loc.center = (self.x, self.y)
        win.blit(img, loc)