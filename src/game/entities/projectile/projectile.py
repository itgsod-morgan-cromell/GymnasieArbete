from src.game.entities.entity import Entity


class Projectile(Entity):
    def __init__(self, x, y, dir):
        self.xOrigin = x
        self.yOrigin = y
        self.angle = dir
        self.type = 'projectile'
        super(Projectile, self).__init__(x, y)

