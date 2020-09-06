import pygame
import RPi.GPIO as GPIO
from pygame import mixer
import random
import time
import math


GPIO.setmode(GPIO.BCM)

x1 = 2
x2 = 3
x3 = 4
x4 = 17
x5 = 18
x6 = 27
x7 = 22
x8 = 23

y1 = 10
y2 = 9
y3 = 11
y4 = 25
y5 = 5
y6 = 6
y7 = 13
y8 = 19

x = [x1,x2,x3,x4,x5,x6,x7,x8]
y = [y1,y2,y3,y4,y5,y6,y7,y8]

GPIO.setup(x1,GPIO.OUT)
GPIO.setup(x2,GPIO.OUT)
GPIO.setup(x3,GPIO.OUT)
GPIO.setup(x4,GPIO.OUT)
GPIO.setup(x5,GPIO.OUT)
GPIO.setup(x6,GPIO.OUT)
GPIO.setup(x7,GPIO.OUT)
GPIO.setup(x8,GPIO.OUT)

GPIO.setup(y1,GPIO.OUT)
GPIO.setup(y2,GPIO.OUT)
GPIO.setup(y3,GPIO.OUT)
GPIO.setup(y4,GPIO.OUT)
GPIO.setup(y5,GPIO.OUT)
GPIO.setup(y6,GPIO.OUT)
GPIO.setup(y7,GPIO.OUT)
GPIO.setup(y8,GPIO.OUT)

power = 2 ** 8
wait = 1 / power

# Initialize pygame
pygame.init()


def led_board_setup():
    for i in range(8):
        GPIO.output(y[i],False)
        GPIO.output(x[i],True)
   


def snake_on_board():
    # for the apple
    #apple_row = appleX // 20
    #apple_column = appleY // 20
    #GPIO.output(y[apple_row],False)
    #GPIO.output(x[apple_column], True)
    #time.sleep(wait)
    #GPIO.output(y[apple_row],True)
    #GPIO.output(x[apple_column], False)

    SNAKE_ROW_LIST = [SNAKE_COORDINATES_X[i] // 20 for i in range(SNAKE_LENGTH)]
    SNAKE_COLUMN_LIST = [SNAKE_COORDINATES_Y[i] // 20 for i in range(SNAKE_LENGTH)]

    # for the snake
    for i in range(SNAKE_LENGTH):
        if SNAKE_ROW_LIST[i] > 7 or SNAKE_ROW_LIST[i] < 0 or SNAKE_COLUMN_LIST[i] > 7 or SNAKE_COLUMN_LIST[i] < 0:
            continue
        GPIO.output(y[SNAKE_ROW_LIST[i]],True)
        GPIO.output(x[SNAKE_COLUMN_LIST[i]],False)
        time.sleep(wait)
        GPIO.output(y[SNAKE_ROW_LIST[i]],False)
        GPIO.output(x[SNAKE_COLUMN_LIST[i]],True)




# If snake goes out of boundary then get it back in the screen from the other side
def reappear():
   
    if SNAKE_COORDINATES_X[0] >= WIDTH:
        for i in range(SNAKE_LENGTH - 1, 0, -1):
            SNAKE_COORDINATES_X[i] = SNAKE_COORDINATES_X[i - 1]
            SNAKE_COORDINATES_Y[i] = SNAKE_COORDINATES_Y[i - 1]
        SNAKE_COORDINATES_X[0] = 0
    if SNAKE_COORDINATES_X[0] < 0:
        for i in range(SNAKE_LENGTH - 1, 0, -1):
            SNAKE_COORDINATES_X[i] = SNAKE_COORDINATES_X[i - 1]
            SNAKE_COORDINATES_Y[i] = SNAKE_COORDINATES_Y[i - 1]
        SNAKE_COORDINATES_X[0] = WIDTH
    if SNAKE_COORDINATES_Y[0] >= HEIGHT:
        for i in range(SNAKE_LENGTH - 1, 0, -1):
            SNAKE_COORDINATES_X[i] = SNAKE_COORDINATES_X[i - 1]
            SNAKE_COORDINATES_Y[i] = SNAKE_COORDINATES_Y[i - 1]
        SNAKE_COORDINATES_Y[0] = 0
    if SNAKE_COORDINATES_Y[0] < 0:
        for i in range(SNAKE_LENGTH - 1, 0, -1):
            SNAKE_COORDINATES_X[i] = SNAKE_COORDINATES_X[i - 1]
            SNAKE_COORDINATES_Y[i] = SNAKE_COORDINATES_Y[i - 1]
        SNAKE_COORDINATES_Y[0] = HEIGHT




# Draw the apple at a random place
def draw_apple():
    # Draw the apple
    screen.blit(appleImg, (appleX, appleY))


# Drawing the snake
def draw_snake():
    pygame.draw.rect(screen, SNAKE_COLOR, (SNAKE_COORDINATES_X[0], SNAKE_COORDINATES_Y[0], SNAKE_WIDTH, SNAKE_WIDTH))
    center1 = (SNAKE_COORDINATES_X[0] + 7, SNAKE_COORDINATES_Y[0] + 6)
    center2 = (SNAKE_COORDINATES_X[0] + 14, SNAKE_COORDINATES_Y[0] + 6)
    pygame.draw.circle(screen, SNAKE_EYE_COLOR, center1, SNAKE_EYE_RADIUS)
    pygame.draw.circle(screen, SNAKE_EYE_COLOR, center2, SNAKE_EYE_RADIUS)
    for i in range(SNAKE_LENGTH - 1):
        pygame.draw.rect(screen, SNAKE_COLOR, (SNAKE_COORDINATES_X[i + 1], SNAKE_COORDINATES_Y[i + 1], SNAKE_WIDTH, SNAKE_WIDTH))


# Snake eats the apple generate new apple
def eat_apple():
    global appleX, appleY, SNAKE_COORDINATES_X, SNAKE_COORDINATES_Y, SNAKE_LENGTH
    # dist = math.sqrt(pow((appleX - SNAKE_COORDINATES_X[0]), 2) + pow((appleY - SNAKE_COORDINATES_Y[0]), 2))
    if appleX == SNAKE_COORDINATES_X[0] and appleY == SNAKE_COORDINATES_Y[0]:
        eating_sound.play()
        appleX = random.randint(0, (WIDTH - APPLE_SIZE) / 20) * 20
        appleY = random.randint(0, (HEIGHT - APPLE_SIZE) / 20) * 20
        # Increasing  the snake length on eating the apple
        SNAKE_LENGTH += 1
        # Appending another body part
        SNAKE_COORDINATES_X.append(SNAKE_COORDINATES_X[0])
        SNAKE_COORDINATES_Y.append(SNAKE_COORDINATES_Y[0])




# Snake bites itself
def bite():
    global running, snakeX_change, snakeY_change
    for i in range(SNAKE_LENGTH - 1):
        if SNAKE_COORDINATES_X[0] == SNAKE_COORDINATES_X[i + 1] and SNAKE_COORDINATES_Y[0] == SNAKE_COORDINATES_Y[i + 1]:
            running = False
            explosion_sound.play()
            snakeX_change = 0
            snakeY_change = 0
            time.sleep(1)


def main():
    global screen, snakeX_change, snakeY_change,running

    # Game loop
    while running:

        # Displaying the screen
        screen.fill((46, 204, 113))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # If a key is pressed
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if snakeX_change == SNAKE_SPEED:
                        pass
                    else:
                        snakeX_change = -SNAKE_SPEED
                        snakeY_change = 0
                elif event.key == pygame.K_RIGHT:
                    if snakeX_change == -SNAKE_SPEED:
                        pass
                    else:
                        snakeX_change = SNAKE_SPEED
                        snakeY_change = 0
                elif event.key == pygame.K_UP:
                    if snakeY_change == SNAKE_SPEED:
                        pass
                    else:
                        snakeY_change = -SNAKE_SPEED
                        snakeX_change = 0
                elif event.key == pygame.K_DOWN:
                    if snakeY_change == -SNAKE_SPEED:
                        pass
                    else:
                        snakeY_change = SNAKE_SPEED
                        snakeX_change = 0
                                                       

               
        pygame.time.delay(60)

       

        for i in range(SNAKE_LENGTH - 1, 0, -1):
            SNAKE_COORDINATES_X[i] = SNAKE_COORDINATES_X[i - 1]
            SNAKE_COORDINATES_Y[i] = SNAKE_COORDINATES_Y[i - 1]
       
        SNAKE_COORDINATES_X[0] += snakeX_change
        SNAKE_COORDINATES_Y[0] += snakeY_change
       
        reappear()
        bite()
        eat_apple()
        draw_apple()
        draw_snake()
        snake_on_board()
        print(SNAKE_COORDINATES_X[0],SNAKE_COORDINATES_Y[0])
        print(appleX,appleY)
        clock.tick(5)
        pygame.display.update()


running = True

LED_BOARD_RATIO = 100

# Screen specifications
HEIGHT = 160
WIDTH = 160




# Snake features
SNAKE_COLOR = (211, 84, 0)
SNAKE_EYE_COLOR = (255, 255, 255)
SNAKE_EYE_RADIUS = 2
SNAKE_WIDTH = 20
SNAKE_LENGTH = 1
snakeX_initial = WIDTH // 2
snakeY_initial = HEIGHT // 2
snakeX_change = 0
snakeY_change = 0
SNAKE_SPEED = SNAKE_WIDTH
SNAKE_COORDINATES_X = [snakeX_initial]
SNAKE_COORDINATES_Y = [snakeY_initial]
SNAKE_BODY_LAG = 20



# Clock
clock =  pygame.time.Clock()

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Title and Icon
pygame.display.set_caption('Snake Warrior')
icon = pygame.image.load('pythoniconSmall.png')
pygame.display.set_icon(icon)

# Background Sound
mixer.music.load('believer-wav.wav')
mixer.music.play(-1)

# Eating sound and Explosion sound
eating_sound = mixer.Sound('apple-crunch-wav.wav')
explosion_sound = mixer.Sound('explosion-wav.wav')


# Apple
APPLE_SIZE = 20
appleImg = pygame.image.load('appleSmall.png')
appleX = WIDTH // 4
appleY = HEIGHT // 4






# Play again
def play():
    global running
    main()
    value = input("to play again press 1")
    #    for event in pygame.event.get():
    #        # If SPACE is pressed
    #        if event.type == pygame.KEYDOWN:
    #            if event.key == pygame.K_SPACE:
    if value == 1:
        running = True
        play()

if __name__ == '__main__':
    led_board_setup()
    play()
    GPIO.cleanup()