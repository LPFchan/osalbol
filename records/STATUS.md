# 오살볼 Status

## Snapshot

- Last updated: 2026-11-18
- Overall posture: `active`
- Current focus: adding entries
- Highest-priority blocker: none
- Next operator decision needed: none

## Current State Summary

The first page is built: one static `public/index.html` with 71 entries,
newest first, and a typewriter title that expands 오살볼 into
오래 살고 볼 일이다. Each entry carries its added time, and a small script
tags the five most recently added as NEW. A sticky chip bar above the
list filters entries by category (테크, 음악, 영상, 게임, 서브컬쳐, 사회); an
entry can sit in several. `wrangler.jsonc` serves `public/` as Workers static
assets on `osalbol.com` and `www.osalbol.com`. The Cloudflare zone is active
and the site is live at `osalbol.com` and `www.osalbol.com`.
