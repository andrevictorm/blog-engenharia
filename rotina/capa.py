#!/usr/bin/env python3
"""Capa 1200x630 para posts do blog. Uso: python capa.py saida.jpg "TAG" "Título" """
import sys
from PIL import Image, ImageDraw, ImageFont
W, H = 1200, 630
NAVY, TEAL, GOLD, WHITE = (10, 33, 71), (14, 78, 92), (224, 165, 38), (245, 247, 250)
F = "/usr/share/fonts/truetype/crosextra/"
def font(n, s): return ImageFont.truetype(F + n, s)
def wrap(d, t, f, mw):
    L, c = [], ""
    for w in t.split():
        x = (c + " " + w).strip()
        if d.textlength(x, font=f) <= mw: c = x
        else: L.append(c); c = w
    if c: L.append(c)
    return L
out, tag, title = sys.argv[1:4]
img = Image.new("RGB", (W, H)); px = img.load()
for y in range(H):
    c = tuple(int(NAVY[i] + (TEAL[i] - NAVY[i]) * y / H) for i in range(3))
    for x in range(W): px[x, y] = c
d = ImageDraw.Draw(img)
d.rectangle([70, 90, 190, 97], fill=GOLD)
d.text((70, 120), tag.upper(), font=font("Carlito-Bold.ttf", 40), fill=GOLD)
ft = font("Caladea-Bold.ttf", 72); y = 200
for l in wrap(d, title, ft, W - 140):
    d.text((70, y), l, font=ft, fill=WHITE); y += 88
d.text((70, H - 70), "AV  |  Eng. André Victor · CREA-RJ 2014128139", font=font("Carlito-Bold.ttf", 28), fill=GOLD)
img.save(out, "JPEG", quality=92)
