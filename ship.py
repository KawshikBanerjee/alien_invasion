import pygame

class Ship:
    def __init__(self, ai_game):
        # initialize ship and set its starting position
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings

        # load the ship image and its rect
        self.image = pygame.image.load('images/rocket.png')
        self.rect = self.image.get_rect()

        # start each ship at the bottom centre of the screen
        self.rect.midbottom = self.screen_rect.midbottom

        #storing dec value ship's horizontal position
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        # movement flag
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
    
    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        if self.moving_up and self.rect.top > 0:
            self.y -= self.settings.ship_speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.ship_speed
        
        # update rect object
        self.rect.x = self.x
        self.rect.y = self.y

    def blitme(self):
        # draw the ship at its current location 
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)