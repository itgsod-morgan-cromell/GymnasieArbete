
import pygame
from pygame.locals import *
from level.level import Level


class Game(object):
    def __init__(self):
        WIDTH = 640
        HEIGHT = WIDTH / 16 * 9
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.camera = pygame.Rect(0, 0, WIDTH, HEIGHT)
        self.clock = pygame.time.Clock()
        self.level = Level('../../res/desert.tmx')


    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

            # Calling the rendering and tick methods
            self.tick()
            self.render()
            self.clock.tick(60)

    def tick(self):
        pass

    def set_resolution(self, width, aspect):
        pass
        # TODO: Find out how to modify the surface size and resolution of the surface.

    def render(self):
        """
        The render method first draws everything on the buffer.
        After the buffer is completed we draw what is on the buffer to the screen with the help of screen.display.flip().
        This results in a flicker-free animations and much nicer rendering.

        """
        self.level.render(self.screen, self.camera)
        pygame.display.flip()

game = Game()
game.run()