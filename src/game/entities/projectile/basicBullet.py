import math
import game.game
import pygame
from src.game.entities.projectile.projectile import Projectile


class BasicBullet(Projectile):
    def __init__(self, x, y, dir):
        super(BasicBullet, self).__init__(x, y, dir)
        self.range = 200
        self.damage = 20
        speed = 10
        self.rateOfFire = 15
        self.nx = speed * math.cos(self.angle)
        self.ny = speed * math.sin(self.angle)
        self.sprite = pygame.image.load('../res/sprites/proj_test.png')
        rect = pygame.Rect(self.x, self.y, 10, 10)
        self.rect = rect.copy()
        self.time = 0

    def update(self):
        self.time += 1
        if self.time > self.range:
            if self in game.game.mapdata[game.game.world.name]:
                self.remove()
        self.rect.x = self.x
        self.rect.y = self.y

        self.move()

    def move(self):
        x = self.x + self.nx
        y = self.y + self.ny
        if not self.hasCollided(x, y):
            self.x += self.nx
            self.y += self.ny
        else:
            if self in game.game.mapdata[game.game.world.name]:
                self.remove()

    def hasCollided(self, xa, ya):

        projectileRect = pygame.Rect(self.rect.x, self.rect.y, self.rect.w, self.rect.h)
        if not game.game.world.mapRect.contains(projectileRect):
            return True
        if game.game.world.collide(projectileRect):
            return True

        object = game.game.world.collide_object(self, projectileRect)
        if object:
            if self.checkInteraction(object):
                return True
        return False

    def checkInteraction(self, object):
        if object.type == 'dummy':
            print "hit dummy"
            if object in game.game.mapdata[game.game.world.name]:
                object.remove()
            if self in game.game.mapdata[game.game.world.name]:
                self.remove()
            return True
        else:
            return False

    def render(self, screen):
        x = self.x - game.game.camera.x
        y = self.y - game.game.camera.y

        screen.blit(self.sprite, (x, y))
        if game.game.debug:
            screen.fill((255, 0, 0),
                        pygame.Rect(x, y, self.rect.w, self.rect.h))