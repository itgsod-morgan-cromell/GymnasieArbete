from src.items.chest import Chest
from src.entities.player import Player
from src.level.level import Level
from src.event_helper import *


class World(object):
    def __init__(self, player):
        self.map = Level(1)
        self.map.setup()
        self.spawn_objects()
        self.player = Player(self.map.spawn, self, player['class'], 'Test')
        self.output = None
        register_handler([WORLD_MOVE_DOWN, WORLD_MOVE_UP], self.handle_event)
        register_handler([PLAYER_DROP_ITEM, PLAYER_PICKUP_ITEM], self.map.handle_event)

    def handle_event(self, event):
        etype = get_event_type(event)
        if etype == WORLD_MOVE_DOWN:
            if self.map.down:
                self.map = self.map.down
            else:
                self.map.down = Level(self.map.floor + 1, self.map)
                self.map = self.map.down
                self.spawn_objects()
                self.player.x, self.player.y = self.map.down_stair
        elif etype == WORLD_MOVE_UP:
            if self.map.up:
                self.map = self.map.up
            else:
                self.map.up = Level(self.map.floor - 1, None, self.map)
                self.map = self.map.up
                self.spawn_objects()
                self.player.x, self.player.y = self.map.up_stair

    def spawn_objects(self):
        for row in range(0, len(self.map.map.tiles)):
            for tile in range(0, len(self.map.map.tiles[row])):
                if self.map.map.tiles[row][tile].id == 10:
                    self.map.map.tiles[row][tile].id = 1
                    self.map.dungeon.grid[row][tile] = 1
                    self.map.items.append(Chest((tile, row), self))

    def update(self, offset):
        self.player.update(offset)
        for monster in self.map.monsters:
            monster.update()

    def draw(self, screen, offset):
        self.map.map.draw(screen, offset, self.map.explored_tiles)
        for item in self.map.items:
            explored = self.map.explored_tiles[item.y][item.x]
            item.draw(screen, offset, explored)
        for monster in self.map.monsters:
            if self.map.explored_tiles[monster.y][monster.x] >= 0:
                monster.draw(screen, offset)
        self.player.draw(screen, offset)

