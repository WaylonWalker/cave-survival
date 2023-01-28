import pygame


def run():
    # Initialize Pygame
    pygame.init()

    # Set the window size and caption
    size = (700, 500)
    caption = "Pygame Image Movement"
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption(caption)

    # Load an image and get its rectangle
    image1 = pygame.image.load("cave_survival/assets/stev/1.png")
    image2 = pygame.image.load("cave_survival/assets/stev/2.png")
    image_rect = image1.get_rect()

    # Set the initial position of the image
    image_rect.x = 0
    image_rect.y = 0
    movement_speed = 0.5

    # Set the animation speed
    animation_speed = 0.005

    # Set the animation frame
    animation_frame = 0

    # Set the movement speed
    movement_speed = 0.5

    # Main game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Get the current key presses
        pressed = pygame.key.get_pressed()

        # Move the image based on the key presses
        if pressed[pygame.K_w]:
            image_rect.y -= movement_speed
        if pressed[pygame.K_a]:
            image_rect.x -= movement_speed
        if pressed[pygame.K_s]:
            image_rect.y += movement_speed
        if pressed[pygame.K_d]:
            image_rect.x += movement_speed

        # Animate the image if the player is moving
        if (
            pressed[pygame.K_w] or
            pressed[pygame.K_a] or
            pressed[pygame.K_s] or
            pressed[pygame.K_d]
        ):
            animation_frame += animation_speed
            if animation_frame >= 2:
                animation_frame = 0

            image_rect.x += movement_speed + 1

            # Draw the image on the screen
            screen.fill((0, 0, 0))
            if animation_frame < 1:
                screen.blit(image1, image_rect)
            else:
                screen.blit(image2, image_rect)
        else:
            screen.fill((0, 0, 0))
            screen.blit(image1, image_rect)
        pygame.display.flip()

    # Clean up
    pygame.quit()
