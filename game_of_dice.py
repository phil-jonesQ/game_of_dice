""" Version 1.00 - Routine to display a Six Sided Dice
The dice can be thrown and be used for simple games
Phil Jones October 2019 - phil.jones.24.4@gmail.com
"""

import pygame
import random

# Constants
WindowWidth = 300
WindowHeight = 300
scale = 90
start_x = WindowWidth / 2 - scale
start_y = WindowHeight / 2 - scale
dice_width = 200
dice_length = 200

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
LIGHT_GREEN = (101, 152, 101)
GREY = (128, 128, 128)
dice_surface = pygame.display.set_mode((WindowWidth, WindowHeight))
clock = pygame.time.Clock()
MY_VERSION = "1.00"

# Dice Faces
# One
ON = ['...',
      '.X.',
      '...']
# Two
TW = ['X..',
      '...',
      '..X']
# Three
TH = ['X..',
      '.X.',
      '..X']
# Four
FO = ['X.X',
      '...',
      'X.X']

# Five
FI = ['X.X',
      '.X.',
      'X.X']

# Six
SI = ['X.X',
      'X.X',
      'X.X']

# Map each face array to a single array
dice_faces = [ON, TW, TH, FO, FI, SI]


def throw():
    # Generate a number 1 - 6
    return random.randrange(1, 7)


def draw_dice(surface, throw):
    # Wipe Screen
    dice_surface.fill(BLACK)
    # Draw Dice
    for i in (range(3)):
        for j in (range(3)):
            # Nested loop is needed to iterate over the selected dice face array (3 x 3)
            if dice_faces[throw - 1][j][i] == "X":
                pygame.draw.circle(surface, RED, (int(start_x + scale * i), int(start_y + scale * j)), int(scale / 3))
    # Update the screen
    pygame.display.flip()


def spin(surface):
    # Generate a spin effect
    for j in range(6):
        draw_dice(surface, j)


def main():
    loop = True
    # Declare Global Vars

    pygame.init()
    pygame.display.set_caption("Dice " + MY_VERSION)

    pygame.key.set_repeat(10, 500)

    # Initialise fonts we will use
    font = pygame.font.SysFont('Arial', 50, False, False)
    font2 = pygame.font.SysFont('Arial', 25, False, False)

    current_throw = throw()

    while loop:

        # Control FPS
        clock.tick(10)

        # Draw Dice
        draw_dice(dice_surface, current_throw)

        # Handle quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # Input handling
        keys = pygame.key.get_pressed()
        for key in keys:
            if keys[pygame.K_SPACE]:
                spin(dice_surface)
                current_throw = throw()


# Call main
main()