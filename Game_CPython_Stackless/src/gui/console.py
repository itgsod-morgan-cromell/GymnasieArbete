from src.gui.gui import Gui
import pygame

from src.event_helper import *
from src.gui.textrect import render_textrect
from src.options import *
from random import randint


class Text(object):
    def __init__(self, rect, data, color):
        self.data = data
        if type(data) == str:
            self.image = CONSOLE_FONT.render(data, 1, color)
        self.rect = rect
        self.rect.w = self.image.get_width()
        self.rect.h = CONSOLE_FONT.get_linesize()


class Console(Gui):
    def __init__(self):
        self.width = WIDTH - MENU_WIDTH
        self.height = CONSOLE_HEIGHT
        self.max_messages = int(CONSOLE_HEIGHT/CONSOLE_FONT_SIZE) - 3
        Gui.__init__(self, 'console', (0, HEIGHT - CONSOLE_HEIGHT), pygame.Surface((self.width, self.height)), True)
        self.log = []
        self.log_processed = []
        self.fill_message = None
        register_handler([POST_TO_CONSOLE, CLEAR_CONSOLE, FILL_CONSOLE, CLEAR_FILL_CONSOLE], self.handle_event)


    def handle_event(self, event):
        etype = get_event_type(event)
        if etype == POST_TO_CONSOLE:
            if hasattr(event, 'color'):
                color = event.color
            else:
                color = (255, 255, 255)
            self.log_processed.insert(0, self.create_text(event.msg, color))
        elif etype == CLEAR_CONSOLE:
            self.log_processed = []

        elif etype == FILL_CONSOLE:
            self.fill_message = Text(self.rect, event.msg, (255, 255, 255))
        elif etype == CLEAR_FILL_CONSOLE:
            self.fill_message = None

    def create_text(self, msg, color):
        if type(msg) == list:
            for i, m in enumerate(msg):
                if type(m) == tuple:
                    color = m[1]
                    m = m[0]

                msg_width = (len(m) * CONSOLE_FONT_SIZE * 0.6)
                print msg_width
                last_msg_width = 0
                for i2 in range(0, len(msg)):
                    if i2 < i:
                        last_msg_width += msg[i2].rect.w
                rect = pygame.Rect((last_msg_width, 5), (msg_width, 20))
                msg[i] = Text(rect, m, color)
            return msg
        else:
            msg_width = (len(msg) * CONSOLE_FONT_SIZE)
            rect = pygame.Rect((5, 5), (msg_width, 20))
            text = Text(rect, msg, color)
            return text



    def draw(self, screen):
        if self.fill_message:
            screen.blit(self.fill_message.image, (self.x, self.y))
            return
        for y, msg in enumerate(self.log_processed):
            if y > self.max_messages - 1:
                return
            if type(msg) == list:
                for m in msg:
                    screen.blit(m.image, (m.rect.x + self.x, m.rect.y + self.y + y * m.rect.h))
            else:
                screen.blit(msg.image, (msg.rect.x + self.x, msg.rect.y + self.y + y * msg.rect.h))