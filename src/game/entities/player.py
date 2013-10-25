import math
import pygame
import game.game
import game.gfx.animate
from .mob import Mob
import random
from src.game.entities.projectile.basicBullet import BasicBullet

'''
The player class is a child of the mob class and is currently just a simple animated sprite moving around via inputs.

The code should be pretty self explanatory.
'''

# TODO: Fix the animations to use the new xml format for more cleanup.
# TODO: Hook in the projectile system.

class Player(Mob):
    def __init__(self, data):
        self.data = data
        self.data.spriteOffsetX = int(self.data.spriteOffsetX)
        self.data.spriteOffsetY = int(self.data.spriteOffsetY)
        x = data.x - self.data.spriteOffsetX
        y = data.y - self.data.spriteOffsetY
        speed = int(data.speed)
        self.moveSpeed = speed
        rect = pygame.Rect(0, 0, data.width, data.height)
        super(Player, self).__init__(data.type, x, y, speed, rect)

        self.anim_objs = {}
        # create the right-facing sprites by copying and flipping the left-facing sprites
        self.anim_objs['LEFT'] = game.gfx.animate.PygAnimation('../res/sprites/player/test_left.xml')
        self.anim_objs['DOWN'] = game.gfx.animate.PygAnimation('../res/sprites/player/test_front.xml')
        self.anim_objs['DOWN_LEFT'] = game.gfx.animate.PygAnimation('../res/sprites/player/test_front_left.xml')
        self.anim_objs['DOWN_RIGHT'] = game.gfx.animate.PygAnimation('../res/sprites/player/test_front_right.xml')
        self.anim_objs['RIGHT'] = game.gfx.animate.PygAnimation('../res/sprites/player/test_right.xml')
        self.anim_objs['UP'] = game.gfx.animate.PygAnimation('../res/sprites/player/test_back.xml')
        self.anim_objs['UP_RIGHT'] = game.gfx.animate.PygAnimation('../res/sprites/player/test_back_right.xml')
        self.anim_objs['UP_LEFT'] = game.gfx.animate.PygAnimation('../res/sprites/player/test_back_left.xml')

        self.anim_objs['front_fire'] = game.gfx.animate.PygAnimation('../res/sprites/player/test_front_fire.xml')

        self.anim_objs['standing'] = game.gfx.animate.PygAnimation('../res/sprites/player/test_standing.xml')
        self.standingDirs = {
            'UP': 0, 'DOWN': 4, 'LEFT': 6, 'RIGHT': 2,
            'UP_LEFT': 7, 'UP_RIGHT': 1, 'DOWN_LEFT': 5, 'DOWN_RIGHT': 3}


        self.spriteRect = self.anim_objs['LEFT'].getRect()

        self.move_conductor = game.gfx.animate.PygConductor(self.anim_objs)

        self.centerX = self.x + self.spriteRect.x + self.spriteRect.w / 2
        self.centerY = self.y + self.spriteRect.y + self.spriteRect.h / 2
        self.time = 30
        self.targetX = 0
        self.targetY = 0
        self.fireTime = 0
        self.fireRate = 0

    def update(self):
        self.fireTime += 1
        # Set the path that the dummy AI should walk towards. We have a bit of delay here so the AI is more human.
        self.time += 1
        if self.time >= 30:
            self.time = 0
            self.targetX = self.rect.x
            self.targetY = self.rect.y

        self.running = False
        self.speed = self.moveSpeed
        xa = 0
        ya = 0
        input = game.game.input
        if input.GetControl('RIGHT'):
            xa += 1
        if input.GetControl('LEFT'):
            xa -= 1
        if input.GetControl('UP'):
            ya -= 1
        if input.GetControl('DOWN'):
            ya += 1

        if xa != 0 or ya != 0:
            for key in self.movingDir:
                self.movingDir[key] = False
            self.move(xa, ya)
            self.isMoving = True
        else:
            self.isMoving = False

        if input.GetControl('FIRE'):
            self.fire = True
            self.isMoving = True
            x = self.rect.x + self.rect.w/2
            y = self.rect.y

            for key in self.movingDir:
                if self.movingDir[key]:
                    projDir = self.projectileAngles[key]

            #projDir = math.atan2(pygame.mouse.get_pos()[1] - self.y, pygame.mouse.get_pos()[0] - self.x)/math.pi*180
            projDir *= math.pi/180

            self.shoot(x, y, projDir)
        else:
            self.fire = False

        self.rect.x = self.x + self.data.spriteOffsetX
        self.rect.y = self.y + self.data.spriteOffsetY
        game.game.camera.center = self.rect.center
        self.centerX = self.rect.center[0]
        self.centerY = self.rect.center[1] - self.spriteRect.h / 2

    def hasCollided(self, xa, ya):
        xa *= self.speed
        ya *= self.speed

        player_rect = pygame.Rect(self.rect.x + xa, self.rect.y + ya, self.rect.w, self.rect.h)
        if not game.game.world.mapRect.contains(player_rect):
            return True
        if game.game.world.collide(player_rect):
            return True

        object = game.game.world.collide_object(self, player_rect)
        if object:
            if self.checkInteraction(object):
                return True

        return False

    def checkInteraction(self, object):
        if object.type == 'sign':
            print("This is a sign")
            return True
        if object.type == 'teleporter':
            self.teleport(object)

        if object.type == 'dummy':
            return True

        '''
        This will move the player to another map by initializing the new map and move out the player entity from the old enitity list
        into the new one.
        '''

    def teleport(self, object):
        print("teleporting to :" + object.map)
        game.game.mapdata[game.game.world.name].remove(self)
        game.game.world = game.level.level.Level('../res/maps/%s/%s.tmx' % (object.map, object.map))
        game.game.mapdata[game.game.world.name].append(self)
        target = game.game.world.find_object("triggers", object.target)
        self.x = target.x + target.width / 2 - self.rect.w / 2 - self.data.spriteOffsetX
        self.y = target.y + target.height / 2 - self.rect.h / 2 - self.data.spriteOffsetY
        if target.spawn_position == "n":
            self.y -= target.height / 2 + 10
        elif target.spawn_position == "s":
            self.y += target.height / 2 + 10
        elif target.spawn_position == "w":
            self.x -= target.width / 2 + 10
        elif target.spawn_position == "e":
            self.x += target.width / 2 + 10

    def shoot(self, x, y, projDir):
        if self.fireTime > self.fireRate:
            p = BasicBullet(x, y, projDir)
            self.projectiles.append(p)
            game.game.world.addEntity(p)
            self.fireRate = p.rateOfFire
            self.fireTime = 0



    def render(self, screen):
        x = self.x - game.game.camera.x
        y = self.y - game.game.camera.y
        if game.game.debug:
            screen.fill((255, 0, 0),
                        pygame.Rect(x + self.data.spriteOffsetX, y + self.data.spriteOffsetY, self.rect.w, self.rect.h))

        if self.isMoving:
            self.move_conductor.play()

            if self.fire:
                self.anim_objs['front_fire'].blit(screen, (x, y))
            else:

                for key in self.movingDir:
                    if self.movingDir[key]:
                        self.anim_objs[key].blit(screen, (x, y))


        else:
            self.move_conductor.stop()

            for key in self.movingDir:
                    if self.movingDir[key]:
                        screen.blit(self.anim_objs['standing'].getFrame(self.standingDirs[key]), (x, y))





