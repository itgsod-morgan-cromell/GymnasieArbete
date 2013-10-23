from .entity import Entity
import pygame
import math


'''
The mob class is a standard set of features that every character needs to function.
Here we handle stuff as the move function and things like that.
'''

class Mob(Entity):

    def __init__(self, type, x, y, speed, rect):
        super(Mob, self).__init__(x, y)
        self.type = type
        self.speed = speed
        self.numSteps = 0
        self.isMoving = False
        self.movingDir = {
            'UP': False, 'DOWN': True, 'LEFT': False, 'RIGHT': False,
            'UP_LEFT': False, 'UP_RIGHT': False, 'DOWN_LEFT': False, 'DOWN_RIGHT': False}
        self.rect = rect.copy()
        self.dirty = 0
        self.projectiles = []
        self.projectileAngles = {
            'UP': 270, 'DOWN': 90, 'LEFT': 180, 'RIGHT': 0,
            'UP_LEFT': 225, 'UP_RIGHT': 315, 'DOWN_LEFT': 135, 'DOWN_RIGHT': 45}


    def move(self, xa, ya):
        if xa != 0 and ya != 0:
            if ya < 0:
                if xa > 0:
                    self.movingDir['UP_RIGHT'] = True
                else:
                    self.movingDir['UP_LEFT'] = True
            else:
                if xa > 0:
                    self.movingDir['DOWN_RIGHT'] = True
                else:
                    self.movingDir['DOWN_LEFT'] = True

            if not self.hasCollided(xa, ya):
                self.x += (xa * self.speed) / math.sqrt(2)
                self.y += (ya * self.speed) / math.sqrt(2)
                self.dirty = 1

            self.numSteps -= 1
            return

        self.numSteps += 1
        if ya < 0:
            self.movingDir['UP'] = True
        if xa > 0:
            self.movingDir['RIGHT'] = True
        if ya > 0:
            self.movingDir['DOWN'] = True
        if xa < 0:
            self.movingDir['LEFT'] = True

        if not self.hasCollided(xa, ya):
            self.x += xa * self.speed
            self.y += ya * self.speed
            self.dirty = 1

    def hasCollided(self, xa, ya):
        pass

