from __future__ import division

import math
import random as rand

import numpy
import pyglet

from chunk import *
from const import *
from state import *
from util import *

class WorldLayer(object):
    '''Represents one layer of a game world as a collection of Chunks.'''

    def __init__(self, world, layer, width, height):
        self.world = world
        self.layer = layer
        self.width = width
        self.height = height

        self.chunks = numpy.array([[Chunk(self.world, self.layer, (x, y)) for y in xrange(int(math.ceil(self.height / Const.CHUNK_SIZE)))] for x in xrange(int(math.ceil(self.width / Const.CHUNK_SIZE)))])

        # The outermost chunks are kept track of to calculate layer size and are updated whenever a chunk is created.
        self.leftmostChunk = (0, 0)
        self.rightmostChunk = (0, 0)
        self.upmostChunk = (0, 0)
        self.downmostChunk = (0, 0)

    def isValidCoords(self, (x, y)):
        '''Returns True if the given block coords refer to a chunk that either can or does exist, False otherwise.'''
        return 0 <= x and x < self.width and 0 <= y and y < self.height

    def isValidChunkCoords(self, (x, y)):
        '''Returns True if the given block coords refer to a chunk that either can or does exist, False otherwise.'''
        return 0 <= x and x < self.width/Const.CHUNK_SIZE and 0 <= y and y < self.height/Const.CHUNK_SIZE

    def isBlockLoaded(self, coords):
        '''Returns True if the block at the given coords is in a loaded chunk, False otherwise.'''
        return Util.blocksToChunks(coords) in self.chunks

    def ensureBlockLoaded(self, coords):
        '''Ensures that the given block is loaded by loading the chunk it is in if it's not already loaded.'''
        if not self.isBlockLoaded(coords):
            self.loadChunk(Util.blocksToChunks(coords))

    def loadChunk(self, coords):
        '''Loads the chunk at the given chunk coordinates from disk, or generates it if it doesn't exist.'''
        pass

    def saveChunk(self, coords):
        '''Writes the chunk at the given chunk coordinates to disk.'''
        pass

    def unloadChunk(self, coords):
        '''Unloads the chunk at the given chunk coordinates, writing to to disk first.'''
        saveChunk(coords)
        pass

    def getBlockAt(self, coords):
        #self.ensureBlockLoaded(coords)
        return self.chunks[Util.blocksToChunks(coords)].getBlockAt(Util.getInChunkCoords(coords))

    def setBlockAt(self, blockType, coords):
        #self.ensureBlockLoaded(coords)

        return self.chunks[Util.blocksToChunks(coords)].setBlockAt(blockType, Util.getInChunkCoords(coords))

    def setBlockAtUnsafe(self, blockType, coords):
        return self.chunks[Util.blocksToChunks(coords)].setBlockAt(blockType, Util.getInChunkCoords(coords))

    def isEmptyAt(self, coords):
        self.ensureBlockLoaded(coords)
        return self.chunks[Util.blocksToChunks(coords)].isEmptyAt(Util.getInChunkCoords(coords))

    def isSolidAt(self, coords):
        self.ensureBlockLoaded(coords)
        return self.chunks[Util.blocksToChunks(coords)].isSolidAt(Util.getInChunkCoords(coords))

    def prepareDraw(self):
        '''Prepares all blocks in the viewing window to be drawn to the screen.'''
        
        for coords in State().justVisibleChunks:
            try:
                self.chunks[coords].onVisible()
            except IndexError:
                pass

        for coords in State().justInvisibleChunks: # All chunks that just became invisible
            try:
                self.chunks[coords].onInvisible()
            except IndexError:
                pass

        for coords in State().visibleChunks:
            try:
                self.chunks[coords].prepareDraw()
            except IndexError:
                pass
