


class Entity(object):
    def __init__(self, world, x, y):
        self.x = x
        self.y = y
        self.world = world

    def update(self):
        pass

    def render(self):
        pass