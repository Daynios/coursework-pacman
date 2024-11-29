# Pygame recreation in pygame with extra features
import pygame

pygame.init()

#Window options
WIDTH = 900
HEIGHT = 950
fps = 60
font = pygame.font.Font('freesansbold.ttf', 20)
screen = pygame.display.set_mode([WIDTH, HEIGHT])
timer = pygame.time.Clock()


run = True
while run:
    timer.tick(fps)
    screen.fill('black')

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.flip()
pygame.quit()