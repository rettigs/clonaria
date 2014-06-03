import os, pyglet, yaml
from const import Const
from model import Model
from singleton import Singleton

@Singleton
class Util(object):

    def __init__(self):
        self.blockModels = self.loadModels("../resources", "block")
        self.entityModels = self.loadModels("../resources", "entity")

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

    def blocksToPixels(self, (x, y)):
        '''Returns the on-screen pixel coordinates to the lower left corner pixel of the given block'''
        return ((x - self.player.x) * Const.PPB + (self.window.width / 2)), (y - self.player.y) * Const.PPB + (self.window.height / 2)
