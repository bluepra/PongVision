# Get parent directory
import sys
import os
from util import *
import pygame
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

# Import the pygame library and initialise the game engine
import pygame

from random import randint
from FaceVideoProcessor import VideoProcessor
from collections import deque
from statistics import mean
 
 
# Define some colors
BLACK = (0,0,0)
WHITE = (255,255,255)
SCREEN_W, SCREEN_H = 700, 500

# Define screen params
SCREEN_CENTER_X = SCREEN_W // 2
SCREEN_CENTER_Y = SCREEN_H // 2
MEAS_MAX_Y = SCREEN_H * 3 // 4
MEAS_MIN_Y = SCREEN_H // 4
# MEAS_MAX_Y = SCREEN_H * 5 // 8
# MEAS_MIN_Y = SCREEN_H *3 // 8

# Sampling window size
SAMPLE_WINDOW_SIZE = 4

# Ball velocity multiplier
VELOCITY_MULT = 1

# Motion sensitivity multiplier
VERT_MULT = 2

# Win condition
WIN_CONDITION = 1

class Pong():

    def __init__(self, surface):
        # Start video capture
        self.vp = VideoProcessor()

        self.clock = pygame.time.Clock()

        # Open a new window
        self.size = (SCREEN_W, SCREEN_H)
        self.surface = surface

        self.paddleA = Paddle(RED, 10, 100)
        self.paddleA.rect.x = 5
        self.paddleA.rect.y = 200

        self.paddleB = Paddle(BLUE, 10, 100)
        self.paddleB.rect.x = SCREEN_W - 15
        self.paddleB.rect.y = 200

        self.ball = Ball(WHITE,20,20)
        self.ball.rect.x = SCREEN_CENTER_X - (self.ball.width // 2)
        self.ball.rect.y = SCREEN_CENTER_Y - (self.ball.height // 2)

        #This will be a list that will contain all the sprites we intend to use in our game.
        self.all_sprites_list = pygame.sprite.Group()

        # Add the paddles and the ball to the list of sprites
        self.all_sprites_list.add(self.paddleA)
        self.all_sprites_list.add(self.paddleB)
        self.all_sprites_list.add(self.ball)

        # The loop will carry on until the user exits the game (e.g. clicks the close button).
        self.carryOn = True

        # Intialize cooldown logic
        self.last = pygame.time.get_ticks()
        self.cooldown_ticks = 2000
        self.cooldown = True

        # Intialize sampling window
        self.samplesA = deque()
        self.samplesB = deque()
        self.window_size = SAMPLE_WINDOW_SIZE

        #Initialise player scores
        self.scoreA = 0
        self.scoreB = 0

        # Intialize player turns
        self.kick_left = False

        # Intialize win conditions
        self.A_won = False
        self.B_won = False

        # Intialize pause
        self.pause = True
    
    # -------- Main Game Loop -----------
    def update_game_state(self):

        # Check for a winner
        if self.scoreA >= WIN_CONDITION:
            self.A_won = True
            return
        elif self.scoreB >= WIN_CONDITION:
            self.B_won = True
            return


        # Get the player y-coords from the VideoProcessor
        a = self.vp.get_Y_coords(show_video=True)
        if self.pause: return
        if a is None:
            print('A is None')
        playerA_y, playerB_y = a

        # Smooth coord values
        if playerA_y:
            self.samplesA.append(playerA_y)
        if playerB_y:
            self.samplesB.append(playerB_y)
        if len(self.samplesA) > self.window_size:
            self.samplesA.popleft()
        if len(self.samplesB) > self.window_size:
            self.samplesB.popleft()

        # Update paddle positions
        if playerA_y:
            self.paddleA.rect.y = self.scale_ycoord(mean(self.samplesA))
        if playerB_y:
            self.paddleB.rect.y = self.scale_ycoord(mean(self.samplesB))

        # --- Game logic should go here
        self.all_sprites_list.update()
        
        #Check if the ball is bouncing against any of the 4 walls:
        # Right wall
        if self.ball.rect.x>=SCREEN_W - 10:
            self.scoreA+=1
            self.ball.velocity[0] = -self.ball.velocity[0]
            self.play_sound(start_sound)
            self.new_round()
        # Left wall
        if self.ball.rect.x<=0:
            self.scoreB+=1
            self.ball.velocity[0] = -self.ball.velocity[0]
            self.play_sound(start_sound)
            self.new_round()
        # Bottom wall
        if self.ball.rect.y>SCREEN_H - 10:
            self.play_sound(paddle_hit_sound, volume = .25)
            self.ball.velocity[1] = -self.ball.velocity[1]
        # Top wall
        if self.ball.rect.y<0:
            self.play_sound(paddle_hit_sound, volume = .25)
            self.ball.velocity[1] = -self.ball.velocity[1]
        # Behind paddleA
        if self.paddleA.rect.y < self.ball.rect.x and self.paddleA.rect.y + self.paddleA.height:
            if self.ball.rect.x < self.paddleA.rect.x:
                self.play_sound(paddle_hit_sound)
                self.ball.velocity[1] = -self.ball.velocity[1]
        # Behind paddleB
        if self.paddleB.rect.y < self.ball.rect.x and self.paddleB.rect.y + self.paddleA.height:
            if self.ball.rect.x > self.paddleB.rect.x:
                self.play_sound(paddle_hit_sound)
                self.ball.velocity[1] = -self.ball.velocity[1]
             

        #Detect collisions between the ball and the paddles
        if pygame.sprite.collide_mask(self.ball, self.paddleA) or pygame.sprite.collide_mask(self.ball, self.paddleB):
            self.play_sound(paddle_hit_sound, volume = .25)
            self.ball.bounce()

        # Check if starting round
        if (not self.pause and self.cooldown and self.cooldown_ticks < 0):
            # Start the ball with a new velocity
            if (self.kick_left):
                self.ball.velocity = [VELOCITY_MULT*-randint(4,8),VELOCITY_MULT*randint(-8,8)]
                self.kick_left = False
            else:
                self.ball.velocity = [VELOCITY_MULT*randint(4,8),VELOCITY_MULT*randint(-8,8)]
                self.kick_left = True
            self.cooldown = False
        else:
            # We need to wait some more time, decrement cooldown clock
            now = pygame.time.get_ticks()
            self.cooldown_ticks -= (now - self.last)
            self.last = now

    def play_sound(self, sound, volume=1):
        sound.set_volume(volume)
        sound.play(maxtime=2000)
        
    def draw_game_surface(self, background):
        # First, clear the screen to black. 
        self.surface.blit(background, (0,0))
        #Draw the net
        # pygame.draw.line(self.surface, WHITE, [349, 0], [349, 500], 5)
        
        #Now let's draw all the sprites in one go. (For now we only have 2 sprites!)
        self.all_sprites_list.draw(self.surface) 

        #Display scores:
        font = pygame.font.Font(score_font, 74)
        text = font.render(str(self.scoreA), 1, WHITE)
        self.surface.blit(text, (250,10))
        text = font.render(str(self.scoreB), 1, WHITE)
        self.surface.blit(text, (420,10))
    
    def new_round(self):
        # Move ball to center
        self.ball.rect.x = SCREEN_CENTER_X - (self.ball.width // 2)
        self.ball.rect.y = SCREEN_CENTER_Y - (self.ball.height // 2)
        # Kill velocity
        self.ball.velocity = [0,0]
        # Start game countdown
        self.last = pygame.time.get_ticks()
        self.cooldown_ticks = 500  
        self.cooldown = True


    def scale_ycoord(self, ycoord: int):
        scaled = (ycoord-MEAS_MIN_Y)*(SCREEN_H / (MEAS_MAX_Y - MEAS_MIN_Y))
        if scaled < 0:
            return 0
        elif scaled > SCREEN_H-self.paddleA.height:
            return SCREEN_H-self.paddleA.height
        else:
            return scaled
    

# # Main program
# def main():
#     # Initialize game
#     pong = Pong()
#     # Kick off main game loop
#     pong.game_loop()
#     #Once we have exited the main program loop we can stop the game engine:
#     pygame.quit()

# if __name__ == "__main__":
#     main()
