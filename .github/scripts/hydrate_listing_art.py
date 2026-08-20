from pathlib import Path
from urllib.parse import urlsplit
import html
import os
import re
import textwrap

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
        if 'article-lead-art' not in text:
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


def safe_slug(href: str):
    raw = urlsplit(href or '').path.strip('/').split('/')[-1] or 'story'
    return re.sub(r'[^a-zA-Z0-9-]+', '-', raw).strip('-').lower() or 'story'


def pretty_slug(slug: str):
    return ' '.join(word.capitalize() for word in slug.replace('-', ' ').split())


def orphan_omo_svg(title: str):
    lines = textwrap.wrap(title, width=28)[:4]
    tspans = ''.join(
        f'<tspan x="78" dy="{0 if i == 0 else 70}">{html.escape(line)}</tspan>'
        for i, line in enumerate(lines)
    )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 675" role="img" aria-labelledby="t d"><title id="t">{html.escape(title)}</title><desc id="d">Original RogueVerse AniManga editorial card for {html.escape(title)}.</desc><defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#04070b"/><stop offset=".55" stop-color="#0a1222"/><stop offset="1" stop-color="#160a05"/></linearGradient><radialGradient id="o"><stop stop-color="#ff6a00"/><stop offset="1" stop-color="#ff6a00" stop-opacity="0"/></radialGradient><radialGradient id="b"><stop stop-color="#1687ff"/><stop offset="1" stop-color="#1687ff" stop-opacity="0"/></radialGradient></defs><rect width="1200" height="675" fill="url(#bg)"/><circle cx="960" cy="330" r="300" fill="url(#o)" opacity=".26"/><circle cx="760" cy="350" r="270" fill="url(#b)" opacity=".20"/><g opacity=".09" stroke="#fff" stroke-width="2"><path d="M0 135h1200M0 270h1200M0 405h1200M0 540h1200"/><path d="M240 0v675M480 0v675M720 0v675M960 0v675"/></g><g transform="translate(935 365)"><circle r="185" fill="none" stroke="#1687ff" stroke-width="7" opacity=".28"/><circle r="148" fill="none" stroke="#ff6a00" stroke-width="7" opacity=".32"/><path d="M-135 255c14-140 43-235 92-291h86c49 56 78 151 92 291z" fill="#080c12" stroke="#252d39" stroke-width="7"/><circle cy="-85" r="76" fill="#704733"/><path d="M-58-70c7 72 29 108 58 108s51-36 58-108c-2 94-18 140-58 140s-56-46-58-140z" fill="#e9eaeb"/><g fill="none" stroke="#050608" stroke-width="10"><rect x="-66" y="-96" width="57" height="36" rx="8"/><rect x="9" y="-96" width="57" height="36" rx="8"/><path d="M-9-78h18"/></g><path d="M0 60v150" stroke="#ff6a00" stroke-width="8"/><path d="M-80 100h45M35 100h45" stroke="#1687ff" stroke-width="7"/></g><path d="M690 96l14 122 43 18-43 18-14 190-14-190-43-18 43-18z" fill="#eaf0f7" opacity=".78"/><text x="78" y="68" fill="#ff7b19" font-family="Arial,sans-serif" font-size="21" font-weight="800" letter-spacing="6">ANIMANGA UPDATES</text><text x="78" y="132" fill="#fff" font-family="Arial,sans-serif" font-size="58" font-weight="900">{tspans}</text><rect x="78" y="590" width="260" height="8" fill="#ff6a00"/><rect x="355" y="590" width="120" height="8" fill="#1687ff"/></svg>'''


leads = article_lead_map()
changed = []
generated = []

for page in ROOT.rglob('*.html'):
    if '.git' in page.parts:
        continue
    text = page.read_text(encoding='utf-8')
    original = text

    # Mark homepage story-stack links so they can be treated as image cards.
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
                    names = f'{class_match.group(2).strip()} story-stack-card'.strip()
                    return tag[:class_match.start()] + f'class={quote}{names}{quote}' + tag[class_match.end():]
                return tag[:-1] + ' class="story-stack-card">'
            return re.sub(r'<a\b[^>]*>', mark_anchor, block, flags=re.I | re.S)
        text = re.sub(
            r'<div\s+class=(["\'])story-stack\1[^>]*>.*?</div>',
            mark_story_stack,
            text,
            flags=re.I | re.S,
        )

    def hydrate_anchor(match):
        tag = match.group(0)
        classes = class_names(tag)
        is_omo = 'omo-card' in classes
        is_story_stack = 'story-stack-card' in classes
        if not (is_omo or is_story_stack):
            return tag

        href = href_value(tag)

        # Preserve deliberately assigned OMO franchise/editorial artwork.
        if is_omo and '--card-image' in tag and not any(marker in tag for marker in GENERIC_MARKERS):
            return tag

        article = resolve_article(page, href)
        if article and article in leads and article.exists():
            art = relative_art(page, article, leads[article])
            return set_css_var(tag, '--card-image' if is_omo else '--rv-card-art', art)

        # Orphan/missing AniManga article links still receive their own visual instead of the shared banner.
        if is_omo:
            slug = safe_slug(href)
            title = pretty_slug(slug)
            art_dir = page.parent / 'card-art'
            art_dir.mkdir(exist_ok=True)
            art_file = art_dir / f'{slug}-card.svg'
            art_file.write_text(orphan_omo_svg(title), encoding='utf-8')
            generated.append(art_file.as_posix())
            art = os.path.relpath(art_file, page.parent).replace('\\', '/')
            return set_css_var(tag, '--card-image', art)

        return tag

    text = re.sub(r'<a\b[^>]*>', hydrate_anchor, text, flags=re.I | re.S)

    if text != original:
        page.write_text(text, encoding='utf-8')
        changed.append(page.as_posix())

print(f'Hydrated listing art on {len(changed)} pages')
print(f'Generated {len(generated)} orphan-card visuals')
for item in changed:
    print('LISTING', item)
for item in generated:
    print('ORPHAN_ART', item)
