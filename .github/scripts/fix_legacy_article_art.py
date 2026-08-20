from pathlib import Path
import html
import hashlib
import re
import textwrap

ROOT = Path('.')


def strip_tags(value):
    return re.sub(r'<[^>]+>', '', value).replace('&amp;', '&').replace('&quot;', '"').replace('&#39;', "'").strip()


def lane(path):
    p = path.as_posix()
    if p.startswith('old-man-otaku/'):
        return '#05070b', '#ff6a00', '#1687ff', 'ANIMANGA UPDATES'
    if p.startswith('news/movies/'):
        return '#05070b', '#ff6a00', '#9c62ff', 'ROGUEVERSE MOVIES'
    if p.startswith('news/games/'):
        return '#04070c', '#ff6a00', '#13a9ff', 'ROGUEVERSE GAMING'
    if p.startswith('news/tech/') or p.startswith('future/'):
        return '#04050c', '#a56cff', '#53b8ff', 'ROGUEVERSE FUTURE'
    if p.startswith('our-culture/'):
        return '#05070b', '#ff6a00', '#16b6c8', 'OUR CULTURE'
    return '#05070b', '#ff6a00', '#1687ff', 'ROGUEVERSE EDITORIAL'


def make_svg(path, title, kicker, mobile=False):
    bg, accent, secondary, label = lane(path)
    width, height = (900, 1200) if mobile else (1600, 900)
    seed = int(hashlib.sha1((path.as_posix() + title).encode()).hexdigest()[:8], 16)
    text_width = 21 if mobile else 31
    lines = textwrap.wrap(title, width=text_width)[:5 if mobile else 4]
    font_size = 61 if mobile else 67
    tx, ty = (55, 205) if mobile else (85, 245)
    tspans = ''.join(
        f'<tspan x="{tx}" dy="{0 if i == 0 else int(font_size * 1.08)}">{html.escape(line)}</tspan>'
        for i, line in enumerate(lines)
    )
    dots = []
    for i in range(18):
        x = 25 + ((seed >> (i % 16)) * (37 + i * 11)) % (width - 50)
        y = 25 + ((seed >> ((i + 5) % 16)) * (31 + i * 7)) % (height - 50)
        r = 8 + ((seed >> ((i + 9) % 16)) % 34)
        dots.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{accent if i % 2 == 0 else secondary}" opacity="{0.025 + (i % 5) * 0.012:.3f}"/>')

    title_lower = title.lower()
    if any(k in title_lower for k in ('movie', 'avatar', 'marvel', 'spider', 'x-men', 'transformers', 'film')):
        symbol = f'<g transform="translate({width * .77:.0f} {height * .28:.0f})" opacity=".7"><rect x="-145" y="-85" width="290" height="185" rx="14" fill="none" stroke="{secondary}" stroke-width="13"/><path d="M-145-25h290M-86-85l38 60M-12-85l38 60M62-85l38 60" stroke="{accent}" stroke-width="12"/></g>'
    elif any(k in title_lower for k in ('game', 'xbox', 'playstation', 'nintendo')):
        symbol = f'<g transform="translate({width * .77:.0f} {height * .28:.0f})" fill="none" stroke="{secondary}" stroke-width="15" opacity=".72"><path d="M-125 25c0-75 42-120 105-120h40c63 0 105 45 105 120 0 88-31 130-72 130-25 0-44-27-64-50h-178c-20 23-39 50-64 50-41 0-72-42-72-130z"/><path d="M-82 3h64M-50-29v64"/><circle cx="78" cy="-7" r="12" fill="{accent}" stroke="none"/><circle cx="113" cy="24" r="12" fill="{accent}" stroke="none"/></g>'
    else:
        symbol = f'<g transform="translate({width * .77:.0f} {height * .28:.0f})" opacity=".65"><circle r="125" fill="none" stroke="{secondary}" stroke-width="13"/><circle r="84" fill="none" stroke="{accent}" stroke-width="8"/><path d="M0-150l17 105 53 22-53 22L0 150-17-105l-53-22 53-22z" fill="#eef2f8"/></g>'

    # Western entertainment lane uses an original generic editorial guide rather than franchise likenesses.
    guide_x = width * (.52 if mobile else .79)
    guide_y = height * (.77 if mobile else .72)
    guide = f'''<g transform="translate({guide_x:.0f} {guide_y:.0f})"><circle cy="-210" r="70" fill="#956347"/><path d="M-66-246q66-62 132 0" stroke="#171719" stroke-width="34" fill="none"/><path d="M-140 230c15-154 46-260 105-319h70c59 59 90 165 105 319z" fill="#0c1016" stroke="#2a313d" stroke-width="8"/><path d="M-102-42h204l-28 224H-74z" fill="#11161d" stroke="{accent}" stroke-width="8"/><path d="M-36-32h72v165h-72z" fill="#ece7df"/><path d="M-99 8l198 155M99 8l-198 155" stroke="{accent}" stroke-width="6" opacity=".7"/><ellipse cx="-76" cy="245" rx="72" ry="23" fill="#eee"/><ellipse cx="76" cy="245" rx="72" ry="23" fill="#eee"/></g>'''

    kicker_text = html.escape((strip_tags(kicker) or 'ROGUEVERSE EDITORIAL')[:80])
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" role="img" aria-labelledby="t d"><title id="t">{html.escape(title)}</title><desc id="d">Original RogueVerse editorial illustration for {html.escape(title)}.</desc><defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop stop-color="{bg}"/><stop offset=".52" stop-color="#0b1020"/><stop offset="1" stop-color="{bg}"/></linearGradient><radialGradient id="a"><stop stop-color="{accent}"/><stop offset="1" stop-color="{accent}" stop-opacity="0"/></radialGradient><radialGradient id="b"><stop stop-color="{secondary}"/><stop offset="1" stop-color="{secondary}" stop-opacity="0"/></radialGradient></defs><rect width="{width}" height="{height}" fill="url(#bg)"/><circle cx="{width * .75:.0f}" cy="{height * .45:.0f}" r="{min(width, height) * .44:.0f}" fill="url(#a)" opacity=".25"/><circle cx="{width * .56:.0f}" cy="{height * .68:.0f}" r="{min(width, height) * .38:.0f}" fill="url(#b)" opacity=".16"/>{''.join(dots)}<g opacity=".09" stroke="#fff" stroke-width="2"><path d="M0 {height * .2:.0f}h{width}M0 {height * .4:.0f}h{width}M0 {height * .6:.0f}h{width}M0 {height * .8:.0f}h{width}"/></g>{symbol}{guide}<text x="{tx}" y="{70 if mobile else 75}" fill="{accent}" font-family="Arial,sans-serif" font-size="{21 if mobile else 24}" font-weight="800" letter-spacing="7">{label}</text><text x="{tx}" y="{116 if mobile else 121}" fill="#acb7c8" font-family="Arial,sans-serif" font-size="{15 if mobile else 17}" font-weight="700" letter-spacing="2">{kicker_text}</text><text x="{tx}" y="{ty}" fill="#fff" font-family="Arial,sans-serif" font-size="{font_size}" font-weight="900">{tspans}</text><rect x="{tx}" y="{height - 74}" width="300" height="8" fill="{accent}"/><rect x="{tx + 320}" y="{height - 74}" width="130" height="8" fill="{secondary}"/></svg>'''


changed = []
generated = []
for path in ROOT.rglob('*.html'):
    if '.git' in path.parts:
        continue
    text = path.read_text(encoding='utf-8')
    if 'article-shell' not in text or 'article-lead-art' in text:
        continue

    h1 = re.search(r'<h1[^>]*>(.*?)</h1>', text, flags=re.I | re.S)
    if not h1:
        continue
    title = strip_tags(h1.group(1))
    kicker_match = re.search(r'<p\s+class=(["\'])kicker\1[^>]*>(.*?)</p>', text, flags=re.I | re.S)
    kicker = strip_tags(kicker_match.group(2)) if kicker_match else ''

    desktop = path.parent / 'rv-article-visual.svg'
    mobile = path.parent / 'rv-article-visual-mobile.svg'
    desktop.write_text(make_svg(path, title, kicker, False), encoding='utf-8')
    mobile.write_text(make_svg(path, title, kicker, True), encoding='utf-8')
    generated.extend((desktop.as_posix(), mobile.as_posix()))

    prefix = '../' * len(path.parent.parts)
    if 'site-2026.css' not in text:
        link = f'<link rel="stylesheet" href="{prefix}site-2026.css?v=20260820-visual-v4">'
        if '</head>' in text:
            text = text.replace('</head>', link + '</head>', 1)
        elif '<main' in text:
            text = text.replace('<main', link + '<main', 1)
        else:
            text = link + text

    figure = f'<figure class="article-lead-art rv-auto-article-art"><picture><source media="(max-width:680px)" srcset="rv-article-visual-mobile.svg"><img src="rv-article-visual.svg" alt="Original RogueVerse editorial illustration for {html.escape(title, quote=True)}" loading="eager" decoding="async"></picture></figure>'
    dek = re.search(r'(<p\s+class=(["\'])dek\2[^>]*>.*?</p>)', text, flags=re.I | re.S)
    anchor = dek or h1
    text = text[:anchor.end()] + figure + text[anchor.end():]
    path.write_text(text, encoding='utf-8')
    changed.append(path.as_posix())

print(f'Upgraded {len(changed)} legacy article pages')
for item in changed:
    print('LEGACY', item)
for item in generated:
    print('LEGACY_ART', item)
