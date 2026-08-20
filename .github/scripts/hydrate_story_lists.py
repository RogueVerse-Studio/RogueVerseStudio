from pathlib import Path
from urllib.parse import urlsplit
import os
import re

ROOT = Path('.')


def lead_map():
    result = {}
    for path in ROOT.rglob('*.html'):
        if '.git' in path.parts:
            continue
        text = path.read_text(encoding='utf-8')
        figure = re.search(
            r'<figure\s+class=(["\'])[^"\']*article-lead-art[^"\']*\1[^>]*>(.*?)</figure>',
            text,
            flags=re.I | re.S,
        )
        if not figure:
            continue
        image = re.search(r'<img[^>]+src=(["\'])(.*?)\1', figure.group(2), flags=re.I | re.S)
        if image:
            result[path] = image.group(2)
    return result


def target_for(page, href):
    if not href or href.startswith(('#', 'http://', 'https://', '//', 'mailto:', 'javascript:')):
        return None
    clean = urlsplit(href).path
    candidate = page.parent / clean
    target = candidate if candidate.suffix.lower() == '.html' else candidate / 'index.html'
    return Path(os.path.normpath(target.as_posix()))


def relative_art(page, article, src):
    if src.startswith(('http://', 'https://', '//', 'data:')):
        return src
    asset = Path(os.path.normpath((article.parent / src).as_posix()))
    return os.path.relpath(asset, page.parent).replace('\\', '/')


def set_var(tag, art):
    style_match = re.search(r'style=(["\'])(.*?)\1', tag, flags=re.I | re.S)
    rule = f'--rv-card-art:url(\'{art}\');'
    if not style_match:
        return tag[:-1] + f' style="{rule}">'
    style = re.sub(r'--rv-card-art\s*:\s*url\([^)]*\)\s*;?', '', style_match.group(2), flags=re.I).strip()
    if style and not style.endswith(';'):
        style += ';'
    style += rule
    quote = style_match.group(1)
    return tag[:style_match.start()] + f'style={quote}{style}{quote}' + tag[style_match.end():]


leads = lead_map()
changed = []

for page in ROOT.rglob('*.html'):
    if '.git' in page.parts:
        continue
    text = page.read_text(encoding='utf-8')
    original = text

    def hydrate_block(block_match):
        block = block_match.group(0)
        def hydrate_anchor(anchor_match):
            tag = anchor_match.group(0)
            href_match = re.search(r'href=(["\'])(.*?)\1', tag, flags=re.I | re.S)
            if not href_match:
                return tag
            target = target_for(page, href_match.group(2))
            if not target or target not in leads or not target.exists():
                return tag
            return set_var(tag, relative_art(page, target, leads[target]))
        return re.sub(r'<a\b[^>]*>', hydrate_anchor, block, flags=re.I | re.S)

    text = re.sub(
        r'<div\s+class=(["\'])[^"\']*story-list[^"\']*\1[^>]*>.*?</div>',
        hydrate_block,
        text,
        flags=re.I | re.S,
    )

    if text != original:
        page.write_text(text, encoding='utf-8')
        changed.append(page.as_posix())

print(f'Hydrated static story lists on {len(changed)} pages')
for item in changed:
    print('STORY_LIST', item)
