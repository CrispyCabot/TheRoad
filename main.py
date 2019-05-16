import pygame
from pygame.locals import QUIT, K_q, K_r, K_ESCAPE, K_BACKSPACE, \
    K_RETURN, KEYDOWN, MOUSEBUTTONDOWN
from config import SIZE, WIDTH, HEIGHT, PATH
from player import Player
from Obstacles import Bush, Tree
from random import randint, choice
from enemy import Enemy
import os
from button import Button

pygame.init()

win = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption('The Road')

bullet = pygame.image.load(PATH+os.path.join('data', 'bullet.png'))
w, h = bullet.get_rect().size
bullet = pygame.transform.scale(bullet, (int(w*SIZE*.3), int(h*SIZE*.3)))
bullet = pygame.transform.rotate(bullet,90)

font = pygame.font.Font(PATH+os.path.join('data', 'font.ttf'), 166)
smallFont = pygame.font.Font(PATH+os.path.join('data', 'font.ttf'), 66)
plainFont = pygame.font.SysFont('', 26)
largeFont = pygame.font.Font(PATH+os.path.join('data', 'font.ttf'), 250)

def main():
    pygame.mouse.set_visible(True)
    player = Player(100,HEIGHT-300)

    mapParts = [getMap()]
    mapParts[0][1] = []
    playerLoc = 0
    currMap = mapParts[playerLoc] #currMap = [[obstacles], [enemies]]
    scoreboard = []

    file = open(PATH+'scoreboard.txt', 'r')
    text = file.readlines()
    for i in text:
        scoreboard.append(i.split())
    file.close()

    playing = True
    end = True
    hiScore = False
    homeScreen = True
    instructions = False
    homeButtons = []
    homeButtons.append(Button(400,250,200,100,'Play',80))
    homeButtons.append(Button(400,355,200,100,'Instructions', 60))
    backBtn = Button(0,HEIGHT-100,100,50,'Back',50)
    while homeScreen:
        for event in pygame.event.get():
            if event.type == QUIT:
                return False
            if event.type == MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if homeButtons[0].clicked(mouse):
                    homeScreen = False
                if homeButtons[1].clicked(mouse):
                    instructions = True
                    homeScreen = False
        keys = pygame.key.get_pressed()
        if keys[K_q] or keys[K_ESCAPE]:
            return False
        win.fill((0,0,0))
        text = largeFont.render('The Road', True, (255,255,255))
        loc = text.get_rect()
        loc.center = (WIDTH/2, 130)
        win.blit(text, loc)
        for i in homeButtons:
            i.draw(win)
        pygame.display.update()

    while instructions:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == QUIT:
                return False
            if event.type == MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if backBtn.clicked(mouse):
                    return True
        if keys[K_q] or keys[K_ESCAPE]:
            return False
        win.fill((0,0,0))
        text = plainFont.render('You\'re objective is to get as far down the road as you can', True, (255,255,255))
        loc = text.get_rect()
        loc.center = (WIDTH/2, 50)
        win.blit(text, loc)
        text = plainFont.render('Their will be enemies patrolling the area that you must avoid', True, (255,255,255))
        loc = text.get_rect()
        loc.center = (WIDTH/2, 100)
        win.blit(text, loc)
        text = plainFont.render('The enemies cannot see past obstacles (Bushes and trees), and cannot see if you are inside an obstacle', True, (255,255,255))
        loc = text.get_rect()
        loc.center = (WIDTH/2, 150)
        win.blit(text, loc)
        text = plainFont.render('The green or red indicator in the top left displays whether or not you are hidden', True, (255,255,255))
        loc = text.get_rect()
        loc.center = (WIDTH/2, 200)
        win.blit(text, loc)
        text = plainFont.render('You also have five bullets to protect yourself with', True, (255,255,255))
        loc = text.get_rect()
        loc.center = (WIDTH/2, 250)
        win.blit(text, loc)
        text = plainFont.render('You can shoot with spacebar', True, (255,255,255))
        loc = text.get_rect()
        loc.center = (WIDTH/2, 300)
        win.blit(text, loc)
        backBtn.draw(win)
        pygame.display.update()

    pygame.mouse.set_visible(False)
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
        redraw(win, player, currMap, playerLoc)
        pygame.display.update()

    scores = []
    scoreSep = lambda a : a[1]
    for i in scoreboard:
        scores.append(scoreSep(i))

    index = 10
    name = ''
    for i in scores:
        if playerLoc > int(i):
            hiScore = True
            index = scores.index(i)
            break
            
    while hiScore:
        for event in pygame.event.get():
            if event.type == QUIT:
                return False
            if event.type == KEYDOWN:
                if event.key == K_BACKSPACE:
                    name = name[:-1]
                elif event.key == K_RETURN:
                    hiScore = False
                else:
                    name += event.unicode
        redraw(win, player, currMap, playerLoc)
        text = font.render('New High Score', True, (100,100,0))
        loc = text.get_rect()
        loc.center = (WIDTH/2, 100)
        win.blit(text, loc)
        text = smallFont.render('Enter your name', True, (100,100,0))
        loc = text.get_rect()
        loc.center = (WIDTH/2, 225)
        win.blit(text, loc)
        text = font.render(name, True, (255,255,255))
        loc = text.get_rect()
        loc.center = (WIDTH/2, HEIGHT-150)
        win.blit(text, loc)
        pygame.display.update()

    if index != 10:
        name = '-'.join(name.split())
        scoreboard.insert(index, [name, playerLoc])
        scoreboard.pop(5)
        file = open(PATH+'scoreboard.txt', 'w')
        for i in scoreboard:
            file.write(i[0]+' '+str(i[1])+'\n')
            
    while end:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == QUIT:
                return False
        if keys[K_r]:
            return True
        if keys[K_q] or keys[K_ESCAPE]:
            return False
        redraw(win, player, currMap, playerLoc)
        text = font.render('Game Over', True, (255,0,0))
        loc = text.get_rect()
        loc.center = (WIDTH/2, HEIGHT/2-200)
        win.blit(text, loc)
        text = font.render('Scoreboard', True, (100,100,0))
        loc = text.get_rect()
        loc.center = (WIDTH/2, HEIGHT/2-50)
        win.blit(text, loc)
        yCounter = HEIGHT-250
        for i in scoreboard:
            text = smallFont.render(i[0].replace('-', ' '), True, (100,100,0))
            loc = text.get_rect()
            loc.midright = (WIDTH/2-25, yCounter)
            win.blit(text, loc)
            text = smallFont.render(str(i[1]), True, (100,100,0))
            loc = text.get_rect()
            loc.midleft = (WIDTH/2+25, yCounter)
            win.blit(text, loc)
            yCounter += 50
        pygame.display.update()

def redraw(win, player, currMap, playerLoc):
    drawBackground(win)
    for i in currMap[0]:
        i.draw(win)
    for i in currMap[1]:
        i.draw(win)
    hidden = False
    for i in currMap[0]:
        loc = pygame.Rect(0,0,40,100)
        loc.midbottom = (i.x, i.y)
        #pygame.draw.rect(win, (255,0,0), loc, 1) #the outline of safety zone on obstacles
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
    text = smallFont.render('Score: '+str(playerLoc), True, (255,255,255))
    loc = text.get_rect()
    loc.bottomleft = (10,HEIGHT-10)
    win.blit(text, loc)

def drawBackground(win):
    win.fill((255,255,255))
    pygame.draw.rect(win, (0,0,0), pygame.Rect(0,HEIGHT-300,WIDTH,300))

def getMap(test=False):
    if test:
        layout = []
        xCounter = 50
        for i in range(0,17):
            layout.append(Tree(xCounter,300, i))
            xCounter += 75
        return [layout, []]
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

pygame.quit()