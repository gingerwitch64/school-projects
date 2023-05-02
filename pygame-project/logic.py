class Coord:
    x = 0
    y = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y

def clamp(num, min_value, max_value):
    return max(min(num, max_value), min_value)