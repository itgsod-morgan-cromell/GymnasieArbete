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
            self.image = render_textrect(data, CONSOLE_FONT_SIZE, rect, color)


class Console(Gui):
    def __init__(self):
        self.width = WIDTH - MENU_WIDTH
        self.height = CONSOLE_HEIGHT
        self.max_messages = int(CONSOLE_HEIGHT/CONSOLE_FONT_SIZE) - 3
        Gui.__init__(self, 'console', (0, HEIGHT - CONSOLE_HEIGHT), pygame.Surface((self.width, self.height)), True)
        self.log = []
        self.log_processed = []
        register_handler([POST_TO_CONSOLE, CLEAR_CONSOLE], self.handle_event)


    def handle_event(self, event):
        etype = event.type if event.type != pygame.USEREVENT else event.event_type
        if etype == POST_TO_CONSOLE:
            if hasattr(event, 'color'):
                color = event.color
            else:
                color = (255, 255, 255)
            self.log_processed.insert(0, self.create_text(event.msg, color))
        elif etype == CLEAR_CONSOLE:
            self.log_processed = []

    def create_text(self, msg, color):
        t = int(200 * (CONSOLE_FONT_SIZE/10))
        if type(msg) == list:
            for i, m in enumerate(msg):
                msg_width = (len(m) * t)
                last_msg_width = 0
                for i2 in range(0, len(msg)):
                    if i2 < i:
                        last_msg_width += (len(msg[i2].data) * CONSOLE_FONT_SIZE * 0.6 + 8)
                rect = pygame.Rect((5 + last_msg_width, 5), (msg_width, 20))
                if type(m) == tuple:
                    msg[i] = Text(rect, m[0], m[1])
                else:
                    msg[i] = Text(rect, m, color)
            return msg
        else:
            msg_width = (len(msg) * t)
            rect = pygame.Rect((5, 5), (msg_width, 20))
            text = Text(rect, msg, color)
            return text



    def draw(self, screen):
        for y, msg in enumerate(self.log_processed):
            if y > self.max_messages - 1:
                return
            if type(msg) == list:
                for m in msg:
                    screen.blit(m.image, (m.rect.x + self.x, m.rect.y + self.y + y * m.rect.h))
            else:
                screen.blit(msg.image, (msg.rect.x + self.x, msg.rect.y + self.y + y * msg.rect.h))