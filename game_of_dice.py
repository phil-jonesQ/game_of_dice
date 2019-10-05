""" Version 1.00 - Routine to display a Six Sided Dice
The dice can be thrown and be used for simple games
The current thrown value is shown in white, with the last 15 historical values displayed in Grey
Phil Jones October 2019 - phil.jones.24.4@gmail.com
"""

import pygame
import random

# Constants
WindowWidth = 300
WindowHeight = 400
scale = 90
offset = 45
start_x = WindowWidth / 2 - scale
start_y = WindowHeight / 2 - scale - offset
dice_width = 225
dice_length = 225
# Use a dictionary to store the results
result_p1 = {}
result_p2 = {}
round = 0

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
LIGHT_GREEN = (101, 152, 101)
GREY = (128, 128, 128)
dice_surface = pygame.display.set_mode((WindowWidth, WindowHeight))
clock = pygame.time.Clock()
MY_VERSION = "1.05"

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
    dice_throw = random.randrange(1, 7)
    return dice_throw


def update_score(round, go, current_throw):
    if go == 1:
        d = {"Player 1 for round " + str(round): current_throw}
        result_p1.update(dict(d))  # update it
    else:
        d2 = {"Player 2 for round " + str(round): current_throw}
        result_p2.update(dict(d2))
    #print(result_p1)
    #print(result_p2)


def draw_dice(surface, throw, go):
    # Wipe Screen
    dice_surface.fill(BLACK)
    # Draw Dice Border
    if go == 1:
        my_colour = GREEN
    else:
        my_colour = BLUE
    pygame.draw.line(surface, my_colour, (start_x - offset, start_y - offset), (start_x + dice_width, start_y - offset))
    pygame.draw.line(surface, my_colour, (start_x - offset, start_y - offset), (start_x - offset, start_y + dice_length))
    pygame.draw.line(surface, my_colour, (start_x + dice_width, start_y - offset),
                     (start_x + dice_width, start_y + dice_length))
    pygame.draw.line(surface, my_colour, (start_x - offset, start_y + dice_length),
                     (start_x + dice_width, start_y + dice_length))
    # Draw Dice Face Based on which 3x3 array has been selected
    for i in (range(3)):
        for j in (range(3)):
            # Nested loop is needed to iterate over the selected dice face array (3 x 3)
            if dice_faces[throw - 1][j][i] == "X":
                pygame.draw.circle(surface, my_colour, (int(start_x + scale * i), int(start_y + scale * j)), int(scale / 3))
    # Update the screen
    pygame.display.flip()


def draw_round_message(surface, font, round):
    # Wipe Screen
    dice_surface.fill(BLACK)
    text = font.render("SPACE TO THROW... ", True, RED)
    surface.blit(text, [offset, WindowHeight / 2 - offset])
    pygame.display.flip()


def draw_score(surface, font, current_throw, font2, go):
    # Get historical scores
    offset_px = 5
    # Print the last 15 values from our p1 result dictionary
    if len(result_p1) > 0:
        for x in list(reversed(list(result_p1)))[0:15]:
            history = font2.render(format(result_p1[x]), True, GREEN)
            surface.blit(history, [start_x + offset_px, WindowHeight - offset * 2])
            offset_px += 15

    offset_px = 5
    #print(go)
    if len(result_p2) > 0:
        for x in list(reversed(list(result_p2)))[0:15]:
            history = font2.render(format(result_p2[x]), True, BLUE)
            surface.blit(history, [start_x + offset_px, WindowHeight - offset ^ 2 * 2])
            offset_px += 15
    # Extract the last winner
    for x in list(reversed(list(result_p1)))[0:1]:
        p1_result = format(result_p1[x])
        print(p1_result)
    for x in list(reversed(list(result_p2)))[0:1]:
        p2_result = format(result_p2[x])
        print(p2_result)
    if p1_result > p2_result:
        text = font.render("P1", True, WHITE)
    if p1_result < p2_result:
        text = font.render("P2", True, WHITE)
    if p1_result == p2_result:
        text = font.render("D", True, WHITE)
    surface.blit(text, [start_x - offset, WindowHeight - offset * 2])
    # Update the screen
    pygame.display.flip()


def spin(surface, go):
    # Generate a spin effect
    for i in range(200):
        for j in range(6):
            draw_dice(surface, j, go)


def main():
    loop = True
    # Declare Global Vars

    start = False
    round = 1
    go = 0
    go_per_round = 2

    pygame.init()
    pygame.display.set_caption("Dice " + MY_VERSION)

    pygame.key.set_repeat(10, 500)

    # Initialise fonts we will use
    font = pygame.font.SysFont('Arial', 50, False, False)
    font2 = pygame.font.SysFont('Arial', 25, False, False)

    current_throw = throw()

    while loop:

        # Control FPS
        clock.tick(5)

        # Draw Dice
        if start:
            draw_dice(dice_surface, current_throw, go)

        # Update Score
        if start:
            update_score(round, go, current_throw)

        # Draw Score
        if start and go == 2:
            draw_score(dice_surface, font, current_throw, font2, go)

        # Round start

        if not start:
            draw_round_message(dice_surface, font2, round)

        # Handle quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    go += 1
                    start = True
                    if go > go_per_round:
                        round += 1
                        go = 1
                        #start = False
                    spin(dice_surface, go)
                    current_throw = throw()
                    #print(go, round)


# Call main
main()