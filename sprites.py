# Sprite module for all or part of all sprites in game

import pygame as pg
from settings import *
vec = pg.math.Vector2


class Player(pg.sprite.Sprite):
    def __init__(self, game):
        self.groups = game.all_sprites, game.main
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.player_img

        self.rot = 270
        self.speed = 0
        self.vel = 0
        self.pos = vec(CENTER_OFFSET, 0).rotate(self.rot) + CENTER

        self.last_shot = 0

        self.score = 0

        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def get_keys(self):
        self.vel = 0
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vel -= PLAYER_SPEED * self.game.dt
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vel += PLAYER_SPEED * self.game.dt

        if keys[pg.K_SPACE]:
            now = pg.time.get_ticks()
            if now - self.last_shot > BULLET_RATE:
                self.last_shot = now
                Bullet(self.game, self.pos + BARREL_OFFSET.rotate(self.rot),
                       self.rot)
                self.score -= SCORE_BULLET_DECREASE

    def update(self):
        self.get_keys()
        self.speed += self.vel
        if self.speed + (PLAYER_SLOW_SPEED * self.game.dt) < 0:
            self.speed += PLAYER_SLOW_SPEED * self.game.dt
        elif self.speed < 0:
            self.speed = 0
        if self.speed - (PLAYER_SLOW_SPEED * self.game.dt) > 0:
            self.speed -= PLAYER_SLOW_SPEED * self.game.dt
        elif self.speed > 0:
            self.speed = 0
        if self.speed > PLAYER_MAX_SPEED:
            self.speed = PLAYER_MAX_SPEED
        if self.speed < -PLAYER_MAX_SPEED:
            self.speed = -PLAYER_MAX_SPEED

        self.rot += self.speed

        self.image = pg.transform.rotate(self.game.player_img, -self.rot + 180)
        self.rect = self.image.get_rect()
        self.pos = vec(CENTER_OFFSET, 0).rotate(self.rot) + CENTER
        self.rect.center = self.pos


class Text(pg.sprite.Sprite):
    def __init__(self, pos, color, parent, text, option):
        self.groups = parent.game.all_sprites, parent.game.texts
        pg.sprite.Sprite.__init__(self, self.groups)
        self.value = 0
        if option == 0:
            self.value = parent.speed
        elif option == 1:
            self.value = parent.vel
        elif option == 2:
            self.value = parent.rot
        elif option == 3:
            self.value = parent.score
        elif option == 4:
            self.value = parent.game.increase + INVADER_CHANCE
        elif option == 5:
            self.value = len(parent.game.invaders)
        elif option == 6:
            self.value = len(parent.game.bgobjects)

        self.image = parent.game.font.render(
            '{} => {}'.format(text, parent.speed), False, color)
        self.parent = parent
        self.color = color
        self.option = option
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.text = text

    def update(self):
        if self.option == 0:
            self.value = self.parent.speed
        elif self.option == 1:
            self.value = self.parent.vel
        elif self.option == 2:
            self.value = self.parent.rot
        elif self.option == 3:
            self.value = self.parent.score
        elif self.option == 4:
            self.value = self.parent.game.increase + INVADER_CHANCE
        elif self.option == 5:
            self.value = len(self.parent.game.invaders)
        elif self.option == 6:
            self.value = len(self.parent.game.bgobjects)
        self.image = self.parent.game.font.render('{} => {}'.format(
            self.text, round(self.value, 3)), False, self.color)


class Earth(pg.sprite.Sprite):
    def __init__(self, game):
        self.groups = game.all_sprites, game.main
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = game.earth_img

        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.radius = self.rect.width / 2


class Bullet(pg.sprite.Sprite):
    def __init__(self, game, pos, rot):
        self.groups = game.all_sprites, game.bullets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.transform.rotate(game.bullet_img, -rot)
        self.game = game
        self.v = vec(BULLET_SPEED, 0).rotate(rot)
        self.rot = rot
        self.pos = vec(pos)

        self.rect = self.image.get_rect()
        self.rect.center = vec(pos)
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        if pg.time.get_ticks() - self.spawn_time > BULLET_LIFETIME:
            self.kill()

        self.pos = self.pos + (self.v * self.game.dt)
        self.rect.center = self.pos


class Invader(pg.sprite.Sprite):
    def __init__(self, game, pos, vel, rot, rot_speed, image):
        self.groups = game.all_sprites, game.invaders
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        self.pos = pos
        self.vel = vel
        self.rot = rot
        self.rot_speed = rot_speed

        self.main_img = image
        self.image = pg.transform.rotate(self.main_img, self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.radius = self.rect.width / 2

    def update(self):
        self.pos = self.pos + (self.vel * self.game.dt)
        self.rot += self.rot_speed * self.game.dt
        if self.rot > 360:
            self.rot -= 360
        elif self.rot < 0:
            self.rot += 360
        self.image = pg.transform.rotate(self.main_img, self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos


class Star(pg.sprite.Sprite):
    def __init__(self, game, pos, vel, rot, rot_speed):
        self.groups = game.all_sprites, game.bgobjects
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        self.pos = pos
        self.vel = vel
        self.rot = rot
        self.rot_speed = rot_speed

        self.main_img = game.star_img
        self.image = pg.transform.rotate(self.main_img, self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def update(self):
        self.pos = self.pos + (self.vel * self.game.dt)
        self.rot += self.rot_speed * self.game.dt
        if self.rot > 360:
            self.rot -= 360
        elif self.rot < 0:
            self.rot += 360
        self.image = pg.transform.rotate(self.main_img, self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos


class Explosion(pg.sprite.Sprite):
    def __init__(self, game, pos):
        self.groups = game.all_sprites, game.explosions
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = game.explosion_imgs[1]
        self.rect = self.image.get_rect()
        self.game = game

        self.pos = pos
        self.rect.center = pos
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        lifetime = pg.time.get_ticks() - self.spawn_time
        if lifetime > len(EXPLOSION_IMGS) * 15:
            self.kill()
        self.image = self.game.explosion_imgs[int(lifetime / 16) - 1]
