#!/usr/bin/env python

from __future__ import division
import getopt
import sys
import time

import pyglet
from pyglet.window import key, mouse
from Box2D import *

from const import *
from entity import *
from model import *
from player import *
from util import *
from world import *

if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], "dh", ["help", "worldtype=", "seed="])
    except getopt.GetoptError as err:
        print str(err)
        sys.exit(2)

    worldOpts = {}

    for o, a in opts:
        if o == "-d":
            State().debug += 1
        elif o == "-h" or o == "--help":
            Util.showHelp()
            exit()
        elif o == "--worldtype":
            worldOpts['worldType'] = a
        elif o == "--seed":
            worldOpts['seed'] = a

    State().window = window = pyglet.window.Window(caption=Const.GAME_NAME, resizable=True)

    State().blockModels = Util.loadModels('block')
    State().entityModels = Util.loadModels('entity')

    State().space = b2World(gravity=(0.0, -Const.ACCELERATION_GRAVITY), doSleep=True)

    State().world = world = World("world1", Const.WORLD_WIDTH, Const.WORLD_HEIGHT, **worldOpts)
    State().world.generate()

    State().player = player = Player(State().entityModels['player'], world, (world.width/2, world.height/2+10))

    keys = key.KeyStateHandler()
    window.push_handlers(keys)

    # Implement mouse state like the keyboard has because pyglet lacks one
    buttons = []
    State().mouseLoc = 0, 0

    # Set window background color
    pyglet.gl.glClearColor(0, 40, 200, 0)

    # Enable transparency
    glEnable(GL_BLEND)

    batch = State().batch

    if State().debug >= 1:
        debugStats = [  '"FPS: {}".format(pyglet.clock.get_fps())',
                        '"player.body.position.x: {}".format(State().player.body.position.x)',
                        '"player.body.position.y: {}".format(State().player.body.position.y)',
                        '"player.body.linearVelocity.x: {}".format(State().player.body.linearVelocity.x)',
                        '"player.body.linearVelocity.y: {}".format(State().player.body.linearVelocity.y)',
                        '"player.stillJumping: {}".format(State().player.stillJumping)',
                        '"player.againstBlockDown: {}".format(State().player.againstBlockDown)',
                        '"player.againstBlockLeft: {}".format(State().player.againstBlockLeft)',
                        '"targetBlock: {}".format(Util.pixelsToBlocks(State().mouseLoc))']
        Util.addDebugStats(debugStats)

    @window.event
    def on_mouse_press(x, y, button, modifiers):
        buttons.append(button)

    @window.event
    def on_mouse_release(x, y, button, modifiers):
        buttons.remove(button)

    @window.event
    def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
        State().mouseLoc = x, y

    @window.event
    def on_mouse_motion(x, y, dx, dy):
        State().mouseLoc = x, y

    @window.event
    def on_draw():
        window.clear()
        State().cameraPos = tuple(State().player.body.position)
        world.prepareDraw()
        player.prepareDraw()
        if State().debug >= 1:
            Util.prepareDrawDebugStats()

        batch.draw()

        if State().debug >= 2:
            Util.drawDebugPhysicsBlocks()
            Util.drawDebugPhysicsBlockHitboxes()
            Util.drawDebugTargetBlock()
            Util.drawDebugChunkBorders()
            Util.drawDebugPhysicsEntityHitboxes()

    def update(self):
        State().physics_blockCoords = Util.physics_getBlockCoords([player])
        State().physics_edgeCoords = Util.physics_getEdgeCoords([player])
        Util.physics_updateEdgePhysics(State().physics_edgeCoords)

        playerJumping = False

        # Handle keyboard input
        if keys[key.LEFT] or keys[key.A]:
            player.walkLeft()
        if keys[key.RIGHT] or keys[key.D]:
            player.walkRight()
        if keys[key.SPACE]:
            playerJumping = True
            player.jump()
        if keys[key.PLUS] or keys[key.NUM_ADD]:
            Const.ZOOM += 1 / Const.PPB
        if keys[key.MINUS] or keys[key.NUM_SUBTRACT]:
            Const.ZOOM -= 1 / Const.PPB
        if keys[key.EQUAL]:
            Const.ZOOM = 1
        
        # Handle mouse input
        if mouse.LEFT in buttons:
            loc = Util.pixelsToBlocks(State().mouseLoc)
            world.setBlockAt(State().blockModels['air'], loc)
        if mouse.MIDDLE in buttons:
            loc = Util.pixelsToBlocks(State().mouseLoc)
            world.setBlockAt(State().blockModels['platform'], loc)
        if mouse.RIGHT in buttons:
            loc = Util.pixelsToBlocks(State().mouseLoc)
            world.setBlockAt(State().blockModels['cone'], loc)

        if not playerJumping or player.curJumpTicks < 1:
            player.stillJumping = False
        
        # Instruct the world to perform a single step of simulation. It is
        # generally best to keep the time step and iterations fixed.
        State().space.Step(Const.TIME_STEP, Const.VEL_ITERS, Const.POS_ITERS)

        # Clear applied body forces. We didn't apply any forces, but you
        # should know about this function.
        State().space.ClearForces() #TODO: Figure out if this line is useful or necessary.

    pyglet.clock.schedule_interval(update, Const.TIME_STEP)
    pyglet.app.run()
