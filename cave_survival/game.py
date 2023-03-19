import pygame
from pydantic import BaseModel

from cave_survival.config import config
from cave_survival.console import console
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
        self.player = Player()
        self.day_length = 60 * 60  # 60 seconds * 60 frames
        self.day_timer = 0
        self.inventory = ["sword", "pickaxe", "axe"]
        self.map = Map()
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
            self.day_timer += 1
            if self.day_timer > self.day_length:
                self.day_timer = 0

            # Update the self.player
            if self.keys[pygame.K_w]:
                self.player.y -= self.player.speed
            if self.keys[pygame.K_s]:
                self.player.y += self.player.speed
            if self.keys[pygame.K_a]:
                self.player.x -= self.player.speed
            if self.keys[pygame.K_d]:
                self.player.x += self.player.speed

            # Check for self.player collisions with the walls and the black tiles on the map
            if self.player.x < 0:
                self.player.x = 0
            if self.player.x > config.screen_width - self.player.width:
                self.player.x = config.screen_width - self.player.width
            if self.player.y < 0:
                self.player.y = 0
            if self.player.y > config.screen_height - self.player.height:
                self.player.y = config.screen_height - self.player.height

            self.player.pos = pygame.math.Vector2(self.player.x, self.player.y)

            if self.map.point_check_collision(self.player.pos.x, self.player.pos.y):

                start_pos = pygame.math.Vector2(self.player.x_last, self.player.y_last)
                end_pos = pygame.math.Vector2(self.player.x, self.player.y)
                movement_vector = end_pos - start_pos
                try:
                    movement_direction = movement_vector.normalize()
                except:
                    end_pos = pygame.math.Vector2(
                        self.player.x + 128, self.player.y + 128
                    )
                    movement_vector = end_pos - start_pos
                    movement_direction = movement_vector.normalize()
                movement_speed = 0.05

                self.player.x = self.player.x_last
                self.player.y = self.player.y_last

                self.player.pos = pygame.math.Vector2(start_pos)

                while self.map.point_check_collision(
                    self.player.pos.x, self.player.pos.y
                ):
                    self.player.pos += movement_speed * movement_direction
                    self.player.x = self.player.pos.x
                    self.player.y = self.player.pos.y

                self.player.pos -= movement_speed * movement_direction
                self.player.x = self.player.pos.x
                self.player.y = self.player.pos.y

            self.player.x_last = self.player.x
            self.player.y_last = self.player.y

            # Draw the screen
            self.screen.fill(config.BLACK)

            # Draw the map
            self.map.offset = Point(x=self.player.x, y=self.player.y)
            self.map.offset = Point(x=0, y=0)
            self.map.draw(self.screen)

            # Draw the self.player
            self.player.draw(self.screen, offset=self.map.offset)

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

            # Draw the day/night cycle
            pygame.draw.rect(
                self.screen,
                config.GREY,
                (0, 0, self.day_timer / self.day_length * config.screen_width, 10),
            )

            # Update the display
            pygame.display.flip()

            # Limit the framerate
            self.clock.tick(60)

        # Quit pygame
        pygame.quit()
