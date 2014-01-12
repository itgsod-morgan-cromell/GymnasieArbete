from src.entities.chest import Chest
from src.entities.player import Player
from src.level.level import Level

import random


class World(object):
    def __init__(self):
        self.generate_floor()
        self.map.setup()
        self.spawn_entities()
        self.player = Player(self.map.spawn, self)
        self.map.entities.append(self.player)

    def generate_floor(self):
        self.map = Level(1)

    def spawn_entities(self):
        for row in range(0, len(self.map.map.tiles)):
            for tile in range(0, len(self.map.map.tiles[row])):
                if self.map.map.tiles[row][tile].id == 10:
                    rng = random.randint(1, 1)
                    if rng == 1:
                        self.map.map.tiles[row][tile] = Chest(self.map.map.tiles[row][tile], self, self.map.floor)
                    else:
                        self.map.map.tiles[row][tile].id = 1
                        self.map.dungeon.grid[row][tile] = 1

    def move_up(self, entity):
        self.map.entities.remove(entity)
        if self.map.up:
            self.map = self.map.up
        else:
            self.map.up = Level(self.map.floor - 1, None, self.map)
            self.map = self.map.up
            self.spawn_entities()
        self.map.entities.append(entity)

    def move_down(self, entity):
        self.map.entities.remove(entity)
        if self.map.down:
            self.map = self.map.down
        else:
            self.map.down = Level(self.map.floor + 1, self.map)
            self.map = self.map.down
            self.spawn_entities()
        self.map.entities.append(entity)

    def update(self, input, offset, mouse):
        for entity in self.map.entities:
            if hasattr(entity, 'update'):
                entity.update(input, offset, mouse)

    def draw(self, screen, offset):
        self.map.map.draw(screen, offset)
        for entity in self.map.entities:
            entity.draw(screen, offset)
        self.player.draw(screen, offset)
