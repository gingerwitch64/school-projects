import pygame
from pygame.locals import *
pygame.init()
display_width,display_height = 600,600
display = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption("Pygame 1 - Nola Gerold")

ellipse_x,ellipse_y = 150,200
circle_x,circle_y = 400,400

active = True
while active:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: active = False
    pygame.draw.rect(display,(230,126,34),pygame.rect.Rect(0,0,display_width,display_height))
    pygame.draw.ellipse(display,(0,200,0),pygame.rect.Rect(ellipse_x/2,ellipse_y/2,ellipse_x,ellipse_y))
    pygame.draw.circle(display,(244,143,177),(circle_x,circle_y),75)
    pygame.draw.line(display,(20,20,20),(ellipse_x,ellipse_y),(circle_x,circle_y),8)
    pygame.display.update()