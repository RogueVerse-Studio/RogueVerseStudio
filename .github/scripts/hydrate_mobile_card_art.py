from pathlib import Path
import os
import re

ROOT = Path('.')
changed = []


def add_mobile_var(page, tag, desktop_name, mobile_name):
    pattern = rf'{re.escape(desktop_name)}\s*:\s*url\((["\']?)([^)"\']*rv-article-visual\.svg)\1\)\s*;?'
    match = re.search(pattern, tag, flags=re.I)
    if not match or mobile_name in tag:
        return tag
    desktop_rel = match.group(2)
    desktop_file = Path(os.path.normpath((page.parent / desktop_rel).as_posix()))
    mobile_file = desktop_file.with_name('rv-article-visual-mobile.svg')
    if not mobile_file.exists():
        return tag
    mobile_rel = os.path.relpath(mobile_file, page.parent).replace('\\', '/')
    style_match = re.search(r'style=(["\'])(.*?)\1', tag, flags=re.I | re.S)
    if not style_match:
        return tag
    style = style_match.group(2).strip()
    if style and not style.endswith(';'):
        style += ';'
    style += f'{mobile_name}:url(\'{mobile_rel}\');'
    quote = style_match.group(1)
    return tag[:style_match.start()] + f'style={quote}{style}{quote}' + tag[style_match.end():]


for page in ROOT.rglob('*.html'):
    if '.git' in page.parts:
        continue
    text = page.read_text(encoding='utf-8')
    original = text

    def patch_tag(match):
        tag = match.group(0)
        tag = add_mobile_var(page, tag, '--card-image', '--card-image-mobile')
        tag = add_mobile_var(page, tag, '--rv-card-art', '--rv-card-art-mobile')
        return tag

    text = re.sub(r'<a\b[^>]*>', patch_tag, text, flags=re.I | re.S)
    if text != original:
        page.write_text(text, encoding='utf-8')
        changed.append(page.as_posix())

print(f'Added mobile card art to {len(changed)} pages')
for item in changed:
    print('MOBILE_CARD', item)
