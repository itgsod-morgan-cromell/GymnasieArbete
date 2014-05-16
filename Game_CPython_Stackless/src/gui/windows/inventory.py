import pygame
from src.options import *
from src.event_helper import *


class Slot(object):
    def __init__(self, x, y, object=None):
        self.object = object
        self.type = 'inventory'
        self.selected = False
        self.bg = pygame.image.load('../res/gui/inventory_slot.png')
        if object:
            self.image = object
        else:
            self.image = pygame.Surface((32, 32), pygame.SRCALPHA, 32)
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, 32, 32)
        self.image.convert_alpha()

    def draw(self, surface):
        self.image.blit(self.bg, (0, 0))
        if self.object:
            if self.object.equipped:
                self.image.fill((0, 255, 0, 200), pygame.Rect(2, 2, 28, 28))
            self.image.blit(self.object.image, (0, 0))
        if self.selected:
            self.image.blit(cursor, (0, 0))

        surface.blit(self.image, (self.x, self.y))


class InventoryWindow(object):
    def __init__(self, player, rect):
        self.rect = rect
        self.width = rect.w
        self.height = rect.h
        self.x = rect.x
        self.y = rect.y
        spacing = 0
        self.image = pygame.Surface((self.width, self.height))
        slots_x = int(self.width/(32 + spacing))
        slots_y = int(self.height/(32 + spacing))
        self.slots = []
        for y in range(0, slots_y):
            for x in range(0, slots_x):
                self.slots.append(Slot(x*32, y * 32))
        register_handler([PLAYER_PICKUP_ITEM, PLAYER_DROP_ITEM, TIME_PASSED], self.handle_event)

    def get_slot(self, mouse):
        for slot in self.slots:
            if mouse.colliderect(slot.rect):
                return slot

    def clear_selected(self):
        for slot in self.slots:
            slot.selected = False

    def handle_event(self, event):
        etype = get_event_type(event)
        if etype in [pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, TIME_PASSED]:
            if etype == TIME_PASSED:
                mouse = pygame.Rect(pygame.mouse.get_pos(), (1, 1)).copy()
            else:
                mouse = pygame.Rect(event.pos, (1, 1)).copy()
            mouse.x -= WIDTH - MENU_WIDTH
            mouse.y -= INTERFACE_Y
            if mouse.colliderect(self.rect):
                mouse.x -= self.x
                mouse.y -= self.y
                slot = self.get_slot(mouse)
                if slot:
                    slot.selected = True
                if slot and slot.object:
                    post_event(GUI_EXAMINE_ITEM, tooltip=slot.object.examine())
                    post_event(GUI_INFOBAR_POST, msg=slot.object.name)
                    slot.object.interact('left')
                else:
                    post_event(GUI_EXAMINE_ITEM_CLEAR)
                    post_event(GUI_INFOBAR_CLEAR)

        elif etype == PLAYER_PICKUP_ITEM:
            for slot in self.slots:
                if not slot.object:
                    slot.object = event.target
                    return
        elif etype == PLAYER_DROP_ITEM:
            for slot in self.slots:
                if slot.object == event.target:
                    slot.object = None

    def draw(self, surface):
        self.image.fill(INTERFACE_COLOR)
        for slot in self.slots:
            slot.draw(self.image)
        surface.blit(self.image, (self.x, self.y))