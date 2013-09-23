import pygame
import game.game
import game.gfx.animate
import game.entities.player
import game.entities.dummy
import os
import game.gfx.PAdLib.occluder as occluder


class Level(object):
    def __init__(self, filename):
        from pytmx import tmxloader
        self.current_path = filename
        self.name = os.path.splitext(os.path.basename(filename))[0]
        self.tiledmap = tmxloader.load_pygame(filename, pixelalpha=True)
        self.map_width = self.tiledmap.width * self.tiledmap.tilewidth
        self.map_height = self.tiledmap.height * self.tiledmap.tileheight
        self.mapRect = pygame.Rect(0, 0, self.map_width, self.map_height)
        self.map_buffer = pygame.Surface((self.map_width, self.map_height))
        self.map_buffer_top = pygame.Surface(game.game.screen.get_size(), pygame.SRCALPHA)
        self.map_object_buffer = pygame.Surface(game.game.screen.get_size(), pygame.SRCALPHA)
        self.map_buffer_top = self.map_buffer_top.convert_alpha()
        self.animated_tiles = {}
        if self.name not in game.game.mapdata:
            self.entities = []
            self.createEntities()
        else:
            self.entities = game.game.mapdata[self.name]
        self.create_map()

    def collide(self, rect):
        tw = self.tiledmap.tilewidth
        th = self.tiledmap.tileheight
        nTile = int(rect.y / th) - 1
        sTile = int((rect.y + rect.h) / th) + 1
        wTile = int(rect.x / tw) - 1
        eTile = int((rect.x + rect.w) / tw) + 1

        if eTile > self.tiledmap.width:
            eTile = self.tiledmap.width
        if sTile > self.tiledmap.height:
            sTile = self.tiledmap.height

        for layer in xrange(0, len(self.tiledmap.tilelayers)):
            for y in xrange(nTile, sTile):
                for x in xrange(wTile, eTile):

                    gid = self.tiledmap.getTileGID(x, y, layer)

                    if gid:
                        if hasattr(self.tiledmap.tilelayers[layer], "is_walls"):
                            tileRect = pygame.Rect(x*tw, y*th, tw, th)
                            if rect.colliderect(tileRect):
                                return True

                        tileProperties = self.tiledmap.getTilePropertiesByGID(gid)
                        if tileProperties:
                            if "wall" in tileProperties:
                                wall = tileProperties["wall"]
                                offsetN = 0
                                offsetS = 0
                                offsetW = 0
                                offsetE = 0

                                if "n" in wall:
                                    offsetN = -th/2
                                if "s" in wall:
                                    offsetS = th/2
                                if "w" in wall:
                                    offsetW = - tw/2
                                if "e" in wall:
                                    offsetE = tw/2

                                tileRect = pygame.Rect(x*tw + offsetE, y*th + offsetS, tw + offsetW - offsetE, th + offsetN - offsetS)
                                if rect.colliderect(tileRect):
                                    return True

    def get_solids(self, occluders, rect):
        tw = self.tiledmap.tilewidth
        th = self.tiledmap.tileheight
        nTile = int(rect.y / th) - 1
        sTile = int((rect.y + rect.h) / th)
        wTile = int(rect.x / tw) - 1
        eTile = int((rect.x + rect.w) / tw)

        if eTile > self.tiledmap.width:
            eTile = self.tiledmap.width
        if sTile > self.tiledmap.height:
            sTile = self.tiledmap.height

        for layer in xrange(0, len(self.tiledmap.tilelayers)):
            for y in xrange(nTile, sTile):
                for x in xrange(wTile, eTile):
                    gid = self.tiledmap.getTileGID(x, y, layer)
                    if gid:
                        if hasattr(self.tiledmap.tilelayers[layer], "is_walls"):
                            occluders.append(occluder.Occluder([[x*tw - rect.x, y*th - rect.y], [x*tw - rect.x, y*th+th - rect.y], [x*tw+tw - rect.x, y*th+th - rect.y], [x*tw+tw - rect.x, y*th - rect.y]]))
        return occluders




    def collide_object(self, obj, rect):
        for og in self.tiledmap.objectgroups:
            if og.name == "triggers":
                for o in og:
                    if o.x > game.game.camera.x and o.x + o.width < game.game.camera.x + game.game.camera.w:
                        if o.y > game.game.camera.y and o.y + o.height < game.game.camera.y + game.game.camera.h:
                            object_rect = pygame.Rect(o.x, o.y, o.width, o.height)
                            if rect.colliderect(object_rect):
                                return o

        for e in game.game.mapdata[self.name]:
            if e != obj:  # To make sure we don't check collision with ourselves.
                if rect.colliderect(e.rect):
                    return e

    def update(self):
        self.map_buffer_top.fill((255, 255, 255, 0))
        self.map_object_buffer.fill((255, 255, 255, 0))
        camera = game.game.camera
        tw = self.tiledmap.tilewidth
        th = self.tiledmap.tileheight

        # Calculate what tiles are visible on the screen
        min_x = int(camera.x/tw)
        max_x = int((camera.x + game.game.screen.get_width())/tw) + 2
        if max_x > self.tiledmap.width: max_x = self.tiledmap.width

        min_y = int(camera.y/th)
        max_y = int((camera.y + game.game.screen.get_height())/th) + 2
        if max_y > self.tiledmap.height: max_y = self.tiledmap.height

        # Draw top tiles
        for layer in xrange(0, len(self.tiledmap.tilelayers)):
            if hasattr(self.tiledmap.tilelayers[layer], "above"):
                for y in xrange(min_y, max_y):
                    for x in xrange(min_x, max_x):
                        gid = self.tiledmap.getTileGID(x, y, layer)
                        tile = self.tiledmap.images[gid]
                        if tile:
                                if y*th > game.game.player.rect.y or \
                                        self.tiledmap.getTileImage(game.game.player.rect.x/tw, game.game.player.rect.y/th, layer) or \
                                        self.tiledmap.getTileImage((game.game.player.rect.x + game.game.player.rect.w)/tw, (game.game.player.rect.y + game.game.player.rect.h)/th, layer):
                                    self.map_buffer_top.blit(tile, (x*tw - camera.x, y*th - camera.y))

        # Draw all the animated tiles to the map buffer
        for anim in self.animated_tiles:
            tile_img = self.animated_tiles[anim][0]
            tile_x = self.animated_tiles[anim][1]
            tile_y = self.animated_tiles[anim][2]
            tile_layer = self.animated_tiles[anim][3]
            if tile_x < min_x or tile_x > max_x or tile_y < min_y or tile_y > max_y:
                self.animated_tiles[anim][0].pause()
            else:
                self.animated_tiles[anim][0].play()
                if hasattr(self.tiledmap.tilelayers[tile_layer], "above"):
                    if tile_y*th > game.game.player.rect.y or \
                            self.tiledmap.getTileImage(game.game.player.rect.x/tw, game.game.player.rect.y/th, tile_layer) or \
                            self.tiledmap.getTileImage((game.game.player.rect.x + game.game.player.rect.w)/tw, (game.game.player.rect.y + game.game.player.rect.h)/th, tile_layer):
                        tile_img.blit(self.map_buffer_top, (tile_x*tw - camera.x, tile_y*th - camera.y))
                    else:
                        tile_img.blit(self.map_object_buffer, (tile_x*tw - camera.x, tile_y*th - camera.y))
                else:
                    tile_img.blit(self.map_object_buffer, (tile_x*tw - camera.x, tile_y*th - camera.y))

        # draw polygon and poly line objects
        if game.game.debug:
            for og in self.tiledmap.objectgroups:
                for o in og:
                    if o.x > min_x*tw and o.x + o.width < max_x*tw and o.y > min_y*th and o.y + o.height < max_y*th:
                        if hasattr(o, 'points'):
                            points = [(i[0]+o.x-camera.x, i[1]+o.y-camera.y) for i in o.points]
                            pygame.draw.lines(self.map_object_buffer, (255,128,128), o.closed, points, 2)
                        else:
                            if hasattr(og, "color"):
                                pygame.draw.rect(self.map_object_buffer, pygame.Color(og.color),
                                                (o.x - camera.x, o.y - camera.y, o.width, o.height), 2)

    def updateEntity(self):
        for e in game.game.mapdata[self.name]:
            if game.game.camera.inflate(-100, -100).contains(e.rect):
                e.start = True
            e.update()

    def create_map(self):
        self.map_buffer.fill((50, 33, 37))
        tw = self.tiledmap.tilewidth
        th = self.tiledmap.tileheight

        # Draw map tiles
        for layer in xrange(0, len(self.tiledmap.tilelayers)):
            for y in xrange(0, self.tiledmap.height):
                for x in xrange(0, self.tiledmap.width):
                    tile_gid = self.tiledmap.getTileGID(x, y, layer)
                    tile = self.tiledmap.images[tile_gid]
                    if tile:
                        gid = (x, y, layer)
                        tile_properties = self.tiledmap.getTilePropertiesByGID(tile_gid)
                        if tile_properties:
                            if 'lightingRadius' in tile_properties:
                                game.game.lighting.addLight(int(tile_properties['lightingRadius']), x*tw+tw/2, y*th+th/2)

                            if 'animation' in tile_properties:
                                if gid not in self.animated_tiles:
                                    self.animated_tiles[gid] = [game.gfx.animate.PygAnimation([('../res/sprites/animated_tiles/%s' % tile_properties['animation'],
                                                                                                float(tile_properties['delay']),
                                                                                                int(tile_properties['frames_x']),
                                                                                                int(tile_properties['frames_y'])
                                                                                             )]), x, y, layer
                                                                ]
                                    self.animated_tiles[gid][0].play()
                            else:
                                self.map_buffer.blit(tile, (x*tw, y*th))
                        else:
                            self.map_buffer.blit(tile, (x*tw, y*th))

    def createEntities(self):
        for og in self.tiledmap.objectgroups:
            if og.name == "entities":
                for o in og:
                    if o.type == "player":
                        player = game.entities.player.Player(o)
                        game.game.player = player
                        self.entities.append(game.game.player)
                    elif o.type == "dummy":
                        self.entities.append(game.entities.dummy.Dummy(o))


        game.game.mapdata[self.name] = self.entities


    def find_object(self, layer_name, obj_name):
        for og in self.tiledmap.objectgroups:
            if og.name == layer_name:
                for o in og:
                    if o.name == obj_name:
                        return o


    def render_background(self):
        game.game.screen.blit(self.map_buffer, (0,0), game.game.camera)
        game.game.screen.blit(self.map_object_buffer, (0, 0))

    def render(self):
        for e in game.game.mapdata[self.name]:
            if game.game.camera.inflate(100, 100).contains(e.rect):
                e.render()
        game.game.screen.blit(self.map_buffer_top, (0, 0))


