import pygame

from cave_survival.config import config
from cave_survival.console import console


class Player:
    def __init__(self):
        self.width = 16
        self.height = 16
        self.x = config.screen_width / 2
        self.y = config.screen_height / 2
        self.speed = 5
        self.image = pygame.image.load("player.png").convert_alpha()
        self.x_last = self.x
        self.y_last = self.y
        self.hitbox_surface = pygame.Surface((self.width, self.height))
        self.hitbox_surface.fill(config.WHITE)
        pygame.draw.rect(
            self.hitbox_surface, (255, 0, 0), (0, 0, self.width, self.height), 1
        )
        self.hitbox_surface.set_alpha(0)

    def draw(self, surface, offset):
        surface.blit(
            pygame.transform.scale(self.image, (16, 16)),
            (self.x - 8 - offset.x, self.y - 8 - offset.y),
        )
