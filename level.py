# import pygame as pg
from tiles import *
from config import player_full_size
from player import Player
from vfx import Dust, Shockwave, Splash
from support import *
from game_data import *
from enemy import *
from random import randint

class Level:
	def __init__(self, surface, pause_btn):
		# general setup
		self.display_surface = surface
		self.WIDTH = surface.get_width()
		self.HEIGHT = surface.get_height()
		self.map_width = 0
		self.true_scroll = [0, 0]
		self.shift = [0, 0]

		self.coins = 0
		self.gained_health = 0
		self.weapon_strength = 15

		# vfx setup
		self.dust_sprite = pg.sprite.Group()
		self.transition = None
		self.visual_effects = []

		self.downloaded = False
		self.completed = False
		self.failed = False
		self.gameover = False
		self.gameover_time = 0

		self.sounds_on = True
		self.torch_sound = pg.mixer.Sound(audio_paths['torch'])
		self.torch_sound.set_volume(0.5)
		self.button_click = pg.mixer.Sound(audio_paths['button'])
		self.button_click.set_volume(0.5)

		self.level_music = pg.mixer.Sound(audio_paths['level']['bg'])
		self.level_music.set_volume(0.8)
		self.level_complete_music = pg.mixer.Sound(audio_paths['level']['complete'])
		self.level_failed_music = pg.mixer.Sound(audio_paths['level']['fail'])

		self.paused = False
		self.pause_btn = pause_btn
		self.pause_btn.rect.topright = (self.WIDTH - 10, 10)
		self.pause_group = pg.sprite.GroupSingle()
		self.pause_group.add(pause_btn)

		self.setup_tiles()

	# region methods: setup_tiles, create_tile_group, create_single_group, create_particles
	def setup_tiles(self):
		# player
		player_layout = import_csv_layout(csv_graphics['player'])
		self.player = self.create_single_group(player_layout, 'player')
		# blocks layout
		block_layout = import_csv_layout(csv_graphics['blocks'])
		self.block_sprites = self.create_tile_group(block_layout, 'blocks')
		# # door bg
		door_bg_layout = import_csv_layout(csv_graphics['door bg'])
		self.door_bg_sprite = self.create_single_group(door_bg_layout, 'door')
		# # door fg
		door_fg_layout = import_csv_layout(csv_graphics['door fg'])
		self.door_fg_sprite = self.create_single_group(door_fg_layout, 'door')
		# # fire
		fire_layout = import_csv_layout(csv_graphics['fire'])
		self.fire_sprites = self.create_tile_group(fire_layout, 'fire')
		# # lava
		lava_layout = import_csv_layout(csv_graphics['lava'])
		self.lava_sprites = self.create_tile_group(lava_layout, 'lava')
		# # coins
		coin_layout = import_csv_layout(csv_graphics['coins'])
		self.coin_sprites = self.create_tile_group(coin_layout, 'coins')
		# # torches
		torch_layout = import_csv_layout(csv_graphics['torch'])
		self.torch_sprites = self.create_tile_group(torch_layout, 'torch')
		# # borders
		borders_layout = import_csv_layout(csv_graphics['borders'])
		self.border_sprites = self.create_tile_group(borders_layout, 'borders')
		# # enemies
		enemy_layout = import_csv_layout(csv_graphics['enemies'])
		self.enemy_sprites = self.create_tile_group(enemy_layout, 'enemies')
		# # background
		bg_layout = import_csv_layout(csv_graphics['background'])
		self.bg_sprites = self.create_tile_group(bg_layout, 'background')

		self.shift[0] = 0
		self.downloaded = True

	def create_tile_group(self, layout, type):
		sprite_group = pg.sprite.Group()

		y_offset = self.HEIGHT - len(layout) * tile_size[1]

		tile_list = []
		if type == 'blocks' or type == 'background':
			# create a list of tiles outside of the loop to use it inside of it
			tile_list = import_cut_graphics(png_graphics[type])

		for r, row in enumerate(layout):
			for c, col in enumerate(row):
				if col != '-1':
					x = c * tile_size[0] + self.shift[0]
					y = r * tile_size[1] + y_offset
					if type == 'blocks':
						tile_surface = tile_list[int(col)]
						tile_surface.set_colorkey((255, 255, 255))
						sprite = StaticTile((x, y), tile_size, tile_surface)
					if type == 'fire':
						sprite = Fire((x, y), 80, 80, tile_size, spritesheet_animations['fire'])
					if type == 'lava':
						sprite = Lava((x, y), *tile_size, tile_size, spritesheet_animations['lava'])
					if type == 'coins':
						sprite = Coin((x, y), *tile_size, tile_size, spritesheet_animations['coins'])
					if type == 'torch':
						sprite = Torch((x, y), *tile_size, tile_size, spritesheet_animations['torch'])
					if type == 'borders':
						sprite = Border((x, y), tile_size)
					if type == 'enemies':
						if col == '1':  # eye
							sprite = Eye((x, y))
						if col == '2':  # goblin
							sprite = Goblin((x, y))
						if col == '3':  # mushroom
							sprite = Mushroom((x, y))
						if col == '4':  # skeleton
							sprite = Skeleton((x, y))
					if type == 'background':
						tile_surface = tile_list[int(col)]
						sprite = BackgroundTile((x, y), tile_size, tile_surface)
					sprite_group.add(sprite)
		return sprite_group

	def create_single_group(self, layout, type):
		sprite_group = pg.sprite.GroupSingle()

		y_offset = self.HEIGHT - len(layout) * tile_size[1]
		for r, row in enumerate(layout):
			for c, col in enumerate(row):
				if col != '-1':
					x = c * tile_size[0] + self.shift[0]
					y = r * tile_size[1] + y_offset
					if type == 'door':
						door_tile_list = import_cut_graphics(png_graphics['door'])
						door_surface = door_tile_list[int(col)]
						sprite = Door((x, y), tile_size, door_surface)
					if type == 'player':
						sprite = Player((x, y), player_full_size, self.create_particles)
					sprite_group.add(sprite)
					break
		return sprite_group

	def create_particles(self, type, pos):
		player = self.player.sprite

		if type == 'jump':
			jump_particle = Dust(pos, 'jump')
			self.dust_sprite.add(jump_particle)

		elif type == 'land':
			land_particle = Dust(pos, 'land')
			self.dust_sprite.add(land_particle)

		elif type == 'run':
			flip = player.facing_left
			run_particle = Dust(pos, 'run', flip=flip)
			self.dust_sprite.add(run_particle)

	# endregion

	# region movement logic
	def scroll_x(self):
		# scroll the entire level so that it follows the player and always stays in view (SMOOTH!!!)
		player = self.player.sprite
		player_x = player.collisionbox.centerx
		player_width = player.collisionbox.width

		self.true_scroll[0] = (self.WIDTH / 2 - player_x) / 20
		self.shift = self.true_scroll.copy()
		self.shift[0] = int(self.shift[0])

	def x_movement(self, dt):
		player = self.player.sprite
		player.pos.x += player.direction.x * player.speed_x * dt  # player runs
		player.collisionbox.centerx = player.pos.x

		# create and kill run particles
		dust_particles = self.dust_sprite.sprites()
		running_particle = False
		for dust in dust_particles:
			if dust.type == 'run':  # find the running particle among others
				if player.state == 'run':  # if player is running, then keep the particle
					running_particle = True
				else:
					dust.kill()  # otherwise kill it
		if not running_particle and player.state == 'run':  # if there are no running particles but the player is running
			self.create_particles('run', player.rect.midbottom)  # create them
		collideble = self.block_sprites.sprites()

		# if the player hits the wall he stops running
		for tile in collideble:
			if tile.rect.colliderect(player.collisionbox):
				if player.direction.x > 0:  # collision on the right to the player
					player.collisionbox.right = tile.rect.left
				if player.direction.x < 0:  # collision on the left to the player
					player.collisionbox.left = tile.rect.right

		player.adjust_rect()

	def y_movement(self, dt):
		player = self.player.sprite
		player.apply_gravity(dt)  # always move the player down

		collideble = self.block_sprites.sprites()

		dead_eyes = []  # if eyemonster dies, it has to fall
		for eye in self.enemy_sprites.sprites():
			if eye.name == 'eye' and eye.state == 'death' and not eye.fallen:
				dead_eyes.append(eye)
				eye.apply_gravity(dt)

		for tile in collideble:
			if tile.rect.colliderect(player.collisionbox):
				# and player.collisionbox.bottom >= tile.rect.top >= player.collisionbox.top
				if player.direction.y > 0 and player.collisionbox.bottom >= tile.rect.top >= player.collisionbox.top:  # collision below the player (floor)
					player.collisionbox.bottom = tile.rect.top
					if player.is_jumping or player.state == 'fall' and not player.on_ground:  # if collided with the floor while jumping => land
						player.land(self.sounds_on)
						self.create_particles('land', player.rect.midbottom)
					player.direction.y = 0
					player.is_jumping = False

				elif player.direction.y < 0 and player.collisionbox.top < tile.rect.bottom:  # collision above the player (ceiling)
					player.collisionbox.top = tile.rect.bottom
					player.direction.y = 0

			for eye in dead_eyes:
				if tile.rect.colliderect(eye.innerbox):
					eye.pos.y = tile.rect.top - 88
					eye.fallen = True
					eye.direction_x = 0
				elif eye.pos.y > self.HEIGHT:
					eye.pos.y = self.HEIGHT - 88
					eye.fallen = True
					eye.direction_x = 0
		if player.collisionbox.bottom > self.HEIGHT:
			player.collisionbox.bottom = self.HEIGHT

		player.adjust_rect()

	# endregion

	# region collision detection
	def check_fire_collision(self):
		player = self.player.sprite
		fire_tiles = self.fire_sprites.sprites()
		lava_tiles = self.lava_sprites.sprites()

		# if player hits fire, he dies
		for fire in [*fire_tiles, *lava_tiles]:
			if fire.rect.colliderect(player.collisionbox) and (player.collisionbox.y <= (fire.rect.bottom)):
				self.gained_health = 0
				if not player.burnt:
					for i in range(200):
						self.visual_effects.append(Splash(
							player.collisionbox.midbottom,
							[randint(0, 250) / 10 - 12.5, randint(0, 200) / 10 - 21],
							randint(20, 30),
							(randint(200, 255), randint(0, 50), randint(0, 50)),
							self.display_surface)
						)
					player.burn(self.sounds_on)

	def check_coin_collision(self):
		player = self.player.sprite
		coins = self.coin_sprites.sprites()

		# if player collides with coins, he collects them
		for coin in coins:
			if coin.hitbox.colliderect(player.collisionbox) and not coin.collected:
				coin.collect(self.sounds_on)
				self.gained_health += 5
				self.coins += 1
				self.visual_effects.append(Shockwave(coin.rect.center, 30, 3, 1.1, 'white', self.display_surface))

	def check_enemy_collision(self):
		player = self.player.sprite
		enemies = self.enemy_sprites.sprites()

		for enemy in enemies:
			if enemy.health > 0:
				if player.state == 'attack' and not enemy.invincible and not enemy.state == 'death':
					if enemy.innerbox.colliderect(player.attackbox):
						if player.facing_left:
							enemy.facing_left = False
							enemy.direction_x = 1
						else:
							enemy.facing_left = True
							enemy.direction_x = -1
						enemy.get_damage(self.weapon_strength, self.sounds_on)
						self.visual_effects.append(
							Shockwave(enemy.innerbox.center, 30, 3, 1.1, 'white', self.display_surface))


				elif not player.invincible and enemy.state != 'take hit':
					if enemy.attackbox.colliderect(player.collisionbox):
						enemy.attack(self.sounds_on)
						if enemy.frame_index >= 6:  # in the attack spritesheet 7th frame is the actual attack
							# player needs to be facing the enemy when being attacked
							if enemy.facing_left:
								player.facing_left = False
							else:
								player.facing_left = True
							player.get_damage(self.sounds_on)
							self.gained_health -= enemy.strength

			else:
				if enemy.state != 'death':
					# if health is already < 0 but enemy is still taking hit
					# then it's the first frame after death
					self.gained_health += int(enemy.strength * 0.75)
					self.visual_effects.append(
						Shockwave(enemy.innerbox.center, 50, 10, 2.1, 'white', self.display_surface))
					if self.sounds_on:
						enemy.death_sound.play()
				enemy.state = 'death'
				if enemy.is_killed:
					enemy.kill()

	def check_collisions(self):
		self.check_enemy_collision()
		self.check_coin_collision()
		self.check_fire_collision()

	# endregion

	def limit_enemies(self):
		# if enemy hits a wall, they turn around and move in the opposide direction
		for enemy in self.enemy_sprites.sprites():
			colliding = False
			for border in self.border_sprites.sprites():
				if enemy.innerbox.colliderect(border.rect):
					enemy.reverse()
					colliding = True
			enemy.colliding = colliding

	def check_gameover(self, health):
		if self.gameover_time: return True

		player = self.player.sprite
		if health <= 0 and player.action != 'death':
			player.die(self.sounds_on)
			for i in range(5):
				self.visual_effects.append(
					Shockwave(player.collisionbox.center, i * 30 + 50, i * 2.5 + 5, i / 4 + 1, 'white',
					          self.display_surface))

		if player.is_dead:
			self.gameover_time = pg.time.get_ticks()
			self.completed = False
			return True  # you lost

		if health > 0:
			door = self.door_fg_sprite.sprite
			if door.rect.colliderect(player.collisionbox):
				# if collided with the door
				if not player.is_won:
					player.is_won = True
					self.gameover_time = pg.time.get_ticks()  # you won
					self.completed = True
					return True

		self.gameover_time = 0
		self.completed = False
		return False

	def run(self, dt, health, keys, mouse_down, mouse_pos, sounds_on):
		self.sounds_on = sounds_on

		self.draw(dt, mouse_down, keys)
		self.pause_group.draw(self.display_surface)
		player = self.player.sprite

		self.limit_enemies()

		self.x_movement(dt)
		self.y_movement(dt)
		self.scroll_x()

		self.check_collisions()

		for i, effect in sorted(enumerate(self.visual_effects), reverse=True):
			effect.update(self.shift)
			if not effect.alive:
				self.visual_effects.pop(i)

		if self.check_gameover(health):
			now = pg.time.get_ticks()
			self.failed = not self.completed
			if now - self.gameover_time > 700:
				self.gameover = True
		else:
			self.pause_group.update(mouse_down, mouse_pos, sounds_on)
			if ((mouse_down and self.pause_btn.hovered) or keys[pg.K_ESCAPE]) and not \
					(self.player.sprite.is_dead or self.player.sprite.burnt or self.player.sprite.action == 'death'):
				# pause is possible only during the game and when player hasn't won or failed yet
				self.paused = True
				if sounds_on:
					self.button_click.play()
				return

	def draw(self, dt, mouse_down, keys):
		# backround
		self.bg_sprites.update(self.shift)
		self.bg_sprites.draw(self.display_surface)
		# dust particles
		self.dust_sprite.update(self.shift, self.player.sprite.rect.midbottom, self.player.sprite.facing_left, dt)
		self.dust_sprite.draw(self.display_surface)
		# fire
		self.fire_sprites.update(self.shift, dt)
		self.fire_sprites.draw(self.display_surface)
		# door bg
		self.door_bg_sprite.update(self.shift)
		self.door_bg_sprite.draw(self.display_surface)
		# torch
		self.torch_sprites.update(self.shift, dt)
		self.torch_sprites.draw(self.display_surface)
		# coins
		self.coin_sprites.update(self.shift, dt)
		self.coin_sprites.draw(self.display_surface)
		# player
		self.player.update(dt, self.shift, mouse_down, keys, self.sounds_on)
		self.player.draw(self.display_surface)
		# lava
		self.lava_sprites.update(self.shift, dt)
		self.lava_sprites.draw(self.display_surface)
		# blocks
		self.block_sprites.update(self.shift)
		self.block_sprites.draw(self.display_surface)

		if self.player.sprite.state == 'attack':  # when attacks player should be drawn upon the blocks
			self.player.draw(self.display_surface)

		# enemies
		self.enemy_sprites.update(self.shift, dt)
		self.enemy_sprites.draw(self.display_surface)
		# door fg
		self.door_fg_sprite.update(self.shift)
		self.door_fg_sprite.draw(self.display_surface)
		# borders
		self.border_sprites.update(self.shift)
		self.border_sprites.draw(self.display_surface)
