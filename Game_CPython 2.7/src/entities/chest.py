import glob
import pygame
from src.entities.entity import Entity
import random
from src.items.item import *
from src.level.generator.map_loader import Tile


class Chest(Entity):
    def __init__(self, tile, world, level):
        Entity.__init__(self, 'Chest', (tile.x, tile.y), world)
        self.level = level
        self.used = False
        self.prev = tile
        closed_img = self.prev.image
        closed_img.blit(pygame.image.load('res/items/other/chest_closed.png'), (0, 0))
        self.image = closed_img

    def open(self):
        if not self.used:
            self.used = True
            open_img = self.prev.image
            open_img.blit(pygame.image.load('res/items/other/chest_open.png'), (0, 0))
            self.image = open_img

    def loot(self):
        if self.used:
            item = self.generate_loot()
            x = self.x/self.prev.w
            y = self.y/self.prev.h
            item.x = x
            item.y = y
            self.world.map.entities.append(item)
            self.world.map.map.tiles[y][x] = Tile(self.x, self.y, self.prev.w, self.prev.h, self.prev.id)

    def generate_loot(self):
        types = ['POWERUP', 'WEAPON']
        type = random.choice(types)
        print type

        if type == 'WEAPON':
            rarities = ['common', 'uncommon', 'rare', 'epic']
            rarity = random.randint(0, len(rarities) - 1)
            category = random.choice(['swords', 'bows', 'wands'])
            name = random.choice(open('res/other/random names/{0}.txt'.format(category)).readlines())
            stats = {'DMG': random.randint(1, 5) * self.level * (rarity + 1)}
            if category == 'bows' or category == 'wands':
                stats['RANGE'] = 3 * (0.5 * self.level * (rarity + 1))
                if category == 'wands':
                    stats['COST'] = stats['DMG'] * random.randint(2, 5)
            return Item(name,
                        'weapon',
                        random.choice(glob.glob('res/items/weapons/{0}/*'.format(category))),
                        stats,
                        {'rarity': rarities[rarity]})

        elif type == 'POWERUP':

            return PowerUp(random.choice(['GOLD', 'HP']),
                           random.randint(10, 100) * self.level)
