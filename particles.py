from support import import_folder
from config import player_frame_size, player_real_size
from game_data import folder_animations
import pygame as pg

class ParticleEffect(pg.sprite.Sprite):
	def __init__(self, pos, type, flip=False):
		super().__init__()
		self.frame_index = 0
		self.animation_speed = 30
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
		# self.rect.midbottom = self.pos
