from __future__ import division

class Const(object):
    '''Game constants'''

    GAME_NAME = "Clonaria"
    RESOURCE_PATH = "../resources"
    TICKS_PER_SECOND = TPS = 60
    PIXELS_PER_BLOCK = PPB = 16
    BLOCK_SCALE = 2
    ZOOM = 1
    NUM_LAYERS = 5
    ACCELERATION_WALK = 0.25 / TPS
    ACCELERATION_GRAVITY = 60 / TPS
    ACCELERATION_JUMP = ACCELERATION_GRAVITY * 8
    ACCELERATION_JUMP_HOLD = ACCELERATION_JUMP * 0.04
    MAX_JUMP_TICKS = TPS / 4
