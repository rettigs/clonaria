import pyglet
from const import Const
from polygon import Polygon

class Model(object):

    def __init__(self, properties):
        self.properties = properties

        #Eval the hitbox string to a list of (x, y) coordinate tuples, then convert to a Polygon
        if 'hitbox' in self.properties:
            self.set('hitbox', Polygon(eval(self.get('hitbox'))))

        # Load the texture
        try:
            self.set('texture', pyglet.image.load("{}/images/{}/{}.png".format(Const.RESOURCE_PATH, self.get('modeltype'), self.get('type'))))
        except:
            self.set('texture', pyglet.image.load("{}/images/{}/{}.png".format(Const.RESOURCE_PATH, self.get('modeltype'), 'default')))

    def get(self, prop):
        if prop in self.properties:
            return self.properties[prop]
        elif 'defaultmodel' in self.properties:
            return self.get('defaultmodel').get(prop)
        else:
            return None

    def set(self, prop, value):
        self.properties[prop] = value
