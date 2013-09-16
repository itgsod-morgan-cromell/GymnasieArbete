from entity import Entity


class Mob(Entity):

    def __init__(self, world, name, x, y, speed, rect):
        super(Mob, self).__init__(world, x, y)
        self.name = name
        self.speed = speed
        self.numSteps = 0
        self.isMoving = False
        self.movingDir = 1
        self.rect = rect.copy()

    def move(self, xa, ya):
        if xa != 0 and ya != 0:
            self.move(xa, 0)
            self.move(0, ya)
            self.numSteps -= 1
            return

        self.numSteps += 1
        if ya < 0:
            self.movingDir = 0 #UP
        if ya > 0:
            self.movingDir = 1 #DOWN
        if xa < 0:
            self.movingDir = 2 #LEFT
        if xa > 0:
            self.movingDir = 3 #RIGHT

        if not self.hasCollided(xa, ya):
            self.x += xa * self.speed
            self.y += ya * self.speed

    def hasCollided(self, xa, ya):
        pass

