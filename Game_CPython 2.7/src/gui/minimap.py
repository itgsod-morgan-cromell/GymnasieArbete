import pygame
from src.gui.gui import Gui
from src.level.generator.map_loader import Map
import copy


class MiniMap(Gui):
    def __init__(self, world):
        self.world = copy.copy(world)
        width = 250
        height = 150
        image = pygame.Surface((width, height))
        image.fill((127, 127, 127), pygame.Rect((0, 0), (3, height)))
        image.fill((127, 127, 127), pygame.Rect((0, height-3), (width, 3)))
        world.map.dungeon.tile_w = world.map.dungeon.tile_h = 4
        self.map = Map()
        self.map.load_dungeon(world.map.dungeon, True)

        self.myfont = pygame.font.Font('res/other/font.ttf', 27)


        Gui.__init__(self, 'minimap', (world.player.playable_area.w, 330), image, True)

        self.image.blit(pygame.image.load('res/gui/minimap.png'), (15, 15))
        floor = self.myfont.render(str(self.world.map.floor), 0, (64, 96, 31))
        self.map.draw(self.image, pygame.Rect(0, 0, 0, 0))
        self.image.blit(floor, (15+187, 15+7))

    def update(self, world):
        self.world = world
        world.map.dungeon.tile_w = world.map.dungeon.tile_h = 4


    def draw(self, screen):

        map_offset = pygame.Rect((self.world.player.x/2, self.world.player.y/2), (self.image.get_rect().w, self.image.get_rect().w))

        self.image.fill((0, 255, 0), pygame.Rect((self.world.player.x*4 - map_offset.x, self.world.player.y*4 - map_offset.y), (4, 4)))
        screen.blit(self.image, (self.x, self.y))