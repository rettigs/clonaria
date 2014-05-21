import pygame, yaml
from singleton import Singleton
from model import Model

@Singleton
class Util(object):
    def __init__(self):
        self.blockModels = self.loadModels("resources/", "block")
        self.entityModels = self.loadModels("resources/", "entity")

    @staticmethod
    def loadModels(path, modeltype):
        models = {}
        defaultmodel = None
        counter = -1
        for dict in yaml.load_all(open(path+modeltype+"models.yml", 'r')):
            
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
                model.set("texture", pygame.image.load("{}/images/{}/{}.png".format(path, modeltype, dict["type"])))
            except:
                model.set("texture", pygame.image.load("{}/images/{}/{}.png".format(path, modeltype, "default")))

        print "Loaded {} {} models".format(counter, modeltype)
        return models
