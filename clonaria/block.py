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
        self.body = pymunk.Body()
        self.shape = pymunk.Poly(self.body, model.get('hitbox'), offset=location)

        self.model = model
        self.world = world
        self.body.position = location
