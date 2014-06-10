import pyglet

from const import Const
from util import Util

class Entity(object):

    def __init__(self, entityModel, world, location):
        self.entityModel = entityModel
        self.world = world
        self.location = self.x, self.y = location
        self.velocity = self.vx, self.vy = 0, 0
        self.aWalk = Const.ACCELERATION_WALK
        self.aGravity = Const.ACCELERATION_GRAVITY
        self.aJump = Const.ACCELERATION_JUMP
        self.sprite = pyglet.sprite.Sprite(entityModel.get('texture'), batch=Util.get().batch, group=Util.get().group['entity'])
        self.againstBlockDown = False
        self.maxJumpTicks = Const.MAX_JUMP_TICKS
        self.curJumpTicks = 0
        self.stillJumping = False

    def prepareDraw(self):
        sx, sy = Util.get().blocksToPixels(self.location)
        self.sprite.position = sx, sy
        self.sprite.scale = Const.ZOOM

    def walkLeft(self):
        self.vx -= self.aWalk

    def walkRight(self):
        self.vx += self.aWalk

    def jump(self):
        if self.againstBlockDown: # We are starting a new jump
            self.stillJumping = True
            self.curJumpTicks = self.maxJumpTicks
            self.vy += self.aJump
        elif self.stillJumping and self.curJumpTicks > 0 and self.vy > 0: # We are continuing an old jump
            self.curJumpTicks -= 1
            self.vy += Const.ACCELERATION_JUMP_HOLD

    def applyGravity(self):
        self.vy -= self.aGravity

    def getClosestBlockDown(self):
        x = self.x
        y = self.y - 1
        while self.world.isEmptyAt(x, y, 1):
            y -= 1
        return int(x), int(y)

    def move(self):
        self.x += self.vx
        diff = self.getClosestBlockDown()[1] - self.y + 1
        if abs(diff) < abs(self.vy) and self.vy < 0:
            self.y += diff
            self.vy = 0
        else:
            self.y += self.vy

        self.againstBlockDown = diff == 0
