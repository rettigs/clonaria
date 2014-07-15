from __future__ import division
import copy
import math

import pyglet
import pymunk

from const import *
from util import *

class Entity(object):
    '''Represents an entity in the world, including its graphics and physics models.'''

    def __init__(self, model, world, location):
        mass = 1
        radius = 1
        inertia = pymunk.moment_for_circle(mass, 0, radius) # 1
        body = pymunk.Body(mass, inertia) # 2
        shape = pymunk.Circle(body, radius) # 4
        State().space.add(body, shape) # 5
        self.body = body

        self.model = model
        self.world = world
        self.body.position = location
        self.aWalk = Const.ACCELERATION_WALK
        self.aGravity = Const.ACCELERATION_GRAVITY
        self.aJump = Const.ACCELERATION_JUMP
        self.sprite = pyglet.sprite.Sprite(model.get('texture'), batch=State().batch, group=State().group['entity'])
        self.facing = 'r'
        self.againstBlockDown = False
        self.againstBlockLeft = False
        self.maxJumpTicks = Const.MAX_JUMP_TICKS
        self.curJumpTicks = 0
        self.stillJumping = False

    def prepareDraw(self):
        self.updateSprite()
        self.sprite.image.anchor_x = self.sprite.image.width / 2
        self.sprite.image.anchor_y = self.sprite.image.height / 2
        sx, sy = Util.blocksToPixels(self.body.position)
        self.sprite.position = sx, sy
        self.sprite.scale = Const.ZOOM * Const.BLOCK_SCALE
        self.sprite.rotation = math.degrees(-self.body.angle)

    def updateSprite(self):
        if self.againstBlockDown:
            action = 'base'
        else:
            action = 'jump'
        self.sprite.image = self.model.get('textures')["{}_{}".format(action, self.facing)]

    def walkLeft(self):
        self.facing = 'l'

    def walkRight(self):
        self.facing = 'r'

    def jump(self):
        if self.againstBlockDown: # We are starting a new jump
            self.stillJumping = True
            self.curJumpTicks = self.maxJumpTicks
            self.vy += self.aJump
        elif self.stillJumping and self.curJumpTicks > 0 and self.vy > 0: # We are continuing an old jump
            self.curJumpTicks -= 1
            self.vy += Const.ACCELERATION_JUMP_HOLD * self.maxJumpTicks / (self.maxJumpTicks - self.curJumpTicks)

    def move(self):
        pass
