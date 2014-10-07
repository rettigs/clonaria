from __future__ import division
import copy
import math

import pyglet
from Box2D import *

from state import *
from const import *

class EdgePhysics(object):
    '''Represents the physics model of an edge, or one line segment of a block's hitbox.'''

    def __init__(self, vertices, location):
        self.shape = b2EdgeShape(vertices=vertices)
        self.body = State().space.CreateStaticBody(vertices=vertices, position=location, fixedRotation=True)
        self.fixture = self.body.CreateEdgeFixture(shape=self.shape, friction=0.3)
        self.body.position = location
