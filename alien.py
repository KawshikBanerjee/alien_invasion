import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen # initializing alien and its starting position
        self.settings = ai_game.settings

        # load the alien image and its rect attribute
        self.image = pygame.image.load('images/alien.png')
        self.rect = self.image.get_rect()

        # start each new alien near top left of screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # store the alien's exact horizontal position
        self.x = float(self.rect.x)
    
    def check_edges(self):
        # return tru if alien is at edge of screen
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

    def update(self):
        # move alien to right/left
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x

    