import pygame
import random
import math
from pygame import mixer

pygame.init()

screen = pygame.display.set_mode((800,600))

#title
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("001-ufo.png")
pygame.display.set_icon(icon)

# background
bg = pygame.image.load('bg1.png')


#backgound music
mixer.music.load('background.mp3')
mixer.music.play(-1)

#bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 5
bullet_state = 'ready'

#alien
alienImg = []
alienX =[]
alienY=[]
alienX_change = []
alienY_change =[]
num_of_alien = 6

for i in range(num_of_alien):
    alienImg.append(pygame.image.load("alien.png"))
    alienX.append(random.randint(0,741))
    alienY.append(random.randint(50,150))
    alienX_change.append(1)
    alienY_change.append(40)

#player
playerImg = pygame.image.load("001-arcade-game.png")
playerX = 370
playerY = 480
playerX_change=0
playerY_change=0

score_value = 0
font = pygame.font.Font('freesansbold.ttf',32)
textX =10
textY =10

over = pygame.font.Font('freesansbold.ttf',64)

def Game_over():
    end = over.render("Game Over",True,(255,200,200))
    screen.blit(end,(200,250))

def show_score(x,y):
    score = font.render("Score :" + str(score_value),True,(255,200,200))
    screen.blit(score,(x,y))

def player(x,y):
    screen.blit(playerImg,(x,y))
        
def alien(x,y):
    screen.blit(alienImg[i],(x,y))
    
def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x+16, y+20))
    
def isCollision(alienX, alienY, bulletX, bulletY):
    distance = math.sqrt(math.pow(alienX - bulletX,2)+math.pow(alienY - bulletY,2)) 
    if distance < 27:
        return True
    else:
        return False
       
    
running = True
while running:
    
    # Adding background color 
    screen.blit(bg, (0, 0))
    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # move right or left
        if event.type == pygame.KEYDOWN:
           
            if event.key == pygame.K_LEFT:
                print("left arrow is pressed")
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                print("right arrow is pressed")
                playerX_change = 5
            #move bullet 
            if event.key == pygame.K_SPACE:
                bullet_sound = mixer.Sound('laser.wav')
                bullet_sound.play()
                print("Space arrow is pressed")
                if bullet_state == "ready":
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                print("key arrow is released")
                playerX_change = 0
                
                
    if bulletY <=0:
        bulletY = 480
        bullet_state = "ready"   
                 
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change
        
    #checking boundariees of spaceship    
    playerX += playerX_change
    if playerX >= 740:
        playerX = 740
    elif playerX <= 0:
        playerX =0

    # Alien movement  
    for i in range(num_of_alien):  
        #Game over
        if alienY[i] > 300:
            for j in range (num_of_alien):
                alienY[j] = 2000
            Game_over()
            break
                
        alienX[i] += alienX_change[i]       
        if alienX[i] >= 740:
            alienX_change[i] = -3
            alienY[i] += alienY_change[i]
        elif alienX[i] <= 0:
            alienX_change[i] =3
            alienY[i] += alienY_change[i]
    
        # collision
        collision = isCollision(alienX[i],alienY[i],bulletX, bulletY)
        if collision == True:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            print(score_value)
            alienX[i] = random.randint(0,741)
            alienY[i] = random.randint(50,150)
        alien(alienX[i],alienY[i])
    
    show_score(textX,textY)    
    player(playerX, playerY)
    pygame.display.update()
    

 
