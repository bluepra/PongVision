# Import the pygame library and initialise the game engine
import pygame
from paddle import Paddle
from ball import Ball
import cv2 as cv
import time
import methods
 
pygame.init()

WIDTH, HEIGHT = 900, 500
 
# Define some colors
BLACK = (0,0,0)
WHITE = (255,255,255)

# set up camera
cam = methods.cam_set_up(WIDTH, HEIGHT)
face_cascade=cv.CascadeClassifier(cv.data.haarcascades + "haarcascade_frontalface_alt2.xml")
ds_factor=0.6

# Open a new window
size = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Pong")
 
paddleA = Paddle(WHITE, 10, 100)
paddleA.rect.x = 5
paddleA.rect.y = 200
 
paddleB = Paddle(WHITE, 10, 100)
paddleB.rect.x = WIDTH - 15
paddleB.rect.y = 200
 
ball = Ball(WHITE,10,10)
ball.rect.x = 345
ball.rect.y = 195
 
#This will be a list that will contain all the sprites we intend to use in our game.
all_sprites_list = pygame.sprite.Group()
 
# Add the paddles and the ball to the list of sprites
all_sprites_list.add(paddleA)
all_sprites_list.add(paddleB)
all_sprites_list.add(ball)
 
# The loop will carry on until the user exits the game (e.g. clicks the close button).
carryOn = True
 
# The clock will be used to control how fast the screen updates
clock = pygame.time.Clock()
 
#Initialise player scores
scoreA = 0
scoreB = 0

cur_time = None
prev_time = 0
def show_fps(frame):
    global cur_time
    global prev_time

    cur_time = time.time()
    fps = int(1/(cur_time-prev_time))
    prev_time = cur_time
    
    # print('FPS:', fps)
    return cv.putText(frame, str(fps), (70,80), cv.FONT_HERSHEY_PLAIN, 3, (255,0,0), 3)
 
# -------- Main Program Loop -----------
while carryOn:
    # --- Main event loop
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
              carryOn = False # Flag that we are done so we exit this loop
        elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_x: #Pressing the x Key will quit the game
                     carryOn=False
 

 
    # --- Game logic should go here
    all_sprites_list.update()

    # face track
    ret, frame = cam.read()
    
    frame, nose_y = methods.pose_estimation(frame)
    paddleA.rect.y = nose_y - 100
    paddleB.rect.y = nose_y - 100

   
    
    #Check if the ball is bouncing against any of the 4 walls:
    if ball.rect.x>=WIDTH:
        scoreA+=1
        ball.velocity[0] = -ball.velocity[0]
    if ball.rect.x<=0:
        scoreB+=1
        ball.velocity[0] = -ball.velocity[0]
    if ball.rect.y>HEIGHT:
        ball.velocity[1] = -ball.velocity[1]
    if ball.rect.y<0:
        ball.velocity[1] = -ball.velocity[1]     
 
    #Detect collisions between the ball and the paddles
    if pygame.sprite.collide_mask(ball, paddleA) or pygame.sprite.collide_mask(ball, paddleB):
      ball.bounce()
    
    # --- Drawing code should go here
    # First, clear the screen to black. 
    screen.fill(BLACK)
    #Draw the net
    pygame.draw.line(screen, WHITE, [WIDTH / 2, 0], [WIDTH / 2, 500], 5)
    
    #Now let's draw all the sprites in one go. (For now we only have 2 sprites!)
    all_sprites_list.draw(screen) 
 
    #Display scores:
    font = pygame.font.Font(None, 74)
    text = font.render(str(scoreA), 1, WHITE)
    screen.blit(text, (WIDTH / 4,10))
    text = font.render(str(scoreB), 1, WHITE)
    screen.blit(text, (WIDTH * (3/4),10))
 
    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
     
    # --- Limit to 60 frames per second
    clock.tick(60)

    frame = show_fps(frame)
    if ret:
        cv.imshow("Hello", frame)
        

        if cv.waitKey(33) == ord('q'):
            break
 
#Once we have exited the main program loop we can stop the game engine:
pygame.quit()