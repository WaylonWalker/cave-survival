import pydantic
import pygame
from noise import snoise2
from PIL import Image, ImageFilter
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
        self.grass = pygame.image.load("grass.webp").convert_alpha()
        self.rock = pygame.image.load("rock.jpg").convert_alpha()
        self.dirt = pygame.image.load("dirt.jpg").convert_alpha()
        self.resolution = 16
        self.scale = 0.14  # Determines the "smoothness" of the terrain
        self.offset = Point(x=0, y=0)
        self.last_offset = self.offset
        # self.width = int(screen_width / self.resolution)
        # self.height = int(screen_height / self.resolution)
        self.screen_width = 800
        self.screen_height = 600
        self.octaves = 2  # Number of layers of noise to combine
        self.persistence = 0.05  # Amplitude of each octave
        self.lacunarity = 1.0  # Frequency of each octave
        self.thresh = 128
        self.pre_draw()

    def refresh_surf(self):
        self.surf = pygame.Surface((self.screen_width, self.screen_height))
        # self.surf.blit(self.grass, (0, 0))

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

    def point_check_collision(self, x, y, thresh=None):
        return self.get_noise(x / self.resolution, y / self.resolution) < (
            thresh or self.thresh
        )

    def pre_draw(self):
        console.log("drawing")
        self.refresh_surf()
        for x in range(int(self.screen_width)):
            for y in range(int(self.screen_height)):
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
        av1 = (
            Image.open("rock.jpg")
            .convert("RGB")
            .resize((self.screen_width, self.screen_height))
        )
        av2 = (
            Image.open("dirt.jpg")
            .convert("RGB")
            .resize((self.screen_width, self.screen_height))
        )
        mask = (
            Image.open("map.png")
            .convert("L")
            .resize((self.screen_width, self.screen_height))
            .filter(ImageFilter.GaussianBlur(3))
        )
        Image.composite(av2, av1, mask).save("result.png")
        result = pygame.image.load("result.png")
        self.surf.blit(result, (0, 0))
