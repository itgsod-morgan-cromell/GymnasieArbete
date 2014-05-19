import sys
from src.gui.gui import *
import pygame
from src.gui.textrect import render_textrect
from src.event_helper import *
from src.options import *
import copy
from collections import OrderedDict


class Button(object):
    def __init__(self, text, x, y, selection_color, logo=None):
        self.text = text
        self.selection_color = selection_color
        self.image = CONSOLE_FONT.render(text, 1, selection_color)
        self.logo = logo
        if self.logo:
            self.rect = (x, y, self.image.get_width() + self.logo.get_width(), self.logo.get_height())
        else:
            self.rect = (x, y, self.image.get_width(), self.image.get_height())
        self.x = x
        self.y = y
        self.selected = False

    def unselect(self):
        self.selected = False

    def draw(self, surface, x=0, y=0):
        if self.logo:
            surface.blit(self.logo, (self.x+x, self.y+y))
            surface.blit(self.image, (self.x + x + self.logo.get_width(), self.y + y + self.logo.get_height()/4))
        else:
            surface.blit(self.image, (self.x+x, self.y+y))
        if self.selected:
            pygame.draw.rect(surface, self.selection_color, self.rect, 1)


class ClassList(object):
    def __init__(self, values, x, y, category, race):
        self.category = category
        self.x = x
        self.y = y
        DATA_PARSER.read('../res/data/races.ini')
        self.compatible_classes = DATA_PARSER.get(race, 'classes')

        self.buttons = self.create_buttons(values, (0, 0, 255))
        self.image = pygame.Surface((200, len(values)*CONSOLE_FONT.get_linesize()), pygame.SRCALPHA, 32)
        self.image.convert_alpha()



    def unselect(self):
        for button in self.buttons:
            button.unselect()

    def create_buttons(self, buttons, color=(255, 255, 255)):
        for i, button in enumerate(buttons):
            x = self.x
            y = self.y
            if button in self.compatible_classes:
                color = (255, 255, 255)
            else:
                color = (128, 128, 128)
            y += CONSOLE_FONT.get_linesize()
            y += (i * CONSOLE_FONT.get_linesize())
            buttons[i] = Button(button, x, y, color)
        return buttons

    def draw(self, surface):
        for button in self.buttons:
                button.draw(surface)
        surface.blit(CONSOLE_FONT.render(self.category, 1, (0, 190, 255)), (self.x, self.y))
        surface.blit(self.image, (self.x, self.y+CONSOLE_FONT.get_linesize()))

class Menu(Gui):
    def __init__(self):
        self.width = WIDTH
        self.height = HEIGHT - CONSOLE_HEIGHT
        Gui.__init__(self, 'menu', (0, 0), pygame.Surface((self.width, self.height)), True)
        register_handler([MENU_QUIT_GAME, pygame.MOUSEBUTTONDOWN, pygame.MOUSEMOTION],
                         self.handle_event)
        self.menu = 'main menu'
        self.buttons = {}
        self.buttons['main menu'] = self.create_buttons([('Dungeon Crawl', pygame.image.load('../res/gui/menu/crawl.png'))])
        DATA_PARSER.read('../res/data/races.ini')
        self.buttons['race select'] = self.create_buttons(DATA_PARSER.sections(), True)
        DATA_PARSER._sections = {}
        self.choices = {}


    def create_class_buttons(self):
        DATA_PARSER.read('../res/data/classes.ini')
        class_types = {}
        class_types['Warrior'] = ['Fighter', 'Gladiator', 'Monk', 'Hunter', 'Assassin']
        class_types['Zealot'] = ['Berserker', 'Abyssal Knight', 'Chaos Knight', 'Death Knight', 'Healer']
        class_types['Warrior-mage'] = ['Skald', 'Transmuter', 'Warper', 'Arcane Marksman', 'Enchanter']
        class_types['Mage'] = ['Wizard', 'Conjurer', 'Summoner', 'Necromancer', 'Fire Elementalist', 'Ice Elementalist', 'Air Elementalist', 'Earth Elementalist', 'Venom Mage']
        class_types['Adventurer'] = ['Artificer', 'Wanderer']
        c = []
        i = 0
        for class_type in class_types:
            x = i * 150 + 100
            y = 100
            c.append(ClassList(class_types[class_type], x, y, class_type, self.choices['race']))
            i += 1
        return c

    def create_buttons(self, buttons, lister=False, color=(255, 255, 255)):
        for i, button in enumerate(buttons):
            x = 0
            y = 0
            height = self.height
            if lister:
                x += 100
                y += 200
                height = 9 * CONSOLE_FONT.get_linesize()

            y += (i * CONSOLE_FONT.get_linesize()) % (height)
            x += int((i * CONSOLE_FONT.get_linesize()) / height) * 100


            if type(button) == tuple:
                buttons[i] = Button(button[0], x, y, color, button[1])
            else:
                buttons[i] = Button(button, x, y, color)
        return buttons

    def handle_button_click(self, button):
        if self.menu == 'main menu':
            if button.text == 'Dungeon Crawl':
                self.menu = 'race select'
        elif self.menu == 'race select':
            self.choices['race'] = button.text
            self.menu = 'class select'
            self.buttons['class select'] = self.create_class_buttons()
            DATA_PARSER._sections = {}
        elif self.menu == 'class select':
            self.choices['class'] = button.text
            post_event(MENU_NEW_GAME, background=self.choices['class'], race=self.choices['race'], name='Morgan')

    def handle_button_hover(self, button):
        if self.menu == 'race select':
            DATA_PARSER.read('../res/data/races.ini')
            post_event(FILL_CONSOLE, msg=DATA_PARSER.get(button.text, 'description'))
        elif self.menu == 'class select':
            DATA_PARSER.read('../res/data/classes.ini')
            post_event(FILL_CONSOLE, msg=DATA_PARSER.get(button.text, 'description'))


    def handle_event(self, event):
        for button in self.buttons[self.menu]:
            button.unselect()
        etype = get_event_type(event)
        if self.active:
            if etype in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEMOTION]:
                mouse_rect = pygame.Rect(event.pos, (2, 2))
                if type(self.buttons[self.menu][0]) is Button:
                    buttons = self.buttons[self.menu]
                elif type(self.buttons[self.menu][0]) is ClassList:
                    buttons = []
                    for b in self.buttons[self.menu]:
                        buttons += b.buttons
                button = mouse_rect.collidelist(buttons)
                if button != -1:
                    if etype == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        self.handle_button_click(buttons[button])
                    else:
                        buttons[button].selected = True
                        self.handle_button_hover(buttons[button])

            elif etype == MENU_QUIT_GAME:
                pygame.event.post(pygame.event.Event(pygame.QUIT))

    def draw(self, screen):
        self.image.fill((0, 0, 0))
        for button in self.buttons[self.menu]:
            button.draw(self.image)

        screen.blit(self.image, (self.x, self.y))