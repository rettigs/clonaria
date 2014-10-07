from __future__ import division

class Vec(object):
    '''Represents a 2D vector or point.'''

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, v):
        return Vec(self.x + v.x, self.y + v.y)

    def __sub__(self, v):
        return Vec(self.x - v.x, self.y - v.y)

    def __mul__(self, v):
        return Vec(self.x * v.x, self.y * v.y)

    def __truediv__(self, v):
        return Vec(self.x / v.x, self.y / v.y)

    def __div__(self, v):
        return Vec(self.x // v.x, self.y // v.y)

    def __int__(self):
        return Vec(int(self.x), int(self.y))

    def __tuple__(self):
        return (self.x, self.y)
