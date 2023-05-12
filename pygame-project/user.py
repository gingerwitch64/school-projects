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
        "horde": 4,
    },
    "gunship": { # Gunship weapons. Note that a firerate of 0 indicates no shot-to-shot cooldown--fire as fast as you can click.
        """"autocannon": {
            "dmg": 25,
            "radius": 4,
            "firerate": 0.03,
            "overheat": 10,
            "cooldown": 5,
        },
        "cannon": {
            "dmg": 75,
            "radius": 20,
            "firerate": 0,
            "rounds": 4,
            "reload": 6,
        },
        "missile": {
            "dmg": 150,
            "radius": 50,
            "firerate": 0,
            "rounds": 1,
            "reload": 10,
        },"""
    },
}
