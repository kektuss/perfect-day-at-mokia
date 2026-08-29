import pygame
from pygame.locals import *

pygame.init()

SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 720

SCREEN = pygame.display.set_mode((1080, 720))

clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()