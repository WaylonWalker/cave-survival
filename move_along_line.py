import pygame

# Initialize Pygame
pygame.init()

clock = pygame.time.Clock()
# Set the window size and caption
WINDOW_SIZE = (500, 500)
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Moving circle along a line")

# Define some colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Set up the starting position and ending position of the line
start_pos = (50, 300)
end_pos = (400, 400)

end_pos = (50, 300)
start_pos = (400, 400)

# Set up the circle's initial position and movement speed
circle_pos = start_pos
circle_radius = 20
movement_speed = 5

# # Game loop
# running = True
# while running:
#     # Handle events
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False

#     # Clear the screen
#     screen.fill(WHITE)

#     # Draw the line
#     pygame.draw.line(screen, BLACK, start_pos, end_pos)

#     # Draw the circle at its current position
#     pygame.draw.circle(screen, BLACK, circle_pos, circle_radius)

#     # Move the circle along the line
#     movement_vector = pygame.math.Vector2(
#         end_pos[0] - start_pos[0], end_pos[1] - start_pos[1]
#     )
#     movement_direction = movement_vector.normalize()
#     circle_pos = (
#         circle_pos[0] + movement_speed * movement_direction.x,
#         circle_pos[1] + movement_speed * movement_direction.y,
#     )

#     # Check if the circle has reached the end of the line
#     if circle_pos.distance_to(end_pos) < movement_speed:
#         circle_pos = end_pos
#         running = False
#     # Update the display
#     pygame.display.update()

#     clock.tick(60)

# # Quit Pygame
# pygame.quit()

# Set up the starting position and ending position of the line
start_pos = pygame.math.Vector2(50, 50)
end_pos = pygame.math.Vector2(400, 400)

# Set up the circle's initial position
circle_pos = pygame.math.Vector2(start_pos)

# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill(WHITE)

    # Draw the line
    pygame.draw.line(screen, BLACK, start_pos, end_pos)

    # Draw the circle at its current position
    pygame.draw.circle(
        screen, BLACK, [int(circle_pos.x), int(circle_pos.y)], circle_radius
    )

    # Move the circle along the line
    movement_vector = end_pos - start_pos
    movement_direction = movement_vector.normalize()
    circle_pos += movement_speed * movement_direction

    # Check if the circle has reached the end of the line
    if circle_pos.distance_to(end_pos) < movement_speed:
        circle_pos = end_pos
        running = False

    # Update the display
    pygame.display.update()
    clock.tick(60)

# Quit Pygame
pygame.quit()
