import pygame as pg
from game_data import png_graphics
from pygame.math import Vector2


class TextLabel(pg.sprite.Sprite):
	def __init__(self, text, font, pos):
		super().__init__()
		self.text_color = (255, 255, 255)
		self.text = text
		self.font = font
		self.label = font.render(text, True, self.text_color)
		self.image = pg.Surface(self.label.get_size(), flags=pg.SRCALPHA)
		self.rect = self.image.get_rect(center=pos)
		self.pos = Vector2(pos)
		self.image.blit(self.label, (0, 0))

	def update_text(self, text):
		self.text_color = (255, 255, 255)
		self.text = text
		self.label = self.font.render(text, True, self.text_color)
		self.image = pg.Surface(self.label.get_size(), flags=pg.SRCALPHA)
		self.rect = self.image.get_rect(center=self.pos)
		self.image.blit(self.label, (0, 0))


class Indicator:
	def __init__(self, font, pos, text, type):
		if type == 'up':
			color = '#42ce29'  # greenish
		elif type == 'down':
			color = '#ad150a'  # redish
		self.text = text
		self.text_surface = font.render(text, True, color)
		self.alpha = 255
		self.pos = Vector2(pos)
		self.starting_y = self.pos.y
		self.alive = True

	def animate_indicator(self, dt):
		if self.alive:
			self.text_surface.set_alpha(self.alpha)
			self.alpha -= 300 * dt
			self.pos.y -= 180 * dt
			if self.alpha < 50 or self.starting_y - self.pos.y >= 125:
				self.alive = False


class UI:
	def __init__(self, screen, current_health, big_font, button_font):
		self.display_surface = screen
		self.font_big = big_font
		self.font_small = button_font

		# coin
		self.coin_icon = pg.image.load(png_graphics['coins']).convert_alpha()
		self.coin_icon = pg.transform.scale(self.coin_icon, (120, 120))
		self.coin_pos = (30, -5)

		# health bar
		self.health_bar = pg.image.load(png_graphics['healthbar']).convert_alpha()
		self.health_bar = pg.transform.scale(self.health_bar, (228, 89))
		self.bar_pos = (65, 90)
		self.bar_max_width = 180
		self.bar_height = 7
		self.current_health = current_health

		self.indicators = []

	def create_indicator(self, pos, gained_health):
		if gained_health > 0:
			indicator = Indicator(self.font_small, pos, f'+{gained_health}', 'up')
		if gained_health < 0:
			indicator = Indicator(self.font_small, pos, f'{gained_health}', 'down')
		self.indicators.append(indicator)

	def display_health(self, health):
		self.display_surface.blit(self.health_bar, self.bar_pos)  # display the health bar
		health_ratio = health / 100

		if health_ratio > 1:
			health_ratio = 1

		current_bar_width = self.bar_max_width * health_ratio
		health_bar_rect = pg.Rect((105, 130), (current_bar_width, self.bar_height))  # fill up the health bar
		pg.draw.rect(self.display_surface, (250, 10, 15), health_bar_rect, 0)

	def display_coins(self, coins):
		self.coin_icon.set_colorkey('black')
		self.display_surface.blit(self.coin_icon, self.coin_pos)

		coin_counter = self.font_big.render(str(coins), True, (230, 230, 230))  # dislay coin counter
		self.display_surface.blit(coin_counter, (150, 30))

	def draw(self, coins, health, dt):
		for i, indicator in sorted(enumerate(self.indicators), reverse=True):
			self.display_surface.blit(indicator.text_surface, indicator.pos)
			indicator.animate_indicator(dt)
			if not indicator.alive:
				self.indicators.pop(i)

		self.display_coins(coins)
		self.display_health(health)
