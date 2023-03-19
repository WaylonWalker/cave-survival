import pygame

from cave_survival.config import config
from cave_survival.console import console


class Player:
    def __init__(self, game):
        self.game = game
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

    def move(self):
        # Update the self
        if self.game.keys[pygame.K_w]:
            self.y -= self.speed
        if self.game.keys[pygame.K_s]:
            self.y += self.speed
        if self.game.keys[pygame.K_a]:
            self.x -= self.speed
        if self.game.keys[pygame.K_d]:
            self.x += self.speed

        # Check for self collisions with the walls and the black tiles on the map
        if self.x < 0:
            self.x = 0
        if self.x > config.screen_width - self.width:
            self.x = config.screen_width - self.width
        if self.y < 0:
            self.y = 0
        if self.y > config.screen_height - self.height:
            self.y = config.screen_height - self.height

        self.pos = pygame.math.Vector2(self.x, self.y)

        if self.game.map.point_check_collision(self.pos.x, self.pos.y):

            start_pos = pygame.math.Vector2(self.x_last, self.y_last)
            end_pos = pygame.math.Vector2(self.x, self.y)
            movement_vector = end_pos - start_pos
            try:
                movement_direction = movement_vector.normalize()
            except:
                end_pos = pygame.math.Vector2(self.x + 128, self.y + 128)
                movement_vector = end_pos - start_pos
                movement_direction = movement_vector.normalize()
            movement_speed = 0.05

            self.x = self.x_last
            self.y = self.y_last

            self.pos = pygame.math.Vector2(start_pos)

            while self.game.map.point_check_collision(self.pos.x, self.pos.y):
                self.pos += movement_speed * movement_direction
                self.x = self.pos.x
                self.y = self.pos.y

            self.pos -= movement_speed * movement_direction
            self.x = self.pos.x
            self.y = self.pos.y

        self.x_last = self.x
        self.y_last = self.y

    def draw(self):
        self.move()
        self.game.screen.blit(
            pygame.transform.scale(self.image, (16, 16)),
            (self.x - 8 - self.game.map.offset.x, self.y - 8 - self.game.map.offset.y),
        )
