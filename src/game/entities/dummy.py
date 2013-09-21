from mob import Mob
import game.game
import pygame
from random import randint


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

        self.sprite = game.gfx.animate.PygAnimation([('../res/sprites/dummy/walk_top.png', 0.3, 4, 1)])
        self.sprite.play()
        self.time = 29
        self.targetX = game.game.player.x
        self.targetY = game.game.player.y
        self.start = False

    def update(self):
        if not self.start:
            return
        xa = 0
        ya = 0
        if game.game.player.targetX > self.x:
            xa += 1
        if game.game.player.targetX < self.x:
            xa -= 1
        if game.game.player.targetY > self.y:
            ya += 1
        if game.game.player.targetY < self.y:
            ya -= 1


        if xa != 0 or ya != 0:
            self.move(xa, ya)
            self.isMoving = True
        else:
            self.isMoving = False

        self.rect.x = self.x + self.data.spriteOffsetX
        self.rect.y = self.y + self.data.spriteOffsetY

    def hasCollided(self, xa, ya):
        xa *= self.speed
        ya *= self.speed

        dummy_rect = pygame.Rect(self.rect.x + xa, self.rect.y + ya, self.rect.w, self.rect.h)
        if not game.game.world.mapRect.contains(dummy_rect):
            self.xa = randint(0, 3) - 1
            self.ya = randint(0, 3) - 1
            return True
        if game.game.world.collide(dummy_rect):
            self.xa = 0
            self.ya = 0
            self.xa = randint(0, 3) - 1
            self.ya = randint(0, 3) - 1
            return True

        object = game.game.world.collide_object(self, dummy_rect)
        if object:
            if self.checkInteraction(object):
                self.xa = randint(0, 3) - 1
                self.ya = randint(0, 3) - 1
                return True

        return False

    def checkInteraction(self, object):
        if object.type == 'player' or object.type == 'dummy':
            return True

    def render(self):
        screen = game.game.screen

        screen.fill((0,255,0), pygame.Rect(self.targetX - game.game.camera.x, self.targetY - game.game.camera.y, 16, 16))
        x = self.x - game.game.camera.x
        y = self.y - game.game.camera.y

        self.sprite.blit(screen, (x, y))