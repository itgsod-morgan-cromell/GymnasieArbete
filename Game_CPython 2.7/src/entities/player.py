
import pygame
from src.entities.classdata import ClassData
from src.entities.entity import Entity
from src.level.generator.astar import *
from src.constants import *


class Player(Entity):
    def __init__(self, pos, world, _class, name):
        self.lvl = 1
        self.classdata = ClassData(_class)
        Entity.__init__(self, name, pos, world)
        self.spritesheet = pygame.image.load('res/player/{0}.png'.format(_class))
        self.images = []
        for i in range(0, 4):
            rect = pygame.Rect((i*32, 0), (32, 32))
            self.images.append(self.spritesheet.subsurface(rect))

        self.dir = 0
        self.icon = self.spritesheet.subsurface(pygame.Rect((4*32, 0), (32, 32)))
        self.move_ticker = 0
        self.inventory = []
        self.weapon = None
        self.armor = None
        self.trinket = None
        self.max_path_delay = 4
        self.astar = Pathfinder()
        self.playable_area = None
        self.KEYBOARD = False
        self.stats = self.classdata.stats
        self.hp = self.stats['HP']
        self.mp = self.stats['MP']
        self.gold = 0
        self.exp = 0
        #Radius is measured in tiles and not in pixels.
        self.radius = 9
        self.mouse_grid_x = 0
        self.mouse_grid_y = 0
        self.path = None
        self.path_delay = 0
        self.follow_p = False
        self.move(0, 0)
        pygame.event.post(pygame.event.Event(REGISTER_EVENT_HANDLER,
                                             event_register_dict([pygame.KEYDOWN, PLAYER_FIND_PATH, PLAYER_TRAVEL_PATH], self)))

    def update(self, offset):
        self.playable_area = offset
        if self.path:
            if self.follow_p:
                self.follow_p = True
                self.travel()
                return
        self.follow_p = False
        self.path_delay = 0

        for item in self.inventory:
            if not self.weapon and item.category == 'weapon':
                self.weapon = item
                item.equip(self)
                self.inventory.remove(item)
            if not self.armor and item.category == 'armor':
                self.armor = item
                item.equip(self)
                self.inventory.remove(item)
            if not self.trinket and item.category == 'trinket':
                self.trinket = item
                item.equip(self)
                self.inventory.remove(item)

        self.calculate_stats()

    def handle_event(self, event):
        xa = 0
        ya = 0
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                xa = -1
            elif event.key == pygame.K_RIGHT:
                xa = 1
            elif event.key == pygame.K_UP:
                ya = -1
            elif event.key == pygame.K_DOWN:
                ya = 1
        elif event.type == PLAYER_FIND_PATH:
            self.calculate_path(event.pos)
        elif event.type == PLAYER_TRAVEL_PATH:
            self.calculate_path(event.pos)

        if xa != 0 or ya != 0:
            self.move(xa, ya)
            pygame.event.post(pygame.USEREVENT, {'event_type': TIME_PASSED, 'amount': 1.0})

    def move(self, xa, ya):
        if xa > 0:
            self.dir = 0
            pygame.event.post(pygame.event.Event(pygame.USEREVENT, {'event_type': POST_TO_CONSOLE, 'msg': str("{0},{1}-----------test--------test".format(self.x, self.y))}))
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
        tile = self.world.map.map.tiles[self.y + ya][self.x + xa]
        item = self.world.map.get_item(self.x + xa, self.y + ya)
        if item:

            if not self.path or not self.follow_p or item.x == self.path[-1][0] and item.y == self.path[-1][1]:
                if item.type == 'item' or item.type == 'powerup':
                    xa = 0
                    ya = 0
                elif item.type == 'chest':
                    xa = 0
                    ya = 0

        if tile.id == 2 or tile.id == 3 or tile.id == 4 or tile.id == 5 or tile.id == 6 or tile.id == 7:
            xa = 0
            ya = 0
        if tile.id == 8 and self.KEYBOARD:
            self.world.move_up(self)
            self.path = None

        elif tile.id == 9 and self.KEYBOARD:
            self.world.move_down(self)
            self.path = None

        else:
            self.x += xa
            self.y += ya
            self.world.map.fog_of_war(self.x, self.y, self.radius)

    def calculate_stats(self):
        if self.exp >= self.stats['EXP']:
            self.lvl += 1
            self.exp = 0

        if self.hp > self.stats['HP']:
            self.hp = self.stats['HP']
        if self.mp > self.stats['MP']:
            self.mp = self.stats['MP']

    def calculate_path(self, end):
        # for row in range(0, len(self.world.map.map.tiles)):
        #     for tile in range(0, len(self.world.map.map.tiles[row])):
        #         if hasattr(self.world.map.map.tiles[row][tile], 'id'):
        #             if self.world.map.map.tiles[row][tile].id in [15, 16]:
        #                 self.world.map.map.tiles[row][tile].id = self.world.map.dungeon.grid[row][tile]
        #                 self.world.map.map.tiles[row][tile].dirs = [2, 2]

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
        elif end> self.y:
            start_dir = 4
        elif self.mouse_grid_y < self.y:
            start_dir = 0

        path = self.astar.find_path(self.world.map.dungeon.grid, start, end, blocked_tiles, start_dir)
        if path:
            self.path = path
            pygame.event.post(pygame.event.Event(pygame.USEREVENT, event_type=PLAYER_FOUND_PATH))

    def travel(self, world=None):
        if self.path:
            self.draw_path()
            self.follow_p = True
        if not self.path:
            self.path_delay = 0
            return
        if len(self.path) == 0:
                self.path_delay = self.max_path_delay
                return
        if self.path_delay == 0:
            self.path_delay = self.max_path_delay
            x = self.path[0][0]
            y = self.path[0][1]
            if hasattr(self.world.map.map.tiles[y][x], 'id'):
                self.world.map.map.tiles[y][x].id = self.world.map.dungeon.grid[y][x]
            if self.path:
                self.path.remove(self.path[0])
            if not self.path:
                self.path_delay = self.max_path_delay
                self.follow_p = False
            self.move(x - self.x, y - self.y)
            if not self.path:
                self.path_delay = self.max_path_delay
                self.follow_p = False

        else:
            self.path_delay -= 1

    def draw_path(self):

        for i in range(0, len(self.path)):
            tile = self.world.map.map.tiles[self.path[i][1]][self.path[i][0]]
            if hasattr(tile, 'id'):
                tile.id = self.world.map.dungeon.grid[self.path[i][1]][self.path[i][0]]
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

                self.world.map.map.tiles[self.path[i][1]][self.path[i][0]].dirs[1] = 9
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
                    tile.id = 15
                tile.load_image()
                self.world.map.map.tiles[self.path[i][1]][self.path[i][0]] = tile

    def draw(self, screen, offset):
        screen.blit(self.images[self.dir], (self.x*32-offset.x, self.y*32-offset.y))