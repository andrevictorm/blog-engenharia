#!/usr/bin/env python3
"""Capas ilustradas 1200x750 dos posts do blog (mesmo estilo de blog/swot.jpg).
Uso: python capas_blog.py  (gera em blog/)"""
import math
from PIL import Image, ImageDraw, ImageFont
W, H, S = 1200, 750, 2
NAVY, TEAL = (10, 33, 71), (14, 78, 92)
WHITE, GOLD = (245, 247, 250), (232, 176, 74)
GREEN, BLUE, RED = (34, 197, 94), (91, 168, 232), (230, 90, 90)
F = "/usr/share/fonts/truetype/crosextra/"
def font(n, s): return ImageFont.truetype(F + n, s)

def base():
    img = Image.new("RGB", (W * S, H * S)); px = img.load()
    for y in range(H * S):
        c = tuple(int(NAVY[i] + (TEAL[i] - NAVY[i]) * y / (H * S)) for i in range(3))
        for x in range(W * S): px[x, y] = c
    d = ImageDraw.Draw(img)
    g = tuple(min(255, v + 14) for v in (22, 52, 92))
    for x in range(0, W * S, 60 * S): d.line([x, 0, x, H * S], fill=g, width=S)
    for y in range(0, H * S, 60 * S): d.line([0, y, W * S, y], fill=g, width=S)
    return img, d

def P(*a): return [v * S for v in a]
def rr(d, b, r, **k): d.rounded_rectangle(P(*b), r * S, **k)
def el(d, b, **k): d.ellipse(P(*b), **k)
def ln(d, pts, w, fill): d.line(P(*pts), fill=fill, width=w * S, joint="curve")
def poly(d, pts, **k): d.polygon([(x * S, y * S) for x, y in pts], **k)

# ícones: desenhados na área ~ (400..800, 90..470)
def i_aep(d):
    rr(d, (420, 150, 640, 300), 14, fill=WHITE); rr(d, (436, 166, 624, 284), 8, fill=BLUE)
    ln(d, (530, 300, 530, 350), 10, WHITE); ln(d, (480, 350, 580, 350), 10, WHITE)
    ln(d, (400, 400, 800, 400), 8, GOLD)
    el(d, (690, 180, 750, 240), fill=WHITE)
    ln(d, (720, 245, 720, 330), 22, WHITE); ln(d, (720, 330, 660, 335), 18, WHITE); ln(d, (660, 335, 660, 400), 16, WHITE)
    ln(d, (720, 330, 760, 400), 16, WHITE); ln(d, (690, 275, 650, 290), 14, WHITE)
    ln(d, (760, 300, 760, 400), 8, GOLD); ln(d, (730, 300, 790, 300), 8, GOLD)
def i_insperi(d):
    poly(d, [(480, 130), (600, 350), (360, 350)], fill=GOLD)
    d.text((480 * S, 285 * S), "!", font=font("Caladea-Bold.ttf", 150 * S), fill=NAVY, anchor="mm")
    # frasco
    poly(d, [(715, 130), (775, 130), (775, 220), (830, 350), (660, 350), (715, 220)], fill=WHITE)
    poly(d, [(690, 290), (800, 290), (830, 350), (660, 350)], fill=GREEN)
    ln(d, (705, 128, 785, 128), 12, BLUE)
    d.text((600 * S, 400 * S), "+", font=font("Caladea-Bold.ttf", 1 * S), fill=GOLD)
def i_acess(d):
    rr(d, (480, 90, 720, 330), 40, fill=BLUE)
    el(d, (580, 120, 620, 160), fill=WHITE)
    ln(d, (600, 165, 600, 235), 16, WHITE); ln(d, (600, 235, 650, 235), 14, WHITE); ln(d, (650, 235, 672, 290), 14, WHITE)
    ln(d, (600, 190, 640, 190), 12, WHITE)
    d.arc(P(530, 205, 640, 315), 40, 330, fill=WHITE, width=14 * S)
def i_gear(d, cx=600, cy=240, R=130, r=95, hole=40, teeth=10, col=WHITE):
    pts = []
    for t in range(teeth):
        a0 = 2 * math.pi * t / teeth; a = 2 * math.pi / teeth
        for (da, rad) in [(0, r), (a * .18, R), (a * .5, R), (a * .68, r)]:
            pts.append((cx + rad * math.cos(a0 + da), cy + rad * math.sin(a0 + da)))
    poly(d, pts, fill=col); el(d, (cx - hole, cy - hole, cx + hole, cy + hole), fill=(14, 60, 80))
def i_nr12(d):
    i_gear(d, 560, 250, 135, 100, 42); i_gear(d, 745, 345, 80, 58, 26, 8, GOLD)
def i_nr18(d):
    for x in (470, 730): ln(d, (x, 110, x, 440), 12, WHITE)
    for y in (180, 280, 380): ln(d, (440, y, 760, y), 12, GOLD)
    ln(d, (470, 190, 730, 280), 8, WHITE); ln(d, (470, 280, 730, 190), 8, WHITE)
    ln(d, (470, 290, 730, 380), 8, WHITE); ln(d, (470, 380, 730, 290), 8, WHITE)
def i_bolt(d):
    el(d, (470, 100, 730, 360), fill=(18, 52, 96), outline=GOLD, width=10 * S)
    poly(d, [(620, 120), (530, 250), (592, 250), (570, 345), (672, 205), (606, 205)], fill=GOLD)
def i_nr3(d):
    pts = [(600 + 140 * math.cos(math.pi / 8 + k * math.pi / 4), 235 + 140 * math.sin(math.pi / 8 + k * math.pi / 4)) for k in range(8)]
    poly(d, pts, fill=RED); rr(d, (500, 210, 700, 260), 8, fill=WHITE)
def i_doc(d, x=480, y=100, w=240, h=300):
    poly(d, [(x, y), (x + w - 60, y), (x + w, y + 60), (x + w, y + h), (x, y + h)], fill=WHITE)
    poly(d, [(x + w - 60, y), (x + w - 60, y + 60), (x + w, y + 60)], fill=(205, 215, 228))
def i_laudo5(d):
    i_doc(d, 440, 100, 230, 300)
    for k in range(4): ln(d, (470, 190 + k * 42, 640, 190 + k * 42), 10, (178, 192, 212))
    el(d, (620, 270, 740, 390), outline=GOLD, width=16 * S); ln(d, (722, 372, 780, 430), 20, GOLD)
    ln(d, (650, 330, 675, 355), 12, GOLD); ln(d, (675, 355, 712, 305), 12, GOLD)
def i_rampa(d):
    poly(d, [(420, 400), (780, 400), (780, 160)], fill=WHITE)
    ln(d, (440, 395, 760, 215), 12, BLUE)
    d.text((640 * S, 372 * S), "8,33%", font=font("Carlito-Bold.ttf", 44 * S), fill=NAVY, anchor="mm")
def i_nr35(d):
    for x in (500, 640): ln(d, (x, 100, x, 440), 14, WHITE)
    for y in range(140, 440, 55): ln(d, (500, y, 640, y), 10, WHITE)
    ln(d, (690, 140, 760, 240), 8, GOLD); el(d, (740, 235, 790, 285), outline=GOLD, width=10 * S)
    ln(d, (690, 140, 640, 140), 8, GOLD)
def i_pgr(d):
    rr(d, (470, 110, 730, 400), 22, fill=WHITE); rr(d, (545, 90, 655, 140), 12, fill=GOLD)
    for k, yy in enumerate((200, 275, 350)):
        rr(d, (500, yy - 18, 540, yy + 22), 6, outline=GREEN, width=6 * S)
        ln(d, (506, yy + 2, 518, yy + 14), 8, GREEN); ln(d, (518, yy + 14, 538, yy - 12), 8, GREEN)
        ln(d, (565, yy, 700, yy), 10, (178, 192, 212))
def i_insobrig(d):
    i_doc(d, 440, 100, 230, 300)
    d.text((555 * S, 220 * S), "NR-15", font=font("Carlito-Bold.ttf", 52 * S), fill=NAVY, anchor="mm")
    for k in range(3): ln(d, (470, 275 + k * 38, 640, 275 + k * 38), 10, (178, 192, 212))
    poly(d, [(745, 250), (795, 250), (795, 310), (840, 400), (700, 400), (745, 310)], fill=WHITE)
    poly(d, [(725, 360), (815, 360), (840, 400), (700, 400)], fill=GREEN)
def i_assina(d):
    i_doc(d, 440, 100, 250, 300)
    for k in range(3): ln(d, (470, 170 + k * 40, 660, 170 + k * 40), 10, (178, 192, 212))
    d.line([(x * S, y * S) for x, y in [(470, 330), (500, 295), (520, 340), (545, 290), (575, 335), (620, 310)]], fill=BLUE, width=7 * S, joint="curve")
    poly(d, [(700, 190), (730, 175), (800, 330), (770, 345)], fill=GOLD); poly(d, [(770, 345), (800, 330), (770, 395)], fill=WHITE)

CAPAS = {
 "aep": (i_aep, "AEP e a NR-17", "ERGONOMIA · MITO X VERDADE"),
 "insal-peri": (i_insperi, "Insalubridade + periculosidade", "DÁ PARA RECEBER OS DOIS?"),
 "acess-erros": (i_acess, "4 erros em acessibilidade", "VISTORIAS · NBR 9050"),
 "nr12": (i_nr12, "Proteção de máquinas", "NR-12 · 4 MITOS"),
 "nr18": (i_nr18, "Queda de andaime", "NR-18 · ERROS COMUNS E CHECKLIST"),
 "nr10": (i_bolt, "Nova NR-10", "REVISÃO DO PRONTUÁRIO ELÉTRICO"),
 "nr3": (i_nr3, "Embargo x interdição", "NR-3 · O QUE A FISCALIZAÇÃO OLHA"),
 "laudo5": (i_laudo5, "5 perguntas antes do laudo", "COMO CONTRATAR SEM SURPRESAS"),
 "rampa": (i_rampa, "Sua rampa passaria?", "QUIZ · NBR 9050"),
 "nr35": (i_nr35, "Trabalho em altura", "NR-35 · O CURSO PODE SER ONLINE?"),
 "pgr": (i_pgr, "Teste rápido do PGR", "NR-1 · SUA EMPRESA PASSARIA?"),
 "insal-obrig": (i_insobrig, "Laudo de insalubridade", "É OBRIGATÓRIO? O QUE DIZ A CLT"),
 "quem-assina": (i_assina, "Quem pode assinar o PGR?", "O QUE DIZ O MINISTÉRIO DO TRABALHO"),
}
for k, (fn, t, sub) in CAPAS.items():
    img, d = base(); fn(d)
    d.text((W // 2 * S, 600 * S), t, font=font("Caladea-Bold.ttf", 64 * S), fill=WHITE, anchor="mm")
    d.text((W // 2 * S, 675 * S), sub, font=font("Carlito-Bold.ttf", 30 * S), fill=GOLD, anchor="mm")
    img.resize((W, H), Image.LANCZOS).save(f"blog/capa-{k}.jpg", "JPEG", quality=92)
print(len(CAPAS))
