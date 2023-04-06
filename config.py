vertical_tile_number = 10

tile_size = (90, 90)  # (RESIZABLE)
# player_size_ratio = 1.5  # height / width
player_full_size = (288, 192)  # size of the entire frame from the sprite sheet  (RESIZABLE)
player_frame_size = 120, 80  # frame scaled down  (STATIC)
player_real_size = (54, 90)  # borders of the character inside that frame  (RESIZABLE)

FPS = 60
TARGET_FPS = 60

BACKGROUND_LIST = [f'assets/backgrounds/background {n}.png' for n in range(1, 9)]
