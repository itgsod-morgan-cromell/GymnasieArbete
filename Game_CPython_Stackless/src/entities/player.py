import pygame
from src.entities.classdata import ClassData
from src.entities.entity import Entity
from src.level.dungeon_generator.astar import *
from src.event_helper import *
import random
import os


class Player(Entity):
    def __init__(self, pos, world, _class, name):
        self.lvl = 1
        self.classdata = ClassData(_class)
        Entity.__init__(self, name, pos, world, 'player')
        self.image = self.build_player(_class)
        self.dir = 0
        self.icon = self.image
        self.move_ticker = 0
        self.inventory = []
        self.item_slots = {'back': None, 'armor': None, 'hand1': None, 'hand2': None}
        self.max_path_delay = 1
        self.astar = Pathfinder()
        self.playable_area = None
        self.KEYBOARD = True
        self.stats = self.classdata.stats
        self.hp = self.stats['HP']
        self.mp = self.stats['MP']
        self.gold = 0
        self.exp = 0
        #Radius is measured in tiles and not in pixels.
        self.radius = 8
        self.mouse_grid_x = 0
        self.mouse_grid_y = 0
        self.path = None
        self.path_delay = 0
        self.travel_dest_event = None
        self.follow_path = False
        self.move(0, 0)
        register_handler([pygame.KEYDOWN, PLAYER_FIND_PATH, PLAYER_ITEM_PROXIMITY, PLAYER_TRAVEL_PATH,
                          PLAYER_ATTACK_ENTITY, TIME_PASSED], self.handle_event)
        register_handler([PLAYER_EXAMINE_ITEM, PLAYER_USE_ITEM, PLAYER_PICKUP_ITEM,
                          PLAYER_DROP_ITEM, PLAYER_EQUIP_ITEM, PLAYER_UNEQUIP_ITEM], self.handle_items)

    def update(self, offset):
        self.playable_area = offset
        if self.path:
            if self.follow_path:
                self.follow_path = True
                self.travel()
                for monster in self.world.monsters:
                    if monster.target:
                        self.path = None
                return
        self.follow_path = False
        self.path_delay = 0
        self.calculate_stats()
        self.stats['DMG'] = 100

    def handle_event(self, event):
        etype = get_event_type(event)
        xa = 0
        ya = 0
        if etype == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                xa = -1
            elif event.key == pygame.K_RIGHT:
                xa = 1
            elif event.key == pygame.K_UP:
                ya = -1
            elif event.key == pygame.K_DOWN:
                ya = 1
        elif etype == PLAYER_FIND_PATH and not self.follow_path:
            self.find_path(event.pos)
            if event.post_to_gui and self.path:
                post_event(GUI_TOOLTIP_POST, target=self, l_mouse=('travel', PLAYER_TRAVEL_PATH))
                post_event(GUI_TOOLTIP_COLOR, target=self, color=(0, 255, 0))
            elif event.post_to_gui:
                post_event(GUI_TOOLTIP_COLOR, target=self, color=(255, 0, 0))
        elif etype == PLAYER_ATTACK_ENTITY:
            post_event(ENTITY_ATTACK, attacker=self, target=event.target)
            post_event(TIME_PASSED, amount=1.0)
        elif etype == PLAYER_ITEM_PROXIMITY and not self.follow_path:
            self.find_path((event.target.x, event.target.y))
            if self.x == event.target.x and self.y == event.target.y or self.path and len(self.path) <= event.range:
                post_event(event.true, **event.args)
            elif self.path:
                post_event(GUI_TOOLTIP_POST, target=self, l_mouse=('travel', PLAYER_TRAVEL_PATH))



        elif etype == PLAYER_TRAVEL_PATH and not self.follow_path:
            self.travel()
        if xa != 0 or ya != 0:
            self.move(xa, ya)


    def next_to(self, target):
        for ya in range(-1, 2):
                for xa in range(-1, 2):
                    if target.x+xa == self.x and target.y+ya == self.y:
                        return True
        return False

    def handle_items(self, event):
        etype = get_event_type(event)
        item = event.target

        if etype == PLAYER_EXAMINE_ITEM:
            if hasattr(item, 'description'):
                post_event(POST_TO_CONSOLE, msg=item.description)
            return

        if item in self.inventory:
            can_interact = True
        else:
            can_interact = self.next_to(item)
        if can_interact:
            if etype == PLAYER_USE_ITEM:
                item.use()
            elif etype == PLAYER_EQUIP_ITEM:
                item.equip(self)
            elif etype == PLAYER_UNEQUIP_ITEM:
                item.unequip(self)
            elif etype == PLAYER_DROP_ITEM:
                if item in self.inventory:
                    if self.item_slots[item.slot] == item:
                        item.unequip(self)
                    self.inventory.remove(item)
                    item.picked_up = False
            elif etype == PLAYER_PICKUP_ITEM:
                if item.x == self.x and item.y == self.y:
                    self.inventory.append(item)
                    item.picked_up = True
            post_event(TIME_PASSED, amount=1.0)

    def build_player(self, base):
        image = self.get_random_image('../res/entities/player/base')
        image.blit(self.get_random_image('../res/entities/player/beard'), (0, 0))
        return image

    def move(self, xa, ya):

        if xa > 0:
            self.dir = 0
            xa = 1
        elif xa < 0:
            self.dir = 2
            xa = -1
        elif ya > 0:
            self.dir = 1
            ya = 1
        elif ya < 0:
            self.dir = 3
            ya = -1
            # Check collision from the grid.
        tile = self.world.map.tiles[self.y + ya][self.x + xa]
        items = self.world.get_item(self.x + xa, self.y + ya)
        if items:
            for item in items:
                if item:
                    if item.type == 'chest':
                        xa = 0
                        ya = 0
                    elif item.type == 'item':
                        post_event(GUI_EXPLORER_ITEMS, items=items)
        for monster in self.world.monsters:
            if monster.x == self.x + xa and monster.y == self.y + ya:
                post_event(ENTITY_ATTACK, attacker=self, target=monster)
                xa = 0
                ya = 0
        else:
            post_event(GUI_EXPLORER_CLEAR)
        id = tile.id if hasattr(tile, 'id') else tile
        if id == 2 or id == 3 or id == 4 or id == 5 or id == 6 or id == 7:
            xa = 0
            ya = 0
        print id
        if id == 8 and self.KEYBOARD:
            post_event(WORLD_MOVE_UP)
            self.path = None

        elif id == 9 and self.KEYBOARD:
            post_event(WORLD_MOVE_DOWN)
            self.path = None

        else:
            self.world.dungeon.grid[self.y][self.x] = 1
            self.x += xa
            self.y += ya
            post_event(TIME_PASSED, amount=1.0)
            self.world.fog_of_war(self.x, self.y, self.radius)

    def calculate_stats(self):
        if self.exp >= self.stats['EXP']:
            self.lvl += 1
            self.exp = 0
        self.classdata.calculate_stats(self)
        self.stats = self.classdata.stats

        if self.hp > self.stats['HP']:
            self.hp = self.stats['HP']
        if self.mp > self.stats['MP']:
            self.mp = self.stats['MP']

    def find_path(self, end):
        if self.world.map.tiles[end[1]][end[0]].explored == 0:
            self.path = None
            return
        start = (self.x, self.y)
        blocked_tiles = [0, 2, 3, 4, 5, 6, 7]
        self.path = None
        start_dir = 0
        if self.mouse_grid_x is not self.x:
            if end[0] > self.x:
                start_dir = 2
            elif end[0] < self.x:
                start_dir = 6
            if end[1] > self.y:
                start_dir += 1
            elif end[1] < self.y:
                start_dir -= 1
        elif end > self.y:
            start_dir = 4
        elif self.mouse_grid_y < self.y:
            start_dir = 0
        path = self.astar.find_path(self.world.dungeon.grid, start, end, blocked_tiles, start_dir)
        if path:
            self.path = path
            post_event(PLAYER_FOUND_PATH, path=path)

    def travel(self):
        if self.path:
            self.draw_path()
            self.follow_path = True
        else:
            self.clear_path()
            self.path_delay = self.max_path_delay
            self.follow_path = False
            post_event(PLAYER_REACHED_DESTINATION, dest=(self.x, self.y))
        if self.path_delay == 0:
            self.path_delay = self.max_path_delay
            x = self.path[0][0]
            y = self.path[0][1]
            if hasattr(self.world.map.tiles[y][x], 'id'):
                self.world.map.tiles[y][x].id = self.world.dungeon.grid[y][x]
            if self.path:
                self.path.remove(self.path[0])
            self.move(x - self.x, y - self.y)
            if not self.path:
                self.clear_path()
                self.path_delay = self.max_path_delay
                self.follow_path = False
                post_event(PLAYER_REACHED_DESTINATION, dest=(self.x, self.y))

        else:
            self.path_delay -= 1

    def draw_path(self):

        for i in range(0, len(self.path)):
            tile = self.world.map.tiles[self.path[i][1]][self.path[i][0]]
            if hasattr(tile, 'id'):
                tile.id = self.world.dungeon.grid[self.path[i][1]][self.path[i][0]]
                tile.dirs = [2, 2]

                if len(self.path) > i + 1:
                    current_node = self.astar.nodes[self.path[i + 1][1]][self.path[i + 1][0]]
                    last = False
                else:
                    current_node = self.astar.nodes[self.path[i][1]][self.path[i][0]]
                    last = True
                dir = 0
                p = 0
                if current_node.parent:
                    p = current_node.parent
                if current_node:
                    c = current_node

                self.world.map.tiles[self.path[i][1]][self.path[i][0]].dirs[1] = 9
                if p:
                    tile.dirs[0] = p.dir
                    tile.dirs[1] = c.dir
                    if c.dir:
                        tile.dirs[1] = c.dir
                    else:
                        tile.dirs[1] = p.dir
                elif c.dir:
                    tile.dirs[0] = c.dir

                if len(self.path) == 1:
                    if not p:
                        tile.dirs[1] = 2
                    else:
                        if p.dir == 7:
                            tile.dirs[0] = 5
                            tile.dirs[1] = 5
                        elif p.dir == 5:
                            tile.dirs[0] = 7
                            tile.dirs[1] = 7
                if c == self.path[-1]:
                    tile.id = 16
                else:
                    self.world.map.tiles[self.y][self.x].feet = None
                    tile.draw_feet()

    def clear_path(self):
        for y in range(len(self.world.map.tiles)):
            for x in range(len(self.world.map.tiles[y])):
                self.world.map.tiles[y][x].feet = None

    def draw(self, screen, offset):
        x = self.x * 32 - offset.x
        y = self.y * 32 - offset.y
        if self.item_slots['back']:
            screen.blit(self.item_slots['back'].equipped_image, (x, y))
        screen.blit(self.image, (x, y))
        if self.item_slots['armor']:
                screen.blit(self.item_slots['armor'].equipped_image, (x, y))
        if self.item_slots['hand1']:
                screen.blit(self.item_slots['hand1'].equipped_image, (x, y))
        if self.item_slots['hand2']:
                screen.blit(self.item_slots['hand2'].equipped_image, (x, y))