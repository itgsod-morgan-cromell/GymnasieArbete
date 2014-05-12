import pygame
from src.gui.char_stat import CharStats

from src.gui.explorer import Explorer
from src.gui.inventory_gui import InventoryGui
from src.gui.minimap import MiniMap
from src.options import *
from src.event_helper import *
import copy


class GuiHandler(object):
    def __init__(self, world):
        self.rect = pygame.Rect((WIDTH - MENU_WIDTH, 0), (MENU_WIDTH, HEIGHT))
        self.bg = pygame.Surface((self.rect.w, self.rect.h))
        self.char_stat = CharStats(world)
        self.minimap = MiniMap(world)
        self.explorer = Explorer()
        self.inventory = InventoryGui()
        register_handler([pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION], self.handle_event)
        self.held_item = None

    def update(self, world):
        pass

    def handle_event(self, event):
        mouse_rect = pygame.Rect(event.pos, (2, 2)).copy()
        mouse_rect.x -= self.rect.x
        mouse_rect.y -= self.rect.y
        slot = None
        gui = self.get_gui(mouse_rect)

        if gui == self.char_stat:
            self.char_stat.mouse(mouse_rect, event)
        elif gui == self.minimap:
            self.minimap.mouse(mouse_rect, event)
        elif gui == self.explorer:
            self.explorer.mouse(mouse_rect, event)
            slot = self.explorer.get_slot(mouse_rect)
            if event.type == pygame.MOUSEBUTTONUP and self.held_item:
                if slot and not slot.object:
                    if self.held_item.type == 'inventory':
                        post_event(GUI_EXPLORER_CLEAR)
                        post_event(PLAYER_DROP_ITEM, target=self.held_item.object)
                    elif self.held_item.type == 'explorer':
                        slot.object = self.held_item.object
        else:
            post_event(GUI_EXAMINE_ITEM_CLEAR)

        if gui == self.inventory:
            self.inventory.mouse(mouse_rect, event)
            slot = self.inventory.get_slot(mouse_rect)
            if event.type == pygame.MOUSEBUTTONUP and self.held_item:
                if slot and not slot.object:
                    if self.held_item.type == 'explorer':
                        post_event(PLAYER_PICKUP_ITEM, target=self.held_item.object, slot=slot)
                    elif self.held_item.type == 'inventory':
                        slot.object = self.held_item.object

        if event.type == pygame.MOUSEBUTTONDOWN:
            if slot and slot.object:
                self.held_item = copy.copy(slot)
                slot.object = None
                pygame.mouse.set_visible(False)
                slot.image = pygame.Surface((32, 32))
                post_event(GUI_EXAMINE_ITEM_CLEAR)

        if event.type == pygame.MOUSEBUTTONUP:
            if self.held_item:
                if not slot:
                    if self.held_item.type == 'inventory':
                        if mouse_rect.x < 0:
                            post_event(PLAYER_DROP_ITEM, target=self.held_item.object)
                        else:
                            self.inventory.slots[
                                self.inventory.slots_rect.index(self.held_item.rect)].object = self.held_item.object
                    elif self.held_item.type == 'explorer':
                        self.explorer.slots[
                            self.explorer.slots_rect.index(self.held_item.rect)].object = self.held_item.object
                self.held_item = None
            pygame.mouse.set_visible(True)


    def get_gui(self, mouse):
        if mouse.colliderect(pygame.Rect(self.char_stat.x, self.char_stat.y,
                                         self.char_stat.width, self.char_stat.height)):
            return self.char_stat
        elif mouse.colliderect(pygame.Rect(self.minimap.x, self.minimap.y,
                                           self.minimap.width, self.minimap.height)):
            return self.minimap
        elif mouse.colliderect(pygame.Rect(self.explorer.x, self.explorer.y,
                                           self.explorer.width, self.explorer.height)):
            return self.explorer
        elif mouse.colliderect(pygame.Rect(self.inventory.x, self.inventory.y,
                                           self.inventory.width, self.inventory.height)):
            return self.inventory


    def draw(self, screen):
        self.bg.fill((54, 54, 54))
        self.minimap.draw(self.bg)
        self.char_stat.draw(self.bg)
        self.explorer.draw(self.bg)
        self.inventory.draw(self.bg)
        screen.blit(self.bg, (self.rect.x, self.rect.y))
        if self.held_item:
            screen.blit(self.held_item.object.image, (pygame.mouse.get_pos()[0] - 16, pygame.mouse.get_pos()[1] - 16))
