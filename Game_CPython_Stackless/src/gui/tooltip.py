import pygame
from src.gui.gui import Gui
from src.gui.textrect import render_textrect
from src.event_helper import *
import copy


class Mouse_select(object):
    def __init__(self, world):
        self.world = world
        self.rect = pygame.Rect((0, 0), (2, 2)).copy()
        self.color = (255, 0, 0)
        self.in_map = True
        self.image = pygame.Surface((32, 32), pygame.SRCALPHA, 32)
        self.image.convert_alpha()
        self.offset = pygame.Rect(0, 0, 0, 0)
        register_handler([pygame.MOUSEMOTION, TIME_PASSED, GUI_TOOLTIP_COLOR, ENTITY_ATTACK], self.handle_event)

    def handle_event(self, event):
        etype = event.type if event.type != pygame.USEREVENT else event.event_type
        if etype == pygame.MOUSEMOTION:
            if 0 < self.rect.x > self.offset.w or 0 < self.rect.y > self.offset.h:
                self.in_map = False

                post_event(SIDEBARMOTION, pos=event.pos, rel=event.rel, buttons=event.buttons)
            else:
                self.in_map = True
                old_grid_x = int(self.rect.x / 32)
                old_grid_y = int(self.rect.y / 32)
                new_grid_x = int(event.pos[0] / 32)
                new_grid_y = int(event.pos[1] / 32)
                if (old_grid_x, old_grid_y) != (new_grid_x, new_grid_y):
                    post_event(GUI_TOOLTIP_CLEAR)
                    self.interact(new_grid_x, new_grid_y)
            self.rect.x = copy.copy(event.pos[0])
            self.rect.y = copy.copy(event.pos[1])
        elif etype == TIME_PASSED or etype == ENTITY_ATTACK:
            if 0 < self.rect.x > self.offset.w or 0 < self.rect.y > self.offset.h:
                self.in_map = False
            else:
                self.in_map = True
                grid_x = int(self.rect.x / 32)
                grid_y = int(self.rect.y / 32)
                self.interact(grid_x, grid_y)
        elif etype == GUI_TOOLTIP_COLOR:
            self.color = event.color

    def interact(self, x, y):
        x += int(self.offset.x / 32)
        y += int(self.offset.y / 32)
        if 0 < x > self.world.map.grid_size_x - 1 or 0 < y > self.world.map.grid_size_y - 1:
            return
        items = self.world.map.get_item(x, y)
        m = None
        for monster in self.world.map.monsters:
            if monster.x == x and monster.y == y:
                m = monster
        if m:
            self.color = (255, 255, 0)
            post_event(PLAYER_ITEM_PROXIMITY, true=GUI_TOOLTIP_POST, target=m, range=self.world.player.stats['RANGE'],
                       args={'l_mouse': ('attack', PLAYER_ATTACK_ENTITY), 'target': m})
            post_event(GUI_TOOLTIP_POST, r_mouse=('examine', PLAYER_EXAMINE_ENTITY), target=m)
        elif items:
            for item in items:
                if self.world.map.map.tiles[y][x].explored == 0:
                    self.color = (255, 0, 0)
                else:
                    self.color = (0, 0, 255)
                    item.interact()

        else:
            tile = self.world.map.map.tiles[y][x]
            id = tile.id if hasattr(tile, 'id') else tile
            if id:
                post_event(PLAYER_FIND_PATH, pos=(x, y), post_to_gui=True)
            else:
                self.color = (255, 0, 0)



    def update(self, offset, world):
        self.offset = offset
        self.world = world


    def draw(self, screen):
        if self.in_map:
            self.image.fill(0)
            pygame.draw.lines(self.image, self.color, False, [(8, 0), (0, 0), (0, 8)], 2) #top left
            pygame.draw.lines(self.image, self.color, False, [(24, 0), (30, 0), (30, 8)], 2) #top right
            pygame.draw.lines(self.image, self.color, False, [(24, 30), (30, 30), (30, 24)], 2) #bottom right
            pygame.draw.lines(self.image, self.color, False, [(0, 24), (0, 30), (8, 30)], 2) #bottom left
            if self.color == (255, 0, 0):
                pygame.draw.line(self.image, self.color, (15, 3), (15, 29), 2)
                pygame.draw.line(self.image, self.color, (3, 15), (29, 15), 2)
            x = int(self.rect.x / 32) * 32
            y = int(self.rect.y / 32) * 32
            screen.blit(self.image, (x, y))


class Tooltip(Gui):
    def __init__(self, world):
        self.world = world
        self.data = None
        self.orientation = None
        image = pygame.Surface((200, 300), pygame.SRCALPHA, 32)
       # image.convert_alpha()
        self.cursors = {'travel': pygame.image.load('../res/other/cursors/travel.png'),
                        'standard': pygame.image.load('../res/other/cursors/default.gif'),
                        'open': pygame.image.load('../res/other/cursors/examine.png')}
        self.options = {}
        self.show_window = False
        self.tooltip_delay = 0
        self.item_tooltip = None
        self.mouse = Mouse_select(world)
        Gui.__init__(self, 'character', (0, 0), image, True)
        register_handler(
            [GUI_TOOLTIP_CLEAR, TIME_PASSED, GUI_TOOLTIP_POST, GUI_EXAMINE_ITEM, GUI_EXAMINE_ITEM_CLEAR, pygame.MOUSEBUTTONDOWN],
            self.handle_event)


    def update_data(self):
        self.show_window = False
        i = 0
        self.image.fill(0)
        string_len = 0
        for key, event in self.options.items():
            string = "[{0}] : {1}".format(key, event[0])
            if len(string) > string_len:
                string_len = len(string)
        for key, event in self.options.items():
            string = "[{0}] : {1}".format(key, event[0])
            rect = pygame.Rect((0, 20 * i), (string_len * 10, 20))
            i += 1
            self.image.blit(render_textrect(string, 20, rect, (255, 255, 255), (24, 72, 240)), (rect.x, rect.y))

    def update(self, world, offset):
        self.world = world
        self.mouse.update(offset, world)


        if (self.x, self.y) != (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1] - self.image.get_bounding_rect().h) or not self.options:
            self.x = pygame.mouse.get_pos()[0]
            self.y = pygame.mouse.get_pos()[1] - self.image.get_bounding_rect().h
            self.show_window = False
            self.tooltip_delay = 0
        else:
            self.tooltip_delay += 1
            if self.tooltip_delay >= 40:
                self.show_window = True




    def handle_event(self, event):
        etype = get_event_type(event)
        if etype == pygame.MOUSEBUTTONDOWN and self.options:

            if pygame.mouse.get_pressed()[0]:  # Left click.
                if 'L-MOUSE' in self.options:
                    post_event(self.options['L-MOUSE'][1], target=self.options['L-MOUSE'][2])
            elif pygame.mouse.get_pressed()[1]:  # Middle click.
                if 'MM-MOUSE' in self.options:
                    post_event(self.options['MM-MOUSE'][1], target=self.options['MM-MOUSE'][2])
            elif pygame.mouse.get_pressed()[2]:  # Right click.
                if 'R-MOUSE' in self.options:
                    post_event(self.options['R-MOUSE'][1], target=self.options['R-MOUSE'][2])

        elif etype == GUI_TOOLTIP_POST:
            #self.options = {}
            if hasattr(event, 'orientation'):
                self.orientation = event.orientation
            if hasattr(event, 'l_mouse'):
                if event.l_mouse:
                    self.options['L-MOUSE'] = event.l_mouse + (event.target,)
            if hasattr(event, 'mm_mouse'):
                if event.mm_mouse:
                    self.options['MM-MOUSE'] = event.mm_mouse + (event.target,)
            if hasattr(event, 'r_mouse'):
                if event.r_mouse:
                    self.options['R-MOUSE'] = event.r_mouse + (event.target,)


            self.update_data()
        elif etype == GUI_TOOLTIP_CLEAR or etype == TIME_PASSED:
            self.options = {}


        elif etype == GUI_EXAMINE_ITEM:
            self.item_tooltip = event.tooltip

        elif etype == GUI_EXAMINE_ITEM_CLEAR:
            self.item_tooltip = None


    def draw(self, screen):
        self.mouse.draw(screen)
        if self.show_window:
            if self.orientation:
                if self.orientation == 'left':
                    screen.blit(self.image, (self.x - self.image.get_width() + 20, self.y + 20))
            else:
                screen.blit(self.image, (self.x + 20, self.y + 20))
        if self.item_tooltip:
            screen.blit(self.item_tooltip,
                        (self.x - self.item_tooltip.get_width(), self.y - self.item_tooltip.get_height()))
