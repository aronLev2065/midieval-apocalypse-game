import pygame as pg
from sprite_sheet import SpriteSheet
from config import player_full_size, tile_size, player_frame_size, player_real_size, FPS, TARGET_FPS
from support import import_folder

class Player(pg.sprite.Sprite):
	def __init__(self, pos, size, create_particles):
		super().__init__()
		self.import_character_assets()
		self.image = pg.Surface(size)
		self.rect = self.image.get_rect(midbottom=pos)

		self.collisionbox = pg.Rect(0, 0, *player_real_size)  # used for collisions
		self.collisionbox.topleft = pos
		self.pos = pg.math.Vector2(self.collisionbox.midbottom)
		self.rect.midbottom = self.collisionbox.midbottom

		self.attackbox = pg.Rect(0, 0, 110, 80)

		# animation
		self.frame_index = 0
		self.animation_speed = 18
		self.death_animation_speed = 10
		self.state = 'idle'  # run, jump, jump_to_fall, fall, attack, roll, crouch
		self.facing_left = False
		self.dt = 0

		# dust particles (used only for jump)
		self.create_particles = create_particles

		# movement
		self.direction = pg.math.Vector2(0, 0)
		# x
		self.base_speed_x = 300
		self.speed_x = 0
		# y
		self.base_gravity = 2400
		self.base_jump_speed = -1020
		self.gravity = self.base_gravity
		self.jump_speed = self.base_jump_speed

		# status
		self.is_too_high = False
		self.is_jumping = False
		self.action = ''  # attack/crouch/roll/hit
		self.on_ground = False
		self.is_dead = False
		self.death_time = 0
		self.burnt = False

		self.just_landed = False

		self.invincible = False
		self.invincibility_duration = 420
		self.hurt_time = 0

		self.attack_pressed = False
		# sounds
		# self.attack_sound = pg.mixer.Sound('assets/audio/player attack 1.wav')
		# self.land_sound = pg.mixer.Sound('assets/audio/player land.wav')
		# self.land_sound.set_volume(0.7)
		# self.burn_sound = pg.mixer.Sound('assets/audio/lava.flac')

	def import_character_assets(self):
		base_path = 'assets/character/'
		self.animation_set = {'idle': [], 'run': [], 'jump': [],
		                      'jump_to_fall': [], 'fall': [], 'roll': [],
		                      'attack': [], 'crouch': [], 'death': [], 'hit': []}

		# for each set take the image with identical name and get animation frames from it
		for animation in self.animation_set.keys():
			full_path = base_path + animation + '.png'
			sprite_sheet = SpriteSheet(full_path, *player_frame_size, player_full_size, (0, 0, 0))
			self.animation_set[animation] = sprite_sheet.import_animation_list()

	def animate(self, dt):
		animation = self.animation_set[self.state]
		# increase the index by animation speed...
		if self.state == 'death':
			self.frame_index += self.death_animation_speed * dt
		else:
			self.frame_index += self.animation_speed * dt

		if self.frame_index >= len(animation):
			if self.state == 'death':
				self.is_dead = True
				self.death_time = pg.time.get_ticks()
				return
			else:
				self.frame_index = 0
				# these only loop once
				if self.state in 'attack roll crouch hit':
					self.action = ''

		# ... and then take the whole number as the index of current frame
		image = animation[int(self.frame_index)]
		image = pg.transform.flip(image, self.facing_left, False).convert_alpha()
		self.image = image

	def apply_gravity(self, dt):
		self.direction.y += self.gravity * dt / 2
		self.pos.y += self.direction.y * dt
		self.direction.y += self.gravity * dt / 2
		self.collisionbox.bottom = self.pos.y

	def attack(self):
		self.action = 'attack'
		self.frame_index = 0
		# self.attack_sound.play()

	def jump(self):
		self.direction.y = self.jump_speed
		self.is_jumping = True
		self.on_ground = False
		self.create_particles('jump', self.rect.midbottom)

	def land(self):
		if self.direction.y > 800 and self.direction.x == 0:
			self.action = 'crouch'
		if self.is_too_high:
			self.just_landed = True
			if self.direction.x != 0:
				self.action = 'roll'
		# if moving when landed - roll, otherwise crouch
		self.on_ground = True

	def get_damage(self):
		if not self.invincible:
			self.action = 'hit'
			self.invincible = True
			self.hurt_time = pg.time.get_ticks()

	def invincibility_timer(self):
		if self.invincible and not self.state == 'death':
			current_time = pg.time.get_ticks()
			if current_time - self.hurt_time >= self.invincibility_duration:
				self.invincible = False

	def burn(self):
		self.burnt = True
		self.die()

	def die(self):
		if self.action != 'death':
			self.facing_left = not self.facing_left
		self.action = 'death'
		self.invincible = True

	def get_state(self):
		prev_state = self.state
		self.is_too_high = self.direction.y > 1100

		if self.direction.y < 0:
			self.state = 'jump'
			self.on_ground = False
		elif self.direction.y > 100:
			self.state = 'fall'
			self.on_ground = False
		else:
			if self.is_jumping:
				self.state = 'jump_to_fall'  # jumping and y in [0, 100] => transition btwn jumping and falling
				self.on_ground = False
			elif self.direction.x != 0:
				self.state = 'run'
				self.on_ground = True
			else:
				self.state = 'idle'
				self.on_ground = True

		if self.action:
			if self.action == 'crouch' and not self.is_jumping:
				if self.direction.x == 0:
					self.state = self.action
			else:
				self.state = self.action

		if self.state != prev_state:
			self.frame_index = 0

	def get_input(self, mouse_down, keys):
		self.direction.x = 0
		if self.state == 'death':
			return
		# control the keyboard

		if keys[pg.K_a] or keys[pg.K_LEFT]:
			self.direction.x -= 1

		if keys[pg.K_d] or keys[pg.K_RIGHT]:
			self.direction.x += 1

		if self.direction.x != 0:
			if self.state == 'crouch':
				self.action = ''
			if not self.state == 'hit':
				if self.direction.x > 0:
					self.facing_left = False
				elif self.direction.x < 0:
					self.facing_left = True

		if (keys[pg.K_SPACE] or keys[pg.K_UP]) and self.on_ground:
			self.jump()

		if keys[pg.K_k] or mouse_down:
			if self.action != 'attack' and not self.attack_pressed:
				self.attack()
				self.attack_pressed = True
		else:
			self.attack_pressed = False

	def adjust_rect(self):
		# align the rect with collisionbox
		self.rect.midbottom = self.collisionbox.midbottom
		if self.facing_left:
			self.rect.centerx = self.collisionbox.centerx - 8
		else:
			self.rect.centerx = self.collisionbox.centerx + 8

		if self.facing_left:
			self.attackbox.bottomright = self.collisionbox.midbottom
		else:
			self.attackbox.bottomleft = self.collisionbox.midbottom

		self.pos = pg.math.Vector2(self.collisionbox.midbottom)

	def update(self, dt, mouse_down, keys):
		if self.death_time:
			return
		self.get_input(mouse_down, keys)
		self.get_state()
		self.animate(dt)
		self.pos = pg.math.Vector2(self.collisionbox.midbottom)
		self.invincibility_timer()
