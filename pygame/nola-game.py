import math
import pygame
from pygame.locals import *
pygame.init()
display_width,display_height = 800,600
disp = pygame.display.set_mode((800,600))
pygame.display.set_caption("Pygame Example (Nola)")

def clamp(num, min_value, max_value):
    return max(min(num, max_value), min_value)

wallewidth,walleheight = 200,250
bg = pygame.transform.scale(pygame.image.load("./getty-lab.jpg").convert(), (800,600))
wall_e = pygame.transform.flip(pygame.transform.scale(pygame.image.load("./wall-e.png").convert_alpha(), (wallewidth,walleheight)),True,False)
wall_e_aha = pygame.transform.scale(pygame.image.load("./wall-e-aha.png").convert_alpha(), (wallewidth,walleheight))
walleX,walleY = 300,300
velox = 0
xbounds = { "min":(wallewidth/2), "max":display_width-(wallewidth/2) }

active = True
while active:
    walle_player = wall_e
    support_rect = walle_player.get_rect(center=(walleX,walleY))
    velox = clamp(velox, -2, 2)
    walleX += velox
    # Quit checker
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            active = False
    
    pressedKey = pygame.key.get_pressed()
    if pressedKey[K_LEFT]:
        velox -=.05
    elif pressedKey[K_RIGHT]:
        velox +=.05
    else:
        rinc = .2 # "Return to normal" increment
        if abs(velox) < .2 or clamp(walleX,xbounds["min"],xbounds["max"]) == xbounds["min"] or clamp(walleX,xbounds["min"],xbounds["max"]) == xbounds["max"]:
            velox = 0
        elif velox < 0:
            velox += rinc
        elif velox > 0:
            velox -= rinc

    # Make sure [the robot] is not out of bounds
    if clamp(walleX,xbounds["min"],xbounds["max"]) == xbounds["min"]:
        walleX = xbounds["min"]
    if clamp(walleX,xbounds["min"],xbounds["max"]) == xbounds["max"]:
        walleX = xbounds["max"]
    
    if pressedKey[K_SPACE]:
        walle_player = wall_e_aha
    mouseX,mouseY = pygame.mouse.get_pos()
    deg = abs((math.atan2((mouseY - walleY), (mouseX - walleX)) * (180/math.pi)) - 180)
    walle_player = pygame.transform.rotate(walle_player, deg)
    disp.blit(bg, (0,0)) # Background
    disp.blit(walle_player, (support_rect.x,support_rect.y)) # Sprite
    pygame.display.update()
pygame.display.quit()
pygame.quit()