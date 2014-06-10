from __future__ import division
import pyglet, random
from block import Block
from const import Const
from util import Util

class World(object):

    def __init__(self, name, size):
        self.name = name
        self.size = self.width, self.height = size
        self.layers = [WorldLayer(self.name, l, (self.width, self.height)) for l in xrange(Const.NUM_LAYERS)]

    def isValidCoords(self, x, y, l):
        return x >= 0 and y >= 0 and x < self.width and y < self.height and l >= 0 and l < Const.NUM_LAYERS

    def getBlockAt(self, x, y, l):
        if self.isValidCoords(x, y, l):
            return self.layers[l].getBlockAt(x, y)
        else:
            return None

    def setBlockAt(self, x, y, l, blockType):
        x = int(x)
        y = int(y)
        if self.isValidCoords(x, y, l):
            self.layers[l].setBlockAt(x, y, blockType)
            return True
        else:
            return False

    def isEmptyAt(self, x, y, l):
        x = int(x)
        y = int(y)
        if self.isValidCoords(x, y, l):
            return self.layers[l].isEmptyAt(x, y)
        else:
            return False

    def isSolidAt(self, x, y, l):
        x = int(x)
        y = int(y)
        if self.isValidCoords(x, y, l):
            return self.layers[l].isSolidAt(x, y)
        else:
            return False


    def generate(self):
        w = self.width
        h = self.height

        air = Util.get().blockModels['air']
        for x in xrange(w):
            for y in xrange(h):
                self.setBlockAt(x, y, 1, air)

        dirt = Util.get().blockModels['dirt']
        for x in xrange(w):
            for y in xrange(int(h/2 + random.random() * 5)):
                self.setBlockAt(x, y, 1, dirt)

        sand = Util.get().blockModels['sand']
        for i in xrange(w*h//400):
            blocks = Util.get().circle(random.random() * w, random.random() * h, random.random() * 20)
            for block in blocks:
                if not self.isEmptyAt(block[0], block[1], 1):
                    self.setBlockAt(block[0], block[1], 1, sand)

        gravel = Util.get().blockModels['gravel']
        for i in xrange(w*h//800):
            blocks = Util.get().circle(random.random() * w, random.random() * h, random.random() * 20)
            for block in blocks:
                if not self.isEmptyAt(block[0], block[1], 1):
                    self.setBlockAt(block[0], block[1], 1, gravel)

    def prepareDraw(self):
        #for layer in self.layers:
            #layer.prepareDraw()
        self.layers[1].prepareDraw() # TODO: We are currently only using layer 1

class WorldLayer(object):

    def __init__(self, world, layer, size):
        self.world = world
        self.layer = layer
        self.size = self.width, self.height = size
        self.blocks = [[None for x in xrange(self.width)] for y in xrange(self.height)]
        self.blockSprites = {}
    def isValidCoords(self, x, y):
        return x >= 0 and y >= 0 and x < self.width and y < self.height

    def getBlockAt(self, x, y):
        return self.blocks[x][y]

    def setBlockAt(self, x, y, blockType):
        #self.blocks[x][y] = Block(Util.get().blockModels[blockType], self.world, (x, y), self.layer)
        self.blocks[x][y] = blockType
        return True

    def isEmptyAt(self, x, y):
        return self.getBlockAt(x, y) == Util.get().blockModels['air']

    def isSolidAt(self, x, y):
        return self.getBlockAt(x, y).get('solid')

    def prepareDraw(self):
        pass
        window = Util.get().window
        player = Util.get().player
        blocksOutHor = window.width / 2 / Const.ZOOM / Const.PPB + 1
        blocksOutVert = window.height / 2 / Const.ZOOM / Const.PPB + 1
        batch = Util.get().batch

        for y in xrange(int(player.y - blocksOutVert), int(player.y + blocksOutVert)):
            for x in xrange(int(player.x - blocksOutHor), int(player.x + blocksOutHor)):
                if x >= 0 and y >= 0:
                    try:
                        block = self.blocks[x][y]
                        if block.get('type') != 'air':
                            sx, sy = Util.get().blocksToPixels((x, y))
                            if (x, y) in self.blockSprites:
                                oldSprite = self.blockSprites[x, y]
                                oldSprite.position = sx, sy
                                oldSprite.scale = Const.ZOOM
                            else:
                                newSprite = pyglet.sprite.Sprite(self.blocks[x][y].get('texture'), x=sx, y=sy, batch=batch, group=Util.get().group['layer0'])
                                newSprite.scale = Const.ZOOM
                                self.blockSprites[x, y] = newSprite
                    except: # Don't crash if we get to the edge of the world, just don't render anything there
                        pass

        for pos in self.blockSprites.keys():
            if not Util.get().isBlockOnScreen(pos):
                del self.blockSprites[pos]
