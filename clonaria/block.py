from __future__ import division
import copy
import math

import pyglet
import pymunk

from const import *

class BlockPhysics(object):
    '''Represents the physics model of a block.'''

    def __init__(self, model, world, location, layer=1):
        self.body = world.body
        from util import *
        self.segments = [pymunk.Segment(self.body, a, b, 0) for (a, b) in Util.polygonPointsToLines(model.get('hitbox'))]

        self.model = model
        self.world = world
        self.body.position = location
