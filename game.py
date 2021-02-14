import pygame
import random
import math
import sys
from pygame import mixer

#initializing pygame
pygame.init()

fpsClock=pygame.time.Clock()

#main screen
screen=pygame.display.set_mode((800,600))

#variable
run=True

#score
score_val=0
font=pygame.font.Font('ArcaMajora3-Bold.otf',32)
textX=10
textY=10

#gameover
game_font=pygame.font.Font('ArcaMajora3-Bold.otf',64)


#main windows
pygame.display.set_caption("GAME")
icon=pygame.image.load("joystick.png")
pygame.display.set_icon(icon)

#player
playerimg=pygame.image.load('space-invaders.png')
playerX=370
playerY=480
playerXchg=0

#enemy
enemyimg=[]
enemyimg=[]
enemyX=[]
enemyY=[]
enemyXchg=[]
enemyYchg=[]

num=6

for i in range(num):
    enemyimg.append(pygame.image.load('cartoon.png'))
    enemyX.append(random.randint(0,736))
    enemyY.append(random.randint(50,150))
    enemyXchg.append(4)
    enemyYchg.append(40)


#bullet
bulletimg=pygame.image.load('bullet.png')
bulletX=0
bulletY=480
bulletYchg=10
bullet_state="ready"

#sound back
mixer.music.load('background.wav')
mixer.music.play(-1)
mixer.music.set_volume(0.3)

#ploting function
def player(x,y):
    screen.blit(playerimg, (x,y))

def enemy(x,y,i):
    screen.blit(enemyimg[i], (x,y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletimg,(x+16,y+10))


def showscore(x,y):
    score=font.render("Score: "+str(score_val),True,(255,255,255))
    screen.blit(score,(x,y))

def game_over():
    game_text=game_font.render("GAME OVER",True,(255,255,255))
    screen.blit(game_text,(200,250))



#collison func

def col(enemyX,enemyY,bulletX,bulletY):
    dist=math.sqrt(math.pow(enemyX-bulletX,2)+math.pow(enemyY-bulletY,2))
    if dist<27:
        return True
    else:
        return False

#main loop
while run:

    #color fill
    background=pygame.image.load('back.png')
    screen.blit(background,(0,0))
 

    #main func
    for event in pygame.event.get():
        if event.type ==pygame.QUIT:
            run=False

        #controls
        if event.type==pygame.KEYDOWN:
            if event.key  == pygame.K_a or event.key  == pygame.K_LEFT:
                playerXchg=-8
                
            if event.key  == pygame.K_d or event.key  == pygame.K_RIGHT:
                playerXchg=8
            if event.key ==pygame.K_SPACE:
                if bullet_state is "ready":
                    bulletX=playerX
                    fire_bullet(bulletX,bulletY)
                    bullet_sound=mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bullet_sound.set_volume(0.3)

        if event.type==pygame.KEYUP:
            if event.key  == pygame.K_a or event.key  == pygame.K_LEFT or pygame.K_d or event.key  == pygame.K_RIGHT:   
                playerXchg=0
            
    #player coordinates
    playerX +=playerXchg
    if playerX <=0:
        playerX=0
    elif playerX>=736:
        playerX=736

    #enemy change
    for i in range(num):

        #game over
        if enemyY[i] >440:
            for j in range(num):
                enemyY[j]=2000
            game_over()
            break

        #Enemy movement


        enemyX[i] += enemyXchg[i]
        if enemyX[i] <=0:
            enemyXchg[i]=4
            enemyY[i]+=enemyYchg[i]
        elif enemyX[i]>=736:
            enemyXchg[i]=-4
            enemyY[i]+=enemyYchg[i]
    
        #collison
        coll=col(enemyX[i],enemyY[i],bulletX,bulletY)
        if coll:
            bulletY=480
            bullet_state ="ready"
            score_val +=1
            col_sound=mixer.Sound('explosion.wav')
            col_sound.play()
            col_sound.set_volume(0.3)
            enemyX[i]=random.randint(0,736)
            enemyY[i]=random.randint(50,150)
        enemy(enemyX[i],enemyY[i] ,i)


    player(playerX,playerY)

    #bullet fire
    if bulletY<0:
        bulletY=480
        bullet_state="ready"
    
    if bullet_state is "fire":
        fire_bullet(bulletX,bulletY)
        bulletY-=bulletYchg


   


    #screen updating

    showscore(textX,textY)
    pygame.display.update()
    fpsClock.tick(60)