import pygame as pg
from sys import exit
import time


class StaticObstacle(pg.sprite.Sprite):
	def __init__(self, pos, size, groups):
		super().__init__(groups)
		self.image = pg.Surface(size)
		self.image.fill('yellow')
		self.rect = self.image.get_rect(topleft=pos)
		self.old_rect = self.rect.copy()


class MovingVerticalObstacle(StaticObstacle):
	def __init__(self, pos, size, groups):
		super().__init__(pos, size, groups)
		self.image.fill('green')
		self.pos = pg.math.Vector2(self.rect.topleft)
		self.direction = pg.math.Vector2((0, 1))
		self.speed = 350
		self.old_rect = self.rect.copy()

	def update(self, dt):
		self.old_rect = self.rect.copy()  # previous frame
		if self.rect.bottom > 600:
			self.rect.bottom = 600
			self.pos.y = self.rect.y
			self.direction.y *= -1
		if self.rect.bottom < 120:
			self.rect.bottom = 120
			self.pos.y = self.rect.y
			self.direction.y *= -1

		self.pos.y += self.direction.y * self.speed * dt
		self.rect.y = round(self.pos.y)  # current frame


class MovingHorizontalObstacle(StaticObstacle):
	def __init__(self, pos, size, groups):
		super().__init__(pos, size, groups)
		self.image.fill('purple')
		self.pos = pg.math.Vector2(self.rect.topleft)
		self.direction = pg.math.Vector2((1, 0))
		self.speed = 350
		self.old_rect = self.rect.copy()

	def update(self, dt):
		self.old_rect = self.rect.copy()
		if self.rect.right > 1000:
			self.rect.right = 1000
			self.pos.x = self.rect.x
			self.direction.x *= -1
		if self.rect.left < 600:
			self.rect.left = 600
			self.pos.x = self.rect.x
			self.direction.x *= -1

		self.pos.x += self.direction.x * self.speed * dt
		self.rect.x = round(self.pos.x)


class Player(pg.sprite.Sprite):
	def __init__(self, groups, obstacles):
		super().__init__(groups)

		# image
		self.image = pg.Surface((30, 60))
		self.image.fill('blue')

		# position
		self.rect = self.image.get_rect(topleft=(640, 360))
		self.old_rect = self.rect.copy()

		# movement
		self.pos = pg.math.Vector2(self.rect.topleft)
		self.direction = pg.math.Vector2()
		self.speed = 300

		self.obstacles = obstacles

	def collision(self, direction):
		collision_sprites = pg.sprite.spritecollide(self, self.obstacles, False)
		if collision_sprites:
			if direction == 'horizontal':
				for obstacle in collision_sprites:
					# collision on the right
					if self.rect.right >= obstacle.rect.left and self.old_rect.right <= obstacle.old_rect.left:
						self.rect.right = obstacle.rect.left
						self.pos.x = self.rect.x

					# collision on the left
					if self.rect.left <= obstacle.rect.right and self.old_rect.left >= obstacle.old_rect.right:
						self.rect.left = obstacle.rect.right
						self.pos.x = self.rect.x
			if direction == 'vertical':
				for obstacle in collision_sprites:
					# collision on the top
					if self.rect.top <= obstacle.rect.bottom and self.old_rect.top >= obstacle.old_rect.bottom:
						self.rect.top = obstacle.rect.bottom
						self.pos.y = self.rect.y

					# collision on the bottom
					if self.rect.bottom >= obstacle.rect.top and self.old_rect.bottom <= obstacle.old_rect.top:
						self.rect.bottom = obstacle.rect.top
						self.pos.y = self.rect.y

	def wall_bounce(self):
		if self.rect.x <= 10:
			self.rect.x = 10
			self.pos.x = 10
		elif self.rect.right >= 1270:
			self.rect.right = 1270
			self.pos.x = self.rect.x

		if self.rect.y <= 10:
			self.rect.y = 10
			self.pos.y = 10
		elif self.rect.bottom >= 710:
			self.rect.bottom = 710
			self.pos.y = self.rect.y

	def input(self):
		keys = pg.key.get_pressed()

		# movement input
		if keys[pg.K_w]:
			self.direction.y = -1
		elif keys[pg.K_s]:
			self.direction.y = 1
		else:
			self.direction.y = 0

		if keys[pg.K_d]:
			self.direction.x = 1
		elif keys[pg.K_a]:
			self.direction.x = -1
		else:
			self.direction.x = 0

	def update(self, dt):
		self.old_rect = self.rect.copy()
		self.input()

		if self.direction.magnitude() != 0:
			self.direction = self.direction.normalize()

		self.wall_bounce()

		self.pos.x += self.direction.x * self.speed * dt
		self.rect.x = round(self.pos.x)
		self.collision('horizontal')
		self.pos.y += self.direction.y * self.speed * dt
		self.rect.y = round(self.pos.y)
		self.collision('vertical')


class Ball(pg.sprite.Sprite):
	def __init__(self, groups, obstacles, player):
		super().__init__(groups)
		self.image = pg.Surface((50, 50))
		self.image.fill('red')
		self.rect = self.image.get_rect(center = (640,360))

		self.pos = pg.math.Vector2(self.rect.topleft)
		self.direction = pg.math.Vector2(1,1)
		self.speed = 400

		self.old_rect = self.rect.copy
		self.obstacles = obstacles
		self.player = player
		self.is_colliding_x = False
		self.is_colliding_y = False

	def collision(self, direction):
		obstacles = pg.sprite.spritecollide(self, self.obstacles, False)

		if self.rect.colliderect(self.player.rect):
			obstacles.append(self.player)

		prev_collision_x = self.is_colliding_x
		prev_collision_y = self.is_colliding_y

		self.is_colliding_x = False
		self.is_colliding_y = False

		if direction == 'horizontal':
			for obstacle in obstacles:
				# collision on the right
				if self.rect.right >= obstacle.rect.left and self.old_rect.right <= obstacle.old_rect.left:
					self.rect.right = obstacle.rect.left
					self.pos.x = self.rect.x
					self.is_colliding_x = True

				# collision on the left
				if self.rect.left <= obstacle.rect.right and self.old_rect.left >= obstacle.old_rect.right:
					self.rect.left = obstacle.rect.right
					self.pos.x = self.rect.x
					self.is_colliding_x = True

		if direction == 'vertical':
			for obstacle in obstacles:
				# collision on the top
				if self.rect.top <= obstacle.rect.bottom and self.old_rect.top >= obstacle.old_rect.bottom:
					self.rect.top = obstacle.rect.bottom
					self.pos.y = self.rect.y
					self.is_colliding_y = True

				# collision on the bottom
				if self.rect.bottom >= obstacle.rect.top and self.old_rect.bottom <= obstacle.old_rect.top:
					self.rect.bottom = obstacle.rect.top
					self.pos.y = self.rect.y
					self.is_colliding_y = True

		if not prev_collision_x and self.is_colliding_x:
			self.direction.x *= -1
		if not prev_collision_y and self.is_colliding_y:
			self.direction.y *= -1

	def wall_bounce(self, direction):
		if direction == 'horizontal':
			if self.rect.x <= 10:
				self.rect.x = 10
				self.pos.x = 10
				self.direction.x *= -1
			elif self.rect.right >= 1270:
				self.rect.right = 1270
				self.pos.x = self.rect.x
				self.direction.x *= -1

		if direction == 'vertical':
			if self.rect.y <= 10:
				self.rect.y = 10
				self.pos.y = 10
				self.direction.y *= -1
			elif self.rect.bottom >= 710:
				self.rect.bottom = 710
				self.pos.y = self.rect.y
				self.direction.y *= -1

	def update(self, dt):
		self.old_rect = self.rect.copy()

		if self.direction.magnitude() != 0:
			self.direction = self.direction.normalize()


		self.pos.x += self.direction.x * self.speed * dt
		self.rect.x = self.pos.x
		self.wall_bounce('horizontal')
		self.collision('horizontal')
		self.pos.y += self.direction.y * self.speed * dt
		self.rect.y = self.pos.y
		self.wall_bounce('vertical')
		self.collision('vertical')

pg.init()
screen = pg.display.set_mode((1280, 720))
screen_rect = pg.Rect(0, 0, *screen.get_size())
clock = pg.time.Clock()

# group setup
all_sprites = pg.sprite.Group()
collision_sprites = pg.sprite.Group()

# sprite setup
StaticObstacle((100,300),(100,50),[all_sprites,collision_sprites])
StaticObstacle((800,550),(100,100),[all_sprites,collision_sprites])
StaticObstacle((900,200),(200,10),[all_sprites,collision_sprites])
MovingVerticalObstacle((200,300),(200,60),[all_sprites,collision_sprites])
MovingHorizontalObstacle((850,350),(100,100),[all_sprites,collision_sprites])
player = Player(all_sprites, collision_sprites)
Ball(all_sprites, collision_sprites, player)

# loop
last_time = time.time()

while True:

	# delta time
	dt = time.time() - last_time
	last_time = time.time()

	# event loop
	for event in pg.event.get():
		if event.type == pg.QUIT:
			pg.quit()
			exit()

		elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
			pg.quit()
			exit()

	# drawing and updating the screen
	screen.fill((50, 50, 50))
	all_sprites.update(dt)
	all_sprites.draw(screen)

	for sprite in all_sprites.sprites():
		pg.draw.rect(screen, 'black', sprite.rect, 3)

	pg.draw.rect(screen, 'white', screen_rect, 10)

	# display output
	pg.display.flip()
	clock.tick(60)
