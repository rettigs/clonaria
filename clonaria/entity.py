import pyglet

from const import Const
from util import Util

class Entity(object):

    def __init__(self, entityModel, world, location):
        self.entityModel = entityModel
        self.world = world
        self.location = self.x, self.y = location
        self.velocity = self.vx, self.vy = 0, 0
        self.acceleration = self.ax, self.ay = Const.ACCELERATION_X, Const.ACCELERATION_Y
        sx, sy = Util.get().getScreenCenter()
        self.sprite = pyglet.sprite.Sprite(entityModel.get('texture'), batch=Util.get().batch, group=Util.get().group['player'], x=sx, y=sy)

    def prepareDraw(self):
        self.sprite.scale = Const.ZOOM

    def left(self):
        self.vx -= self.ax

    def right(self):
        self.vx += self.ax

    def move(self):
        self.x += self.vx
        self.y += self.vy
