import glob
import pygame
import random
from src.items.item import *
from src.event_helper import *
from src.util.get_sprite import *
import os


class Chest(object):
    def __init__(self, pos, world):
        self.name = 'chest'
        self.type = 'chest'
        self.description = "It's a old chest. May contain some nice loot!"
        self.x = pos[0]
        self.y = pos[1]
        self.world = world
        self.level = self.world.floor
        self.used = False
        closed_img = pygame.image.load('../res/items/other/chest_closed.png')
        self.image = closed_img
        self.shadow = pygame.Surface((32, 32), pygame.SRCALPHA, 32)
        self.shadow.fill((0, 0, 0, 150))

    def use(self):
        if self.used:
            self.loot()
        else:
            self.open()

    def open(self):
        if not self.used:
            self.used = True
            open_img = pygame.image.load('../res/items/other/chest_open.png')
            self.image = open_img

    def loot(self):
        item = self.generate_loot()
        item.x = self.x
        item.y = self.y
        self.world.items.append(item)
        self.world.items.remove(self)
        self.world.dungeon.grid[self.y][self.x] = 1

    def interact(self):
        r_mouse = ('examine', PLAYER_EXAMINE_ITEM)

        action = 'open' if not self.used else 'loot'
        l_mouse = (action, PLAYER_USE_ITEM)
        post_event(PLAYER_ITEM_PROXIMITY, target=self, range=1, true=GUI_TOOLTIP_POST, args={'l_mouse': l_mouse, 'target': self})
        post_event(GUI_TOOLTIP_POST, r_mouse=r_mouse, target=self)

    def generate_loot(self):
        types = ['WEAPON']
        type = random.choice(types)

        if type == 'WEAPON':
            rarities = ['common', 'uncommon', 'rare', 'epic']
            rarity = random.randint(0, len(rarities) - 1)
            category = random.choice(['sword', 'bow', 'wand'])
            name = random.choice(open('../res/other/random names/{0}.txt'.format(category)).readlines())
            name = name.rstrip('\n')
            stats = {'DMG': random.randint(1, 5) * self.level * (rarity + 1)}
            if category == 'bow' or category == 'wand':
                stats['RANGE'] = 3 * (0.5 * self.level * (rarity + 1))
                if category == 'wand':
                    stats['COST'] = stats['DMG'] * random.randint(2, 5)
            return Item(name, 'weapon',
                        'RHand',
                        random.choice(os.listdir('../res/items/weapon')),
                        stats,
                        {'rarity': rarities[rarity]})

        elif type == 'POWERUP':

            return PowerUp(random.choice(['GOLD', 'HP']),
                           random.randint(10, 100) * self.level)

    def draw(self, screen, offset, explored):
        if explored:
            screen.blit(self.image, (self.x * 32 - offset.x, self.y * 32 - offset.y))
        if explored == 1:
            screen.blit(self.shadow, (self.x * 32 - offset.x, self.y * 32 - offset.y))