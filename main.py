# Pygame recreation in pygame with extra features

#imports
from board import boards #import tilemaps from board file
import pygame
import math

pygame.init()

#Window options
WIDTH = 900
HEIGHT = 950 # 50 extra pixels, so that  there is space for amount of coins & lives.
fps = 60
pygame.display.set_caption('Pacman - Version 1')
font = pygame.font.Font('freesansbold.ttf', 20) # set font
screen = pygame.display.set_mode([WIDTH, HEIGHT]) # set screen size
timer = pygame.time.Clock()
PI = math.pi # sets pi as a variable, so that it can be easily called in future without having to use math.pi

colour = 'blue' #colour for all of the tilemap shapes. (excl powerups & coins.)

player_images = []
for i in range(1,5):
    player_images.append(pygame.transform.scale(pygame.image.load(f'assets/player_images/{i}.png'), (45,45)))
player_x = 450 # Player starting position x
player_y = 663# Player starting position y
direction = 0 # Player starting direction (right)
counter = 0
flicker = False # flicker for powerup tiles


#function for drawing the player sprite

def drawPlayer():
    if direction == 0:
        screen.blit(player_images[counter // 5], (player_x, player_y)) # RIGHT
    elif direction == 1:
        screen.blit(pygame.transform.flip(player_images[counter // 5], True, False), (player_x, player_y)) # LEFT
    elif direction == 2:
        screen.blit(pygame.transform.rotate(player_images[counter // 5], 90), (player_x, player_y)) # UP
    elif direction == 3:
        screen.blit(pygame.transform.rotate(player_images[counter // 5], 270), (player_x, player_y)) # DOWN



#function for drawing the tilemap board

level = boards

def drawBoard():
    num1 = ((HEIGHT - 50) // 32) #to leave space for the score & number of lives remaining.
    num2 = (WIDTH // 30)
    # the two above are using floor division, so that the output will always be an integer
    for i in range(len(level)):
        for j in range(len(level[i])):
            if level[i][j] == 1:
                pygame.draw.circle(screen, 'white', (j * num2 + (0.5*num2), i * num1 + (0.5*num1)), 4) #draw small circles (coins)
            if level[i][j] == 2 and not flicker:
                pygame.draw.circle(screen, 'gold', (j * num2 + (0.5*num2), i * num1 + (0.5*num1)), 10) #draw large circles (powerups)
            if level[i][j] == 3:
                pygame.draw.line(screen, colour, (j * num2 + (0.5*num2), i * num1), (j * num2 + (0.5*num2), i * num1 + num1), 3) # draw vertical walls
            if level[i][j] == 4:
                pygame.draw.line(screen, colour, (j * num2 , i * num1 + (0.5*num1)), (j * num2 + num2, i * num1 + (0.5*num1)), 3) # draw horizontal walls
            if level[i][j] == 5:
                pygame.draw.arc(screen, colour, [(j*num2 - (num2*0.4)) - 2, (i * num1 + (0.5*num1)), num2, num1], 0, PI/2, 3) # draw curve for corners
            if level[i][j] == 6:
                pygame.draw.arc(screen, colour, [(j*num2 + (num2*0.5)), (i * num1 + (0.5*num1)), num2, num1], PI/2, PI, 3) # draw curve for corners
            if level[i][j] == 7:
                pygame.draw.arc(screen, colour, [(j * num2 + (num2 * 0.5)), (i * num1 - (0.4 * num1)), num2, num1], PI, 3 * PI / 2, 3) # draw curve for corners
            if level[i][j] == 8:
                pygame.draw.arc(screen, colour, [(j * num2 - (num2 * 0.4)) - 2, (i * num1 - (0.4 * num1)), num2, num1], 3 * PI / 2, 2 * PI, 3) # draw curve for corners
            if level[i][j] == 9:
                pygame.draw.line(screen, 'white', (j * num2 , i * num1 + (0.5*num1)), (j * num2 + num2, i * num1 + (0.5*num1)), 3) # draw horizontal walls (ghost area gate)


#game loop
run = True
while run:
    timer.tick(fps)
    if counter < 19:
        counter += 1
        if counter > 3:
            flicker = False
        
    else:
        counter = 0
        flicker = True

    screen.fill('black')
    drawBoard()
    drawPlayer()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:    #Register direction changes with arrow keys
            if event.key == pygame.K_RIGHT:
                direction = 0
            if event.key == pygame.K_LEFT:
                direction = 1
            if event.key == pygame.K_UP:
                direction = 2
            if event.key == pygame.K_DOWN:
                direction = 3

    pygame.display.flip()
pygame.quit()
