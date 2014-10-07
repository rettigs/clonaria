from __future__ import division

from vec import *

class Seg(object):
    '''Represents a 2D line segment composed of two Vec vectors/points.'''

    def __init__(self, a, b=None):
        '''Can be initialized with either an (a, b) tuple or an a and a b.'''
        if b is None:
            object.__setattr__(self, "a", a[0])
            object.__setattr__(self, "b", a[1])
        else:
            object.__setattr__(self, "a", a)
            object.__setattr__(self, "b", b)

    # Make Seg objects "immutable".
    def __setattr__(self, *args):
        raise TypeError
    def __delattr__(self, *args):
        raise TypeError

    def __str__(self):
        return "Seg({}, {})".format(self.a, self.b)

    def __eq__(self, s):
        return self.a == s.a and self.b == s.b

    def __hash__(self):
        return self.tuple.__hash__()

    @property
    def int(self):
        return Seg(self.a.int, self.b.int)

    @property
    def tuple(self):
        return (self.a, self.b)

    def sort(self):
        '''Returns a new Seg whose points are sorted such that the lower one is always first.'''
        points = sort([self.a, self.b])
        return Seg(points[0], points[1])
