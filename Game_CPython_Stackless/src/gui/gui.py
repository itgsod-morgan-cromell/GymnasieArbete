import pygame
from src.event_helper import *
from src.gui.textrect import render_textrect


class Button(object):
    def __init__(self, data, event_type, rect):
        self.data = data
        self.rect = rect
        self.event_type = event_type
        if type(self.data) == str:
            self.image = render_textrect(self.data, self.rect.w, self.rect, (255, 255, 255), None, 1)
        else:
            self.image = self.data

    def onclick(self):
        post_event(self.event_type)

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))


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