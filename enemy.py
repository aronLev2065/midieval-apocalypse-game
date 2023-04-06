from game_data import folder_animations
from random import randint, choice
import pygame as pg
from support import import_folder

class Enemy(pg.sprite.Sprite):
	def __init__(self, name, pos, size):
		super().__init__()
		self.animation_set = self.get_animations(folder_animations[name])
		self.frame_index = 0
		self.animation_speed = 12
		self.attack_animation_speed = 22
		self.takehit_animation_speed = 10
		self.death_animation_speed = 4
		self.state = 'run'
		self.name = name

		self.scale = (350, 350)
		self.size = size
		self.pos = pos

		self.image = self.animation_set[self.state][self.frame_index].convert_alpha()
		self.rect = self.image.get_rect(center=pos)
		self.innerbox = pg.Rect(*pos, *size)
		self.innerbox.center = pos
		self.innerbox.y += 28
		self.pos = pg.math.Vector2(self.innerbox.center)

		self.speed = randint(200, 300)
		self.speed_x = self.speed
		self.facing_left = False

		while True:
			self.direction_x = randint(-1, 1)
			if self.direction_x != 0:
				break

		self.facing_left = True if self.direction_x == -1 else False
		self.colliding = False

		self.invincible = False
		self.invincibility_duration = 1000
		self.hurt_time = 0
		self.is_killed = False

	def get_animations(self, set):
		surface_list = {}
		for anim in set.keys():
			path = set[anim]
			surface_list[anim] = import_folder(path)
		return surface_list

	def increase_frame_index(self, dt):
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

	def reverse(self):
		if self.colliding:
			return
		if self.facing_left:
			self.direction_x = 1
			self.facing_left = False
		else:
			self.direction_x = -1
			self.facing_left = True

	def move(self, dt):
		self.pos.x += self.direction_x * self.speed_x * dt

	def get_damage(self, damage):
		self.state = 'take hit'
		self.invincible = True
		self.direction_x = 0
		self.frame_index = 0
		self.health -= damage
		self.hurt_time = pg.time.get_ticks()

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

	def attack(self):
		if self.state == 'attack': return
		self.state = 'attack'
		self.direction_x = 0
		self.frame_index = 0

	def update(self, shift, dt):
		self.pos.x += shift[0]
		self.pos.y += shift[1]

		self.animate(dt)
		self.image = pg.transform.scale(self.image, self.scale).convert_alpha()
		self.rect = self.image.get_rect(center=self.innerbox.center)

		self.move(dt)
		self.adjust()
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


class Mushroom(Enemy):
	def __init__(self, pos):
		self.size = (90, 100)
		super().__init__('mushroom', pos, self.size)
		self.strength = 30
		self.health = 30
		self.attackbox_size = (75, 70)
		self.attackbox = pg.Rect(0, 0, *self.attackbox_size)


class Skeleton(Enemy):
	def __init__(self, pos):
		self.size = (90, 140)
		super().__init__('skeleton', pos, self.size)
		self.strength = 50
		self.health = 60
		self.attackbox_size = (100, 110)
		self.attackbox = pg.Rect(0, 0, *self.attackbox_size)
