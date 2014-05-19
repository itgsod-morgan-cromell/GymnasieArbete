import pygame
from src.entities.classdata import ClassData
from src.entities.entity import Entity
from src.level.dungeon_generator.astar import *
from src.event_helper import *
import random
import os
from src.level.dungeon_generator.fov import *


class Monster(Entity):
    def __init__(self, pos, world):
        self.lvl = 1
        _class = random.choice(os.listdir('../res/entities/monster_classes')).replace('.xls', '')
        name = random.choice(os.listdir('../res/entities/monster'))
        image = pygame.image.load('../res/entities/monster/{0}'.format(name))
        name_string = name.replace("_", ' ').replace(".png", "")
        Entity.__init__(self, name_string, _class, pos, world, random.randint(5, 10), 'monster', image)

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
            if self.world.map.tiles[y][x].id in [0, 2, 3, 4, 5, 6, 8, 9]:
                return False
            else:
                return True
        except IndexError:
            return False

    def attack(self, target):
        post_event(ENTITY_ATTACK, attacker=self, target=target)

    def die(self):
        self.world.entities.remove(self)