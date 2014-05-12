import pygame


class Slot(object):
    def __init__(self, x, y, contains=None):
        self.x = x
        self.y = y
        self.rect = pygame.Rect((self.x, self.y), (32, 32))
        self.containts = contains