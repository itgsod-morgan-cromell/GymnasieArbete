import pygame
from src.entities.classdata import ClassData
from src.entities.entity import Entity
from src.level.dungeon_generator.astar import *
from src.event_helper import *
import random
import os
from src.level.dungeon_generator.fov import *


class Monster(Entity):
    def __init__(self, name, _class, pos, world):
        self.lvl = 1
        self.classdata = ClassData(_class)
        name = random.choice(os.listdir('../res/entities/monster'))
        name_string = name.replace("_", ' ')
        Entity.__init__(self, name_string.replace(".png", ""), pos, world, 'monster')
        self.image = pygame.image.load('../res/entities/monster/{0}'.format(name))
        self.dir = 0
        self.icon = self.image
        self.move_ticker = 0
        self.inventory = []
        self.weapon = None
        self.armor = None
        self.trinket = None
        self.astar = Pathfinder()
        self.stats = self.classdata.stats
        self.hp = self.stats['HP']
        self.mp = self.stats['MP']
        self.gold = 0
        self.exp = 0
        #Radius is measured in tiles and not in pixels.
        self.radius = 5
        self.path = None
        self.travel_dest_event = None
        self.follow_path = False
        self.move(0, 0)
        self.target = None
        register_handler(TIME_PASSED, self.time_passed)

    def update(self):
        self.calculate_stats()

    def time_passed(self, event):
        self.scan_fov()
        if self.target:
            if not self.path:
                self.find_path(self.target)
            if self.path:
                if self.path[-1][0] != self.target[0] or self.path[-1][1] != self.target[1]:
                    self.find_path(self.target)
                if self.path:
                    self.travel()



    def scan_fov(self):
        self.target = None
        x = self.x
        y = self.y
        radius = self.radius
        fov = FOVCalc()
        fov.NOT_VISIBLE_BLOCKS_VISION = True
        fov.RESTRICTIVENESS = 0
        fov.VISIBLE_ON_EQUAL = False
        fov.calc_visible_cells_from(x, y, radius, self.is_unobstructed)

    def is_unobstructed(self, x, y):
        if x == self.world.player.x and y == self.world.player.y:
            self.target = (self.world.player.x, self.world.player.y)
        try:
            if self.world.map.tiles[y][x].id in [0, 2, 3, 4, 5, 6]:
                return False
            else:
                return True
        except IndexError:
            return False

    def die(self):
        self.world.monsters.remove(self)
        unregister_handler(self.time_passed)

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
                if monster.x == self.x + xa and monster.y == self.y + ya:
                    xa = 0
                    ya = 0

        if self.world.player and self.x +xa == self.world.player.x and self.y +ya == self.world.player.y:
            self.attack(self.world.player)
        id = tile.id if hasattr(tile, 'id') else tile
        if id == 2 or id == 3 or id == 4 or id == 5 or id == 6 or id == 7 or id == 10 or id == 15:
            xa = 0
            ya = 0
        else:
            self.world.dungeon.grid[self.y][self.x] = 1
            self.x += xa
            self.y += ya
            self.world.dungeon.grid[self.y][self.x] = 7

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
        blocked_tiles = [0, 2, 3, 4, 5, 6, 7, 15]
        self.path = None
        path = self.astar.find_path(self.world.dungeon.grid, start, end, blocked_tiles, 0)
        if path:
            self.path = path

    def travel(self):
        if self.path:
            self.follow_path = True
        else:
            self.follow_path = False
        x = self.path[0][0]
        y = self.path[0][1]
        if hasattr(self.world.map.tiles[y][x], 'id'):
            self.world.map.tiles[y][x].id = self.world.dungeon.grid[y][x]
        if self.path:
            self.path.remove(self.path[0])
        self.move(x - self.x, y - self.y)
        if not self.path:
            self.follow_path = False

    def attack(self, target):
        post_event(ENTITY_ATTACK, attacker=self, target=target)

    def draw(self, screen, offset):
        screen.blit(self.image, (self.x * 32 - offset.x, self.y * 32 - offset.y))