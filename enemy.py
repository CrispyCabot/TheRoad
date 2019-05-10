import pygame
from config import WIDTH, HEIGHT, SIZE, PATH
import os
from random import choice, randint

pygame.init()

font = pygame.font.Font(PATH+os.path.join('data', 'font.ttf'), 56)

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
    def update(self, player, obstacles):
        if self.dir == 'left' and player.x < self.x:
            alerted = True
            for i in obstacles:
                if i.x > player.x and i.x < self.x:
                    alerted = False
                if i.x - 20 < player.x < i.x+20:
                    alerted = False
            if alerted:
                print('Was alerted at', self.cautionTimer)
                if self.cautionTimer > 100:
                    self.behavior = 'alerted'
                    self.alertTimer = 0
                else:
                    self.behavior = 'cautious'
        if self.dir == 'right' and player.x > self.x:
            alerted = True
            for i in obstacles:
                if i.x < player.x and i.x > self.x:
                    alerted = False
                if i.x - 20 < player.x < i.x+20:
                    alerted = False
            if alerted:
                print('Was alerted at', self.cautionTimer)
                if self.cautionTimer > 100:
                    self.behavior = 'alerted'
                    self.alertTimer = 0
                else:
                    self.behavior = 'cautious'
        if self.behavior == 'idle':
            if randint(0,100) == 0:
                if self.dir == '':
                    if randint(0,1) == 0:
                        self.dir = 'right'
                    else:
                        self.dir = 'left'
                else:
                    self.dir = ''
        elif self.behavior == 'cautious':
            self.cautionTimer += 1
            if self.cautionTimer >= 500:
                self.behavior = 'idle'
                self.cautionTimer = 0
            if randint(0,100) == 0:
                if randint(0,1) == 0:
                    self.dir = 'right'
                else:
                    self.dir = 'left'
        elif self.behavior == 'alerted':
            print('alerted')
        if self.dir == 'right':
            self.x += self.vel
            if self.x > WIDTH:
                self.x = WIDTH
        elif self.dir == 'left':
            self.x -= self.vel
            if self.x < 0:
                self.x = 0
    def draw(self, win):
        loc = pygame.Rect(0,0,25,50)
        loc.midbottom = (self.x, self.y)
        pygame.draw.rect(win, (60,0,0), loc)
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