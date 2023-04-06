import pygame as pg
from game_data import csv_graphics


class Node(pg.sprite.Sprite):
	def __init__(self, pos, available):
		super().__init__()
		self.image = pg.Surface((100, 100))
		if available:
			self.image.fill('green')
		else:
			self.image.fill('red')
		self.rect = self.image.get_rect(center=pos)
		self.available = available

		self.detection_zone = pg.Rect(self.rect.centerx-4, self.rect.centery-4, 8, 8)


class Icon(pg.sprite.Sprite):
	def __init__(self, pos):
		super().__init__()
		self.image = pg.Surface((40, 40))
		self.image.fill('blue')
		self.rect = self.image.get_rect(center=pos)
		self.pos = self.rect.center

	def update(self):
		self.rect.center = self.pos

class Overworld:
	def __init__(self, start_level, max_level, surface, create_level):
		# setup
		self.display_surface = surface
		self.max_level = max_level
		self.current_level = start_level
		self.create_level = create_level

		# sprites
		self.setup_nodes()
		self.setup_icon()

		# movement
		self.move_direction = pg.math.Vector2(0, 0)
		self.speed = 20
		self.moving = False

	def setup_nodes(self):
		self.nodes = pg.sprite.Group()
		for i, node_data in enumerate(levels.values()):
			if i <= self.max_level:
				available = True
			else:
				available = False

			node_sprite = Node(node_data['node_pos'], available)
			self.nodes.add(node_sprite)

	def setup_icon(self):
		self.icon = pg.sprite.GroupSingle()
		icon_sprite = Icon(levels[self.current_level]['node_pos'])
		self.icon.add(icon_sprite)

	def draw_paths(self):
		points = [node['node_pos'] for i, node in enumerate(levels.values()) if i <= self.max_level]
		if len(points) >= 2:
			pg.draw.lines(self.display_surface, 'green', False, points, 10)

	def get_input(self):
		keys = pg.key.get_pressed()
		if not self.moving:
			if (keys[pg.K_a] or keys[pg.K_LEFT]) and self.current_level > 0:
				self.move_direction = self.get_movement_data()
				self.current_level -= 1
				self.moving = True
			elif (keys[pg.K_d] or keys[pg.K_RIGHT]) and self.current_level < self.max_level:
				self.move_direction = self.get_movement_data(is_next=True)
				self.current_level += 1
				self.moving = True
			elif keys[pg.K_SPACE]:
				self.create_level(self.current_level)

	def update_icon(self):
		if self.moving and self.move_direction:
			icon = self.icon.sprite
			icon.pos += self.move_direction * self.speed
			target_node = self.nodes.sprites()[self.current_level]
			if icon.rect.colliderect(target_node.detection_zone):
				self.moving = False
				icon.pos = target_node.rect.center

	def get_movement_data(self, is_next=False):
		start = pg.math.Vector2(self.nodes.sprites()[self.current_level].rect.center)
		end = pg.math.Vector2(self.nodes.sprites()[self.current_level-1].rect.center)
		if is_next:
			end = pg.math.Vector2(self.nodes.sprites()[self.current_level+1].rect.center)
			return (end-start).normalize()
		return (end-start).normalize()

	def run(self):
		self.get_input()
		self.update_icon()

		self.draw_paths()
		self.nodes.update()
		self.nodes.draw(self.display_surface)
		self.icon.update()
		self.icon.draw(self.display_surface)
