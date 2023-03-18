from noise import snoise2
import pydantic
import pygame
from rich.console import Console

console = Console()

# Generate the map using perlin noise

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (128, 128, 128)
RED = (255, 128, 128)


class Point(pydantic.BaseModel):
    x: int
    y: int


class Map:
    def __init__(self):
        self.resolution = 32
        self.scale = 0.1  # Determines the "smoothness" of the terrain
        self.offset = Point(x=0, y=0)
        self.last_offset = self.offset
        # self.width = int(screen_width / self.resolution)
        # self.height = int(screen_height / self.resolution)
        self.screen_width = 800
        self.screen_height = 600
        self.octaves = 6  # Number of layers of noise to combine
        self.persistence = 0.5  # Amplitude of each octave
        self.lacunarity = 2.0  # Frequency of each octave
        self.thresh = 128
        self.surf = pygame.Surface(
            (self.screen_width / self.resolution, self.screen_height / self.resolution)
        )
        self.pre_draw()

        # self.noise_map = self.generate_noise_map()

    # def generate_noise_map(self):

    #     noise_map = [
    #         [self.get_noise(x, y) for x in range(self.width)]
    #         for y in range(self.height)
    #     ]
    #     return noise_map

    def get_noise(self, x, y):
        value = snoise2(
            (x + self.offset.x) * self.scale,
            (y + self.offset.y) * self.scale,
            self.octaves,
            self.persistence,
            self.lacunarity,
        )
        value = (value + 1) / 2 * 255
        return value

    def draw(self, screen):
        # if self.last_offset != self.offset:
        #     self.last_offset = self.offset
        screen.blit(
            pygame.transform.scale(self.surf, (self.screen_width, self.screen_height)),
            (0, 0),
        )

    def point_check_collision(self, x, y):
        return self.get_noise(x / self.resolution, y / self.resolution) < self.thresh

    def pre_draw(self):
        console.log("drawing")
        self.surf = pygame.Surface((self.screen_width, self.screen_height))
        for x in range(self.screen_width):
            for y in range(self.screen_height):
                if not self.point_check_collision(x, y):
                    pygame.draw.rect(
                        self.surf,
                        WHITE,
                        (
                            x,
                            y,
                            1,
                            1,
                            # self.resolution,
                            # self.resolution,
                        ),
                    )
        pygame.image.save(self.surf, "map.png")
