import pygame
import game.game
import PAdLib.particles as particles


class Particle(object):
    def __init__(self):
        global surf_lighting
        self.particle_system = particles.ParticleSystem()
        self.particle_system.set_particle_acceleration([0.0,500.0])
        self.emitters = []
        self.surface = pygame.Surface((game.game.camera.w/2, game.game.camera.h/2))

    def update(self, dt):
        self.emitters[0].set_position([game.game.player.x, game.game.player.y])
        self.particle_system.update(dt)
    def addEmitter(self):
        emitter = particles.Emitter()
        emitter.set_density(1000)
        emitter.set_angle(0.0, 360.0)
        emitter.set_speed([150.0,350.0])
        emitter.set_life([0.5, 1.0])
        emitter.set_colors([(255,0,0),(255,255,0),(0,255,0),(0,255,255),(0,0,255),(0,0,0)])
        self.emitters.append(emitter)
        self.particle_system.add_emitter(emitter, 'test')




    def render(self):
        self.particle_system.draw(self.surface)