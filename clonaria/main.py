#!/usr/bin/env python

import pyglet, sys, time

from entity import Entity
from model import Model
from util import Util
from world import World

if __name__ == '__main__':
    Util.get().window = window = pyglet.window.Window()
#    label = pyglet.text.Label('Hello, world',
#                              font_name='Times New Roman',
#                              font_size=36,
#                              x=window.width//2, y=window.height//2,
#                              anchor_x='center', anchor_y='center')

    Util.get().world = world = World("world1", (1000, 1000))
    world.generate()

    Util.get().player = player = Entity("player", world.name, (world.width / 2, world.height / 2 + 1))

    @window.event
    def on_draw():
        window.clear()
        world.draw()

    pyglet.app.run()
