import random

from src.items.chest import Chest
from src.entities.player import Player
from src.level.level import Level


class World(object):
    def __init__(self, player):
        self.generate_floor()
        self.map.setup()
        self.spawn_objects()
        self.player = Player(self.map.spawn, self, player['class'], 'Test')

    def generate_floor(self):
        self.map = Level(1)

    def spawn_objects(self):
        for row in range(0, len(self.map.map.tiles)):
            for tile in range(0, len(self.map.map.tiles[row])):
                if self.map.map.tiles[row][tile].id == 10:
                    rng = random.randint(1, 1)
                    if rng == 1:
                        self.map.map.tiles[row][tile].id = 1
                        self.map.items.append(Chest((tile, row), self))
                    else:
                        self.map.map.tiles[row][tile].id = 1
                        self.map.dungeon.grid[row][tile] = 1

    def move_up(self, entity):
        if self.map.up:
            self.map = self.map.up
        else:
            self.map.up = Level(self.map.floor - 1, None, self.map)
            self.map = self.map.up
            self.spawn_objects()

    def move_down(self, entity):
        if self.map.down:
            self.map = self.map.down
        else:
            self.map.down = Level(self.map.floor + 1, self.map)
            self.map = self.map.down
            self.spawn_objects()

    def update(self, input, offset, mouse):
        self.player.update(input, offset, mouse)
        for monster in self.map.monsters:
            monster.update()

    def draw(self, screen, offset):
        self.map.map.draw(screen, offset)
        for item in self.map.items:
            item.draw(screen, offset)
        for monster in self.map.monsters:
            monster.draw(screen, offset)
        self.player.draw(screen, offset)

