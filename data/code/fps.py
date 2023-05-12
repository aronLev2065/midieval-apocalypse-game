import pygame as pg

def draw_fps(screen, pos, clock):
	fps = round(clock.get_fps())
	font = pg.font.SysFont('Arial', 30)
	fps_surface = font.render(f'fps: {str(fps)}', True, 'white')
	screen.blit(fps_surface, pos)
