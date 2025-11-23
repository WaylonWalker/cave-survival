import sys

import pygame

from map import generate_map

pygame.init()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

player_skin = pygame.image.load("player.png")
# load the player image
player_image = pygame.image.load("player.png").convert_alpha()

# set the size of the hitbox
hitbox_width = 16
hitbox_height = 32

# create a surface to draw the hitbox on
hitbox_surface = pygame.Surface((hitbox_width, hitbox_height), pygame.SRCALPHA)

# draw the hitbox outline
outline_color = (255, 0, 0)  # red outline color
outline_width = 5  # outline width in pixels
pygame.draw.rect(
    hitbox_surface, outline_color, hitbox_surface.get_rect(), outline_width
)

# scale the player image to the size of the hitbox
player_skin = pygame.transform.scale(player_image, (hitbox_width, hitbox_height))
player_x = 0
player_y = 0
player_speed = 5
player_direction = "right"

map_data = generate_map(screen_width * 5, screen_height)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        player_x -= player_speed

    if keys[pygame.K_RIGHT]:
        player_x += player_speed

    if keys[pygame.K_DOWN]:
        # Handle crouching
        ...

    if keys[pygame.K_SPACE]:
        # Handle jumping
        ...

    if keys[pygame.K_LSHIFT]:
        # Handle running
        ...

        # Handle aiming and firing the grapple hook using Pygame's mouse functions

    screen.fill((255, 255, 255))

    # Draw the map using the map_data generated with perlin noise
    tile_size = 16
    for y, row in enumerate(map_data):
        for x, noise_value in enumerate(row):
            if noise_value > 0.3:
                pygame.draw.rect(
                    screen,
                    (0, 0, 0),
                    (x * tile_size, y * tile_size, tile_size, tile_size),
                )

    # Draw the player's skin and hitbox on the screen
    screen.blit(player_skin, (player_x, player_y))
    # pygame.draw.rect(
    #     screen, (255, 0, 0, 128), (player_x, player_y, hitbox_width, hitbox_height)
    # )

    # blit the hitbox surface onto the player surface
    player_surface = pygame.Surface((hitbox_width, hitbox_height), pygame.SRCALPHA)
    player_surface.blit(hitbox_surface, (0, 0))

    pygame.display.update()
    clock.tick(60)
