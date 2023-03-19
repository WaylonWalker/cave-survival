import pygame

from cave_survival.config import config
from cave_survival.console import console


class DayLightCycle:
    def __init__(self, game):
        self.game = game
        self.console = console
        self.day_length = config.day_length
        self.day_timer = 0

    @property
    def game_time(self):
        return pygame.time.get_ticks() / self.day_length

    @property
    def days(self):
        return int(self.game_time)

    @property
    def time(self):
        return self.game_time - self.days

    def draw(self):

        pygame.draw.rect(
            self.game.screen,
            config.GREY,
            (
                0,
                0,
                self.time * config.screen_width,
                10,
            ),
        )
