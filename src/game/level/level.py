
class Level(object):
    def __init__(self, filename):
        from pytmx import tmxloader
        self.tiledmap = tmxloader.load_pygame(filename, pixelalpha=True)

    def render(self, surface, camera):

        tw = self.tiledmap.tilewidth
        th = self.tiledmap.tileheight
        gt = self.tiledmap.getTileImage

        # Draw map tiles
        for layer in xrange(0, len(self.tiledmap.tilelayers)):
            for y in xrange(0, self.tiledmap.height):
                for x in xrange(0, self.tiledmap.width):
                    tile = gt(x, y, layer)
                    if tile: surface.blit(tile, (x*tw - camera.x, y*th - camera.y))

        # draw polygon and poly line objects
        for og in self.tiledmap.objectgroups:
            for o in og:
                if hasattr(o, 'points'):
                    points = [ (i[0]+o.x, i[1]+o.y) for i in o.points ]
                    pygame.draw.lines(surface, (255,128,128), o.closed, points, 2)
                else:
                    pygame.draw.rect(surface, (255,128,128),
                                    (o.x, o.y, o.width, o.height), 2)