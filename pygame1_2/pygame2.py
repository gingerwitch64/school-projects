import pygame, time
from pygame.locals import *
pygame.init()
clock = pygame.time.Clock()
display_width,display_height = 600,600
display = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption("Pygame 2 - Nola Gerold")
framerate = 60

def clamp(num, min_value, max_value):
    return max(min(num, max_value), min_value)

circle_x,circle_y = 100,100
square_x,square_y = 500,500
width = 50
speed = 10

last_time = time.time()

active = True
while active:
    dt = (time.time() - last_time) * 60
    last_time = time.time()
    for event in pygame.event.get():
        if event.type == pygame.QUIT: active = False
    pressedKeys = pygame.key.get_pressed()
    if pressedKeys[K_RIGHT]:    square_x+=speed
    if pressedKeys[K_LEFT]:     square_x-=speed
    if pressedKeys[K_UP]:       square_y-=speed
    if pressedKeys[K_DOWN]:     square_y+=speed
    if pressedKeys[K_d]:    circle_x+=speed
    if pressedKeys[K_a]:    circle_x-=speed
    if pressedKeys[K_w]:    circle_y-=speed
    if pressedKeys[K_s]:    circle_y+=speed
    
    if circle_x > display_width: circle_x = 0
    if circle_x < 0: circle_x = display_width
    if circle_y > display_height: circle_y = 0
    if circle_y < 0: circle_y = display_height

    square_x = clamp(square_x,width,display_width-width)
    square_y = clamp(square_y,width,display_height-width)

    pygame.draw.rect(display,(235,235,235),pygame.rect.Rect(0,0,display_width,display_height))
    pygame.draw.rect(display,(0,200,0),pygame.rect.Rect(square_x-width,square_y-width,width*2,width*2))
    pygame.draw.circle(display,(244,143,177),(circle_x,circle_y),width)
    pygame.draw.line(display,(20,20,20),(square_x,square_y),(circle_x,circle_y),6)
    pygame.display.update()
    clock.tick(framerate)