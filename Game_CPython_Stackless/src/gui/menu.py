import sys
from src.gui.gui import *
import pygame
from src.gui.textrect import render_textrect
from src.event_helper import *
from src.options import *
import copy


class Menu(Gui):
    def __init__(self):
        self.width = WIDTH
        self.height = HEIGHT
        #self.logo = render_textrect('Dungeon of Doom (Alpha)', 30, self.logo_rect, (255, 255, 0), None, 1)
        self.main_bg = pygame.image.load('../res/gui/main_menu_bg.png')
        self.main_bg = pygame.transform.scale(self.main_bg, (self.width, self.height))
        Gui.__init__(self, 'menu', (0, 0), pygame.Surface((self.width, self.height)), True)
        self.main = True
        register_handler([MENU_NEW_GAME, MENU_CLASS_SELECT, MENU_ENTER_NAME, MENU_QUIT_GAME, pygame.MOUSEBUTTONDOWN],
                         self.handle_event)

        self.buttons = [
            Button('New game', MENU_NEW_GAME, pygame.Rect((self.width / 2 - 100, self.height / 2 - 40), (200, 50))),
            Button('Load game', MENU_NEW_GAME, pygame.Rect((self.width / 2 - 100, self.height / 2), (200, 50))),
            Button('Quit', MENU_QUIT_GAME, pygame.Rect((self.width / 2 - 100, self.height / 2 + 40), (200, 50)))
        ]

    def handle_event(self, event):
        etype = get_event_type(event)
        if self.active:
            if etype == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_rect = pygame.Rect(event.pos, (2, 2))
                button = mouse_rect.collidelist(self.buttons)
                if button != -1:
                    self.buttons[button].onclick()

            elif etype == MENU_NEW_GAME:
                self.main = False
                self.active = False
            elif etype == MENU_QUIT_GAME:
                pygame.event.post(pygame.event.Event(pygame.QUIT))

    def draw(self, screen):
        self.image.fill((0, 0, 0))
        if self.main:
            self.image.blit(self.main_bg, (0, 0))

        for button in self.buttons:
            button.draw(self.image)

        screen.blit(self.image, (self.x, self.y))