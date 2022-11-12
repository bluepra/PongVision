# Import the pygame library and initialise the game engine
import pygame
from paddle import Paddle
from ball import Ball
from random import randint
import methods
from VideoProcessor import VideoProcessor
 
 
# Define some colors
BLACK = (0,0,0)
WHITE = (255,255,255)
WIDTH, HEIGHT = 700, 500

# Define screen params
SCREEN_CENTER_X = WIDTH / 2
SCREEN_CENTER_Y = HEIGHT / 2

class Pong():

    def __init__(self):
        # Start pygame engine
        pygame.init()

        # Start video capture
        self.vp = VideoProcessor()

        # Open a new window
        self.size = (WIDTH, HEIGHT)
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption("Pong")

        self.paddleA = Paddle(WHITE, 10, 100)
        self.paddleA.rect.x = 5
        self.paddleA.rect.y = 200

        self.paddleB = Paddle(WHITE, 10, 100)
        self.paddleB.rect.x = WIDTH - 15
        self.paddleB.rect.y = 200

        self.ball = Ball(WHITE,10,10)
        self.ball.rect.x = SCREEN_CENTER_X
        self.ball.rect.y = SCREEN_CENTER_Y

        #This will be a list that will contain all the sprites we intend to use in our game.
        self.all_sprites_list = pygame.sprite.Group()

        # Add the paddles and the ball to the list of sprites
        self.all_sprites_list.add(self.paddleA)
        self.all_sprites_list.add(self.paddleB)
        self.all_sprites_list.add(self.ball)

        # The loop will carry on until the user exits the game (e.g. clicks the close button).
        self.carryOn = True

        # The clock will be used to control how fast the screen updates
        self.clock = pygame.time.Clock()

        # Intialize cooldown logic
        self.last = pygame.time.get_ticks()
        self.cooldown_ticks = 0
        self.cooldown = False

        #Initialise player scores
        self.scoreA = 0
        self.scoreB = 0

        # Intialize player turns
        self.kick_left = False

    # -------- Main Game Loop -----------
    def game_loop(self):
        while self.carryOn:
            # --- Main event loop
            for event in pygame.event.get(): # User did something
                if event.type == pygame.QUIT: # If user clicked close
                    self.carryOn = False # Flag that we are done so we exit this loop
                elif event.type==pygame.KEYDOWN:
                        if event.key==pygame.K_x: #Pressing the x Key will quit the game
                            self.carryOn=False

            # Get the player y-coords from the VideoProcessor
            playerA_y, playerB_y = self.vp.get_Y_coords(show_video=True)

            # Update paddle positions
            if playerA_y:
                self.paddleA.rect.y = playerA_y
            if playerB_y:
                self.paddleB.rect.y = playerB_y

            # --- Game logic should go here
            self.all_sprites_list.update()
            
            #Check if the ball is bouncing against any of the 4 walls:
            if self.ball.rect.x>=WIDTH - 10:
                self.scoreA+=1
                self.ball.velocity[0] = -self.ball.velocity[0]
                self.new_round()
            if self.ball.rect.x<=0:
                self.scoreB+=1
                self.ball.velocity[0] = -self.ball.velocity[0]
                self.new_round()
            if self.ball.rect.y>HEIGHT - 10:
                self.ball.velocity[1] = -self.ball.velocity[1]
            if self.ball.rect.y<0:
                self.ball.velocity[1] = -self.ball.velocity[1]     

            #Detect collisions between the ball and the paddles
            if pygame.sprite.collide_mask(self.ball, self.paddleA) or pygame.sprite.collide_mask(self.ball, self.paddleB):
                self.ball.bounce()

            # Check if starting round
            if (self.cooldown and self.cooldown_ticks < 0):
                # Start the ball with a new velocity
                if (self.kick_left):
                    self.ball.velocity = [-randint(4,8),randint(-8,8)]
                    self.kick_left = False
                else:
                    self.ball.velocity = [randint(4,8),randint(-8,8)]
                    self.kick_left = True
                self.cooldown = False
            else:
                # We need to wait some more time, decrement cooldown clock
                now = pygame.time.get_ticks()
                self.cooldown_ticks -= (now - self.last)
                self.last = now
            
            # --- Redraw the screen
            self.update_screen()
            
            # --- Limit to 60 frames per second
            self.clock.tick(60)

        # End of game clean up
        self.vp.close() 


    def update_screen(self):
        # First, clear the screen to black. 
        self.screen.fill(BLACK)
        #Draw the net
        pygame.draw.line(self.screen, WHITE, [349, 0], [349, 500], 5)
        
        #Now let's draw all the sprites in one go. (For now we only have 2 sprites!)
        self.all_sprites_list.draw(self.screen) 

        #Display scores:
        font = pygame.font.Font(None, 74)
        text = font.render(str(self.scoreA), 1, WHITE)
        self.screen.blit(text, (250,10))
        text = font.render(str(self.scoreB), 1, WHITE)
        self.screen.blit(text, (420,10))

        # --- Go ahead and update the screen with what we've drawn.
        pygame.display.flip()
    
    def new_round(self):
        # Move ball to center
        self.ball.rect.x = SCREEN_CENTER_X
        self.ball.rect.y = SCREEN_CENTER_Y
        # Kill velocity
        self.ball.velocity = [0,0]
        # Start game countdown
        self.last = pygame.time.get_ticks()
        self.cooldown_ticks = 500  
        self.cooldown = True

    #Check if the ball is bouncing against any of the 4 walls:
    def check_wall_collisions(self):
        if self.ball.rect.x>=690:
            self.scoreA+=1
            self.ball.velocity[0] = -self.ball.velocity[0]
            self.new_round()
        if self.ball.rect.x<=0:
            self.scoreB+=1
            self.ball.velocity[0] = -self.ball.velocity[0]
            self.new_round()
        if self.ball.rect.y>490:
            self.ball.velocity[1] = -self.ball.velocity[1]
        if self.ball.rect.y<0:
            self.ball.velocity[1] = -self.ball.velocity[1]  
        

# Main program
def main():
    # Initialize game
    pong = Pong()
    # Kick off main game loop
    pong.game_loop()
    #Once we have exited the main program loop we can stop the game engine:
    pygame.quit()

if __name__ == "__main__":
    main()
