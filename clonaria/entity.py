from __future__ import division
import copy
import math

import pyglet
from Box2D import *

from const import *
from util import *

class Entity(object):
    '''Represents an entity in the world, including its graphics and physics models.'''

    def __init__(self, model, world, location):
        self.sprite = pyglet.sprite.Sprite(model.get('texture'), batch=State().batch, group=State().group['entity'])
        self.offset = (-self.sprite.image.width / Const.PPB, -self.sprite.image.height / Const.PPB)

        self.body = State().space.CreateDynamicBody(position=location, fixedRotation=True)
        self.shape = b2PolygonShape(vertices=[Util.add_tuple(p, self.offset) for p in model.get('hitbox')])
        self.fixture = self.body.CreatePolygonFixture(shape=self.shape, density=1, friction=0.3)

        self.model = model
        self.world = world
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
        self.body.ApplyLinearImpulse(impulse=(-Const.ACCELERATION_WALK, 0), point=self.body.worldCenter, wake=True)

    def walkRight(self):
        self.facing = 'r'
        self.body.ApplyLinearImpulse(impulse=(Const.ACCELERATION_WALK, 0), point=self.body.worldCenter, wake=True)

    def jump(self):
        self.body.ApplyLinearImpulse(impulse=(0, Const.ACCELERATION_JUMP), point=self.body.worldCenter, wake=True)
        if self.againstBlockDown: # We are starting a new jump
            self.stillJumping = True
            self.curJumpTicks = self.maxJumpTicks
            self.body.apply_impulse(self.aJump)
        elif self.stillJumping and self.curJumpTicks > 0 and self.vy > 0: # We are continuing an old jump
            self.curJumpTicks -= 1
            self.body.apply_impulse(Const.ACCELERATION_JUMP_HOLD * self.maxJumpTicks / (self.maxJumpTicks - self.curJumpTicks))
