import pygame


class Gui(object):
    def __init__(self, type, pos, image, active):
        self.type = type
        self.x = pos[0]
        self.y = pos[1]
        self.image = image
        self.active = active

    def activate(self):
        self.active = not self.active

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))