#!/usr/bin/env python

import getopt, pyglet, sys, time
from pyglet.window import key

from const import Const
from entity import Entity
from model import Model
from util import Util
from world import World

if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], "d")
    except getopt.GetoptError as err:
        print str(err)
        sys.exit(2)

    for o, a in opts:
        if o == "-d":
            Util.get().debug += 1

    Util.get().window = window = pyglet.window.Window(resizable=True)

    Util.get().world = world = World("world1", (400, 400))
    world.generate()

    Util.get().player = player = Entity(Util.get().entityModels['player'], world.name, (world.width / 2, world.height / 2 + 1))

    keys = key.KeyStateHandler()
    window.push_handlers(keys)

    pyglet.gl.glClearColor(0, 40, 200, 0)

    batch = Util.get().batch

    if Util.get().debug:
        debugStats = [  '"FPS: {}".format(pyglet.clock.get_fps())',
                        '"player.x: {}".format(self.player.x)',
                        '"player.y: {}".format(self.player.y)',
                        '"player.vx: {}".format(self.player.vx)',
                        '"player.vy: {}".format(self.player.vy)']
        Util.get().addDebugStats(debugStats)

    @window.event
    def on_draw():
        window.clear()
        world.prepareDraw()
        if Util.get().debug:
            Util.get().updateDebugStats()
        player.prepareDraw()
        batch.draw()

    def update(self):
        if keys[key.LEFT] or keys[key.A]:
            player.left()
        if keys[key.RIGHT] or keys[key.D]:
            player.right()
        if keys[key.SPACE]:
            player.jump()
        if keys[key.PLUS] or keys[key.NUM_ADD]:
            Const.ZOOM += 1. / Const.PPB
        if keys[key.MINUS] or keys[key.NUM_SUBTRACT]:
            Const.ZOOM -= 1. / Const.PPB
        if keys[key.EQUAL]:
            Const.ZOOM = 1

        #player.applyGravity()
        #player.applyFriction()
        player.move()

    pyglet.clock.schedule_interval(update, 1/60.)
    pyglet.app.run()
