import pygame
from src.options import *
from src.event_helper import *
from collections import OrderedDict
from src.gui.windows import *


class NavigationButton(object):
    def __init__(self, category, x, y):
        self.category = category
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, 20, 20)
        self.states = {
            'selected': pygame.image.load('../res/gui/tab_selected_square.png'),
            'unselected': pygame.image.load('../res/gui/tab_unselected_square.png'),
            'hover': pygame.image.load('../res/gui/tab_hover_square.png')
        }
        self.state = 'unselected'
        self.image = pygame.image.load('../res/gui/buttons/{0}.png'.format(category))
        register_handler(GUI_INTERFACE_BUTTON, self.handle_event)

    def handle_event(self, event):
        etype = get_event_type(event)
        if etype == pygame.MOUSEMOTION:
            if self.state != 'selected':
                post_event(GUI_INTERFACE_BUTTON, button=self, state='hover')
        elif etype == pygame.MOUSEBUTTONDOWN:
            if self.state != 'selected':
                post_event(GUI_INTERFACE_BUTTON, button=self, state='selected')
        elif etype == GUI_INTERFACE_BUTTON:
            if event.button == self:
                self.state = event.state
            elif event.button:
                if self.state == 'selected':
                    if event.state != 'hover':
                        self.state = 'unselected'
                else:
                    self.state = 'unselected'
            elif self.state == 'hover':
                self.state = 'unselected'


    def draw(self, surface):
        surface.blit(self.states[self.state], (self.x, self.y))
        surface.blit(self.image, (self.x, self.y))


class InterfaceManager(object):
    def __init__(self, world):
        self.world = world
        self.x = 0
        self.y = 300
        self.width = MENU_WIDTH
        self.height = 200
        self.rect = (self.x, self.y, self.width, self.height)
        self.image = pygame.Surface((self.width, self.height))
        windows_x = 20
        windows_width = MENU_WIDTH - windows_x
        windows_height = 200
        window_rect = pygame.Rect(windows_x, 0, windows_width, windows_height)
        self.buttons = OrderedDict({})
        self.active_window = 'inventory'
        self.windows = OrderedDict({})
        self.windows['inventory'] = InventoryWindow(self.world, window_rect)
        self.windows['stats'] = StatsWindow(self.world.player, window_rect)
        i = 0
        for window in self.windows:
            self.buttons[window] = NavigationButton(window, 0, i * 20)
            i += 1

        register_handler([pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION], self.handle_event)

    def update(self):
        for button in self.buttons:
            if self.buttons[button].state == 'selected':
                self.active_window = button

    def handle_event(self, event):
        post_event(GUI_EXAMINE_ITEM_CLEAR)
        post_event(GUI_INTERFACE_BUTTON, button=None)
        mouse = pygame.Rect(event.pos, (1, 1)).copy()
        mouse.x -= WIDTH - MENU_WIDTH
        if mouse.colliderect(self.rect):
            mouse.x -= self.x
            mouse.y -= self.y
            for window in self.windows:
                if mouse.colliderect(self.windows[window].rect) and self.active_window == window:
                    self.windows[window].handle_event(event)
            for button in self.buttons:
                if mouse.colliderect(self.buttons[button].rect):
                    self.buttons[button].handle_event(event)


    def draw(self, surface):
        self.image.fill((54, 54, 54))
        for button in self.buttons:
            self.buttons[button].draw(self.image)
        self.windows[self.active_window].draw(self.image)


        surface.blit(self.image, (self.x, self.y))