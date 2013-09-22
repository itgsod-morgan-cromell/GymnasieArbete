import game.game
import game.gfx.animate

class Projectile(Entity):

	def __init__(self, x, y, direction, typeOf, flyTime, speed, damage):
		self.x = x
		self.y = y
		self.vector = direction
		self.typeOf = typeOf
		self.maxFlyTime = flyTime
		self.flyTime = 0
		self.speed = speed
		self.damage = damage
		self.alive = True
		rect = pygame.Rect(0, 0, data.width, data.height)

	def update(self):
		pass
		if maxFlyTime == self.flyTime:
			self.kill

		if self.alive?:
			self.flyTime += 1



	def render(self):
		pass


	def alive?(self):
		return alive

	def kill:
		self.alive = False