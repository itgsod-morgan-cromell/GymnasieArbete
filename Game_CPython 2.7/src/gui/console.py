from src.gui.gui import Gui
import pygame
import sys
from StringIO import StringIO
from src.event_constants import *
from src.gui.textrect import render_textrect


class Text(object):
    def __init__(self, rect, data, color=(255, 255, 255)):
        self.data = data
        self.rect = rect
        if type(data) == str:
            self.image = render_textrect(data, 15, rect, color)


class Console(Gui):
    def __init__(self, world, world_screen):
        self.width = world_screen.get_width()
        self.height = 6 * 32
        Gui.__init__(self, 'console', (0, world_screen.get_height()), pygame.Surface((self.width, self.height)), True)
        self.log = []
        self.log_processed = None
        self.world = world
        pygame.event.post(pygame.event.Event(REGISTER_EVENT_HANDLER, event_register_dict(POST_TO_CONSOLE, self)))

    def update(self, world):
        self.world = world

    def handle_event(self, event):
        etype = event.type if event.type != pygame.USEREVENT else event.event_type
        if etype == POST_TO_CONSOLE:
            self.log.append(event.msg)
            if len(self.log) > 10:
                self.log = self.log[-10:]
            text = ""
            for i, line in enumerate(self.log):
                text += line + '\n'
            rect = pygame.Rect((5, 5), (self.width, self.height))
            self.log_processed = (Text(rect, text))

    def draw(self, screen):
        if self.log_processed:
            screen.blit(self.log_processed.image, (self.log_processed.rect.x + self.x, self.log_processed.rect.y + self.y))