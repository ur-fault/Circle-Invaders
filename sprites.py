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
        self.speed_text = Speed_text(30, 30, WHITE, self)
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
        self.rect.centerx = vec(100, 0).rotate(self.rot).x + CENTER[0]
        self.rect.centery = vec(100, 0).rotate(self.rot).y + CENTER[1]


class Speed_text(pg.sprite.Sprite):
    def __init__(self, x, y, color, parent):
        pg.sprite.Sprite.__init__(self)
        self.image = parent.game.font.render(
            'Vel => {}'.format(parent.speed), False, color)
        self.parent = parent
        self.color = color
        self.pos = (x, y)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def update(self):
        self.image = self.parent.game.font.render('Vel => {}'.format(
            round(self.parent.speed, 2)), False, self.color)

class Earth(pg.sprite.Sprite):
    def __init__(self, game):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = game.earth_img
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.centery = HEIGHT / 2

    def update(self):
        pass
