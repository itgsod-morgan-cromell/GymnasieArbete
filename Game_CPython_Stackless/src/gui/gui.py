import pygame
from src.event_helper import *
from src.gui.textrect import render_textrect





class Gui(object):
    def __init__(self, type, pos, image, active):
        self.type = type
        self.x = pos[0]
        self.y = pos[1]
        self.image = image
        self.rect = pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())
        self.active = active

    def activate(self):
        self.active = not self.active

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))