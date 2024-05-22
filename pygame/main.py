import pygame
import random
import math
from pygame import mixer

pygame.init()
    #Initalizes the pygame

screen = pygame.display.set_mode((800, 600))
    #creates the screen, width is 800px and height is 600px

background = pygame.image.load("artwork-colorful-universe.jpg")
background_1 = pygame.transform.scale(background, (800, 600))
    #scales the background image to 800px by 600px

mixer.music.load("background.wav")
    #loads the background music
mixer.music.play(-1)
    #plays the music, the value is "-1" because that is how you make it loop forever



pygame.display.set_caption("Space Invaders")
    #creates a title for the application
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)
    #creates a icon



score_value = 0
font = pygame.font.Font("freesansbold.ttf", 32)
    #inside of "Font" is type of font and size of font, you can also add other fonts by downloading it from "DaFont" and putting it in the projects folder

textX = 10
testY = 10
    #cordinates for where our font would appear

def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
        #renders the text and inside of "render" is the text, antialias (just put True), and color
    screen.blit(score, (x, y)) 
        #draws the score on the screen to (10, 10)



over_font = pygame.font.Font("freesansbold.ttf", 64)

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
        #renders the over_text and inside of "render" is the text, antialias (just put True), and color
    screen.blit(over_text, (200, 250))


playerImg = pygame.image.load ("player.png")
playerX = 370
playerY = 480
playerX_change = 0

def player(x, y):
    player = pygame.transform.scale(playerImg, (64, 64))
        #scale the image to 64px by 64px
    screen.blit(player, (x, y)) 
        #draws player.png to (370, 480)



enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
    #the arrays above are going to be inputed by data, when all 6 enemies are added
num_of_enemies = 6


for i in range(num_of_enemies):
    #for each i in this case 6, in num_of_enemies do the code below
    enemyImg.append(pygame.image.load ("enemy.png"))
    enemyX.append(random.randint(0, 735))
    #makes x random between 0 and 800
    enemyY.append(random.randint(50, 150))
    #makes y random between 50 and 150
    enemyX_change.append(random.choice([0.3, -0.3]))
    #makes enemyX_change random between 2 choices "0.3" or "-0.3"
    enemyY_change.append(40)

def enemy(x, y, i):
    enemy = pygame.transform.scale(enemyImg[i], (64, 64))
        #scale the image to 64px by 64px
    screen.blit(enemy, (x, y)) 
        #draws enemy.png to ()



bulletImg = pygame.image.load ("bullet.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 1
bullet_state = "ready"
    #"bullet_state" is used to make the bullet disapear

def fire_bullet(x, y):
    global bullet_state
        #"global" allows to use a variable outside the function
    bullet_state = "fire"
        #this activates the if bullet_state = "fire"
    screen.blit(bulletImg,(x + 16, y + 10))
        #"+ 16" and "+ 10" allows it to be in the center of the spaceship



def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt ((math.pow(enemyX-bulletX, 2)) + (math.pow(enemyY-bulletY, 2)))
        #using distance between 2 objects formula
    if distance < 27:
        #"27" was the number that was found through trial and testinging
        return True
    else:
        return False



running = True
while running:

    screen.fill((0, 0, 0))
        #based on RGB (Red, Green, and Blue)
    
    screen.blit(background_1, (0,0))

    for event in pygame.event.get():
        #loops the events in python
        if event.type == pygame.QUIT:
            #if the event is equal to pygame.quit which is the x button to close an application, it will do the code below
            running = False
        if event.type == pygame.KEYDOWN:
            #if a key is pressed
            if event.key == pygame.K_a:
                playerX_change = -0.3
            if event.key == pygame.K_d:
                playerX_change = 0.3
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    #this allows it so when you press space multiple times the bulletX won't change
                    bullet_Sound = mixer.Sound("laser.wav")
                    bullet_Sound.play()
                        #plays the bullet sound
                    bulletX = playerX
                        #saves the spaceships current position, this allows it so the bullet doesn't follow the players x cordinate
                    fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            #if a key is let go of
            if event.key == pygame.K_a or event.key == pygame.K_d:
                playerX_change = 0



    playerX += playerX_change
        #playerX is being added or subtracted based on playerX_change which changed values when a key is pressed

    if playerX <= 0:
        playerX = 0
            #makes sure that the spaceship doesn't go outside of the left side of the screen
    if playerX >= 736:
        playerX = 736
            #makes sure that the spaceship doesn't go outside of the right side of the screen
    


    for i in range(num_of_enemies):

        if enemyY[i] > 440:
            #when one of the enemies go to y 440
            for j in range (num_of_enemies):
                enemyY[j] = 2000
                    #moves each enemy out of the screen
            game_over_text()
                #shows the "Game Over" on the screen
            break
                #breaking out of the loop
        
        enemyX[i] += enemyX_change[i]
            #enemyX is being added or subtracted based on enemyX_change which changed values when a key is pressed
        if enemyX[i] <= 0:
                #makes sure that the alien doesn't go outside of the left side of the screen
            enemyX_change[i] = 0.3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
                #makes sure that the alien doesn't go outside of the right side of the screen
            enemyX_change[i] = -0.3
            enemyY[i] += enemyY_change[i]
                #there is "[i]" to be specific on which enemy value we want to change

        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_Sound = mixer.Sound("explosion.wav")
            explosion_Sound.play()
                #plays the explosion sound
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)
                #this makes the enemy respawn to it's default position
        
        enemy(enemyX[i], enemyY[i], i)
        #put it infront of the "screen.fill" because the code goes down the list

    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
            #onces the bullet touches the border, it go back to position 480 and back to the "ready" state

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change
            #makes the bullet move up, with the help of the while loop to update this if statement



    player(playerX, playerY)
        #put it infront of the "screen.fill" because the code goes down the list
    show_score(textX, testY)
        #shows the score
    pygame.display.update()
        #updates the screen, as important as pygame.init()