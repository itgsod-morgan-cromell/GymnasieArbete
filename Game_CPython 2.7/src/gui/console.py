from src.gui.gui import Gui
import pygame
import sys
from StringIO import StringIO
from src.constants import *
from src.gui.textrect import render_textrect


class Text(object):
    def __init__(self, rect, data, color=(255, 255, 255)):
        self.data = data
        self.rect = rect
        if type(data) == str:
            self.image = render_textrect(data, 50, rect, color)


class Console(Gui):
    def __init__(self, world, world_screen):
        self.width = world_screen.get_width()
        self.height = 100
        Gui.__init__(self, 'console', (0, world_screen.get_height()), pygame.Surface((self.width, self.height)), True)
        self.log = []
        self.log_processed = [None] * 5
        self.world = world
        pygame.event.post(pygame.event.Event(pygame.USEREVENT+1, event_register_dict(POST_TO_CONSOLE, self)))

    def update(self, world):
        self.world = world

    def process_event(self, event):
        self.log.append(event.msg)
        if len(self.log) > 5:
            self.log = self.log[-5:]
        for i, line in enumerate(self.log):
            rect = pygame.Rect((5, i*16), (self.width, 15))
            self.log_processed[i] = (Text(rect, line))

    def draw(self, screen):
        for line in self.log_processed:
            if line:
                screen.blit(line.image, (line.rect.x + self.x, line.rect.y + self.y))