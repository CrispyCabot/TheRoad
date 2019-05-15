import pygame
import os
from random import randint
from config import WIDTH, HEIGHT, PATH, SIZE

bushImg = pygame.image.load(PATH+os.path.join('data', 'bush.png'))
w, h = bushImg.get_rect().size
bushImg = pygame.transform.scale(bushImg, (int(w*SIZE), int(h*SIZE)))

trees = []
for i in range(1,18):
    img = pygame.image.load(PATH+os.path.join('data', 'trees', 'tree'+str(i)+'.png'))
    w, h = img.get_rect().size
    img = pygame.transform.scale(img, (int(w*SIZE*5), int(h*SIZE*5)))
    trees.append(img)

class Object:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Bush(Object):
    def __init__(self, x, y):
        Object.__init__(self, x, y)
    def draw(self, win):
        loc = bushImg.get_rect()
        loc.midbottom = (self.x, self.y)
        win.blit(bushImg, loc)

class Tree(Object):
    def __init__(self, x, y, test=100):
        Object.__init__(self, x, y)
        self.type = randint(0,16)
        if test != 100:
            self.type = test
    def draw(self, win):
        img = trees[self.type]
        loc = img.get_rect()
        loc.midbottom = (self.x, self.y)
        win.blit(img, loc)
