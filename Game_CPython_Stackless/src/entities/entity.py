import pygame
from src.entities.classdata import ClassData
from src.level.dungeon_generator.astar import *
from src.event_helper import *
import random
import os

class Entity(object):
    def __init__(self, name, _class, pos, world, radius, type, image):
        self.name = name
        self.type = type
        self.image = image

        self.classdata = ClassData(type, _class)
        self.stats = self.classdata.stats
        self.skills = self.classdata.skills
        self.inventory = []
        self.item_slots = {'back': None, 'armor': None, 'hand1': None, 'hand2': None}
        self.hp = self.stats['HP']
        self.mp = self.stats['MP']
        self.exp = self.stats['EXP']
        self.lvl = 1

        self.target = None
        self.x = pos[0]
        self.y = pos[1]
        self.radius = radius
        self.astar = Pathfinder()
        self.world = world
        self.path = None
        self.follow_path = False
        self.move(0, 0)

    def update(self):
        self.calculate_stats()
        if self.hp <= 0:
            self.die()

    def time_passed(self, event):
        pass

    def die(self):
        pass

    def calculate_stats(self):
        if self.exp >= self.stats['EXP']:
            self.lvl += 1
            self.exp = 0
        self.classdata.calculate_stats(self.lvl)
        self.stats = self.classdata.stats

        if self.hp > self.stats['HP']:
            self.hp = self.stats['HP']
        if self.mp > self.stats['MP']:
            self.mp = self.stats['MP']

    def move(self, xa, ya):
        if xa > 0:
            xa = 1
        elif xa < 0:
            xa = -1
        elif ya > 0:
            ya = 1
        elif ya < 0:
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
        for entity in self.world.entities:
            if entity.x == self.x + xa and entity.y == self.y + ya and entity is not self:
                if entity.type is not self.type:
                    self.attack(entity)
                xa = 0
                ya = 0

        id = tile.id if hasattr(tile, 'id') else tile
        if id in [2, 3, 4, 5, 6, 7, 10]:
            xa = 0
            ya = 0
        if xa != 0 or ya != 0:
            self.world.dungeon.grid[self.y][self.x] = 1
            self.x += xa
            self.y += ya
            if self.type == 'monster':
                self.world.dungeon.grid[self.y][self.x] = 7
            return True
        else:
            return False

    def find_path(self, end):
        if self.world.map.tiles[end[1]][end[0]].explored == 0:
            self.path = None
            return
        start = (self.x, self.y)
        blocked_tiles = [0, 2, 3, 4, 5, 6, 7, 10]
        self.path = None
        path = self.astar.find_path(self.world.dungeon.grid, start, end, blocked_tiles)
        if path:
            self.path = path

    def travel(self):
        if not self.path:
            return False
        x = self.path[0][0]
        y = self.path[0][1]
        if self.path:
            self.path.remove(self.path[0])
        return self.move(x - self.x, y - self.y)

    def next_to(self, target, radius=1):
        for ya in range(-1*radius, 2*radius):
                for xa in range(-1*radius, 2*radius):
                    if target.x+xa == self.x and target.y+ya == self.y:
                        return True
        return False

    def attack(self, target):
        post_event(ENTITY_ATTACK, attacker=self, target=target)

    def draw(self, screen, offset):
        x = self.x * 32 - offset.x
        y = self.y * 32 - offset.y
        if self.item_slots['back']:
            screen.blit(self.item_slots['back'].equipped_image, (x, y))
        screen.blit(self.image, (x, y))
        if self.item_slots['armor']:
                screen.blit(self.item_slots['armor'].equipped_image, (x, y))
        if self.item_slots['hand1']:
                screen.blit(self.item_slots['hand1'].equipped_image, (x, y))
        if self.item_slots['hand2']:
                screen.blit(self.item_slots['hand2'].equipped_image, (x, y))

        p_hp = float(self.hp)/self.stats['HP']
        if p_hp != 1.0 and p_hp > 0:
            green = int(255 * p_hp)
            red = int(255 * (1.0 - p_hp))
            color = (red, green, 0)
            width = int(32 * p_hp)
            pygame.draw.line(screen, (0, 0, 0), (x, y+31), (x+32, y+31), 2)
            pygame.draw.line(screen, color, (x, y+31), (x+width, y+31), 2)