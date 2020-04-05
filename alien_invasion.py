import sys
import pygame
from time import sleep
from settings import Settings
from game_stats import Gamestats
from scoreboard import Scoreboard
from button import Button
from star import Star
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion:
    # overall class for game assets and behaviour
    def __init__(self):
        pygame.init()    # initialize the game
        self.settings = Settings()
        # self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        
        # for full screen mode
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")

        self.stats = Gamestats(self)    # instance for game stats
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.stars = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()    
        self.aliens = pygame.sprite.Group()
        self._create_tara()
        self._create_fleet()
        self.play_button = Button(self, "START!")

    def run_game(self):
        while True:    # starts the main loop for game
            self._check_events()    # watch for keyboard and mouse movements
            self.stars.update()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()

    def _create_tara(self):
        star = Star(self)    # make a star
        star_width, star_height = star.rect.size
        available_space_x = self.settings.screen_width - 10*star_width
        number_stars_x = available_space_x // (25*star_width)

        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3*star_height) - ship_height)
        number_rows = available_space_y // (2*star_height)

        for row_number in range (number_rows):
            for star_number in range(number_stars_x):
                self._create_star(star_number, row_number)

    def _create_star(self, star_number, row_number):
        star = Star(self)
        star_width, star_height = star.rect.size
        star.x = star_width + 40*star_width*star_number
        star.rect.x = star.x + 10
        star.rect.y = (5*star.rect.height + 40*star.rect.height*row_number)
        self.stars.add(star)
    
    def _create_fleet(self):
        # create a fleet of aliens
        alien = Alien(self)    # make an alien
        alien_width, alien_height = alien.rect.size 
        available_space_x = self.settings.screen_width - (2*alien_width)
        number_aliens_x = available_space_x // (2*alien_width)

        # determine the number of rows of aliens to fit on screen
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3*alien_height) - ship_height)
        number_rows = available_space_y // (2*alien_height) 

        # create the full sleet of aliens
        for row_number in range(number_rows):
            for alien_number in range (number_aliens_x):
                self._create_alien(alien_number, row_number)
            
    def _create_alien(self, alien_number, row_number):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2*alien_width*alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2*alien.rect.height*row_number
        self.aliens.add(alien)
    
    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    
    def _change_fleet_direction(self):
        # drop the entire fleet and change its direction
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= (-1)
    
    def _update_aliens(self):
        self._check_fleet_edges() # check if fleet is at an edge
        self.aliens.update()    # update the position of all aliens
        # look for alien-ship collisions
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        self._check_aliens_bottom()    # check if alien has hit bottom

    def _check_aliens_bottom(self):
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

    def _ship_hit(self):
        if self.stats.ships_left > 0:   
            self.stats.ships_left -= 1     # decreament ships left
            # get rid of remaining aliens and bullets
            self.aliens.empty()
            self.bullets.empty()
            # create new fleet and centre the ship
            self._create_fleet()
            self.ship.center_ship
            sleep(0.5)  #pause
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)
    
    def _update_bullets(self):
        self.bullets.update()
        # deleting bullets vanished from screen
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        #print(len(self.bullets))
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        # check if a bullet has hit an alien; if hits, get reid of both
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)    # score update
            self.sb.prep_score()
            self.sb.check_high_score()

        # if aliens group is empty, create new fleet
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            self.stats.level += 1
            self.sb.prep_level()

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                lekho = open(r"highscore.txt", "w")
                lekho.write(str(self.stats.high_score))
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
            elif event.type == pygame.KEYDOWN:    # keydown=pressing/holding key, keyup=releasing 
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            
    
    def _check_play_button(self, mouse_pos):
        # start game when user hit play button
        button_clicked = self.play_button.rect.collidepoint(mouse_pos) 
        if button_clicked and not self.stats.game_active:
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()    # reset the game stat
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level

            self.aliens.empty()
            self.bullets.empty()

            self._create_fleet()
            self.ship.center_ship()
            pygame.mouse.set_visible(False)
    
    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_ESCAPE:
            lekho = open(r"highscore.txt", "w")
            lekho.write(str(self.stats.high_score))
            sys.exit()

    def _check_keyup_events (self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False

    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)   # create new bullet and add it in group
            self.bullets.add(new_bullet)

    def _update_screen(self):
            # redraw the screen during each pass through the loop
            self.screen.fill(self.settings.bg_color)
            self.stars.draw(self.screen)
            self.ship.blitme()
            for bullet in self.bullets.sprites():
                bullet.draw_bullet()
            self.aliens.draw(self.screen)

            self.sb.show_score()

            # draw the play button if the game is inactive
            if not self.stats.game_active:
                self.play_button.draw_button()

            pygame.display.flip()    # make the recent screen visible

if __name__ == '__main__':
    ai = AlienInvasion()    # make a game instance
    ai.run_game()   # run the game
