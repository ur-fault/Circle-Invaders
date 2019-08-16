import pygame as pg
from os import path
screen = pg.display.set_mode((512, 512))
img = pg.image.load(path.join(path.join(path.dirname(__file__), 'img'), 'earth001.png'))
screen.blit(img, (256, 256))
pg.display.flip()

running = True
while running:
    for e in pg.event.get():
        if e.type == pg.QUIT:
            running = False
