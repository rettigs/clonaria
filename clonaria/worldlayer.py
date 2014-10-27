from __future__ import division

import random as rand

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
        return Util.blocksToChunks(coords) in self.chunks

    def ensureBlockLoaded(self, coords):
        '''Ensures that the given block is loaded by loading the chunk it is in if it's not already loaded.'''
        if not self.isBlockLoaded(coords):
            return self.loadChunk(Util.blocksToChunks(coords))

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
        return self.chunks[Util.blocksToChunks(coords)].getBlockAt(Util.getInChunkCoords(coords))

    def setBlockAt(self, blockType, coords):
        self.ensureBlockLoaded(coords)

        if coords in self.blockSprites:
            del self.blockSprites[coords]

        return self.chunks[Util.blocksToChunks(coords)].setBlockAt(blockType, Util.getInChunkCoords(coords))

    def setBlockAtUnsafe(self, blockType, coords):
        return self.chunks[Util.blocksToChunks(coords)].setBlockAt(blockType, Util.getInChunkCoords(coords))

    def isEmptyAt(self, coords):
        self.ensureBlockLoaded(coords)
        return self.chunks[Util.blocksToChunks(coords)].isEmptyAt(Util.getInChunkCoords(coords))

    def isSolidAt(self, coords):
        self.ensureBlockLoaded(coords)
        return self.chunks[Util.blocksToChunks(coords)].isSolidAt(Util.getInChunkCoords(coords))

    def cellIter(self, blocks):
        '''Given a 2D list blocks, performs a cellular automata smoothing iteration.'''
        #expand 'blocks' out in all directions by the number of iterations to do

        w = len(blocks)
        h = len(blocks[0])

        newBlocks = [[None for x in xrange(w)] for y in xrange(h)]
        air = State().blockModels['air']
        dirt = State().blockModels['dirt']
        for x in xrange(w):
            for y in xrange(h):
                numAir = 0
                for (bx, by) in Util.getSurroundingBlocks((x, y)):
                    if blocks[bx%w][by%h] is air:
                        numAir += 1
                if numAir >= Const.WORLDGEN_MIN_NEARBY_AIR_BLOCKS:
                    newBlocks[bx%w][by%h] = air
                else:
                    newBlocks[bx%w][by%h] = dirt

        return newBlocks

    def generateRect(self, (x1, y1), (x2, y2)):
        '''Generates or regenerates all blocks in the rectangle defined by the given lower left and upper right block coordinates.  The upper right block is not included.'''
        iters = Const.WORLDGEN_CELL_ITERS
        w = x2-x1+iters*2
        h = y2-y1+iters*2
        tw = x2-x1
        th = y2-y1
        air = State().blockModels['air']
        dirt = State().blockModels['dirt']
        blocks = [[air for x in xrange(w)] for y in xrange(h)]
        for x in xrange(w):
            for y in xrange(h):
                rand.seed((x1+x, y1+y))
                if rand.random() <= Const.WORLDGEN_AIR_PROBABILITY:
                    blocks[x][y] = air
                else:
                    blocks[x][y] = dirt

        for i in xrange(iters+1):
            print "iter", i
            blocks = self.cellIter(blocks)

        trimmedBlocks = [[None for x in xrange(tw)] for y in xrange(th)]
        for x in xrange(tw):
            for y in xrange(th):
                trimmedBlocks[x][y] = blocks[iters+x][iters+y]

        return trimmedBlocks

    def generateChunk(self, coords):
        '''Generates all blocks in the chunk at the given coords.'''
        self.chunks[coords] = Chunk(self.world, self, coords)

        bx, by = Util.chunksToBlocks(coords)
        newBlocks = self.generateRect((bx, by), (bx+Const.CHUNK_SIZE, by+Const.CHUNK_SIZE))
        for x in xrange(Const.CHUNK_SIZE):
            for y in xrange(Const.CHUNK_SIZE):
                self.setBlockAtUnsafe(newBlocks[x][y], (bx+x, by+y))

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
