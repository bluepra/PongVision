import pygame
import sys
import os
from util import *
from constants import *
from FaceVideoProcessor import VideoProcessor
from collections import deque
from facepong import Pong

states = {'menu': 0, 'pong':1, 'exit': 2, 'game-over': 3}


class Game():
    def __init__(self) -> None:
        pygame.init()
        self.state = 0

        self.clock = pygame.time.Clock()

        # Create pygame window
        os.environ['SDL_VIDEO_WINDOW_POS'] = '%d,%d' % PYGAME_WINDOW
        self.game_screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Push Pong')
        

        self.winner = None

        # Game music
        music = pygame.mixer.Sound(background_music)
        music.set_volume(.1)
        music.play(-1)

        

    def run(self):
        while self.state != states['exit']:
            if self.state == states["menu"]:
                self.run_menu()
            elif self.state == states['pong']:
                print('hi')
                self.run_pong()
            elif self.state == states['game-over']:
                self.run_game_over()
            else:
                self.quit_game()

    def create_menu_buttons(self):
        # play_img = pygame.transform.scale(pygame.image.load('assets/play.png'), (50,50))
        play_button = Button("(Play)", 460, 170, 175, 60, background_color=BLACK, text_color=GRAY, fontsize=40)
        exit_button = Button("(Exit )", 460, 250, 150, 60, background_color=BLACK, text_color=GRAY, fontsize=40)

        return [play_button, exit_button]

    def run_menu(self):
        menu_surface = pygame.Surface((WIDTH, HEIGHT))
        back_img = pygame.image.load(menu_background_img)
        back_img = pygame.transform.scale(back_img, (WIDTH, HEIGHT))

        top_title = TextBox('PONG', 25, 170, 450, 250, (9,9,9), text_color=WHITE, font_size=80, font=title_font_top)
        bottom_title = TextBox('VISION', 25, 230, 400, 250, (9,9,9), text_color=GRAY, font_size=54, font=title_font_bottom)

        buttons = self.create_menu_buttons()
        while self.state == states['menu']:
            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type is pygame.QUIT:
                    self.state = states["exit"]
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self.state = states["exit"]
                elif pygame.mouse.get_pressed()[0] == 1:
                
                    for button in buttons:
                        if button.check_if_clicked(mouse_pos):
                            if button.text == "(Play)":
                                self.state = states['pong']
                            elif button.text == "(Exit )":
                                self.state = states['exit']
            

            menu_surface.blit(back_img, (0,0))
            top_title.draw(menu_surface)
            bottom_title.draw(menu_surface)
            for button in buttons:
                button.update(mouse_pos)
                button.draw(menu_surface)

            self.game_screen.fill(BLACK)
            self.game_screen.blit(menu_surface, (0,0))
            pygame.display.update()
            self.clock.tick(60)
        
   
    def run_pong(self):
        game_surface = pygame.Surface((WIDTH, HEIGHT))
        background = pygame.image.load(game_background_img)
        background = pygame.transform.scale(background, (WIDTH, HEIGHT))

        pong = Pong(game_surface)
        pong.pause = True

        # Keep updating the game while we're not in a win state or exit state
        while self.state == states['pong'] and not (pong.A_won or pong.B_won):
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pong.vp.close()
                    self.state = states["exit"]
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pong.vp.close()
                        self.state = states["exit"]
                    elif event.key == pygame.K_SPACE:
                        pong.pause = not pong.pause

                

            # pong.refresh_surface(background)
            pong.update_game_state()
            pong.draw_game_surface(background)

            # Put some text on the game surface
            if pong.pause:
                message_surface = pygame.Surface((500,50))
                message_surface.fill(BLACK)
                font = pygame.font.Font(score_font, 50)
                text = font.render("Hit Space to Play", 1, GRAY)
                message_surface.blit(text, (0,0))
                game_surface.blit(message_surface, (120,220))

            self.game_screen.fill(BLACK)
            self.game_screen.blit(game_surface, (0,0))

            pygame.display.update()
            self.clock.tick(60)
        
        if pong.A_won:
            self.winner = 'Left'
        if pong.B_won:
            self.winner = 'Right'
        
        self.state = states['game-over']
        pong.vp.close()
        

    def get_winner_message(self):
        winner_surface = pygame.Surface((800,100))
        winner_surface.fill(BLACK)
        font = pygame.font.Font(score_font, 100)
        color = RED if self.winner == "Left" else BLUE
        text = font.render(self.winner + " Wins!", 1, color)
        winner_surface.blit(text, (0,0))
        return winner_surface

    def run_game_over(self):
        game_over_surface = pygame.Surface((WIDTH, HEIGHT))
        back_to_menu = Button('(Back to Menu)', 160,220,400,100,background_color=BLACK, text_color=GRAY, hover_color=WHITE, fontsize=50)
        # Keep updating the game while we're not in a win state or exit state
        while self.state == states['game-over']:
            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type is pygame.QUIT:
                    self.state = states["exit"]
                elif pygame.mouse.get_pressed()[0] == 1:
                    if back_to_menu.check_if_clicked(mouse_pos):
                        self.winner = None
                        self.state = states['menu']
            
            if self.winner:
                
                winner_surface = self.get_winner_message()
                pos = (70,100) if self.winner == 'Left' else (40,100)
                game_over_surface.blit(winner_surface,pos)

            back_to_menu.update(mouse_pos)
            back_to_menu.draw(game_over_surface)
            
            self.game_screen.fill(BLACK)
            
            self.game_screen.blit(game_over_surface, (0,0))

            pygame.display.update()
            self.clock.tick(60)

    def quit_game(self):
        pygame.quit()
        sys.exit()


if __name__ == '__main__':
    game = Game()
    game.run()
