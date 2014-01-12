import pygame
from src.gui.character_status import StatsUi
from src.gui.explorer import Explorer
from src.gui.minimap import MiniMap


class GuiHandler(object):
    def __init__(self, world):
        self.guis = []
        player_stats = StatsUi(world.player)
        self.guis.append(player_stats)
        minimap = MiniMap(world)
        self.guis.append(minimap)
        explorer = Explorer(world)
        self.guis.append(explorer)
        self.mouse_col = (0, 255, 0)
        self.mouse = None
        self.mouse_grid_x = 0
        self.mouse_grid_y = 0

    def update(self, world, offset, mouse, events):
        self.mouse_col = (255, 0, 0)
        for gui in self.guis:
            if gui.active:
                if gui.type == 'explorer':
                    gui.update(world, self.mouse)
                else:
                    gui.update(world)
        self.mouse = None
        self.mouse_grid_x = mouse[0]
        self.mouse_grid_y = mouse[1]
        mouse_grid_x = self.mouse_grid_x + offset.x/32
        mouse_grid_y = self.mouse_grid_y + offset.y/32
        if self.mouse_grid_x*32 < 700:
            if len(world.map.map.tiles) - 1 >= mouse_grid_y:
                if len(world.map.map.tiles[mouse_grid_y]) - 1 >= mouse_grid_x:
                    tile = world.map.map.tiles[mouse_grid_y][mouse_grid_x]
                    if hasattr(tile, 'id'):
                        id = tile.id
                        if id == 1 or id == 11 or id == 15:
                            self.mouse_col = (0, 255, 0)
                    else:
                        self.mouse_col = (255, 0, 255)
                        self.mouse = tile
                    for entity in world.map.entities:
                        if entity.x == mouse_grid_x and entity.y == mouse_grid_y:
                            self.mouse_col = (0, 0, 255)
                            self.mouse = entity
        else:
            mouse_rect = pygame.Rect((pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]), (2, 2))
            for gui in self.guis:
                if gui.type == 'character':
                    mouse_rect.x -= gui.x
                    mouse_rect.y -= gui.y
                    colliding_slots = []
                    for slot in gui.slots:
                        if mouse_rect.colliderect(slot.rect):
                            colliding_slots.append(slot.containts)
                    for slot in gui.inventory_slots:
                        if mouse_rect.colliderect(slot.rect):
                            colliding_slots.append(slot.containts)

                    if colliding_slots:
                        self.mouse = colliding_slots[0]
                        if hasattr(colliding_slots[0], 'type'):
                            if colliding_slots[0].type == 'item':
                                for event in events:
                                    if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                                        colliding_slots[0].interacting(world, offset)
                                        colliding_slots[0].drop(world)

    def draw(self, screen, offset):
        for gui in self.guis:
            if gui.active:
                gui.draw(screen)
        mouse_grid_x = self.mouse_grid_x*32
        mouse_grid_y = self.mouse_grid_y*32
        if mouse_grid_x < 700:

            pygame.draw.rect(screen, self.mouse_col, pygame.Rect((mouse_grid_x, mouse_grid_y), (32, 32)), 2)