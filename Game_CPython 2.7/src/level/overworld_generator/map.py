import pygame



class Map:


    def __init__(self, type, map):

        self.type = type
        self.tiles = map
        self.width = len(self.tiles[0])
        self.height = len(self.tiles)
        self.tile_size = 32

        self.waterline = 0
        
        self.minimap = pygame.Surface((self.width * self.tile_size,
                                       self.height * self.tile_size))
        self.draw_minimap()


    def get_waterline(self):

        values = []
        for y in range(0, self.height):
            for x in range(0, self.width):
                values.append(self.tiles[y][x])
        values.sort()

        return values[int((len(values)-1)*.60)]
        

    def draw_minimap(self):

        self.waterline = self.get_waterline()

        for y in range(0, self.height):
            for x in range(0, self.width):
                self.tiles[y][x] = int(self.tiles[y][x])
                if self.tiles[y][x] > 255:
                    self.tiles[y][x] = 255
                tile = int(self.tiles[y][x])

                if tile <= self.waterline:
                    color = (25, 25, tile+75)
                elif tile > self.waterline and tile <= self.waterline + 10:
                    color = (tile+80, tile+80, 100)
                elif tile > self.waterline + 10 and tile <= self.waterline + 40:
                    color = (0, 255-tile, 0)
                elif tile > self.waterline + 40 and tile <= 190:
                    color = (0, 255-tile, 0)
                elif tile > 190:
                    color = (255-tile, 255-tile, 255-tile)

                #color = (tile, tile, tile)
                
                image = pygame.Surface((self.tile_size, self.tile_size))
                image.fill(color)
                self.minimap.blit(image, (x * self.tile_size,
                                          y * self.tile_size))
    def draw(self, surface, offset, nothing):
        surface.blit(self.minimap, (-offset.x, -offset.y))
