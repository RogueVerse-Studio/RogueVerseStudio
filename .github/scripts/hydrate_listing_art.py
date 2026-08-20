from pathlib import Path
from urllib.parse import urlsplit
import os
import re

ROOT = Path('.')
GENERIC_MARKERS = (
    'animanga-updates-1440.webp',
    'movies-hero-desktop-v1.png',
    'games-hero-desktop-v1.png',
    'future-hero-desktop-v1.png',
    'our-culture-hero-desktop-v1.png',
    'community-hero-desktop-v1.png',
    'editorial-fallback.svg',
)


def article_lead_map():
    result = {}
    for path in ROOT.rglob('*.html'):
        if '.git' in path.parts:
            continue
        text = path.read_text(encoding='utf-8')
        if 'article-page' not in text:
            continue
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


def resolve_article(current_page: Path, href: str):
    if not href or href.startswith(('#', 'mailto:', 'javascript:', 'http://', 'https://', '//')):
        return None
    clean = urlsplit(href).path
    if not clean:
        return None
    candidate = current_page.parent / clean
    target = candidate if candidate.suffix.lower() == '.html' else candidate / 'index.html'
    return Path(os.path.normpath(target.as_posix()))


def relative_art(current_page: Path, article: Path, src: str):
    if src.startswith(('http://', 'https://', 'data:', '//')):
        return src
    asset = Path(os.path.normpath((article.parent / src).as_posix()))
    return os.path.relpath(asset, current_page.parent).replace('\\', '/')


def class_names(tag: str):
    match = re.search(r'class=(["\'])(.*?)\1', tag, flags=re.I | re.S)
    return match.group(2).split() if match else []


def href_value(tag: str):
    match = re.search(r'href=(["\'])(.*?)\1', tag, flags=re.I | re.S)
    return match.group(2) if match else None


def set_css_var(tag: str, name: str, value: str):
    style_match = re.search(r'style=(["\'])(.*?)\1', tag, flags=re.I | re.S)
    rule = f'{name}:url(\'{value}\');'
    if not style_match:
        return tag[:-1] + f' style="{rule}">'
    style = re.sub(
        rf'{re.escape(name)}\s*:\s*url\([^)]*\)\s*;?',
        '',
        style_match.group(2),
        flags=re.I,
    ).strip()
    if style and not style.endswith(';'):
        style += ';'
    style += rule
    quote = style_match.group(1)
    return tag[:style_match.start()] + f'style={quote}{style}{quote}' + tag[style_match.end():]


leads = article_lead_map()
changed = []

for page in ROOT.rglob('*.html'):
    if '.git' in page.parts:
        continue
    text = page.read_text(encoding='utf-8')
    original = text

    def hydrate_anchor(match):
        tag = match.group(0)
        classes = class_names(tag)
        is_omo = 'omo-card' in classes
        is_story_stack = 'story-stack-card' in classes
        if not (is_omo or is_story_stack):
            return tag

        href = href_value(tag)
        article = resolve_article(page, href)
        if not article or article not in leads or not article.exists():
            return tag

        # Preserve intentionally assigned art. Replace only missing/generic OMO card art.
        if is_omo and '--card-image' in tag and not any(marker in tag for marker in GENERIC_MARKERS):
            return tag

        art = relative_art(page, article, leads[article])
        return set_css_var(tag, '--card-image' if is_omo else '--rv-card-art', art)

    # Mark the homepage stack links so the generic anchor scanner can distinguish them safely.
    if 'story-stack' in text:
        def mark_story_stack(block_match):
            block = block_match.group(0)
            def mark_anchor(anchor_match):
                tag = anchor_match.group(0)
                classes = class_names(tag)
                if 'story-stack-card' in classes:
                    return tag
                class_match = re.search(r'class=(["\'])(.*?)\1', tag, flags=re.I | re.S)
                if class_match:
                    quote = class_match.group(1)
                    names = class_match.group(2).strip()
                    names = f'{names} story-stack-card'.strip()
                    return tag[:class_match.start()] + f'class={quote}{names}{quote}' + tag[class_match.end():]
                return tag[:-1] + ' class="story-stack-card">'
            return re.sub(r'<a\b[^>]*>', mark_anchor, block, flags=re.I | re.S)
        text = re.sub(
            r'<div\s+class=(["\'])story-stack\1[^>]*>.*?</div>',
            mark_story_stack,
            text,
            flags=re.I | re.S,
        )

    text = re.sub(r'<a\b[^>]*>', hydrate_anchor, text, flags=re.I | re.S)

    if text != original:
        page.write_text(text, encoding='utf-8')
        changed.append(page.as_posix())

print(f'Hydrated listing art on {len(changed)} pages')
for item in changed:
    print('LISTING', item)
