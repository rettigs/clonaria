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

    def isValidCoords(self, (x, y)):
        '''Returns True if the given block coords are within the world size, False otherwise.'''
        return 0 <= x and x < self.w and 0 <= y and y < self.h

    def setBlocks(self, coords, blockType=None):
        '''Sets all of the blocks at the given coords to the given block type, as long as the coords are valid.'''
        if blockType is None:
            blockType = self.b['air']
        for c in coords:
            if self.isValidCoords(c):
                self.a[c] = blockType

    def fill(self, blockType=None):
        '''Fills the array with the given block type (air by default).'''
        if blockType is None:
            blockType = self.b['air']
        coords = [(x, y) for x in xrange(self.w) for y in xrange(self.h)]
        self.setBlocks(coords, blockType)

    def rect(self, blockType=None, p0=None, p1=None):
        '''Fills the array (or rectangle given by low and high corners, inclusive-exclusive) with the given block type (air by default).'''
        if blockType is None: blockType = self.b['air']
        if p0 is None: p0 = (0, 0)
        if p1 is None: p1 = (self.w, self.h)
        x0, y0 = p0
        x1, y1 = p1
        coords = [(x, y) for x in xrange(x0, x1) for y in xrange(y0, y1)]
        self.setBlocks(coords, blockType)

    def sineMask(self):
        '''Generates a sum of randomized sine waves and deletes all blocks above it.'''
        self.sineNumbers = []
        rand.seed(self.seed)
        for n in xrange(10):
            self.sineNumbers.append((rand.randint(1, 20), rand.randint(1, 5), rand.randint(-10, 10)))
        coords = []
        for x in xrange(self.w):
            height = self.h / 2
            for s in self.sineNumbers:
                height += math.sin(x/s[0])*s[1]+s[2]
            for y in xrange(self.h):
                if y > height:
                    coords.append((x, y))
        self.setBlocks(coords, self.b['air'])

    def splotches(self, count=1, **kwargs):
        '''Draws the given number of splotches.'''
        for i in xrange(count):
            self.splotch(**kwargs)

    def splotch(self, blockType=None, minSize=4, maxSize=20):
        '''Draws a random-size splotch to a random place.'''
        if blockType is None:
            blockType = self.b['air']

        x = rand.randint(0, self.w)
        y = rand.randint(0, self.h)
        r = rand.uniform(minSize, maxSize)

        coords = []
        points = Util.circle(x, y, r)
        for p in points:
            coords.append(p)
        self.setBlocks(coords, blockType)

    def growGrass(self, height=None):
        '''Turns dirt blocks above a certain height into grass blocks if they're open to the air.'''
        if height is None:
            height = self.h/2
        air = self.b['air']
        dirt = self.b['dirt']
        coords = []
        for x in xrange(self.w):
            for y in xrange(height, self.h):
                block = self.a[x][y]
                if block == dirt:
                    openAir = False
                    for p in Util.getAdjacentCoords((x, y)):
                        if self.isValidCoords(p) and self.a[p] == air:
                            openAir = True
                            break
                    if openAir:
                        coords.append((x, y))
        self.setBlocks(coords, self.b['grass'])

    def genCaves(self, count=1):
        '''Draws the given number of caves.'''
        for i in xrange(count):
            self.genCave()

    def genCave(self):
        '''Generates a cave by drawing a random line and expanding it randomly.'''

        # Generate parameters randomly
        # TODO: put in const.py
        expansions = int(rand.triangular(3, 10, 3)) # Iterations to perform
        chance = rand.uniform(.50, .80) # Likelihood of a cave block expanding into a neighbor

        # Start the cave as a random line
        x0 = rand.randint(0, self.w)
        x1 = rand.randint(0, self.w)
        y0 = rand.randint(0, self.h)
        y1 = rand.randint(0, self.h)
        coords = set(Util.line((x0, y0), (x1, y1)))

        # Perform cave expansion iterations
        for e in xrange(expansions):
            newcoords = set()
            for p in coords:
                for ap in Util.getAdjacentCoords(p, world=self):
                    if rand.random() < chance:
                        newcoords.add(ap)
            coords |= newcoords

        # Set all cave blocks to air
        self.setBlocks(coords, self.b['air'])
