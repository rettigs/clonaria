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
    def getClosestSolidBlock(step, world, loc, l=1):
        '''Returns the coordinates of the closest solid block in 'world' on layer 'l' at 'loc' in the direction of the unit vector 'step'.'''

        while world.isSolidAt(loc, l=l) is False:
            loc = Util.addTuples(loc, step)
        if world.isSolidAt(loc, l=l):
            return int(loc[0]), int(loc[1])
        else:
            return None

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
    def getPhysicsBlocks(entities):
        '''Returns a list of block coordinates to be used for physics calculations based on those nearest to entities.'''
        blocks = []
        for entity in entities:
            #blocks.append((int(entity.body.position.x), int(entity.body.position.y)))
            #blocks.append(Util.getClosestSolidBlock(entity.body.velocity.normalized(), entity.world, entity.body.position))
            blocks.append(Util.getClosestSolidBlock(Const.DOWN, entity.world, entity.body.position))

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
            if newCoords is not None and newCoords not in State().physicsBlocks:
                newPhysics = BlockPhysics(State().world.getBlockAt(newCoords), State().world, newCoords)
                State().space.add(newPhysics.shape)
                State().physicsBlocks[newCoords] = newPhysics

    @staticmethod
    def prepareDrawDebugPhysicsBlocks():
        '''Prepares physics block markers to be drawn'''
        
        coords = State().physicsBlocks.keys()

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
            sprite.position = Util.blocksToPixels(State().physicsBlocks[coords].body.position)
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
