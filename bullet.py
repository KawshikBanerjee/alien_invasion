import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):

    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        '''self.color = self.settings.bullet_color'''
        # load the bullet image and its rect
        self.image = pygame.image.load('images/fire.png')
        self.rect = self.image.get_rect()

        '''# create bullet at (0,0) then correct position
        # self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)'''
        # load the bullets at ship's top mid position
        self.rect.midtop = ai_game.ship.rect.midtop

        # store the bullet's position as decimal value
        self.y = float(self.rect.y)

    def update(self):
        # moving the bullet up 
        self.y -= self.settings.bullet_speed    # update decimal position
        self.rect.y = self.y    # update rect position

    def draw_bullet(self):
        self.screen.blit(self.image, self.rect)
        # pygame.draw.rect(self.screen, self.color, self.rect)    # draw it on screen

     