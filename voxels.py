import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# Set up the dimensions of the window
window_width, window_height = 800, 600

# Initialize Pygame
pygame.init()
pygame.display.set_mode((window_width, window_height), DOUBLEBUF | OPENGL)

# Set up the perspective view
gluPerspective(45, (window_width / window_height), 0.1, 50.0)

# Move the camera backward to view the scene
glTranslatef(0.0, 0.0, -5)

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    # Keyboard input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_s]:
        glRotatef(1, 0, 1, 0)
    if keys[pygame.K_d]:
        glRotatef(-1, 0, 1, 0)
    if keys[pygame.K_w]:
        glRotatef(1, 1, 0, 0)
    if keys[pygame.K_d]:
        glRotatef(-1, 1, 0, 0)

    # Clear the screen and draw the cubes
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Draw your 3D voxel grid here
    glBegin(GL_QUADS)
    # Example: Draw a simple 1x1x1 cube at (0, 0, 0)
    glColor3f(1, 0, 0)
    glVertex3f(-0.5, -0.5, -0.5)
    glVertex3f(0.5, -0.5, -0.5)
    glVertex3f(0.5, 0.5, -0.5)
    glVertex3f(-0.5, 0.5, -0.5)
    glEnd()

    # Update the display
    pygame.display.flip()
    pygame.time.wait(10)
