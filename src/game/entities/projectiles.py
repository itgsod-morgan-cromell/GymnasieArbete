from .entity import Entity
import game.gfx.animate
import game.game
import pygame


class Projectile(Entity):
    type = {}
    type['Fireball'] = {'damage': 2, 'travel time': 2, 'speed': 5, 'image': pygame.image.Load('')}

    def __init__(self, x, y, dir, projectileType, modifier = None):
        Entity.__init__(self, x, y)
        self.projectileData = Projectile.type[projectileType]
        self.image = self.projectileData['image']
        self.rect = pygame.Rect(x, y, self.image.getWidth(), self.image.getHeight())

