from src.level.generator.map_generator import Dungeon
from src.level.generator.map_loader import Map


class Level(object):
    def __init__(self, floor, up=None, down=None):
        self.monsters = []
        self.items = []
        self.up = up
        self.floor = floor
        self.down = down
        self.dungeon = Dungeon((45, 25), "None", 50, (4, 4), (12, 12), (32, 32))

        self.dungeon.generate_dungeon()
        self.map = Map()
        self.map.load_dungeon(self.dungeon)
        for y in range(0, len(self.dungeon.grid)):
                for x in range(0, len(self.dungeon.grid[0])):
                    if self.dungeon.grid[y][x] == 8:
                        self.up_stair = (x, y)
                    if self.dungeon.grid[y][x] == 9:
                        self.down_stair = (x, y)

    def setup(self):
       # Prepare first level
        if not self.up:
            self.dungeon.grid[self.up_stair[1]][self.up_stair[0]] = 1
            self.spawn = self.up_stair
            self.map.load_dungeon(self.dungeon)

    def get_item(self, x, y):
        for item in self.items:
            if item:
                if item.x == x and item.y == y:
                    return item