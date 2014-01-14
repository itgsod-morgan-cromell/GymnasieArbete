import sys
from src.gui.gui import Gui
import pygame
from src.gui.textrect import render_textrect


class MenuItem(object):
    def __init__(self, rect, data):
        self.rect = rect
        self.active = False
        self.data = data
        self.image = render_textrect(str(self.data), 30, self.rect, (128, 128, 128), None, 1)
        self.active_image = render_textrect(str(self.data), 30, self.rect, (255, 255, 255), None, 1)


class Menu(Gui):
    def __init__(self, middle, options):
        self.options = options
        self.middle = middle
        self.width = 15 * len(max(options, key=len))
        self.height = 30*len(options)
        self.main = True
        self.main_bg = pygame.image.load('res/gui/main_menu_bg.png')
        self.main_bg = pygame.transform.scale(self.main_bg, (self.middle[0]*2, self.middle[1]*2))
        image = pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32)
        image.convert_alpha()
        self.rect = pygame.Rect((middle[0] - self.width/2, self.middle[1] - self.height/2), (self.width, self.height))
        self.items = []
        self.logo_rect = pygame.Rect((0, 0), (250, 50))
        self.title = render_textrect(' ', 30, self.logo_rect, (255, 255, 0), None, 1)
        self.title_text = ' '
        self.logo = render_textrect('Dungeon of Doom (Alpha)', 30, self.logo_rect, (255, 255, 0), None, 1)
        Gui.__init__(self, 'menu', (self.rect.x, self.rect.y), image, True)
        self.choices_to_send = {}
        for key, option in enumerate(self.options):
            rect = pygame.Rect((0, 0 + (30 * key)), (self.width, 30))
            self.items.append(MenuItem(rect, option))

    def change_title(self, string):
        self.title = render_textrect(string, 30, self.logo_rect, (255, 255, 0), None, 1)
        self.title_text = string

    def change_options(self, options):
        self.options = options
        self.items = []
        for key, option in enumerate(self.options):
            rect = pygame.Rect((0, 0 + (30 * key)), (self.width, 30))
            self.items.append(MenuItem(rect, option))

    def update(self, game):
        for item in self.items:
            if item.rect.collidepoint(pygame.mouse.get_pos()[0] - self.x, pygame.mouse.get_pos()[1] - self.y) and item.data in self.options:
                item.active = True
                for event in game.events:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if pygame.mouse.get_pressed()[0]:
                            if item.data == 'New Game':
                                self.prev_title = self.title
                                self.prev_options = self.options
                                self.change_title('Select gender')
                                self.change_options(['Male', 'Female', 'Back'])
                            elif item.data == 'Quit':
                                pygame.quit()
                                sys.exit()

                            elif item.data is 'Back':
                                self.title = self.prev_title
                                self.change_options(self.prev_options)
                            elif item.data is 'back to menu':
                                game.__init__()
                            elif self.title_text == 'Select gender':
                                self.choices_to_send['gender'] = item.data
                                self.prev_title = self.title
                                self.prev_options = self.options
                                self.change_title('Select class')
                                self.change_options(['Warrior', 'Mage', 'Ranger'])
                            elif self.title_text == 'Select class':
                                self.choices_to_send['class'] = item.data
                                game.new_game(self.choices_to_send)
                                self.choices_to_send = {}
                                self.change_options(['back to menu', 'Save game', 'Quit'])
                                self.active = False
                                self.main = False

                            #self.active = False
                            #self.main = False
            else:
                item.active = False

    def draw(self, screen):
        self.image.fill((0, 0, 0))
        if self.main:
            self.image.blit(self.main_bg, (-self.x, -self.y))
            screen.blit(self.main_bg, (0, 0))
            screen.blit(self.logo, (10 + self.middle[0] - self.logo_rect.w/2, 100))
            if self.title:
                screen.blit(self.title, (self.middle[0] - self.logo_rect.w/2, 200))
        for item in self.items:
            if item.active:
                self.image.blit(item.active_image, (item.rect.x, item.rect.y))
            else:
                self.image.blit(item.image, (item.rect.x, item.rect.y))
        screen.blit(self.image, (self.x, self.y))