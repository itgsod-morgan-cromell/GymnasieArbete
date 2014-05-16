import pygame
from src.gui.char_stat import CharStats
from src.event_helper import *
from src.gui.minimap import MiniMap
from src.gui.interface_manager import InterfaceManager
from src.options import *


class GuiHandler(object):
    def __init__(self, world):
        self.rect = pygame.Rect((WIDTH - MENU_WIDTH, 0), (MENU_WIDTH, HEIGHT))
        self.bg = pygame.Surface((self.rect.w, self.rect.h))
        self.char_stat = CharStats(world)
        self.minimap = MiniMap(world)
        self.interface_manager = InterfaceManager(world)
        self.held_item = None


    def update(self):
        self.char_stat.update()
        self.interface_manager.update()

    def draw(self, screen):
        self.bg.fill(INTERFACE_COLOR)
        self.minimap.draw(self.bg)
        self.char_stat.draw(self.bg)
        self.interface_manager.draw(self.bg)
        screen.blit(self.bg, (self.rect.x, self.rect.y))
        if self.held_item:
            screen.blit(self.held_item.object.image, (pygame.mouse.get_pos()[0] - 16, pygame.mouse.get_pos()[1] - 16))
