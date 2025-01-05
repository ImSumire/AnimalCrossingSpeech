from os import listdir

import pygame as pg
from noise import snoise2

from speech import Speech


W, H = 520, 520
FONT_SIZE = 18
PAD = 24

CAT_SIZE = 64

FG = 242, 231, 243
BG = 9, 5, 10

VOLUME = 0.2


def load_letter(path: str):
    sound = pg.mixer.Sound("assets/pitched/" + path)
    sound.set_volume(VOLUME)
    return sound


pg.init()
pg.mixer.init()

screen = pg.display.set_mode((W, H))
clock = pg.time.Clock()
font = pg.font.Font("assets/yoster.ttf", FONT_SIZE)  # SysFont("Arial", FONT)

# fmt: off
sounds = {
    path[0]: load_letter(path)
    for path in listdir("assets/pitched")
}
# fmt: on

cat = pg.transform.scale(
    pg.image.load("assets/cat.png").convert_alpha(),
    (CAT_SIZE, CAT_SIZE)
)
cat_name_surf = font.render("Katie", True, FG)

pg.display.set_caption("Animal Crossing Speaking")


tts = "Bonjour ! Comment allez-vous aujourd'hui ? Le soleil brille et les \
fleurs sont en pleine floraison dans notre charmant village. J'ai passé la \
matinée à pêcher au bord de la rivière et j'ai attrapé un beau poisson. Et \
vous, qu'avez-vous fait aujourd'hui ?\n\
\n\
Je me demandais si vous aviez vu Tom Nook récemment. J'ai besoin de quelques \
meubles pour ma maison et je me demandais s'il avait de nouvelles arrivées. Et \
comment va votre jardin ? J'ai vu que vous aviez planté de nouvelles fleurs \
l'autre jour. Elles sont déjà en fleur ?\n\
\n\
Je suis impatiente de voir ce que vous avez fait aujourd'hui !\n"

speech = Speech(tts, sounds)

while True:
    # Update
    dt = clock.tick(60)
    tick = pg.time.get_ticks()

    speech.update(dt, tick)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()

    # Render
    screen.fill(BG)

    # Cat profile
    screen.blit(cat_name_surf, (PAD + 6, PAD + CAT_SIZE))
    screen.blit(cat, (PAD, PAD))

    # Speech lines
    speech.render(
        screen,
        PAD + PAD + CAT_SIZE,
        PAD,
        FG,
        line_height=FONT_SIZE,
        font=font,
        width=35
    )

    # Speed random (simplex noise) helper
    FACTOR = 20
    pg.draw.circle(
        screen,
        FG,
        (W - PAD, (FACTOR - (snoise2(tick * 0.0005, 0)) * FACTOR) + (H - FACTOR * 2 - PAD)),
        2.5,
    )

    pg.display.flip()
