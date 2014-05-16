import sys

import pygame
from src.gui.console import Console

from src.gui.menu import Menu
from src.level.world import World
from src.main.gameclock import GameClock
from src.gui.guihandler import GuiHandler
from src.gui.tooltip import Tooltip
from src.util.get_sprite import *
from src.event_manager import EventManager
from src.options import *
from src.event_helper import *




class Game(object):
    '''
    Main core of the main.
    '''

    def __init__(self):
        pygame.init()
        get_item_sprite('test', 0)
        self.event_manager = EventManager()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.HWACCEL)
        self.world_screen = pygame.Surface((WIDTH - MENU_WIDTH, HEIGHT - CONSOLE_HEIGHT))
        self.clock = GameClock(40)
        self.camera = self.world_screen.get_rect().copy()
        self.events = None
        self.menu = Menu()
        register_handler(MENU_NEW_GAME, self.new_game)

    def new_game(self, event):
        player = {'name': 'Test', 'class': 'warrior'}
        self.screen.blit(pygame.image.load('../res/gui/loading_screen.png'), (WIDTH / 2 - 110, HEIGHT / 2 - 17))
        pygame.display.flip()
        self.world = World(player)
        self.world.update()
        self.ui = GuiHandler(self.world)
        self.console = Console()
        self.tooltip = Tooltip(self.world)

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
                if not self.menu.active:
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

        self.world.update()
        self.camera.centerx = int(self.world.player.x) * 32
        self.camera.centery = int(self.world.player.y) * 32
        if self.camera.x < 0:
            self.camera.x = 0
        if self.camera.x + self.camera.w > self.world.map.width:
            self.camera.x = self.world.map.width - self.camera.w
        if self.camera.y < 0:
            self.camera.y = 0
        if self.camera.y + self.camera.h > self.world.map.height:
            self.camera.y = self.world.map.height - self.camera.h

        self.ui.update()
        self.tooltip.update(self.world, self.camera)

    def draw(self):
        '''
        Main draw loop.
        '''
        self.screen.fill((0, 0, 0))
        self.world.draw(self.world_screen, self.camera)
        self.screen.blit(self.world_screen, (0, 0))
        self.ui.draw(self.screen)
        self.console.draw(self.screen)
        self.tooltip.draw(self.screen)
