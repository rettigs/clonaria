from __future__ import division

import pyglet

from const import *
from entity import *
from state import *
from util import *

class Player(Entity):
    '''Represents the player in the world.'''

    def __init__(self, entityModel, world, location):
        super(Player, self).__init__(entityModel, world, location)
        sc = Util.getScreenCenter()
        self.sprite = pyglet.sprite.Sprite(entityModel.get('texture'), batch=State().batch, group=State().group['player'], x=sc.x, y=sc.y)
