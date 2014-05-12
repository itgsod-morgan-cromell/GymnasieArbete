import pygame
from src.gui.gui import Gui
from src.level.dungeon_generator.map_loader import Map
from src.options import *
from src.event_helper import *


class ZoomArrow(object):
    """
    Simple helper class for the zoom in arrows of the minimap.
    dir: 0 == up/in    1 == down/out
    """

    def __init__(self, dir, pos):
        self.arrow = pygame.Surface((12, 6), pygame.SRCALPHA, 32).convert_alpha()
        self.color = (255, 255, 255)
        self.rect = self.arrow.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.dir = dir
        self.zoom_level = 0
        self.max_zoom_level = 2

    def create(self):
        if self.zoom_level > self.max_zoom_level - 1:
            self.color = (127, 127, 127)
        else:
            self.color = (255, 255, 255)
        if self.dir == 0:
            pygame.draw.polygon(self.arrow, self.color, [(0, 6), (6, 0), (12, 6)])
        elif self.dir == 1:
            pygame.draw.polygon(self.arrow, self.color, [(0, 0), (6, 6), (12, 0)])


class MiniMap(Gui):
    def __init__(self, world):
        self.world = world
        self.tile_size = 6
        self.width = 192
        self.height = 192
        self.camera = pygame.Rect((0, 0), (self.width, self.height)).copy()
        self.map = Map()
        self.map.load_dungeon(world.map.dungeon, None, True, self.tile_size)
        self.zoom_in_arrow = ZoomArrow(0, (174, 10))
        self.zoom_in_arrow.create()
        self.zoom_out_arrow = ZoomArrow(1, (174, 20))
        self.zoom_out_arrow.create()

        Gui.__init__(self, 'minimap', (4, 4), pygame.Surface((self.width, self.height)), True)
        x = self.world.player.x * self.tile_size
        y = self.world.player.y * self.tile_size
        self.camera.center = (x, y)
        self.map.draw(self.image, self.camera, self.world.map.map.tiles)
        self.image.fill((0, 255, 0), pygame.Rect((x - self.camera.x, y - self.camera.y),
                                                 (self.tile_size, self.tile_size)))
        self.image.blit(self.zoom_in_arrow.arrow, (self.zoom_in_arrow.rect.x, self.zoom_in_arrow.rect.y))
        self.image.blit(self.zoom_out_arrow.arrow, (self.zoom_out_arrow.rect.x, self.zoom_out_arrow.rect.y))

        register_handler([TIME_PASSED, pygame.MOUSEBUTTONDOWN], self.handle_event)

    def redraw(self):
        self.image.fill((0, 0, 0))
        x = self.world.player.x * self.tile_size
        y = self.world.player.y * self.tile_size
        self.camera.center = (x, y)
        self.map.load_dungeon(self.world.map.dungeon, None, True, self.tile_size)
        self.map.draw(self.image, self.camera)
        self.image.fill((0, 255, 0), pygame.Rect((x - self.camera.x, y - self.camera.y),
                                                 (self.tile_size, self.tile_size)))
        self.zoom_in_arrow.create()
        self.zoom_out_arrow.create()
        self.image.blit(self.zoom_in_arrow.arrow, (self.zoom_in_arrow.rect.x, self.zoom_in_arrow.rect.y))
        self.image.blit(self.zoom_out_arrow.arrow, (self.zoom_out_arrow.rect.x, self.zoom_out_arrow.rect.y))

    def handle_event(self, event):
        etype = get_event_type(event)
        if etype == TIME_PASSED:
            self.redraw()
        elif etype == pygame.MOUSEBUTTONDOWN and event.button in [4, 5]:
            if event.button == 4:
                self.zoom_in()
            elif event.button == 5:
                self.zoom_out()

    def mouse(self, mouse, event):
        mouse.x -= self.x
        mouse.y -= self.y
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if mouse.colliderect(self.zoom_in_arrow.rect):
                    self.zoom_in()
                elif mouse.colliderect(self.zoom_out_arrow.rect):
                    self.zoom_out()

    def zoom_in(self):
        if self.zoom_in_arrow.zoom_level < self.zoom_in_arrow.max_zoom_level:
            self.zoom_in_arrow.zoom_level += 1
            self.zoom_out_arrow.zoom_level -= 1
            self.tile_size += 2
            self.redraw()

    def zoom_out(self):
        if self.zoom_out_arrow.zoom_level < self.zoom_out_arrow.max_zoom_level:
            self.zoom_out_arrow.zoom_level += 1
            self.zoom_in_arrow.zoom_level -= 1
            self.tile_size -= 2
            self.redraw()


    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))