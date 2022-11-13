import pygame
import sys
from util import *
from constants import *
from FaceVideoProcessor import VideoProcessor
from collections import deque
from facepong import Pong

states = {'menu': 0, 'pong':1, 'exit': 2}


class Game():
    def __init__(self) -> None:
        pygame.init()
        self.state = 0

        self.clock = pygame.time.Clock()

        self.game_screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Push Pong')


    
    def run(self):
        while self.state != states['exit']:
            if self.state == states["menu"]:
                self.run_menu()
            elif self.state == states['pong']:
                print('hi')
                self.run_pong()
            else:
                self.quit_game()

    def create_buttons(self):
        play_button = Button("Play", 100, 100, 200, 50, color=WHITE)
        exit_button = Button("Exit", 100, 300, 200, 50, color=WHITE)

        return [play_button, exit_button]

    def run_menu(self):
        menu_surface = pygame.Surface((WIDTH, HEIGHT))

        buttons = self.create_buttons()
        while self.state == states['menu']:
            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.state == states["exit"]
                elif pygame.mouse.get_pressed()[0] == 1:
                
                    for button in buttons:
                        if button.check_if_clicked(mouse_pos):
                            if button.text == "Play":
                                self.state = states['pong']
                            elif button.text == "Exit":
                                self.state = states['exit']

            for button in buttons:
                button.update(mouse_pos)
                button.draw(menu_surface)

            self.game_screen.fill(BLACK)
            self.game_screen.blit(menu_surface, (0,0))
            pygame.display.update()
            self.clock.tick(60)
        
   
    def run_pong(self):
        game_surface = pygame.Surface((WIDTH, HEIGHT))
        
        pong = Pong(game_surface)

        while self.state == states['pong']:
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pong.vp.close()
                    self.state == states["exit"]
                


            pong.update_game_state()
            pong.draw_game_surface()


            self.game_screen.fill(BLACK)
            self.game_screen.blit(game_surface, (0,0))

            pygame.display.update()
            self.clock.tick(60)

    def quit_game(self):
        pygame.quit()
        sys.exit()


if __name__ == '__main__':
    game = Game()
    game.run()
