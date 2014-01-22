from src.gui.gui import Gui
import pygame
from src.gui.textrect import *


class Field(object):
    def __init__(self, rect, data, color=(255, 255, 255)):
        self.data  = data
        if type(data) == str:
            self.image = render_textrect(data, 50, rect, color)
        else:
            self.image = data
        self.rect = rect

    def change_text(self, text, color=(255, 255, 255)):
        self.data = text
        self.image = render_textrect(text, 50, self.rect, color)


class Explorer(Gui):
    def __init__(self, world):
        width = 250
        height = 200
        image = pygame.Surface((width, height))
        image.fill((127, 127, 127), pygame.Rect((0, 0), (3, height)))
        image.fill((127, 127, 127), pygame.Rect((0, height-3), (width, 3)))
        self.icon = Field(pygame.Rect((15 + 16, 10 + 16), (32, 32)), None)
        self.info = Field(pygame.Rect((15 + 60, 10 + 5), (150, 65)), " ")
        self.subinfo = Field(pygame.Rect((15 + 16, 10 + 70), (150, 44)), "+ 10")
        self.myfont = pygame.font.Font('res/other/font.ttf', 27)

        Gui.__init__(self, 'explorer', (world.player.playable_area.w, 330 + 150 - 3), image, True)

    def update(self, world, data):
        if data:
            if hasattr(data, 'icon'):
                if self.icon.image != data.icon:
                    self.icon.image = data.icon
            elif hasattr(data, 'image'):
                if self.icon.image != data.image:
                    self.icon.image = data.image
            if hasattr(data, 'name'):
                if self.info.data != data.name:
                    self.info.change_text(data.name)
            if data.type == 'item':
                stats = ''
                for key, value in data.stats.iteritems():
                    sign = '+' if value > 0 else ''
                    stats += '\n{0}: {1}{2}'.format(key, sign, value)
                    if self.subinfo.data != stats:
                        self.subinfo.change_text(stats)
                if 'rarity' in data.extra:
                    if data.extra['rarity'] == 'epic':
                        self.info.change_text(data.name, (163, 53, 238))

        else:
            self.icon.image = None
            self.info.change_text(' ')
            self.subinfo.change_text(' ')
    def draw(self, screen):
        self.image.blit(pygame.image.load('res/gui/explorer.png'), (15, 10))
        if self.icon.image:
            self.image.blit(self.icon.image, (self.icon.rect.x, self.icon.rect.y))
        self.image.blit(self.info.image, (self.info.rect.x, self.info.rect.y))
        self.image.blit(self.subinfo.image, (self.subinfo.rect.x, self.subinfo.rect.y))
        screen.blit(self.image, (self.x, self.y))


