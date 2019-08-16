# Sprite module for all or part of all sprites in game

import pygame as pg
from settings import *
vec = pg.math.Vector2


class Player(pg.sprite.Sprite):
    def __init__(self, game):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.player_img
        self.rect = self.image.get_rect()
        self.rot = 270
        self.speed = 0
        self.speed_text = Speed_text((30, 30), WHITE, self)
        self.game.all_sprites.add(self.speed_text)
        self.rect.centerx = vec(75, 0).rotate(self.rot).x + CENTER[0]
        self.rect.centery = vec(75, 0).rotate(self.rot).y + CENTER[1]

    def update(self):
        vel = 0
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            vel -= PLAYER_SPEED * self.game.dt
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            vel += PLAYER_SPEED * self.game.dt

        if keys[pg.K_SPACE]:
            Bullet(self.game, self.rect.center, self.rot)

        self.speed += vel
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
        self.rect.center = (vec(100, 0).rotate(self.rot).x + CENTER[0],
                            vec(100, 0).rotate(self.rot).y + CENTER[1])


class Speed_text(pg.sprite.Sprite):
    def __init__(self, pos, color, parent):
        pg.sprite.Sprite.__init__(self)
        self.image = parent.game.font.render(
            'Vel => {}'.format(parent.speed), False, color)
        self.parent = parent
        self.color = color
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

    def update(self):
        self.image = self.parent.game.font.render('Vel => {}'.format(
            round(self.parent.speed, 2)), False, self.color)


class Earth(pg.sprite.Sprite):
    def __init__(self, game):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = game.earth_img
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)


class Bullet(pg.sprite.Sprite):
    def __init__(self, game, pos, rot):
        self.groups = game.all_sprites, game.bullets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.v = vec(BULLET_SPEED, 0).rotate(rot)
        self.rot = rot
        self.image = pg.transform.rotate(game.bullet_img, -rot)
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        if pg.time.get_ticks() - self.spawn_time > BULLET_LIFETIME:
            self.kill()

        self.rect.centerx += self.v.x * self.game.dt
        self.rect.centery += self.v.y * self.game.dt
