import pygame
from src.gui.textrect import *
from src.options import *

class StatsWindow(object):
    def __init__(self, player, rect):
        self.rect = rect
        self.width = rect.w
        self.height = rect.h
        self.x = rect.x + 20
        self.y = rect.y
        self.image = pygame.Surface((self.width, self.height))
        self.starting_stats = player.classdata.pfs
        self.stats = player.stats
        self.stat_list = []
        self.text_size = 12
        i = 0
        for stat, value in self.starting_stats.items():
            if value != 0:
                text = '{0}: {1} + {2}'.format(stat, value, self.stats[stat] - value)
                rect = pygame.Rect(0, self.text_size * i, 100, self.text_size*2)
                image = render_textrect(text, self.text_size, rect, (255, 255, 255))
                self.stat_list.append((image, rect))
                i += 1

    def update(self):
        self.stat_list = []
        i = 0
        for stat, value in self.starting_stats.items():
            if value != 0:
                text = '{0}: {1} + {2}'.format(stat, value, self.stats[stat] - value)
                rect = pygame.Rect(0, self.text_size * i, 100, self.text_size*2)
                image = render_textrect(text, self.text_size, rect, (255, 255, 255))
                self.stat_list.append((image, rect))
                i += 1

    def handle_event(self, event):
        pass

    def draw(self, surface):
        self.image.fill(INTERFACE_COLOR)
        for stat in self.stat_list:
            self.image.blit(stat[0], (stat[1].x, stat[1].y))
        surface.blit(self.image, (self.x, self.y))