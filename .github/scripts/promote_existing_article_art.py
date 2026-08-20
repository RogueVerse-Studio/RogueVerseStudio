from pathlib import Path
from urllib.parse import urlsplit
import os
import re

ROOT = Path('.')
TEMP_MARKERS = ('rv-article-visual.svg', 'rv-article-visual-mobile.svg', 'editorial-fallback.svg')
PREFERRED = ('feature', 'hero', 'header', 'cover', 'lead', 'key-visual', 'key_visual', '01-', '01.')
SKIP = ('logo', 'icon', 'sword-mark', 'avatar', 'qr', 'badge', 'tiktok', 'social', 'facebook', 'instagram', 'youtube', 'mobile')
RASTER = {'.webp', '.jpg', '.jpeg', '.png'}


def local_exists(page: Path, src: str) -> bool:
    if src.startswith(('http://', 'https://', '//', 'data:')):
        return False
    clean = src.split('?')[0].split('#')[0]
    if not clean:
        return False
    return Path(os.path.normpath((page.parent / clean).as_posix())).exists()


def score_src(src: str) -> int:
    lower = src.lower()
    if any(x in lower for x in SKIP):
        return -1000
    score = 0
    for i, key in enumerate(PREFERRED):
        if key in lower:
            score += 120 - i * 8
    ext = Path(urlsplit(src).path).suffix.lower()
    if ext in RASTER:
        score += 25
    if 'assets/' in lower:
        score += 10
    return score


def add_lead_class(figure: str) -> str:
    opening = re.search(r'<figure\b[^>]*>', figure, flags=re.I | re.S)
    if not opening:
        return figure
    tag = opening.group(0)
    cls = re.search(r'class=(["\'])(.*?)\1', tag, flags=re.I | re.S)
    if cls:
        names = cls.group(2).split()
        if 'article-lead-art' not in names:
            names.append('article-lead-art')
        quote = cls.group(1)
        new_tag = tag[:cls.start()] + f'class={quote}{" ".join(names)}{quote}' + tag[cls.end():]
    else:
        new_tag = tag[:-1] + ' class="article-lead-art">'
    return figure[:opening.start()] + new_tag + figure[opening.end():]


def article_title(text: str) -> str:
    match = re.search(r'<h1[^>]*>(.*?)</h1>', text, flags=re.I | re.S)
    if not match:
        return 'RogueVerse editorial artwork'
    title = re.sub(r'<[^>]+>', '', match.group(1))
    title = re.sub(r'\s+', ' ', title).strip()
    return title.replace('&amp;', '&').replace('&#39;', "'").replace('&quot;', '"')


def find_obvious_local_asset(page: Path):
    candidates = []
    for asset in page.parent.rglob('*'):
        if not asset.is_file() or asset.suffix.lower() not in RASTER:
            continue
        rel = os.path.relpath(asset, page.parent).replace('\\', '/')
        score = score_src(rel)
        if score < 100:
            continue
        try:
            size_bonus = min(asset.stat().st_size // 50000, 20)
        except OSError:
            size_bonus = 0
        candidates.append((score + size_bonus, rel))
    if not candidates:
        return None
    candidates.sort(reverse=True)
    return candidates[0][1]


changed = []
for page in ROOT.rglob('index.html'):
    if '.git' in page.parts:
        continue
    text = page.read_text(encoding='utf-8')
    if 'article-shell' not in text or not any(marker in text for marker in TEMP_MARKERS):
        continue

    lead = re.search(r'<figure\s+class=(["\'])[^"\']*article-lead-art[^"\']*\1[^>]*>.*?</figure>', text, flags=re.I | re.S)
    if not lead or not any(marker in lead.group(0) for marker in TEMP_MARKERS):
        continue

    # First preference: art already intentionally embedded in the article body.
    candidates = []
    for fig in re.finditer(r'<figure\b[^>]*>.*?</figure>', text, flags=re.I | re.S):
        if fig.start() == lead.start():
            continue
        img = re.search(r'<img[^>]+src=(["\'])(.*?)\1', fig.group(0), flags=re.I | re.S)
        if not img:
            continue
        src = img.group(2)
        if any(marker in src for marker in TEMP_MARKERS) or not local_exists(page, src):
            continue
        candidates.append((score_src(src), fig.start(), fig.end(), fig.group(0), src))

    if candidates:
        candidates.sort(key=lambda item: (item[0], -item[1]), reverse=True)
        score, start, end, figure, src = candidates[0]
        if score >= 0 and start > lead.end():
            promoted = add_lead_class(figure)
            before = text[:lead.start()]
            between = text[lead.end():start]
            after = text[end:]
            text = before + promoted + between + after
            page.write_text(text, encoding='utf-8')
            changed.append((page.as_posix(), src, 'embedded'))
            continue

    # Second preference: an obvious hero/header/cover file already stored inside the article directory.
    src = find_obvious_local_asset(page)
    if not src:
        continue
    title = article_title(text)
    replacement = f'<figure class="article-lead-art"><img src="{src}" alt="RogueVerse editorial artwork for {title}" loading="eager" decoding="async"></figure>'
    text = text[:lead.start()] + replacement + text[lead.end():]
    page.write_text(text, encoding='utf-8')
    changed.append((page.as_posix(), src, 'stored'))

print(f'Promoted finished existing art on {len(changed)} article pages')
for page, src, mode in changed:
    print('PROMOTED', mode, page, '->', src)
