import pygame
from src.level.world import World
from src.main.gameclock import GameClock
from src.gui.guihandler import GuiHandler
import sys
from src.profilehooks import profile


class Game(object):

    '''
    Main core of the main.
    '''

    def __init__(self):
        pygame.init()
        self.WIDTH = 30 * 32
        self.HEIGHT = 22 * 32
        self.SCALE = 1
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT), pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.world_screen = pygame.Surface((self.WIDTH - 250, self.HEIGHT))
        self.clock = GameClock(60)
        self.camera = pygame.Rect(0, 0, self.WIDTH - 250, self.HEIGHT)
        self.world = World()
        self.events = pygame.event.get()
        self.world.update(self.events, self.camera, (pygame.mouse.get_pos()[0]/32, pygame.mouse.get_pos()[1]/32))
        self.ui = GuiHandler(self.world)



    def run(self):
        """
        Handles the looping of the main with a clock that follows a set amount of ticks per second.
        Also prints out the current fps, ups and polls the latest inputs.
        """
        while True:
            pygame.display.set_caption("FPS: {0},  UPS: {1}".format(self.clock.get_fps(), self.clock.get_ups()))
            dt = self.clock.tick()
            if self.clock.update_ready:
                self.update(dt)

            if self.clock.frame_ready:
                self.draw(dt)

    def update(self, dt):
        '''
        Main update loop.
        '''

        self.events = pygame.event.get()

        keys = pygame.key.get_pressed()
        for event in self.events:
            if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                pygame.quit()
                sys.exit()
        mouse = (pygame.mouse.get_pos()[0]/32, pygame.mouse.get_pos()[1]/32)
        self.world.update(self.events, self.camera, mouse)
        self.camera.centerx = int(self.world.player.x)*32 + 3
        self.camera.centery = int(self.world.player.y)*32
        if self.camera.x < 0:
            self.camera.x = 0
        if self.camera.x + self.camera.w > self.world.map.dungeon.width:
            self.camera.x = self.world.map.dungeon.width - self.camera.w + 6
        if self.camera.y < 0:
            self.camera.y = 0
        if self.camera.y + self.camera.h > self.world.map.dungeon.height:
            self.camera.y = self.world.map.dungeon.height - self.camera.h

        self.ui.update(self.world, self.camera, mouse, self.events)



    def draw(self, dt):
        '''
        Main draw loop.
        '''
        self.screen.fill((0, 0, 0))
        self.world.draw(self.world_screen, self.camera)
        self.screen.blit(self.world_screen, (0, 0))
        self.ui.draw(self.screen, self.camera)
        pygame.display.flip()
