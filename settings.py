import pygame as pg
vec = pg.math.Vector2


# game options/settings
WIDTH = 512
HEIGHT = 512
FPS = 60
CENTER = vec(WIDTH / 2, HEIGHT / 2)


# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHT_BLUE = (21, 133, 189)
DARK_GREY = (32, 32, 32)
LIGHT_GREY = (128, 128, 128)

BGCOLOR = BLACK

# Title's settings
TITLE = "Circle Invaders!"
TITLE_POS = vec(WIDTH / 2, 75)
TITLE_COLOR = LIGHT_GREY
TITLE_BCCOLOR = DARK_GREY

# Player's settings
PLAYER_SPEED = 30
PLAYER_SLOW_SPEED = 10
PLAYER_MAX_SPEED = 25
PLAYER_IMG = 'player001.png'
CENTER_OFFSET = 90
BARREL_OFFSET = vec(15, 0)

# Invader's settings
INVADER_CHANCE = 0.02
INVADER_OFFSET = vec(400, 0)
INVADER_MIN_ROT_SPEED = 30
INVADER_MAX_ROT_SPEED = 360
INVADER_MIN_SPEED = 10
INVADER_MAX_SPEED = 50
INVADER_IMGS = [
    'meteor001.png',
    'meteor002.png',
    'meteor003.png',
    'meteor004.png'
]

# Bullet's settings
BULLET_SPEED = 750
BULLET_LIFETIME = 1000
BULLET_RATE = 120
BULLET_IMG = 'bullet001.png'

# Earth's settings
EARTH_IMG = 'earth001.png'

# Score's settings
SCORE_STEP = 10000
SCORE_INVADER_INCREASE = 0.005
SCORE_BULLET_DECREASE = 100
KILL_SCORE = 1100
