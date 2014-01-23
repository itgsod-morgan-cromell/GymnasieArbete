"""
### Dungeon Generator --- map_loader.py ###
###########################################
####### Breiny Games (c) 2011 #############
###########################################
## This file contains the classes and    ##
## functions used to graphically display ##
## the data representing a randomly      ##
## generated dungeon generated from the  ##
## map_generator.py module.              ##
"""


import pygame
import random
from src.util.pyganim import *


class MinimapTile:

    def __init__(self, x, y, w, h, tile_id):

        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.rect = pygame.Rect(self.x, self.y,
                                self.w, self.h)
        self.image = pygame.surface.Surface((self.w, self.h), pygame.SRCALPHA, 32)
        self.image.convert_alpha()

        self.id = tile_id
        if self.id == 1 or self.id == 11 or self.id == 7:
            self.image.fill((40, 40, 40))
        elif self.id in [2, 3, 4, 5, 6]:
            self.image.fill((20, 20, 20))
        elif self.id == 8:
            self.image.fill((75, 75, 75))
        elif self.id == 9:
            self.image.fill((255, 10, 10))


class Tile:

    def __init__(self, x, y, w, h, tile_id):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.dirs = [0, 0]  # Each index of dir is able to be in 8 directions. 0 being up and 7 being left-up
        self.rect = pygame.Rect(self.x, self.y,
                                self.w, self.h)

        self.image = pygame.surface.Surface((self.w, self.h), pygame.SRCALPHA, 32)

        self.anim = None
        self.id = tile_id
        self.load_image()

    def load_tile_image(self, type, name, range=None):
        if range:
            self.image.blit(pygame.image.load('res/tiles/{0}/{1}{2}.png'.format(type, name, random.randint(*range))), (0, 0))
        else:
            self.image.blit(pygame.image.load('res/tiles/{0}/{1}.png'.format(type, name)), (0, 0))

    def load_image(self):
        self.feet = None
        if self.id == 0:
            self.image.fill((0, 0, 0))
        elif self.id == 1 or self.id == 11:
            self.load_tile_image('floor', 'cobble_blood', (1, 12))
        elif self.id == 2 or self.id == 3 or self.id == 4 or self.id == 5 or self.id == 6:
            self.load_tile_image('wall', 'brick_dark', (0, 3))
        elif self.id == 7:
            self.image.fill((255, 0, 0))
        elif self.id == 8:
            self.load_tile_image('floor', 'cobble_blood', (1, 12))
            self.load_tile_image('gateways', 'stone_stair_up')
        elif self.id == 9:
            self.load_tile_image('floor', 'cobble_blood', (1, 12))
            self.load_tile_image('gateways', 'stone_stair_down')
        elif self.id == 10:
            self.load_tile_image('floor', 'cobble_blood', (1, 12))
        elif self.id == 12:
            self.load_tile_image('gateways', 'door_closed')
        elif self.id == 15:
            self.feet = pygame.Surface((32, 32), pygame.SRCALPHA, 32)
            # If its a pathfinding tile, draw out footsteps based on the directions of the feet.
            if self.dirs[0] != 9:
                f = pygame.image.load('res/other/footsteps/parent/0.png')
                f = self.rot_center(f, self.dirs[0] * -45)
                self.feet.blit(f, (0, 0))
            if self.dirs[1] != 9:
                f2 = pygame.image.load('res/other/footsteps/current/0.png')
                f2 = self.rot_center(f2, self.dirs[1] * -45)
                self.feet.blit(f2, (0, 0))

    def rot_center(self, image, angle):
        """rotate an image while keeping its center and size"""
        orig_rect = image.get_rect()
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image


class Map:

    def __init__(self):

        self.dungeon = None
        self.tiles = []
        self.shadow_tile = pygame.Surface((32, 32), pygame.SRCALPHA, 32)
        self.shadow_tile.fill((0, 0, 0, 200))

    def load_dungeon(self, dungeon, minimap=False, tile_size=None):

        self.dungeon = dungeon
        self.minimap = minimap
        self.tiles = []

        for y in range(0, self.dungeon.grid_size[1]):
            row = []
            for x in range(0, self.dungeon.grid_size[0]):
                if minimap:
                    row.append(MinimapTile(x * tile_size,
                                           y * tile_size,
                                           tile_size,
                                           tile_size,
                                           self.dungeon.grid[y][x]))
                else:
                    row.append(Tile(x * dungeon.tile_w,
                                    y * dungeon.tile_h,
                                    dungeon.tile_w,
                                    dungeon.tile_h,
                                    self.dungeon.grid[y][x]))
            self.tiles.append(row)


    def draw(self, surface, offset, explored_tiles=None):

        for row in self.tiles:
            for tile in row:
                x = tile.x -offset.x
                y = tile.y -offset.y
                tile_img = tile.image
                if not self.minimap:
                    if -1 < x < offset.w and -1 < y < offset.h:
                        if explored_tiles:
                            if explored_tiles[tile.y/tile.h][tile.x/tile.w] == 0:
                                surface.blit(tile_img, (x, y))
                                surface.blit(self.shadow_tile, (x, y))
                            elif explored_tiles[tile.y/tile.h][tile.x/tile.w] == 1:
                                surface.blit(tile_img, (x, y))
                            else:
                                pygame.draw.rect(surface, (0, 0, 0), pygame.Rect(x, y, 32, 32))
                        else:
                            surface.blit(tile_img, (x, y))
                        if tile.feet and tile.id == 15:
                            surface.blit(tile.feet, (x, y))
                else:
                    if explored_tiles:
                        if explored_tiles[tile.y/tile.h][tile.x/tile.w] in [1, 0]:
                            surface.blit(tile_img, (x, y))
                    else:
                        surface.blit(tile_img, (x, y))
