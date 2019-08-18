# MineFuf
# Circle Invaders!
# Main file with class Game

import pygame as pg
import random
from settings import *
from sprites import *
from os import path
from random import randint, choice, uniform
vec = pg.math.Vector2


class Game:
    def __init__(self):
        # initialize game window, etc
        pg.init()
        pg.mixer.init()
        self.screen = pg.Surface((WIDTH, HEIGHT))
        self.screen_rect = self.screen.get_rect()
        self.screen_rect.center = SCREEN_CENTER
        print('Game field is {}:{}'.format(WIDTH, HEIGHT))
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
        self.objects = pg.sprite.Group()
        self.bombs = pg.sprite.Group()
        self.items = pg.sprite.Group()

        self.increase = 0
        self.step = 1
        self.step_checked = 0
        self.shields = 1
        self.booster = 0
        self.player = Player(self)
        # self.h1 = Helper(self, self.player, 180)
        # self.b1 = Bomb(self, BOMB_OFFSET.rotate(30) + CENTER)
        self.earth = Earth(self)

        self.score_text = Text(vec(30, HEIGHT - 30), YELLOW, self.player, 'Score', 3)
        self.shields_text = Text(vec(30, 30), BLUE, self.player, 'Shields', 7)
        self.booster_text = Text(vec(30, 60), RED, self.player, 'Boosters', 8)
        self.fps_text = Text(vec(30, 90), GREEN, self.player, 'FPS', 9)

        # self.invaders_text = Text(
        #     vec(30, 30), RED, self.player, 'Invaders', 5)

        self.run()

    def load_data(self):
        # Load game data
        self.load_images()

        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img')
        explosion_folder = path.join(img_folder, 'explosions')
        item_folder = path.join(img_folder, 'items')
        self.bgobject_imgs = []
        self.explosion_imgs = []
        self.invader_imgs = []
        self.item_imgs = {}

        for img_path in BGOBJECT_IMGS:
            self.bgobject_imgs.append(pg.image.load(path.join(img_folder, img_path)).convert_alpha())
        for img_path in INVADER_IMGS:
            sur = pg.image.load(path.join(img_folder, img_path)).convert_alpha()
            surwidth = int(WIDTH / 16)
            surheight = int(surwidth / (sur.get_rect().width / sur.get_rect().height))
            self.invader_imgs.append(pg.transform.scale(sur, (surwidth, surheight)))

        for img_path in EXPLOSION_IMGS:
            sur = pg.image.load(path.join(explosion_folder, img_path))
            sur.set_colorkey(BLACK)
            self.explosion_imgs.append(sur)

        for img_path in ITEM_IMGS:
            sur = pg.image.load(path.join(item_folder, ITEM_IMGS[img_path])).convert_alpha()
            surwidth = min(int(WIDTH / 21), 24)
            surheight = int(surwidth / (sur.get_rect().width / sur.get_rect().height))
            self.item_imgs[img_path] = pg.transform.scale(sur, (surwidth, surheight))

        self.font = pg.font.SysFont(
            GAME_FONT, min(int(WIDTH / 25.6), 20), bold=50, italic=0, constructor=None)
        self.title_font = pg.font.SysFont(
            GAME_FONT, int(WIDTH / 15), bold=50, italic=0, constructor=None)

    def load_images(self):
        # Load game data
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img')
        explosion_folder = path.join(img_folder, 'explosions')
        item_folder = path.join(img_folder, 'items')

        sur = pg.image.load(path.join(img_folder, PLAYER_IMG)).convert_alpha()
        surwidth = int(WIDTH / 8)
        surheight = int(surwidth / (sur.get_rect().width / sur.get_rect().height))
        self.player_img = pg.transform.rotate(pg.transform.scale(sur, (surwidth, surheight)), 90)

        sur = pg.image.load(path.join(img_folder, EARTH_IMG)).convert_alpha()
        surwidth = int(WIDTH / 4)
        surheight = int(surwidth / (sur.get_rect().width / sur.get_rect().height))
        self.earth_img = pg.transform.scale(pg.image.load(path.join(img_folder, EARTH_IMG)), (surwidth, surheight))

        sur = pg.image.load(path.join(img_folder, BULLET_IMG)).convert_alpha()
        surwidth = int(WIDTH / 100)
        surheight = int(surwidth / (sur.get_rect().width / sur.get_rect().height))
        self.bullet_img = pg.transform.rotate(pg.transform.scale(sur, (surwidth, surheight)), 270)

        sur = pg.image.load(path.join(img_folder, HELPER_IMG)).convert_alpha()
        surwidth = int(WIDTH / 10)
        surheight = int(surwidth / (sur.get_rect().width / sur.get_rect().height))
        self.helper_img = pg.transform.rotate(pg.transform.scale(sur, (surwidth, surheight)), 90)

        sur = pg.image.load(path.join(img_folder, BOMB_IMG)).convert_alpha()
        surwidth = int(WIDTH / 20)
        surheight = int(surwidth / (sur.get_rect().width / sur.get_rect().height))
        self.bomb_img = pg.transform.scale(sur, (surwidth, surheight))

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
        hits = pg.sprite.groupcollide(self.invaders, self.bullets, False, False)
        for hit in hits:
            if isinstance(hit, Invader):
                Explosion(self, hit.pos)
                self.chance_for_item(hit.pos, hit.vel)
                hit.kill()
                self.player.score += KILL_SCORE

        for item in self.items:
            if pg.sprite.collide_mask(self.player, item):
                item.use()
                item.kill()

        if self.player.score > SCORE_STEP * self.step and \
                self.step_checked < self.step:
            self.step += 1
            self.increase += SCORE_INVADER_INCREASE

        for invader in self.invaders:
            if pg.sprite.collide_circle(self.earth, invader):
                Explosion(self, invader.pos)
                invader.kill()
                if self.shields > 0:
                    self.shields -= 1
                else:
                    self.playing = False

        for object in self.all_sprites:
            if not isinstance(object, Rate_Booster):
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

        for idx, key in enumerate(pg.key.get_pressed()):
            if idx == pg.K_ESCAPE and key:
                if self.playing:
                    self.playing = False
                self.running = False

    def draw(self):
        # Game Loop - draw
        self.screen.fill(BGCOLOR)
        SCREEN.fill(BGCOLOR)
        # self.all_sprites.draw(self.screen)
        self.bgobjects.draw(self.screen)
        self.bullets.draw(self.screen)
        self.invaders.draw(self.screen)
        self.objects.draw(self.screen)
        self.items.draw(self.screen)
        self.main.draw(self.screen)
        self.explosions.draw(self.screen)
        self.texts.draw(self.screen)
        pg.display.set_caption('{} => {}'.format(
            TITLE, round(self.clock.get_fps(), 2)))
        # *after* drawing everything, flip the display
        # print('Pos to blit is {}:{}'.format((SCREEN_WIDTH - WIDTH) // 2, (SCREEN_HEIGHT - HEIGHT) // 2))
        SCREEN.blit(self.screen, self.screen_rect)
        pg.display.flip()

    def show_start_screen(self):
        # game splash/start screen
        self.screen.fill(BGCOLOR)
        title = self.title_font.render(TITLE, False, TITLE_COLOR)
        title_rect = title.get_rect()
        title_rect.center = TITLE_POS
        answered = False
        while not answered:
            self.clock.tick(FPS)
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
        chance = round(uniform(
            0, int(1 / (INVADER_CHANCE + self.increase)) * 10 - 10) / 10, 0)
        if chance == 0:
            img = choice(self.invader_imgs)
            facing = uniform(0, 360)
            pos = vec(INVADER_OFFSET, 0).rotate(facing) + CENTER
            vel = vec(uniform(INVADER_MIN_SPEED, INVADER_MAX_SPEED),
                      0).rotate(facing - 180)
            rot = uniform(0, 360)
            rot_speed = uniform(INVADER_MIN_ROT_SPEED, INVADER_MAX_ROT_SPEED)
            Invader(self, pos, vel, rot, rot_speed, img)

    def chance_for_bgobject(self):
        chance = round(randint(
            0, int(1 / (BGOBJECT_CHANCE)) * 10 - 10) / 10, 0)
        if chance == 0:
            img = choice(self.bgobject_imgs)
            facing_pos = uniform(0, 360)
            pos = vec(BGOBJECT_OFFSET, 0).rotate(facing_pos) + CENTER
            facing = uniform(0, 360)
            vel = vec(
                uniform(
                    BGOBJECT_MIN_SPEED, BGOBJECT_MAX_SPEED), 0).rotate(facing)
            rot = uniform(0, 360)
            rot_speed = uniform(BGOBJECT_MIN_ROT_SPEED, BGOBJECT_MAX_ROT_SPEED)
            BGObject(self, pos, vel, rot, rot_speed, img)

    def chance_for_item(self, pos, vel):
        chance = round(uniform(
            0, int(1 / (ITEM_CHANCE)) * 10 - 10) / 10, 0)
        if chance == 0.0:
            item = choice(ITEMS_CHANCE)
            Item(self, pos, item, vel)


g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()
