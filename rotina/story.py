#!/usr/bin/env python3
"""Gera stories 1080x1920 (JPEG) que levam o público do Instagram ao blog.
Uso: python story.py stories.json pasta_saida
"icone" (opcional em cada post): chave de capas_blog.py ICONS, desenhada ao lado do titulo.
stories.json: [{"data":"2026-11-11","posts":[{"titulo":"...","tag":"NR-1 · PGR"}, ...]}, ...]"""
import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from capas_blog import render_icon
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
    for p in posts:
        ic = render_icon(p["icone"]) if p.get("icone") else None
        ft = font("Caladea-Bold.ttf", 66 if ic else 76); lh = 80 if ic else 92
        tw = W - 160 - (290 if ic else 0)
        y0 = y
        d.text((80, y), p["tag"].upper(), font=font("Carlito-Bold.ttf", 36), fill=GOLD); y += 54
        for l in wrap(d, p["titulo"], ft, tw):
            d.text((80, y), l, font=ft, fill=WHITE); y += lh
        if ic:
            k = min(250 / ic.width, 250 / ic.height)
            ic = ic.resize((int(ic.width * k), int(ic.height * k)), Image.LANCZOS)
            cy = (y0 + y) // 2
            img.paste(ic, (W - 80 - ic.width, cy - ic.height // 2), ic)
            y = max(y, y0 + ic.height + 40) if ic.height + 40 > y - y0 else y
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
