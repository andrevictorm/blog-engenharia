#!/usr/bin/env python3
"""Gera slides 1080x1350 (JPEG) no estilo do perfil @engperitoandre.
Uso: python arte.py conteudo.json pasta_saida
conteudo.json: {"slides":[{"kicker":"...", "titulo":"...", "texto":"...", "cta":false}, ...]}
O ultimo slide deve ter "cta": true (mostra o WhatsApp)."""
import json, sys, os, textwrap
from PIL import Image, ImageDraw, ImageFont
W, H = 1080, 1350
NAVY, TEAL, GOLD, WHITE = (10, 33, 71), (14, 78, 92), (224, 165, 38), (245, 247, 250)
F = "/usr/share/fonts/truetype/crosextra/"
def font(name, size): return ImageFont.truetype(F + name, size)

def gradient():
    img = Image.new("RGB", (W, H)); px = img.load()
    for y in range(H):
        t = y / H
        c = tuple(int(NAVY[i] + (TEAL[i] - NAVY[i]) * t) for i in range(3))
        for x in range(W): px[x, y] = c
    return img

def wrap(d, text, f, maxw):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= maxw: cur = t
        else: lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines

def slide(s, n, total, path):
    img = gradient(); d = ImageDraw.Draw(img)
    d.rectangle([80, 120, 200, 128], fill=GOLD)
    d.text((80, 150), s.get("kicker", "").upper(), font=font("Carlito-Bold.ttf", 38), fill=GOLD)
    y = 260
    ft = font("Caladea-Bold.ttf", 86)
    for l in wrap(d, s["titulo"], ft, W - 160):
        d.text((80, y), l, font=ft, fill=WHITE); y += 104
    y += 40
    fb = font("Carlito-Regular.ttf", 46) if os.path.exists(F + "Carlito-Regular.ttf") else font("Carlito-Bold.ttf", 46)
    for l in wrap(d, s.get("texto", ""), fb, W - 160):
        d.text((80, y), l, font=fb, fill=(220, 228, 238)); y += 66
    if s.get("cta"):
        d.rounded_rectangle([80, H - 330, W - 80, H - 190], 36, fill=(34, 197, 94))
        d.text((W // 2, H - 260), "Chame no WhatsApp: 21 99419-2878", font=font("Carlito-Bold.ttf", 50), fill=(8, 40, 20), anchor="mm")
    d.text((80, H - 100), "AV  |  Eng. André Victor · CREA-RJ 2014128139", font=font("Carlito-Bold.ttf", 32), fill=GOLD)
    d.text((W - 80, H - 100), f"{n}/{total}", font=font("Carlito-Bold.ttf", 32), fill=WHITE, anchor="ra")
    img.save(path, "JPEG", quality=95)

if __name__ == "__main__":
    data = json.load(open(sys.argv[1], encoding="utf-8")); out = sys.argv[2]
    os.makedirs(out, exist_ok=True)
    sl = data["slides"]
    for i, s in enumerate(sl, 1): slide(s, i, len(sl), f"{out}/slide_{i}.jpg")
    print(f"{len(sl)} slides em {out}")
