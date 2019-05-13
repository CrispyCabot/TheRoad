import pygame
from pygame.locals import QUIT, K_q, K_r, K_ESCAPE
from config import SIZE, WIDTH, HEIGHT, PATH
from player import Player
from Obstacles import Bush, Tree
from random import randint, choice
from enemy import Enemy
import os

pygame.init()

win = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption('The Road')

bullet = pygame.image.load(PATH+os.path.join('data', 'bullet.png'))
w, h = bullet.get_rect().size
bullet = pygame.transform.scale(bullet, (int(w*SIZE*.3), int(h*SIZE*.3)))
bullet = pygame.transform.rotate(bullet,90)

font = pygame.font.Font(PATH+os.path.join('data', 'font.ttf'), 166)

def main():
    player = Player(100,HEIGHT-300)

    mapParts = [getMap('test')]
    playerLoc = 0
    currMap = mapParts[playerLoc] #currMap = [[obstacles], [enemies]]

    playing = True
    end = True
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
        for i in player.shots:
            if i.x > WIDTH+50 or i.x < -50:
                player.shots.remove(i)
                break
            for x in currMap[1]:
                if i.x > x.x-12 and i.x < x.x+12:
                    currMap[1].remove(x)
                    player.shots.remove(i)
                    break
        continuedEnemies = []
        if player.x > WIDTH:
            for i in currMap[1]:
                if i.behavior == 'alerted':
                    continuedEnemies.append(i)
            for i in continuedEnemies:
                i.x -= WIDTH
            player.x = 0
            playerLoc += 1
            try:
                currMap = mapParts[playerLoc]
            except IndexError:
                mapParts.append(getMap())
                currMap = mapParts[playerLoc]
            for i in continuedEnemies:
                currMap[1].append(i)
        elif player.x < 0:
            for i in currMap[1]:
                if i.behavior == 'alerted':
                    continuedEnemies.append(i)
            for i in continuedEnemies:
                i.x += WIDTH
            player.x = WIDTH
            playerLoc -= 1
            if playerLoc >= 0:
                currMap = mapParts[playerLoc]
            else:
                playerLoc += 1
                currMap = mapParts[playerLoc]
                player.x = 0
            for i in continuedEnemies:
                currMap[1].append(i)

        for i in currMap[1]:
            i.update(player, currMap[0])
        if player.health <= 0:
            playing = False
        redraw(win, player, currMap)
        pygame.display.update()

    while end:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == QUIT:
                return False
        if keys[K_r]:
            return True
        if keys[K_q] or keys[K_ESCAPE]:
            return False
        redraw(win, player, currMap)
        text = font.render('Game Over', True, (255,0,0))
        loc = text.get_rect()
        loc.center = (WIDTH/2, HEIGHT/2)
        win.blit(text, loc)
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
    xCounter = 25
    for i in range(player.numShots):
        loc = bullet.get_rect()
        loc.topleft = (xCounter, 5)
        win.blit(bullet, loc)
        xCounter += 15
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

while main():
    main()