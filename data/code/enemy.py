from game_data import folder_animations, audio_paths
from random import randint
import pygame as pg
from support import import_folder


class Enemy(pg.sprite.Sprite):
	def __init__(self, name, pos, size):
		super().__init__()
		# animation info
		self.animation_set = self.get_animations(folder_animations[name])
		self.frame_index = 0
		self.animation_speed = 12
		self.attack_animation_speed = 22
		self.takehit_animation_speed = 10
		self.death_animation_speed = 4
		self.state = 'run'
		self.name = name
		# geometry
		self.scale = (350, 350)
		self.size = size
		self.pos = pos
		# rects
		self.image = self.animation_set[self.state][self.frame_index].convert_alpha()
		self.rect = self.image.get_rect(center=pos)
		self.innerbox = pg.Rect(*pos, *size)
		self.innerbox.center = pos
		self.innerbox.y += 28
		self.old_rect = self.innerbox.copy()
		self.pos = pg.math.Vector2(self.innerbox.center)
		# movement
		self.speed = randint(200, 300)
		self.speed_x = self.speed
		self.facing_left = False

		while True:
			self.direction_x = randint(-1, 1)
			if self.direction_x != 0:
				break
		# booleans
		self.facing_left = True if self.direction_x == -1 else False

		self.invincible = False
		self.invincibility_duration = 1000
		self.hurt_time = 0
		self.is_killed = False
		# sounds
		self.death_sound = pg.mixer.Sound(audio_paths['enemy']['death'])
		self.hit_sound = pg.mixer.Sound(audio_paths['enemy']['hit'])

	def get_animations(self, set):
		surface_list = {}
		for anim in set.keys():
			path = set[anim]
			surface_list[anim] = import_folder(path)
		return surface_list

	def increase_frame_index(self, dt):
		# the animation speed differs depending on the current state
		if self.state == 'attack':
			self.frame_index += self.attack_animation_speed * dt
		elif self.state == 'take hit':
			self.frame_index += self.takehit_animation_speed * dt
		elif self.state == 'death':
			self.frame_index += self.death_animation_speed * dt
		else:
			self.frame_index += self.animation_speed * dt

	def animate(self, dt):
		self.increase_frame_index(dt)
		if self.frame_index >= len(self.animation_set[self.state]):
			self.frame_index = 0
			if self.state == 'death':
				self.is_killed = True
				return
			if self.state == 'take hit' or self.state == 'attack':
				self.state = 'run'
				self.direction_x = -1 if self.facing_left else 1

		self.image = self.animation_set[self.state][int(self.frame_index)].convert_alpha()
		if self.facing_left:
			self.image = pg.transform.flip(self.image, True, False)

	def limit(self, borders):
		for border in borders:
			if border.rect.colliderect(self.innerbox):
				if self.old_rect.right <= border.old_rect.left and self.innerbox.right >= border.rect.left:
					# collision on the right
					self.direction_x = -1
					self.facing_left = True
				if self.old_rect.left >= border.old_rect.right and self.innerbox.left <= border.rect.right:
					# collision on the left
					self.direction_x = 1
					self.facing_left = False

	def move(self, dt):
		self.pos.x += self.direction_x * self.speed_x * dt

	def get_damage(self, damage, sounds_on):
		self.state = 'take hit'
		self.invincible = True
		self.direction_x = 0
		self.frame_index = 0
		self.health -= damage
		self.hurt_time = pg.time.get_ticks()
		if sounds_on:
			self.hit_sound.play()

	def invincibility_timer(self):
		if self.invincible:
			current_time = pg.time.get_ticks()
			if current_time - self.hurt_time >= self.invincibility_duration:
				self.invincible = False

	def adjust(self):
		self.innerbox.center = self.pos
		self.rect.center = self.innerbox.center
		self.attackbox.bottom = self.innerbox.bottom - 20
		if self.facing_left:
			self.attackbox.right = self.innerbox.centerx + 5
		else:
			self.attackbox.left = self.innerbox.centerx - 5
		self.image.set_colorkey((255, 255, 255))

	def attack(self, sounds_on):
		if self.state == 'attack': return
		if sounds_on:
			self.attack_sound.play()
		self.state = 'attack'
		self.direction_x = 0
		self.frame_index = 0

	def update(self, shift, borders, dt):
		self.pos.x += shift[0]
		self.pos.y += shift[1]

		self.animate(dt)
		self.image = pg.transform.scale(self.image, self.scale).convert_alpha()
		self.old_rect = self.innerbox.copy()
		self.rect = self.image.get_rect(center=self.innerbox.center)
		self.move(dt)
		self.adjust()
		self.limit(borders)
		self.invincibility_timer()


class Eye(Enemy):
	def __init__(self, pos):
		self.size = (90, 60)
		super().__init__('eye', pos, self.size)
		self.strength = 40
		self.health = 45
		self.attackbox_size = (75, 70)
		self.attackbox = pg.Rect(0, 0, *self.attackbox_size)
		self.gravity = 2400
		self.direction_y = 0
		self.fallen = False

		attack_sound_path = audio_paths['enemy']['attack']['eye']
		self.attack_sound = pg.mixer.Sound(attack_sound_path)

	def apply_gravity(self, dt):
		if self.fallen:
			self.direction_x = 0
			self.speed_x = 0
		else:
			self.direction_y += self.gravity * dt / 2
			self.pos.y += self.direction_y * dt
			self.direction_y += self.gravity * dt / 2
			self.innerbox.bottom = self.pos.y
			self.adjust()

	def adjust(self):
		self.innerbox.centery = self.pos.y + 28
		self.innerbox.centerx = self.pos.x
		self.rect.center = self.innerbox.center
		self.attackbox.bottom = self.innerbox.bottom - 20
		if self.facing_left:
			self.attackbox.right = self.innerbox.centerx + 5
		else:
			self.attackbox.left = self.innerbox.centerx - 5
		self.image.set_colorkey((255, 255, 255))


class Goblin(Enemy):
	def __init__(self, pos):
		self.size = (90, 92)
		super().__init__('goblin', pos, self.size)
		self.strength = 30
		self.health = 30
		self.attackbox_size = (75, 70)
		self.attackbox = pg.Rect(0, 0, *self.attackbox_size)

		attack_sound_path = audio_paths['enemy']['attack']['goblin']
		self.attack_sound = pg.mixer.Sound(attack_sound_path)


class Mushroom(Enemy):
	def __init__(self, pos):
		self.size = (90, 100)
		super().__init__('mushroom', pos, self.size)
		self.strength = 30
		self.health = 30
		self.attackbox_size = (75, 70)
		self.attackbox = pg.Rect(0, 0, *self.attackbox_size)

		attack_sound_path = audio_paths['enemy']['attack']['eye']
		self.attack_sound = pg.mixer.Sound(attack_sound_path)


class Skeleton(Enemy):
	def __init__(self, pos):
		self.size = (90, 140)
		super().__init__('skeleton', pos, self.size)
		self.strength = 50
		self.health = 60
		self.attackbox_size = (100, 110)
		self.attackbox = pg.Rect(0, 0, *self.attackbox_size)

		attack_sound_path = audio_paths['enemy']['attack']['skeleton']
		self.attack_sound = pg.mixer.Sound(attack_sound_path)
