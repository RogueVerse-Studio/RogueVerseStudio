from __future__ import annotations

import argparse
import html
import json
import os
import shutil
from datetime import datetime, timezone
from email.utils import format_datetime
from pathlib import Path, PurePosixPath
from xml.sax.saxutils import escape as xml_escape

from package_tools import (
    SECTION_CONFIG,
    SITE_URL,
    PackageError,
    load_package,
    make_captions,
    require_valid_package,
    strip_html,
)


AUTOMATION_START = "<!-- RV_AUTOMATION_ARTICLES_START -->"
AUTOMATION_END = "<!-- RV_AUTOMATION_ARTICLES_END -->"


def _article_url(package: dict) -> str:
    return f"{SITE_URL}/{package['section']}/{package['slug']}/"


def _root_prefix(package: dict) -> str:
    return "../" * (len(PurePosixPath(package["section"]).parts) + 1)


def _render_blocks(blocks: list[dict]) -> str:
    rendered: list[str] = []
    for block in blocks:
        kind = block["type"]
        content = block["html"].strip()
        if kind == "paragraph":
            rendered.append(f"  <p>{content}</p>")
        elif kind == "heading":
            rendered.append(f"  <h2>{content}</h2>")
        elif kind == "blockquote":
            rendered.append(f"  <blockquote>{content}</blockquote>")
        elif kind == "list":
            items = [item.strip() for item in content.split("\n") if item.strip()]
            rendered.append("  <ul>" + "".join(f"<li>{item}</li>" for item in items) + "</ul>")
    return "\n".join(rendered)


def _render_sources(sources: list[dict]) -> str:
    if not sources:
        return ""
    links = " · ".join(
        f'<a href="{html.escape(source["url"], quote=True)}" target="_blank" rel="noopener">'
        f'{html.escape(source["label"])}</a>'
        for source in sources
    )
    return (
        '  <aside class="article-sources">\n'
        "    <h2>Reporting sources</h2>\n"
        f"    <p>{links}</p>\n"
        "  </aside>"
    )


def render_article(package: dict) -> str:
    config = SECTION_CONFIG[package["section"]]
    prefix = _root_prefix(package)
    hero_src = prefix + package["hero"]["src"]
    title = html.escape(package["title"])
    description = html.escape(package["description"], quote=True)
    kicker = html.escape(package["kicker"])
    dek = html.escape(package["dek"])
    label = html.escape(config["label"])
    blocks = _render_blocks(package["article"]["blocks"])
    sources = _render_sources(package["article"].get("sources", []))
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <meta name="description" content="{description}">
  <title>{title} | RogueVerse Studio</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Orbitron:wght@600;700&family=Russo+One&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{prefix}styles.css">
  <link rel="icon" href="{prefix}assets/brand/studio/rogueverse-sword-mark.png">
</head>
<body class="article-page">
<header class="site-header article-header">
  <a class="brand brand-image" href="{prefix}"><img src="{prefix}assets/brand/studio/rogueverse-sword-mark.png" alt=""><span><b>ROGUEVERSE</b><small>STUDIO</small></span></a>
  <a class="button button-primary" href="../">{label}</a>
</header>
<main>
<article class="article-shell article-shell--feature">
  <p class="kicker">{kicker}</p>
  <h1>{title}</h1>
  <p class="dek">{dek}</p>
  <figure class="article-lead-art"><img src="{hero_src}" alt="{html.escape(package['hero']['alt'], quote=True)}" decoding="async"></figure>
{blocks}
{sources}
  <aside class="article-sources">
    <h2>Editorial image &amp; ownership notice</h2>
    <p>Third-party editorial materials remain the property of their respective creators, publishers, studios and rights holders. RogueVerse uses them only for reporting and commentary and does not claim ownership.</p>
  </aside>
  <p><a href="../">← More {label}</a></p>
</article>
</main>
<footer><a class="brand brand-image" href="{prefix}"><img src="{prefix}assets/brand/studio/rogueverse-sword-mark.png" alt=""><span><b>ROGUEVERSE</b><small>STUDIO</small></span></a><p>© <span data-year></span> RogueVerse Studio</p></footer>
<script src="{prefix}script.js"></script>
</body>
</html>
"""


def _relative_hero_for_index(package: dict) -> str:
    section = PurePosixPath(package["section"])
    return os.path.relpath(package["hero"]["src"], section.as_posix()).replace("\\", "/")


def render_index_card(package: dict) -> str:
    config = SECTION_CONFIG[package["section"]]
    href = f'{package["slug"]}/'
    kicker = html.escape(package["kicker"])
    title = html.escape(package["title"])
    description = html.escape(package["description"])
    if package["section"] == "news/movies":
        return f'        <a href="{href}"><small>{kicker}</small><h3>{title}</h3><p>{description}</p></a>'
    hero = html.escape(_relative_hero_for_index(package), quote=True)
    return (
        f'          <a class="{config["card_class"]}" href="{href}" '
        f'style="--card-image: url(&quot;{hero}&quot;);"><small>{kicker}</small>'
        f"<h3>{title}</h3><p>{description}</p></a>"
    )


def update_index(package: dict, site_root: Path) -> Path:
    index_path = site_root / SECTION_CONFIG[package["section"]]["index"]
    text = index_path.read_text(encoding="utf-8")
    if f'href="{package["slug"]}/"' in text:
        return index_path
    if AUTOMATION_START not in text or AUTOMATION_END not in text:
        raise PackageError(f"Automation markers are missing from {index_path}")
    card = render_index_card(package)
    text = text.replace(AUTOMATION_START, f"{AUTOMATION_START}\n{card}", 1)
    index_path.write_text(text, encoding="utf-8", newline="\n")
    return index_path


def update_feed(package: dict, site_root: Path) -> Path:
    feed_path = site_root / "feed.xml"
    text = feed_path.read_text(encoding="utf-8")
    url = _article_url(package)
    if f"<guid isPermaLink=\"true\">{url}</guid>" in text:
        return feed_path
    published = datetime.fromisoformat(package["publish_at"].replace("Z", "+00:00"))
    if published.tzinfo is None:
        published = published.replace(tzinfo=timezone.utc)
    config = SECTION_CONFIG[package["section"]]
    item = f"""
    <item>
      <title><![CDATA[{package['title']}]]></title>
      <link>{url}</link>
      <guid isPermaLink="true">{url}</guid>
      <pubDate>{format_datetime(published)}</pubDate>
      <dc:creator><![CDATA[{config['brand']}]]></dc:creator>
      <category><![CDATA[{config['label']}]]></category>
      <description><![CDATA[{package['description']}]]></description>
      <media:content url="{SITE_URL}/{package['hero']['src']}" medium="image" />
      <content:encoded><![CDATA[
        <p><strong>{config['brand']}</strong></p>
        <p>{strip_html(package['dek'])}</p>
        <p><a href="{url}">Read Full Article</a></p>
      ]]></content:encoded>
    </item>
"""
    first_item = text.find("    <item>")
    if first_item == -1:
        first_item = text.find("  </channel>")
    if first_item == -1:
        raise PackageError("feed.xml does not contain a channel insertion point")
    text = text[:first_item] + item + text[first_item:]
    text = re_last_build_date(text, format_datetime(datetime.now(timezone.utc)))
    feed_path.write_text(text, encoding="utf-8", newline="\n")
    return feed_path


def re_last_build_date(text: str, date_value: str) -> str:
    import re

    return re.sub(
        r"<lastBuildDate>.*?</lastBuildDate>",
        f"<lastBuildDate>{date_value}</lastBuildDate>",
        text,
        count=1,
    )


def write_discovery_files(site_root: Path) -> list[Path]:
    urls: list[str] = []
    ignored_roots = {".git", "automation", "content-packages", "tests", "node_modules"}
    for index_path in sorted(site_root.rglob("index.html")):
        relative = index_path.relative_to(site_root)
        if relative.parts and relative.parts[0] in ignored_roots:
            continue
        parent = relative.parent.as_posix()
        urls.append(f"{SITE_URL}/" if parent == "." else f"{SITE_URL}/{parent}/")
    sitemap = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    sitemap.extend(f"  <url><loc>{xml_escape(url)}</loc></url>" for url in urls)
    sitemap.append("</urlset>")
    sitemap_path = site_root / "sitemap.xml"
    sitemap_path.write_text("\n".join(sitemap) + "\n", encoding="utf-8", newline="\n")
    robots_path = site_root / "robots.txt"
    robots_path.write_text(
        f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n",
        encoding="utf-8",
        newline="\n",
    )
    return [sitemap_path, robots_path]


def prepare_video_inputs(package: dict, site_root: Path, output_dir: Path) -> Path:
    public_root = output_dir / "video-public" / "site"
    asset_paths = {package["hero"]["src"]}
    asset_paths.update(scene["image"] for scene in package["video"]["scenes"] if scene.get("image"))
    if package["video"].get("audio"):
        asset_paths.add(package["video"]["audio"])
    for asset in asset_paths:
        source = site_root / PurePosixPath(asset)
        target = public_root / PurePosixPath(asset)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)

    props = {
        "title": package["title"],
        "dek": package["dek"],
        "brand": SECTION_CONFIG[package["section"]]["brand"],
        "articleUrl": _article_url(package),
        "durationSeconds": package["video"]["duration_seconds"],
        "audio": f"site/{package['video']['audio']}" if package["video"].get("audio") else None,
        "scenes": [
            {
                "headline": scene["headline"],
                "body": scene["body"],
                "image": f"site/{scene.get('image') or package['hero']['src']}",
            }
            for scene in package["video"]["scenes"]
        ],
        "captions": package["video"].get("captions")
        or make_captions(package["video"]["scenes"], package["video"]["duration_seconds"]),
    }
    props_path = output_dir / "video-props.json"
    props_path.write_text(json.dumps(props, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return props_path


def build(package_path: Path, site_root: Path, output_dir: Path) -> dict:
    package = load_package(package_path)
    require_valid_package(package, site_root)

    article_dir = site_root / PurePosixPath(package["section"]) / package["slug"]
    article_dir.mkdir(parents=True, exist_ok=True)
    article_path = article_dir / "index.html"
    if article_path.exists():
        raise PackageError(f"Article already exists: {article_path}")
    article_path.write_text(render_article(package), encoding="utf-8", newline="\n")

    changed = [article_path, update_index(package, site_root), update_feed(package, site_root)]
    changed.extend(write_discovery_files(site_root))
    output_dir.mkdir(parents=True, exist_ok=True)
    props_path = prepare_video_inputs(package, site_root, output_dir)

    approved_dir = site_root / "content-packages" / "approved"
    approved_dir.mkdir(parents=True, exist_ok=True)
    approved_path = approved_dir / f"{package['slug']}.json"
    approved_package = dict(package)
    approved_package["workflow_state"] = "awaiting_pull_request_merge"
    approved_path.write_text(
        json.dumps(approved_package, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    changed.append(approved_path)

    manifest = {
        "slug": package["slug"],
        "package": str(approved_path.relative_to(site_root)).replace("\\", "/"),
        "article": str(article_path.relative_to(site_root)).replace("\\", "/"),
        "article_url": _article_url(package),
        "video_props": str(props_path),
        "changed": sorted({str(path.relative_to(site_root)).replace("\\", "/") for path in changed}),
        "social": package["social"],
    }
    manifest_path = output_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description="Build one RogueVerse content package")
    parser.add_argument("--package", required=True, type=Path)
    parser.add_argument("--site-root", type=Path, default=Path.cwd())
    parser.add_argument("--output-dir", type=Path, default=Path("automation/build"))
    parser.add_argument("--check", action="store_true", help="Validate only; do not write files")
    args = parser.parse_args()

    site_root = args.site_root.resolve()
    package = load_package(args.package)
    require_valid_package(package, site_root)
    if args.check:
        print(f"Valid package: {package['slug']}")
        return 0
    manifest = build(args.package, site_root, args.output_dir.resolve())
    print(json.dumps(manifest, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except PackageError as exc:
        print(exc)
        raise SystemExit(2)
