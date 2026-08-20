from pathlib import Path
from urllib.parse import urlsplit
import os
import re

ROOT = Path('.')
html_files = [p for p in ROOT.rglob('*.html') if '.git' not in p.parts]
article_pages = []
missing_article_art = []
missing_listing_art = []
missing_image_files = []
major_pages_without_visual_hero = []
placeholder_refs = []
broken_internal_links = []

visual_hero_markers = ('section-art-hero', 'art-hero', 'rv-hero', 'omo-hero', 'culture-hero', 'wellness-card')


def exists_from(page, value):
    if value.startswith(('http://', 'https://', '//', 'data:', '#', 'mailto:', 'javascript:')):
        return True
    value = value.split('?')[0].split('#')[0]
    if not value:
        return True
    return Path(os.path.normpath((page.parent / value).as_posix())).exists()


for page in html_files:
    text = page.read_text(encoding='utf-8')
    rel = page.as_posix()

    if 'article-shell' in text:
        article_pages.append(rel)
        if 'article-lead-art' not in text:
            missing_article_art.append(rel)

    if 'under-construction' in text.lower():
        placeholder_refs.append(rel)

    if page.name == 'index.html' and len(page.parent.parts) <= 2 and 'article-shell' not in text:
        if not any(marker in text for marker in visual_hero_markers):
            major_pages_without_visual_hero.append(rel)

    for match in re.finditer(r'<a\b[^>]*class=(["\'])(.*?)\1[^>]*>', text, flags=re.I | re.S):
        tag = match.group(0)
        classes = match.group(2).split()
        if 'omo-card' in classes and '--card-image' not in tag:
            missing_listing_art.append(f'{rel} :: OMO card :: {tag[:140]}')
        if 'story-stack-card' in classes and '--rv-card-art' not in tag:
            missing_listing_art.append(f'{rel} :: story stack :: {tag[:140]}')

    for block in re.finditer(r'<div\s+class=(["\'])[^"\']*story-list[^"\']*\1[^>]*>(.*?)</div>', text, flags=re.I | re.S):
        for anchor in re.finditer(r'<a\b[^>]*>', block.group(2), flags=re.I | re.S):
            if '--rv-card-art' not in anchor.group(0):
                missing_listing_art.append(f'{rel} :: story-list :: {anchor.group(0)[:140]}')

    for img in re.finditer(r'<img[^>]+src=(["\'])(.*?)\1', text, flags=re.I | re.S):
        src = img.group(2)
        if not exists_from(page, src):
            missing_image_files.append(f'{rel} -> {src}')

    for source in re.finditer(r'<source[^>]+srcset=(["\'])(.*?)\1', text, flags=re.I | re.S):
        first = source.group(2).split(',')[0].strip().split()[0]
        if first and not exists_from(page, first):
            missing_image_files.append(f'{rel} -> {first}')

    for anchor in re.finditer(r'<a[^>]+href=(["\'])(.*?)\1', text, flags=re.I | re.S):
        href = anchor.group(2)
        if href.startswith(('#', 'http://', 'https://', '//', 'mailto:', 'javascript:')):
            continue
        clean = urlsplit(href).path
        if not clean:
            continue
        candidate = page.parent / clean
        target = candidate if candidate.suffix else candidate / 'index.html'
        target = Path(os.path.normpath(target.as_posix()))
        if not target.exists():
            broken_internal_links.append(f'{rel} -> {href}')

report = [
    '# RogueVerse Visual Coverage Audit',
    '',
    f'- HTML pages scanned: **{len(html_files)}**',
    f'- Article pages detected: **{len(article_pages)}**',
    f'- Article pages missing lead art: **{len(missing_article_art)}**',
    f'- Listing cards missing visual assignment: **{len(missing_listing_art)}**',
    f'- Missing local image files: **{len(missing_image_files)}**',
    f'- Major landing pages without visual hero: **{len(major_pages_without_visual_hero)}**',
    f'- Pages still referencing under-construction imagery/text: **{len(placeholder_refs)}**',
    f'- Broken internal links: **{len(broken_internal_links)}**',
    '',
]

sections = [
    ('Articles missing lead art', missing_article_art),
    ('Listing cards missing art', missing_listing_art),
    ('Missing local image files', missing_image_files),
    ('Major pages without visual hero', major_pages_without_visual_hero),
    ('Under-construction references', placeholder_refs),
    ('Broken internal links', broken_internal_links),
]
for title, items in sections:
    report.append(f'## {title}')
    if not items:
        report.append('- None')
    else:
        report.extend(f'- `{item}`' for item in sorted(set(items)))
    report.append('')

Path('visual-audit.md').write_text('\n'.join(report), encoding='utf-8')
print('\n'.join(report[:12]))
