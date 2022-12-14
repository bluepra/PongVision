import pygame
from constants import *
from random import uniform, randint

class Button:
    def __init__(self, text, x, y, width, height, background_color, text_color, fontsize, hover_color = WHITE):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font = pygame.font.Font(button_font, fontsize)
        self.hover = False
        self.background_color = background_color
        self.text_color = text_color
        self.hover_color = hover_color
        self.surface = None

    def draw(self, surface):
        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill(self.background_color)

        if self.hover:
            word = self.font.render(self.text, True, self.hover_color)
        else:
            word = self.font.render(self.text, True, self.text_color)
        self.surface.blit(word, (10,10))

        surface.blit(self.surface, (self.x,self.y))
        

    def update(self, mouse_pos):
        if mouse_pos[0] >= self.x and mouse_pos[0] <= (self.x + self.width):
            if mouse_pos[1] >= self.y and mouse_pos[1] <= (self.y + self.height):
                self.hover = True
            else:
                self.hover = False
        else:
            self.hover = False

    def check_if_clicked(self, mouse_pos):
        if mouse_pos[0] >= self.x and mouse_pos[0] <= (self.x + self.width):
            if mouse_pos[1] >= self.y and mouse_pos[1] <= (self.y + self.height):
                return True
            else:
                return False
        else:
            return False

class TextBox:
    def __init__(self, text, x, y, width, height, box_color, text_color, font_size, font):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.box_color = box_color
        self.text_color = text_color
        self.font_size = font_size
        self.font = font
        self.font =  pygame.font.Font(self.font, self.font_size)

    def draw(self, surface):
        # box_surface = pygame.Surface((self.width, self.height))
        # box_surface.set_alpha(0)

        # pygame.draw.rect(
        #     surface, self.box_color, (self.x, self.y, self.width, self.height))
        word = self.font.render(self.text, True, self.text_color)
        surface.blit(word, (self.x, self.y))
        # surface.blit(box_surface, (self.x, self.y))


    def update_text(self, new_text):
        self.text = new_text

class Ball(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        # Call the parent class (Sprite) constructor
        super().__init__()
        
        # Pass in the color of the ball, its width and height.
        # Set the background color and set it to be transparent
        self.width = width
        self.height = height
        self.image = pygame.transform.scale(pygame.image.load(ball_image_path), (width,height))
        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()
 
        self.velocity = [0,0]
        
        
    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
          
    def bounce(self):
        self.velocity[0] = -self.velocity[0]*uniform(.9,1.25)
        self.velocity[1] = randint(-8,8)


class Paddle(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        # Call the parent class (Sprite) constructor
        super().__init__()
        
        # Pass in the color of the Paddle, its width and height.
        # Set the background color and set it to be transparent
        self.height = height
        self.width = width
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
 
        # Draw the paddle (a rectangle!)
        pygame.draw.rect(self.image, color, [0, 0, width, height])
        
        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()
        
    def moveUp(self, pixels):
        self.rect.y -= pixels
        #Check that you are not going too far (off the screen)
        if self.rect.y < 0:
          self.rect.y = 0
          
    def moveDown(self, pixels):
        self.rect.y += pixels
        #Check that you are not going too far (off the screen)
        if self.rect.y > 400:
          self.rect.y = 400