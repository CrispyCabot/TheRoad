import pygame
from config import WIDTH, HEIGHT, PATH
import os

pygame.init()

class Button:
    def __init__(self, x, y, w, h, text, tSize):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.text = text
        self.font = pygame.font.Font(PATH+os.path.join('data', 'font.ttf'), tSize)
    def clicked(self, mouse):
        rect = pygame.Rect(self.x, self.y, self.w, self.h)
        if rect.collidepoint(mouse[0], mouse[1]):
            return True
        return False
    def draw(self, win):
        mouse = pygame.mouse.get_pos()
        rect = pygame.Rect(self.x, self.y, self.w, self.h)
        if rect.collidepoint(mouse):
            pygame.draw.rect(win, (0,0,0), rect)
            pygame.draw.rect(win, (255,255,255), rect, 1)
            text = self.font.render(self.text, True, (255,255,255))
        else:
            pygame.draw.rect(win, (255,255,255), rect)
            text = self.font.render(self.text, True, (0,0,0))
        loc = text.get_rect()
        loc.center = (self.x+self.w/2, self.y+self.h/2)
        win.blit(text, loc)