import sys
from src.gui.gui import Gui
import pygame
from src.gui.textrect import render_textrect
import copy


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
        self.current_string = []
        self.textbox = pygame.Surface((200, 30))
        pygame.draw.rect(self.textbox, (128, 128, 128), self.textbox.get_rect(), 2)
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

    def update(self, game, events):
        for item in self.items:
            if item.rect.collidepoint(pygame.mouse.get_pos()[0] - self.x, pygame.mouse.get_pos()[1] - self.y) and item.data in self.options:
                item.active = True
                for event in game.events:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if pygame.mouse.get_pressed()[0]:
                            if item.data == 'New Game':
                                self.prev_title = self.title
                                self.prev_options = self.options
                                self.change_title('Select class')
                                self.change_options(['Warrior', 'Mage', 'Ranger'])
                            elif item.data == 'Quit':
                                pygame.quit()
                                sys.exit()

                            elif item.data is 'Back':
                                self.title = self.prev_title
                                self.change_options(self.prev_options)
                            elif item.data is 'back to menu':
                                game.__init__()
                            elif self.title_text == 'Select class':
                                self.choices_to_send['class'] = item.data
                                self.change_options([' '])
                                self.change_title("Enter your character's name")

            else:
                item.active = False

        if self.title_text is "Enter your character's name":
            oldstring = copy.copy(self.current_string)
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        self.current_string = self.current_string[0:-1]
                    elif event.key == pygame.K_RETURN:
                        self.change_title(' ')
                        self.choices_to_send['name'] = ' '.join(self.current_string)
                        game.new_game(self.choices_to_send)
                        self.choices_to_send = {}
                        self.change_options(['back to menu', 'Save game', 'Quit'])
                        self.active = False
                        self.main = False
                    elif 64 < event.key < 91 or 96 < event.key < 123 or event.key == 32:
                        if len(self.current_string) < 14:
                            self.current_string.append(chr(event.key))
            #print self.current_string
            if oldstring is not self.current_string:
                rect = pygame.Rect((0, 0), (self.textbox.get_rect().w - 3, self.textbox.get_rect().h - 2))
                self.textbox.blit(render_textrect(''.join(self.current_string), 30, rect, (255, 255, 255), (0, 0, 0)), (2, 1))

                            #self.active = False
                            #self.main = False


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
        if self.title_text == "Enter your character's name":
            screen.blit(self.textbox, (self.middle[0] - self.textbox.get_rect().w/2, self.middle[1] - self.textbox.get_rect().h/2))
