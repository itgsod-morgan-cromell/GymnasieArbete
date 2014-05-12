from src.gui.gui import Gui
import pygame
from src.options import *
from src.event_helper import *


class Slot(object):
    def __init__(self, x, y, object=None):
        self.object = object
        self.type = 'explorer'
        if object:
            self.image = object
        else:
            self.image = pygame.Surface((32, 32))
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, 32, 32)

    def draw(self, surface):
        if self.object:
            self.image = self.object.image
        surface.blit(self.image, (self.x, self.y))


class Explorer(Gui):
    def __init__(self):
        self.width = MENU_WIDTH
        self.height = 80

        Gui.__init__(self, 'explorer', (30, 400),
                     pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32).convert_alpha(), False)
        self.slots = []
        self.slots_rect = []
        for y in range(0, 2):
            for x in range(0, 4):
                self.slots_rect.append(pygame.Rect(5 + x * 35, 5 + y * 35, 32, 32))
                self.slots.append(Slot(5 + x * 35, 5 + y * 35))
        register_handler([GUI_EXPLORER_ITEMS, GUI_EXPLORER_CLEAR, PLAYER_PICKUP_ITEM], self.handle_event)

    def handle_event(self, event):
        etype = get_event_type(event)

        if etype == GUI_EXPLORER_ITEMS:
            self.active = True
            for i, item in enumerate(event.items):
                self.slots[i].object = item
        elif etype == GUI_EXPLORER_CLEAR:
            for slot in self.slots:
                slot.object = None
                self.active = False
                slot.image = pygame.Surface((32, 32))
        elif etype == PLAYER_PICKUP_ITEM:
            if event.target in self.slots:
                self.slots.remove(event.target)


    def get_slot(self, mouse):
        mouse.x -= self.x
        mouse.y -= self.y
        slot = mouse.collidelist(self.slots_rect)
        if self.slots[slot] and slot != -1:
            return self.slots[slot]

    def mouse(self, mouse, event):
        if event.type == pygame.MOUSEMOTION:
            slot = self.get_slot(mouse)
            if slot and slot.object:

                post_event(GUI_EXAMINE_ITEM, tooltip=slot.object.examine())
            else:
                post_event(GUI_EXAMINE_ITEM_CLEAR)


    def draw(self, surface):
        if self.active:
            for slot in self.slots:
                slot.draw(self.image)
            surface.blit(self.image, (self.x, self.y))


