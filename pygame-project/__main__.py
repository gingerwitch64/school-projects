import user, pygame, time, pathlib  # Note that "user" is a custom python library for storing user preferences.
from random import randrange    # Using this as apparently it's better than randint() in that it fixes an annoyance.
from pygame.locals import *
from pygame import mixer
from logic import *             # Imports custom classes and constants that allow for ease of reading and code writing.
relpath = pathlib.Path(__file__).parent.resolve()   # This allows the game to be run from any directory and not have issues finding assets.
clock = pygame.time.Clock()     # Used for framerate purposes. See EOF.
pygame.init()
mixer.init()
mixer.music.set_volume(user.preferences["volume"])
display = Window(user.preferences["window"][0],user.preferences["window"][1],None) # Get the x and y dimensions from the tuple in the user preferences
display.surface = pygame.display.set_mode((display.x,display.y))
pygame.display.set_caption("ZGSClone")
framerate = user.preferences["framerate"]
thermal_bg = pygame.transform.scale(pygame.image.load(f"{relpath}/assets/img/thermal_topdown.png"),(1366,768))
undead_rising = pygame.image.load(f"{relpath}/assets/img/undead_rising.png")
undead_walk_1 = pygame.image.load(f"{relpath}/assets/img/undead_walk_1.png")
undead_walk_2 = pygame.image.load(f"{relpath}/assets/img/undead_walk_2.png")
undead_fallen = pygame.image.load(f"{relpath}/assets/img/undead_fallen.png")

special_elite = pygame.font.Font(f"{relpath}/assets/fonts/SpecialElite-Regular.ttf",24) # Load the font needed for the stats UI.

CHAMBER_TIME = user.difficulty["gunship"]["firerate"]
chambered = True
ANIMATE = 750   # These are the event cooldowns in milliseconds.
STATUS = 50     # Status checks to see if undead are dead or alive, and if the latter, moves them.
RISETIME = 1500
WAVE = user.difficulty["undead"]["wavetime"]*1000   # The time between waves spawned.

weaponevent = pygame.USEREVENT + 1      # Gunship/Player events will always have an odd offset,
animationevent = pygame.USEREVENT + 2   # while background/status/undead events will always have an even offset.
statusevent = pygame.USEREVENT + 4      # This will make the addition of new kinds of events (and in turn new mechanics) much simpler.
waveevent = pygame.USEREVENT + 6
riseevent = pygame.USEREVENT + 8

pygame.time.set_timer(animationevent,ANIMATE)   # Here are the actual events.
pygame.time.set_timer(statusevent,STATUS)       # They run infinitely every so and so milliseconds (the constants from earlier).
pygame.time.set_timer(waveevent,WAVE)
pygame.time.set_timer(riseevent,RISETIME)

view = Coord(0,0)
viewspeed = user.preferences["viewspeed"]   # Note that this value is fetched from user.py
entities = []
score = 0 # Your score!
basehp = user.difficulty["base"]["hp"]
initbasehp = basehp
waveinc = user.difficulty["undead"]["wavesizeinc"]

# This is the first undead. Although I used this guy for testing purposes, I think I'll keep him here because there's not much use in removing him.
entities.append(Undead(1111,642,undead_walk_1,randrange(0,20,1)/10,user.difficulty["undead"]["hp"],[(5,deviate([233],10))]))

last_time = time.time()
pygame.mouse.set_visible(False)

active = True
while active:
    dt = (time.time() - last_time) * 60 # These two lines allow for "framerate independence",
    last_time = time.time()             # meaning that the game will act the same way even with lag.
    for event in pygame.event.get():    # These next lines may look complex, but they're just tedious.
        if event.type == pygame.QUIT: active = False
        elif event.type == animationevent:
            for entity in entities:
                if type(entity) == Undead: # These type = Undead statements allow for class attribute recognition in editors such as Visual Studio Code.
                    if   entity.state == undead_walk_1: entity.state = undead_walk_2    # Obviously, here we're just moving from one frame to another.
                    elif entity.state == undead_walk_2: entity.state = undead_walk_1
                    elif entity.state == undead_fallen: entities.remove(entity)         # Removes fallen (dead) undead.
                    elif entity.state == undead_rising: pass
        elif event.type == riseevent:
            for entity in entities:
                if type(entity) == Undead:
                    if entity.state == undead_rising:
                        tempdecider = randrange(1,2,1)  # This is supposed to randomize the starting walking animation for undead,
                        if tempdecider == 1:            # but I don't think it really works right now.
                            entity.state = undead_walk_1
                        elif tempdecider == 2:
                            entity.state = undead_walk_2
        elif event.type == statusevent:
            for entity in entities:
                if type(entity) == Undead:
                    if entity.state == undead_walk_1 or entity.state == undead_walk_2:
                        if entity.x <= 0:   # Removes an undead when it has reached the bounds.
                            entities.remove(entity)
                            score -= 50
                        destination = Coord(entity.path[len(entity.path)-1][0],entity.path[len(entity.path)-1][1])
                        entity.x -= user.difficulty["undead"]["speed"]
                        slope = (entity.inity-destination.y)/(entity.initx-destination.x)   # Unfortunately, as of right now, undead do not move across a line at a speed consistent relative to that line.
                        entity.y = (slope*(entity.x-destination.x))+destination.y           # Their x is changed and their y is set depending on it.
        elif event.type == waveevent:
            i = 0
            wavesize = randrange(user.difficulty["undead"]["minwavesize"]+waveinc,user.difficulty["undead"]["maxwavesize"]+waveinc) # Randomly determines wave size based on user.difficulty min, max and increase over time
            while i < wavesize:
                entities.append(Undead(                     # Here is where the Undead() are created. It seems complex, but again, it's just tedious.
                    deviate(1100,90), deviate(650,90),      # The deviate(a,b) function is from logic.py and randomly chooses a value between a-b and a+b.
                    undead_rising, randrange(0,20,1)/10,    # State is set to risen (player has a bit of time to notice new undead), but that second variable (animation offset) is actually unused.
                    user.difficulty["undead"]["hp"],        # Undead hit points are set here from user.difficulty, and
                    [(5,deviate([233],10))]                 # these are the points of the path for the undead to travel. It is a list, but in reality I've only programmed them to use one point.
                ))
                i += 1  # Repeat until satisfied.
        elif event.type == weaponevent:
            chambered = True

    
    mousex,mousey = pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1] # Get mouse position. This is from before I set up a Coord class to store it in.

    pressedKeys = pygame.key.get_pressed()
    pressedMouse = pygame.mouse.get_pressed()
    if pressedKeys[K_ESCAPE]:   # Escape is an alternative way of quitting the game,
        active = False          # besides using the "X" presented on a window's title bar by most window managers.
    if pressedKeys[K_d]: view.x += viewspeed*dt # Note that "dt" (delta time) is used here--this is what compensates for aforementioned lag.
    if pressedKeys[K_a]: view.x -= viewspeed*dt
    if pressedKeys[K_w]: view.y -= viewspeed*dt
    if pressedKeys[K_s]: view.y += viewspeed*dt
    if pressedKeys[K_SPACE]:
        if chambered == True:
            chambered = False
            mixer.music.load(f"{relpath}/assets/audio/cannon.mp3")
            mixer.music.play()
            pygame.time.set_timer(weaponevent,CHAMBER_TIME)
            hitrect = pygame.rect.Rect(
                mousex-(user.difficulty["gunship"]["dmgwidth"]/2),
                mousey-(user.difficulty["gunship"]["dmgwidth"]/2),
                user.difficulty["gunship"]["dmgwidth"],
                user.difficulty["gunship"]["dmgwidth"]
                )
            for entity in entities:
                if type(entity) == Undead:
                    if type(entity.state) == pygame.surface.Surface:
                        if hitrect.colliderect(entity.state.get_rect(topleft=(entity.x,entity.y))):
                            entity.hp -= user.difficulty["gunship"]["dmg"]
                            if entity.hp <= 0 and entity.state != undead_fallen:
                                score += 100
                                entity.state = undead_fallen

    if user.DEBUG:
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
        if pressedKeys[K_p]:
            for i in range(len(entities)):
                print(entities[i-1].hp)

    view.x = clamp(view.x,0,thermal_bg.get_width()-display.x) # Values clamped to min 0 as background is img drawn from top left
    view.y = clamp(view.y,0,thermal_bg.get_height()-display.y)

    # Everything after this point is related to actually drawing images and other visuals.

    pygame.draw.rect(display.surface,MISPRP,(0,0,display.x,display.y))
    pygame.Surface.blit(display.surface,thermal_bg,(-view.x,-view.y)) # Values are negative because to move the view right, you need to shift the background left.

    for entity in entities:
        if type(entity) is Undead:
            pygame.Surface.blit(display.surface,entity.state,(entity.x-view.x,entity.y-view.y))

    stats = special_elite.render(f"Base HP: {basehp}/{initbasehp} | Score: {score}",True,WHITE,None)
    display.surface.blit(stats,(10,10))
    
    if True: # This was all written to de-obfuscate the process of drawing some lines. In short, coords are taken and drawn out a-coord-ingly (of course, pun intended).
        c = user.preferences["crosshair"]["length"]
        m = user.preferences["crosshair"]["multiplier"]
        w = user.difficulty["gunship"]["dmgwidth"] # Fundementally, the crosshair width relies on the damage width.
        regdiff = w/2
        perdiff = (m*w)/2
        cross = [
            [(mousex+regdiff,mousey),(mousex+perdiff,mousey)],
            [(mousex-regdiff,mousey),(mousex-perdiff,mousey)],
            [(mousex,mousey+regdiff),(mousex,mousey+perdiff)],
            [(mousex,mousey-regdiff),(mousex,mousey-perdiff)],
            ]
        criss = [
            [(mousex+perdiff,mousey+c),(mousex+perdiff,mousey-c)],
            [(mousex-perdiff,mousey+c),(mousex-perdiff,mousey-c)],
            [(mousex+c,mousey+perdiff),(mousex-c,mousey+perdiff)],
            [(mousex+c,mousey-perdiff),(mousex-c,mousey-perdiff)],
            ]
        for i in range(0,4):
            pygame.draw.line(display.surface,user.preferences["crosshair"]["color"],cross[i][0],cross[i][1],user.preferences["crosshair"]["width"])
            pygame.draw.line(display.surface,user.preferences["crosshair"]["color"],criss[i][0],criss[i][1],user.preferences["crosshair"]["width"])

    pygame.display.update() # Updates the entire display.
    clock.tick(framerate)   # Runs program at a target framerate.
