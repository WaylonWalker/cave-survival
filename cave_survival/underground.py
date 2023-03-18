from pydantic import BaseModel
import pygame
from rich.console import Console

from cave_survival.map import Map, Point

console = Console()

# Initialize pygame
pygame.init()

# Set up the display
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Underground Survival")

# Set up the clock
clock = pygame.time.Clock()

# Set up the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (128, 128, 128)
RED = (255, 128, 128)

# Set up the player


class Collisions(BaseModel):
    top: bool = False
    right: bool = False
    bottom: bool = False
    left: bool = False


class Player:
    def __init__(self):
        self.width = 16
        self.height = 16
        self.x = screen_width / 2
        self.y = screen_height / 2
        self.speed = 5
        self.image = pygame.image.load("player.png").convert_alpha()
        self.x_last = self.x
        self.y_last = self.y
        self.hitbox_surface = pygame.Surface((self.width, self.height))
        self.hitbox_surface.fill(WHITE)
        pygame.draw.rect(
            self.hitbox_surface, (255, 0, 0), (0, 0, self.width, self.height), 1
        )
        self.hitbox_surface.set_alpha(0)

    def draw(self, surface, offset):
        surface.blit(
            pygame.transform.scale(self.image, (16, 16)),
            (self.x - 8 - offset.x, self.y - 8 - offset.y),
        )


# def generate_perlin_noise(width, height, scale):
#     map.noise_map = [[0 for y in range(height)] for x in range(width)]
#     for i in range(width):
#         for j in range(height):
#             map.noise_map[i][j] = noise.pnoise2(
#                 i / float(scale),
#                 j / float(scale),
#                 octaves=6,
#                 persistence=0.5,
#                 lacunarity=2.0,
#                 repeatx=1024,
#                 repeaty=1024,
#                 base=0,
#             )
#     return map.noise_map


player = Player()

# Set up the enemies
enemy_width = 32
enemy_height = 32
enemy_speed = 2
enemy_image = pygame.image.load("enemy.png").convert_alpha()

# Set up the items
item_width = 32
item_height = 32
item_image = pygame.image.load("item.png").convert_alpha()

# Set up the day/night cycle
day_length = 60 * 60  # 60 seconds * 60 frames
day_timer = 0

# Set up the inventory
inventory = ["sword", "pickaxe", "axe"]

# Set up the map

map = Map()
map_image = pygame.image.load("map.png").convert_alpha()

# Set up the inventory surface
inventory_surface = pygame.Surface((len(inventory) * 32, 32))
inventory_surface.fill(GREY)

# Generate the map using perlin noise
# map.noise_map = [[0 for x in range(map.width)] for y in range(map.height)]
# map.noise_map = generate_perlin_noise(map.width, map.height, map.scale)
# for x in range(map.width):
#     for y in range(map.height):
#         map.noise_map[x][y] = random.randint(0, 255)

# Make sure the player starts on a white block
# while (
#     map.noise_map[int(player.x / map.resolution)][int(player.y / map.resolution)]
#     < map.thresh
# ):

# while map.point_check_collision(player.pos.x, player.pos.y):
#     player.x += 1
#     player.y += 1
# player.x -= 1
# player.y -= 1

# Main game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update the day/night cycle
    day_timer += 1
    if day_timer > day_length:
        day_timer = 0

    # Update the player
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player.y -= player.speed
    if keys[pygame.K_s]:
        player.y += player.speed
    if keys[pygame.K_a]:
        player.x -= player.speed
    if keys[pygame.K_d]:
        player.x += player.speed

    # Check for player collisions with the walls and the black tiles on the map
    collisions = Collisions()
    if player.x < 0:
        player.x = 0
        collisions.left = True
    if player.x > screen_width - player.width:
        player.x = screen_width - player.width
        collisions.right = True
    if player.y < 0:
        player.y = 0
        collisions.top = True
    if player.y > screen_height - player.height:
        player.y = screen_height - player.height
        collisions.bottom = True

    player.pos = pygame.math.Vector2(player.x, player.y)

    if map.point_check_collision(player.pos.x, player.pos.y):

        start_pos = pygame.math.Vector2(player.x_last, player.y_last)
        end_pos = pygame.math.Vector2(player.x, player.y)
        movement_vector = end_pos - start_pos
        try:
            movement_direction = movement_vector.normalize()
        except:
            end_pos = pygame.math.Vector2(player.x + 128, player.y + 128)
            movement_vector = end_pos - start_pos
            movement_direction = movement_vector.normalize()
        movement_speed = 0.05

        player.x = player.x_last
        player.y = player.y_last

        player.pos = pygame.math.Vector2(start_pos)

        while map.point_check_collision(player.pos.x, player.pos.y):
            # map.noise_map[int(player.pos.x / map.resolution)][
            #     int(player.pos.y / map.resolution)
            # ] <
            # map.thresh
            # ):
            print("moving")
            print(movement_speed)
            print(movement_direction)

            player.pos += movement_speed * movement_direction
            player.x = player.pos.x
            player.y = player.pos.y

        player.pos -= movement_speed * movement_direction
        player.x = player.pos.x
        player.y = player.pos.y

    player.x_last = player.x
    player.y_last = player.y

    # Update the enemies
    # for enemy in enemies:
    # enemy_x += enemy_speed
    # enemy_y += enemy_speed

    # Draw the screen
    screen.fill(BLACK)

    # Draw the map
    map.offset = Point(x=player.x, y=player.y)
    map.offset = Point(x=0, y=0)
    map.draw(screen)

    # Draw the player
    player.draw(screen, offset=map.offset)

    # Draw the enemies
    # for enemy in enemies:
    # screen.blit(enemy_image, (enemy_x, enemy_y))

    # Draw the items
    # for item in items:
    # screen.blit(item_image, (item_x, item_y))

    # Draw the inventory
    for i, item_name in enumerate(inventory):
        inventory_surface.blit(
            pygame.image.load(item_name + ".png").convert_alpha(), (i * 32, 0)
        )
    screen.blit(
        inventory_surface,
        (
            screen_width / 2 - inventory_surface.get_width() / 2,
            screen_height - inventory_surface.get_height(),
        ),
    )

    # Draw the day/night cycle
    pygame.draw.rect(screen, GREY, (0, 0, day_timer / day_length * screen_width, 10))

    # collision debug
    # top

    # pygame.draw.rect(screen, RED, (0, 0, screen_width, 5))
    # # bottom
    # pygame.draw.rect(screen, RED, (0, screen_height - 5, screen_width, 5))
    # # left
    # pygame.draw.rect(screen, RED, (0, 0, 5, screen_height))
    # # right
    # pygame.draw.rect(screen, RED, (screen_width - 5, 0, 5, screen_height))

    # Update the display
    pygame.display.flip()

    # Limit the framerate
    clock.tick(60)
    # console.log(clock.get_fps())


# Quit pygame
pygame.quit()
