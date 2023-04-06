import pygame as pg

class Button(pg.sprite.Sprite):
	def __init__(self, unhovered_image, hovered_image, pos, text_input, font, display_surface):
		super().__init__()
		self.display_surface = display_surface
		self.hovered_image = hovered_image
		self.unhovered_image = unhovered_image
		self.unhovered_image.set_colorkey('black')
		self.hovered_image.set_colorkey('black')
		self.image_rect = self.hovered_image.get_rect()

		self.image = pg.Surface(self.image_rect.size)
		self.image.set_colorkey('white')
		self.pos = pos
		self.rect = self.image.get_rect(center=pos)

		self.text_input = text_input
		if text_input:
			self.text_input = text_input
			self.font = font

			self.text = self.font.render(self.text_input, True, 'black')
			self.text_rect = self.text.get_rect()
			self.text_pos = ((self.rect.w-self.text_rect.w)/2, (self.rect.h-self.text_rect.h)/2)

		self.hovered = False
		self.pressed = False

	def press(self):
		self.pressed = True

	def check_hover(self, mouse_pos):
		if self.rect.left <= mouse_pos[0] <= self.rect.right and self.rect.top <= mouse_pos[1] <= self.rect.bottom:
			self.hovered = True
			self.image.blit(self.hovered_image, (0, 0))
		else:
			self.hovered = False
			self.image.blit(self.unhovered_image, (0, 0))

	def update(self, mouse_down, mouse_position):
		self.check_hover(mouse_position)
		if self.hovered and mouse_down:
			self.pressed = True
		else:
			self.pressed = False

		if self.text_input:
			self.image.blit(self.text, self.text_pos)

