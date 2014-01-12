import pygame
from src.entities.entity import Entity
from src.items.item import Item
from src.level.generator.astar import *

class Player(Entity):
    def __init__(self, pos, world):
        Entity.__init__(self, 'Draughtbane, Secret of Honor', pos, world)
        self.images = [pygame.image.load('res/player/m/ranger/back.png'),
                       pygame.image.load('res/player/m/ranger/right.png'),
                       pygame.image.load('res/player/m/ranger/front.png'),
                       pygame.image.load('res/player/m/ranger/left.png')]
        self.dir = 0
        self.icon = pygame.image.load('res/player/m/ranger/icon.png')
        self.move_ticker = 0
        self.inventory = []
        self.weapon = None
        self.armor = None
        self.trinket = None
        self.astar = Pathfinder()

        self.stats = {'STATUS': ' ',
                           'HP': [50, 100],
                           'MP': [70, 100],
                           'EXP': [0, 100],
                           'LVL': 1,
                           'DMG': 6,
                           'DEF': 9,
                           'MAG': 12,
                           'GOLD': 128}


        self.mouse_grid_x = 0
        self.mouse_grid_y = 0
        self.path = None
        self.path_delay = 0
        self.follow_p = False

    def update(self, events, offset, mouse):
        xa = 0
        ya = 0
        if self.path:
            if self.follow_p:
                self.follow_p = True
                self.follow_path(mouse)
                return
        self.follow_p = False
        self.path_delay = 0

        for item in self.inventory:
            if not self.weapon and item.category == 'weapon':
                self.weapon = item
                item.equip(self)
                self.inventory.remove(item)
            if not self.armor and item.category == 'armor':
                self.armor = item
                item.equip(self)
                self.inventory.remove(item)
            if not self.trinket and item.category == 'trinket':
                self.trinket = item
                item.equip(self)
                self.inventory.remove(item)


        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0] and self.path and mouse[0]*32 < 700:
                    self.follow_p = True

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    xa = -1
                if event.key == pygame.K_RIGHT:
                    xa = 1
                if event.key == pygame.K_UP:
                    ya = -1
                if event.key == pygame.K_DOWN:
                    ya = 1

        if self.mouse_grid_x != mouse[0] + offset.x/32 or self.mouse_grid_y != mouse[1] + offset.y/32:
            self.mouse_grid_x = mouse[0] + offset.x/32
            self.mouse_grid_y = mouse[1] + offset.y/32
            self.calculate_path(mouse)

        if xa != 0 or ya != 0:
            self.calculate_path(mouse)
            self.move(xa, ya)

        self.calculate_stats()

    def move(self, xa, ya):
        if xa > 0:
            self.dir = 1
            xa = 1
        elif xa < 0:
            self.dir = 3
            xa = -1
        elif ya > 0:
            self.dir = 2
            ya = 1
        elif ya < 0:
            self.dir = 0
            ya = -1
        # Check collision from the grid.
        tile = self.world.map.map.tiles[self.y + ya][self.x + xa]

        for entity in self.world.map.entities:
            if entity != self:
                if entity.x == self.x + xa and entity.y == self.y + ya:
                    if entity.x == self.path[-1][0] and entity.y == self.path[-1][1]:
                        if entity.type == 'item' or entity.type == 'powerup':
                            entity.pickup(self.world)

        if hasattr(tile, 'id'):
            if tile.id == 2 or tile.id == 3 or tile.id == 4 or tile.id == 5 or tile.id == 6 or tile.id == 7:
                xa = 0
                ya = 0
            if tile.id == 8:
                self.world.move_up(self)
                self.path = None
                self.x, self.y = self.world.map.down_stair

            elif tile.id == 9:
                self.world.move_down(self)
                self.path = None
                self.x, self.y = self.world.map.up_stair

            else:
                self.x += xa
                self.y += ya

        else:
            if tile.name == 'Chest':
                tile.loot()
                tile.open()

    def calculate_stats(self):
        if self.stats['EXP'][0] >= self.stats['EXP'][1]:
            self.stats['LVL'] += 1
            self.stats['EXP'][0] = 0
            self.stats['EXP'][1] = 100 * self.stats['LVL']

        if self.stats['HP'][0] > self.stats['HP'][1]:
            self.stats['HP'][0] = self.stats['HP'][1]
        if self.stats['MP'][0] > self.stats['MP'][1]:
            self.stats['MP'][0] = self.stats['MP'][1]

    def calculate_path(self, mouse):
        for row in range(0, len(self.world.map.map.tiles)):
            for tile in range(0, len(self.world.map.map.tiles[row])):
                if hasattr(self.world.map.map.tiles[row][tile], 'id'):
                    if self.world.map.map.tiles[row][tile].id == 15:
                        self.world.map.map.tiles[row][tile].id = self.world.map.dungeon.grid[row][tile]
                        self.world.map.map.tiles[row][tile].dirs = [2, 2]
                        self.world.map.map.tiles[row][tile].load_image()

        if mouse[0]*32 < 700:

            if len(self.world.map.map.tiles) - 1 >= self.mouse_grid_y:
                if len(self.world.map.map.tiles[self.mouse_grid_y]) - 1 >= self.mouse_grid_x:

                    start = (self.x, self.y)
                    end = (self.mouse_grid_x, self.mouse_grid_y)
                    blocked_tiles = [0, 2, 3, 4, 5, 6, 7, 8, 9, 10]
                    self.path = None
                    start_dir = 0
                    if self.mouse_grid_x is not self.x:
                        if self.mouse_grid_x > self.x:
                            start_dir = 2
                        elif self.mouse_grid_x < self.x:
                            start_dir = 6
                        if self.mouse_grid_y > self.y:
                            start_dir += 1
                        elif self.mouse_grid_y < self.y:
                            start_dir -= 1
                    elif self.mouse_grid_y > self.y:
                        start_dir = 4
                    elif self.mouse_grid_y < self.y:
                        start_dir = 0


                    path = self.astar.find_path(self.world.map.dungeon.grid, start, end, blocked_tiles, start_dir)
                    if path:

                        self.path = path
                        tile = self.world.map.map.tiles[path[-1][1]][path[-1][0]]
                        if hasattr(tile, 'id'):
                            if tile.id == 1 or tile.id == 11:
                                tile.id = 15
                                tile.load_image()
                        for i in range(0, len(path)):
                            tile = self.world.map.map.tiles[path[i][1]][path[i][0]]
                            if hasattr(tile, 'id'):
                                tile.id = self.world.map.dungeon.grid[path[i][1]][path[i][0]]
                                tile.dirs = [2, 2]
                                tile.load_image()
                                if len(path) > i + 1:
                                    current_node = self.astar.nodes[path[i + 1][1]][path[i + 1][0]]
                                    last = False
                                else:
                                    current_node = self.astar.nodes[path[i][1]][path[i][0]]
                                    last = True
                                dir = 0
                                p = 0
                                if current_node.parent:
                                    p = current_node.parent
                                if current_node.dir:
                                    dir = current_node.dir

                                self.world.map.map.tiles[path[i][1]][path[i][0]].dirs[1] = 9
                                if p:
                                    tile.dirs[0] = p.dir
                                    tile.dirs[1] = dir
                                    if dir:
                                        tile.dirs[1] = dir
                                    else:
                                        tile.dirs[1] = p.dir
                                elif dir:
                                    tile.dirs[0] = dir

                                if len(path) == 1:
                                    if not p:
                                        tile.dirs[1] = 2
                                    else:
                                        if p.dir == 7:
                                            tile.dirs[0] = 5
                                            tile.dirs[1] = 5
                                        elif p.dir == 5:
                                            tile.dirs[0] = 7
                                            tile.dirs[1] = 7

                                tile.id = 15
                                tile.load_image()
                                self.world.map.map.tiles[path[i][1]][path[i][0]] = tile

    def follow_path(self, mouse):
        if not self.path:
            self.path_delay = 0
            return
        if len(self.path) == 0:
                self.path_delay = 5
                self.calculate_path(mouse)
                return
        if self.path_delay == 0:
            self.path_delay = 5
            x = self.path[0][0]
            y = self.path[0][1]
            if hasattr(self.world.map.map.tiles[y][x], 'id'):
                self.world.map.map.tiles[y][x].id = self.world.map.dungeon.grid[y][x]
                self.world.map.map.tiles[y][x].load_image()
            self.move(x - self.x, y - self.y)
            if self.path:
                self.path.remove(self.path[0])
            if not self.path:
                self.path_delay = 5
                self.follow_p = False
                self.calculate_path(mouse)

        else:
            self.path_delay -= 1

    def draw(self, screen, offset):
        screen.blit(self.images[self.dir], (self.x*32-offset.x, self.y*32-offset.y))