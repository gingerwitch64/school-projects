import user, pygame, time, pathlib
from random import randrange
from pygame.locals import *
from logic import * # For classes or constants that allow for ease of reading.
relpath = pathlib.Path(__file__).parent.resolve() # This allows the game to be run from any directory and not have issues finding assets.
clock = pygame.time.Clock()
pygame.init()
display = Window(user.preferences["window"][0],user.preferences["window"][1],None) # Get the x and y dimensions from the tuple in the user preferences
display.surface = pygame.display.set_mode((display.x,display.y))
pygame.display.set_caption("ZGSClone")
framerate = user.preferences["framerate"]
thermal_bg = pygame.transform.scale(pygame.image.load(f"{relpath}/assets/img/thermal_topdown.png"),(1366,768))
undead_rising = pygame.image.load(f"{relpath}/assets/img/undead_rising.png")
undead_walk_1 = pygame.image.load(f"{relpath}/assets/img/undead_walk_1.png")
undead_walk_2 = pygame.image.load(f"{relpath}/assets/img/undead_walk_2.png")
undead_fallen = pygame.image.load(f"{relpath}/assets/img/undead_fallen.png")

ANIMATE = 750
STATUS = 50
RISETIME = 1500
WAVE = user.difficulty["undead"]["wavetime"]*1000
# Gunship/Player events will always have an odd offset, while background/status/undead events will always have an even offset.
# This will make the addition of new kinds of events and in turn new mechanics much simpler.
weaponevent = pygame.USEREVENT + 1
animationevent = pygame.USEREVENT + 2
statusevent = pygame.USEREVENT + 4
waveevent = pygame.USEREVENT + 6
riseevent = pygame.USEREVENT + 8

pygame.time.set_timer(animationevent,ANIMATE)
pygame.time.set_timer(statusevent,STATUS)
pygame.time.set_timer(waveevent,WAVE)
pygame.time.set_timer(riseevent,RISETIME)

view = Coord(0,0)
viewspeed = 5
entities = []
entities.append(Undead(1111,642,undead_walk_1,randrange(0,20,1)/10,user.difficulty["undead"]["hp"],[(5,deviate([233],10))]))

last_time = time.time()
pygame.mouse.set_visible(False)

active = True
while active:
    dt = (time.time() - last_time) * 60
    last_time = time.time()
    for event in pygame.event.get():
        if event.type == pygame.QUIT: active = False
        elif event.type == animationevent:
            for entity in entities:
                if type(entity) == Undead:
                    if   entity.state == undead_walk_1: entity.state = undead_walk_2
                    elif entity.state == undead_walk_2: entity.state = undead_walk_1
                    elif entity.state == undead_fallen: entities.remove(entity)
                    elif entity.state == undead_rising: pass
                        #tempdecider = randrange(1,2,1)
                        #if tempdecider == 1:
                        #    entity.state = undead_walk_1
                        #elif tempdecider == 2:
                        #    entity.state = undead_walk_2
                        #else: print("Warning: Entity ", entity.index(), "is in an invalid state: ", entity.state)
        elif event.type == riseevent:
            for entity in entities:
                if type(entity) == Undead:
                    if entity.state == undead_rising:
                        tempdecider = randrange(1,2,1)
                        if tempdecider == 1:
                            entity.state = undead_walk_1
                        elif tempdecider == 2:
                            entity.state = undead_walk_2
        elif event.type == statusevent:
            for entity in entities:
                if (type(entity) == Undead) and (entity.state != undead_rising):
                    if entity.x <= 0:
                        entities.remove(entity)
                    destination = Coord(entity.path[len(entity.path)-1][0],entity.path[len(entity.path)-1][1])
                    entity.x -= user.difficulty["undead"]["speed"]
                    slope = (entity.inity-destination.y)/(entity.initx-destination.x)
                    entity.y = (slope*(entity.x-destination.x))+destination.y
        elif event.type == waveevent:
            i = 0
            wavesize = randrange(user.difficulty["undead"]["minwavesize"],user.difficulty["undead"]["maxwavesize"])
            while i < wavesize:
                entities.append(Undead(
                    deviate(1100,50), deviate(650,50),
                    undead_rising, randrange(0,20,1)/10,
                    user.difficulty["undead"]["hp"],
                    [(5,deviate([233],10))]
                ))
                i += 1
    
    mousex,mousey = pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]
    
    mousex,mousey = pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]
    pressedKeys = pygame.key.get_pressed()
    if pressedKeys[K_ESCAPE]:
        active = False
    if pressedKeys[K_RIGHT]: view.x += viewspeed*dt
    if pressedKeys[K_LEFT]:  view.x -= viewspeed*dt
    if pressedKeys[K_UP]:    view.y -= viewspeed*dt
    if pressedKeys[K_DOWN]:  view.y += viewspeed*dt
    if pressedKeys[K_d]: # Debug - get current coords (plan to add other info as well)
        print("\nView Coords:",(round(view.x),round(view.y)),"\nMouse Pos (screen):",pygame.mouse.get_pos(),"\nMouse Pos (rel):",(round(view.x)+mousex,round(view.y)+mousey),"\nDelta Time:",round(dt,4))
    if pressedKeys[K_g]: # Goto coords
        goto = input("Input coords exactly as (excluding the quotation marks) \"x,y\":")
        goto = goto.split(",")
        if goto == "":       print("Nothing specified; passing")
        elif len(goto) != 2: print(f"{len(goto)} parameters specified: requires 2")
        else:
            goto = Coord(int(goto[0]),int(goto[1]))
            view.x = goto.x
            view.y = goto.y
    if pressedKeys[K_p]: print("\n", entities, "\n")

    view.x = clamp(view.x,0,thermal_bg.get_width()-display.x) # Values clamped to min 0 as background is img drawn from top left
    view.y = clamp(view.y,0,thermal_bg.get_height()-display.y)
    
    pygame.draw.rect(display.surface,MISPRP,(0,0,display.x,display.y))
    pygame.Surface.blit(display.surface,thermal_bg,(-view.x,-view.y)) # Values are negative because to move the view right, you need to shift the background left.

    for entity in entities:
        if type(entity) is Undead:
            pygame.Surface.blit(display.surface,entity.state,(entity.x-view.x,entity.y-view.y))

    pygame.draw.rect(display.surface,WHITE,pygame.Rect(mousex-40*user.preferences["crosshairmulti"],mousey-20*user.preferences["crosshairmulti"],80*user.preferences["crosshairmulti"],40*user.preferences["crosshairmulti"]),2)
    pygame.display.update()
    clock.tick(framerate)
