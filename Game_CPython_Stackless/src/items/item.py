import pygame
from src.event_helper import *
from src.options import *
from src.gui.textrect import render_textrect


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
        self.font = pygame.font.Font('../res/other/visitor2.ttf', 20)
        self.image = pygame.image.load('../res/items/other/{0}_{1}.gif'.format(self.name.lower(), image_amount))
        self.x = 0
        self.y = 0
        self.options = {'LMouse': 'pickup'}

    def pickup(self, world):
        world.map.items.remove(self)


    def draw(self, screen, offset):
        screen.blit(self.image, (self.x * 32 - offset.x, self.y * 32 - offset.y))

        screen.blit(self.font.render(str(self.amount), 0, (192, 192, 192)),
                    (self.x * 32 - offset.x + 12, self.y * 32 - offset.y + 16))


class Item(object):
    def __init__(self, name, category, slot, image, stats, extra={}):
        self.name = name
        self.extra = extra
        self.type = 'item'
        self.category = category
        self.slot = slot
        self.description = 'a {0}'.format(self.category)
        self.stats = stats
        if 'AMOUNT' in self.stats:
            self.stackable = True
        else:
            self.stackable = False

        self.picked_up = False
        self.equipped = False
        self.image = pygame.image.load('../res/items/{0}/{1}'.format(category, image))
        self.equipped_image = pygame.image.load('../res/entities/player/equipment/{0}/{1}'.format(slot, image))
        self.x = 0
        self.y = 0
        self.shadow = pygame.Surface((32, 32), pygame.SRCALPHA, 32)
        self.shadow.fill((0, 0, 0, 150))
        self.stats_font = pygame.font.Font('../res/other/visitor2.ttf', 20)

    def use(self):
        pass

    def interact(self, orientation=None):

        if self.picked_up:
            if self.equipped:
                r_mouse = ('unequip', PLAYER_UNEQUIP_ITEM)
            else:
                r_mouse = ('equip', PLAYER_EQUIP_ITEM)
        else:
            r_mouse = ('examine', PLAYER_EXAMINE_ITEM)
            l_mouse = ('pick up', PLAYER_PICKUP_ITEM)
            post_event(PLAYER_ITEM_PROXIMITY, target=self, range=0, true=GUI_TOOLTIP_POST, args={'l_mouse': l_mouse, 'target': self})

        post_event(GUI_TOOLTIP_POST, r_mouse=r_mouse, target=self, orientation=orientation)


    def examine(self):
        width = 250
        info = pygame.Surface((width, 80))
        info.fill((54, 54, 54))
        info.blit(self.image, (0, 0))
        info.blit(render_textrect(self.name, 32, pygame.Rect(0, 0, width, 40), eval(self.extra['rarity'])), (40, 1))
        info.blit(render_textrect(self.description, 15, pygame.Rect(0, 0, width, 40), (255, 255, 255)), (0, 45))

        stats = pygame.Surface((width, 50))
        stats.fill((54, 54, 54))
        y = 0
        for stat, i in self.stats.items():
            stats.blit(self.stats_font.render('{0}: '.format(stat), 0, (255, 255, 255)), (0, y * 10))
            stats.blit(self.stats_font.render(str(i), 0, (255, 255, 143)),
                       (self.stats_font.size('{0}: '.format(stat))[0], y * 10))
            y += 1
        image = pygame.Surface((width + 20, info.get_rect().h + stats.get_rect().h + 20))
        image.fill((54, 54, 54))
        image.blit(info, (10, 10))
        image.blit(stats, (10, info.get_rect().h + 20))
        pygame.draw.line(image, (0, 0, 0), (10, info.get_rect().h + 13),
                         (info.get_rect().w + 10, info.get_rect().h + 13), 2)
        pygame.draw.rect(image, (155, 155, 155), image.get_rect(), 1)
        return image

    def draw(self, screen, offset, explored=1):
        if explored:
            screen.blit(self.image, (self.x * 32 - offset.x, self.y * 32 - offset.y))
        if explored == 1:
            screen.blit(self.shadow, (self.x * 32 - offset.x, self.y * 32 - offset.y))
