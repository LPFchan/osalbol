# 오살볼 Status

## Snapshot

- Last updated: 2026-11-18
- Overall posture: `active`
- Current focus: getting the first page live at osalbol.com
- Highest-priority blocker: osalbol.com nameservers still point at Porkbun
- Next operator decision needed: none

## Current State Summary

The first page is built: one static `public/index.html` with 35 entries,
newest first, and a typewriter title that expands 오살볼 into
오래 살고 볼 일이다. `wrangler.jsonc` serves `public/` as Workers static
assets on `osalbol.com` and `www.osalbol.com`. The Cloudflare zone is still
pending until the registrar switches nameservers to `lina.ns.cloudflare.com`
and `santino.ns.cloudflare.com`.
