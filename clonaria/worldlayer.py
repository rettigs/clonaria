from __future__ import division

import pyglet

from chunk import *
from const import *
from state import *
from util import *

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
        self.chunks[(x, y)] = Chunk(self.world, self, (x, y))

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
        batch = State().batch

        onscreenBlocks = Util.getOnscreenBlocks()

        for (x, y) in onscreenBlocks:
            if self.isValidCoords((x, y)):
                block = self.getBlockAt((x, y))
                if block.get('type') != 'air':
                    sx, sy = Util.blocksToPixels((x, y))
                    if (x, y) in self.blockSprites:
                        oldSprite = self.blockSprites[x, y]
                        oldSprite.position = sx, sy
                        oldSprite.scale = Const.ZOOM * Const.BLOCK_SCALE
                    else:
                        newSprite = pyglet.sprite.Sprite(block.get('texture'), x=sx, y=sy, batch=batch, group=State().group['layer1'])
                        newSprite.scale = Const.ZOOM * Const.BLOCK_SCALE
                        self.blockSprites[x, y] = newSprite

        # Cull blocks sprites that don't need to be drawn.
        for pos in self.blockSprites.keys():
            if pos not in onscreenBlocks:
                del self.blockSprites[pos]
