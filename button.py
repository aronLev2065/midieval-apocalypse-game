import pygame as pg
from game_data import button_images, audio_paths

class Button(pg.sprite.Sprite):
	def __init__(self, name, size):
		super().__init__()
		normal_image = pg.image.load(button_images[name][0]).convert_alpha()
		hovered_image = pg.image.load(button_images[name][1]).convert_alpha()

		self.hovered_image = pg.transform.scale(hovered_image, size)
		self.normal_image = pg.transform.scale(normal_image, size)

		self.image_rect = self.normal_image.get_rect()

		self.image = pg.Surface(self.image_rect.size, flags=pg.SRCALPHA)
		self.image.set_colorkey('white')
		self.rect = self.image.get_rect()

		self.hovered = False
		self.pressed = False

		self.click = pg.mixer.Sound(audio_paths['button'])
		self.click.set_volume(0.5)

	def check_hover(self, mouse_pos):
		if (self.rect.left <= mouse_pos[0] <= self.rect.right) and (self.rect.top <= mouse_pos[1] <= self.rect.bottom):
			self.hovered = True
			self.image.blit(self.hovered_image, (0, 0))
		else:
			self.hovered = False
			self.image.blit(self.normal_image, (0, 0))

	def update(self, mouse_down, mouse_position, sounds_on):
		self.check_hover(mouse_position)
		if self.hovered and mouse_down:
			self.pressed = True
		else:
			self.pressed = False


class AudioButton(Button):
	def __init__(self, name, size, is_audio_on):
		super().__init__(name, size)
		name = name.replace('on', 'off')
		self.image_off = pg.transform.scale(pg.image.load(button_images[name][0]).convert_alpha(), size)
		self.image_off_hovered = pg.transform.scale(pg.image.load(button_images[name][1]).convert_alpha(), size)
		self.audio_on = True

		if not is_audio_on:
			self.toggle_audio(False)

	def toggle_audio(self, sounds_on):
		if sounds_on:
			self.click.play()
		self.audio_on = not self.audio_on
		self.image_off, self.normal_image = self.normal_image, self.image_off
		self.image_off_hovered, self.hovered_image = self.hovered_image, self.image_off_hovered


class ButtonGroup(pg.sprite.Group):
	def __init__(self, buttons, display_size):
		self.WIDTH = display_size[0]
		self.HEIGHT = display_size[1]
		super().__init__(buttons)
		self.place_buttons()

	def place_buttons(self):
		y = self.HEIGHT * 3 / 4
		current_x = self.WIDTH / (len(self.buttons) + 1)
		for button in self.buttons:
			button.rect.center = (current_x, y)
			current_x += self.WIDTH / (len(self.buttons) + 1)


class MenuButtonGroup(ButtonGroup):
	def __init__(self, display_size):
		# start button
		self.start_btn = Button('start', (180, 180))
		# quit button
		self.quit_btn = Button('quit', (180, 180))
		# settings button
		self.settings_btn = Button('settings', (180, 180))
		self.buttons = [self.start_btn, self.settings_btn, self.quit_btn]
		super().__init__(self.buttons, display_size)


class PauseButtonGroup(ButtonGroup):
	def __init__(self, display_size):
		# start button
		self.start_btn = Button('start', (180, 180))
		# quit button
		self.quit_btn = Button('quit', (180, 180))
		# restart button
		self.restart_btn = Button('restart', (180, 180))
		# settings button
		self.settings_btn = Button('settings', (180, 180))
		self.buttons = [self.start_btn, self.restart_btn, self.settings_btn, self.quit_btn]
		super().__init__(self.buttons, display_size)


class GameoverButtonGroup(ButtonGroup):
	def __init__(self, display_size):
		# quit button
		self.quit_btn = Button('quit', (180, 180))
		# restart button
		self.restart_btn = Button('restart', (180, 180))
		# settings button
		self.settings_btn = Button('settings', (180, 180))
		self.buttons = [self.restart_btn, self.settings_btn, self.quit_btn]
		super().__init__(self.buttons, display_size)


class SettingsButtonGroup(ButtonGroup):
	def __init__(self, display_size, music_on, sounds_on):
		# go back button
		self.back_btn = Button('back', (180, 180))
		# music management button
		self.music_btn = AudioButton('music_on', (180, 180), music_on)
		# sound management button
		self.sound_btn = AudioButton('sound_on', (180, 180), sounds_on)
		self.buttons = [self.back_btn, self.music_btn, self.sound_btn]
		super().__init__(self.buttons, display_size)
