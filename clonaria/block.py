from __future__ import division
import copy
import math

import pyglet
import pymunk

from const import *
from line import *

class BlockPhysics(object):
    '''Represents the physics model of a block.'''

    def __init__(self, model, world, location, layer=1):
        radius = 1
        body = pymunk.Body()
        self.shape = pymunk.Circle(body, radius)
        self.body = body

        self.model = model
        self.world = world
        self.body.position = location
