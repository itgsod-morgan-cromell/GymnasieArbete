import pygame
import os
import random


class Entity(object):
    def __init__(self, name, pos, world, type=None):
        self.name = name
        self.type = type
        self.x = pos[0]
        self.y = pos[1]
        self.world = world

    def get_random_image(self, folder):
        image = pygame.image.load(folder + '/' + random.choice(os.listdir(folder)))
        return image