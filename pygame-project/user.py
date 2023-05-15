# A file meant to be modified by the user, for personal preferences or different workings of the program.

preferences = {
    "noborder": False, # If True, no system window control bar or other border will appear.
    "window": (1366,768),#(800,600), # Specific (width,height) of the window.
    "framerate": 60, # Frames per second target for the game.
    "viewspeed": 5, # How fast the view moves.
    "crosshairmulti": 1, # The size multiplier of the crosshair. Values < 1 will shrink, values > 1 will expand.
    "crosshairrbg": (255,255,255), # (r,b,g) color value for the crosshair.
}

difficulty = {
    "undead": {
        "hp": 100,
        "speed": 1,
        "wavetime": 10, # The time between waves in seconds.
        "minwavesize": 2, # Minimum zombies spawned per wave.
        "maxwavesize": 5, # Maximum zombies spawned per wave.
    },
    "gunship": {
        "firerate": 100, # The delay between shots fired in milliseconds.
        "dmgradius": 10, # The damage radius in pixels of the weapon.
        "dmg": 25, # The damage of the weapon.     
    },
}

DEBUG = True
