# Making space invaders using pygame
import pygame
import random
import math
from pygame import mixer

# Initialize the pygame
pygame.init()

# Initializing mixer
mixer.pre_init(44100, -16, 1, 512)
mixer.init()

# Creating the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('background1.png').convert()

# Background sound
mixer.music.load('background.wav')
mixer.music.play(-1)

# Title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)

# Player
playerimg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyimg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 5
xchange = 0.4

for i in range(num_of_enemies):
    enemyimg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(xchange)
    enemyY_change.append(20)

# Bullet

# Ready_state = You can't see the bullet
# Fire_state = The bullet is currently being fired
bulletimg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 0.75
bullet_state = "ready"

# Bomb
bombimg = pygame.image.load('bomb.png')
bombX = 0
bombY = 10
bombX_change = 0
bombY_change = 0.75
bomb_state = "ready"

# Score
score_value = 0
font = pygame.font.SysFont('Arial', 28, False, False)
textX = 10
textY = 10

# Game over
over_font = pygame.font.SysFont('Arial', 64, False, False)

# Functions
def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (192, 192, 192))
    screen.blit(over_text, (200, 250))

def player(x, y):
    screen.blit(playerimg, (x, y))

def enemy(x, y, i):
    screen.blit(enemyimg[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletimg, (x + 16, y + 10))

def drop_bomb(x, y):
    global bomb_state
    bomb_state = "fire"
    screen.blit(bombimg, (x + 16, y + 10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.hypot(enemyX - bulletX, enemyY - bulletY)
    if distance < 27:
        return True
    else:
        return False

def bombCollision(playerX, playerY, bombX, bombY):
    bomb_distance = math.hypot(playerX - bombX, playerY - bombY)
    if bomb_distance < 27:
        return True
    else:
        return False

# Game Loop

running = True
while running:

    # Background color using RGB

    screen.fill((0, 0, 0))

    # Background image

    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # This checks which keystroke has been pressed

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                playerX_change -= 0.5

            if event.key == pygame.K_d:
                playerX_change = 0.5

            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_Sound = mixer.Sound('laser.wav')
                    bullet_Sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_d:
                playerX_change = 0

    # Checking for boundaries of spaceship

    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy movement

    for i in range(num_of_enemies):

        # Game over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
                playerY = -2000
            game_over_text()
            mixer.music.stop()
            over = mixer.Sound('over.wav')
            over.play(0)
            break

        enemyX[i] += enemyX_change[i]

        if enemyX[i] <= 0:
            enemyX_change[i] = xchange
            enemyY[i] += enemyY_change[i]

        elif enemyX[i] >= 736:
            enemyX_change[i] -= xchange
            enemyY[i] += enemyY_change[i]

        # Bullet collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)

        if collision:
            explosion_Sound = mixer.Sound('explosion.wav')
            explosion_Sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            if score_value % 2 == 0:
                xchange += 0.06
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    if score_value > 10:
        if bomb_state == "ready":
            random_enemyX = random.choice(enemyX)
            bombX = random_enemyX
            drop_bomb(bombX, bombY)

    # Bullet movement

    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # Bomb collision

    bomb_collision = bombCollision(playerX, playerY, bombX, bombY)

    if bomb_collision:
        bomb_state = "null"
        explosion_Sound.play()
        for j in range(num_of_enemies):
            enemyY[j] = 2000
            playerY = -2000
        game_over_text()
        mixer.music.stop()
        over = mixer.Sound('over.wav')
        over.play(0)

    # Bomb movement

    if bombY >= 550:
        bombY = 30
        bomb_state = "ready"

    if bomb_state == "fire":
        drop_bomb(bombX, bombY)
        bombY += bombY_change

    # Bug checking

    for i in range(num_of_enemies):
        if enemyX_change[i] < 0.4:
            xchange = 0.52

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
