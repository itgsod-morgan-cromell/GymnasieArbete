import game.game
'''
Simple base class that every entity in the world needs. Very simple things such as position and time created.
'''

class Entity(object):
    def __init__(self, world, x, y):
        self.x = x
        self.y = y
        self.world = world
        self.timeCreated = game.game.clock.time

    def update(self):
        pass

    def render(self):
        pass