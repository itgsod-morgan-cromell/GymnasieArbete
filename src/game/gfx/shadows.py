import pygame

from .PAdLib import occluder
from .PAdLib import shadow
import game.game
from random import randint
from game.profilehooks import profile


surf_lighting = None


class Lighting(object):
    def __init__(self):
        global surf_lighting
        surf_lighting = pygame.Surface((game.game.camera.w, game.game.camera.h))
        self.lights = []


    def update(self):
        global surf_lighting
        surf_lighting.fill((25,25,25))
        for light in self.lights:
            if game.game.camera.inflate(100, 100).contains(light.rect):
                light.update()


    def addLight(self, radius, x, y):
        light = Light(radius, x, y)
        self.lights.append(light)
        return light

    def render(self):
        game.game.screen.blit(surf_lighting, (0, 0), special_flags=pygame.BLEND_MULT)


class Light(object):
    def __init__(self, radius, x, y):
        self.x = x
        self.y = y
        self.radius = radius
        self.rect = pygame.Rect(x, y, 30, 30)
        self.surf_falloff = pygame.image.load("../res/light_falloff100.png").convert()

    def update(self):
        global surf_lighting
        randsize = randint(0, 2)
        surf_falloff = pygame.transform.scale(self.surf_falloff, (self.radius * 2 + 10 + randsize, self.radius * 2 + 10 + randsize))
        surf_lighting.blit(surf_falloff, (self.x - game.game.camera.x - self.radius,self.y - game.game.camera.y - self.radius), special_flags=pygame.BLEND_MAX)

    def move(self, x, y):
        self.x, self.y = x, y
        self.rect.x = self.x
        self.rect.y = self.y