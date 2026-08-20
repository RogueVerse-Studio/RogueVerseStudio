from pathlib import Path
from urllib.parse import urlsplit
import re, html, hashlib, textwrap, os

root = Path('.')
generic_markers = (
    'animanga-updates-1440.webp','movies-hero-desktop-v1.png','games-hero-desktop-v1.png',
    'future-hero-desktop-v1.png','our-culture-hero-desktop-v1.png','community-hero-desktop-v1.png',
    'editorial-fallback.svg','rv-article-visual.svg','rv-article-visual-mobile.svg'
)

def strip_tags(value):
    return re.sub(r'<[^>]+>', '', value).replace('&amp;','&').replace('&quot;','"').replace('&#39;',"'").strip()

def lane(path):
    p = path.as_posix()
    if p.startswith('old-man-otaku/'):
        return ('omo','#05070b','#ff6a00','#1687ff','ANIMANGA UPDATES')
    if p.startswith('news/movies/'):
        return ('culture','#05070b','#ff6a00','#9c62ff','ROGUEVERSE MOVIES')
    if p.startswith('news/games/'):
        return ('culture','#04070c','#ff6a00','#13a9ff','ROGUEVERSE GAMING')
    if p.startswith('news/tech/') or p.startswith('future/'):
        return ('future','#04050c','#a56cff','#53b8ff','ROGUEVERSE FUTURE')
    if p.startswith('our-culture/'):
        return ('culture','#05070b','#ff6a00','#16b6c8','OUR CULTURE')
    if p.startswith('community/'):
        return ('community','#07100f','#ff8a3d','#55c7b8','ROGUEVERSE COMMUNITY')
    if p.startswith('mythra/') or p.startswith('create/'):
        return ('creator','#070707','#d5a94c','#ff6a00','ROGUEVERSE MYTHRA')
    return ('creator','#05070b','#ff6a00','#1687ff','ROGUEVERSE STUDIO')

def motif(title, accent, secondary, mobile=False):
    t = title.lower(); x = 665 if mobile else 1130; y = 250 if mobile else 175
    if any(k in t for k in ('game','xbox','playstation','nintendo','atari','raid','destiny')):
        return f'<g transform="translate({x} {y})" fill="none" stroke="{secondary}" stroke-width="15" opacity=".7"><path d="M-125 25c0-75 42-120 105-120h40c63 0 105 45 105 120 0 88-31 130-72 130-25 0-44-27-64-50h-178c-20 23-39 50-64 50-41 0-72-42-72-130z"/><path d="M-82 3h64M-50-29v64"/><circle cx="78" cy="-7" r="12" fill="{accent}" stroke="none"/><circle cx="113" cy="24" r="12" fill="{accent}" stroke="none"/></g>'
    if any(k in t for k in ('movie','film','tv','stream','cast','trailer')):
        return f'<g transform="translate({x} {y})" opacity=".72"><rect x="-145" y="-82" width="290" height="180" rx="14" fill="none" stroke="{secondary}" stroke-width="13"/><path d="M-145-23h290M-88-82l38 59M-16-82l38 59M56-82l38 59" stroke="{accent}" stroke-width="12"/></g>'
    if any(k in t for k in ('manga','anime','webtoon','comic','chapter','boruto','naruto','horikoshi')):
        return f'<g transform="translate({x} {y})" opacity=".72"><path d="M-155-92h130c34 0 59 17 75 43 16-26 41-43 75-43h130v210H125c-34 0-59 14-75 38-16-24-41-38-75-38h-130z" fill="none" stroke="{secondary}" stroke-width="12"/><path d="M0-48v200M-116-48h75M-116 1h75M41-48h75M41 1h75" stroke="{accent}" stroke-width="9"/></g>'
    if any(k in t for k in ('ai','robot','tech','computer','chip','future')):
        return f'<g transform="translate({x} {y})" opacity=".74"><rect x="-100" y="-100" width="200" height="200" rx="20" fill="none" stroke="{secondary}" stroke-width="14"/><rect x="-42" y="-42" width="84" height="84" fill="none" stroke="{accent}" stroke-width="11"/><path d="M-140-58h40M-140 0h40M-140 58h40M100-58h40M100 0h40M100 58h40M-58-140v40M0-140v40M58-140v40M-58 100v40M0 100v40M58 100v40" stroke="{secondary}" stroke-width="11"/></g>'
    if any(k in t for k in ('space','moon','planet','star')):
        return f'<g transform="translate({x} {y})" opacity=".76"><circle r="90" fill="none" stroke="{secondary}" stroke-width="14"/><ellipse rx="165" ry="50" fill="none" stroke="{accent}" stroke-width="11" transform="rotate(-14)"/></g>'
    if any(k in t for k in ('tabletop','convention','fandom','cosplay')):
        return f'<g transform="translate({x} {y})" opacity=".72"><path d="M0-120l110 62v124L0 130-110 66V-58z" fill="none" stroke="{secondary}" stroke-width="13"/><circle cx="-40" cy="-20" r="13" fill="{accent}"/><circle cx="43" cy="32" r="13" fill="{accent}"/><circle cx="7" cy="78" r="13" fill="{accent}"/></g>'
    return f'<g transform="translate({x} {y})" opacity=".62"><circle r="122" fill="none" stroke="{secondary}" stroke-width="12"/><circle r="84" fill="none" stroke="{accent}" stroke-width="8"/><path d="M0-145l17 101 52 21-52 21L0 145-17-101l-52-21 52-21z" fill="#e8edf6"/></g>'

def character_scene(kind, width, height, accent, secondary, mobile=False):
    if kind == 'omo':
        cx = width*.5 if mobile else width*.79; cy = height*.70 if mobile else height*.55; scale = 1.18 if mobile else 1
        return f'''<g transform="translate({cx:.0f} {cy:.0f}) scale({scale})"><circle r="225" fill="{secondary}" opacity=".12"/><circle r="178" fill="none" stroke="{accent}" stroke-width="8" opacity=".36"/><path d="M-165 265c18-170 49-284 113-337h104c64 53 95 167 113 337z" fill="#090c12" stroke="#202938" stroke-width="7"/><circle cy="-112" r="86" fill="#6d4634"/><path d="M-67-96c8 82 34 121 67 121s59-39 67-121c-2 106-22 158-67 158s-65-52-67-158z" fill="#e5e7e8"/><g fill="none" stroke="#050608" stroke-width="11"><rect x="-74" y="-123" width="64" height="41" rx="8"/><rect x="10" y="-123" width="64" height="41" rx="8"/><path d="M-10-103h20"/></g><path d="M0 45v180" stroke="{accent}" stroke-width="9"/><path d="M-96 90h58M38 90h58" stroke="{secondary}" stroke-width="8" opacity=".8"/></g>'''
    if kind == 'future':
        base = height*.79; obsx = width*.56 if mobile else width*.78
        skyline = ''.join(f'<rect x="{i*(width/10):.0f}" y="{base-(80+(i%5)*48):.0f}" width="{width/11:.0f}" height="{80+(i%5)*48:.0f}"/>' for i in range(11))
        return f'''<g opacity=".78" fill="#0a0d18">{skyline}</g><circle cx="{width*(.5 if mobile else .72):.0f}" cy="{height*(.45 if mobile else .43):.0f}" r="{min(width,height)*.24:.0f}" fill="none" stroke="{accent}" stroke-width="17" opacity=".38"/><g transform="translate({obsx:.0f} {base:.0f})"><path d="M-140 150c15-148 40-250 88-324l-17-116 38 87h62l38-87-17 116c48 74 73 176 88 324z" fill="#05070c" stroke="#232a3e" stroke-width="8"/><path d="M-70-288l27-106 34 111M70-288l-27-106-34 111" fill="#0c0f17" stroke="#2c3347" stroke-width="8"/><ellipse cy="-240" rx="88" ry="74" fill="#090c14"/><path d="M-55-238h110" stroke="{accent}" stroke-width="14" stroke-linecap="round" filter="url(#glow)"/><g transform="translate(-115 20)"><ellipse rx="58" ry="70" fill="#f0f1f2"/><path d="M-40-54l-21-45 45 25M40-54l21-45-45 25" fill="#11151f"/><circle cx="-21" cy="-10" r="9" fill="#111"/><circle cx="21" cy="-10" r="9" fill="#111"/></g></g>'''
    if kind == 'community':
        base = height*.78
        return f'''<rect x="0" y="{height*.44:.0f}" width="{width}" height="{height*.56:.0f}" fill="#17120e" opacity=".5"/><circle cx="{width*.18:.0f}" cy="{height*.48:.0f}" r="{min(width,height)*.11:.0f}" fill="{accent}" opacity=".18"/><g transform="translate({width*.55:.0f} {base:.0f})"><rect x="-300" y="-35" width="600" height="125" rx="35" fill="#201a18"/><rect x="-350" y="65" width="700" height="28" rx="14" fill="#38271c"/><g transform="translate(-210 -105)"><circle cy="-82" r="52" fill="#b87d5c"/><path d="M-65 28c11-84 33-131 65-147 32 16 54 63 65 147z" fill="#9b4150"/></g><g transform="translate(-65 -115)"><circle cy="-82" r="52" fill="#8d5b3f"/><path d="M-68 32c12-88 34-136 68-153 34 17 56 65 68 153z" fill="#0d1218"/></g><g transform="translate(95 -112)"><circle cy="-82" r="52" fill="#6b4432"/><path d="M-70 34c12-90 35-139 70-156 35 17 58 66 70 156z" fill="#111721"/></g><g transform="translate(235 -104)"><circle cy="-82" r="52" fill="#b67a59"/><path d="M-62 28c11-84 31-131 62-147 31 16 51 63 62 147z" fill="#1b5a67"/></g><rect x="65" y="-8" width="150" height="86" rx="8" fill="#f0e4c8" transform="rotate(-8 140 32)"/></g>'''
    if kind == 'culture':
        cx = width*.52 if mobile else width*.79; cy = height*.75 if mobile else height*.60
        return f'''<g transform="translate({cx:.0f} {cy:.0f})"><circle cy="-200" r="72" fill="#9a684b"/><path d="M-65-238q65-64 130 0" stroke="#1a1715" stroke-width="36" fill="none"/><path d="M-135 255c14-158 43-266 100-326h70c57 60 86 168 100 326z" fill="#0b0e13" stroke="#282f39" stroke-width="8"/><path d="M-100-34h200l-27 250H-73z" fill="#11151b" stroke="{accent}" stroke-width="8"/><path d="M-35-24h70v176h-70z" fill="#eee8df"/><path d="M-96 18l192 164M96 18l-192 164" stroke="{accent}" stroke-width="6" opacity=".7"/><ellipse cx="-72" cy="270" rx="72" ry="24" fill="#eae9e5"/><ellipse cx="72" cy="270" rx="72" ry="24" fill="#eae9e5"/></g>'''
    return f'''<g transform="translate({width*(.5 if mobile else .72):.0f} {height*(.72 if mobile else .58):.0f})"><g transform="translate(-115 0)"><circle cy="-165" r="63" fill="#a86f51"/><path d="M-75 195c12-139 36-234 75-291 39 57 63 152 75 291z" fill="#c95647" stroke="#ef7b63" stroke-width="7"/><path d="M78-235l32 400" stroke="#ffd36a" stroke-width="21" stroke-linecap="round" filter="url(#glow)"/></g><g transform="translate(120 0)"><circle cy="-165" r="63" fill="#6b4432"/><path d="M-79 200c12-142 37-239 79-296 42 57 67 154 79 296z" fill="#0b1118" stroke="#202b38" stroke-width="8"/><g fill="none" stroke="#08090c" stroke-width="9"><rect x="-52" y="-182" width="43" height="29" rx="7"/><rect x="9" y="-182" width="43" height="29" rx="7"/><path d="M-9-167h18"/></g><path d="M-100-250l-40 410" stroke="{secondary}" stroke-width="19" stroke-linecap="round" filter="url(#glow)"/></g></g>'''

def make_svg(path, title, kicker, mobile=False):
    kind, bg, accent, secondary, label = lane(path)
    width, height = (900,1200) if mobile else (1600,900)
    seed = int(hashlib.sha1((path.as_posix()+title).encode()).hexdigest()[:8],16)
    dots=[]
    for i in range(14):
        x=30+((seed>>(i%18))*(29+i*11))%(width-60); y=30+((seed>>((i+7)%18))*(31+i*7))%(height-60); r=7+((seed>>((i+11)%18))%30)
        dots.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{accent if i%2==0 else secondary}" opacity="{0.025+(i%5)*0.014:.3f}"/>')
    lines=textwrap.wrap(title,width=22 if mobile else 32)[:5 if mobile else 4]; fs=62 if mobile else 66; tx=58 if mobile else 84; ty=190 if mobile else 250
    tspans=''.join(f'<tspan x="{tx}" dy="{0 if i==0 else int(fs*1.08)}">{html.escape(line)}</tspan>' for i,line in enumerate(lines)); kick=html.escape((strip_tags(kicker) or 'ROGUEVERSE EDITORIAL')[:78])
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" role="img" aria-labelledby="t d"><title id="t">{html.escape(title)}</title><desc id="d">Original RogueVerse editorial illustration for {html.escape(title)}.</desc><defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop stop-color="{bg}"/><stop offset=".52" stop-color="#0b1020"/><stop offset="1" stop-color="{bg}"/></linearGradient><radialGradient id="ra"><stop stop-color="{accent}"/><stop offset="1" stop-color="{accent}" stop-opacity="0"/></radialGradient><radialGradient id="rb"><stop stop-color="{secondary}"/><stop offset="1" stop-color="{secondary}" stop-opacity="0"/></radialGradient><filter id="glow"><feGaussianBlur stdDeviation="11" result="g"/><feMerge><feMergeNode in="g"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs><rect width="{width}" height="{height}" fill="url(#bg)"/><circle cx="{width*.75:.0f}" cy="{height*.45:.0f}" r="{min(width,height)*.43:.0f}" fill="url(#ra)" opacity=".24"/><circle cx="{width*.58:.0f}" cy="{height*.66:.0f}" r="{min(width,height)*.38:.0f}" fill="url(#rb)" opacity=".16"/>{''.join(dots)}<g opacity=".09" stroke="#fff" stroke-width="2"><path d="M0 {height*.2:.0f}h{width}M0 {height*.4:.0f}h{width}M0 {height*.6:.0f}h{width}M0 {height*.8:.0f}h{width}"/><path d="M{width*.2:.0f} 0v{height}M{width*.4:.0f} 0v{height}M{width*.6:.0f} 0v{height}M{width*.8:.0f} 0v{height}"/></g>{motif(title,accent,secondary,mobile)}{character_scene(kind,width,height,accent,secondary,mobile)}<text x="{tx}" y="{68 if mobile else 74}" fill="{accent}" font-family="Arial,Helvetica,sans-serif" font-size="{21 if mobile else 24}" font-weight="800" letter-spacing="7">{label}</text><text x="{tx}" y="{112 if mobile else 120}" fill="#aeb9cb" font-family="Arial,Helvetica,sans-serif" font-size="{15 if mobile else 17}" font-weight="700" letter-spacing="2">{kick}</text><text x="{tx}" y="{ty}" fill="#fff" font-family="Arial,Helvetica,sans-serif" font-size="{fs}" font-weight="900">{tspans}</text><rect x="{tx}" y="{height-(75 if mobile else 70)}" width="{260 if mobile else 320}" height="8" fill="{accent}"/><rect x="{tx+(275 if mobile else 340)}" y="{height-(75 if mobile else 70)}" width="{110 if mobile else 145}" height="8" fill="{secondary}"/></svg>'''

def add_stylesheet(path,text):
    if 'site-2026.css' in text or '</head>' not in text: return text
    prefix='../'*len(path.parent.parts)
    return text.replace('</head>',f'<link rel="stylesheet" href="{prefix}site-2026.css?v=20260820-visual-v3">\n</head>',1)

def add_class(tag,name):
    m=re.search(r'class=(["\'])(.*?)\1',tag,flags=re.I|re.S)
    if not m: return tag[:-1]+f' class="{name}">'
    classes=m.group(2).split()
    if name not in classes: classes.append(name)
    return tag[:m.start()]+f'class={m.group(1)}{" ".join(classes)}{m.group(1)}'+tag[m.end():]

def set_card_image(tag,value):
    m=re.search(r'style=(["\'])(.*?)\1',tag,flags=re.I|re.S); rule=f'--card-image:url("{value}");'
    if not m: return tag[:-1]+f' style="{rule}">'
    style=re.sub(r'--card-image\s*:\s*url\([^)]*\)\s*;?','',m.group(2),flags=re.I).strip()
    if style and not style.endswith(';'): style+=';'
    style+=rule
    return tag[:m.start()]+f'style={m.group(1)}{style}{m.group(1)}'+tag[m.end():]

def replace_series_art(path,text):
    if path.as_posix()=='mythra/index.html':
        text=re.sub(r'(<a id="sentou"[^>]*>)<img[^>]*>',r'\1<img src="../assets/mythra/sentou-title.svg" alt="Sentou original RogueVerse Mythra title artwork" loading="lazy" decoding="async">',text,count=1,flags=re.I|re.S)
    if path.as_posix()=='index.html':
        replacements={
          'sentou':'<img src="assets/mythra/sentou-title.svg" alt="Sentou original RogueVerse Mythra title artwork" loading="lazy" decoding="async">',
          'love':'<img src="assets/mythra/love-power-ai-love-cover.png" alt="Love × Power original RogueVerse Mythra artwork" loading="lazy" decoding="async">',
          'stranded':'<img src="assets/mythra/stranded-title.webp" alt="Stranded in a Bounty Hunter World original RogueVerse Mythra title artwork" loading="lazy" decoding="async">',
        }
        for cls,img in replacements.items():
            text=re.sub(rf'(<a class="series-card series-card--{cls}"[^>]*>)\s*<img[^>]*>',rf'\1\n          {img}',text,count=1,flags=re.I|re.S)
    return text

changed=set(); generated=set()

# Pass 1: article headers + known Mythra placeholder corrections.
for path in root.rglob('*.html'):
    if '.git' in path.parts: continue
    text=path.read_text(encoding='utf-8'); original=text
    text=add_stylesheet(path,text); text=replace_series_art(path,text)
    if 'article-page' in text:
        h1=re.search(r'<h1[^>]*>(.*?)</h1>',text,flags=re.I|re.S); title=strip_tags(h1.group(1)) if h1 else path.parent.name.replace('-',' ').title()
        km=re.search(r'<p\s+class=["\']kicker["\'][^>]*>(.*?)</p>',text,flags=re.I|re.S); kicker=strip_tags(km.group(1)) if km else ''
        desktop=path.parent/'rv-article-visual.svg'; mobile=path.parent/'rv-article-visual-mobile.svg'
        lead=re.search(r'<figure\s+class=["\'][^"\']*article-lead-art[^"\']*["\'][^>]*>.*?</figure>',text,flags=re.I|re.S)
        needs=not lead or any(marker in lead.group(0) for marker in generic_markers)
        if needs:
            desktop.write_text(make_svg(path,title,kicker,False),encoding='utf-8'); mobile.write_text(make_svg(path,title,kicker,True),encoding='utf-8'); generated.update((desktop.as_posix(),mobile.as_posix()))
            alt=html.escape(f'Original RogueVerse editorial illustration for {title}',quote=True)
            figure=f'<figure class="article-lead-art rv-auto-article-art"><picture><source media="(max-width:680px)" srcset="rv-article-visual-mobile.svg"><img src="rv-article-visual.svg" alt="{alt}" loading="eager" decoding="async"></picture></figure>'
            if lead: text=text[:lead.start()]+figure+text[lead.end():]
            else:
                dek=re.search(r'(<p\s+class=["\']dek["\'][^>]*>.*?</p>)',text,flags=re.I|re.S); anchor=dek or h1
                if anchor: text=text[:anchor.end()]+'\n'+figure+text[anchor.end():]
    if text!=original: path.write_text(text,encoding='utf-8'); changed.add(path.as_posix())

# Map article lead art so cards can inherit it.
lead_map={}
for path in root.rglob('*.html'):
    if '.git' in path.parts: continue
    text=path.read_text(encoding='utf-8')
    if 'article-page' not in text: continue
    lead=re.search(r'<figure\s+class=["\'][^"\']*article-lead-art[^"\']*["\'][^>]*>(.*?)</figure>',text,flags=re.I|re.S)
    if not lead: continue
    im=re.search(r'<img[^>]+src=(["\'])(.*?)\1',lead.group(1),flags=re.I|re.S)
    if im: lead_map[path]=im.group(2)

def visual_for(current,href):
    if not href or href.startswith(('#','mailto:','javascript:','http://','https://','//')): return None
    clean=urlsplit(href).path
    if not clean: return None
    candidate=current.parent/clean; target=candidate if candidate.suffix.lower()=='.html' else candidate/'index.html'; target=Path(os.path.normpath(target.as_posix()))
    if target not in lead_map or not target.exists(): return None
    src=lead_map[target]
    if src.startswith(('http://','https://','data:','//')): return src
    asset=Path(os.path.normpath((target.parent/src).as_posix()))
    return os.path.relpath(asset,current.parent).replace('\\','/')

# Pass 2: clickable article cards use the article's actual lead image.
for path in root.rglob('*.html'):
    if '.git' in path.parts: continue
    text=path.read_text(encoding='utf-8'); original=text
    def replace_anchor(match):
        tag=match.group(0); cm=re.search(r'class=(["\'])(.*?)\1',tag,flags=re.I|re.S)
        if not cm or 'section-card' not in cm.group(2).split(): return tag
        hm=re.search(r'href=(["\'])(.*?)\1',tag,flags=re.I|re.S)
        if not hm: return tag
        art=visual_for(path,hm.group(2))
        if not art: return tag
        dedicated='--card-image' in tag and not any(marker in tag for marker in generic_markers)
        if dedicated: return tag
        return set_card_image(add_class(tag,'section-card--image'),art)
    text=re.sub(r'<a\b[^>]*>',replace_anchor,text,flags=re.I|re.S)
    if text!=original: path.write_text(text,encoding='utf-8'); changed.add(path.as_posix())

# Dynamic story-list links also hydrate from their article lead image.
script=root/'script.js'
if script.exists():
    js=script.read_text(encoding='utf-8'); marker='data-rv-story-art-hydrator'
    if marker not in js:
        js += r'''

// data-rv-story-art-hydrator: dynamically generated story links use each article's lead art.
(() => {
  const links = [...document.querySelectorAll('.story-list a')];
  if (!links.length) return;
  links.forEach(async (link) => {
    try {
      const response = await fetch(link.href, {cache: 'force-cache'});
      if (!response.ok) return;
      const doc = new DOMParser().parseFromString(await response.text(), 'text/html');
      const img = doc.querySelector('.article-lead-art img');
      if (!img) return;
      const artUrl = new URL(img.getAttribute('src'), link.href).href;
      link.style.setProperty('--rv-card-art', `url("${artUrl}")`);
    } catch (_) {}
  });
})();
'''
        script.write_text(js,encoding='utf-8')

print(f'Updated {len(changed)} HTML files')
print(f'Generated/refreshed {len(generated)} responsive visual assets')
for p in sorted(changed): print('PAGE',p)
for p in sorted(generated): print('ART',p)
