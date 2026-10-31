# -*- coding: utf-8 -*-
"""Быстрая сборка сайта: картинки отдельными webp-файлами + облегчённый набор для телефона."""
import re, os, base64
from PIL import Image

BASE = '/Users/mustari/Desktop/Boost 11/Непал'
OUT = os.path.join(BASE, 'site-punhil')
IMG = os.path.join(OUT, 'img')
os.makedirs(IMG, exist_ok=True)

src = open(os.path.join(BASE, 'nepal-lending-punhil.html'), encoding='utf-8').read()

saved = {}
def repl(mo):
    name, data = mo.group(1), mo.group(2)
    if name not in saved:
        tmp = os.path.join(IMG, name + '.tmp.jpg')
        open(tmp, 'wb').write(base64.b64decode(data))
        im = Image.open(tmp).convert('RGB')
        os.remove(tmp)
        if max(im.size) > 1000:
            k = 1000 / max(im.size)
            im = im.resize((round(im.size[0]*k), round(im.size[1]*k)), Image.LANCZOS)
        q = 82 if name.startswith('hero') else 72
        im.save(os.path.join(IMG, name + '.webp'), 'WEBP', quality=q, method=6)
        sm = im.copy()
        if max(sm.size) > 620:
            k = 620 / max(sm.size)
            sm = sm.resize((round(sm.size[0]*k), round(sm.size[1]*k)), Image.LANCZOS)
        sm.save(os.path.join(IMG, name + '-sm.webp'), 'WEBP', quality=70, method=6)
        saved[name] = os.path.getsize(os.path.join(IMG, name + '.webp'))
    return '.im-%s { background-image: url("img/%s.webp"); }' % (name, name)

out = re.sub(r'\.im-([a-z0-9-]+)\s*\{\s*background-image:\s*url\("data:image/jpeg;base64,([^"]+)"\);\s*\}', repl, src)

mobile_css = '\n  @media (max-width: 760px) {\n' + '\n'.join(
    '    .im-%s { background-image: url("img/%s-sm.webp"); }' % (n, n) for n in sorted(saved)) + '\n  }\n'
out = out.replace('</style>', mobile_css + '</style>', 1)

out = out.replace('<title>', '<link rel="preload" as="image" href="img/hero-drug-sm.webp" media="(max-width: 760px)">\n'
                             '<link rel="preload" as="image" href="img/hero-drug.webp" media="(min-width: 761px)">\n<title>', 1)

meta = '''<meta name="description" content="Непал для своих — 11 дней, 20–30 марта 2027: тибетский квартал Катманду, Патан, озеро Фева и четырёхдневный трек Гхорепани — Пунхилл — Гандрук. Группа до 6 человек.">
<meta property="og:type" content="website">
<meta property="og:title" content="Непал для своих — 11 дней, март 2027">
<meta property="og:description" content="Затеряемся в переулках старого города, встретим рассвет в Гималаях и, возможно, узнаем себя чуть лучше. 20–30 марта 2027, максимум 6 человек.">
<meta property="og:image" content="preview.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>🏔️</text></svg>">
'''
out = out.replace('<title>', meta + '<title>', 1)

open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8').write(out)
desk = sum(saved.values())
mob = sum(os.path.getsize(os.path.join(IMG, n + '-sm.webp')) for n in saved)
print('index.html:', round(os.path.getsize(os.path.join(OUT,'index.html'))/1024, 1), 'КБ')
print('картинки для компьютера:', round(desk/1024/1024, 2), 'МБ | для телефона:', round(mob/1024, 0), 'КБ')
