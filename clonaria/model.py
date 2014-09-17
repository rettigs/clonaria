from __future__ import division
import os

import pyglet
from pyglet.gl import *

from const import *

class Model(object):
    '''Container for stateless, generic data that is not specific to a particular object, such as a block or entity.'''

    def __init__(self, properties):
        self.properties = properties

        # Eval the hitbox string to a list of (x, y) coordinate tuples.
        if 'hitbox' in self.properties:
            hitbox = eval(self.get('hitbox'))
            hitbox = [(x/Const.PPB, y/Const.PPB) for x, y in hitbox] # Scale the hitbox to the current block proportions.
            self.set('hitbox', hitbox)

        # Prepare to load the textures.
        texDir = "{}/images/{}".format(Const.RESOURCE_PATH, self.get('modeltype'))
        typeTexDir = os.path.join(texDir, self.get('type'))
        textures = {}

        # Load the main texture file.
        try:
            texture = self.__noAA(pyglet.image.load(typeTexDir+'.png'))
        except: # Load the default texture if it fails.
            texture = self.__noAA(pyglet.image.load(os.path.join(texDir, 'default.png')))
        self.set('texture', texture)
        textures['base'] = texture

        # Load any additional textures
        if os.path.isdir(typeTexDir): # If we have a texture folder, load each texture inside it.
            for filename in os.listdir(typeTexDir):
                if filename.endswith('.png'):
                    try:
                        textures[filename[:-4]] = self.__noAA(pyglet.image.load(os.path.join(typeTexDir, filename)))
                    except: # Load the default texture if it fails.
                        print "Could not load texture {}".format(os.path.join(typeTexDir, filename))
                        textures[filename[:-4]] = self.__noAA(pyglet.image.load(os.path.join(texDir, 'default.png')))

        # Make horizontally-flipped versions of every entity texture.
        if self.get('modeltype') is 'entity':
            for name, texture in textures.items():
                textures[name+'_r'] = texture # Textures start out facing right.
                textures[name+'_l'] = texture.get_texture().get_transform(flip_x=True)
                del textures[name]

        self.set('textures', textures)

    def get(self, prop):
        if prop in self.properties:
            return self.properties[prop]
        elif 'defaultmodel' in self.properties:
            return self.get('defaultmodel').get(prop)
        else:
            return None

    def set(self, prop, value):
        self.properties[prop] = value

    @staticmethod
    def __noAA(image):
        '''Disables image antialiasing for the given image.'''
        texture = image.get_texture()
        glBindTexture(texture.target, texture.id)
        glTexParameteri(texture.target, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glBindTexture(texture.target, 0)
        return image
