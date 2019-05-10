import pygame
from pygame.locals import K_UP, K_LEFT, K_DOWN, K_RIGHT, K_w, K_a, \
    K_s, K_d
from config import SIZE, WIDTH, HEIGHT, PATH

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel = 4
        self.shots = 5

    def update(self, keys):
        if keys[K_RIGHT] or keys[K_d]:
            self.x += self.vel
        if keys[K_LEFT] or keys[K_a]:
            self.x -= self.vel

    def draw(self, win):
        loc = pygame.Rect(0,0,25,50)
        loc.midbottom = (self.x, self.y)
        pygame.draw.rect(win, (0,0,0), loc)