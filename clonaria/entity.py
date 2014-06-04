from const import Const
from util import Util

class Entity(object):

    def __init__(self, entityModel, world, location):
        self.entityModel = entityModel
        self.world = world
        self.location = self.x, self.y = location
        self.velocity = self.vx, self.vy = 0, 0
        self.horAccel = Const.HOR_ACCEL

    def draw(self):
        self.entityModel.get('texture').blit(*Util.get().blocksToPixels((self.x, self.y)))

    def left(self):
        self.vx -= self.horAccel

    def right(self):
        self.vx += self.horAccel

    def move(self):
        self.x += self.vx
        self.y += self.vy
