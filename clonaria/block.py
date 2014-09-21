from __future__ import division
import copy
import math

import pyglet
from Box2D import *

from const import *

class BlockPhysics(object):
    '''Represents the physics model of a block.'''

    def __init__(self, model, world, location, layer=1):
        from util import *
        self.body = State().space.CreateStaticBody(position=location, fixedRotation=True)
        self.shape = b2PolygonShape(vertices=model.get('hitbox'))
        self.fixture = self.body.CreatePolygonFixture(shape=self.shape, density=1, friction=0.3)

        self.model = model
        self.world = world
        self.body.position = location
