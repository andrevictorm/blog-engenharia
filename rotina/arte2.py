#!/usr/bin/env python3
"""Carrossel v2 (1080x1350) @engperitoandre: mais visual, com mascote "Capacete", selos e icones.
Uso: python arte2.py conteudo.json pasta_saida
slide: {"kicker","titulo","texto","icone","fala","selo":["MITO","red"|"green"|"gold"|"blue"],"cta":bool,"num":"1"}"""
import json, sys, os
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import capas_blog as cb
from capas_blog import render_icon, P, rr, el, ln, poly, S as SS, WHITE as CW, GOLD as CG, BLUE as CB, GREEN as CGR
W, H = 1080, 1350
NAVY, TEAL, GOLD, WHITE = (10, 33, 71), (14, 78, 92), (224, 165, 38), (245, 247, 250)
F = "/usr/share/fonts/truetype/crosextra/"
def font(n, s): return ImageFont.truetype(F + n, s)
SELOS = {"red": (214, 69, 69), "green": (34, 170, 90), "gold": (224, 165, 38), "blue": (60, 130, 210)}

# ---- icones extras (perfil / chat / predio) ----
def i_perfil(d):
    rr(d, (430, 120, 770, 400), 26, fill=WHITE); rr(d, (560, 100, 640, 140), 10, fill=CG)
    el(d, (470, 190, 570, 290), fill=CB)
    d.pieslice(P(470, 170, 570, 260), 180, 360, fill=CG); rr(d, (462, 214, 578, 228), 6, fill=(200, 140, 20))
    for k, w in enumerate((130, 110, 90)): ln(d, (600, 205 + k * 38, 600 + w, 205 + k * 38), 12, (178, 192, 212))
    ln(d, (470, 340, 730, 340), 10, CG)
def i_chat(d):
    rr(d, (420, 120, 700, 300), 30, fill=WHITE); poly(d, [(470, 300), (470, 360), (540, 300)], fill=WHITE)
    for k in range(3): el(d, (480 + k * 70, 195, 520 + k * 70, 235), fill=CB)
    rr(d, (600, 250, 800, 380), 26, fill=CGR); poly(d, [(740, 380), (770, 430), (700, 380)], fill=CGR)
    ln(d, (640, 300, 760, 300), 10, WHITE); ln(d, (640, 335, 730, 335), 10, WHITE)
def i_predio(d):
    rr(d, (470, 110, 690, 420), 10, fill=WHITE); rr(d, (690, 220, 790, 420), 10, fill=(200, 212, 230))
    for r in range(4):
        for c in range(3): rr(d, (495 + c * 62, 140 + r * 62, 530 + c * 62, 180 + r * 62), 4, fill=CB if (r + c) % 2 else CG)
    rr(d, (560, 360, 600, 420), 4, fill=NAVY); ln(d, (440, 420, 820, 420), 10, CG)
cb.ICONS.update({"perfil": i_perfil, "chat": i_chat, "predio": i_predio})

# ---- mascote Capacete ----
def mascote(size, olhos="ok"):
    k = 4; s = 300 * k
    im = Image.new("RGBA", (s, s), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    def B(*a): return [v * k for v in a]
    d.rounded_rectangle(B(60, 235, 240, 330), 50 * k, fill=(60, 130, 210))            # ombros
    d.rectangle(B(130, 235, 170, 262), fill=(245, 247, 250))                            # gola
    d.ellipse(B(70, 80, 230, 240), fill=(250, 222, 190))                                # rosto
    d.ellipse(B(60, 140, 90, 180), fill=(250, 222, 190)); d.ellipse(B(210, 140, 240, 180), fill=(250, 222, 190))
    d.pieslice(B(58, 28, 242, 190), 180, 360, fill=GOLD)                                # capacete
    d.rounded_rectangle(B(44, 105, 256, 128), 11 * k, fill=(196, 138, 18))              # aba
    d.rounded_rectangle(B(138, 30, 162, 106), 8 * k, fill=(245, 247, 250))              # faixa
    d.ellipse(B(106, 150, 124, 172), fill=NAVY); d.ellipse(B(176, 150, 194, 172), fill=NAVY)
    d.ellipse(B(110, 153, 117, 160), fill=WHITE); d.ellipse(B(180, 153, 187, 160), fill=WHITE)
    d.arc(B(112, 168, 188, 214), 20, 160, fill=NAVY, width=7 * k)
    d.ellipse(B(92, 180, 112, 196), fill=(244, 160, 150)); d.ellipse(B(188, 180, 208, 196), fill=(244, 160, 150))
    return im.resize((size, size), Image.LANCZOS)

def wrap(d, text, f, maxw):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= maxw: cur = t
        else: lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines

def fundo():
    img = Image.new("RGB", (W, H)); px = img.load()
    for y in range(H):
        c = tuple(int(NAVY[i] + (TEAL[i] - NAVY[i]) * y / H) for i in range(3))
        for x in range(W): px[x, y] = c
    img = img.convert("RGBA"); ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    for x in range(0, W, 60): d.line([x, 0, x, H], fill=(255, 255, 255, 9), width=1)
    for y in range(0, H, 60): d.line([0, y, W, y], fill=(255, 255, 255, 9), width=1)
    d.ellipse([W - 330, -170, W + 170, 330], fill=(224, 165, 38, 22)); d.ellipse([-200, H - 520, 330, H + 10], fill=(91, 168, 232, 18))
    return Image.alpha_composite(img, ov)

def slide(s, n, total, path):
    img = fundo(); d = ImageDraw.Draw(img)
    gap = 8; seg = (W - 160 - gap * (total - 1)) / total
    for i in range(total):
        x0 = 80 + i * (seg + gap)
        d.rounded_rectangle([x0, 62, x0 + seg, 70], 4, fill=GOLD if i < n else (86, 118, 160))
    fk = font("Carlito-Bold.ttf", 34); kt = s.get("kicker", "").upper()
    kw = d.textlength(kt, font=fk) + 44
    d.rounded_rectangle([80, 110, 80 + kw, 166], 28, fill=GOLD); d.text((102, 138), kt, font=fk, fill=NAVY, anchor="lm")
    if s.get("selo"):
        txt, cor = s["selo"]; fs = font("Carlito-Bold.ttf", 46); tw = d.textlength(txt, font=fs) + 60
        lay = Image.new("RGBA", (int(tw) + 20, 100), (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
        ld.rounded_rectangle([8, 12, 8 + tw, 78], 18, fill=SELOS[cor], outline=(255, 255, 255), width=4)
        ld.text((8 + tw / 2, 46), txt, font=fs, fill=(255, 255, 255), anchor="mm")
        lay = lay.rotate(6, expand=True, resample=Image.BICUBIC)
        img.alpha_composite(lay, (W - 70 - lay.width, 92))
    y = 230; ft = font("Caladea-Bold.ttf", 80)
    for l in wrap(d, s["titulo"], ft, W - 160):
        d.text((80, y), l, font=ft, fill=WHITE); y += 94
    y += 26
    fb = font("Carlito-Regular.ttf", 44) if os.path.exists(F + "Carlito-Regular.ttf") else font("Carlito-Bold.ttf", 44)
    lines = wrap(d, s.get("texto", ""), fb, W - 160 - 60)
    if lines:
        h = len(lines) * 62 + 40
        ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
        od.rounded_rectangle([80, y, W - 80, y + h], 28, fill=(255, 255, 255, 22)); od.rounded_rectangle([80, y + 18, 90, y + h - 18], 5, fill=GOLD)
        img = Image.alpha_composite(img, ov); d = ImageDraw.Draw(img)
        yy = y + 20
        for l in lines: d.text((120, yy), l, font=fb, fill=(232, 238, 246)); yy += 62
        y += h
    zbot = (H - 360) if s.get("cta") else (H - 150); ztop = y + 30; zh = zbot - ztop
    if zh >= 190:
        masc = zh >= 330
        dia = int(min(zh, 460 if masc else 520, W - 160))
        cx = 80 + dia // 2 if masc else W // 2
        if s.get("icone") and not s.get("cta"):
            ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
            cy = ztop + zh // 2
            od.ellipse([cx - dia // 2, cy - dia // 2, cx + dia // 2, cy + dia // 2], fill=(255, 255, 255, 20), outline=(224, 165, 38, 140), width=4)
            img = Image.alpha_composite(img, ov)
            ic = render_icon(s["icone"]); k = min(dia * 0.74 / ic.width, dia * 0.74 / ic.height)
            ic = ic.resize((int(ic.width * k), int(ic.height * k)), Image.LANCZOS)
            img.alpha_composite(ic, (cx - ic.width // 2, cy - ic.height // 2))
        if masc or (s.get("cta") and zh >= 200):
            m = int(min(300, zh * 0.72)); mx = W - 80 - m; my = zbot - m
            img.alpha_composite(mascote(m), (mx, my)); d = ImageDraw.Draw(img)
            fala = s.get("fala")
            if fala:
                fl = font("Carlito-Bold.ttf", 36); ls = wrap(d, fala, fl, 330); bh = len(ls) * 44 + 36
                bw = max(d.textlength(t, font=fl) for t in ls) + 48
                bx1 = W - 70; bx0 = bx1 - bw; by1 = my + 14; by0 = by1 - bh
                if by0 < ztop - 10: by0 = ztop - 10; by1 = by0 + bh
                d.rounded_rectangle([bx0, by0, bx1, by1], 26, fill=(255, 255, 255))
                d.polygon([(bx1 - 90, by1 - 2), (bx1 - 40, by1 - 2), (mx + m * 0.62, my + m * 0.22)], fill=(255, 255, 255))
                for i, t in enumerate(ls): d.text((bx0 + 24, by0 + 18 + i * 44), t, font=fl, fill=NAVY)
    d = ImageDraw.Draw(img)
    if s.get("cta"):
        d.rounded_rectangle([80, H - 330, W - 80, H - 190], 36, fill=(34, 197, 94))
        d.text((W // 2, H - 260), "Chame no WhatsApp: 21 99419-2878", font=font("Carlito-Bold.ttf", 50), fill=(8, 40, 20), anchor="mm")
    d.line([80, H - 135, W - 80, H - 135], fill=(255, 255, 255, 60), width=2)
    d.text((80, H - 95), "AV  |  Eng. André Victor · CREA-RJ 2014128139", font=font("Carlito-Bold.ttf", 32), fill=GOLD)
    d.text((W - 80, H - 95), f"{n}/{total}" + ("  →" if n < total else ""), font=font("Carlito-Bold.ttf", 32), fill=WHITE, anchor="ra")
    img.convert("RGB").save(path, "JPEG", quality=95)

def gerar(slides, out):
    os.makedirs(out, exist_ok=True)
    for i, s in enumerate(slides, 1): slide(s, i, len(slides), f"{out}/slide_{i}.jpg")

if __name__ == "__main__":
    gerar(json.load(open(sys.argv[1], encoding="utf-8"))["slides"], sys.argv[2]); print("ok")
