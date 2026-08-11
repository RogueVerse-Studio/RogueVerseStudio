from __future__ import annotations

import html
import json
import re
from datetime import datetime
from pathlib import Path, PurePosixPath
from typing import Any
from urllib.parse import urlparse


SITE_URL = "https://rogueversemedia.com"
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
UNSAFE_HTML_RE = re.compile(
    r"<(?:script|iframe|object|embed)\b|\bon[a-z]+\s*=|javascript\s*:", re.I
)

SECTION_CONFIG = {
    "old-man-otaku": {
        "index": "old-man-otaku/index.html",
        "label": "AniManga Updates",
        "brand": "OLD MAN OTAKU",
        "card_class": "section-card section-card--image",
    },
    "news/movies": {
        "index": "news/movies/index.html",
        "label": "Movies & TV",
        "brand": "ROGUEVERSE MOVIES",
        "card_class": "story-card",
    },
    "future": {
        "index": "future/index.html",
        "label": "Future",
        "brand": "ROGUEVERSE FUTURE",
        "card_class": "section-card section-card--image",
    },
}


class PackageError(ValueError):
    pass


def load_package(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise PackageError(f"Cannot read package {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise PackageError("Package root must be a JSON object")
    return data


def _required_text(container: dict[str, Any], key: str, errors: list[str]) -> str:
    value = container.get(key)
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{key} must be a non-empty string")
        return ""
    return value.strip()


def _valid_repo_path(value: str) -> bool:
    if not value or "\\" in value:
        return False
    parsed = urlparse(value)
    path = PurePosixPath(value)
    return not parsed.scheme and not path.is_absolute() and ".." not in path.parts


def _valid_https_url(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme == "https" and bool(parsed.netloc)


def validate_package(data: dict[str, Any], site_root: Path) -> list[str]:
    errors: list[str] = []
    if data.get("version") != 1:
        errors.append("version must be 1")

    slug = _required_text(data, "slug", errors)
    if slug and not SLUG_RE.fullmatch(slug):
        errors.append("slug must contain lowercase letters, numbers, and single hyphens")

    section = _required_text(data, "section", errors)
    if section and section not in SECTION_CONFIG:
        errors.append(f"section must be one of: {', '.join(SECTION_CONFIG)}")

    for key in ("title", "description", "kicker", "dek"):
        _required_text(data, key, errors)

    publish_at = _required_text(data, "publish_at", errors)
    if publish_at:
        try:
            datetime.fromisoformat(publish_at.replace("Z", "+00:00"))
        except ValueError:
            errors.append("publish_at must be an ISO-8601 date-time")

    hero = data.get("hero")
    if not isinstance(hero, dict):
        errors.append("hero must be an object")
    else:
        hero_src = _required_text(hero, "src", errors)
        _required_text(hero, "alt", errors)
        if hero_src and not _valid_repo_path(hero_src):
            errors.append("hero.src must be a safe repository-relative path")
        elif hero_src and not (site_root / PurePosixPath(hero_src)).is_file():
            errors.append(f"hero.src does not exist: {hero_src}")

    article = data.get("article")
    if not isinstance(article, dict):
        errors.append("article must be an object")
    else:
        blocks = article.get("blocks")
        if not isinstance(blocks, list) or not blocks:
            errors.append("article.blocks must be a non-empty array")
        else:
            allowed_types = {"paragraph", "heading", "blockquote", "list"}
            for index, block in enumerate(blocks):
                if not isinstance(block, dict) or block.get("type") not in allowed_types:
                    errors.append(f"article.blocks[{index}] has an unsupported type")
                    continue
                content = block.get("html")
                if not isinstance(content, str) or not content.strip():
                    errors.append(f"article.blocks[{index}].html must be non-empty")
                elif UNSAFE_HTML_RE.search(content):
                    errors.append(f"article.blocks[{index}].html contains unsafe markup")

        sources = article.get("sources", [])
        if article.get("kind") != "original" and not sources:
            errors.append("reported articles require at least one source")
        if not isinstance(sources, list):
            errors.append("article.sources must be an array")
        else:
            for index, source in enumerate(sources):
                if not isinstance(source, dict):
                    errors.append(f"article.sources[{index}] must be an object")
                    continue
                _required_text(source, "label", errors)
                url = _required_text(source, "url", errors)
                if url and not _valid_https_url(url):
                    errors.append(f"article.sources[{index}].url must be HTTPS")

    video = data.get("video")
    if not isinstance(video, dict):
        errors.append("video must be an object")
    else:
        duration = video.get("duration_seconds")
        if not isinstance(duration, int) or not 25 <= duration <= 60:
            errors.append("video.duration_seconds must be an integer from 25 to 60")
        audio = video.get("audio")
        if audio:
            if not isinstance(audio, str) or not _valid_repo_path(audio):
                errors.append("video.audio must be a safe repository-relative path")
            elif not (site_root / PurePosixPath(audio)).is_file():
                errors.append(f"video.audio does not exist: {audio}")
        scenes = video.get("scenes")
        if not isinstance(scenes, list) or not 3 <= len(scenes) <= 8:
            errors.append("video.scenes must contain 3 to 8 scenes")
        else:
            for index, scene in enumerate(scenes):
                if not isinstance(scene, dict):
                    errors.append(f"video.scenes[{index}] must be an object")
                    continue
                _required_text(scene, "headline", errors)
                _required_text(scene, "body", errors)
                image = scene.get("image")
                if image:
                    if not isinstance(image, str) or not _valid_repo_path(image):
                        errors.append(f"video.scenes[{index}].image must be repository-relative")
                    elif not (site_root / PurePosixPath(image)).is_file():
                        errors.append(f"video.scenes[{index}].image does not exist: {image}")

    social = data.get("social")
    if not isinstance(social, dict):
        errors.append("social must be an object")
    else:
        youtube = social.get("youtube")
        tiktok = social.get("tiktok")
        if not isinstance(youtube, dict) or not isinstance(tiktok, dict):
            errors.append("social.youtube and social.tiktok must be objects")
        else:
            _required_text(youtube, "title", errors)
            _required_text(youtube, "description", errors)
            _required_text(tiktok, "caption", errors)

    return errors


def require_valid_package(data: dict[str, Any], site_root: Path) -> None:
    errors = validate_package(data, site_root)
    if errors:
        raise PackageError("Invalid content package:\n- " + "\n- ".join(errors))


def strip_html(value: str) -> str:
    return html.unescape(re.sub(r"<[^>]+>", "", value)).strip()


def make_captions(scenes: list[dict[str, Any]], duration_seconds: int) -> list[dict[str, Any]]:
    scene_ms = duration_seconds * 1000 / len(scenes)
    captions: list[dict[str, Any]] = []
    for index, scene in enumerate(scenes):
        text = f" {scene['headline']}. {scene['body']}"
        captions.append(
            {
                "text": text,
                "startMs": round(index * scene_ms),
                "endMs": round((index + 1) * scene_ms),
                "timestampMs": round(index * scene_ms),
                "confidence": 1,
            }
        )
    return captions
