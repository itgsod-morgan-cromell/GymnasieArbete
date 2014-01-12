
class Entity(object):
    def __init__(self, name, pos, world, type=None):
        self.name = name
        self.type = type
        self.x = pos[0]
        self.y = pos[1]
        self.world = world