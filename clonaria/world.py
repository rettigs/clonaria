from __future__ import division
import random

from Box2D import *
import math
import pyglet
import random as rand

from const import *
from state import *
from util import *

class World(object):
    '''Represents a game world as a list of WorldLayers.'''

    def __init__(self, name, worldType='NORMAL'):
        self.name = name
        self.worldType = worldType
        self.layers = [WorldLayer(self, l) for l in xrange(Const.NUM_LAYERS)]
        
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

    def generateBlock(self, coords, l=1):
        '''Generates the block at the given coords.'''
        return self.layers[l].generateBlock(coords)
        

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

class WorldLayer(object):
    '''Represents one layer of a game world as a collection of Chunks.'''

    def __init__(self, world, layer):
        self.world = world
        self.layer = layer

        # TODO: Make lookups more efficient than using a dictionary?  It needs to support negative indices.
        self.chunks = {} # Dict with chunk coordinates (block coordinates / CHUNK_SIZE) as the key and the Chunk itself as the value.

        # The outermost chunks are kept track of to calculate layer size and are updated whenever a chunk is created.
        self.leftmostChunk = (0, 0)
        self.rightmostChunk = (0, 0)
        self.upmostChunk = (0, 0)
        self.downmostChunk = (0, 0)

        self.blockSprites = {}

    def isValidCoords(self, coords):
        '''Returns True if the given block coords refer to a chunk that either can or does exist, False otherwise.'''
        '''Currently only returns True because the world lacks any hard boundaries, so any chunk can exist.'''
        return True

    def isBlockLoaded(self, coords):
        '''Returns True if the block at the given coords is in a loaded chunk, False otherwise.'''
        return Util.getChunkAt(coords) in self.chunks

    def ensureBlockLoaded(self, coords):
        '''Ensures that the given block is loaded by loading the chunk it is in if it's not already loaded.'''
        if not self.isBlockLoaded(coords):
            return self.loadChunk(Util.getChunkAt(coords))

    def loadChunk(self, coords):
        '''Loads the chunk at the given chunk coordinates from disk, or generates it if it doesn't exist.'''
        return self.generateChunk(coords)

    def saveChunk(self, coords):
        '''Writes the chunk at the given chunk coordinates to disk.'''
        pass

    def unloadChunk(self, coords):
        '''Unloads the chunk at the given chunk coordinates, writing to to disk first.'''
        saveChunk(coords)
        pass

    def getBlockAt(self, coords):
        self.ensureBlockLoaded(coords)
        return self.chunks[Util.getChunkAt(coords)].getBlockAt(Util.getInChunkCoords(coords))

    def setBlockAt(self, blockType, coords):
        self.ensureBlockLoaded(coords)

        if coords in self.blockSprites:
            del self.blockSprites[coords]

        return self.chunks[Util.getChunkAt(coords)].setBlockAt(blockType, Util.getInChunkCoords(coords))

    def setBlockAtUnsafe(self, blockType, coords):
        return self.chunks[Util.getChunkAt(coords)].setBlockAt(blockType, Util.getInChunkCoords(coords))

    def isEmptyAt(self, coords):
        self.ensureBlockLoaded(coords)
        return self.chunks[Util.getChunkAt(coords)].isEmptyAt(Util.getInChunkCoords(coords))

    def isSolidAt(self, coords):
        self.ensureBlockLoaded(coords)
        return self.chunks[Util.getChunkAt(coords)].isSolidAt(Util.getInChunkCoords(coords))

    def generateChunk(self, (x, y)):
        '''Generates all blocks in the chunk at the given coords.'''
        self.chunks[(x, y)] = Chunk(self.world, self)

        wx = x * Const.CHUNK_SIZE
        wy = y * Const.CHUNK_SIZE
        for dx in xrange(Const.CHUNK_SIZE):
            for dy in xrange(Const.CHUNK_SIZE):
                # Add world coordinates of chunk to in-chunk coords of each block to get world coordinates of each block.
                self.generateBlock((wx+dx, wy+dy))

    def generateBlock(self, (x, y)):
        '''Generates the block at the given coords.'''
        if self.world.worldType == 'FLAT':
            if y > 0:
                block = State().blockModels['air']
            else:
                block = State().blockModels['dirt']
            return self.setBlockAtUnsafe(block, (x, y))
        elif self.world.worldType == 'SINE':
            height = 0
            for s in self.world.sineNumbers:
                height += math.sin(x/s[0])*s[1]+s[2]
            if y > height:
                block = State().blockModels['air']
            else:
                block = State().blockModels['dirt']
            return self.setBlockAtUnsafe(block, (x, y))
        else:
            if y > 0:
                block = State().blockModels['air']
            else:
                block = State().blockModels['dirt']
            return self.setBlockAtUnsafe(block, (x, y))

    def prepareDraw(self):
        '''Prepares all blocks in the viewing window to be drawn to the screen.'''
        window = State().window
        player = State().player
        blocksOutHor = window.width / 2 / Const.ZOOM / Const.PPB + 1
        blocksOutVert = window.height / 2 / Const.ZOOM / Const.PPB + 1
        batch = State().batch

        for y in xrange(int(player.body.position.y - blocksOutVert), int(player.body.position.y + blocksOutVert)):
            for x in xrange(int(player.body.position.x - blocksOutHor), int(player.body.position.x + blocksOutHor)):
                if self.isValidCoords((x, y)):
                    block = self.getBlockAt((x, y))
                    if block.get('type') != 'air':
                        sx, sy = Util.blocksToPixels((x, y))
                        if (x, y) in self.blockSprites:
                            oldSprite = self.blockSprites[x, y]
                            oldSprite.position = sx, sy
                            oldSprite.scale = Const.ZOOM * Const.BLOCK_SCALE
                        else:
                            newSprite = pyglet.sprite.Sprite(self.getBlockAt((x, y)).get('texture'), x=sx, y=sy, batch=batch, group=State().group['layer1'])
                            newSprite.scale = Const.ZOOM * Const.BLOCK_SCALE
                            self.blockSprites[x, y] = newSprite

        # Cull blocks sprites that don't need to be drawn.
        for pos in self.blockSprites.keys():
            if not Util.isBlockOnScreen(pos):
                del self.blockSprites[pos]

class Chunk(object):
    '''Represents one 64x64 area of a game world as block Models with optional special data.'''

    def __init__(self, world, layer):
        self.world = world
        self.layer = layer
        self.blocks = [[None for x in xrange(Const.CHUNK_SIZE)] for y in xrange(Const.CHUNK_SIZE)]
        self.blockData = {} # Dict with block location tuple as key and a dict of special data as the value.

    def getBlockAt(self, (x, y)):
        return self.blocks[x][y]

    def setBlockAt(self, blockType, (x, y)):
        self.blocks[x][y] = blockType 
        return True

    def isEmptyAt(self, coords):
        return self.getBlockAt(coords) is State().blockModels['air']

    def isSolidAt(self, coords):
        return self.getBlockAt(coords).get('solid')
