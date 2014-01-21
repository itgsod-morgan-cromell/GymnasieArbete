import pygame


def get_item_sprite(sheet, id):
    items = pygame.image.load("res/spritesheets/items/{0}.png".format(sheet))
    spritesheet_width = items.get_width()
    spritesheet_height = items.get_height()
    x = id*32 % spritesheet_width
    y = int(id*32/spritesheet_width)
    y *= 32
    if y > spritesheet_height:
        print "Cant find given item image"
        return None
    rect = pygame.Rect((x, y), (32, 32))
    image = pygame.Surface((32, 32))
    image.blit(items, (0, 0), rect)
    return image

