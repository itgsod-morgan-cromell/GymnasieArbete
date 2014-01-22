import pygame
from src.gui.character_status import StatsUi
from src.gui.explorer import Explorer
from src.gui.minimap import MiniMap
from src.gui.mouse_gui import MouseGui
from src.gui.console import Console


class GuiHandler(object):
    def __init__(self, world, world_screen):
        self.player_stats = StatsUi(world)
        self.minimap = MiniMap(world)
        self.explorer = Explorer(world)
        self.console = Console(world, world_screen)
        self.mouse_col = (0, 255, 0)
        self.mouse = None
        self.mouse_grid_x = 0
        self.mouse_grid_y = 0
        self.mouse_gui = MouseGui(world)
        self.mouse_img = pygame.Surface((32, 32), pygame.SRCALPHA, 32)
        self.mouse_img.convert_alpha()


    def update(self, world, offset):
        self.mouse_col = (255, 0, 0)
        self.player_stats.update(world)
        self.minimap.update(world)
        self.explorer.update(world, self.mouse)
        self.mouse_gui.update(world, offset)
        self.console.update(world)

    def draw(self, screen, offset):
        self.player_stats.draw(screen)
        self.minimap.draw(screen)
        self.explorer.draw(screen)
        self.console.draw(screen)
        self.mouse_gui.draw(screen)
