import pygame as pg
from game_data import spritesheet_animations
from sprite_sheet import SpriteSheet
from pygame.math import Vector2

class Indicator:
	def __init__(self, font, pos, text, type):
		if type == 'up':
			color = (66, 206, 41)  # greenish
		elif type == 'down':
			color = (173, 21, 10)  # redish
		self.text_surface = font.render(text, True, color)
		self.alpha = 255
		self.pos = Vector2(pos)
		self.done = False

	def animate_indicator(self, dt):
		if not self.done:
			self.text_surface.set_alpha(self.alpha)
			self.alpha -= 5
			self.pos.y -= 180 * dt
			if self.alpha < 50:
				self.done = True


class UI:
	def __init__(self, screen, current_health, big_font, button_font):
		self.display_surface = screen
		self.font_big = big_font
		self.font_small = button_font

		# coin
		self.coin_icon = pg.image.load('assets/tile assets/tiles/coin.png').convert_alpha()
		self.coin_icon = pg.transform.scale(self.coin_icon, (120, 120))
		self.coin_pos = (30, -5)

		# health bar
		self.health_bar = pg.image.load('assets/ui/health_bar.png').convert_alpha()
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
		self.change_health(gained_health)

	def change_health(self, health):
		self.current_health += health
		if self.current_health < 0:
			self.current_health = 0
		if self.current_health > 100:
			self.current_health = 100

	def display_health(self, health):
		self.display_surface.blit(self.health_bar, self.bar_pos)
		current_health_ratio = health / 100

		if current_health_ratio > 1:
			current_health_ratio = 1

		current_bar_width = self.bar_max_width * current_health_ratio
		health_bar_rect = pg.Rect((105, 130), (current_bar_width, self.bar_height))
		pg.draw.rect(self.display_surface, (250, 10, 15), health_bar_rect, 0)

	def display_coins(self, coins):
		self.coin_icon.set_colorkey('black')
		self.display_surface.blit(self.coin_icon, self.coin_pos)

		coin_counter = self.font_big.render(str(coins), True, (230, 230, 230))  # dislay coin counter
		self.display_surface.blit(coin_counter, (150, 30))

	def draw(self, coins, health, dt):
		for indicator in self.indicators:
			self.display_surface.blit(indicator.text_surface, indicator.pos)
			indicator.animate_indicator(dt)
			if indicator.done:
				self.indicators.remove(indicator)

		self.display_coins(coins)
		self.display_health(health)
