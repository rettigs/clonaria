from __future__ import division

import numpy

from const import *
from state import *
from util import *

class Chunk(object):
    '''Represents one 64x64 area of a game world as block Models with optional special data.'''

    def __init__(self, world, layer, location):
        self.world = world
        self.layer = layer
        self.location = location
        self.blocks = numpy.array([[None for x in xrange(Const.CHUNK_SIZE)] for y in xrange(Const.CHUNK_SIZE)])
        self.blockData = {} # Dict with block location tuple as key and a dict of special data as the value.

    def __str__(self):
        return "Chunk({}, {}, {})".format(self.world, self.layer, self.location)

    def __repr__(self):
        return "{}".format(self.location)

    def getBlockAt(self, (x, y)):
        return self.blocks[x][y]

    def setBlockAt(self, blockType, (x, y)):
        self.blocks[x][y] = blockType 
        return True

    def isEmptyAt(self, coords):
        return self.getBlockAt(coords) is State().blockModels['air']

    def isSolidAt(self, coords):
        return self.getBlockAt(coords).get('solid')

    def drawDebugBorders(self):
        cs = Const.CHUNK_SIZE
        x = self.location[0]*cs
        y = self.location[1]*cs
        bPoints = [(x, y), (x+cs, y), (x+cs, y+cs), (x, y+cs)]
        pPoints = [Util.blocksToPixels(point) for point in bPoints]
        Util.drawPolygonOutline(pPoints, Const.COLORS['DEBUG_CHUNK_BORDER'])
