#!/usr/bin/env python3
"""Gera stories 1080x1920 (JPEG) que levam o público do Instagram ao blog.
Uso: python story.py stories.json pasta_saida
stories.json: [{"data":"2026-11-11","posts":[{"titulo":"...","tag":"NR-1 · PGR"}, ...]}, ...]"""
import json, sys, os
from PIL import Image, ImageDraw, ImageFont
W, H = 1080, 1920
NAVY, TEAL, GOLD, WHITE = (10, 33, 71), (14, 78, 92), (224, 165, 38), (245, 247, 250)
F = "/usr/share/fonts/truetype/crosextra/"
def font(n, s): return ImageFont.truetype(F + n, s)
def wrap(d, text, f, maxw):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= maxw: cur = t
        else: lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines
def story(posts, path):
    img = Image.new("RGB", (W, H)); px = img.load()
    for y in range(H):
        c = tuple(int(NAVY[i] + (TEAL[i] - NAVY[i]) * y / H) for i in range(3))
        for x in range(W): px[x, y] = c
    d = ImageDraw.Draw(img)
    y = 260  # zona segura: topo livre
    d.rectangle([80, y, 200, y + 8], fill=GOLD); y += 40
    d.text((80, y), "NOVO NO BLOG", font=font("Carlito-Bold.ttf", 56), fill=GOLD); y += 110
    ft = font("Caladea-Bold.ttf", 76)
    for p in posts:
        d.text((80, y), p["tag"].upper(), font=font("Carlito-Bold.ttf", 36), fill=GOLD); y += 54
        for l in wrap(d, p["titulo"], ft, W - 160):
            d.text((80, y), l, font=ft, fill=WHITE); y += 92
        y += 60
    fb = font("Carlito-Bold.ttf", 52)
    by = H - 560
    d.rounded_rectangle([80, by, W - 80, by + 190], 36, fill=GOLD)
    d.text((W // 2, by + 62), "Leia no blog", font=font("Caladea-Bold.ttf", 60), fill=NAVY, anchor="mm")
    d.text((W // 2, by + 130), "link na bio do perfil", font=fb, fill=NAVY, anchor="mm")
    d.text((W // 2, by + 250), "engperitoandrevictor.blogspot.com", font=font("Carlito-Bold.ttf", 40), fill=WHITE, anchor="mm")
    d.text((W // 2, H - 250), "AV  |  Eng. André Victor · CREA-RJ 2014128139", font=font("Carlito-Bold.ttf", 32), fill=GOLD, anchor="mm")
    img.save(path, "JPEG", quality=95)
if __name__ == "__main__":
    data = json.load(open(sys.argv[1], encoding="utf-8")); out = sys.argv[2]
    for s in data:
        d = f"{out}/{s['data']}"; os.makedirs(d, exist_ok=True)
        story(s["posts"], f"{d}/story.jpg")
    print(len(data), "stories")
