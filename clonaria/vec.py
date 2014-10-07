from __future__ import division

class Vec(object):
    '''Represents a 2D vector or point.'''

    def __init__(self, x, y=None):
        '''Can be initialized with either an (x, y) tuple or an x and a y.'''
        if y is None:
            object.__setattr__(self, "x", x[0])
            object.__setattr__(self, "y", x[1])
        else:
            object.__setattr__(self, "x", x)
            object.__setattr__(self, "y", y)

    # Make Vec objects "immutable".
    def __setattr__(self, *args):
        raise TypeError
    def __delattr__(self, *args):
        raise TypeError

    def __str__(self):
        return "Vec({}, {})".format(self.x, self.y)

    def __eq__(self, v):
        return self.x == v.x and self.y == v.y

    def __hash__(self):
        return self.tuple.__hash__()

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

    @property
    def int(self):
        return Vec(int(self.x), int(self.y))

    @property
    def tuple(self):
        return (self.x, self.y)
