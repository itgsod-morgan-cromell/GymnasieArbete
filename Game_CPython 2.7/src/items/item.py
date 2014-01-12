import pygame


class PowerUp(object):
    def __init__(self, type, amount):
        self.type = 'powerup'
        self.name = type
        self.amount = amount
        if amount >= 100:
            image_amount = 'large'
        elif amount > 50:
            image_amount = 'medium'
        elif amount > 25:
            image_amount = 'small'
        else:
            image_amount = 'tiny'
        self.font = pygame.font.Font('res/other/visitor2.ttf', 20)
        self.image = pygame.image.load('res/items/other/{0}_{1}.gif'.format(self.name.lower(), image_amount))
        self.x = 0
        self.y = 0

    def pickup(self, world):
        world.map.entities.remove(self)
        if type(world.player.stats[self.name]) == list:
            world.player.stats[self.name][0] += self.amount
        else:
            world.player.stats[self.name] += self.amount

    def draw(self, screen, offset):
        screen.blit(self.image, (self.x*32 - offset.x, self.y*32 - offset.y))

        screen.blit(self.font.render(str(self.amount), 0, (192, 192, 192)), (self.x*32 - offset.x + 12, self.y*32 - offset.y + 16))


class Item(object):
    def __init__(self, name, category, image, stats, extra={}):
        self.name = name
        self.extra = extra
        self.type = 'item'
        self.category = category
        self.stats = stats
        if 'AMOUNT' in self.stats:
            self.stackable = True
        else:
            self.stackable = False

        self.equipped = False
        self.image = pygame.image.load(image)
        self.x = 0
        self.y = 0

    def drop(self, world):
        self.unequip(world.player)
        tile = world.map.map.tiles[world.player.y][world.player.x]
        if tile.id == 1 or tile.id == 11:
            self.x = world.player.x
            self.y = world.player.y
            if not self.stackable:
                world.map.entities.append(self)
                if self in world.player.inventory:
                    world.player.inventory.remove(self)
                elif self == world.player.weapon:
                    world.player.weapon = None
                elif self == world.player.armor:
                    world.player.armor = None
                elif self == world.player.trinket:
                    world.player.trinket = None
            else:
                world.player.inventory.remove(self)
                for item in world.map.entities:
                    if item.x == world.player.x and item.y == world.player.y:
                        if item.name == self.name:
                            item.stats['AMOUNT'] += self.stats['AMOUNT']
                            return
                world.map.entities.append(Item(self.name, self.category, self.image, self.stats, self.extra))



    def equip(self, player):
        if not self.equipped:
            for elem in self.stats:
                player.stats[elem] = player.stats.get(elem, 0) + self.stats[elem]
            self.equipped = True

    def unequip(self, player):
        if self.equipped:
            for elem in self.stats:
                player.stats[elem] = player.stats.get(elem, 0) - self.stats[elem]
            self.equipped = False

    def pickup(self, world):
        if self.stackable:
            for item in world.plater.inventory:
                if item.name == self.name:
                    world.map.entities.remove(self)
                    item.stats['AMOUNT'] += self.stats['AMOUNT']
                    return

        if len(world.player.inventory) < 9:
                world.player.inventory.append(self)
                world.map.entities.remove(self)

    def interacting(self, world, offset):
        mouse_x = pygame.mouse.get_pos()[0]
        mouse_y = pygame.mouse.get_pos()[1]


    def draw(self, screen, offset):
        screen.blit(self.image, (self.x*32 - offset.x, self.y*32 - offset.y))
