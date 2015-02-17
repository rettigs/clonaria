from __future__ import division
import math
import random as rand
import time

import numpy

from const import *
from state import *
from util import *

class WorldGen(object):
    '''Array wrapper with various helpful functions for generating worlds.'''

    def __init__(self, width, height, seed=time.time()):
        self.w = width
        self.h = height
        self.seed = seed
        self.b = State().blockModels
        self.a = numpy.empty([self.w, self.h], dtype=type(self.b['air']))

    def fill(self, blocktype=None):
        '''Fills the array with the given block type (air by default).'''
        if blocktype is None:
            blocktype = self.b['air']
        for x in xrange(self.w):
            for y in xrange(self.h):
                self.a[x][y] = blocktype

    def rect(self, blocktype=None, p0=None, p1=None):
        '''Fills the array (or rectangle given by low and high corners, inclusive-exclusive) with the given block type (air by default).'''
        if blocktype is None: blocktype = self.b['air']
        if p0 is None: p0 = (0, 0)
        if p1 is None: p1 = (self.w, self.h)
        x0, y0 = p0
        x1, y1 = p1
        for x in xrange(x0, x1):
            for y in xrange(y0, y1):
                self.a[x][y] = blocktype

    def sineMask(self):
        '''Generates a sum of randomized sine waves and deletes all blocks above it.'''
        air = self.b['air']
        self.sineNumbers = []
        rand.seed(self.seed)
        for n in xrange(10):
            self.sineNumbers.append((rand.randint(1, 20), rand.randint(1, 5), rand.randint(-10, 10)))
        for x in xrange(self.w):
            height = self.h / 2
            for s in self.sineNumbers:
                height += math.sin(x/s[0])*s[1]+s[2]
            for y in xrange(self.h):
                if y > height:
                    self.a[x][y] = air
