import pygame
from pygame import mixer
import math
import random
import sys
import os



pygame.init()
pygame.mixer.pre_init(44100, 16, 2, 4096)


# GAME WINDOW
pygame.display.set_caption('BOMBER RUN-SG')
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)
run = True
screen = pygame.display.set_mode((1920, 1080))  # ,pygame.FULLSCREEN)
backgroundimg = pygame.image.load('background.png')

# MUSIC
mixer.music.load('background.mp3')
mixer.music.play(-1)
explosionsound=mixer.Sound('explosion.wav')



# SCORE
scorex = 1550
scorey = 10
score_value = 0


def scoring(x, y):
    score = font.render('SCORE:' + str(score_value), True, (34, 139, 34))
    screen.blit(score, (x, y))


# HEALTH
healthx = 10
healthy = 10
health_value = 100
health_change = 20
font = pygame.font.Font('Consequences.ttf', 64)


def health(x, y):
    health = font.render('Health:' + str(health_value), True, (34, 139, 34))
    screen.blit(health, (x, y))


# GAME OVER
def gameover():
    overtext = font.render('GAME OVER DONE BY SHUBHAM GANDHI', True, (255, 0, 0))
    screen.blit(overtext, (200, 500))


#  PLANE
planex = 500
planey = 100
planex_change = 1
planey_change = 10
planeimg = pygame.image.load('plane.png')


def plane(x, y):
    screen.blit(planeimg, (x, y))


# BOMBS
bombx = planex
bomby = planey
bomby_change = 2.5
bombimg = pygame.image.load('bomb.png')
bomb_state = 'not ready'


def bomb(x, y):
    global bomb_state
    bomb_state = 'ready'
    screen.blit(bombimg, (x + 50, y + 70))


# JEEP
jeepimg = pygame.image.load('jeep.png')
jeepx = 50
jeepy = 820


def jeep(x, y):
    screen.blit(jeepimg, (x, y))


# HELICOPTER
helix = 1770
heliy = 810
heliimg = pygame.image.load('helicopter.png')


def heli(x, y):
    screen.blit(heliimg, (x, y))


explosionx = bombx
explosiony = bomby
explosionimg = pygame.image.load('explosion.png')


def explode(x, y):
    screen.blit(explosionimg, (x, y))


# PLAYER
playerx = 500
playerx_change = 0
playery_change = 0
playery = 862
player1img = pygame.image.load('player.png')
player2img = pygame.image.load('player2.png')
missileimg = pygame.image.load('missile.png')
missilex = playerx
missiley = playery

missiley_change = 5
missile_state = 'ready'


def missile(x, y):
    global missile_state
    missile_state = 'fire'
    screen.blit(missileimg, (x, y))


def col(missilex, missiley, bombx, bomby):
    dist = math.sqrt((math.pow((missilex - bombx), 2)) + (math.pow((missiley - bomby), 2)))
    if dist < 64:
        return True
    else:
        return False


# Fire
firex = bombx + 55
firey = 880
fireimg = pygame.image.load('fire.png')
firechk = False


def fire(x, y):
    screen.blit(fireimg, (x, y))


def player1(x, y):
    screen.blit(player1img, (x, y))


def player2(x, y):
    screen.blit(player2img, (x, y))


# BASE
base1x = 700
base2x = 300
base3x = 1500
basehealth = 100
base1y = 675
base2y = 715
base3y = 690
base1img = pygame.image.load('base.png')
base2img = pygame.image.load('base2.png')
base3img = pygame.image.load('base3.png')


def base(base, x, y):
    screen.blit(base, (x, y))


while run:

    screen.blit(backgroundimg, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    plane(planex, planey)
    jeep(jeepx, jeepy)
    heli(helix, heliy)

    base(base1img, base1x, base1y)
    base(base2img, base2x, base2y)
    base(base3img, base3x, base3y)
    if playerx < (1920 // 2) - 100:
        player1(playerx, playery)
    else:
        player2(playerx, playery)

    planex += planex_change
    plane(planex, planey)
    if planex == 1920:
        planex = 0

    playerx_change = 0
    if event.type == pygame.KEYDOWN:
        if event.key == ord('a'):
            playerx_change -= 10
        if event.key == ord('d'):
            playerx_change += 10
        if event.key == ord(' '):
            if missile_state == 'ready':
                missilex = playerx
                missile(missilex, missiley)

    if event.type == pygame.KEYUP:
        if event.key == ord('a') or event.key == ord('d'):
            playerx_change = 0
    playerx += playerx_change
    if playerx < 180:
        playerx = 180
    if playerx > 1700:
        playerx = 1700

    if score_value < 5:
        count = random.randint(1, 100)
    elif score_value < 10:
        count = random.randint(1, 50)
    elif score_value < 15:
        count = random.randint(1, 25)
    else:
        count = random.randint(1, 6)

    if count == 5:
        bomb_state = 'ready'

    if bomb_state == 'ready':
        bomb(bombx, bomby)
        bomby += bomby_change
    collision = col(missilex, missiley, bombx, bomby)
    if collision == True:
        explosionsound.play()
        explode(bombx, bomby)
        explode(bombx + 25, bomby)
        explode(bombx + 50, bomby)
        explode(bombx, bomby - 50)
        bombx = planex
        bomby = planey
        missilex = playerx
        missiley = 820
        score_value += 1
        missile_state = 'ready'

    if bomby >= 820:
        explosionsound.play()
        firex = bombx + 50
        health_value -= health_change
        firechk = True
        bomby = planey
        bombx = planex
        bomb_state = 'not ready'
    if firechk == True:
        fire(firex, firey)
    if missiley <= 0:
        missiley = 820
        missile_state = 'ready'
    if missile_state == 'fire':
        missile(missilex, missiley)
        missiley -= missiley_change

    if health_value == 0:
        heliy = 2000
        jeepy = 2000
        planey = 2000
        base1y = 2000
        base2y = 2000
        base3y = 2000
        playery = 2000
        firey = 2000
        bomby = -1000
        gameover()
    health(healthx, healthy)
    scoring(scorex, scorey)



    pygame.display.update()


