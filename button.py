import pygame.font

class Button:
    def __init__(self, ai_game, msg):
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # setting up properties
        self.width, self.height = 320, 80
        self.button_color = (243,198,35)
        self.text_color = (16,55,92)
        self.font = pygame.font.Font("fonts/Gilroy-ExtraBold.otf", 50)

        # button's rect object and centering
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # the button message
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        # turn msg into a rendered image
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)

