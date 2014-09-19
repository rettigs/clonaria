from __future__ import division
import math
import os

import pyglet
import yaml

from block import *
from const import *
from model import *
from state import *

class Util(object):
    '''Utility class with various helpful functions.'''

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
    def addTuples(a, b):
        return tuple(map(sum, zip(a, b)))

    @staticmethod
    def int_tuple(a):
        return tuple(map(int, a))

    @staticmethod
    def getLineOfSightBlocks((dx, dy), world, loc, l=1, maxblocks=None, maxdistance=None):
        '''Returns a list of all coordinates up to and including the first solid block found in 'world' on layer 'l' at 'loc' in the direction of the unit vector '(dx, dy)'.  Stops checking if maxdistance or maxblocks are specified and reached.  The returned list is ordered from closest to farthest.'''

        blocks = []

        # Special case: Direction is zero. Return current block.
        if dx == 0 and dy == 0:
            print 'a'
            if world.isSolidAt(loc, l=l):
                blocks.append(Util.int_tuple(loc))

        # Special case: Direction is vertical or horizontal. Add direction vector to location until solid block is found.
        elif dx == 0 or dy == 0:
            print 'b'
            newloc = loc
            while True:
                blocks.append(Util.int_tuple(newloc))
                if world.isSolidAt(newloc, l=l) is not False: break # Stop once we hit a solid block or the edge of the world.
                if maxblocks is not None and len(blocks) >= maxblocks: break # Stop once we hit the maxblocks limit.
                if maxdistance is not None and Util.distancePoint(loc, newloc) >= maxdistance: break # Stop once we hit the maxdistance limit.
                newloc = Util.addTuples(newloc, (dx, dy))

        # Otherwise, use Bresenham's line algorithm.
        else:
            print 'c'
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
        bb = entity.shape.bb
        blocks = []
        for x in xrange(int(bb.left - 1), int(bb.right + 2)):
            for y in xrange(int(bb.bottom - 1), int(bb.top + 2)):
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
    def blocksToPixels((x, y)):
        '''Returns the on-screen pixel coordinates to the lower left corner pixel of the given block'''
        return ((x - State().player.body.position.x) * Const.PPB * Const.ZOOM + (State().window.width / 2)), (y - State().player.body.position.y) * Const.PPB * Const.ZOOM + (State().window.height / 2)

    @staticmethod
    def pixelsToBlocks((x, y)):
        '''Returns the world coordinates of the block at the given on-screen pixel coordinates'''
        return ((int) ((math.floor(x) - (State().window.width / 2)) / Const.PPB / Const.ZOOM + State().player.body.position.x), (int) ((math.floor(y) - (State().window.height / 2)) / Const.PPB / Const.ZOOM + State().player.body.position.y))

    @staticmethod
    def isBlockOnScreen((x, y)):
        blocksOutHor = State().window.width / 2 / Const.ZOOM / Const.PPB + 1
        blocksOutVert = State().window.height / 2 / Const.ZOOM / Const.PPB + 1
        return x >= int(State().player.body.position.x - blocksOutHor) and x < int(State().player.body.position.x + blocksOutHor) and y >= int(State().player.body.position.y - blocksOutVert) and y < int(State().player.body.position.y + blocksOutVert)

    @staticmethod
    def getPhysicsBlockCoords(entities):
        '''Returns a list of block coordinates to be used for physics calculations based on those nearest to entities.'''
        blocks = []
        for entity in entities:
            #blocks.append(Util.getClosestSolidBlock(entity.body.velocity.normalized(), entity.world, entity.body.position))
            #blocks.append(Util.getClosestSolidBlock(Const.DOWN, entity.world, entity.body.position))
            blocks.extend(Util.getNearbySolidBlocks(entity))

        return blocks

    @staticmethod
    def updatePhysicsBlocks(coords):
        '''Update the local cache of blocks to be used for physics calculations given a list of block coordinates to use. BlockPhysics objects are created and deleted as necessary.'''

        # Stop simulating blocks that are no longer relevant.
        for oldCoords, oldPhysics in State().physicsBlocks.items():
            if oldCoords not in coords:
                State().space.remove(oldPhysics.shape)
                del State().physicsBlocks[oldCoords]

        # Create new BlockPhysics objects for blocks that are relevant (if they don't already exist).
        for newCoords in coords:
            if newCoords is not None and newCoords not in State().physicsBlocks and State().world.isSolidAt(newCoords):
                newPhysics = BlockPhysics(State().world.getBlockAt(newCoords), State().world, newCoords)
                State().space.add(newPhysics.shape)
                State().physicsBlocks[newCoords] = newPhysics

    @staticmethod
    def prepareDrawDebugPhysicsBlocks():
        '''Prepares physics block markers to be drawn'''
        
        coords = State().physicsBlockCoords

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
            hitbox = [Util.blocksToPixels((coords.x, coords.y)) for coords in entity.shape.get_vertices()]
            datalist = Util.createGLDataList(hitbox, (255,0,255,64))
            pyglet.graphics.draw(len(hitbox), pyglet.gl.GL_POLYGON, *datalist)

    @staticmethod
    def createGLDataList(points, color):
        datalist = (('v2f', sum(points, ())), ('c4B', color * len(points)))
        return datalist
