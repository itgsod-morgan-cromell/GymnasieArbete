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
        Gui.__init__(self, 'character', (0, 0), image, True)

    def update_data(self, data):
        self.options = {}
        self.data = data
        self.image = pygame.Surface((200, 100), pygame.SRCALPHA, 32)
        #self.image.convert_alpha()
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
            return
        self.x = pygame.mouse.get_pos()[0]
        self.y = pygame.mouse.get_pos()[1] - self.image.get_bounding_rect().h
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:  # Left click.
                    if 'LMouse' in self.options:
                        if hasattr(self.data, self.options['LMouse']):
                            getattr(self.data, self.options['LMouse'])(self.world)

    def draw(self, screen):
        if not self.active:
            return
        screen.blit(self.image, (self.x, self.y))