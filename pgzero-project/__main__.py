import pgzrun
from random import randint
from pgzhelper import *

### Lore ###
# You are on a large cargo spaceship when you take a wrong turn and veer into an asteroid field.
# Unable to back out, you must take fire on asteroids that are drawn towards the mass of your heavy spaceship.
# Hold off as long as possible.

WIDTH,HEIGHT = 800,600
score = 0
hit = 0
miss = 0
hp = 5
inithp = hp
gravity = 2
asteroids = []

laser = Actor("lasercannon.png")
laser.angle = 90

def draw():
    global score,hit,miss,gravity,hp,inithp
    if hp == 0: screen.draw.text(f"Game Over!\nScore: {score}\nHits: {hit}\nMisses: {miss}",center=(WIDTH/2,HEIGHT/2),fontsize=50); return;
    screen.clear()
    bg = Actor("starry-bg.jpg",(0,0),(300,0))
    bg.draw()
    laser.draw()
    display_text = f"Score: {score}; Hits: {hit}; Misses: {miss}; Gravity: {round(gravity,3)}; HP: {hp}/{inithp}"
    screen.draw.text(display_text, (10,10))
    for asteroid in asteroids:
        asteroid.draw()

def update():
    global gravity,hp,asteroids
    if hp == 0: return;
    if len(asteroids) < round(gravity):
        spawn_asteroid()
    for asteroid in asteroids:
        asteroid.y += gravity + (asteroid.randacc)/5
        asteroid.angle += asteroid.spinspeed
        if asteroid.y > HEIGHT:
            asteroids.remove(asteroid)
            hp -= 1
            if hp == 0: music.play_once("gameover.wav"); return;

def on_mouse_down(pos):
    global gravity,score,hit,miss,hp
    if hp == 0: return;
    anything = False
    for asteroid in asteroids:
        if asteroid.collidepoint(pos):
            asteroids.remove(asteroid)
            gravity += 0.01
            score += asteroid.randacc
            hit += 1
            anything = True
            if hit % 10 == 0:
                sounds.pling.play()
    if anything == False:
        miss += 1
    sounds.lasergun.play()

def on_mouse_move(pos):
    global laser
    laser.x = pos[0]
    laser.y = HEIGHT-50

def spawn_asteroid():
    if hp == 0: return;
    global asteroids
    newasteroid = Actor("asteroid.png")
    newasteroid.pos = (randint(10,790), -40)
    newasteroid.angle = randint(0,360)
    newasteroid.spinspeed = randint(1,5)
    newasteroid.randacc = randint(1,10)
    asteroids.append(newasteroid)

pgzrun.go()
