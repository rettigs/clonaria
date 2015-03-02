from __future__ import division

import random as rand
import time

from const import *
from state import *
from util import *
from worldgen import *
from worldlayer import *

class World(object):
    '''Represents a game world as a list of WorldLayers.'''

    def __init__(self, name, width, height, worldType='NORMAL', seed=time.time()):
        self.name = name
        self.width = width
        self.height = height
        self.worldType = worldType
        self.seed = seed
        self.layers = [WorldLayer(self, l, self.width, self.height) for l in xrange(Const.NUM_LAYERS)]

    def isValidCoords(self, loc, l=1):
        '''Returns True if the given block coords refer to a chunk that actually exists, False otherwise. Layer can be specified as the third element in the location tuple or as an argument.'''
        if len(loc) > 2:
            loc, l = loc[:2], loc[2]
        if l >= 0 and l < len(self.layers):
            return self.layers[l].isValidCoords(loc)
        else:
            return False

    def getBlockAt(self, coords, l=1):
        '''Returns the block at the given coords on the given layer if the coordinates are valid.'''
        coords = Util.int_tuple(coords)
        if self.isValidCoords(coords, l):
            return self.layers[l].getBlockAt(coords)
        else:
            return None

    def setBlockAt(self, blockType, coords, l=1):
        coords = Util.int_tuple(coords)
        if self.isValidCoords(coords, l):

            # If given a string, get the model it refers to.
            if isinstance(blockType, basestring):
                blockType = State().blockModels[blockType]

            return self.layers[l].setBlockAt(blockType, coords)
        else:
            return None

    def breakBlockAt(self, coords, l=1):
        coords = Util.int_tuple(coords)
        if self.isEmptyAt(coords, l):
            blockType = State().blockModels['air']
            result = self.layers[l].setBlockAt(blockType, coords)
            if result:
                pass
                # Spawn block item
            return result
        else:
            return None

    def isEmptyAt(self, (x, y), l=1):
        x = int(x)
        y = int(y)
        if self.isValidCoords((x, y), l):
            return self.layers[l].isEmptyAt((x, y))
        else:
            return None

    def isSolidAt(self, (x, y), l=1):
        x = int(x)
        y = int(y)
        if self.isValidCoords((x, y), l):
            return self.layers[l].isSolidAt((x, y))
        else:
            return None

    def generate(self):
        '''Generates the world.'''
        layer0 = WorldGen(self.width, self.height, seed=self.seed)
        layer1 = WorldGen(self.width, self.height, seed=self.seed)
        if self.worldType == 'SINE':
            layer1.fill(State().blockModels['dirt'])
            layer1.sineMask()
        elif self.worldType == 'NORMAL':
            layer0.fill(State().blockModels['dirt'])
            layer1.rect(State().blockModels['stone'], (0, 0), (self.width, int(self.height*.40)))
            layer1.rect(State().blockModels['dirt'], (0, int(self.height*.40)), (self.width, self.height))
            layer1.splotches(300, blockType=State().blockModels['sand'], minSize=5, maxSize=25)
            layer1.splotches(300, blockType=State().blockModels['gravel'], minSize=5, maxSize=12)
            layer1.splotches(2000, blockType=State().blockModels['stone'], minSize=0, maxSize=5)
            layer1.splotches(2000, blockType=State().blockModels['dirt'], minSize=0, maxSize=5)
            layer0.sineMask()
            layer1.sineMask()
            layer1.genCaves(20)
            layer1.growGrass(height=int(self.height*.40))
        else: # Default to FLAT
            layer1.rect(State().blockModels['air'], (0, self.height//2), (self.width, self.height))
            layer1.rect(State().blockModels['dirt'], (0, 0), (self.width, self.height//2))

        # Copy the worldgen array into the world
        l = self.layers[0]
        for x in xrange(self.width):
            for y in xrange(self.height):
                l.setBlockAtUnsafe(layer0.a[x][y], (x, y))
        l = self.layers[1]
        for x in xrange(self.width):
            for y in xrange(self.height):
                l.setBlockAtUnsafe(layer1.a[x][y], (x, y))

    def prepareDraw(self):
        old = State().visibleChunks
        new = Util.getOnscreenChunks(self)
        State().justVisibleChunks = new - old # All chunks that just became visible
        State().justInvisibleChunks = old - new # All chunks that just became invisible
        State().visibleChunks = new

        #for layer in self.layers:
            #layer.prepareDraw()
        self.layers[0].prepareDraw() # TODO: Draw all layers; fix performance issues with this.
        self.layers[1].prepareDraw() # TODO: Draw all layers; fix performance issues with this.

