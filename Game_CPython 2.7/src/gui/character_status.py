import math
from src.gui.gui import Gui
import pygame
from src.gui.slot import Slot
from src.gui.textrect import *
import copy


class StatsUi(Gui):
    def __init__(self, world):
        self.world = world
        width = 250
        height = 345
        image = pygame.Surface((width, height))
        image.fill((127, 127, 127), pygame.Rect((0, 0), (3, height)))

        Gui.__init__(self, 'character', (world.player.playable_width, 0), image, True)
        self.stats = copy.copy(world.player.stats)
        self.icon = world.player.icon

        self.stats_rect = pygame.Rect((15, 45), (220, 124))
        self.inventory_rect = pygame.Rect((15, self.stats_rect.y + self.stats_rect.h + 30), (220, 160))
        self.slots = [Slot(self.stats_rect.x+12, self.stats_rect.y+80), Slot(self.stats_rect.x+56, self.stats_rect.y+80), Slot(self.stats_rect.x+100, self.stats_rect.y+80)]
        self.inventory_slots = [None] * 20
        self.stats_font = {}
        self.update_stats()
        self.show_inventory = True

    def update(self, world):
        self.world = world
        self.slots[0].containts = self.world.player.weapon
        self.slots[1].containts = self.world.player.armor
        self.slots[2].containts = self.world.player.trinket
        for i in range(20):
            if len(world.player.inventory) >= i + 1:
                item = world.player.inventory[i]
            else:
                item = None
            y = 7
            x = 7
            x += (33*i) % 165
            y += math.trunc(i/5 - 0.1)*33
            if i > 4:
                y += 33

            x += self.inventory_rect.x
            y += self.inventory_rect.y
            self.inventory_slots[i] = Slot(x, y, item)
            for key in world.player.stats.keys():
                if not key in self.stats or self.stats[key] != world.player.stats[key]:
                    self.stats = copy.copy(world.player.stats)
                    self.update_stats()

    def update_stats(self):

        text_rect = pygame.Rect((0, 0), (44, 30))
        self.stats_font['LVL'] = self.get_stat(self.world.player.lvl, text_rect, 0, (247, 226, 107))
        self.stats_font['DMG'] = self.get_stat('STR', text_rect, 2, (0, 200, 0))
        self.stats_font['MAG'] = self.get_stat('WIS', text_rect, 2, (0, 200, 0))
        self.stats_font['DEF'] = self.get_stat('CON', text_rect, 2, (0, 200, 0))
        self.stats_font['GOLD'] = self.get_stat(self.world.player.gold, pygame.Rect((0, 0), (100, 30)), 2, (186, 186, 186))

    def draw(self, screen):
        self.draw_status()
        self.draw_stats()
        self.draw_inventory()

        screen.blit(self.image, (self.x, self.y))

    def draw_status(self):
        self.image.blit(pygame.image.load('res/gui/status.png'), (15, 5))


    def draw_stats(self):

        self.image.blit(pygame.image.load('res/gui/stats.png'), (self.stats_rect.x, self.stats_rect.y))
        self.image.blit(self.icon, (self.stats_rect.x + 12, self.stats_rect.y + 12))

        ### Draw bar stats ########
        hp_in_width = float(self.world.player.hp)/float(self.stats['HP'])
        hp_in_width *= 84
        self.image.fill((206, 0, 31), pygame.Rect((self.stats_rect.x+51, self.stats_rect.y+16), (hp_in_width, 8)))
        mp_in_width = float(self.world.player.mp)/float(self.stats['MP'])
        mp_in_width *= 84
        self.image.fill((62, 59, 255), pygame.Rect((self.stats_rect.x+51, self.stats_rect.y+32), (mp_in_width, 8)))
        ###########################

        ### Draw numeric stats ####
        self.image.blit(self.stats_font['LVL'], (self.stats_rect.x + 53, self.stats_rect.y+51))
        self.image.blit(self.stats_font['DMG'], (self.stats_rect.x+137, self.stats_rect.y+20))
        self.image.blit(self.stats_font['MAG'], (self.stats_rect.x+137, self.stats_rect.y+51))
        self.image.blit(self.stats_font['DEF'], (self.stats_rect.x+137, self.stats_rect.y+83))
        ###########################

        ### Draw items in slots ###
        for slot in self.slots:
            if slot.containts:
                self.image.blit(slot.containts.image, (slot.x, slot.y))
        ###########################

    def draw_inventory(self):
        self.image.blit(pygame.image.load('res/gui/inventory.png'), (self.inventory_rect.x, self.inventory_rect.y))
        for slot in self.inventory_slots:
            if slot:
                if slot.containts:
                    self.image.blit(slot.containts.image, (slot.x, slot.y))
        self.image.blit(self.stats_font['GOLD'], (self.inventory_rect.x+115, self.inventory_rect.y+10))

    def get_stat(self, stat, rect, alignment=0, color=(255, 255, 255)):

        if stat in self.stats:
            text = render_textrect(self.stats[stat], 50, rect, color, None, alignment)
            return text
        elif type(stat) == int:
            text = render_textrect(str(stat), 50, rect, color, None, alignment)
            return text
        else:
            print "No such type exists."




