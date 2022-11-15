import pygame
from time import time, sleep

pygame.init()

start_time = time()

clock = pygame.time.Clock()

count = 0
while True:
    cur_time = time()
    # print(cur_time - start_time)
    # sleep(3)
    count +=1
    if (cur_time - start_time) >= 1:
        break

    
    clock.tick(60)

print(f'We looped {count} timees')