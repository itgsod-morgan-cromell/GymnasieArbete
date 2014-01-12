from src.gui.gui import Gui
import pygame
from src.gui.slot import Slot
from src.gui.textrect import *


class StatsUi(Gui):
    def __init__(self, player):
        width = 250
        height = 330
        image = pygame.Surface((width, height))
        image.fill((127, 127, 127), pygame.Rect((0, 0), (3, height)))
        Gui.__init__(self, 'character', (710, 0), image, True)
        self.stats = player.stats
        self.icon = player.icon
        self.stats_rect = pygame.Rect((15, 45), (220, 124))
        self.inventory_rect = pygame.Rect((15, self.stats_rect.y + self.stats_rect.h + 15), (220, 145))
        self.slots = [Slot(self.stats_rect.x+12, self.stats_rect.y+80), Slot(self.stats_rect.x+56, self.stats_rect.y+80), Slot(self.stats_rect.x+100, self.stats_rect.y+80)]
        self.inventory_slots = [None] * 10

    def update(self, world):
        self.stats = world.player.stats
        self.world = world
        self.slots[0].containts = self.world.player.weapon
        self.slots[1].containts = self.world.player.armor
        self.slots[2].containts = self.world.player.trinket
        for i in range(0, 10):
            if len(world.player.inventory) >= i + 1:
                item = world.player.inventory[i]
            else:
                item = None
            y = 12
            x = 12
            x += (44*i)
            if i+1 > 6:
                y += 2*44
                x -= 44*6
            elif i+1 > 3:
                y += 44
                x -= 44*3

            x += self.inventory_rect.x
            y += self.inventory_rect.y
            self.inventory_slots[i] = Slot(x, y, item)

    def draw(self, screen):
        self.draw_status()
        self.draw_stats()
        self.draw_inventory()
        screen.blit(self.image, (self.x, self.y))

    def draw_status(self):
        self.image.blit(pygame.image.load('res/gui/status.png'), (15, 5))
        if self.world.player.stats['STATUS']:
            self.image.blit(self.get_stat('STATUS', pygame.Rect((0, 0), (213, 28)), 1, (186, 186, 186)), (15 + 8, 5 + 7))

    def draw_stats(self):

        self.image.blit(pygame.image.load('res/gui/stats.png'), (self.stats_rect.x, self.stats_rect.y))
        self.image.blit(self.icon, (self.stats_rect.x + 12, self.stats_rect.y + 12))

        ### Draw bar stats ########
        hp_in_width = float(self.stats['HP'][0])/float(self.stats['HP'][1])
        hp_in_width *= 84
        self.image.fill((206, 0, 31), pygame.Rect((self.stats_rect.x+51, self.stats_rect.y+16), (hp_in_width, 8)))
        mp_in_width = float(self.stats['MP'][0])/float(self.stats['MP'][1])
        mp_in_width *= 84
        self.image.fill((62, 59, 255), pygame.Rect((self.stats_rect.x+51, self.stats_rect.y+32), (mp_in_width, 8)))
        ###########################

        ### Draw numeric stats ####
        text_rect = pygame.Rect((0, 0), (44, 30))
        self.image.blit(self.get_stat('LVL', text_rect, 0, (247, 226, 107)), (self.stats_rect.x + 53, self.stats_rect.y+51))
        self.image.blit(self.get_stat('DMG', text_rect, 2, (0, 200, 0)), (self.stats_rect.x+137, self.stats_rect.y+20))
        self.image.blit(self.get_stat('MAG', text_rect, 2, (0, 200, 0)), (self.stats_rect.x+137, self.stats_rect.y+51))
        self.image.blit(self.get_stat('DEF', text_rect, 2, (0, 200, 0)), (self.stats_rect.x+137, self.stats_rect.y+83))
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
        self.image.blit(self.get_stat('GOLD', pygame.Rect((0, 0), (100, 30)), 2, (186, 186, 186)), (self.inventory_rect.x+115, self.inventory_rect.y+10))

    def get_stat(self, stat, rect, alignment=0, color=(255, 255, 255)):
        if stat in self.stats:
            text = render_textrect(self.stats[stat], 27, rect, color, None, alignment)
            return text
        else:
            print "No such type exists."




