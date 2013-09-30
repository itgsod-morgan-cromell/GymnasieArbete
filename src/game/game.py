'''

This is the main game class where everything is happening. From here we call to all other functions that the game needs.

'''


import pygame
from pygame.locals import *
from . import gameclock
from .level import level
from .gfx import shadows, particles
from profilehooks import profile
from . import input_handler


pygame.init()

'''
These are the global variables that we use among the other classes.

'''

world = None
player = None
mapdata = {}
screen = None
input = input_handler.Input()
camera = None
debug = False # Dev testing feature. Press X to enter debug mode.
minimap_scale = 8
player = None
clock = gameclock.GameClock(60)
game = None
lighting = None


class Game(object):
    def __init__(self):
        global world, player, mapdata, screen, camera, clock, game, lighting
        self.screen_width = 1024
        self.screen_height = 576
        game_width = 1024
        game_height = 576
        game = self
        screen = pygame.Surface((game_width, game_height))
        self.window = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.HWSURFACE | pygame.DOUBLEBUF)
        camera = pygame.Rect(0, 0, game_width, game_height)
        lighting = shadows.Lighting()
        world = level.Level("../res/maps/level_1/level_1.tmx")
        self.font = pygame.font.Font('../res/gothic.ttf', 15)

        pygame.mixer.init()
        pygame.mixer.music.load("../res/test.ogg")
        #pygame.mixer.music.play()
    def run(self):
        while True:
            input.Poll()
            global debug, world
            if input.GetControl('QUIT'):
                pygame.quit()
                return

            if input.GetControl('DEBUG'):
                debug = not debug
            if input.GetControl('RELOAD'):
                world = level.Level(world.current_path)




            # Calling the rendering and update methods

            pygame.display.set_caption("FPS: " + str(clock.get_fps()) + " UPS: " + str(clock.get_ups()))
            dt = clock.tick()
            if clock.update_ready:
                self.update(dt)
            if clock.frame_ready:
                self.render()

    def update(self, dt):
        '''
        Main update loop. This is where we call every object that needs to update. Most of the objects are found in the world object where the entities
        are being loaded and updated.
        We also readjust the camera here to make sure it does not step out of map bounds.
        '''

        world.updateEntity()
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
       # lighting.update()


    def set_resolution(self, width, aspect):
        pass
        # TODO: Find out how to modify the surface size and resolution of the surface.

    def render(self):
        """
        The main render methods tell the world to draw every visible entity to the buffer surface.
        We then draw the buffered surface to the screen.

        """
        screen.fill((50,33,37))
        world.render_background()
        world.render()
      #  lighting.render()
        if debug:
            screen.fill((0,0,0), pygame.Rect(camera.w - 130, 40, 150, 180))
            self.text("--- DEBUG ---", (camera.w - 120, 60))
            self.text("MAP: " + world.name, (camera.w - 120, 80))
            self.text("FPS: " + str(clock.get_fps()), (camera.w - 120, 100))
            self.text("UPS: " + str(clock.get_ups()), (camera.w - 120, 120))

        if self.screen_width == camera.w:
            self.window.blit(screen, (0,0))
        else:
            surf = pygame.transform.scale(screen, (self.screen_width, self.screen_height))
            self.window.blit(surf, (0,0))

        pygame.display.update(pygame.Rect(0,0, self.screen_width, self.screen_height))


    def text(self, input, pos):
        text = self.font.render(input, 2, (255,0,0))
        screen.blit(text, pos)
