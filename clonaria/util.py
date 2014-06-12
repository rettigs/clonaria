from __future__ import division
import math, os, pyglet, yaml
from const import Const
from model import Model
from singleton import Singleton

class Util(Singleton):

    def init(self):
        self.debug = 0
        self.blockModels = Util.loadModels('block')
        self.entityModels = Util.loadModels('entity')
        self.batch = pyglet.graphics.Batch()
        self.debugStats = []
        self.group = {}
        for x in xrange(Const.NUM_LAYERS):
            self.group['layer{}'.format(x-1)] = pyglet.graphics.OrderedGroup(x-1)
        self.group['entity'] = pyglet.graphics.OrderedGroup(Const.NUM_LAYERS)
        self.group['player'] = pyglet.graphics.OrderedGroup(Const.NUM_LAYERS+1)
        self.group['debug'] = pyglet.graphics.OrderedGroup(Const.NUM_LAYERS+2)

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
    def getClosestBlockDown(world, (x, y), l=1):
        while world.isEmptyAt(x, y, l):
            y -= 1
        return int(x), int(y)

    def addDebugStats(self, texts):
        '''Adds new debug stats to the HUD'''
        for text in texts:
            number = len(self.debugStats)
            label = pyglet.text.Label(text, font_size=14, color=(228, 228, 0, 255), batch=self.batch, group=self.group['debug'])
            self.debugStats.append((number, label, text))

    def updateDebugStats(self):
        '''Updates existing debug stats'''
        for (number, label, text) in self.debugStats:
            label.begin_update()
            label.text = eval(text)
            label.y = self.window.height-(number+1)*16
            label.end_update()

    def getScreenCenter(self):
        '''Returns the on-screen pixel coordinates to the pixel in the middle of the screen'''
        return (self.window.width / 2, self.window.height / 2)

    def blocksToPixels(self, (x, y)):
        '''Returns the on-screen pixel coordinates to the lower left corner pixel of the given block'''
        return ((x - self.player.x) * 1 * Const.PPB * Const.ZOOM + (self.window.width / 2)), (y - self.player.y) * 1* Const.PPB * Const.ZOOM + (self.window.height / 2)

    def isBlockOnScreen(self, (x, y)):
        blocksOutHor = self.window.width / 2 / Const.ZOOM / Const.PPB + 1
        blocksOutVert = self.window.height / 2 / Const.ZOOM / Const.PPB + 1
        return x >= int(self.player.x - blocksOutHor) and x < int(self.player.x + blocksOutHor) and y >= int(self.player.y - blocksOutVert) and y < int(self.player.y + blocksOutVert)
