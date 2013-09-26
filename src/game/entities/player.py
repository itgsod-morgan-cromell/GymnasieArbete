import pygame
import game.game
import game.gfx.animate
from .mob import Mob
import random

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
        super(Player, self).__init__(game.game.world, data.type, x, y, speed, rect)
        self.standing = {}
        self.standing['UP'] = pygame.image.load('../res/sprites/player/crono_back.gif')
        self.standing['DOWN'] = pygame.image.load('../res/sprites/player/crono_front.gif')
        self.standing['LEFT'] = pygame.image.load('../res/sprites/player/crono_left.gif')
        self.standing['RIGHT'] = pygame.transform.flip(self.standing['LEFT'], True, False)

        anim_types = 'back_run back_walk front_run front_walk left_run left_walk'.split()
        self.anim_objs = {}
        for anim_type in anim_types:
            images_and_duration = [('../res/sprites/player/crono_%s.%s.gif' % (anim_type, str(num).rjust(3, '0')), 0.1) for num in range(6)]
            self.anim_objs[anim_type] = game.gfx.animate.PygAnimation(images_and_duration)

        # create the right-facing sprites by copying and flipping the left-facing sprites
        self.anim_objs['left_walk'] = game.gfx.animate.PygAnimation([('../res/sprites/dummy/walk_top.png', 1, 6, 1)])
        self.anim_objs['right_walk'] = self.anim_objs['left_walk'].getCopy()
        self.anim_objs['right_walk'].flip(True, False)
        self.anim_objs['right_walk'].makeTransformsPermanent()
        self.anim_objs['right_run'] = self.anim_objs['left_run'].getCopy()
        self.anim_objs['right_run'].flip(True, False)
        self.anim_objs['right_run'].makeTransformsPermanent()

        self.move_conductor = game.gfx.animate.PygConductor(self.anim_objs)
        self.spriteRect = self.anim_objs['right_run'].getRect()

        self.centerX = self.x + self.spriteRect.x + self.spriteRect.w/2
        self.centerY = self.y + self.spriteRect.y + self.spriteRect.h/2
        self.time = 30
        self.targetX = 0
        self.targetY = 0

    def update(self):

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
        if input.GetControl('RUN'):
            self.running = True
            self.speed *= 1.3
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

        self.rect.x = self.x + self.data.spriteOffsetX
        self.rect.y = self.y + self.data.spriteOffsetY
        game.game.camera.center = self.rect.center
        self.centerX = self.rect.center[0]
        self.centerY = self.rect.center[1] - self.spriteRect.h/2

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
            self.x = target.x + target.width/2 - self.rect.w/2 - self.data.spriteOffsetX
            self.y = target.y + target.height/2 - self.rect.h/2 - self.data.spriteOffsetY
            if target.spawn_position == "n":
                self.y -= target.height/2 + 10
            elif target.spawn_position == "s":
                self.y += target.height/2 + 10
            elif target.spawn_position == "w":
                self.x -= target.width/2 + 10
            elif target.spawn_position == "e":
                self.x += target.width/2 + 10


    def render(self):
        screen = game.game.screen
        x = self.x - game.game.camera.x
        y = self.y - game.game.camera.y
        if game.game.debug:
            screen.fill((255, 0, 0), pygame.Rect(x + self.data.spriteOffsetX, y + self.data.spriteOffsetY, self.rect.w, self.rect.h))


            # TODO: This code is so messy. Clean it up and add a standardized 8-directional animation system that the mob class could use.
        if self.isMoving:
            self.move_conductor.play()
            if not self.running:

                if self.movingDir['UP']:
                    self.anim_objs['back_walk'].blit(screen, (x, y))
                elif self.movingDir['DOWN']:
                    self.anim_objs['front_walk'].blit(screen, (x, y))
                elif self.movingDir['LEFT']:
                    self.anim_objs['left_walk'].blit(screen, (x, y))
                elif self.movingDir['RIGHT']:
                    self.anim_objs['right_walk'].blit(screen, (x, y))

            else:
                if self.movingDir['UP']:
                    self.anim_objs['back_run'].blit(screen, (x, y))
                elif self.movingDir['DOWN']:
                    self.anim_objs['front_run'].blit(screen, (x, y))
                elif self.movingDir['LEFT']:
                    self.anim_objs['left_run'].blit(screen, (x, y))
                elif self.movingDir['RIGHT']:
                    self.anim_objs['right_run'].blit(screen, (x, y))


        else:
            self.move_conductor.stop()
            for key in self.movingDir:
                if self.movingDir[key]:
                    screen.blit(self.standing[key], (x, y))








