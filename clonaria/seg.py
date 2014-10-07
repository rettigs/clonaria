from __future__ import division

from vec import *

class Seg(object):
    '''Represents a 2D line segment composed of two Vec vectors/points.'''

    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __int__(self):
        return Seg(int(self.a), int(self.b))

    def __tuple__(self):
        return (self.a, self.b)

    def sort(self):
        '''Returns a new Seg whose points are sorted such that the lower one is always first.'''
        points = sort([self.a, self.b])
        return Seg(points[0], points[1])
