from random import randrange

# This file is just for things like classes or functions that help make the structure of this project a bit more readable.
# Remember, logic.py is to make things easier for developers, user.py is to make things easier for the end user.

class Coord:
    x = 0
    y = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y

class Bounds:
    min = 0
    max = 0

    def __init__(self, min, max):
        self.min = min
        self.max = max

class Window:
    x = 0
    y = 0
    surface = None

    def __init__(self, x, y, surface):
        self.x = x
        self.y = y
        self.surface = surface

class Undead:
    x = 0
    y = 0
    initx = x
    inity = y
    state = None
    anoff = 0.0 # A (later) randomly generated offset for animation update times.
    hp = 0
    path = []

    def __init__(self, x, y, state, anoff, hp, path):
        self.x = x
        self.y = y
        self.initx = x
        self.inity = y
        self.state = state
        self.anoff = anoff
        self.hp = hp
        self.path = path

def clamp(num, min_value, max_value):
    return max(min(num, max_value), min_value)

def deviate(nums = list[int] | int,dev = int) -> list[int] | int:
    if type(nums) == list and len(nums) == 1:
        return randrange(nums[0]-dev,nums[0]+dev)
    elif type(nums) == int:
        return randrange(nums-dev,nums+dev)
    returnlist = []
    for num in nums:
        returnlist.append(randrange(num-dev,num+dev))
    return returnlist

BLACK = (0,)*3
DARKGR = (25,)*3
LIGHTGR = (150,)*3
WHITE = (255,)*3
MISPRP = (255,1,255)
