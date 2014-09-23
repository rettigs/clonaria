from __future__ import division
import copy
import math

import pyglet
from Box2D import *

from const import *
from util import *

class Chain(object):
    '''Represents a chain of physics segments.'''

    def __init__(self, startLocation, maxLength=5):
        self.maxLength = maxLength
        self.segments = {}



        self.root = ChainSegment(self, )
        
    def getSegment(self, point):
        '''If possible, returns a valid segment that connects at the given location, borders a non-solid block, and isn't already part of the chain, otherwise returns None.'''

        # Get up to 4 solid blocks that surround the given point. If point is within a block, then some effort will be wasted gathering the hitboxes of nearby blocks.
        nearbyBlocks = []
        for offset in [(0,0),(-1,0),(0,-1),(-1,-1)]:
            coords = Util.addTuples(point, offset))
            block = State().world.getBlockAt(coords)
            if block.get('solid'):
                nearbyBlocks.append((coords, block))

        # Put the hitbox lines of each solid nearby block into a set.
        checkLines = Set()
        for coords, block in nearbyBlocks:
            checkLines |= Set([Util.addTuples(coords, p) for p in block.get('hitbox')])

        # Remove hitbox lines that aren't connected with where the chain left off (i.e. those that don't intersect 'point').
        # If a line intersects the point but doesn't start or end at it, split it into two lines that start at point and end at the original line's endpoints.
        for line in checkLines:

        # Remove hitbox lines that are already part of the chain.
        for line in checkLines:
            if self.hasSegment(line):
                checkLines.remove(line)

        # Remove hitbox lines that are not next to a non-solid area.
        for line in checkLines:
            # Get block coords by flooring the other coord of the line (i.e. that isn't 'point')
            # If the point is on an edge, test the block adjacent for whether it's solid and if so, if the hitbox goes up to the edge.  If it's non-solid or if it's solid but outside the hitbox, it's next to a non-solid area.
            # If the point is not on an edge, test if it's outside or intersecting the hitbox.  If it is, it's next to a non-solid area.

        # Return one of the lines, if there are any.
        # TODO: If there are multiple lines, then we are at a possible chain intersection point.  Try and be smart about which line we return here so as to prevent chain intersections.
        if len(checkLines) > 0:
            return checkLines[0]
        else:
            return None




#                # Use the center of the block for calculations.
#                testLocation = Util.addTuples(coords, (0.5, 0.5))
#                # Test all lines that make up the block's hitbox.
#                hitboxLines = nearbyBlock.get('hitbox')
#                while True:
#                    # Get hitbox segment of block that is in between block and nearbyBlock
#                    line = self.returnClosestLine(hitboxBlocks, testLocation)
#                    # If the given segment is already part of the/a chain, remove it from the hitbox and try again
#                    if self.hasSegment(line):
#                        hitboxBlocks.remove(line)
#                    else:
#                        break

    def hasSegment(self, line):
        '''Returns true if a segment for the given line exists in the chain.'''
        return line in self.segments

    def returnClosestLine(lines, location):
        '''Given a location and a list of line segments, the line segment whose vertices are closest to the given location will be returned.'''
        
        pairs = []
        for line in lines:
            distance = 0
            distance += Util.distancePoint(line[0], location)
            distance += Util.distancePoint(line[1], location)
            pairs.append((distance, line))

        pairs.sort() # Sort by distance from location.
        return pairs[0][1] # Return line whose distance is the least of all of the lines.

class ChainSegment(object):
    def __init__(self, chain, segment):
        self.chain = chain
        self.segment = segment
