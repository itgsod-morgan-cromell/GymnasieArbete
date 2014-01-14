import pygame
from src.gui.character_status import StatsUi
from src.gui.explorer import Explorer
from src.gui.minimap import MiniMap
from src.gui.mouse_gui import MouseGui


class GuiHandler(object):
    def __init__(self, world):
        self.player_stats = StatsUi(world)
        self.minimap = MiniMap(world)
        self.explorer = Explorer(world)
        self.mouse_col = (0, 255, 0)
        self.mouse = None
        self.mouse_grid_x = 0
        self.mouse_grid_y = 0
        self.mouse_gui = MouseGui(world)
        self.mouse_img = pygame.Surface((32, 32), pygame.SRCALPHA, 32)
        self.mouse_img.convert_alpha()

    def update(self, world, offset, mouse, events):
        self.mouse_col = (255, 0, 0)
        self.player_stats.update(world)
        self.minimap.update(world)
        self.explorer.update(world, self.mouse)
        self.mouse_gui.update(world, events)
        self.mouse = None
        self.mouse_grid_x = mouse[0]
        self.mouse_grid_y = mouse[1]
        mouse_grid_x = self.mouse_grid_x + offset.x/32
        mouse_grid_y = self.mouse_grid_y + offset.y/32
        if self.mouse_grid_x*32 < offset.w - 16:
            for item in world.map.items:
                if item.x == mouse_grid_x and item.y == mouse_grid_y:
                    self.mouse_col = (0, 0, 255)
                    self.mouse = item
                    self.mouse_gui.update_data(item)
                    self.mouse_gui.active = True
                elif world.player.x == mouse_grid_x and world.player.y == mouse_grid_y:
                        self.mouse_col = (0, 0, 255)
                        self.mouse = world.player
                        self.mouse_gui.update_data(world.player)
                        self.mouse_gui.active = True
                else:
                    self.mouse_gui.active = False

        else:
            mouse_rect = pygame.Rect((pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]), (2, 2))
            mouse_rect.x -= self.player_stats.x
            mouse_rect.y -= self.player_stats.y
            colliding_slots = []
            for slot in self.player_stats.slots:
                if mouse_rect.colliderect(slot.rect):
                    colliding_slots.append(slot.containts)
            for slot in self.player_stats.inventory_slots:
                if mouse_rect.colliderect(slot.rect):
                    colliding_slots.append(slot.containts)

            if colliding_slots:
                self.mouse = colliding_slots[0]
                self.mouse_gui.update_data(colliding_slots[0])
                self.mouse_gui.active = True
            else:
                self.mouse_gui.active = False

    def draw(self, screen, offset):
        self.player_stats.draw(screen)
        self.minimap.draw(screen)
        self.explorer.draw(screen)
        self.mouse_gui.draw(screen)
        mouse_grid_x = self.mouse_grid_x*32
        mouse_grid_y = self.mouse_grid_y*32
        if mouse_grid_x < offset.w - 16:

            pygame.draw.lines(self.mouse_img, self.mouse_col, False, [(8, 0), (0, 0), (0, 8)], 2) #top left
            pygame.draw.lines(self.mouse_img, self.mouse_col, False, [(24, 0), (30, 0), (30, 8)], 2) #top right
            pygame.draw.lines(self.mouse_img, self.mouse_col, False, [(24, 30), (30, 30), (30, 24)], 2) #bottom right
            pygame.draw.lines(self.mouse_img, self.mouse_col, False, [(0, 24), (0, 30), (8, 30)], 2) #bottom left
            screen.blit(self.mouse_img, (mouse_grid_x, mouse_grid_y))
