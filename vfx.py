from support import import_folder
from config import player_real_size
from game_data import folder_animations
import pygame as pg


class Dust(pg.sprite.Sprite):
	def __init__(self, pos, type, flip=False):
		super().__init__()
		self.frame_index = 0
		self.animation_speed = 20
		path = folder_animations[type]
		self.frames = import_folder(path)
		self.image = self.frames[self.frame_index]
		self.rect = self.image.get_rect(midbottom=pos)
		self.type = type
		self.flip = flip
		# (14, 10) x 2.5
		self.size = 35, 25
		self.pos = pg.math.Vector2()

	def animate(self, dt):
		self.frame_index += self.animation_speed * dt
		if self.frame_index >= len(self.frames):
			if self.type in 'jump land':  # these only run once
				self.kill()
			else:  # if type is run
				self.frame_index = 0  # keeps going
		else:
			frame = self.frames[int(self.frame_index)]
			frame = pg.transform.scale(frame, self.size)
			frame = pg.transform.flip(frame, self.flip, False).convert_alpha()
			self.image = frame
			self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
			self.pos = pg.math.Vector2(self.rect.midbottom)

	def update(self, shift, opt_pos, flip, dt):
		self.animate(dt)
		self.flip = flip
		self.pos.x += shift[0]
		self.pos.y += shift[1]
		self.rect.midbottom = self.pos
		if self.type == 'run':
			self.rect.midbottom = opt_pos
			if self.flip:  # left
				self.rect.x += player_real_size[0] * 3 / 4
			else:  # right
				self.rect.x -= player_real_size[0] * 3 / 4


class Shockwave:
	def __init__(self, pos, radius, delta_radius, delta_thickness, color, display):
		self.pos = pg.Vector2(pos)
		self.radius = radius
		self.delta_radius = delta_radius
		self.delta_thickness = delta_thickness
		self.color = color
		self.display = display

		self.thickness = self.radius / 2
		self.thickness_int = int(self.thickness)
		self.radius_int = int(self.radius)
		self.alive = True

	def update(self, shift):
		pg.draw.circle(self.display, self.color, self.pos, self.radius_int, self.thickness_int)

		self.thickness -= self.delta_thickness
		self.radius += self.delta_radius
		self.thickness_int = int(self.thickness)
		self.radius_int = int(self.radius)
		self.pos.x += shift[0]
		self.pos.y += shift[1]

		if self.thickness <= 1:
			self.alive = False


class Splash:
	def __init__(self, pos, speed, radius, color, display_surface, gravity=True):
		self.pos = pg.Vector2(pos)
		self.speed = pg.Vector2(speed)
		self.radius = radius
		self.color = color
		self.display_surface = display_surface
		self.WIDTH, self.HEIGHT = display_surface.get_size()
		self.gravity = gravity
		self.alive = True

	def update(self, shift):
		if self.pos.x < self.WIDTH and self.pos.x + 2 * self.radius > 0 and \
				self.pos.y < self.HEIGHT and self.pos.y + 2 * self.radius > 0:
			pg.draw.circle(self.display_surface, self.color, [int(self.pos.x), int(self.pos.y)], self.radius)
		self.pos.x += self.speed.x + shift[0]
		self.pos.y += self.speed.y + shift[1]

		if self.gravity:
			self.speed.y += 0.3
		self.radius -= 0.25
		if self.radius <= 0:
			self.alive = False


class Transition:
	def __init__(self, pos, display_surface):
		self.pos = pg.Vector2(pos)
		self.display_surface = display_surface

		self.radius = abs(display_surface.get_width() - self.pos.x)
		self.inner_radius = 10
		self.alive = True

	def animate(self, dt):
		pg.draw.circle(self.display_surface, 'black', self.pos, self.radius, self.inner_radius)

		self.inner_radius += 100
		print(self.radius, self.inner_radius, self.alive)
		if self.inner_radius >= self.radius:
			self.alive = False
