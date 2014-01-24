import pygame
from src.event_helper import *


class PowerUp(object):
    def __init__(self, type, amount):
        self.type = 'powerup'
        self.name = type
        self.amount = amount
        if amount >= 100:
            image_amount = 'large'
        elif amount > 50:
            image_amount = 'medium'
        elif amount > 25:
            image_amount = 'small'
        else:
            image_amount = 'tiny'
        self.font = pygame.font.Font('res/other/visitor2.ttf', 20)
        self.image = pygame.image.load('res/items/other/{0}_{1}.gif'.format(self.name.lower(), image_amount))
        self.x = 0
        self.y = 0
        self.options = {'LMouse': 'pickup'}

    def pickup(self, world):
        world.map.items.remove(self)
        if type(world.player.stats[self.name]) == list:
            world.player.stats[self.name][0] += self.amount
        else:

            world.player.stats[self.name] += self.amount

    def draw(self, screen, offset):
        screen.blit(self.image, (self.x*32 - offset.x, self.y*32 - offset.y))

        screen.blit(self.font.render(str(self.amount), 0, (192, 192, 192)), (self.x*32 - offset.x + 12, self.y*32 - offset.y + 16))


class Item(object):
    def __init__(self, name, category, image, stats, extra={}):
        self.name = name
        self.extra = extra
        self.type = 'item'
        self.category = category
        self.description = 'a {0}'.format(self.category)
        self.stats = stats
        if 'AMOUNT' in self.stats:
            self.stackable = True
        else:
            self.stackable = False

        self.picked_up = False
        self.equipped = False
        self.image = pygame.image.load(image)
        self.x = 0
        self.y = 0
        self.shadow = pygame.Surface((32, 32), pygame.SRCALPHA, 32)
        self.shadow.fill((0, 0, 0, 200))

    def use(self):
        pass

    def interact(self):
        r_mouse = ('examine', PLAYER_EXAMINE_ITEM)
        if self.picked_up:
            l_mouse = ('drop', PLAYER_DROP_ITEM)
            if self.equipped:
                mm_mouse = ('unquip', PLAYER_UNEQUIP_ITEM)
            else:
                mm_mouse = ('equip', PLAYER_EQUIP_ITEM)
        else:
            l_mouse = ('pick up', PLAYER_PICKUP_ITEM)
            mm_mouse = None

        post_event(GUI_TOOLTIP_POST, l_mouse=l_mouse, r_mouse=r_mouse, mm_mouse=mm_mouse, target=self)

    def draw(self, screen, offset, explored=1):
        if explored >= 0:
            screen.blit(self.image, (self.x*32 - offset.x, self.y*32 - offset.y))
        if explored == 0:
            screen.blit(self.shadow, (self.x*32 - offset.x, self.y*32 - offset.y))
