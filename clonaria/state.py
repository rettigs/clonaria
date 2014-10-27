from __future__ import division
import math, os

import pyglet

from const import *
from singleton import *

class State(Singleton):
    '''Global program state'''

    def init(self):

        # Basic program variables
        self.debug = 0
        self.window = None
        self.mouseLoc = None

        # Game world variables
        self.space = None
        self.world = None
        self.player = None
        self.physics_blockCoords = []
        self.physics_edgeCoords = []
        self.physics_edgePhysics = {}

        # Graphics variables
        self.cameraPos = (0, 0) # In block coordinates
        self.blockModels = None
        self.entityModels = None
        self.batch = pyglet.graphics.Batch()
        self.debugStats = []
        self.group = {}
        for x in xrange(Const.NUM_LAYERS):
            self.group['layer{}'.format(x-1)] = pyglet.graphics.OrderedGroup(x-1)
        self.group['entity'] = pyglet.graphics.OrderedGroup(Const.NUM_LAYERS)
        self.group['player'] = pyglet.graphics.OrderedGroup(Const.NUM_LAYERS+1)
        self.group['debug'] = pyglet.graphics.OrderedGroup(Const.NUM_LAYERS+2)
