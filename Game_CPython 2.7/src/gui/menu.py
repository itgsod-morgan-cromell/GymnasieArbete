import sys
from src.gui.gui import Gui
import pygame
from src.gui.textrect import render_textrect


class MenuItem(object):
    def __init__(self, rect, data):
        self.rect = rect
        self.active = False
        self.data = data
        self.image = render_textrect(str(self.data), 30, self.rect, (255, 255, 255))
        self.active_image = render_textrect(str(self.data), 30, self.rect, (0, 255, 0))


class Menu(Gui):
    def __init__(self, middle, options):
        self.options = options
        width = 15 * len(max(options, key=len))
        height = 30*len(options)
        image = pygame.Surface((width, height))
        self.rect = pygame.Rect((middle[0] - width/2, middle[1] - height/2), (width, height))
        self.items = []
        Gui.__init__(self, 'menu', (self.rect.x, self.rect.y), image, True)

        for key, option in enumerate(self.options):
            rect = pygame.Rect((0, 0 + (30 * key)), (15*len(option), 30))
            self.items.append(MenuItem(rect, option))

    def update(self, game):
        for item in self.items:
            if item.rect.collidepoint(pygame.mouse.get_pos()[0] - self.x, pygame.mouse.get_pos()[1] - self.y):
                item.active = True
                if pygame.mouse.get_pressed()[0]:
                    if item.data == 'New Game':
                        game.new_game()
                    if item.data == 'Quit':
                        pygame.quit()
                        sys.exit()
                    self.active = False
            else:
                item.active = False

    def draw(self, screen):
        for item in self.items:
            if item.active:
                self.image.blit(item.active_image, (item.rect.x, item.rect.y))
            else:
                self.image.blit(item.image, (item.rect.x, item.rect.y))
        screen.blit(self.image, (self.x, self.y))