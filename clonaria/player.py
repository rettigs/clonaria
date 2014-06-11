from __future__ import division
import pyglet

from const import Const
from entity import Entity
from util import Util

class Player(Entity):

    def __init__(self, entityModel, world, location):
        super(Player, self).__init__(entityModel, world, location)
        sx, sy = Util.get().getScreenCenter()
        self.sprite = pyglet.sprite.Sprite(entityModel.get('texture'), batch=Util.get().batch, group=Util.get().group['player'], x=sx, y=sy)

    def prepareDraw(self):
        self.sprite.scale = Const.ZOOM
