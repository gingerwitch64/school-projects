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
wall_e = pygame.transform.scale(pygame.image.load("./wall-e.png").convert_alpha(), (wallewidth,walleheight))
wall_e_aha = pygame.transform.flip(pygame.transform.scale(pygame.image.load("./wall-e-aha.png").convert_alpha(), (wallewidth,walleheight)),True,False)

walleX=300
walleY=300
velox=0

active = True
while active:
    velox = clamp(velox, -2, 2)
    walleX += velox
    walle_player = wall_e
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
        if abs(velox) < .2 or clamp(walleX,0,display_width-wallewidth) == 0 or clamp(walleX,0,display_width-wallewidth) == display_width-wallewidth:
            velox = 0
        elif velox < 0:
            velox += rinc
        elif velox > 0:
            velox -= rinc

    # Make sure [the robot] is not out of bounds
    if clamp(walleX,0,display_width-wallewidth) == 0:
        walleX = 0
    if clamp(walleX,0,display_width-wallewidth) == display_width-wallewidth:
        walleX = display_width-wallewidth
    
    if pressedKey[K_SPACE]:
        walle_player = wall_e_aha
    disp.blit(bg, (0,0)) # Background
    disp.blit(walle_player, (walleX,walleY))
    pygame.display.update()
pygame.display.quit()
pygame.quit()