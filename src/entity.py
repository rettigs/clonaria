class Entity(object):

#    name # String; The name of this entity (e.g. "xXsupan00b69Xx", but usually null)
#    entityModel # EntityModel; The model of this entity (stores stateless data)
#    world # World; The world the entity is in
#    location # Vector; The entity's location in the world (in block coordinates)
#    againstBlockUp # boolean; Whether the entity is against a block above it
#    againstBlockDown # boolean; Whether the entity is against a block below it
#    againstBlockLeft # boolean; Whether the entity is against a block left of it
#    againstBlockRight # boolean; Whether the entity is against a block right of it
#    velocity # Vector; The entity's velocity, in blocks per tick
#    target # Entity; The entity's target the entity will attempt to move toward it
#    gravity # double; The entity's downward acceleration due to "gravity", in blocks/tick^2
#    airResistance # double; The entity's horizontal damping multiplier due to "air resistance", in dampAmount/tick
#    jumpAccel # double; The entity's upward acceleration when jumping in blocks/tick^2
#    horAccel # double; The entity's horizontal acceleration in blocks/tick^2
#    maxJumps # int; How many times the entity is allowed to jump (usually 1)
#    curJumps # int; How many times the entity has jumped.  Resets upon contact with ground
#    maxHealth # int; How much health the entity can have
#    curHealth # int; How much health the entity currently has
#    defense # int; How much defense the entity has
#    light # int; How bright this entity is
#    inventory # Map<String, Item>; Holds the inventory of the entity mostly used for players and to hold mob drops
#    holding # String; The key to the inventory item the entity is currently holding

    def __init__(self, entityModel, world, location):
        self.entityModel = entityModel
        self.world = world
        self.location = self.x, self.y = location
