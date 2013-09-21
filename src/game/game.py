
import sys
import os


import pygame
from pygame.locals import *
import gameclock
import level.level
import gfx.shadows
from profilehooks import profile
import input_handler


pygame.init()
world = None
player = None
mapdata = {}
screen = None
input = input_handler.Input()
camera = None
debug = True
minimap_scale = 8
player = None
clock = gameclock.GameClock(60)
game = None

class Game(object):
    def __init__(self):
        global world, player, mapdata, screen, camera, clock, game
        screen_width = 800
        screen_height = 600

        self.tmap = pygame.threads.tmap
        self.wq = pygame.threads.WorkerQueue(0)
        game = self
        screen = pygame.display.set_mode((screen_width, screen_height), pygame.HWSURFACE | pygame.DOUBLEBUF)
        camera = pygame.Rect(0, 0, screen_width, screen_height)
        world = level.level.Level("../res/maps/level_1/level_1.tmx")
        self.font = pygame.font.Font('../res/gothic.ttf', 15)
        self.lighting = gfx.shadows.Lighting()
        pygame.mixer.init()
        pygame.mixer.music.load("../res/test.ogg")
        #pygame.mixer.music.play()



    @profile
    def run(self):
        while True:
            input.Poll()
            global debug, world
            if input.GetControl('QUIT'):
                pygame.quit()
                return

            if input.GetControl('DEBUG'):

                if debug:
                    debug = False
                else:
                    debug = True
            if input.GetControl('RELOAD'):
                world = level.level.Level(world.current_path)




            # Calling the rendering and update methods

            pygame.display.set_caption("FPS: " + str(clock.get_fps()) + " UPS: " + str(clock.get_ups()))
            self.dt = clock.tick()
            if clock.update_ready:
                self.update()
            if clock.frame_ready:
                self.render()

    def update(self):
        self.tmap(world.updateEntity, mapdata[world.name], worker_queue=self.wq)
        if camera.w < world.map_width:

            if camera.x + camera.w > world.map_width:
                camera.x = world.map_width - camera.w

            if camera.x < 0:
                camera.x = 0
        else:
            camera.x = -(camera.w - world.map_width)/2

        if camera.h < world.map_height:

            if camera.y + camera.h > world.map_height:
                camera.y = world.map_height - camera.h

            if camera.y < 0:
                camera.y = 0
        else:
            camera.y = -(camera.h - world.map_height)/2

        world.update()
        self.lighting.update()


    def set_resolution(self, width, aspect):
        pass
        # TODO: Find out how to modify the surface size and resolution of the surface.

    def render(self):
        """
        The render method first draws everything on the buffer.
        After the buffer is completed we draw what is on the buffer to the screen with the help of screen.display.flip().
        This results in a flicker-free animations and much nicer rendering.

        """
        screen.fill((50,33,37))
        world.render_background()
        world.render()
        self.lighting.draw()

        if debug:
            screen.fill((0,0,0), pygame.Rect(camera.w - 130, 40, 150, 180))
            self.text("--- DEBUG ---", (camera.w - 120, 60))
            self.text("MAP: " + world.name, (camera.w - 120, 80))
            self.text("FPS: " + str(clock.get_fps()), (camera.w - 120, 100))
            self.text("UPS: " + str(clock.get_ups()), (camera.w - 120, 120))
        pygame.display.flip()


    def text(self, input, pos):
        text = self.font.render(input, 2, (255,0,0))
        screen.blit(text, pos)
