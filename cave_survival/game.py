import pygame
from pydantic import BaseModel

from cave_survival.config import config
from cave_survival.console import console
from cave_survival.daylightcycle import DayLightCycle
from cave_survival.map import Map, Point
from cave_survival.player import Player


class Game:
    def __init__(self):
        # Initialize pygame
        pygame.init()
        pygame.display.set_caption("Underground Survival")

        self.screen = pygame.display.set_mode(
            (config.screen_width, config.screen_height)
        )
        self.clock = pygame.time.Clock()
        self.player = Player(game=self)
        self.map = Map(self)
        self.daylightcycle = DayLightCycle(self)
        self.inventory = ["sword", "pickaxe", "axe"]
        self.inventory_surface = pygame.Surface((len(self.inventory) * 32, 32))
        self.inventory_surface.fill(config.GREY)

        self.running = True

    def run(self):
        while self.running:
            self.events = pygame.event.get()
            self.keys = pygame.key.get_pressed()
            for event in self.events:
                if event.type == pygame.QUIT:
                    self.running = False

            # Update the day/night cycle

            # Draw the screen
            self.screen.fill(config.BLACK)

            self.map.draw()
            self.player.draw()

            # Draw the inventory
            for i, item_name in enumerate(self.inventory):
                self.inventory_surface.blit(
                    pygame.image.load(item_name + ".png").convert_alpha(), (i * 32, 0)
                )
            self.screen.blit(
                self.inventory_surface,
                (
                    config.screen_width / 2 - self.inventory_surface.get_width() / 2,
                    config.screen_height - self.inventory_surface.get_height(),
                ),
            )
            self.daylightcycle.draw()
            pygame.display.flip()
            self.clock.tick(config.fps)

        pygame.quit()
