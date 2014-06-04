import os, pyglet, yaml
from const import Const
from model import Model
from singleton import Singleton

@Singleton
class Util(object):

    def __init__(self):
        self.debug = 0
        self.blockModels = self.loadModels("../resources", "block")
        self.entityModels = self.loadModels("../resources", "entity")
        self.batch = pyglet.graphics.Batch()
        self.debugStats = []
        self.blockSprites = {}

    @staticmethod
    def loadModels(path, modeltype):
        '''Loads flyweight models from yaml files given the path and model type'''
        models = {}
        defaultmodel = None
        counter = -1
        for dict in yaml.load_all(open("{}/{}models.yml".format(path, modeltype), 'r')):
            
            counter += 1
            
            # Set the default model
            model = Model(dict)
            models[dict["type"]] = model
            if dict["type"] == "default":
                defaultmodel = model
            elif "defaultmodel" not in dict:
                model.set("defaultmodel", defaultmodel)

            # Load the texture file for each model
            try:
                model.set("texture", pyglet.image.load("{}/images/{}/{}.png".format(path, modeltype, dict["type"])))
            except:
                model.set("texture", pyglet.image.load("{}/images/{}/{}.png".format(path, modeltype, "default")))

        print "Loaded {} {} models".format(counter, modeltype)
        return models

    @staticmethod
    def circle(x, y, r):
        blocks = []
        for ix in xrange(int(x-r), int(x+r)):
            for iy in xrange(int(y-r), int(y+r)):
                if (ix-x)**2 + (iy-y)**2 < r**2:
                    blocks.append((ix, iy))
        return blocks

    def addDebugStats(self, texts):
        '''Adds new debug stats to the HUD'''
        for text in texts:
            number = len(self.debugStats)
            label = pyglet.text.Label(text, font_size=14, color=(228, 228, 0, 255), batch=self.batch)
            self.debugStats.append((number, label, text))

    def updateDebugStats(self):
        '''Updates existing debug stats'''
        for (number, label, text) in self.debugStats:
            label.begin_update()
            label.text = eval(text)
            label.y = self.window.height-(number+1)*16
            label.end_update()

    def blocksToPixels(self, (x, y)):
        '''Returns the on-screen pixel coordinates to the lower left corner pixel of the given block'''
        return ((x - self.player.x) * Const.PPB + (self.window.width / 2)), (y - self.player.y) * Const.PPB + (self.window.height / 2)

    def isBlockOnScreen(self,( x, y)):
        blocksOutHor = self.window.width / 2 / Const.PPB + 1
        blocksOutVert = self.window.height / 2 / Const.PPB + 1
        return x >= int(self.player.x - blocksOutHor) and x < int(self.player.x + blocksOutHor) and y >= int(self.player.y - blocksOutVert) and y < int(self.player.y + blocksOutVert)
