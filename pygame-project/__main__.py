import pygame, time, pathlib
from pygame.locals import *
from logic import *
relpath = pathlib.Path(__file__).parent.resolve() # This allows the game to be run from any directory and not have issues finding assets.
clock = pygame.time.Clock()
pygame.init()
display_width,display_height = 800,600
display = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption("ZGSClone")
framerate = 60

BLACK = (0,0,0)
DARKGR = (25,25,25)
LIGHTGR = (150,150,150)
WHITE = (255,255,255)
MISPRP = (255,1,255)

thermal_bg = pygame.image.load(f"{relpath}/assets/img/thermal-topdown.png") # Need to check windows compatability.

view = Coord(0,0)
viewspeed = 5
active = True
entities = []

last_time = time.time()
pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))


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

    view.x = clamp(view.x,0,566)
    view.y = clamp(view.y,0,280)
    print(view.x,view.y)
    
    pygame.draw.rect(display,MISPRP,(0,0,display_width,display_height))
    pygame.Surface.blit(display,thermal_bg,(-view.x,-view.y))
    pygame.display.update()
    clock.tick(framerate)
