import pygame
from src.gui.gui import Gui
from src.gui.textrect import render_textrect
from src.constants import *


class Mouse_select(object):
    def __init__(self, world):
        self.world = world
        self.rect = pygame.Rect((0, 0), (2, 2)).copy()
        self.color = (255, 0, 0)
        self.in_map = True
        self.image = pygame.Surface((32, 32), pygame.SRCALPHA, 32)
        self.image.convert_alpha()
        self.offset = pygame.Rect(0, 0, 0, 0)
        pygame.event.post(pygame.event.Event(REGISTER_EVENT_HANDLER, event_register_dict([pygame.MOUSEMOTION,
                                                                                          TIME_PASSED], self)))

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION or event.type == TIME_PASSED:
            self.rect.x = event.pos[0]
            self.rect.y = event.pos[1]
            if 0 < self.rect.x > self.offset.w or 0 < self.rect.y > self.offset.h:
                self.in_map = False
            else:
                self.in_map = True
                mouse_grid_x = int(self.rect.x/32) + int(self.offset.x/32)
                mouse_grid_y = int(self.rect.y/32) + int(self.offset.y/32)
                item = self.world.map.get_item(mouse_grid_x, mouse_grid_y)
                if item:
                    self.color = (0, 0, 255)
                    item.interact()
                elif self.world.map.dungeon.grid[mouse_grid_y][mouse_grid_x] in [1, 11]:
                    pygame.event.post(pygame.event.Event(PLAYER_FIND_PATH))


    def update(self, offset, world):
        self.offset = offset
        self.world = world



    def draw(self, screen):
        if self.in_map:
            pygame.draw.lines(self.image, self.color, False, [(8, 0), (0, 0), (0, 8)], 2) #top left
            pygame.draw.lines(self.image, self.color, False, [(24, 0), (30, 0), (30, 8)], 2) #top right
            pygame.draw.lines(self.image, self.color, False, [(24, 30), (30, 30), (30, 24)], 2) #bottom right
            pygame.draw.lines(self.image, self.color, False, [(0, 24), (0, 30), (8, 30)], 2) #bottom left
            x = int(self.rect.x/32)*32
            y = int(self.rect.y/32)*32
            screen.blit(self.image, (x, y))


class MouseGui(Gui):
    def __init__(self, world):
        self.world = world
        self.data = None
        image = pygame.Surface((200, 100), pygame.SRCALPHA, 32)
        #image.convert_alpha()
        self.options = {}
        self.target = None
        self.show_window = False
        self.mouse = Mouse_select(world)
        Gui.__init__(self, 'character', (0, 0), image, True)
        pygame.event.post(pygame.event.Event(REGISTER_EVENT_HANDLER, event_register_dict([GUI_TOOLTIP_OPTIONS, pygame.MOUSEBUTTONDOWN], self)))

    def update_data(self):
        self.show_window = False
        self.image = pygame.Surface((200, 100), pygame.SRCALPHA, 32)
        i = 0
        for option, action in self.options:
            string = "{0}: {1}".format(option, action)
            rect = pygame.Rect((0, 15 * i), (len(string) * 7, 15))
            i += 1
            self.image.blit(render_textrect(string, 15, rect, (128, 128, 128), (0, 0, 0)), (rect.x, rect.y))

    def update(self, world, offset):
        self.world = world
        self.x = pygame.mouse.get_pos()[0]
        self.y = pygame.mouse.get_pos()[1] - self.image.get_bounding_rect().h
        self.mouse.update(offset, world)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.target:
            if pygame.mouse.get_pressed()[0]:  # Left click.
                if self.show_window:
                    if 'L-MOUSE' in self.options:
                        if hasattr(self.data, self.options['L-MOUSE']):
                            getattr(self.data, self.options['L-MOUSE'])
                self.show_window = not self.show_window
            elif pygame.mouse.get_pressed()[2]:  # Right click.
                    if self.show_window:
                        if 'R-MOUSE' in self.options:
                            if hasattr(self.data, self.options['R-MOUSE']):
                                getattr(self.data, self.options['R-MOUSE'])

        elif event.event_type == GUI_TOOLTIP_OPTIONS:
            self.target = event.target
            self.options = {}
            if hasattr(event, 'l_mouse'):
                self.options['L-MOUSE'] = event.l_mouse
            if hasattr(event, 'r_mouse'):
                self.options['R-MOUSE'] = event.r_mouse
            self.update_data()

    def draw(self, screen):
        self.mouse.draw(screen)
        if self.show_window:
            screen.blit(self.image, (self.x, self.y))

