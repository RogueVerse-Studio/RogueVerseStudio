from __future__ import annotations

import argparse
import json
import os
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

from package_tools import PackageError, load_package


TOKEN_URL = "https://oauth2.googleapis.com/token"
UPLOAD_URL = "https://www.googleapis.com/upload/youtube/v3/videos"


def _json_request(url: str, *, data: bytes, headers: dict[str, str]) -> tuple[dict, dict]:
    request = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            return json.loads(response.read().decode("utf-8")), dict(response.headers)
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise PackageError(f"YouTube request failed ({exc.code}): {detail}") from exc


def refresh_access_token() -> str:
    required = ("YOUTUBE_CLIENT_ID", "YOUTUBE_CLIENT_SECRET", "YOUTUBE_REFRESH_TOKEN")
    missing = [name for name in required if not os.environ.get(name)]
    if missing:
        raise PackageError("Missing YouTube secrets: " + ", ".join(missing))
    body = urllib.parse.urlencode(
        {
            "client_id": os.environ["YOUTUBE_CLIENT_ID"],
            "client_secret": os.environ["YOUTUBE_CLIENT_SECRET"],
            "refresh_token": os.environ["YOUTUBE_REFRESH_TOKEN"],
            "grant_type": "refresh_token",
        }
    ).encode()
    payload, _ = _json_request(
        TOKEN_URL,
        data=body,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    token = payload.get("access_token")
    if not token:
        raise PackageError("Google token response did not include access_token")
    return token


def upload(package: dict, video_path: Path) -> dict:
    access_token = refresh_access_token()
    youtube = package["social"]["youtube"]
    metadata = {
        "snippet": {
            "title": youtube["title"],
            "description": youtube["description"],
            "tags": youtube.get("tags", []),
            "categoryId": str(youtube.get("category_id", "24")),
        },
        "status": {
            "privacyStatus": youtube.get("privacy_status", "private"),
            "selfDeclaredMadeForKids": bool(youtube.get("made_for_kids", False)),
            "containsSyntheticMedia": bool(youtube.get("contains_synthetic_media", True)),
        },
    }
    if youtube.get("publish_at"):
        metadata["status"]["privacyStatus"] = "private"
        metadata["status"]["publishAt"] = youtube["publish_at"]
    data = json.dumps(metadata).encode("utf-8")
    query = urllib.parse.urlencode({"part": "snippet,status", "uploadType": "resumable"})
    request = urllib.request.Request(
        f"{UPLOAD_URL}?{query}",
        data=data,
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json; charset=UTF-8",
            "X-Upload-Content-Length": str(video_path.stat().st_size),
            "X-Upload-Content-Type": "video/mp4",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            upload_url = response.headers.get("Location")
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise PackageError(f"YouTube upload initialization failed ({exc.code}): {detail}") from exc
    if not upload_url:
        raise PackageError("YouTube did not return a resumable upload URL")
    upload_request = urllib.request.Request(
        upload_url,
        data=video_path.read_bytes(),
        headers={"Authorization": f"Bearer {access_token}", "Content-Type": "video/mp4"},
        method="PUT",
    )
    try:
        with urllib.request.urlopen(upload_request, timeout=900) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise PackageError(f"YouTube video upload failed ({exc.code}): {detail}") from exc


def main() -> int:
    parser = argparse.ArgumentParser(description="Publish an approved RogueVerse short to YouTube")
    parser.add_argument("--package", required=True, type=Path)
    parser.add_argument("--video", required=True, type=Path)
    parser.add_argument("--publish", action="store_true")
    args = parser.parse_args()
    package = load_package(args.package)
    if not args.video.is_file():
        raise PackageError(f"Video does not exist: {args.video}")
    if not args.publish:
        print(json.dumps({"dry_run": True, "platform": "youtube", "title": package["social"]["youtube"]["title"], "video": str(args.video)}, indent=2))
        return 0
    result = upload(package, args.video)
    print(json.dumps({"platform": "youtube", "video_id": result.get("id"), "status": result.get("status")}, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except PackageError as exc:
        print(exc)
        raise SystemExit(2)
