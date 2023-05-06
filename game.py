import pygame as pg

from button import Button, MenuButtonGroup, PauseButtonGroup, GameoverButtonGroup, SettingsButtonGroup
from config import tile_size
from game_data import audio_paths, png_graphics
from level import Level
from tiles import StaticTile
from ui import UI, TextLabel


class Game:
	def __init__(self, screen, state):
		# settings
		self.display_surface = screen
		self.WIDTH = screen.get_width()
		self.HEIGHT = screen.get_height()
		# fonts
		self.author_font = pg.font.Font('assets/ui/ARCADEPI.TTF', 30)
		self.small_font = pg.font.Font('assets/ui/ARCADEPI.TTF', 35)
		self.normal_font = pg.font.Font('assets/ui/ARCADEPI.TTF', 50)
		self.midium_font = pg.font.Font('assets/ui/ARCADEPI.TTF', 60)
		self.big_font = pg.font.Font('assets/ui/ARCADEPI.TTF', 70)
		# level
		self.state = state  # menu/game/pause/gameover/settings
		self.prev_state = state
		self.pause_btn = Button('pause', (100, 100))
		self.health = 100
		self.level = Level(screen, self.pause_btn, self.health)
		self.coins = 0
		self.ui = UI(screen, self.health, self.midium_font, self.small_font)
		self.running = True
		self.open_level_time = 0
		self.last_button_press = 0
		# labels
		self.title = TextLabel('Medieval Apocalypse', self.big_font, (self.WIDTH / 2, self.HEIGHT / 4))
		self.author_label = TextLabel('Made By Lev Aronov', self.author_font, (0, 0))
		self.author_label.rect.bottomright = (self.WIDTH - 50, self.HEIGHT - 50)
		self.start_label = TextLabel('Enjoy the game!', self.normal_font, (self.WIDTH / 2, self.HEIGHT / 2))
		self.pause_label = TextLabel('Game paused', self.normal_font, (self.WIDTH / 2, self.HEIGHT / 2))
		self.lose_label = TextLabel('YOU LOST!', self.normal_font, (self.WIDTH / 2, self.HEIGHT / 2 - 50))
		self.win_label = TextLabel('YOU WON!', self.normal_font, (self.WIDTH / 2, self.HEIGHT / 2 - 50))
		self.score_label = TextLabel('Coins: ', self.normal_font, (self.WIDTH / 2, self.HEIGHT / 2 + 50))
		# audio & buttons
		self.music_on = True
		self.sounds_on = True
		self.button_click = pg.mixer.Sound(audio_paths['button'])
		self.button_click.set_volume(0.5)
		self.create_buttons()
		# background
		self.create_background()

	def create_buttons(self):
		# all buttons except pause are created in each of these classes separately
		self.menu_buttons = MenuButtonGroup([self.WIDTH, self.HEIGHT])
		self.pause_buttons = PauseButtonGroup([self.WIDTH, self.HEIGHT])
		self.gameover_buttons = GameoverButtonGroup([self.WIDTH, self.HEIGHT])
		self.settings_buttons = SettingsButtonGroup([self.WIDTH, self.HEIGHT], self.music_on, self.sounds_on)

	def create_background(self):
		# create a brick tile spritegroup and fill up the entire screen with them
		self.background = pg.Surface((self.WIDTH, self.HEIGHT))
		self.bg_tiles_sprites = pg.sprite.Group()
		tile_surface = pg.image.load(png_graphics['brick']).convert_alpha()

		y_offset = self.HEIGHT - len(range(0, self.HEIGHT // tile_size[0] + 1)) * tile_size[1]
		for y in range(self.HEIGHT // tile_size[0] + 1):
			y = y * tile_size[1] + y_offset
			for x in range(self.WIDTH // tile_size[1] + 1):
				x *= tile_size[0]
				sprite = StaticTile((x, y), tile_size, tile_surface)
				self.bg_tiles_sprites.add(sprite)

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
		self.display_surface.blit(self.title.image, self.title.rect)
		self.display_surface.blit(self.author_label.image, self.author_label.rect)

	# region game stages methods
	def play(self, dt, keys, mouse_down, mouse_pos):
		# main game mode
		mouse_down = mouse_down and pg.time.get_ticks() - self.open_level_time > 50  # mouse down only 0.05s after opening the level
		self.level.run(dt, self.health, keys, mouse_down, mouse_pos, self.sounds_on)

		player = self.level.player.sprite
		if self.level.paused:
			self.state = 'pause'
			self.level.level_music.stop()
			self.level.torch_sound.stop()
			return

		if self.level.gained_health != 0:
			# when some health was gained
			collide_pos = self.level.player.sprite.collisionbox.center
			self.ui.create_indicator(collide_pos, self.level.gained_health)  # shows an indicator when health is gained

		# update coin and health information
		self.coins = self.level.coins
		self.health += self.level.gained_health
		# limit health within [0; 100]
		if self.health < 0:
			self.health = 0
		if self.health > 100:
			self.health = 100

		self.level.gained_health = 0
		self.ui.draw(self.coins, self.health, dt)

		if self.level.gameover:
			self.level.level_music.stop()
			self.level.torch_sound.stop()
			if self.music_on:
				if self.level.completed:
					self.level.level_complete_music.play()
				elif self.level.failed:
					self.level.level_failed_music.play()
			self.state = 'gameover'
			self.score_label.update_text(self.score_label.text + str(self.coins))

	def menu(self, mouse_down, mouse_pos):
		self.display_bg()

		self.display_surface.blit(self.start_label.image, self.start_label.rect)

		self.menu_buttons.update(mouse_down, mouse_pos, self.sounds_on)
		self.menu_buttons.draw(self.display_surface)

		if pg.time.get_ticks() - self.last_button_press < 100:
			return

		if self.menu_buttons.start_btn.pressed:
			self.open_level()
		if self.menu_buttons.settings_btn.pressed:
			self.goto_settings()
		if self.menu_buttons.quit_btn.pressed:
			self.quit()

	def pause(self, mouse_down, mouse_pos):
		self.display_bg()

		self.display_surface.blit(self.pause_label.image, self.pause_label.rect)

		self.pause_buttons.update(mouse_down, mouse_pos, self.sounds_on)
		self.pause_buttons.draw(self.display_surface)

		if pg.time.get_ticks() - self.last_button_press < 100:
			return

		if self.pause_buttons.start_btn.pressed:
			self.level.paused = False
			self.open_level()
		if self.pause_buttons.restart_btn.pressed:
			self.restart_level()
		if self.pause_buttons.settings_btn.pressed:
			self.goto_settings()
		if self.pause_buttons.quit_btn.pressed:
			self.quit()

	def settings(self, mouse_down, mouse_pos):
		self.display_bg()

		self.settings_buttons.update(mouse_down, mouse_pos, self.sounds_on)
		self.settings_buttons.draw(self.display_surface)

		if pg.time.get_ticks() - self.last_button_press < 100:
			return

		if self.settings_buttons.sound_btn.pressed:
			self.settings_buttons.sound_btn.toggle_audio(self.sounds_on)
			self.sounds_on = self.settings_buttons.sound_btn.audio_on

		if self.settings_buttons.music_btn.pressed:
			self.settings_buttons.music_btn.toggle_audio(self.sounds_on)
			self.music_on = self.settings_buttons.music_btn.audio_on

		if self.settings_buttons.back_btn.pressed:
			self.state = self.prev_state
			self.last_button_press = pg.time.get_ticks()
			if self.sounds_on:
				self.button_click.play()

	def gameover(self, mouse_down, mouse_pos):
		self.display_bg()

		if self.level.failed:  # if character is dead, player loses
			self.display_surface.blit(self.lose_label.image, self.lose_label.rect)
		elif self.level.completed:
			self.display_surface.blit(self.win_label.image, self.win_label.rect)  # otherwise player wins

		self.display_surface.blit(self.score_label.image, self.score_label.rect)

		self.gameover_buttons.update(mouse_down, mouse_pos, self.sounds_on)
		self.gameover_buttons.draw(self.display_surface)

		if pg.time.get_ticks() - self.last_button_press < 100:
			return

		if self.gameover_buttons.restart_btn.pressed:
			self.restart_level()
		if self.gameover_buttons.settings_btn.pressed:
			self.goto_settings()
		if self.gameover_buttons.quit_btn.pressed:
			self.quit()

	# endregion

	# region button methods
	def goto_settings(self):
		if self.sounds_on:
			self.button_click.play()
		self.last_button_press = pg.time.get_ticks()

		self.prev_state = self.state
		self.state = 'settings'

	def restart_level(self):
		if self.sounds_on:
			self.button_click.play()
		self.last_button_press = pg.time.get_ticks()

		self.level.level_complete_music.stop()
		self.level.level_failed_music.stop()
		self.level.torch_sound.stop()

		self.score_label.update_text('Coins: ')  # reset the score label
		self.prev_state = self.state
		self.state = 'game'
		self.health = 100
		self.level = Level(self.display_surface, self.pause_btn, self.health)  # recreate level
		self.coins = 0  # reset coins and health

		if self.sounds_on:
			self.level.torch_sound.play(-1)
		if self.music_on:
			self.level.level_music.play(-1)

	def open_level(self):
		if self.sounds_on:
			self.button_click.play()
		self.last_button_press = pg.time.get_ticks()

		self.prev_state = self.state
		self.state = 'game'
		self.open_level_time = pg.time.get_ticks()
		if self.sounds_on:
			self.level.torch_sound.play(-1)
		if self.music_on:
			self.level.level_music.play(-1)

	def quit(self):
		self.running = False

	# endregion

	def run(self, dt, keys, mouse_down, mouse_pos):
		if self.state == 'menu':
			self.menu(mouse_down, mouse_pos)
		if self.state == 'game':
			self.play(dt, keys, mouse_down, mouse_pos)
		if self.state == 'settings':
			self.settings(mouse_down, mouse_pos)
		if self.state == 'pause':
			self.pause(mouse_down, mouse_pos)
		if self.state == 'gameover':
			self.gameover(mouse_down, mouse_pos)
