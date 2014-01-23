import glob
import pygame
import random
from src.items.item import *
from src.constants import *


class Chest(object):
    def __init__(self, pos, world):
        self.name = 'chest'
        self.type = 'chest'
        self.description = "It's a old chest. May contain some nice loot!"
        self.x = pos[0]
        self.y = pos[1]
        self.world = world
        self.level = self.world.map.floor
        self.used = False
        closed_img = pygame.image.load('res/items/other/chest_closed.png')
        self.image = closed_img
        self.shadow = pygame.Surface((32, 32), pygame.SRCALPHA, 32)
        self.shadow.fill((0, 0, 0, 200))

    def use(self):
        if self.used:
            self.loot()
        else:
            self.open()

    def open(self):
        if not self.used:
            self.used = True
            open_img = pygame.image.load('res/items/other/chest_open.png')
            self.image = open_img

    def loot(self):
        item = self.generate_loot()
        item.x = self.x
        item.y = self.y
        self.world.map.items.append(item)
        self.world.map.items.remove(self)
        self.world.map.dungeon.grid[self.y][self.x] = 1

    def interact(self):
        r_mouse = ('examine', PLAYER_EXAMINE_ITEM)
        action = 'open' if not self.used else 'loot'
        l_mouse = (action, PLAYER_USE_ITEM)
        post_event(GUI_TOOLTIP_POST, l_mouse=l_mouse, r_mouse=r_mouse, target=self)

    def generate_loot(self):
        types = ['WEAPON']
        type = random.choice(types)

        if type == 'WEAPON':
            rarities = ['common', 'uncommon', 'rare', 'epic']
            rarity = random.randint(0, len(rarities) - 1)
            category = random.choice(['swords', 'bows', 'wands'])
            name = random.choice(open('res/other/random names/{0}.txt'.format(category)).readlines())
            name = name.rstrip('\n')
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

    def draw(self, screen, offset, explored):
        if explored >= 0:
            screen.blit(self.image, (self.x*32 - offset.x, self.y*32 - offset.y))
        if explored == 0:
            screen.blit(self.shadow, (self.x*32 - offset.x, self.y*32 - offset.y))