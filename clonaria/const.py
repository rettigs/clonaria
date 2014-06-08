class Const(object):
    RESOURCE_PATH = "../resources"
    TICKS_PER_SECOND = TPS = 60
    PIXELS_PER_BLOCK = PPB = 16
    ZOOM = 1
    NUM_LAYERS = 5
    ACCELERATION_WALK = 0.3 / TPS
    ACCELERATION_GRAVITY = 1.0 / TPS
    ACCELERATION_JUMP = ACCELERATION_GRAVITY * 16
    ACCELERATION_JUMP_HOLD = ACCELERATION_JUMP * 0.04
    MAX_JUMP_TICKS = TPS / 2
