from __future__ import division

import random as rand
import time

from const import *
from state import *
from util import *
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
        
        if self.worldType == 'SINE':
            self.sineNumbers = []
            for n in xrange(10):
                self.sineNumbers.append((rand.randint(1, 20), rand.randint(1, 5), rand.randint(-10, 10)))

    def isValidCoords(self, location, l=1):
        '''Returns True if the given block coords refer to a chunk that actually exists, False otherwise.'''
        if l >= 0 and l < len(self.layers):
            return self.layers[l].isValidCoords(location)
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

    def generate(self):
        '''Generates the world.'''
        w = self.width
        h = self.height
        l = self.layers[1]
        air = State().blockModels['air']
        dirt = State().blockModels['dirt']
        for x in xrange(w):
            for y in xrange(h):
                if y > h/2:
                    l.setBlockAt(air, (x, y))
                else:
                    l.setBlockAt(dirt, (x, y))

    def getAdjacentBlocks(self, (x, y), l=1, multiLayer=False):
        '''Returns all blocks directly adjacent to the block at the given coords.  If multiLayer is enabled, will also return the blocks behind and in front.'''
        blocks = []

        checkCoords = (x+1,y,l),(x-1,y,l),(x,y+1,l),(x,y-1,l)
        if multiLayer:
            checkCoords.extend([(x,y,l+1),(x,y,l-1)])

        for coords in checkCoords:
            block = self.getBlockAt(coords, l=l)
            if block is not None:
                blocks.append(block)

        return blocks

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

    def prepareDraw(self):
        #for layer in self.layers:
            #layer.prepareDraw()
        self.layers[1].prepareDraw() # TODO: Draw all layers; fix performance issues with this.
