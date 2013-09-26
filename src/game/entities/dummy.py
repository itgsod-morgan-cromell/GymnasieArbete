from .mob import Mob
import game.game
import pygame
from random import randint

'''
This is a simple straight up 'follow player' AI that i am using as a prototype. See player and the parent class for more info.
'''

class Dummy(Mob):

    def __init__(self, data):
        self.data = data
        if not hasattr(self.data, 'spriteOffsetX'):
            self.data.spriteOffsetX = 0
        if not hasattr(self.data, 'spriteOffsetY'):
            self.data.spriteOffsetY = 0
        self.data.spriteOffsetX = int(self.data.spriteOffsetX)
        self.data.spriteOffsetY = int(self.data.spriteOffsetY)
        x = data.x - self.data.spriteOffsetX
        y = data.y - self.data.spriteOffsetY
        speed = int(data.speed)
        rect = pygame.Rect(x, y, data.width, data.height)
        super(Dummy, self).__init__(game.game.world, data.type, x, y, speed, rect)

        self.sprite = game.gfx.animate.PygAnimation('../res/sprites/dummy/test.xml')
        self.sprite.play()
        self.time = 29
        self.start = False
        self.thinking = False

    def update(self):
        if not self.start:
            return
        self.dirty = 0
        targetX = game.game.player.targetX
        targetY = game.game.player.targetY
        xa = 0
        ya = 0
        if targetX > self.x:
            xa += 1
        if targetX < self.x:
            xa -= 1
        if targetY > self.y:
            ya += 1
        elif targetY < self.y:
            ya -= 1


        if xa != 0 or ya != 0:
            self.move(xa, ya)
            self.isMoving = True
        else:
            self.isMoving = False

        self.rect.x = self.x + self.data.spriteOffsetX
        self.rect.y = self.y + self.data.spriteOffsetY

        self.oldPos = (self.x, self.y)
    def hasCollided(self, xa, ya):
        xa *= self.speed
        ya *= self.speed

        dummy_rect = pygame.Rect(self.rect.x + xa, self.rect.y + ya, self.rect.w, self.rect.h)
        if not game.game.world.mapRect.contains(dummy_rect):
            self.xa = randint(0, 3) - 1
            self.ya = randint(0, 3) - 1
            return True
        if game.game.world.collide(dummy_rect):
            return True

        object = game.game.world.collide_object(self, dummy_rect)
        if object:
            if self.checkInteraction(object):
                return True

        self.thinking = False
        return False

    def checkInteraction(self, object):
        if object.type == 'dummy':
            self.thinking = True
            return True

        if object.type == 'player':
            if self in game.game.mapdata[game.game.world.name]:
                game.game.mapdata[game.game.world.name].remove(self)

    def render(self):
        screen = game.game.screen


        x = self.x - game.game.camera.x
        y = self.y - game.game.camera.y

        self.sprite.blit(screen, (x, y))