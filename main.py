# MineFuf
# Circle Invaders!
# Main file with class Game

import pygame as pg
import random
from settings import *
from sprites import *
from os import path
from random import randint, choice
vec = pg.math.Vector2


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
        self.explosions = pg.sprite.Group()
        self.main = pg.sprite.Group()
        self.texts = pg.sprite.Group()
        self.bgobjects = pg.sprite.Group()

        self.increase = 0
        self.step = 1
        self.step_checked = 0
        self.player = Player(self)
        self.earth = Earth(self)

        self.score_text = Text(vec(30, HEIGHT - 30),
                               YELLOW, self.player, 'Score', 3)

        self.invaders_text = Text(
            vec(30, 30), RED, self.player, 'Invaders', 5)

        self.run()

    def load_data(self):
        # Load game data
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img')
        explosion_folder = path.join(img_folder, 'explosions')
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
        self.bgobject_imgs = []
        for img_path in BGOBJECT_IMGS:
            self.bgobject_imgs.append(
                pg.image.load(
                    path.join(img_folder, img_path)))
        self.invader_imgs = [pg.transform.rotozoom(
            pg.image.load(
                path.join(
                    img_folder, img)), 0, 1 / 20) for img in INVADER_IMGS]
        self.explosion_imgs = []
        for img_path in EXPLOSION_IMGS:
            sur = pg.image.load(path.join(explosion_folder, img_path))
            sur.set_colorkey(BLACK)
            self.explosion_imgs.append(sur)
        # self.explosion_imgs = [pg.transform.rotozoom(
        #     pg.image.load(
        #         path.join(
        #             explosion_folder, img)),
        #     0, 1) for img in EXPLOSION_IMGS]
        self.font = pg.font.SysFont(
            'consolas', 20, bold=50, italic=0, constructor=None)
        self.title_font = pg.font.SysFont(
            'consolas', 50, bold=50, italic=0, constructor=None)

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
        self.chance_for_bgobject()
        self.chance_for_enemy()
        self.all_sprites.update()
        hits = pg.sprite.groupcollide(
            self.invaders, self.bullets, False, False)
        for hit in hits:
            if isinstance(hit, Invader):
                pos = vec(hit.pos)
                hit.kill()
                Explosion(self, pos)
                self.player.score += KILL_SCORE

        if self.player.score > SCORE_STEP * self.step and \
                self.step_checked < self.step:
            self.step += 1
            self.increase += SCORE_INVADER_INCREASE

        for invader in self.invaders:
            if pg.sprite.collide_circle(self.earth, invader):
                print('DONE')
                self.playing = False

        for object in self.bgobjects:
            if not SCREEN_WITH_OFFSET.colliderect(object.rect):
                object.kill()

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
        self.screen.fill(BGCOLOR)
        # self.all_sprites.draw(self.screen)
        self.bgobjects.draw(self.screen)
        self.bullets.draw(self.screen)
        self.invaders.draw(self.screen)
        self.main.draw(self.screen)
        self.explosions.draw(self.screen)
        self.texts.draw(self.screen)
        pg.display.set_caption('{} => {}'.format(
            TITLE, round(self.clock.get_fps(), 2)))
        # *after* drawing everything, flip the display
        pg.display.flip()

    def show_start_screen(self):
        # game splash/start screen
        self.screen.fill(BGCOLOR)
        title = self.title_font.render(TITLE, False, TITLE_COLOR)
        title_rect = title.get_rect()
        title_rect.center = TITLE_POS
        answered = False
        while not answered:
            self.events()
            keys = pg.key.get_pressed()
            for key in keys:
                if key:
                    answered = True

            self.screen.fill(BGCOLOR)
            self.screen.blit(title, title_rect)
            pg.display.flip()

    def show_go_screen(self):
        # game over/continue
        pass

    def chance_for_enemy(self):
        chance = round(randint(
            0, int(1 / (INVADER_CHANCE + self.increase)) * 10) / 10, 0)
        if chance == 0:
            img = choice(self.invader_imgs)
            facing = randint(0, 360)
            pos = vec(INVADER_OFFSET, 0).rotate(facing) + CENTER
            vel = vec(randint(INVADER_MIN_SPEED, INVADER_MAX_SPEED),
                      0).rotate(facing - 180)
            rot = randint(0, 360)
            rot_speed = randint(INVADER_MIN_ROT_SPEED, INVADER_MAX_ROT_SPEED)
            Invader(self, pos, vel, rot, rot_speed, img)

    def chance_for_bgobject(self):
        chance = round(randint(
            0, int(1 / (BGOBJECT_CHANCE)) * 10) / 10, 0)
        if chance == 0:
            img = choice(self.bgobject_imgs)
            facing = randint(0, 360)
            pos = vec(BGOBJECT_OFFSET, 0).rotate(facing) + CENTER
            vel = vec(randint(BGOBJECT_MIN_SPEED, BGOBJECT_MAX_SPEED),
                      0).rotate(facing - 180)
            rot = randint(0, 360)
            rot_speed = randint(BGOBJECT_MIN_ROT_SPEED, BGOBJECT_MAX_ROT_SPEED)
            BGObject(self, pos, vel, rot, rot_speed, img)


g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()
