import math
import pygame
from pygame.locals import *
pygame.init()
display_width,display_height = 800,600
display = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption("Z")

BLACK = (0,0,0)
DARKGR = (25,25,25)
WHITE = (255,255,255)

def clamp(num, min_value, max_value):
    return max(min(num, max_value), min_value)

def delta_line(coord1,coord2):
    return abs(math.sqrt(((coord2[0]-coord1[0])*(coord2[0]-coord1[0]))+((coord2[1]-coord1[1])*(coord2[1]-coord1[1]))))

active = True
rotating_square_points = [[0,0],
                          [0,400],
                          [400,400],
                          [400,0]]
entities = []
inc = 0.1

while active:
    # Quit checker
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            active = False
    
    pygame.draw.rect(display,DARKGR,(0,0,display_width,display_height))

    pygame.draw.polygon(display,WHITE,rotating_square_points)
    rotating_square_points[0][0] += inc
    rotating_square_points[0][1] -= inc
    rotating_square_points[1][0] -= inc
    rotating_square_points[1][1] -= inc
    """rotating_square_points[3][0] += inc
    rotating_square_points[3][1] += inc
    rotating_square_points[2][0] -= inc
    rotating_square_points[2][1] += inc"""
    print(rotating_square_points)
    print(delta_line(rotating_square_points[0],rotating_square_points[1]))
    pygame.display.update()
    