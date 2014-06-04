#!/usr/bin/env python

import getopt, pyglet, sys, time
from pyglet.window import key

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

    fps_display = pyglet.clock.ClockDisplay()

    batch = Util.get().batch

    if Util.get().debug:
        debugStats = [  '"player.x: {}".format(self.player.x)',
                        '"player.y: {}".format(self.player.y)',
                        '"player.vx: {}".format(self.player.vx)',
                        '"player.vy: {}".format(self.player.vy)']
        Util.get().addDebugStats(debugStats)

    @window.event
    def on_draw():
        window.clear()
        world.draw()

        if Util.get().debug:
            batch.draw()
            fps_display.draw()
            Util.get().updateDebugStats()

        player.draw()

    def update(self):
        if keys[key.LEFT] or keys[key.A]:
            player.left()
        if keys[key.RIGHT] or keys[key.D]:
            player.right()

        player.move()

    pyglet.clock.schedule_interval(update, 1/60.)
    pyglet.app.run()
