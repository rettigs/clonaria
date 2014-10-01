from __future__ import division
import random

import pyglet
from Box2D import *

from const import *
from state import *
from util import *

class World(object):
    '''Represents a game world as layers of blocks.'''

    def __init__(self, name, size):
        self.name = name
        self.size = self.width, self.height = size
        self.layers = [WorldLayer(self.name, l, (self.width, self.height)) for l in xrange(Const.NUM_LAYERS)]

    def isValidCoords(self, (x, y), l=1):
        return x >= 0 and y >= 0 and x < self.width and y < self.height and l >= 0 and l < Const.NUM_LAYERS

    def getBlockAt(self, (x, y), l=1):
        if self.isValidCoords((x, y), l):
            return self.layers[l].getBlockAt((x, y))
        else:
            return None

    def setBlockAt(self, blockType, (x, y), l=1):
        x = int(x)
        y = int(y)
        if self.isValidCoords((x, y), l):
            self.layers[l].setBlockAt(blockType, (x, y))
            return True
        else:
            return None

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

    def generate(self, worldType='NORMAL'):
        w = self.width
        h = self.height

        air = State().blockModels['air']
        for x in xrange(w):
            for y in xrange(h):
                self.setBlockAt(air, (x, y))

        dirt = State().blockModels['dirt']

        if worldType == 'FLAT':
            for x in xrange(w):
                for y in xrange(int(h/2)):
                    self.setBlockAt(dirt, (x, y))

        elif worldType is 'NORMAL':
            for x in xrange(w):
                for y in xrange(int(h/2 + random.random() * 5)):
                    self.setBlockAt(dirt, (x, y))

            sand = State().blockModels['sand']
            for i in xrange(w*h//400):
                blocks = Util.circle(random.random() * w, random.random() * h, random.random() * 20)
                for block in blocks:
                    if not self.isEmptyAt(block):
                        self.setBlockAt(sand, block)

            gravel = State().blockModels['gravel']
            for i in xrange(w*h//800):
                blocks = Util.circle(random.random() * w, random.random() * h, random.random() * 20)
                for block in blocks:
                    if not self.isEmptyAt(block):
                        self.setBlockAt(gravel, block)

    def prepareDraw(self):
        #for layer in self.layers:
            #layer.prepareDraw()
        self.layers[1].prepareDraw() # TODO: We are currently only using layer 1

class WorldLayer(object):
    '''Represents one layer of a game world as blocks.'''

    def __init__(self, world, layer, size):
        self.world = world
        self.layer = layer
        self.size = self.width, self.height = size
        self.blocks = [[None for x in xrange(self.width)] for y in xrange(self.height)]
        self.blockSprites = {}
    def isValidCoords(self, (x, y)):
        return x >= 0 and y >= 0 and x < self.width and y < self.height

    def getBlockAt(self, (x, y)):
        return self.blocks[x][y]

    def setBlockAt(self, blockType, (x, y)):
        self.blocks[x][y] = blockType 
        if (x, y) in self.blockSprites:
            del self.blockSprites[(x, y)]
        return True

    def isEmptyAt(self, (x, y)):
        return self.getBlockAt((x, y)) == State().blockModels['air']

    def isSolidAt(self, (x, y)):
        return self.getBlockAt((x, y)).get('solid')

    def prepareDraw(self):
        window = State().window
        player = State().player
        blocksOutHor = window.width / 2 / Const.ZOOM / Const.PPB + 1
        blocksOutVert = window.height / 2 / Const.ZOOM / Const.PPB + 1
        batch = State().batch

        for y in xrange(int(player.body.position.y - blocksOutVert), int(player.body.position.y + blocksOutVert)):
            for x in xrange(int(player.body.position.x - blocksOutHor), int(player.body.position.x + blocksOutHor)):
                if self.isValidCoords((x, y)):
                    block = self.blocks[x][y]
                    if block.get('type') != 'air':
                        sx, sy = Util.blocksToPixels((x, y))
                        if (x, y) in self.blockSprites:
                            oldSprite = self.blockSprites[x, y]
                            oldSprite.position = sx, sy
                            oldSprite.scale = Const.ZOOM * Const.BLOCK_SCALE
                        else:
                            newSprite = pyglet.sprite.Sprite(self.blocks[x][y].get('texture'), x=sx, y=sy, batch=batch, group=State().group['layer1'])
                            newSprite.scale = Const.ZOOM * Const.BLOCK_SCALE
                            self.blockSprites[x, y] = newSprite

        for pos in self.blockSprites.keys():
            if not Util.isBlockOnScreen(pos):
                del self.blockSprites[pos]
