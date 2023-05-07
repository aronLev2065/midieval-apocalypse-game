from sys import exit
import pygame as pg
from time import time
from config import FPS
from game import Game

pg.init()
screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
pg.display.set_caption('Medieval Apocalypse')
screen_width = screen.get_width()
screen_height = screen.get_height()

clock = pg.time.Clock()

game = Game(screen, 'menu')

last_time = time()

while True:
	mouse_down = False
	mouse_pos = pg.mouse.get_pos()

	for event in pg.event.get():
		if event.type == pg.QUIT:
			pg.quit()
			exit()
		if event.type == pg.MOUSEBUTTONUP:
			mouse_down = True

	keys = pg.key.get_pressed()

	dt = time() - last_time
	last_time = time()

	game.run(dt, keys, mouse_down, mouse_pos)

	if not game.running:
		break

	pg.display.flip()
	clock.tick(FPS)

pg.quit()
exit()
