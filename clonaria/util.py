from __future__ import division
import math
import operator
import os

import pyglet
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
            ("--worldtype TYPE", "Choose a world type to generate.  Options: {}".format(Const.WORLD_TYPES))
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
    def distancePoint(a, b):
         ax, ay = a
         bx, by = b
         return math.sqrt((bx-ax)**2 + (by-ay)**2)

    @staticmethod
    def add_tuple(a, b):
        return tuple(map(operator.add, a, b))

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
    def getLineOfSightBlocks((dx, dy), world, loc, l=1, maxblocks=None, maxdistance=None):
        '''Returns a list of all coordinates up to and including the first solid block found in 'world' on layer 'l' at 'loc' in the direction of the unit vector '(dx, dy)'.  Stops checking if maxdistance or maxblocks are specified and reached.  The returned list is ordered from closest to farthest.'''

        blocks = []

        # Special case: Direction is zero. Return current block.
        if dx == 0 and dy == 0:
            if world.isSolidAt(loc, l=l):
                blocks.append(Util.int_tuple(loc))

        # Special case: Direction is vertical or horizontal. Add direction vector to location until solid block is found.
        elif dx == 0 or dy == 0:
            newloc = loc
            while True:
                blocks.append(Util.int_tuple(newloc))
                if world.isSolidAt(newloc, l=l) is not False: break # Stop once we hit a solid block or the edge of the world.
                if maxblocks is not None and len(blocks) >= maxblocks: break # Stop once we hit the maxblocks limit.
                if maxdistance is not None and Util.distancePoint(loc, newloc) >= maxdistance: break # Stop once we hit the maxdistance limit.
                newloc = Util.add_tuple(newloc, (dx, dy))

        # Otherwise, use Bresenham's line algorithm.
        else:
            slope = dy / dx
            x, y = loc
            while True:
                blocks.append(Util.int_tuple((x, y)))
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
        for x in xrange(int(bb.lowerBound[0] - 1), int(bb.upperBound[0] + 2)):
            for y in xrange(int(bb.lowerBound[1] - 1), int(bb.upperBound[1] + 2)):
                if entity.world.isSolidAt((x, y)):
                    blocks.append(Util.int_tuple((x, y)))
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
    def prepareDrawDebugTarget():
        '''Prepares the mouse-targeted debug block to be drawn'''

        State().debugTarget.position = Util.blocksToPixels(Util.pixelsToBlocks(State().mouseLoc))
        State().debugTarget.scale = Const.ZOOM

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
    def isBlockOnScreen((x, y)):
        '''Returns True if the block at the given coordinates is on the screen.'''
        camX, camY = State().cameraPos
        blocksOutHor = State().window.width / 2 / Const.ZOOM / Const.PPB + 1
        blocksOutVert = State().window.height / 2 / Const.ZOOM / Const.PPB + 1
        return x >= int(camX - blocksOutHor) and x < int(camX + blocksOutHor) and y >= int(camY - blocksOutVert) and y < int(camY + blocksOutVert)

    @staticmethod
    def getChunkAt((x, y)):
        '''Returns the coordinates of the chunk containing the block at the given coords.  Does not guarantee that the chunk exists, just that that block would mathematically be there.'''
        return (x//Const.CHUNK_SIZE, y//Const.CHUNK_SIZE)

    @staticmethod
    def getInChunkCoords((x, y)):
        '''Returns the in-chunk coordinates of the block at the given coords.  Does not guarantee that the chunk exists, just that that block would mathematically be there.'''
        return (x%Const.CHUNK_SIZE, y%Const.CHUNK_SIZE)

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
    def prepareDrawDebugPhysicsBlocks():
        '''Prepares physics block markers to be drawn'''
        
        coords = State().physics_blockCoords

        # Stop drawing blocks that are no longer relevant.
        for oldCoords in State().debugPhysicsBlocks.keys():
            if oldCoords not in coords:
                del State().debugPhysicsBlocks[oldCoords]

        # Create new Sprite objects for blocks that are relevant (if they don't already exist).
        for newCoords in coords:
            if newCoords is not None and newCoords not in State().debugPhysicsBlocks:
                newSprite = pyglet.sprite.Sprite(pyglet.image.SolidColorImagePattern(color=(255,255,0,128)).create_image(16, 16), batch=State().batch, group=State().group['debug'])
                State().debugPhysicsBlocks[newCoords] = newSprite

        # Update the properties of each Sprite.
        for coords, sprite in State().debugPhysicsBlocks.iteritems():
            sprite.position = Util.blocksToPixels(coords)
            sprite.scale = Const.ZOOM

    @staticmethod
    def drawDebugPhysicsEntities():
        '''Draws entity hitboxes for debugging.'''
        
        allEntities = [State().player]

        for entity in allEntities:
            #if Util.isBlockOnScreen(entity.body.position):
            hitbox = [Util.blocksToPixels(Util.add_tuple(entity.body.position, coords)) for coords in entity.shape.vertices]
            datalist = Util.createGLDataList(hitbox, (255,0,255,64))
            pyglet.graphics.draw(len(hitbox), pyglet.gl.GL_POLYGON, *datalist)

    @staticmethod
    def createGLDataList(points, color):
        datalist = (('v2f', sum(points, ())), ('c4B', color * len(points)))
        return datalist

    @staticmethod
    def polygonPointsToLines(polygon):
        '''Converts a list of polygon point tuples to a list of polygon line tuples.'''
        lines = []
        for i in xrange(len(polygon)):
            lines.append((polygon[i-1], polygon[i]))
        return lines
