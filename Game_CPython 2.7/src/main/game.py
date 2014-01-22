import pygame
from src.gui.menu import Menu
from src.level.world import World
from src.main.gameclock import GameClock
from src.gui.guihandler import GuiHandler
import sys
from src.util.get_sprite import *
from src.main.eventmanager import EventManager
from src.profilehooks import profile


class Game(object):

    '''
    Main core of the main.
    '''

    def __init__(self):
        pygame.init()
        get_item_sprite('test', 0)
        self.event_manager = EventManager()
        self.WIDTH = 30 * 32
        self.HEIGHT = 20 * 32
        self.MENU_WIDTH = 10 * 32
        self.CONSOLE_HEIGHT = 6 * 32
        self.SCALE = 1
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT), pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.HWACCEL)
        self.world_screen = pygame.Surface((self.WIDTH - self.MENU_WIDTH, self.HEIGHT - self.CONSOLE_HEIGHT))
        self.clock = GameClock(40)
        self.camera = self.world_screen.get_rect().copy()
        self.events = None
        self.menu = Menu((self.screen.get_width()/2, self.screen.get_height()/2), ['New Game', 'Load Game', 'Quit'])

    def new_game(self, player):
        self.screen.blit(pygame.image.load('res/gui/loading_screen.png'), (self.WIDTH/2 - 110, self.HEIGHT/2 - 17))
        pygame.display.flip()
        self.world = World(player)
        self.world.update(self.camera)
        self.ui = GuiHandler(self.world, self.world_screen)


    def run(self):
        """
        Handles the looping of the main with a clock that follows a set amount of ticks per second.
        Also prints out the current fps, ups and polls the latest inputs.
        """
        while True:
            pygame.display.set_caption("FPS: {0},  UPS: {1}".format(self.clock.get_fps(), self.clock.get_ups()))
            dt = self.clock.tick()
            if self.clock.update_ready:
                self.event_manager.update()
                self.events = self.event_manager.events
                for event in self.events:
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            if not self.menu.main:
                                self.menu.active = not self.menu.active
                    elif event.type == pygame.VIDEORESIZE:
                        self.WIDTH, self.HEIGHT = event.dict['size']
                        self.WIDTH = int(self.WIDTH/64)*64
                        self.HEIGHT = int(self.HEIGHT/64)*64
                        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT), pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.HWACCEL | pygame.RESIZABLE)
                        self.world_screen = pygame.Surface((self.WIDTH - self.MENU_WIDTH, self.HEIGHT))
                        self.clock = GameClock(40)
                        self.camera = pygame.Rect(0, 0, self.WIDTH - self.MENU_WIDTH, self.HEIGHT)
                        self.ui = GuiHandler(self.world)

                if self.menu.active:
                    self.menu.update(self, self.events)
                else:
                    self.update()

            if self.clock.frame_ready:
                if self.menu.active:
                    self.menu.draw(self.screen)
                else:
                    self.draw()
                pygame.display.flip()

    def update(self):
        '''
        Main update loop.
        '''

        self.world.update(self.camera)
        self.camera.centerx = int(self.world.player.x)*32
        self.camera.centery = int(self.world.player.y)*32
        if self.camera.x < 0:
            self.camera.x = 0
        if self.camera.x + self.camera.w > self.world.map.dungeon.width:
            self.camera.x = self.world.map.dungeon.width - self.camera.w
        if self.camera.y < 0:
            self.camera.y = 0
        if self.camera.y + self.camera.h > self.world.map.dungeon.height:
            self.camera.y = self.world.map.dungeon.height - self.camera.h

        self.ui.update(self.world, self.camera)

    def draw(self):
        '''
        Main draw loop.
        '''
        self.screen.fill((0, 0, 0))
        self.world.draw(self.world_screen, self.camera)
        self.screen.blit(self.world_screen, (0, 0))
        self.ui.draw(self.screen, self.camera)
