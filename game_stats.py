class Gamestats:
    def __init__(self, ai_game):
        self.settings = ai_game.settings

        dekho = open(r"highscore.txt", "r")
        self.high_score = int(dekho.read())

        self.reset_stats()
        self.game_active = False    # game in active state

    def reset_stats(self):
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
        