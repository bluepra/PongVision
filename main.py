# Import the pygame library and initialise the game engine
import pygame
import cv2 as cv
import time
from pong import Pong
 
pygame.init()

WIDTH, HEIGHT = 700, 500

# Open a new window
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Pong")


# MAIN LOOP
running = True
while running:

    # Screen background
    screen.fill((0, 0, 0))

    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
              running = False # Flag that we are done so we exit this loop
        elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x: #Pressing the x Key will quit the game
                    running = False
                if event.key == pygame.K_p:
                    pong = Pong()
                    pong.game_loop()
                    
    # Screen Update
    pygame.display.update()