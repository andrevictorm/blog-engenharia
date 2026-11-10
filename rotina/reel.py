#!/usr/bin/env python3
"""Monta um Reel vertical (1080x1920, mp4 H.264) a partir dos slides JPEG de um carrossel.
Uso: python3 rotina/reel.py pasta_com_slides saida.mp4 [segundos_por_slide=3.5]
Sem som (adicione música livre de direitos depois, se quiser). Requer ffmpeg e Pillow."""
import sys, os, glob, subprocess, tempfile
from PIL import Image, ImageFilter

pasta, saida = sys.argv[1], sys.argv[2]
dur = float(sys.argv[3]) if len(sys.argv) > 3 else 3.5
slides = sorted(glob.glob(os.path.join(pasta, 'slide_*.jpg')))
assert slides, 'sem slides'
FADE, FPS = 0.5, 30
tmp = tempfile.mkdtemp()
quadros = []
for i, s in enumerate(slides):
    im = Image.open(s).convert('RGB')
    bg = im.resize((1080, 1920)).filter(ImageFilter.GaussianBlur(40))
    bg = Image.eval(bg, lambda v: int(v * 0.55))
    w = 1000; h = round(im.height * w / im.width)
    fg = im.resize((w, h), Image.LANCZOS)
    bg.paste(fg, ((1080 - w) // 2, (1920 - h) // 2))
    p = os.path.join(tmp, f'q{i}.png'); bg.save(p); quadros.append(p)

# 1) um clipe por slide (zoom suave), 2) junta com transição em fade
dframes = int((dur + FADE) * FPS)
clipes = []
for i, q in enumerate(quadros):
    c = os.path.join(tmp, f'c{i}.mp4')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', q, '-vf',
        f"scale=1188:2112,zoompan=z='min(zoom+0.0006,1.06)':d={dframes}:s=1080x1920:fps={FPS},setsar=1",
        '-frames:v', str(dframes), '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-pix_fmt', 'yuv420p', c], check=True)
    clipes.append(c)
cmd = ['ffmpeg', '-y', '-loglevel', 'error']
for c in clipes:
    cmd += ['-i', c]
filt = []; ult = '0:v'; off = dur
for i in range(1, len(clipes)):
    nome = f'x{i}'
    filt.append(f'[{ult}][{i}:v]xfade=transition=fade:duration={FADE}:offset={off:.2f}[{nome}]')
    ult = nome; off += dur
if filt:
    cmd += ['-filter_complex', ';'.join(filt), '-map', f'[{ult}]']
cmd += ['-c:v', 'libx264', '-preset', 'veryfast', '-crf', '24', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', saida]
subprocess.run(cmd, check=True)
print('ok', saida, os.path.getsize(saida)//1024, 'KB')
