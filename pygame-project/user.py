from logic import * # So that the user can use preset colors.
# A file meant to be modified by the user, for personal preferences or different workings of the program.

preferences = {
    "noborder": False, # If True, no system window control bar or other border will appear.
    "window": (1366,768),#(800,600),# Specific (width,height) of the window.
    "framerate": 60, # Frames per second target for the game.
    "viewspeed": 5, # How fast the view moves.
    "crosshair": {
        "length": 10, # Length of the perpendicular crosshairs in pixels.
        "multiplier": 2.5,
        "color": WHITE, # (r,b,g) color value for the crosshair (or a predefined color from logic.py).
        "width": 5,
    },
    "volume": 0.5 # The volume of sounds, on a scale of 0 to 1.
}

difficulty = {
    "undead": {
        "hp": 100,
        "speed": 1,
        "wavetime": 10,     # The time between waves in seconds.
        "minwavesize": 2,   # Minimum zombies spawned per wave.
        "maxwavesize": 5,   # Maximum zombies spawned per wave.
    },
    "gunship": {
        "firerate": 150,    # The delay between shots fired in milliseconds.
        "dmgwidth": 50,     # The damage hitbox's width in pixels.
        "dmg": 25,          # The damage of the weapon.     
    },
}

DEBUG = True
