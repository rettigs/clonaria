from __future__ import division

class Const(object):
    '''Game constants'''

    GAME_NAME = "Clonaria"
    RESOURCE_PATH = "../resources"
    TICKS_PER_SECOND = TPS = 60
    TIME_STEP = 1 / TPS
    VEL_ITERS = 6 # Box2D stuff
    POS_ITERS = 2 # Box2D stuff
    PIXELS_PER_BLOCK = PPB = 16
    BLOCK_SCALE = 2
    ZOOM = 1
    NUM_LAYERS = 5
    CHUNK_SIZE = 256
    ACCELERATION_GRAVITY = 4000 / TPS
    ACCELERATION_WALK = ACCELERATION_GRAVITY / 10
    ACCELERATION_JUMP = ACCELERATION_GRAVITY / 4
    ACCELERATION_JUMP_HOLD = ACCELERATION_JUMP * 0.04
    MAX_JUMP_TICKS = TPS / 4

    BLOCK_THRESHOLD = 1 / PPB / 4

    UP      = (0, 1)
    DOWN    = (0, -1)
    RIGHT   = (1, 0)
    LEFT    = (-1, 0)

    # World types
    WORLD_TYPES = ['NORMAL', 'FLAT', 'SINE']

    # Predefined colors for certain drawables
    COLORS = dict(
        DEBUG_CHUNK_BORDER=(0,255,0,255), # Green
        DEBUG_ENTITY_HITBOX=(255,0,0,255), # Red
        DEBUG_PHYSICS_BLOCK_HITBOX=(0,0,255,255), # Blue
        DEBUG_TARGET_BLOCK_HIGHLIGHT=(255,0,0,128), # Transparent red
        DEBUG_PHYSICS_BLOCK_HIGHLIGHT=(255,255,0,128) # Transparent yellow
    )
