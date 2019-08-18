# Option module for simplified adjusting game

import pygame as pg
import ctypes
vec = pg.math.Vector2

ctypes.windll.user32.SetProcessDPIAware()
true_res = (ctypes.windll.user32.GetSystemMetrics(0), ctypes.windll.user32.GetSystemMetrics(1))

# game options/settings
SCREEN = pg.display.set_mode(true_res, pg.FULLSCREEN | pg.DOUBLEBUF)
SCREEN_WIDTH = SCREEN.get_width()
SCREEN_HEIGHT = SCREEN.get_height()
print('Screen size is {}:{}'.format(SCREEN_WIDTH, SCREEN_HEIGHT))
WIDTH = min(SCREEN.get_width(), SCREEN.get_height())
HEIGHT = WIDTH
SCREEN_OFFSET = WIDTH / 2
SCREEN_WITH_OFFSET = pg.Rect(-SCREEN_OFFSET, -SCREEN_OFFSET,
                             WIDTH + 2 * SCREEN_OFFSET,
                             HEIGHT + 2 * SCREEN_OFFSET)
FPS = 120
CENTER = vec(WIDTH / 2, HEIGHT / 2)
SCREEN_CENTER = vec(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
GAME_FONT = 'consolas'
# GAME_FONT = 'arial'


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
TITLE_POS = vec(WIDTH / 2, HEIGHT / 4)
TITLE_COLOR = LIGHT_GREY
TITLE_BCCOLOR = DARK_GREY

# Player's settings
PLAYER_SPEED = 30
PLAYER_SLOW_SPEED = 10
PLAYER_MAX_SPEED = 25
PLAYER_IMG = 'player011.png'
PLAYER_FIRE_RATE = 120
CENTER_OFFSET = vec(WIDTH / 5.5, 0)
BARREL_OFFSET = vec(WIDTH / 42.5, 0)

# Invader's settings
INVADER_CHANCE = 0.02
INVADER_OFFSET = vec(WIDTH / 1.3, 0)
INVADER_MIN_SPEED = WIDTH / 51.2
INVADER_MAX_SPEED = WIDTH / 10.2
INVADER_MIN_ROT_SPEED = 30
INVADER_MAX_ROT_SPEED = 360
INVADER_IMGS = [
    'meteor011.png',
    'meteor012.png',
    'meteor013.png',
    'meteor014.png'
]

# Bullet's settings
BULLET_SPEED = WIDTH / 0.7
BULLET_LIFETIME = 1000
BULLET_IMG = 'bullet002.png'

# Earth's settings
EARTH_IMG = 'earth002.png'
EARTH_ROT_SPEED = 5

# Score's settings
SCORE_STEP = 10000
SCORE_INVADER_INCREASE = 0.003
SCORE_BULLET_DECREASE = 100
KILL_SCORE = 1100

# Explosion effect's settings
ONE_TICK = 16
EXPLOSION_IMGS = ['explosion{}.png'.format(img) for img in range(1, 64, 1)]

# BackGround objects ()
BGOBJECT_CHANCE = 0.02
BGOBJECT_OFFSET = vec(WIDTH / 1.3, 0)
BGOBJECT_MIN_ROT_SPEED = 10
BGOBJECT_MAX_ROT_SPEED = 15
BGOBJECT_MIN_SPEED = WIDTH / 102.5
BGOBJECT_MAX_SPEED = WIDTH / 17
BGOBJECT_IMGS = [
    'bgobj1.png',
    'bgobj2.png',
    'bgobj3.png',
]

# Helper's settings
HELPER_LIFETIME = 15000
HELPER_IMG = 'helper011.png'
HELPER_FIRE_RATE = 350

# Bomb's settings
BOMB_OFFSET = vec(WIDTH / 3.5, 0)
BOMB_IMG = 'bomb001.png'

# Rate Booster's settings
BOOSTER_LIFETIME = 15000

# Items properities
ITEMS = {
    'bomb': 12,
    'helper': 6,
    'shield': 3,
    'tornado': 1,
    'rate_booster': 6
}
# ITEMS = {
#     'bomb': 1,
#     'helper': 10,
#     'shield': 1,
#     'tornado': 1,
#     'rate_booster': 1
# }
ITEMS_CHANCE = []
for item in ITEMS:
    for chance in range(0, ITEMS[item]):
        ITEMS_CHANCE.append(item)
ITEM_CHANCE = 0.3
ITEM_IMGS = {'bomb': 'bomb_item002.png',
             'helper': 'helper_item002.png',
             'shield': 'shield_item001.png',
             'tornado': 'tornado_item001.png',
             'rate_booster': 'rate_booster_item001.png'
             }
# print(ITEMS)
# print(ITEMS_CHANCE)
# print(ITEM_IMGS)
