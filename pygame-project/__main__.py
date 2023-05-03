import pygame, time, pathlib
from pygame.locals import *
from logic import *
relpath = pathlib.Path(__file__).parent.resolve() # This allows the game to be run from any directory and not have issues finding assets.
clock = pygame.time.Clock()
pygame.init()
display = Window(800,600,None)
display.surface = pygame.display.set_mode((display.x,display.y))
pygame.display.set_caption("ZGSClone")
framerate = 60

TRANS = (0,)*4 # 4th value is alpha
BLACK = (0,)*3
DARKGR = (25,)*3
LIGHTGR = (150,)*3
WHITE = (255,)*3
MISPRP = (255,1,255)

thermal_bg = pygame.image.load(f"{relpath}/assets/img/thermal-topdown.png") # Need to check windows compatability.

view = Coord(0,0)
viewspeed = 5
entities = []

last_time = time.time()
pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0)) # Credit to Rockybilly via stackoverflow: https://stackoverflow.com/a/40628090/16863801

active = True
while active:
    dt = (time.time() - last_time) * framerate
    last_time = time.time()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            active = False
    
    pressedKeys = pygame.key.get_pressed()
    if pressedKeys[K_ESCAPE]:
        active = False
    if pressedKeys[K_RIGHT]:
        view.x += viewspeed
    if pressedKeys[K_LEFT]:
        view.x -= viewspeed
    if pressedKeys[K_UP]:
        view.y -= viewspeed
    if pressedKeys[K_DOWN]:
        view.y += viewspeed
    if pressedKeys[K_d]: # Debug - get current coords (plan to add other info as well)
        print(view.x,view.y,dt)
    if pressedKeys[K_g]: # Goto coords
        goto = input("Input coords exactly as (excluding the quotation marks) \"x,y\":")
        goto = goto.split(",")
        if goto == "":
            print("Nothing specified; passing")
            pass
        elif len(goto) != 2:
            print(f"{len(goto)} parameters specified: requires 2")
        else:
            goto = Coord(int(goto[0]),int(goto[1]))
            view.x = goto.x
            view.y = goto.y

    view.x = clamp(view.x,0,thermal_bg.get_width()-display.x)
    view.y = clamp(view.y,0,thermal_bg.get_height()-display.y)
    
    pygame.draw.rect(display.surface,MISPRP,(0,0,display.x,display.y))
    pygame.Surface.blit(display.surface,thermal_bg,(-view.x,-view.y))
    pygame.display.update()
    clock.tick(framerate)
