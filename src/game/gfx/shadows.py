import pygame
import PAdLib.occluder as occluder
import PAdLib.shadow as shadow
import game.game
from random import randint


class Lighting(object):
    def __init__(self):

        self.surf_lighting = pygame.Surface((game.game.camera.w, game.game.camera.h))
        self.shad = shadow.Shadow()

        self.shad.set_radius(100.0)
        self.surf_falloff = pygame.image.load("../res/light_falloff100.png").convert()


    def update(self):
        randsize = randint(0, 2)
        self.shad.set_radius(100.0 + randsize)
        occluders = game.game.world.get_solids([], game.game.camera)
        self.shad.set_occluders(occluders)
        self.shad.set_light_position((game.game.player.centerX - game.game.camera.x, game.game.player.centerY - game.game.camera.y))
        mask, draw_pos = self.shad.get_mask_and_position(False)
        surf_falloff = pygame.transform.scale(self.surf_falloff, (self.surf_falloff.get_width() + 10, self.surf_falloff.get_height() + 10))
        mask.blit(surf_falloff, (0,0),special_flags=pygame.BLEND_MULT)
        self.surf_lighting.fill((25,25,25))
        self.surf_lighting.blit(mask, draw_pos, special_flags=pygame.BLEND_MAX)

    def draw(self):
        game.game.screen.blit(self.surf_lighting, (0,0), special_flags=pygame.BLEND_MULT)
