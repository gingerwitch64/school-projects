import math
from math import sin, cos, radians
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

"""Credit goes this amazing person on stackoverflow: https://stackoverflow.com/a/45511474"""
def rotatePolygon(polygon, degrees):
    """ Rotate polygon the given angle about its center. """
    theta = radians(degrees)  # Convert angle to radians
    cosang, sinang = cos(theta), sin(theta)

    points = polygon
    # find center point of Polygon to use as pivot
    n = len(points)
    cx = sum(p[0] for p in points) / n
    cy = sum(p[1] for p in points) / n

    new_points = []
    for p in points:
        x, y = p[0], p[1]
        tx, ty = x-cx, y-cy
        new_x = ( tx*cosang + ty*sinang) + cx
        new_y = (-tx*sinang + ty*cosang) + cy
        new_points.append([new_x, new_y])

    return new_points

active = True
rotating_square_length = 400
rotating_square_points = [
    [(display_width-rotating_square_length)/2,(display_height-rotating_square_length)/2],
    [(display_width+rotating_square_length)/2,(display_height-rotating_square_length)/2],
    [(display_width+rotating_square_length)/2,(display_height+rotating_square_length)/2],
    [(display_width-rotating_square_length)/2,(display_height+rotating_square_length)/2]
]
entities = []
rotation = 0
inc = 0.01

while active:
    # Quit checker
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            active = False
    
    rotation += inc
    if rotation >= 360:
        rotation = 0
    pygame.draw.rect(display,DARKGR,(0,0,display_width,display_height))
    pygame.draw.polygon(display,WHITE,rotatePolygon(rotating_square_points, rotation))
    pygame.display.update()
    