import pygame

pygame.mixer.init()

BLACK = (9,9,9)
WHITE = (255,255,255)

WIDTH = 700
HEIGHT = 500

# Define screen params
SCREEN_CENTER_X = WIDTH // 2
SCREEN_CENTER_Y = HEIGHT // 2
MEAS_MAX_Y = HEIGHT * 3 // 4
MEAS_MIN_Y = WIDTH // 4
# MEAS_MAX_Y = SCREEN_H * 5 // 8
# MEAS_MIN_Y = SCREEN_H *3 // 8

# Sampling window size
SAMPLE_WINDOW_SIZE = 4

# Ball velocity multiplier
VELOCITY_MULT = 4

# Motion sensitivity multiplier
VERT_MULT = 2

menu_background_img = './assets/menu_background.png'
game_background_img = './assets/black999-background.png'


title_font = './assets/fonts/Charge_Vector.ttf'
button_font = './assets/fonts/BarcadeBold.ttf'
score_font = './assets/fonts/Charge_Vector.ttf'

background_music = './assets/Pump.wav'

score_sound = pygame.mixer.Sound('./assets/sounds/score.wav')
paddle_hit_sound = pygame.mixer.Sound('./assets/sounds/paddle-hit.wav')
start_sound = pygame.mixer.Sound('./assets/sounds/start.wav')
countdown_sound = pygame.mixer.Sound('./assets/sounds/countdown.wav')


RED = (207,64,67)
BLUE = (108,182,207)
GRAY = (138,138,138)