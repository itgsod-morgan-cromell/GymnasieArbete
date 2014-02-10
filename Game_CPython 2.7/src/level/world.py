
from src.entities.player import Player
from src.level.dungeon import DungeonLevel
from src.event_helper import *
from src.level.overworld import OverworldLevel


class World(object):
    def __init__(self, player):
        self.map = DungeonLevel(1)
        self.map.setup()
        self.map.spawn_objects()
        self.player = Player(self.map.spawn, self.map, player['class'], 'Test')
        self.output = None
        register_handler([WORLD_MOVE_DOWN, WORLD_MOVE_UP, PLAYER_DROP_ITEM], self.handle_event)
        register_handler([PLAYER_PICKUP_ITEM], self.map.handle_event)

    def handle_event(self, event):
        etype = get_event_type(event)
        if etype == WORLD_MOVE_DOWN:
            if self.map.down:
                self.map = self.map.down
            else:
                self.map.down = DungeonLevel(self.map.floor + 1, self.map)
                self.map = self.map.down
                self.spawn_objects()
                self.player.x, self.player.y = self.map.down_stair
        elif etype == WORLD_MOVE_UP:
            if self.map.up:
                self.map = self.map.up
            else:
                self.map.up = DungeonLevel(self.map.floor - 1, None, self.map)
                self.map = self.map.up
                self.spawn_objects()
                self.player.x, self.player.y = self.map.up_stair
        elif etype == PLAYER_DROP_ITEM:
            event.target.x = self.player.x
            event.target.y = self.player.y
            self.map.items.append(event.target)
            self.player.move(0, 0)


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

