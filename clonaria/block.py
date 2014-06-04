import pyglet
from const import Const
from util import Util

class Block(pyglet.sprite.Sprite):

    def __init__(self, blockModel, world, location, layer):
        self.blockModel = blockModel
        self.world = world
        self.location = self.bx, self.by = location # In block coordinates
        self.layer = layer
        super(Block, self).__init__(blockModel.get('texture'))

    def get(self, prop):
        return self.blockModel.get(prop)

    def draw(self):
        self.x, self.y = Util.get().blocksToPixels((self.bx, self.by))
        super(Block, self).draw()
