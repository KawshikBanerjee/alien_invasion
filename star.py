import pygame
from pygame.sprite import Sprite
#from random import randint

class Star(Sprite):
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        # load the star image
        self.image = pygame.image.load('images/star.png')
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width   # start each star near top-left of screen
        self.rect.y = 5*self.rect.height

        self.x = float(self.rect.x)    # store position
    
    def update(self):
        self.rect.x = self.x + 100
