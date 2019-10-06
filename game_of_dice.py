""" Version 1.07 - Routine to display a Six Sided Dice
The dice can be thrown and be used for simple games
The current thrown value is shown in white, with the last 15 historical values displayed in Grey
Phil Jones October 2019 - phil.jones.24.4@gmail.com
V1.06 Added historic scores and results to UI
V1.07 Toned down colours
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
result_overall = {}
round = 0

BLACK = (10, 10, 10)
WHITE = (255, 255, 255)
BLUE = (22, 55, 200)
RED = (200, 55, 10)
GREEN = (0, 200, 0)
LIGHT_GREEN = (101, 152, 101)
GREY = (128, 128, 128)
dice_surface = pygame.display.set_mode((WindowWidth, WindowHeight))
clock = pygame.time.Clock()
MY_VERSION = "1.07"

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
                pygame.draw.circle(surface, WHITE, (int(start_x + scale * i), int(start_y + scale * j)), int(scale / 3))
    # Update the screen
    pygame.display.flip()


def draw_round_message(surface, font, round):
    # Wipe Screen
    dice_surface.fill(BLACK)
    text = font.render("SPACE TO START.....", True, RED)
    surface.blit(text, [offset / 2, WindowHeight / 2 - offset])
    pygame.display.flip()


def draw_score(surface, font, current_throw, font2, round):
    # Get historical results
    pad = 4
    offset_px = 0
    if len(result_overall) > 0:
        for x in list(reversed(list(result_overall)))[0:15]:
            #history = font2.render(format(result_overall[x]), True, RED)
            win_indicator = "*"
            draw_indicator = "D"
            draw_indicator_blit = font2.render(draw_indicator, True, GREY)
            win_indicator_blit_p1 = font2.render(win_indicator, True, GREEN)
            win_indicator_blit_p2 = font2.render(win_indicator, True, BLUE)
            if format(result_overall[x]) == "D":
                surface.blit(draw_indicator_blit, [start_x + offset_px + pad -2, WindowHeight - offset * 2])
                offset_px += 20
            if format(result_overall[x]) == "P1":
                surface.blit(win_indicator_blit_p1, [start_x + offset_px + pad +2, WindowHeight - offset * 1.8])
                offset_px += 20
            if format(result_overall[x]) == "P2":
                surface.blit(win_indicator_blit_p2, [start_x + offset_px + pad +2, WindowHeight - offset / 2.5])
                offset_px += 20
    # Get historical scores
    # Print the last 15 values from our p1 and p2 result dictionary
    offset_px = 0
    if len(result_p1) > 0:
        for x in list(reversed(list(result_p1)))[0:15]:
            # Draw dividing lines
            pygame.draw.line(surface, GREY, (start_x + offset_px, WindowHeight - (offset * 2) - pad * 2),
                             (start_x + offset_px, WindowHeight - 5))
            history = font2.render(format(result_p1[x]), True, GREEN)
            surface.blit(history, [start_x + offset_px + pad, WindowHeight - offset * 1.5])
            offset_px += 20

    offset_px = 0
    if len(result_p2) > 0:
        for x in list(reversed(list(result_p2)))[0:15]:
            history = font2.render(format(result_p2[x]), True, BLUE)
            surface.blit(history, [start_x + offset_px + pad, WindowHeight - offset ^ 2 * 2])
            offset_px += 20

    # Extract the last winner
    for x in list(reversed(list(result_p1)))[0:1]:
        p1_result = format(result_p1[x])
    for x in list(reversed(list(result_p2)))[0:1]:
        p2_result = format(result_p2[x])


    # Calculate Winner Now
    won = "D"
    if p1_result > p2_result:
        text = font.render("P1", True, GREEN)
        text2 = font2.render("WON",True, GREEN)
        surface.blit(text2, [offset / 64, WindowHeight - 30])
        won = "P1"
    if p1_result < p2_result:
        text = font.render("P2", True, BLUE)
        text2 = font2.render("WON", True, BLUE)
        surface.blit(text2, [offset / 64, WindowHeight - 30])
        won = "P2"
    if p1_result == p2_result:
        text = font.render("D", True, WHITE)
        won = "D"
    surface.blit(text, [offset / 64, WindowHeight - 80])

    # Display the round number
    round_blit = font2.render("R: " + str(round), True, RED)
    surface.blit(round_blit, [offset / 16, WindowHeight - 100])

    # Update the screen
    pygame.display.flip()

    # Record overall round results and return dict (for future use)
    d = {"round " + str(round): won}
    result_overall.update(dict(d))

    return (result_overall)

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
            overall = draw_score(dice_surface, font, current_throw, font2, round)
            # To do overall dict can be called by something in the UI to summarise the round results
            #print(overall)

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