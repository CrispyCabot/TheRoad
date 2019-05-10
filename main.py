import pygame
from pygame.locals import QUIT, K_q, K_r, K_ESCAPE
from config import SIZE, WIDTH, HEIGHT
from player import Player
from Obstacles import Bush, Tree
from random import randint, choice
from enemy import Enemy

pygame.init()

win = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption('The Road')

def main():
    player = Player(100,HEIGHT-300)

    mapParts = [getMap('test')]
    playerLoc = 0
    currMap = mapParts[playerLoc] #currMap = [[obstacles], [enemies]]

    playing = True
    while playing:
        for event in pygame.event.get():
            if event.type == QUIT:
                return False
        keys = pygame.key.get_pressed()
        if keys[K_r]:
            return True
        if keys[K_q] or keys[K_ESCAPE]:
            return False
        player.update(keys)
        if player.x > WIDTH:
            player.x = 0
            playerLoc += 1
            try:
                currMap = mapParts[playerLoc]
            except IndexError:
                mapParts.append(getMap())
                currMap = mapParts[playerLoc]
        if player.x < 0:
            player.x = WIDTH
            playerLoc -= 1
            try:
                currMap = mapParts[playerLoc]
            except IndexError:
                player.loc = 0

        for i in currMap[1]:
            i.update(player, currMap[0])
        redraw(win, player, currMap)
        pygame.display.update()

def redraw(win, player, currMap):
    drawBackground(win)
    for i in currMap[0]:
        i.draw(win)
    for i in currMap[1]:
        i.draw(win)
    hidden = False
    for i in currMap[0]:
        loc = pygame.Rect(0,0,40,100)
        loc.midbottom = (i.x, i.y)
        pygame.draw.rect(win, (255,0,0), loc, 1)
        if i.x-20 < player.x < i.x+20:
            hidden = True
    if hidden:
        pygame.draw.circle(win, (0,255,0), (10,10), 8)
    else:
        pygame.draw.circle(win, (255,0,0), (10,10), 8)
    player.draw(win)

def drawBackground(win):
    win.fill((255,255,255))
    pygame.draw.rect(win, (0,0,0), pygame.Rect(0,HEIGHT-300,WIDTH,300))

def getMap(test=''):
    numObs = randint(1,6)
    layout = []
    for i in range(numObs):
        if randint(0,1) == 0:
            layout.append(Bush(randint(0,WIDTH), 300))
        else:
            layout.append(Tree(randint(0,WIDTH), 305))
    numEnemies = randint(0,3)
    enemies = []
    for i in range(numEnemies):
        enemies.append(Enemy(randint(200,WIDTH), 300))
    return [layout, enemies]

def getMap2():
    possible = []
    layout = [
        Bush(200,300),
        Bush(600,300)
    ]
    enemies = [
        Enemy(500,300),
        Enemy(600,300)
    ]
    possible.append([layout, enemies])
    layout = [
        Bush(100,300),
        Bush(200,300),
        Bush(800,300),
        Tree(500, 300)
    ]
    enemies = [
        Enemy(200,300)
    ]
    possible.append([layout, enemies])
    return possible[randint(0,len(possible)-1)]
    
while main():
    main()