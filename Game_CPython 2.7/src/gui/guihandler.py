import pygame
from src.gui.char_stat import CharStats

from src.gui.explorer import Explorer
from src.gui.minimap import MiniMap
from src.options import *


class GuiHandler(object):
    def __init__(self, world):
        self.rect = pygame.Rect((WIDTH-MENU_WIDTH, 0), (MENU_WIDTH, HEIGHT))
        self.bg = pygame.Surface((self.rect.w, self.rect.h))
        self.char_stat = CharStats(world)
        self.minimap = MiniMap(world)
        #self.explorer = Explorer(world)
       # self.console = Console(world_screen)

    def update(self, world):
        pass

    def draw(self, screen):
        self.bg.fill((54, 54, 54))
        self.minimap.draw(self.bg)
        self.char_stat.draw(self.bg)
        screen.blit(self.bg, (self.rect.x, self.rect.y))
