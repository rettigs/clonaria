from __future__ import division

import numpy
import pyglet

from const import *
from state import *
from util import *

class Chunk(object):
    '''Represents one 64x64 area of a game world as block Models with optional special data.'''

    def __init__(self, world, layer, location):
        self.world = world
        self.layer = layer
        self.location = location
        self.blocks = numpy.array([[None for y in xrange(Const.CHUNK_SIZE)] for x in xrange(Const.CHUNK_SIZE)])
        self.blockData = {} # Dict with block location tuple as key and a dict of special data as the value.

        self.visible = False
        self.blockSprites = {}

    def __str__(self):
        return "Chunk({}, {}, {})".format(self.world, self.layer, self.location)

    def __repr__(self):
        return "{}".format(self.location)

    def getBlockAt(self, (x, y)):
        return self.blocks[x][y]

    def setBlockAt(self, blockType, coord):
        
        # Set the block
        oldBlock = self.blocks[coord]
        newBlock = blockType
        if newBlock != oldBlock: # Only do things if the new block is different.
            self.blocks[coord] = newBlock

            if self.visible:
                # Delete the old sprite
                if coord in self.blockSprites:
                    del self.blockSprites[coord]
                
                # Create a new sprite if we're not using air
                if newBlock.get('type') != 'air':
                    newSprite = pyglet.sprite.Sprite(newBlock.get('texture'), batch=State().batch, group=State().group['layer{}'.format(self.layer)])
                    self.blockSprites[coord] = newSprite

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

    def onVisible(self):
        self.visible = True

        for x in xrange(Const.CHUNK_SIZE):
            for y in xrange(Const.CHUNK_SIZE):
                # Create a new sprite if we're not using air
                newBlock = self.blocks[x][y]
                if newBlock.get('type') != 'air':
                    newSprite = pyglet.sprite.Sprite(newBlock.get('texture'), batch=State().batch, group=State().group['layer{}'.format(self.layer)])
                    newSprite.scale = Const.BLOCK_SCALE
                    self.blockSprites[(x, y)] = newSprite

    def onInvisible(self):
        self.visible = False
        self.blockSprites = {}

    def prepareDraw(self):
        '''Prepares all block sprites in the chunk to be drawn to the screen by updating their positions and sizes.'''
        for (cx, cy), s in self.blockSprites.iteritems():
            cs = Const.CHUNK_SIZE
            x = self.location[0]*cs + cx
            y = self.location[1]*cs + cy
            s.position = Util.blocksToPixels((x, y))
            if State().perf < 1:
                s.scale = Const.ZOOM * Const.BLOCK_SCALE
