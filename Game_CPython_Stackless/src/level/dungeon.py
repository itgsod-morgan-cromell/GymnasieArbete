from src.level.dungeon_generator.map_generator import Dungeon
from src.level.dungeon_generator.map_loader import Map
import copy
from src.items.chest import Chest
import random
from src.event_helper import *
from src.entities.enemy import *
from src.level.dungeon_generator.fov import *

class DungeonLevel(object):
    def __init__(self, floor, up=None, down=None):
        self.monsters = []
        self.items = []
        self.up = up
        self.player = None
        self.floor = floor
        self.down = down
        self.dungeon = Dungeon((random.randint(33, 50), random.randint(33, 50)), "None", 100, (5, 5), (32, 32),
                               (32, 32))
        self.dungeon.generate_dungeon()
        self.map = Map()
        self.width = self.dungeon.width
        self.height = self.dungeon.height
        self.grid_size_x = self.dungeon.grid_size_x
        self.grid_size_y = self.dungeon.grid_size_y
        self.map.load_dungeon(self.dungeon)
        for y in range(0, len(self.dungeon.grid)):
            for x in range(0, len(self.dungeon.grid[0])):
                if self.dungeon.grid[y][x] == 8:
                    self.up_stair = (x, y)
                elif self.dungeon.grid[y][x] == 9:
                    self.down_stair = (x, y)

    def setup(self):
    # Prepare first level
        if not self.up:
            self.dungeon.grid[self.up_stair[1]][self.up_stair[0]] = 1
            self.spawn = self.up_stair
            self.map.load_dungeon(self.dungeon)


    def fog_of_war(self, x0, y0, radius):
        for y in range(len(self.map.tiles)):
            for x in range(len(self.map.tiles[y])):
                if self.map.tiles[y][x].explored == 2:
                    self.map.tiles[y][x].explored = 1
        fov = FOVCalc()
        fov.NOT_VISIBLE_BLOCKS_VISION = True
        fov.RESTRICTIVENESS = 0
        fov.VISIBLE_ON_EQUAL = False
        cells = fov.calc_visible_cells_from(x0, y0, radius, self.is_unobstructed)
        for coords in cells:
            if len(coords) == 2:
                self.map.tiles[coords[1]][coords[0]].explored = 2

    def is_unobstructed(self, x, y):
        try:
            if self.map.tiles[y][x].id in [0, 2, 3, 4, 5, 6]:
                return False
            else:
                return True
        except IndexError:
            return False

    def handle_event(self, event):
        etype = get_event_type(event)
        if etype == PLAYER_DROP_ITEM:
            self.items.append(event.target)
        elif etype == PLAYER_PICKUP_ITEM:
            self.items.remove(event.target)

    def spawn_objects(self):
        for row in range(0, len(self.map.tiles)):
            for tile in range(0, len(self.map.tiles[row])):
                if self.map.tiles[row][tile].id == 10:
                    self.map.tiles[row][tile].id = 1
                    self.map.tiles[row][tile].load_image()
                    self.items.append(Chest((tile, row), self))
                if self.map.tiles[row][tile].id == 7:
                    self.map.tiles[row][tile].id = 1
                    self.dungeon.grid[row][tile] = 1
                   # self.monsters.append(Monster('test', 'warrior', (tile, row), self))
                if self.map.tiles[row][tile].id == 11:
                    self.map.tiles[row][tile].id = 1
                    self.dungeon.grid[row][tile] = 1
                self.map.tiles[row][tile].load_image()

    def get_item(self, x, y):
        items = []
        for item in self.items:
            if item:
                if item.x == x and item.y == y:
                    items.append(item)
        if items:
            return items

    def get_line(self, x1, y1, x2, y2):
        points = []
        issteep = abs(y2 - y1) > abs(x2 - x1)
        if issteep:
            x1, y1 = y1, x1
            x2, y2 = y2, x2
        rev = False
        if x1 > x2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1
            rev = True
        deltax = x2 - x1
        deltay = abs(y2 - y1)
        error = int(deltax / 2)
        y = y1
        ystep = None
        if y1 < y2:
            ystep = 1
        else:
            ystep = -1
        for x in range(x1, x2 + 1):
            if issteep:
                points.append((y, x))
            else:
                points.append((x, y))
            error -= deltay
            if error < 0:
                y += ystep
                error += deltax
            # Reverse the list if the coordinates were reversed
        if rev:
            points.reverse()
        return points
