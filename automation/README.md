# RogueVerse approval publishing

This repository uses a two-stage, approval-first publishing workflow for three
complete content packages per week.

## What one package contains

- Static HTML article and category card
- RSS entry, sitemap, and robots discovery files
- 1080x1920 faceless Remotion video with burned-in captions
- YouTube Shorts metadata
- TikTok caption and creator-inbox upload instructions

Facebook is intentionally disabled until a Facebook Page is supplied.

## Approval flow

1. Copy `content-packages/examples/faceless-package.example.json` into
   `content-packages/drafts/<slug>.json`.
2. Replace the sample copy, artwork, and primary reporting sources.
3. Commit the draft to `main`.
4. In GitHub Actions, run **Prepare content package for approval** and provide
   the draft path.
5. Download and watch the approval artifact, then review the generated article
   in the pull request.
6. Merge the pull request to approve the package. Until it is merged, neither
   the article nor social package is published.

The social workflow is additionally locked by the repository variable
`SOCIAL_PUBLISH_ENABLED`. Leave it unset or set to `false` during setup.

## GitHub secrets

Store these in repository or `social-production` environment secrets. Never
put them in package JSON, commits, issues, or chat.

### YouTube

- `YOUTUBE_CLIENT_ID`
- `YOUTUBE_CLIENT_SECRET`
- `YOUTUBE_REFRESH_TOKEN` with the `youtube.upload` scope

YouTube uploads default to private. Set a package's `publish_at` or change its
YouTube metadata only after verifying the channel's desired schedule.

### TikTok

- `TIKTOK_CLIENT_KEY`
- `TIKTOK_CLIENT_SECRET`
- `TIKTOK_REFRESH_TOKEN` authorized for `video.upload`

TikTok uses the creator-inbox upload endpoint. After an approved video is sent,
the account owner completes the final editing/posting flow in TikTok. Direct
public posting remains disabled until the TikTok app passes the required audit
and its creator-consent UX is implemented.

## Local validation

Python is the only local requirement for package validation:

```text
python automation/build_package.py --package content-packages/drafts/<slug>.json --check
```

The full video render runs on GitHub's runner with Node.js and Remotion. Local
Node.js, FFmpeg, Docker, and n8n are not required.

Videos are silent by default so the workflow never adds unlicensed music.
Set `video.audio` to a repository-relative licensed voiceover or music file to
mix it into the render. TikTok creator-inbox uploads can also receive their
final sound selection inside TikTok before posting.

## Safety boundaries

- Only a merged file under `content-packages/approved/` can trigger social work.
- Social work is skipped unless `SOCIAL_PUBLISH_ENABLED=true`.
- The example package cannot publish by itself.
- Reported articles require at least one HTTPS source.
- Package markup rejects scripts, embedded frames, event handlers, and
  `javascript:` URLs.
- Generated MP4 files and OAuth material are excluded from Git.
