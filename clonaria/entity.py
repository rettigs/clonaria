from __future__ import division
import copy, pyglet

from const import Const
from line import Line
from util import Util

class Entity(object):

    def __init__(self, model, world, location):
        self.model = model
        self.world = world
        self.x, self.y = location
        self.vx, self.vy = 0, 0
        self.aWalk = Const.ACCELERATION_WALK
        self.aGravity = Const.ACCELERATION_GRAVITY
        self.aJump = Const.ACCELERATION_JUMP
        self.sprite = pyglet.sprite.Sprite(model.get('texture'), batch=Util().batch, group=Util().group['entity'])
        self.againstBlockDown = False
        self.againstBlockLeft = False
        self.maxJumpTicks = Const.MAX_JUMP_TICKS
        self.curJumpTicks = 0
        self.stillJumping = False

    @property
    def location(self):
        return (self.x, self.y)

    @location.setter
    def location(self, point):
        self.x, self.y = point

    @property
    def velocity(self):
        return (self.vx, self.vy)

    @velocity.setter
    def velocity(self, vector):
        self.vx, self.vy = vector

    def prepareDraw(self):
        sx, sy = Util().blocksToPixels(self.location)
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
            self.vy += Const.ACCELERATION_JUMP_HOLD * self.maxJumpTicks / (self.maxJumpTicks - self.curJumpTicks)

    def applyGravity(self):
        self.vy -= self.aGravity

    def getHitboxScanPoints(self):
        points = []
        for point in self.model.get('hitbox').points:
            points.append(Util.addTuples(point, self.location))
        return points

    def move(self):
        
        self.moveDown()
        self.x += self.vx

    def moveDown(self):
        '''Handle vertical movement and downward block collision'''

        testPlayerLocs = self.getHitboxScanPoints()
        distances = []
        for testPlayerLoc in testPlayerLocs:
            testBlockLoc = Util.getClosestSolidBlockDown(self.world, testPlayerLoc)
            testBlockPoly = copy.copy(self.world.getBlockAt(*testBlockLoc).get('hitbox'))
            testBlockPoly.translate(testBlockLoc)
            testLine = Line((testPlayerLoc[0], testBlockLoc[1] + 1), (testPlayerLoc[0], testBlockLoc[1] - 1))
            intersections = testBlockPoly.intersectLine(testLine)
            for intersection in intersections:
                distances.append(abs(intersection[1] - testPlayerLoc[1]))

        minDistance = min(distances)
        if abs(minDistance) < abs(self.vy) and self.vy < 0:
            self.y -= minDistance
            self.vy = 0
        else:
            self.y += self.vy

        self.againstBlockDown = minDistance == 0
