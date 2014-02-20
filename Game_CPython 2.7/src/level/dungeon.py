from src.level.dungeon_generator.map_generator import Dungeon
from src.level.dungeon_generator.map_loader import Map
import copy
from src.items.chest import Chest
import random
from src.event_helper import *
from src.entities.enemy import *

class DungeonLevel(object):
    def __init__(self, floor, up=None, down=None):
        self.monsters = []
        self.items = []
        self.up = up
        self.floor = floor
        self.down = down
        self.dungeon = Dungeon((random.randint(33, 50), random.randint(33, 50)), "None", 100, (5, 5), (32, 32), (32, 32))
        self.dungeon.generate_dungeon()
        self.explored_tiles = copy.deepcopy(self.dungeon.grid)
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
                    self.explored_tiles[y][x] = -1

    def setup(self):
       # Prepare first level
        if not self.up:
            self.dungeon.grid[self.up_stair[1]][self.up_stair[0]] = 1
            self.spawn = self.up_stair
            self.map.load_dungeon(self.dungeon)

    def fog_of_war(self, x0, y0, radius):

        for y in range(len(self.explored_tiles)):
            for x in range(len(self.explored_tiles[y])):
                if self.explored_tiles[y][x] == 1:
                    self.explored_tiles[y][x] = 0

        end_points = []
        lines = []
        f = 1 - radius
        ddf_x = 1
        ddf_y = -2 * radius
        x = 0
        y = radius

        end_points.append((x0, y0 + radius))
        end_points.append((x0, y0 - radius))
        end_points.append((x0 + radius, y0))
        end_points.append((x0 - radius, y0))
        end_points.append((x0 - 7, y0 + 3))
        end_points.append((x0 + 7, y0 + 3))
        end_points.append((x0 - 7, y0 - 3))
        end_points.append((x0 + 7, y0 - 3))
        end_points.append((x0 - 3, y0 - 7))
        end_points.append((x0 + 3, y0 - 7))
        end_points.append((x0 - 7, y0 - 6))
        end_points.append((x0 - 7, y0 + 6))
        end_points.append((x0 + 7, y0 - 6))
        end_points.append((x0 + 7, y0 + 6))

        end_points.append((x0 - 6, y0 - 7))
        end_points.append((x0 + 6, y0 - 7))
        end_points.append((x0 - 6, y0 + 7))
        end_points.append((x0 + 6, y0 + 7))


        while x < y:
            if f >= 0:
                y -= 1
                ddf_y += 1
                f += ddf_y
            x += 1
            ddf_x += 1
            f += ddf_x
            end_points.append((x0 + x, y0 + y))
            end_points.append((x0 - x, y0 + y))
            end_points.append((x0 + x, y0 - y))
            end_points.append((x0 - x, y0 - y))
            end_points.append((x0 + y, y0 + x))
            end_points.append((x0 - y, y0 + x))
            end_points.append((x0 + y, y0 - x))
            end_points.append((x0 - y, y0 - x))



        for i in range(len(end_points)):
            if end_points[i][0] < 0:
                end_points[i] = (0, end_points[i][1])
            elif end_points[i][0] > len(self.explored_tiles[0]) - 1:
                end_points[i] = (len(self.explored_tiles[0]) - 1, end_points[i][1])
            if end_points[i][1] < 0:
                end_points[i] = (end_points[i][0], 0)
            elif end_points[i][1] > len(self.explored_tiles) - 1:
                end_points[i] = (end_points[i][0], len(self.explored_tiles) - 1)

            line = self.get_line(x0, y0, end_points[i][0], end_points[i][1])
            lines.append(line)

        for line in lines:
            for pos in line:
                x = pos[0]
                y = pos[1]
                if self.dungeon.grid[y][x] in [0, 2, 3, 4, 5, 6]:
                    self.explored_tiles[y][x] = 1
                    break
                else:
                    self.explored_tiles[pos[1]][pos[0]] = 1


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
                elif self.map.tiles[row][tile].id == 7:
                    self.map.tiles[row][tile].id = 1
                    self.map.tiles[row][tile].load_image()
                    self.monsters.append(Monster('test', 'warrior', (tile, row), self))



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
        issteep = abs(y2-y1) > abs(x2-x1)
        if issteep:
            x1, y1 = y1, x1
            x2, y2 = y2, x2
        rev = False
        if x1 > x2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1
            rev = True
        deltax = x2 - x1
        deltay = abs(y2-y1)
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