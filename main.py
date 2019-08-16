# MineFuf
# Circle Invaders!

import pygame as pg
import random
from settings import *
from sprites import *
from os import path
from random import randint


class Game:
    def __init__(self):
        # initialize game window, etc
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.load_data()

    def new(self):
        # start a new game
        self.all_sprites = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.invaders = pg.sprite.Group()

        self.player = Player(self)
        self.earth = Earth(self)
        self.run()

    def load_data(self):
        # Load game data
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img')
        self.player_img = pg.transform.rotozoom(
            pg.image.load(
                path.join(
                    img_folder, PLAYER_IMG)), 90, 1 / 15)
        self.earth_img = pg.transform.rotozoom(
            pg.image.load(
                path.join(
                    img_folder, EARTH_IMG)), 0, 1 / 2)
        self.bullet_img = pg.transform.rotozoom(
            pg.image.load(
                path.join(
                    img_folder, BULLET_IMG)), 270, 1 / 20)
        self.font = pg.font.SysFont(
            'consolas', 20, bold=50, italic=0, constructor=None)

    def run(self):
        # Game Loop
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def update(self):
        # Game Loop - Update
        self.chance_for_enemy()
        self.all_sprites.update()

    def events(self):
        # Game Loop - events
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

    def draw(self):
        # Game Loop - draw
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        pg.display.set_caption('{} => {}'.format(
            TITLE, round(self.clock.get_fps(), 2)))
        # *after* drawing everything, flip the display
        pg.display.flip()

    def show_start_screen(self):
        # game splash/start screen
        pass

    def show_go_screen(self):
        # game over/continue
        pass

    def chance_for_enemy(self):
        pass


g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()
