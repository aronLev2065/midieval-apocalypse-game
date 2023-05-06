from os import walk
import pygame as pg
from csv import reader
from config import tile_size


def import_csv_layout(path):
	# import csv file and return a list of 'numbers'
	layout = []
	with open(path) as level_map:
		level = reader(level_map, delimiter=',')
		for row in level:
			layout.append(list(row))

	return layout


def import_cut_graphics(path, size):
	# takes a tileset and cuts it in tiles; returns list of surfaces
	surface = pg.image.load(path).convert_alpha()
	tile_num_x = surface.get_width() // size[0]
	tile_num_y = surface.get_height() // size[1]
	graphics = []
	for row in range(tile_num_y):
		for col in range(tile_num_x):
			x = col * size[0]
			y = row * size[1]
			new_surface = pg.Surface(size, flags=pg.SRCALPHA)
			new_surface.blit(surface, (0, 0), pg.Rect(x, y, *size))
			graphics.append(new_surface)

	return graphics


def import_folder(path):
	# takes all images from the folder[path] and puts them on pg.surface; returns a list of these surfaces
	surfaces = []

	for _, __, img_files in walk(path):
		for img_file in img_files:
			full_path = path + img_file
			image = pg.image.load(full_path).convert_alpha()
			surfaces.append(image)

	return surfaces

# def import_button_folder(path):
# 	buttons = {}
# 	for _, __, img_files in walk(path):
# 		for img_file in img_files:
# 			full_path = path + img_file
# 			image = pg.image.load(full_path).convert_alpha()
# 			img_file = img_file.replace('.png', '')
# 			img_file = img_file.replace(' button', '')
# 			buttons[img_file] = image
# 			print(img_file, buttons[img_file])
# 	return buttons
