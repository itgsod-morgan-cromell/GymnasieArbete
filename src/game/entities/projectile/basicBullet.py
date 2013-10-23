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
        rect = pygame.Rect(self.x, self.y, 32, 32)
        self.rect = rect.copy()

    def update(self):
        self.move()
        self.rect.x = self.x
        self.rect.y = self.y

    def move(self):
        self.x += self.nx
        self.y += self.ny


    def render(self, screen):
        x = self.x - game.game.camera.x
        y = self.y - game.game.camera.y
        screen.blit(self.sprite, (x, y))