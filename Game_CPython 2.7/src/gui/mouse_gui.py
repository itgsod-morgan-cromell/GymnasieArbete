import pygame
from src.gui.gui import Gui
from src.gui.textrect import render_textrect
import copy


class MouseGui(Gui):
    def __init__(self, world):
        self.world = world
        self.data = None
        image = pygame.Surface((200, 100), pygame.SRCALPHA, 32)
        #image.convert_alpha()
        self.options = {}
        self.show_window = False
        Gui.__init__(self, 'character', (0, 0), image, True)

    def update_data(self, data):
        if self.data != data:
            self.active = True
            self.show_window = False
            #self.image.convert_alpha()
        self.data = data
        self.options = {}
        self.image = pygame.Surface((200, 100), pygame.SRCALPHA, 32)
        if hasattr(data, 'options'):
            i = 0
            for option, action in data.options.items():
                string = "{0}: {1}".format(option, action)
                rect = pygame.Rect((0, 15 * i), (len(string) * 7, 15))
                i += 1
                self.options[option] = action
                self.image.blit(render_textrect(string, 15, rect, (128, 128, 128), (0, 0, 0)), (rect.x, rect.y))

    def update(self, world, events):
        self.world = world
        if not self.active:
            self.show_window = False
            return
        self.x = pygame.mouse.get_pos()[0]
        self.y = pygame.mouse.get_pos()[1] - self.image.get_bounding_rect().h
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:  # Left click.
                    if self.show_window:
                        if 'LMouse' in self.options:
                            if hasattr(self.data, self.options['LMouse']):
                                getattr(self.data, self.options['LMouse'])(self.world)
                    self.show_window = not self.show_window
                elif pygame.mouse.get_pressed()[2]:  # Right click.
                    if self.show_window:
                        if 'RMouse' in self.options:
                            if hasattr(self.data, self.options['RMouse']):
                                getattr(self.data, self.options['RMouse'])(self.world)

    def draw(self, screen):
        if not self.active:
            return
        if self.show_window:
            screen.blit(self.image, (self.x, self.y))
