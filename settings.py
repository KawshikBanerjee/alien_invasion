class Settings:
    def __init__(self):
        # screen settings
        '''self.screen_width = 1000
        self.screen_height = 600'''
        self.bg_color = (22, 13, 34)

        # ship settings
        self.ship_limit = 2

        # bullet settings
        '''self.bullet_width = 5
        self.bullet_height = 7
        self.bullet_color = (255, 0, 0) '''
        self.bullets_allowed = 3

        # alien settings
        self.fleet_drop_speed = 10

        # game speed
        self.speedup_scale = 1.1    # game speedup
        self.score_scale = 1.5     # score speedup
        self.initialize_dynamic_settings()
        
    def initialize_dynamic_settings(self):
        self.ship_speed = 1.5
        self.bullet_speed = 3
        self.alien_speed = 1.0
        self.fleet_direction = 1    # 1 means right, -1 means left
        self.alien_points = 5
    
    def increase_speed(self):
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)


