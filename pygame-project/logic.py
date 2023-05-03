# This file is just for things like classes or functions that help make the structure of this project a bit more readable.

class Coord:
    x = 0
    y = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y

class Bounds:
    min = 0
    max = 0

    def __init__(self, min, max) -> None:
        self.min = min
        self.max = max

class Window:
    x = 0
    y = 0
    surface = None

    def __init__(self, x, y, surface) -> None:
        self.x = x
        self.y = y
        self.surface = surface

def clamp(num, min_value, max_value):
    return max(min(num, max_value), min_value)

TRANS = (0,)*4
BLACK = (0,)*3
DARKGR = (25,)*3
LIGHTGR = (150,)*3
WHITE = (255,)*3
MISPRP = (255,1,255)
