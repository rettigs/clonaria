from __future__ import division
import math
import operator
import os

import numpy
import pyglet
from pyglet.gl import *
import yaml

from edge import *
from const import *
from model import *
from state import *

class Util(object):
    '''Utility class with various helpful functions.'''

    @staticmethod
    def showHelp():
        '''Prints command line usage help.'''
        helpLines = [
            ("-h, --help", "Shows this help."),
            ("-d", "Displays debug information in-game."),
            ("--worldtype TYPE", "Choose a world type to generate. Options: {}".format(Const.WORLD_TYPES)),
            ("--seed STRING", "Specify a world seed to use. Uses system time by default.")
        ]
        for line in helpLines:
            print "{:<16}\t{}".format(*line)

    @staticmethod
    def loadModels(modeltype):
        '''Loads flyweight models from yaml files given the model type'''
        models = {}
        defaultmodel = None
        counter = -1
        for dict in yaml.load_all(open("{}/{}models.yml".format(Const.RESOURCE_PATH, modeltype), 'r')):
            
            counter += 1
            dict['modeltype'] = modeltype
            model = Model(dict)
            models[dict['type']] = model
            
            # Set the default model
            if dict['type'] == 'default':
                defaultmodel = model
            elif 'defaultmodel' not in dict:
                model.set('defaultmodel', defaultmodel)

        print "Loaded {} {} models".format(counter, modeltype)
        return models

    @staticmethod
    def circle(x, y, r):
        blocks = []
        for ix in xrange(int(x-r), int(x+r)):
            for iy in xrange(int(y-r), int(y+r)):
                if (ix-x)**2 + (iy-y)**2 < r**2:
                    blocks.append((ix, iy))
        return blocks

    @staticmethod
    def line((x, y), (x2, y2)):
        '''
        Returns a list of all block coordinates between the two points, inclusive, using Brensenham's line algorithm.
        From http://mail.scipy.org/pipermail/scipy-user/2009-September/022602.html
        '''
        steep = 0
        coords = []
        dx = abs(x2 - x)
        if (x2 - x) > 0: sx = 1
        else: sx = -1
        dy = abs(y2 - y)
        if (y2 - y) > 0: sy = 1
        else: sy = -1
        if dy > dx:
            steep = 1
            x,y = y,x
            dx,dy = dy,dx
            sx,sy = sy,sx
        d = (2 * dy) - dx
        for i in range(0,dx):
            if steep: coords.append((y,x))
            else: coords.append((x,y))
            while d >= 0:
                y = y + sy
                d = d - (2 * dx)
            x = x + sx
            d = d + (2 * dy)
        return coords #added by me

    @staticmethod
    def distancePoint(a, b):
         ax, ay = a
         bx, by = b
         return math.sqrt((bx-ax)**2 + (by-ay)**2)

    @staticmethod
    def getAdjacentCoords(loc, world=None, multiLayer=False):
        '''
        Returns all coords directly adjacent to the given coords (i.e. left, right, above, and below).
        If a world is specified, it will only return coordinates valid for the world.
        This works on any "world" object that has a "isValidCoords" method, including World, WorldGen, WorldLayer, and Chunk.
        If multiLayer is enabled, it will also return the coords behind and in front, with the layer in each tuple.
        The layer of the input coords must be specified as the third element in the location tuple if using multiLayer.
        '''
        x, y = loc[:2]
        if multiLayer:
            l = loc[2]
            checkCoords = [(x+1,y,l),(x-1,y,l),(x,y+1,l),(x,y-1,l),(x,y,l+1),(x,y,l-1)]
        else:
            checkCoords = (x+1,y),(x-1,y),(x,y+1),(x,y-1)

        if world is not None:
            validCoords = []
            for coords in checkCoords:
                if world.isValidCoords(coords):
                    validCoords.append(coords)
        else:
            validCoords = checkCoords

        return validCoords

    @staticmethod
    def add_tuple(*args):
        return tuple(map(sum, zip(*args)))

    @staticmethod
    def sub_tuple(a, b):
        return tuple(map(operator.sub, a, b))

    @staticmethod
    def mul_tuple(a, b):
        return tuple(map(operator.mul, a, b))

    @staticmethod
    def div_tuple(a, b):
        return tuple(map(operator.div, a, b))

    @staticmethod
    def int_tuple(a):
        return tuple(map(int, a))

    @staticmethod
    def int_floor(a):
        return tuple(map(int, map(math.floor, a)))

    @staticmethod
    def getLineOfSightBlocks((dx, dy), world, loc, l=1, maxblocks=None, maxdistance=None):
        '''Returns a list of all coordinates up to and including the first solid block found in 'world' on layer 'l' at 'loc' in the direction of the unit vector '(dx, dy)'.  Stops checking if maxdistance or maxblocks are specified and reached.  The returned list is ordered from closest to farthest.'''

        blocks = []

        # Special case: Direction is zero. Return current block.
        if dx == 0 and dy == 0:
            if world.isSolidAt(loc, l=l):
                blocks.append(Util.int_floor(loc))

        # Special case: Direction is vertical or horizontal. Add direction vector to location until solid block is found.
        elif dx == 0 or dy == 0:
            newloc = loc
            while True:
                blocks.append(Util.int_floor(newloc))
                if world.isSolidAt(newloc, l=l) is not False: break # Stop once we hit a solid block or the edge of the world.
                if maxblocks is not None and len(blocks) >= maxblocks: break # Stop once we hit the maxblocks limit.
                if maxdistance is not None and Util.distancePoint(loc, newloc) >= maxdistance: break # Stop once we hit the maxdistance limit.
                newloc = Util.add_tuple(newloc, (dx, dy))

        # Otherwise, use Bresenham's line algorithm.
        else:
            slope = dy / dx
            x, y = loc
            while True:
                blocks.append(Util.int_floor((x, y)))
                if world.isSolidAt((x, y), l=l) is not False: break # Stop once we hit a solid block or the edge of the world.
                if maxblocks is not None and len(blocks) >= maxblocks: break # Stop once we hit the maxblocks limit.
                if maxdistance is not None and Util.distancePoint(loc, (x, y)) >= maxdistance: break # Stop once we hit the maxdistance limit.
                x += dx
                y = slope * (x - loc[0]) + loc[1]
            
        return blocks

    @staticmethod
    def getClosestSolidBlock((dx, dy), world, loc, l=1, maxdistance=None):
        '''Returns the coordinates of the closest solid block in 'world' on layer 'l' at 'loc' in the direction of the unit vector '(dx, dy)'.  Stops checking if maxdistance is specified and reached.'''
        blocks = Util.getLineOfSightBlocks((dx, dy), world, loc, l, maxdistance=maxdistance)
        if len(blocks) == 0: return None
        else: return blocks[-1]

    @staticmethod
    def getNearbySolidBlocks(entity):
        bb = entity.shape.getAABB(entity.body.transform, 0)
        blocks = []
        for x in xrange(int(bb.lowerBound[0] - 2), int(bb.upperBound[0] + 2)):
            for y in xrange(int(bb.lowerBound[1] - 2), int(bb.upperBound[1] + 2)):
                if entity.world.isSolidAt((x, y)):
                    blocks.append(Util.int_floor((x, y)))
        return blocks

    @staticmethod
    def getSurroundingBlocks(coords, r=1):
        '''Returns the blocks around (in square formation) the given block coordinates within the given range r, not including the center block.'''
        x, y = Util.int_floor(coords)
        blocks = []
        for bx in xrange(x-r, x+r+1):
            for by in xrange(y-r, y+r+1):
                blocks.append((bx, by))
        blocks.remove(coords)
        return blocks

    @staticmethod
    def addDebugStats(texts):
        '''Adds new debug stats to the HUD'''
        for text in texts:
            number = len(State().debugStats)
            label = pyglet.text.Label(text, font_size=14, color=(228, 228, 0, 255), batch=State().batch, group=State().group['debug'])
            State().debugStats.append((number, label, text))

    @staticmethod
    def prepareDrawDebugStats():
        '''Updates existing debug stats to prepare the for drawing'''
        for (number, label, text) in State().debugStats:
            label.begin_update()
            label.text = eval(text)
            label.y = State().window.height-(number+1)*16
            label.end_update()

    @staticmethod
    def getScreenCenter():
        '''Returns the on-screen pixel coordinates to the pixel in the middle of the screen'''
        return (State().window.width / 2, State().window.height / 2)

    @staticmethod
    def blocksToPixels((bx, by)):
        '''Returns the on-screen pixel coordinates to the lower left corner pixel of the given block'''
        camX, camY = State().cameraPos
        px = (bx - camX) * Const.PPB * Const.ZOOM + (State().window.width / 2)
        py = (by - camY) * Const.PPB * Const.ZOOM + (State().window.height / 2 + 1)
        return (px, py)

    @staticmethod
    def pixelsToBlocks((px, py)):
        '''Returns the world coordinates of the block at the given on-screen pixel coordinates'''
        camX, camY = State().cameraPos
        bx = math.floor((math.floor(px) - (State().window.width / 2)) / Const.PPB / Const.ZOOM + camX)
        by = math.floor((math.floor(py) - (State().window.height / 2)) / Const.PPB / Const.ZOOM + camY)
        return (bx, by)

    @staticmethod
    def blocksToChunks((x, y)):
        '''Returns the coordinates of the chunk containing the block at the given coords.  Does not guarantee that the chunk exists, just that that block would mathematically be there.'''
        return (x//Const.CHUNK_SIZE, y//Const.CHUNK_SIZE)

    @staticmethod
    def chunksToBlocks((x, y)):
        '''Returns the coordinates of the lower-left-most block in the chunk at the given chunk coords.'''
        return (x*Const.CHUNK_SIZE, y*Const.CHUNK_SIZE)

    @staticmethod
    def getInChunkCoords((x, y)):
        '''Returns the in-chunk coordinates of the block at the given coords.  Does not guarantee that the chunk exists, just that that block would mathematically be there.'''
        return (x%Const.CHUNK_SIZE, y%Const.CHUNK_SIZE)

    @staticmethod
    def getOnscreenBlocks():
        '''Returns a list of (x, y) coordinates to all blocks that are onscreen.'''
        window = State().window
        camX, camY = State().cameraPos
        blocksOutHor = window.width / 2 / Const.ZOOM / Const.PPB + 1
        blocksOutVert = window.height / 2 / Const.ZOOM / Const.PPB + 1

        blocks = []

        for y in xrange(int(camY - blocksOutVert), int(camY + blocksOutVert)):
            for x in xrange(int(camX - blocksOutHor), int(camX + blocksOutHor)):
                blocks.append((x, y))

        return blocks

    @staticmethod
    def isBlockOnScreen(coords):
        '''Returns True if the block at the given coordinates is on the screen.'''
        return coords in Util.getOnscreenBlocks()

    @staticmethod
    def isBlockOnScreen2((x, y)):
        '''Returns True if the block at the given coordinates is on the screen.'''
        window = State().window
        camX, camY = State().cameraPos
        blocksOutHor = window.width / 2 / Const.ZOOM / Const.PPB + 1
        blocksOutVert = window.height / 2 / Const.ZOOM / Const.PPB + 1

        xmin = int(camX - blocksOutHor)
        xmax = int(camX + blocksOutHor)
        ymin = int(camY - blocksOutVert)
        ymax = int(camY + blocksOutVert)

        return xmin < x and x < xmax and ymin < y and y < ymax

    @staticmethod
    def getOnscreenChunks(world):
        '''Returns a list of (x, y) coordinates to all chunks that are onscreen. Uses world.width and world.height to validate the coords.'''
        window = State().window
        camX, camY = State().cameraPos
        blocksOutHor = window.width / 2 / Const.ZOOM / Const.PPB + 1
        blocksOutVert = window.height / 2 / Const.ZOOM / Const.PPB + 1

        chunks = set()

        xmin = int(max(camX - blocksOutHor, 0))
        xmax = int(min(camX + blocksOutHor, world.width))
        ymin = int(max(camY - blocksOutVert, 0))
        ymax = int(min(camY + blocksOutVert, world.height))

        for y in xrange(ymin, ymax+Const.CHUNK_SIZE, Const.CHUNK_SIZE):
            for x in xrange(xmin, xmax+Const.CHUNK_SIZE, Const.CHUNK_SIZE):
                chunks.add((x//Const.CHUNK_SIZE, y//Const.CHUNK_SIZE))

        return chunks

    @staticmethod
    def isChunkOnScreen(coords):
        '''Returns True if the chunk at the given coordinates is on the screen.'''
        return coords in Util.getOnscreenChunks()

    @staticmethod
    def isChunkOnScreen2((cx, cy)):
        '''Returns True if the chunk at the given coordinates is on the screen.'''
        window = State().window
        camX, camY = State().cameraPos
        blocksOutHor = window.width / 2 / Const.ZOOM / Const.PPB + 1 + Const.CHUNK_SIZE
        blocksOutVert = window.height / 2 / Const.ZOOM / Const.PPB + 1 + Const.CHUNK_SIZE

        xmin = int(camX - blocksOutHor)
        xmax = int(camX + blocksOutHor)
        ymin = int(camY - blocksOutVert)
        ymax = int(camY + blocksOutVert)

        cx *= Const.CHUNK_SIZE
        cy *= Const.CHUNK_SIZE

        return xmin < cx and cx < xmax and ymin < cy and cy < ymax

    @staticmethod
    def physics_getBlockCoords(entities):
        '''Returns a list of block coordinates to be used for physics calculations based on those nearest to entities.'''
        blocks = []
        for entity in entities:
            #blocks.append(Util.getClosestSolidBlock(entity.body.velocity.normalized(), entity.world, entity.body.position))
            #blocks.append(Util.getClosestSolidBlock(Const.DOWN, entity.world, entity.body.position))
            blocks.extend(Util.getNearbySolidBlocks(entity))

        return blocks

    @staticmethod
    def physics_getEdgeCoords(entities):
        '''Returns a list of edge coords in (vertices, location) format for blocks near the given entities, one for each line segment of each block's hitbox.  The 'vertices' variable is a tuple of vertices.'''
        coords = Util.physics_getBlockCoords(entities)
        edges = []
        for coord in coords:
            points = State().world.getBlockAt(coord).get('hitbox')
            lines = Util.polygonPointsToLines(points)
            for line in lines:
                edges.append((line, coord))
        return edges

    @staticmethod
    def physics_updateEdgePhysics(newEdgeCoords):
        '''Updates the cache of edges to be used for physics calculations given a list of edges in (vertices, location) format to use.  EdgePhysics objects are created and deleted as necessary.'''

        # Stop simulating edges that are no longer relevant.
        for oldEdgeCoord, oldEdgePhysics in State().physics_edgePhysics.items():
            if oldEdgeCoord not in newEdgeCoords:
                State().space.DestroyBody(oldEdgePhysics.body)
                del State().physics_edgePhysics[oldEdgeCoord]

        # Create new EdgePhysics objects for edges that are relevant (if they don't already exist).
        for newEdgeCoord in newEdgeCoords:
            if newEdgeCoord not in State().physics_edgePhysics:
                State().physics_edgePhysics[newEdgeCoord] = EdgePhysics(list(newEdgeCoord[0]), newEdgeCoord[1])

    @staticmethod
    def drawDebugPhysicsBlocks():
        '''Highlights all blocks currently being used for physics calculations.'''
        coords = State().physics_blockCoords
        for coord in coords:
            points = [Util.blocksToPixels(point) for point in Util.blockToSquarePoints(coord)]
            Util.drawPolygonHighlight(points, Const.COLORS['DEBUG_PHYSICS_BLOCK_HIGHLIGHT'])

    @staticmethod
    def drawDebugPhysicsBlockHitboxes():
        '''Draws the hitboxes of all blocks currently being used for physics calculations.'''
        coords = State().physics_blockCoords
        for coord in coords:
            points = [Util.blocksToPixels(Util.add_tuple(coord, point)) for point in State().world.getBlockAt(coord).get('hitbox')]
            Util.drawPolygonOutline(points, Const.COLORS['DEBUG_PHYSICS_BLOCK_HITBOX'])

    @staticmethod
    def drawDebugTargetBlock():
        '''Highlights the currently targeted block.'''
        coord = Util.pixelsToBlocks(State().mouseLoc)
        points = [Util.blocksToPixels(point) for point in Util.blockToSquarePoints(coord)]
        Util.drawPolygonHighlight(points, Const.COLORS['DEBUG_TARGET_BLOCK_HIGHLIGHT'])

    @staticmethod
    def drawDebugChunkBorders():
        '''Draws chunk borders for debugging.'''
        for _,chunk in numpy.ndenumerate(State().world.layers[1].chunks):
            chunk.drawDebugBorders()

    @staticmethod
    def drawDebugPhysicsEntityHitboxes():
        '''Draws the hitboxes of all entities in the world.'''
        allEntities = [State().player]
        for entity in allEntities:
            entity.drawDebugHitbox()

    @staticmethod
    def createGLDataList(points, color):
        datalist = (('v2f', sum(points, ())), ('c4B', color * len(points)))
        return datalist

    @staticmethod
    def drawPolygonOutline(points, color):
        '''Draws the outline of a polygon defined by the given points in pixel coordinates.'''
        for (a, b) in Util.polygonPointsToLines(points):
            data = Util.createGLDataList((a, b), color)
            pyglet.graphics.draw(2, pyglet.gl.GL_LINES, *data)

    @staticmethod
    def drawPolygonHighlight(points, color):
        '''Draws a filled polygon defined by the given points in pixel coordinates.'''
        data = Util.createGLDataList(points, color)
        pyglet.graphics.draw(len(points), pyglet.gl.GL_POLYGON, *data)

    @staticmethod
    def blockToSquarePoints((x, y)):
        '''Returns a list of points that describe the square at the given coordinates.'''
        return [(x, y), (x+1, y), (x+1, y+1), (x, y+1)]

    @staticmethod
    def polygonPointsToLines(polygon):
        '''Converts a list of polygon point tuples to a list of polygon line tuples.'''
        lines = []
        for i in xrange(len(polygon)):
            lines.append((polygon[i-1], polygon[i]))
        return lines
