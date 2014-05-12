from src.gui.gui import Gui
import pygame

from src.event_helper import *
from src.gui.textrect import render_textrect
from src.options import *


class Text(object):
    def __init__(self, rect, data, color):
        self.data = data
        self.rect = rect
        if type(data) == str:
            self.image = render_textrect(data, 15, rect, color)


class Console(Gui):
    def __init__(self):
        self.width = WIDTH - MENU_WIDTH
        self.height = CONSOLE_HEIGHT
        Gui.__init__(self, 'console', (0, HEIGHT - CONSOLE_HEIGHT), pygame.Surface((self.width, self.height)), True)
        self.log = []
        self.log_processed = []
        register_handler([POST_TO_CONSOLE, CLEAR_CONSOLE], self.handle_event)


    def handle_event(self, event):
        etype = event.type if event.type != pygame.USEREVENT else event.event_type
        if etype == POST_TO_CONSOLE:
            rect = pygame.Rect((5, 5), (self.width, 15))
            color = event.color if hasattr(event, 'color') else (255, 255, 255)
            self.log_processed.append(Text(rect, event.msg, color))
            if len(self.log_processed) > 7:
                self.log_processed = self.log_processed[-7:]
        elif etype == CLEAR_CONSOLE:
            self.log_processed = []

    def draw(self, screen):
        for y, msg in enumerate(self.log_processed):
            screen.blit(msg.image, (msg.rect.x + self.x, msg.rect.y + self.y + y * msg.rect.h))