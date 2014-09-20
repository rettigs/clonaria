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
        self.sprite = pyglet.sprite.Sprite(model.get('texture'), batch=State().batch, group=State().group['entity'])

        inertia = pymunk.moment_for_poly(model.get('mass'), model.get('hitbox'), offset=location)
        self.body = pymunk.Body(model.get('mass'), inertia)
        self.shape = pymunk.Poly(self.body, model.get('hitbox'), offset=(-self.sprite.image.width / Const.PPB, -self.sprite.image.height / Const.PPB))
        State().space.add(self.body, self.shape)

        self.model = model
        self.world = world
        self.body.position = location
        self.aWalk = Const.ACCELERATION_WALK
        self.aGravity = Const.ACCELERATION_GRAVITY
        self.aJump = Const.ACCELERATION_JUMP
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
        self.body.apply_impulse(Const.LEFT)

    def walkRight(self):
        self.facing = 'r'
        self.body.apply_impulse(Const.RIGHT)

    def jump(self):
        self.body.apply_impulse(Const.UP * 10)
        if self.againstBlockDown: # We are starting a new jump
            self.stillJumping = True
            self.curJumpTicks = self.maxJumpTicks
            self.body.apply_impulse(self.aJump)
        elif self.stillJumping and self.curJumpTicks > 0 and self.vy > 0: # We are continuing an old jump
            self.curJumpTicks -= 1
            self.body.apply_impulse(Const.ACCELERATION_JUMP_HOLD * self.maxJumpTicks / (self.maxJumpTicks - self.curJumpTicks))
