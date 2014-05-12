from src.level.overworld_generator.map import *
from src.level.overworld_generator.perlin_noise import *
from src.level.overworld_generator.island_generator import *


class OverworldLevel(object):
    def __init__(self):
        self.items = []
        self.monsters = []
        self.width = 100 * 32
        self.height = 80 * 32
        self.grid_size_x = 100
        self.grid_size_y = 80
        self.map = Map('Island', IslandGenerator().generate_island(100, 80, 1, 16))
        self.map.draw_minimap()
        self.explored_tiles = []
        self.spawn = (10, 10)


    def get_item(self, x, y):
        items = []
        for item in self.items:
            if item:
                if item.x == x and item.y == y:
                    items.append(item)
        if items:
            return items
