from __future__ import annotations

import argparse
import subprocess
from pathlib import Path, PurePosixPath

SITE_URL = "https://rogueversemedia.com"
ARTICLE_ROOTS = {"old-man-otaku", "news", "community"}


def changed_files(base: str, head: str) -> list[str]:
    result = subprocess.run(
        ["git", "diff", "--name-only", f"{base}...{head}"],
        check=True,
        capture_output=True,
        text=True,
    )
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def article_url_for(path: str) -> str | None:
    p = PurePosixPath(path)
    if p.name != "index.html" or len(p.parts) < 3:
        return None
    if p.parts[0] not in ARTICLE_ROOTS:
        return None
    parent = p.parent.as_posix()
    return f"{SITE_URL}/{parent}/"


def main() -> int:
    parser = argparse.ArgumentParser(description="Ensure changed article pages are present in RogueVerse discovery files.")
    parser.add_argument("--base", required=True)
    parser.add_argument("--head", default="HEAD")
    parser.add_argument("--site-root", default=".")
    args = parser.parse_args()

    root = Path(args.site_root)
    feed = (root / "feed.xml").read_text(encoding="utf-8")
    sitemap = (root / "sitemap.xml").read_text(encoding="utf-8")

    urls = sorted({url for path in changed_files(args.base, args.head) if (url := article_url_for(path))})
    if not urls:
        print("No changed article pages require discovery validation.")
        return 0

    failures: list[str] = []
    for url in urls:
        if url not in sitemap:
            failures.append(f"Missing from sitemap.xml: {url}")
        if url not in feed:
            failures.append(f"Missing from feed.xml: {url}")

    if failures:
        print("Discovery validation failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print(f"Discovery validation passed for {len(urls)} changed article page(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
