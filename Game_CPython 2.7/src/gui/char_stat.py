from src.gui.textrect import *
from src.constants import *
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
        self.hovering = False
        self.image = pygame.Surface((176, 16))
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.image.fill((84, 84, 84))
        width = int((self.current/self.max)*self.image.get_width())
        self.image.fill(color, rect=pygame.Rect((0, 0), (width, self.image.get_height())))
        self.image.blit(render_textrect(str(info), 50, self.rect, (255, 255, 255)), (3, 0))
    def refresh(self):
        self.image.fill((84, 84, 84))
        width = int((self.current/self.max)*self.image.get_width())
        self.image.fill(self.color, rect=pygame.Rect((0, 0), (width, self.image.get_height())))
        self.image.blit(render_textrect(str(self.info), 50, self.rect, (255, 255, 255)), (3, 0))
        self.text = '{0}/{1}'.format(self.current, self.max)
        if self.hovering:
            self.image.blit(render_textrect(self.text, 50, self.rect, (255, 255, 255), None, 1,), (0, 0))


class CharStats(Gui):
    def __init__(self, world):
        self.width = 180
        self.height = 95
        Gui.__init__(self, 'character', (0, 200), pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32), True)
        self.image.convert_alpha()
        self.player_image = world.player.images[0].copy()
        self.player_image = pygame.transform.scale(self.player_image, (self.player_image.get_width()/2,
                                                                       self.player_image.get_height()/2))
        self.name = render_textrect(world.player.name, 30, self.image.get_rect(), (255, 255, 255))
        self.exp = Bar(world.player.exp, world.player.stats['EXP'], 'Lvl {0}'.format(world.player.lvl), (50, 255, 10), (5, 20))
        self.hp = Bar(world.player.hp, world.player.stats['HP'], 'HP', (224, 52, 52), (5, 45))
        self.mp = Bar(world.player.mp, world.player.stats['MP'], 'MP', (96, 132, 224), (5, 70))
        register_handler(SIDEBARMOTION, self.handle_event)


    def handle_event(self, event):
        etype = get_event_type(event)
        if etype == SIDEBARMOTION:
            mouse_rect = pygame.Rect(event.pos, (2, 2)).copy()
            mouse_rect.x -= (WIDTH-MENU_WIDTH) + self.x
            mouse_rect.y -= self.y
            self.exp.hovering = False
            self.hp.hovering = False
            self.mp.hovering = False
            if mouse_rect.colliderect(self.exp.rect):
                self.exp.hovering = True
            elif mouse_rect.colliderect(self.hp.rect):
                self.hp.hovering = True
            elif mouse_rect.colliderect(self.mp.rect):
                self.mp.hovering = True
            self.exp.refresh()
            self.hp.refresh()
            self.mp.refresh()




    def draw(self, surface):
        self.image.blit(self.player_image, (5, 0))
        self.image.blit(self.name, (40, 0))
        self.image.blit(self.exp.image, (self.exp.rect.x, self.exp.rect.y))
        self.image.blit(self.hp.image, (self.hp.rect.x, self.hp.rect.y))
        self.image.blit(self.mp.image, (self.mp.rect.x, self.mp.rect.y))
        surface.blit(self.image, (self.x, self.y))