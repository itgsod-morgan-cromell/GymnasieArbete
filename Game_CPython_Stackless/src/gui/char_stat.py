from src.gui.textrect import *
from src.event_helper import *
from src.options import *
from src.gui.gui import Gui
import pygame


class Bar(object):
    def __init__(self, current, max, info, color, pos):
        self.info = info
        self.current = current * 1.0
        self.max = max * 1.0
        self.color = color
        self.info = info
        self.hovering = ALWAYS_SHOW_STATS
        self.image = pygame.Surface((MENU_WIDTH - 10, 16))
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.image.fill((84, 84, 84))
        width = int((self.current / self.max) * self.image.get_width())
        self.image.fill(color, rect=pygame.Rect((0, 0), (width, self.image.get_height())))
        self.image.blit(render_textrect(str(info), 50, self.rect, (255, 255, 255)), (3, 0))
        self.text = '{0}/{1}'.format(int(self.current), int(self.max))
        if self.hovering:
            self.image.blit(render_textrect(self.text, 50, self.rect, (255, 255, 255), None, 1, ), (0, 0))

    def refresh(self, new_value=None):
        if new_value:
            self.current = new_value
        self.image.fill((84, 84, 84))
        width = int((self.current/self.max) * self.image.get_width())
        self.image.fill(self.color, rect=pygame.Rect((0, 0), (width, self.image.get_height())))
        self.image.blit(render_textrect(str(self.info), 50, self.rect, (255, 255, 255)), (3, 0))
        self.text = '{0}/{1}'.format(int(self.current), int(self.max))
        if self.hovering:
            self.image.blit(render_textrect(self.text, 50, self.rect, (255, 255, 255), None, 1, ), (0, 0))

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))


class CharStats(Gui):
    def __init__(self, world):
        self.width = MENU_WIDTH
        self.height = 95
        self.world = world
        Gui.__init__(self, 'character', (0, 200), pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32), True)
        self.image.convert_alpha()
        self.generate_bars()

        register_handler([TIME_PASSED, pygame.MOUSEMOTION], self.handle_event)
        
    def generate_bars(self):
        self.player_image = self.world.player.image.copy()
        self.time_passed = 0.0
        self.player_image = pygame.transform.scale(self.player_image, (self.player_image.get_width() / 2,
                                                                       self.player_image.get_height() / 2))
        self.name = render_textrect(self.world.player.name, 20, self.image.get_rect(), (255, 255, 255), INTERFACE_COLOR)
        self.time_passed_text = render_textrect(self.time_passed, 20, pygame.Rect(0, 0, MENU_WIDTH - 100, 100), (255, 255, 255),
                                                INTERFACE_COLOR)
        self.exp = Bar(self.world.player.exp, self.world.player.stats['EXP'], 'Lvl {0}'.format(self.world.player.lvl), (50, 255, 10),
                       (5, 20))
        self.hp = Bar(self.world.player.hp, self.world.player.stats['HP'], 'HP', (224, 52, 52), (5, 45))
        self.mp = Bar(self.world.player.mp, self.world.player.stats['MP'], 'MP', (96, 132, 224), (5, 70))

    def update(self):
        if self.exp.current != self.world.player.exp:
            self.exp.refresh(self.world.player.exp)
        if self.hp.current != self.world.player.hp:
            self.hp.refresh(self.world.player.hp)
        if self.mp.current != self.world.player.mp:
            self.mp.refresh(self.world.player.mp)

    def handle_event(self, event):
        etype = get_event_type(event)
        if etype == pygame.MOUSEMOTION:
            mouse = pygame.Rect(event.pos, (1, 1)).copy()
            mouse.x -= WIDTH - MENU_WIDTH
            if mouse.colliderect(self.rect):
                mouse.x -= self.x
                mouse.y -= self.y

                if mouse.colliderect(self.exp.rect):
                    self.exp.hovering = True
                    self.exp.refresh()
                elif mouse.colliderect(self.hp.rect):
                    self.hp.hovering = True
                    self.hp.refresh()
                elif mouse.colliderect(self.mp.rect):
                    self.mp.hovering = True
                    self.mp.refresh()
                else:
                    if self.exp.hovering:
                        self.exp.hovering = ALWAYS_SHOW_STATS
                        self.exp.refresh()
                    elif self.hp.hovering:
                        self.hp.hovering = ALWAYS_SHOW_STATS
                        self.hp.refresh()
                    elif self.mp.hovering:
                        self.mp.hovering = ALWAYS_SHOW_STATS
                        self.mp.refresh()
        elif etype == TIME_PASSED:
            self.time_passed += event.amount
            self.time_passed_text = render_textrect(self.time_passed, 20, pygame.Rect(0, 0, 100, 100), (255, 255, 255),
                                                    INTERFACE_COLOR)

    def draw(self, surface):
        self.image.blit(self.player_image, (5, 0))
        self.image.blit(self.name, (40, 0))
        self.image.blit(self.time_passed_text, (MENU_WIDTH - 100, 0))
        self.hp.draw(self.image)
        self.exp.draw(self.image)
        self.mp.draw(self.image)
        surface.blit(self.image, (self.x, self.y))



