
import pygame
from src.entities.classdata import ClassData
from src.entities.entity import Entity
from src.level.generator.astar import *
from src.event_helper import *


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
        self.travel_dest_event = None
        self.follow_path = False
        self.move(0, 0)
        register_handler([pygame.KEYDOWN, PLAYER_FIND_PATH, PLAYER_TRAVEL_PATH, TIME_PASSED], self.handle_event)
        register_handler([PLAYER_EXAMINE_ITEM, PLAYER_USE_ITEM, PLAYER_PICKUP_ITEM,
                          PLAYER_DROP_ITEM, PLAYER_EQUIP_ITEM, PLAYER_UNEQUIP_ITEM], self.handle_items)

    def update(self, offset):
        self.playable_area = offset
        if self.path:
            if self.follow_path:
                self.follow_path = True
                self.travel()
                return
        self.follow_path = False
        self.path_delay = 0
        self.calculate_stats()

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
            if event.post_to_gui:
                post_event(GUI_TOOLTIP_POST, target=self, l_mouse=('travel', PLAYER_TRAVEL_PATH))
        elif etype == PLAYER_TRAVEL_PATH and not self.follow_path:
            self.travel()
        if xa != 0 or ya != 0:
            self.move(xa, ya)

    def handle_items(self, event):
        etype = get_event_type(event)
        item = event.target
        if etype == PLAYER_USE_ITEM:
            item.use()
        elif etype == PLAYER_EQUIP_ITEM:
            item.equipped = True
        elif etype == PLAYER_UNEQUIP_ITEM:
            item.equipped = False
        elif etype == PLAYER_DROP_ITEM:
            self.inventory.remove(item)
        elif etype == PLAYER_PICKUP_ITEM:
            self.inventory.append(item)
        post_event(TIME_PASSED, amount=1.0)



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
        tile = self.world.map.map.tiles[self.y + ya][self.x + xa]
        items = self.world.map.get_item(self.x + xa, self.y + ya)
        if items:
            for item in items:
                if item:
                    if item.type == 'chest':
                        xa = 0
                        ya = 0
                    elif item.type == 'item':
                        post_event(GUI_EXPLORER_ITEMS, items=items)
        else:
            post_event(GUI_EXPLORER_CLEAR)

        if tile.id == 2 or tile.id == 3 or tile.id == 4 or tile.id == 5 or tile.id == 6 or tile.id == 7:
            xa = 0
            ya = 0
        if tile.id == 8 and self.KEYBOARD:
            post_event(WORLD_MOVE_UP)
            self.path = None

        elif tile.id == 9 and self.KEYBOARD:
            post_event(WORLD_MOVE_DOWN)
            self.path = None

        else:
            self.x += xa
            self.y += ya
            post_event(TIME_PASSED, amount=1.0)
            self.world.map.fog_of_war(self.x, self.y, self.radius)

    def calculate_stats(self):
        if self.exp >= self.stats['EXP']:
            self.lvl += 1
            self.exp = 0

        if self.hp > self.stats['HP']:
            self.hp = self.stats['HP']
        if self.mp > self.stats['MP']:
            self.mp = self.stats['MP']

    def find_path(self, end):

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
            post_event(PLAYER_FOUND_PATH, path=path)

    def travel(self):
        if self.path:
            self.draw_path()
            self.follow_path = True
        else:
            self.path_delay = self.max_path_delay
            self.follow_path = False
            post_event(PLAYER_REACHED_DESTINATION, dest=(self.x, self.y))
        if self.path_delay == 0:
            self.path_delay = self.max_path_delay
            x = self.path[0][0]
            y = self.path[0][1]
            if hasattr(self.world.map.map.tiles[y][x], 'id'):
                self.world.map.map.tiles[y][x].id = self.world.map.dungeon.grid[y][x]
            if self.path:
                self.path.remove(self.path[0])
            self.move(x - self.x, y - self.y)
            if not self.path:
                self.path_delay = self.max_path_delay
                self.follow_path = False
                post_event(PLAYER_REACHED_DESTINATION, dest=(self.x, self.y))

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