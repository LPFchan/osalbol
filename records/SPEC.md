# 오살볼 Spec

- Project: 오살볼 (osalbol)
- Canonical repo: `LPFchan/osalbol` (public)
- Project id: `osalbol`
- Site: https://osalbol.com
- Operator: LPFchan
- Last updated: 2026-11-18

## Thesis

오살볼 is short for **오래 살고 볼 일이다**: live long enough and you get to see it.

The site is a static page that collects things that once felt like they would
never happen, and then happened. Each entry is a small piece of evidence that
the future can surprise you in a good way. The page is an encouragement: even
on days when you want to give up, keep walking, because unexpected and
wonderful things turn up in your footsteps.

## Invariants

- One static page. No accounts, no tracking, no backend.
- Every entry names when it happened, and links a public source when one exists.
- Every entry records when it was added to the page (`data-added` on its `<li>`, KST). The five most recently added carry a NEW tag.
- Only public events. Never quote private conversations or name private people.
- Korean first.

## Non-goals

- A news feed or a complete archive.
- A pile of sad news. Negative entries (오살볼(negative)) are rare and get a gray label instead of the accent color.
