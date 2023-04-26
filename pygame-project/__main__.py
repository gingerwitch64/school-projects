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
LIGHTGR = (150,150,150)
WHITE = (255,255,255)

thermal_bg = pygame.image.load("./assets/img/thermal-topdown.png")

def clamp(num, min_value, max_value):
    return max(min(num, max_value), min_value)

active = True
entities = []
rotation = 0
inc = 0.01

while active:
    # Quit checker
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            active = False

    pygame.draw.rect(display,DARKGR,(0,0,display_width,display_height))
    pygame.display.update()
    