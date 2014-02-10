import pygame
from src.entities.classdata import ClassData
from src.entities.entity import Entity
from src.level.dungeon_generator.astar import *
from src.event_helper import *

class Monster(Entity):
    def __init__(self, name, _class, pos, world):
        self.lvl = 1
        self.classdata = ClassData(_class)
        Entity.__init__(self, name, pos, world, 'Enemy')
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
        self.stats = self.classdata.stats
        self.hp = self.stats['HP']
        self.mp = self.stats['MP']
        self.gold = 0
        self.exp = 0
        #Radius is measured in tiles and not in pixels.
        self.radius = 9
        self.path = None
        self.path_delay = 0
        self.travel_dest_event = None
        self.follow_path = False
        self.move(0, 0)
        #register_handler([PLAYER_FIND_PATH, PLAYER_TRAVEL_PATH, TIME_PASSED], self.handle_event)

    def update(self):
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
        if xa != 0 or ya != 0:
            self.move(xa, ya)

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
        tile = self.world.map.tiles[self.y + ya][self.x + xa]
        items = self.world.get_item(self.x + xa, self.y + ya)
        if items:
            for item in items:
                if item:
                    if item.type == 'chest':
                        xa = 0
                        ya = 0
        for monster in self.world.monsters:
            if monster is not self:
                if monster.x == self.x+xa and monster.y == self.y+ya:
                    xa = 0
                    ya = 0
        id = tile.id if hasattr(tile, 'id') else tile
        if id == 2 or id == 3 or id == 4 or id == 5 or id == 6 or id == 7 or id == 10:
            xa = 0
            ya = 0
        else:
            self.world.dungeon.grid[self.y][self.x] = 1
            self.x += xa
            self.y += ya
            self.world.dungeon.grid[self.y][self.x] = 7
            post_event(TIME_PASSED, amount=1.0)
            #self.world.map.fog_of_war(self.x, self.y, self.radius)

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
        path = self.astar.find_path(self.world.dungeon.grid, start, end, blocked_tiles, 0)
        if path:
            self.path = path

    def travel(self):
        if self.path:
            self.draw_path()
            self.follow_path = True
        else:
            self.path_delay = self.max_path_delay
            self.follow_path = False
        if self.path_delay == 0:
            self.path_delay = self.max_path_delay
            x = self.path[0][0]
            y = self.path[0][1]
            if hasattr(self.world.map.tiles[y][x], 'id'):
                self.world.map.tiles[y][x].id = self.world.dungeon.grid[y][x]
            if self.path:
                self.path.remove(self.path[0])
            self.move(x - self.x, y - self.y)
            if not self.path:
                self.path_delay = self.max_path_delay
                self.follow_path = False

        else:
            self.path_delay -= 1

    def draw(self, screen, offset):
        screen.blit(self.images[self.dir], (self.x*32-offset.x, self.y*32-offset.y))