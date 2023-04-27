import pygame as pg
from config import tile_size, vertical_tile_number
from sprite_sheet import SpriteSheet
from support import import_cut_graphics, import_folder
from game_data import png_graphics, spritesheet_animations, audio_paths


# region parent classes
class Tile(pg.sprite.Sprite):
	def __init__(self, pos, size):
		super().__init__()
		self.image = pg.Surface(size)
		self.rect = self.image.get_rect(topleft=pos)
		self.image.set_colorkey('white')
		self.pos = pg.math.Vector2(self.rect.topleft)

	def update(self, shift):
		# scroll the tile
		self.pos.x += shift[0]
		self.pos.y += shift[1]
		self.rect.topleft = self.pos


class StaticTile(Tile):
	def __init__(self, pos, size, surface):
		super().__init__(pos, size)
		self.image = surface
		self.image.set_colorkey('white')


class AnimatedTile(Tile):
	def __init__(self, pos, width, height, scale, path, bg_color):
		super().__init__(pos, (width, height))
		self.size = (width, height)
		self.frame_index = 0
		self.get_animation(path, width, height, scale, bg_color)
		self.animation_speed = 9
		self.bg_color = bg_color

	def get_animation(self, path, width, height, scale, bg_color):
		self.frames = SpriteSheet(path, width, height, scale, bg_color).import_animation_list()
		self.image = self.frames[self.frame_index]

	def animate(self, dt):
		self.frame_index += self.animation_speed * dt
		if self.frame_index >= len(self.frames):
			self.frame_index = 0

		self.image = self.frames[int(self.frame_index)]

	def update(self, shift, dt):
		self.animate(dt)
		self.image.set_colorkey(self.bg_color)
		self.pos.x += shift[0]
		self.pos.y += shift[1]
		self.rect.topleft = self.pos


# endregion

class Border(Tile):
	def __init__(self, pos, size):
		super().__init__(pos, size)
		self.image.set_colorkey('black')


class BackgroundTile(StaticTile):
	def __init__(self, pos, size, surface):
		super().__init__(pos, size, surface)
		self.parallax_index = 0.7

	def update(self, shift):
		# scroll the tile
		self.pos.x += shift[0] * self.parallax_index
		self.pos.y += shift[1] * self.parallax_index
		self.rect.topleft = self.pos


class Door(StaticTile):
	def __init__(self, pos, size, surface):
		super().__init__(pos, size, surface)
		self.image = surface
		self.image.set_colorkey('white')
		self.type = 'door'


class Lava(AnimatedTile):
	def __init__(self, pos, width, height, scale, path):
		self.bg_color = 'white'
		super().__init__(pos, width, height, scale, path, self.bg_color)
		self.animation_speed = 6
		self.parallax_index = 0.9

	def update(self, shift, dt):
		self.animate(dt)
		self.image.set_colorkey(self.bg_color)
		self.pos.x += shift[0] * self.parallax_index
		self.pos.y += shift[1] * self.parallax_index
		self.rect.topleft = self.pos


class Fire(AnimatedTile):
	def __init__(self, pos, width, height, scale, path):
		self.path = path
		self.size = (width, height)
		self.type = 'fire'
		self.bg_color = 'black'
		super().__init__(pos, width, height, scale, path, self.bg_color)


class Coin(AnimatedTile):
	def __init__(self, pos, width, height, scale, path):
		self.path = path
		self.size = (width, height)
		self.scale = scale
		self.collected = False
		self.hitbox = pg.Rect(0, 0, 34, 34)
		self.bg_color = 'white'
		self.collect_sound = pg.mixer.Sound(audio_paths['coin']['collect'])
		super().__init__(pos, width, height, scale, path, self.bg_color)

	def animate(self, dt):
		self.frame_index += self.animation_speed * dt
		if self.frame_index >= len(self.frames):
			if self.collected:
				self.kill()
			self.frame_index = 0

		self.image = self.frames[int(self.frame_index)]

	def collect(self, sounds_on):
		self.path = spritesheet_animations['collect']
		self.frames = SpriteSheet(self.path, *self.size, self.scale, self.bg_color).import_animation_list()
		self.collected = True
		self.frame_index = 0
		self.animation_speed = 9
		self.image = self.frames[self.frame_index]
		if sounds_on:
			self.collect_sound.play()

	def update(self, shift, dt):
		self.animate(dt)
		self.image.set_colorkey(self.bg_color)
		self.pos.x += shift[0]
		self.pos.y += shift[1]
		self.rect.topleft = self.pos
		self.hitbox.center = self.rect.center


class Torch(AnimatedTile):
	def __init__(self, pos, width, height, scale, path):
		self.path = path
		self.size = (width, height)
		self.bg_color = 'white'
		self.parallax_index = 0.7
		super().__init__(pos, width, height, scale, path, self.bg_color)

	def update(self, shift, dt):
		# scroll the tile
		self.animate(dt)
		self.pos.x += shift[0] * self.parallax_index
		self.pos.y += shift[1] * self.parallax_index
		self.rect.topleft = self.pos
