import pygame as pg
from level import Level
from config import *
from ui import UI
from button import Button
from tiles import StaticTile

class Game:
	def __init__(self, screen, state):
		# settings
		self.display_surface = screen
		self.WIDTH = screen.get_width()
		self.HEIGHT = screen.get_height()
		# fonts
		self.author_font = pg.font.Font('assets/ui/ARCADEPI.TTF', 30)
		self.small_font = pg.font.Font('assets/ui/ARCADEPI.TTF', 50)
		self.midium_font = pg.font.Font('assets/ui/ARCADEPI.TTF', 60)
		self.big_font = pg.font.Font('assets/ui/ARCADEPI.TTF', 70)
		self.button_font = pg.font.Font('assets/ui/ARCADEPI.TTF', 35)
		self.create_buttons()
		# level
		self.state = state  # menu/game/pause/gameover
		self.level = Level(screen, self.pause_btn)
		self.coins = 0
		self.health = 100
		self.ui = UI(screen, self.health, self.midium_font, self.button_font)
		self.running = True
		self.open_level_time = 0
		# labels
		self.text_color = (255, 255, 255)
		self.title = self.create_label('Medieval Apocalypse', self.big_font)
		self.title_pos = ((self.WIDTH-self.title.get_width())/2, 200)
		self.author_label = self.create_label('By Aronov Lev', self.author_font)
		self.author_pos = (self.WIDTH - 330, self.HEIGHT - 50)
		self.tutorial_label = self.create_label('Tutorial:', self.midium_font)
		self.tutorial_pos = ((self.WIDTH-self.tutorial_label.get_width())/2, 350)
		self.pause_label = self.create_label('Game paused', self.small_font)
		self.pause_pos = ((self.WIDTH-self.pause_label.get_width())/2, 500)
		self.lose_label = self.create_label('YOU DIED!', self.small_font)
		self.win_label = self.create_label('YOU WON!', self.small_font)
		self.gameover_pos = ((self.WIDTH-self.lose_label.get_width())/2, 500)
		# background
		self.create_background()
		# music
		self.level_music = pg.mixer.Sound('assets/audio/level bg.wav')
		self.level_music.set_volume(0.8)
		self.level_complete_music = pg.mixer.Sound('assets/audio/level complete.wav')
		self.level_failed_music = pg.mixer.Sound('assets/audio/game over.wav')
		# sounds
		self.hit_sound = pg.mixer.Sound('assets/audio/hit.wav')  #
		self.death_sound = pg.mixer.Sound('assets/audio/death.wav')  #
		self.burn_sound = pg.mixer.Sound('assets/audio/lava.flac')
		self.attack_sound = pg.mixer.Sound('assets/audio/player attack 1.wav') #
		self.land_sound = pg.mixer.Sound('assets/audio/player land.wav')  #
		self.land_sound.set_volume(0.7)
		self.coin_collect_sound = pg.mixer.Sound('assets/audio/coin.mp3') #
		self.coin_collect_sound.set_volume(0.7)

	def create_buttons(self):
		# create button spritegroups
		button_image = pg.image.load('assets/ui/button.png').convert_alpha()
		button_hovered_image = pg.image.load('assets/ui/button_hovered.png').convert_alpha()

		pause_btn_image = pg.image.load('assets/ui/pause button.png').convert_alpha()
		pause_btn_hovered_image = pg.image.load('assets/ui/pause button hovered.png').convert_alpha()

		self.menu_buttons = pg.sprite.Group()
		self.pause_buttons = pg.sprite.Group()
		self.gameover_buttons = pg.sprite.Group()
		# buttons
		self.start_btn = Button(button_image, button_hovered_image, (self.WIDTH/3, 700), 'START', self.button_font, self.display_surface)
		self.quit_btn = Button(button_image, button_hovered_image, (self.WIDTH*2/3, 700), 'QUIT', self.button_font, self.display_surface)
		self.coninue_btn = Button(button_image, button_hovered_image, (self.WIDTH/3, 700), 'CONTINUE', self.button_font, self.display_surface)
		self.pause_btn = Button(pause_btn_image, pause_btn_hovered_image, (self.WIDTH-70, 70), '', None, self.display_surface)
		self.restart_btn = Button(button_image, button_hovered_image, (self.WIDTH/3, 700), 'RESTART', self.button_font, self.display_surface)

		self.menu_buttons.add(self.start_btn, self.quit_btn)
		self.pause_buttons.add(self.coninue_btn, self.quit_btn)
		self.gameover_buttons.add(self.restart_btn, self.quit_btn)

	def create_background(self):
		# create a brick tile spritegroup and fill up the entire screen with them
		self.background = pg.Surface((self.WIDTH, self.HEIGHT))
		self.bg_tiles_sprites = pg.sprite.Group()
		tile_surface = pg.image.load('assets/tile assets/tiles/brick tile.png').convert_alpha()

		y_offset = self.HEIGHT - len(range(0, self.HEIGHT // tile_size[0] + 1)) * tile_size[1]
		for y in range(self.HEIGHT // tile_size[0] + 1):
			y = y * tile_size[1] + y_offset
			for x in range(self.WIDTH // tile_size[1] + 1):
				x *= tile_size[0]
				sprite = StaticTile((x, y), tile_size, tile_surface)
				self.bg_tiles_sprites.add(sprite)

	def create_label(self, text, font):
		label = font.render(text, True, self.text_color)
		return label

	def display_bg(self):
		# draw background with a bit of shading
		self.bg_tiles_sprites.draw(self.background)
		self.display_surface.blit(self.background, (0, 0))
		# add shading
		surface = pg.Surface((self.WIDTH, self.HEIGHT))
		surface.fill('black')
		surface.set_alpha(50)
		self.display_surface.blit(surface, (0, 0))
		# add title label
		self.display_surface.blit(self.title, self.title_pos)
		self.display_surface.blit(self.author_label, self.author_pos)

	def play(self, dt, keys, mouse_down, mouse_pos):
		# main game mode
		mouse_down = mouse_down and pg.time.get_ticks() - self.open_level_time > 50  # mouse down only 0.05s after opening the level
		self.level.run(dt, self.health, keys, mouse_down, mouse_pos)
		self.manage_audio()

		if self.level.paused:
			self.state = 'pause'
			self.level_music.stop()
			return

		if self.level.gained_health != 0:
			# when some health was gained
			collide_pos = self.level.player.sprite.collisionbox.center
			self.ui.create_indicator(collide_pos, self.level.gained_health)  # shows an indicator when health is gained
			self.level.gained_health = 0
		# update coin and health information
		self.coins = self.level.coins
		self.health = self.ui.current_health
		self.ui.draw(self.coins, self.health, dt)

		if self.level.gameover:
			self.level_music.stop()
			if self.level.win_time:
				self.level_complete_music.play()
			else:
				self.level_failed_music.play()
			self.state = 'gameover'

	def manage_audio(self):
		level = self.level
		player = level.player.sprite

		if player.just_landed:
			self.land_sound.play()

		if level.gained_health < 0:  # if lost health
			if self.health + level.gained_health > 0: # still alive
				self.hit_sound.play()
			elif player.state != 'death': # already dead; frame before the one when it is detected
				self.death_sound.play()

		if player.state == 'attack' and player.frame_index == 0:  # first frame of attack
			self.attack_sound.play()

		if self.coins != level.coins:  # unequal number of coins means more coins
			self.coin_collect_sound.play()

		for enemy in level.enemy_sprites.sprites():
			if enemy.state == 'take hit' and pg.time.get_ticks() - enemy.hurt_time < 20:  # check every enemy for being hurt
				if enemy.health > 0:  # still alive
					self.hit_sound.play()
				else:
					self.death_sound.play()  # already dead

		if player.burnt and player.state != 'death':  # already burnt but not yet dead lol
			self.burn_sound.play()

	def menu(self, mouse_down, mouse_pos):
		self.display_bg()

		self.menu_buttons.update(mouse_down, mouse_pos)
		self.menu_buttons.draw(self.display_surface)

		if self.start_btn.pressed:
			self.state = 'game'
			self.level_music.play(-1)
			self.open_level_time = pg.time.get_ticks()
		if self.quit_btn.pressed:
			self.running = False

	def pause(self, mouse_down, mouse_pos):
		self.display_bg()

		self.display_surface.blit(self.pause_label, self.pause_pos)

		self.pause_buttons.update(mouse_down, mouse_pos)
		self.pause_buttons.draw(self.display_surface)

		if self.coninue_btn.pressed:
			self.level.paused = False
			self.state = 'game'
			self.open_level_time = pg.time.get_ticks()
			self.level_music.play(-1)
		if self.quit_btn.pressed:
			self.running = False

	def gameover(self, mouse_down, mouse_pos):
		self.display_bg()

		if self.health <= 0 or self.level.player.sprite.burnt: # if character is dead, player loses
			self.display_surface.blit(self.lose_label, self.gameover_pos)
		else:
			self.display_surface.blit(self.win_label, self.gameover_pos)  # otherwise player wins

		self.gameover_buttons.update(mouse_down, mouse_pos)
		self.gameover_buttons.draw(self.display_surface)

		if self.restart_btn.pressed:
			self.level_complete_music.stop()
			self.level_failed_music.stop()

			self.state = 'game'
			self.level = Level(self.display_surface, self.pause_btn)
			self.coins = 0
			self.health = 100
			self.ui = UI(self.display_surface, self.health, self.midium_font, self.button_font)
			self.level_music.play(-1)

		if self.quit_btn.pressed:
			self.running = False

	def run(self, dt, keys, mouse_down, mouse_pos):
		if self.state == 'menu':
			self.menu(mouse_down, mouse_pos)
		if self.state == 'game':
			self.play(dt, keys, mouse_down, mouse_pos)
		if self.state == 'pause':
			self.pause(mouse_down, mouse_pos)
		if self.state == 'gameover':
			self.gameover(mouse_down, mouse_pos)
