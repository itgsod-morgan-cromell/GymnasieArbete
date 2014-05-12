from src.gui.textrect import *
from src.event_helper import *
from src.options import *
from src.gui.slot import Slot
from src.gui.gui import Gui
import pygame


class Bar(object):
    def __init__(self, current, max, info, color, pos):
        self.info = info
        self.current = current
        self.max = max
        self.color = color
        self.info = info
        self.hovering = ALWAYS_SHOW_STATS
        self.image = pygame.Surface((176, 16))
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.image.fill((84, 84, 84))
        width = int((self.current / self.max) * self.image.get_width())
        self.image.fill(color, rect=pygame.Rect((0, 0), (width, self.image.get_height())))
        self.image.blit(render_textrect(str(info), 50, self.rect, (255, 255, 255)), (3, 0))
        self.text = '{0}/{1}'.format(self.current, self.max)
        if self.hovering:
            self.image.blit(render_textrect(self.text, 50, self.rect, (255, 255, 255), None, 1, ), (0, 0))

    def refresh(self, new_value=None):
        if new_value:
            self.current = new_value
        self.image.fill((84, 84, 84))
        width = int((self.current / self.max) * self.image.get_width())
        self.image.fill(self.color, rect=pygame.Rect((0, 0), (width, self.image.get_height())))
        self.image.blit(render_textrect(str(self.info), 50, self.rect, (255, 255, 255)), (3, 0))
        self.text = '{0}/{1}'.format(self.current, self.max)
        if self.hovering:
            self.image.blit(render_textrect(self.text, 50, self.rect, (255, 255, 255), None, 1, ), (0, 0))


class CharStats(Gui):
    def __init__(self, world):
        self.width = 180
        self.height = 95
        self.world = world
        Gui.__init__(self, 'character', (0, 200), pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32), True)
        self.image.convert_alpha()
        self.player_image = world.player.image.copy()
        self.time_passed = 0.0
        self.player_image = pygame.transform.scale(self.player_image, (self.player_image.get_width() / 2,
                                                                       self.player_image.get_height() / 2))
        self.name = render_textrect(world.player.name, 20, self.image.get_rect(), (255, 255, 255))
        self.time_passed_text = render_textrect(self.time_passed, 20, pygame.Rect(0, 0, 100, 100), (255, 255, 255),
                                                (54, 54, 54))
        self.generate_bars()
        register_handler(TIME_PASSED, self.handle_event)
        
    def generate_bars(self):

        self.exp = Bar(self.world.player.exp, self.world.player.stats['EXP'], 'Lvl {0}'.format(self.world.player.lvl), (50, 255, 10),
                       (5, 20))
        self.hp = Bar(self.world.player.hp, self.world.player.stats['HP'], 'HP', (224, 52, 52), (5, 45))
        self.mp = Bar(self.world.player.mp, self.world.player.stats['MP'], 'MP', (96, 132, 224), (5, 70))
        


    def handle_event(self, event):
        etype = get_event_type(event)
        if etype == TIME_PASSED:
            self.time_passed += event.amount
            self.time_passed_text = render_textrect(self.time_passed, 20, pygame.Rect(0, 0, 100, 100), (255, 255, 255),
                                                    (54, 54, 54))
            if self.exp.current != self.world.player.exp:
                self.exp.refresh(self.world.player.exp)
            if self.hp.current != self.world.player.hp:
                self.hp.refresh(self.world.player.hp)
            if self.mp.current != self.world.player.mp:
                self.mp.refresh(self.world.player.mp)

    def mouse(self, mouse, event):
        mouse.x -= self.x
        mouse.y -= self.y
        self.exp.hovering = ALWAYS_SHOW_STATS
        self.hp.hovering = ALWAYS_SHOW_STATS
        self.mp.hovering = ALWAYS_SHOW_STATS
        if mouse.colliderect(self.exp.rect):
            self.exp.hovering = True
        elif mouse.colliderect(self.hp.rect):
            self.hp.hovering = True
        elif mouse.colliderect(self.mp.rect):
            self.mp.hovering = True
        self.exp.refresh()
        self.hp.refresh()
        self.mp.refresh()


    def draw(self, surface):
        self.image.blit(self.player_image, (5, 0))
        self.image.blit(self.time_passed_text, (120, 0))
        self.image.blit(self.name, (40, 0))
        self.image.blit(self.exp.image, (self.exp.rect.x, self.exp.rect.y))
        self.image.blit(self.hp.image, (self.hp.rect.x, self.hp.rect.y))
        self.image.blit(self.mp.image, (self.mp.rect.x, self.mp.rect.y))
        surface.blit(self.image, (self.x, self.y))