csv_graphics = {
	'blocks': 'levels/level 1/level_blocks.csv',  #
	'door bg': 'levels/level 1/level_door bg.csv',  #
	'door fg': 'levels/level 1/level_door fg.csv',  #
	'coins': 'levels/level 1/level_coins.csv',  #
	'enemies': 'levels/level 1/level_enemies.csv',
	'fire': 'levels/level 1/level_fire.csv',  #
	'lava': 'levels/level 1/level_lava.csv',  #
	'player': 'levels/level 1/level_player.csv',
	'torch': 'levels/level 1/level_torch.csv',  #
	'borders': 'levels/level 1/level_borders.csv',
	'background': 'levels/level 1/level_background.csv',
	'decoration': 'levels/level 1/level_decoration.csv',
	'node_pos': (150, 400),
	'unlock': 1
}

png_graphics = {
	'background': 'assets/tile assets/tiles/background 1 tileset.png',
	'bg torch': 'assets/tile assets/tiles/background torch.png',
	'blocks': 'assets/tile assets/tiles/brick tileset.png',
	'coins': 'assets/tile assets/tiles/coin.png',
	'door': 'assets/tile assets/tiles/door.png',
	'enemies': 'assets/enemies/enemy sprites/',  # FOLDER
	'fire': 'assets/tile assets/tiles/fire.png',
	'lava': 'assets/tile assets/tiles/lava.png',
	'torch': 'assets/tile assets/tiles/torch.png',
	'player': 'assets/character/knight.png',
	'healthbar': 'assets/ui/health_bar.png'
}

spritesheet_animations = {
	# sprite sheets
	'coins': 'assets/tile assets/tiles/coin animation.png',
	'collect': 'assets/tile assets/tiles/collect coin.png',
	'fire': 'assets/tile assets/tiles/fire animation.png',
	'torch': 'assets/tile assets/tiles/torch animation.png',
	'lava': 'assets/tile assets/tiles/lava animation.png'
}

folder_animations = {
	# folders
	'skeleton': {
		'attack': 'assets/enemies/Skeleton/attack/',
		'death': 'assets/enemies/Skeleton/death/',
		'run': 'assets/enemies/Skeleton/walk/',
		'take hit': 'assets/enemies/Skeleton/take hit/',
		'idle': 'assets/enemies/Skeleton/idle/',
	},

	'eye': {
		'attack': 'assets/enemies/Flying eye/attack/',
		'death': 'assets/enemies/Flying eye/death/',
		'run': 'assets/enemies/Flying eye/flight/',
		'idle': 'assets/enemies/Flying eye/flight/',
		'take hit': 'assets/enemies/Flying eye/take hit/',
	},

	'goblin': {
		'attack': 'assets/enemies/Goblin/attack/',
		'death': 'assets/enemies/Goblin/death/',
		'run': 'assets/enemies/Goblin/run/',
		'take hit': 'assets/enemies/Goblin/take hit/',
		'idle': 'assets/enemies/Goblin/idle/',
	},

	'mushroom': {
		'attack': 'assets/enemies/Mushroom/attack/',
		'death': 'assets/enemies/Mushroom/death/',
		'run': 'assets/enemies/Mushroom/run/',
		'take hit': 'assets/enemies/Mushroom/take hit/',
		'idle': 'assets/enemies/Mushroom/idle/',
	},

	'jump': 'assets/dust particles/jump/',
	'run': 'assets/dust particles/run/',
	'land': 'assets/dust particles/land/',
	'torch': 'assets/tile assets/tiles/torch animation/',
}

button_images = {
	'start': ['assets/ui/buttons/start button.png', 'assets/ui/buttons/start button hovered.png'],
	'restart': ['assets/ui/buttons/restart button.png', 'assets/ui/buttons/restart button hovered.png'],
	'pause': ['assets/ui/buttons/pause button.png', 'assets/ui/buttons/pause button hovered.png'],
	'quit': ['assets/ui/buttons/quit button.png', 'assets/ui/buttons/quit button hovered.png'],
	'sound_off': ['assets/ui/buttons/mute sound button.png', 'assets/ui/buttons/mute sound button hovered.png'],
	'sound_on': ['assets/ui/buttons/sound button.png', 'assets/ui/buttons/sound button hovered.png'],
	'music_off': ['assets/ui/buttons/mute music button.png', 'assets/ui/buttons/mute music button hovered.png'],
	'music_on': ['assets/ui/buttons/music button.png', 'assets/ui/buttons/music button hovered.png'],
	'settings': ['assets/ui/buttons/settings button.png', 'assets/ui/buttons/settings button hovered.png'],
	'back': ['assets/ui/buttons/back button.png', 'assets/ui/buttons/back button hovered.png'],
}

audio_paths = {
	'level': {
		'bg': 'assets/audio/level bg.wav',
		'complete': 'assets/audio/level complete.wav',
		'fail': 'assets/audio/game over.wav'
	},
	'player': {
		'attack': 'assets/audio/player attack 1.wav',
		'land': 'assets/audio/player land.wav',
		'death': 'assets/audio/player death.wav',
		'burn': 'assets/audio/player burn.flac',
		'hit': 'assets/audio/hit.wav',
	},
	'enemy': {
		'hit': 'assets/audio/hit.wav',
		'death': 'assets/audio/enemy death.wav',
		'attack': {
			'skeleton': 'assets/audio/skeleton attack.wav',
			'eye': 'assets/audio/enemy bite.wav',
			'mushroom': '',
			'goblin': 'assets/audio/skeleton attack.wav',
		},
	},
	'coin': {
		'collect': 'assets/audio/coin.mp3',
	},
	'button': 'assets/audio/button click.wav',
	'torch': 'assets/audio/torch burning.wav'
}
