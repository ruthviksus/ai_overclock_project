import pygame
from OpenGL.GL import *
from OpenGL.GLUT import *
import numpy as np

# Initialize Pygame and OpenGL
pygame.init()
screen = pygame.display.set_mode((1920, 1080), pygame.OPENGL | pygame.DOUBLEBUF)
glEnable(GL_DEPTH_TEST)

# Function to draw a large number of random triangles
def draw_objects():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Clear the screen
    glBegin(GL_TRIANGLES)  # Start drawing triangles
    for _ in range(10000000):  # Draw 100,000 triangles to stress GPU
        glColor3f(np.random.rand(), np.random.rand(), np.random.rand())  # Random color
        # Random positions for vertices
        glVertex3f(np.random.rand(), np.random.rand(), np.random.rand())
        glVertex3f(np.random.rand(), np.random.rand(), np.random.rand())
        glVertex3f(np.random.rand(), np.random.rand(), np.random.rand())
    glEnd()
    pygame.display.flip()  # Update the screen with the rendered frame

# Main loop to keep the stress test running
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Handle window close
            running = False
    draw_objects()  # Continuously draw the random triangles

pygame.quit()