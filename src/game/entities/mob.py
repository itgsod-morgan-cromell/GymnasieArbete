from .entity import Entity


class Mob(Entity):

    def __init__(self, world, type, x, y, speed, rect):
        super(Mob, self).__init__(world, x, y)
        self.type = type
        self.speed = speed
        self.numSteps = 0
        self.isMoving = False
        self.movingDir = {'UP': False, 'DOWN': True, 'LEFT': False, 'RIGHT': False}
        self.rect = rect.copy()

    def move(self, xa, ya):
        if xa != 0 and ya != 0:
            self.move(xa, 0)
            self.move(0, ya)
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

    def hasCollided(self, xa, ya):
        pass

