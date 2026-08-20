from pathlib import Path
from urllib.parse import urlsplit
import os
import re

ROOT = Path('.')
TEMP_MARKERS = ('rv-article-visual.svg', 'rv-article-visual-mobile.svg', 'editorial-fallback.svg')
PREFERRED = ('feature', 'hero', 'header', 'cover', 'lead', '01-', '01.', 'key-visual')
SKIP = ('logo', 'icon', 'sword-mark', 'avatar', 'qr', 'badge')


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
            score += 100 - i * 7
    ext = Path(urlsplit(src).path).suffix.lower()
    if ext in ('.webp', '.jpg', '.jpeg', '.png'):
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
        new_tag = tag[:cls.start()] + f'class={cls.group(1)}{" ".join(names)}{cls.group(1)}' + tag[cls.end():]
    else:
        new_tag = tag[:-1] + ' class="article-lead-art">'
    return figure[:opening.start()] + new_tag + figure[opening.end():]


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

    if not candidates:
        continue

    candidates.sort(key=lambda item: (item[0], -item[1]), reverse=True)
    score, start, end, figure, src = candidates[0]
    if score < 0:
        continue

    promoted = add_lead_class(figure)
    # Move the approved/embedded article figure into the lead position and remove its duplicate.
    if start > lead.end():
        before = text[:lead.start()]
        between = text[lead.end():start]
        after = text[end:]
        text = before + promoted + between + after
    else:
        # Unusual article ordering; avoid risky mutation.
        continue

    page.write_text(text, encoding='utf-8')
    changed.append((page.as_posix(), src))

print(f'Promoted finished embedded art on {len(changed)} article pages')
for page, src in changed:
    print('PROMOTED', page, '->', src)
