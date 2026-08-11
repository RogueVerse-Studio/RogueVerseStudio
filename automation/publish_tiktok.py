from __future__ import annotations

import argparse
import json
import os
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

from package_tools import PackageError, load_package


TOKEN_URL = "https://open.tiktokapis.com/v2/oauth/token/"
INIT_URL = "https://open.tiktokapis.com/v2/post/publish/inbox/video/init/"
MAX_CHUNK = 64 * 1024 * 1024


def _post_form(url: str, values: dict[str, str]) -> dict:
    request = urllib.request.Request(
        url,
        data=urllib.parse.urlencode(values).encode(),
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        raise PackageError(f"TikTok token request failed ({exc.code}): {exc.read().decode('utf-8', errors='replace')}") from exc


def refresh_access_token() -> str:
    if os.environ.get("TIKTOK_ACCESS_TOKEN"):
        return os.environ["TIKTOK_ACCESS_TOKEN"]
    required = ("TIKTOK_CLIENT_KEY", "TIKTOK_CLIENT_SECRET", "TIKTOK_REFRESH_TOKEN")
    missing = [name for name in required if not os.environ.get(name)]
    if missing:
        raise PackageError("Missing TikTok secrets: " + ", ".join(missing))
    payload = _post_form(
        TOKEN_URL,
        {
            "client_key": os.environ["TIKTOK_CLIENT_KEY"],
            "client_secret": os.environ["TIKTOK_CLIENT_SECRET"],
            "grant_type": "refresh_token",
            "refresh_token": os.environ["TIKTOK_REFRESH_TOKEN"],
        },
    )
    token = payload.get("access_token")
    if not token:
        raise PackageError(f"TikTok token response did not include access_token: {payload}")
    return token


def upload_to_inbox(video_path: Path) -> dict:
    token = refresh_access_token()
    video_size = video_path.stat().st_size
    if video_size > MAX_CHUNK:
        raise PackageError("TikTok v1 uploader requires an MP4 no larger than 64 MB; render with a higher CRF")
    chunk_size = video_size
    total_chunks = 1
    body = json.dumps(
        {
            "source_info": {
                "source": "FILE_UPLOAD",
                "video_size": video_size,
                "chunk_size": chunk_size,
                "total_chunk_count": total_chunks,
            }
        }
    ).encode()
    request = urllib.request.Request(
        INIT_URL,
        data=body,
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json; charset=UTF-8"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        raise PackageError(f"TikTok upload initialization failed ({exc.code}): {exc.read().decode('utf-8', errors='replace')}") from exc
    if payload.get("error", {}).get("code") not in (None, "ok"):
        raise PackageError(f"TikTok rejected the upload initialization: {payload}")
    upload_url = payload.get("data", {}).get("upload_url")
    publish_id = payload.get("data", {}).get("publish_id")
    if not upload_url or not publish_id:
        raise PackageError(f"TikTok did not return upload_url and publish_id: {payload}")

    with video_path.open("rb") as handle:
        offset = 0
        while offset < video_size:
            chunk = handle.read(chunk_size)
            end = offset + len(chunk) - 1
            upload_request = urllib.request.Request(
                upload_url,
                data=chunk,
                headers={
                    "Content-Type": "video/mp4",
                    "Content-Length": str(len(chunk)),
                    "Content-Range": f"bytes {offset}-{end}/{video_size}",
                },
                method="PUT",
            )
            try:
                with urllib.request.urlopen(upload_request, timeout=300):
                    pass
            except urllib.error.HTTPError as exc:
                raise PackageError(f"TikTok media upload failed ({exc.code}): {exc.read().decode('utf-8', errors='replace')}") from exc
            offset = end + 1
    return {"publish_id": publish_id, "next_step": "Open TikTok inbox and complete the creator posting flow."}


def main() -> int:
    parser = argparse.ArgumentParser(description="Send an approved RogueVerse short to the TikTok creator inbox")
    parser.add_argument("--package", required=True, type=Path)
    parser.add_argument("--video", required=True, type=Path)
    parser.add_argument("--publish", action="store_true")
    args = parser.parse_args()
    package = load_package(args.package)
    if not args.video.is_file():
        raise PackageError(f"Video does not exist: {args.video}")
    if not args.publish:
        print(json.dumps({"dry_run": True, "platform": "tiktok_inbox", "caption": package["social"]["tiktok"]["caption"], "video": str(args.video)}, indent=2))
        return 0
    print(json.dumps(upload_to_inbox(args.video), indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except PackageError as exc:
        print(exc)
        raise SystemExit(2)
