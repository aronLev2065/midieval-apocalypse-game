import pygame as pg

class SpriteSheet:
	def __init__(self, path, width, height, scale, color):
		super().__init__()
		self.image = pg.image.load(path)
		self.rect = self.image.get_rect()
		self.width = width
		self.height = height
		self.scale = scale
		self.bg_color = color

	def get_image(self, frame_index):
		# get a single frame from a spritesheet based on given parameters
		offset = (frame_index * self.width, 0)
		image = pg.Surface((self.width, self.height)).convert_alpha()
		image.blit(self.image, (0, 0), (*offset, self.width, self.height))
		image = pg.transform.scale(image, self.scale)
		image.set_colorkey(self.bg_color)

		return image

	def import_animation_list(self):
		frame_number = self.image.get_width() // self.width
		frames = []
		for frame in range(frame_number):
			frames.append(self.get_image(frame))

		return frames