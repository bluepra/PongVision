import pygame
from time import time, sleep
import sys

pygame.init()

screen = pygame.display.set_mode((1000,700))

class Ball:
    def __init__(self) -> None:
        self.image = pygame.image.load('/Users/prannav/Coding/CheeseHacks/CheeseHacks_2022/tennis_ball.jpeg')
        
        self.rect = self.image.get_rect()
        print('image width and height', self.rect.width, self.rect.height)
        self.rect.topleft = (100,100)

    def update(self, mouse_pos):
        print(self.rect.topleft)
        
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)

done = False
ball = Ball()

clock = pygame.time.Clock()

def quit_handler():
    pygame.quit()
    sys.exit()

while not done:
    game_surface = pygame.Surface((1000,700))


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                quit_handler()

    ball.update(pygame.mouse.get_pos())
    ball.draw(game_surface)

    screen.blit(game_surface, (0,0))
    pygame.display.update()

    clock.tick(60)

quit_handler()

