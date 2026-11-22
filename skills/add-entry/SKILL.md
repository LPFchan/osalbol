---
name: add-entry
description: "Add or edit an entry on osalbol.com (public/index.html), verify facts and mobile layout, update records/STATUS.md, commit with the repo contract, push, and deploy to Cloudflare Workers."
argument-hint: "Event description, date, or source link (or an edit to an existing entry)"
---

# Add Entry

Use this skill whenever adding a new entry to (or editing an existing entry on) [https://osalbol.com](https://osalbol.com).

References:

- [../../records/SPEC.md](../../records/SPEC.md) — product invariants and wait-label rule
- [../../records/STATUS.md](../../records/STATUS.md) — live entry count
- [../../public/index.html](../../public/index.html) — the static page
- [../commit-generator/SKILL.md](../commit-generator/SKILL.md) — required `LOG-*` commit flow
- [../../wrangler.jsonc](../../wrangler.jsonc) — Cloudflare Workers static-asset deploy config
- [scripts/check-entries.py](scripts/check-entries.py) — structural validator for `public/index.html` and `records/STATUS.md`

## Inputs

- An event candidate (from the operator, a GitHub issue, a link, or a suggestion)
- Public source URL(s) and date — research them if the request did not include them

## Procedure

### 1. Sync and check for duplicates

1. Pull the latest `main` (`git fetch origin && git pull --ff-only`), or branch from `origin/main` in a temporary worktree per `parallel-tree` when other agents may be active.
2. Search `public/index.html` to confirm the event is not already listed.

### 2. Verify facts, date, and source

1. **Public events only.** Never quote private conversations or name private individuals.
2. **Verify against a primary public source** (official newsroom, press release, blog, YouTube upload, or official social post preferred; credible news coverage when no official page exists). Do not rely solely on a secondary tweet or a press headline's year count.
3. **Pick `<time datetime="...">`:**
   - Format: `YYYY-MM-DD`, or `YYYY-MM` only when no exact day exists. Keep the `datetime` attribute and visible text identical.
   - Use the date the event **actually happens or happened** (release, broadcast, opening, award, ruling, retirement) — not the tweet or announcement date, unless the announcement itself is the milestone or no event date is announced yet. Confirmed future dates are allowed.
   - Use the event's local date (e.g., US local date for US rulings, Japanese premiere date when the Japan release is the milestone, Korean release date for Korean milestones).
4. **Format the source link:**
   - Always use `출처` as the link text: `<a href="...">출처</a>`.
   - Escape `&` as `&amp;` inside `href` attributes (e.g., `bbs_num=13525&amp;tb=...`).
   - Omit the link (and the ` · ` separator) only if genuinely no public source exists.

### 3. Draft title, wait label, tags, and tone

1. **Title (`<h2>`):**
   - Korean first, short, matter-of-fact headline — no filler or clickbait.
   - Wrap work, show, film, game, album, song, and product titles in single angle brackets `〈...〉` (`U+3008` / `U+3009`, not `< >` or `《 》`).
   - Use curly quotes `“...”` for direct quotations and spaced em-dash ` — ` to pair a headline with a specific name or lineup.
   - Use the official or natural proper-noun form (`Underscores`, `EDP 2026 -KOREA-`, `Synthesizer V`, `Apple Pay`, `오아시스`, `아이폰`) and omit redundant descriptors (`TAK`, not `K-pop 작곡가 TAK`; `일본 예능`, not `일본 예능 프로그램`).
   - `body` uses `word-break: keep-all`; insert `&nbsp;` inside short two-word names or phrases if mobile wraps awkwardly (e.g., `〈Do&nbsp;It〉`, `모델&nbsp;Y`, `1위&nbsp;차지`).

2. **Wait label (`<span class="wait">`):**
   - Use a bare `N년 만`, counted from when people started waiting to the entry's `<time>` date. Check the math yourself — press reports sometimes count to a future broadcast/release year instead of the dated milestone.
   - Do **not** prefix what was counted from (`발표 N년 만`, `라이트닝 도입 N년 만`, etc.). Add a prefix only when the bare number would actively mislead, and explain why in the commit's `rationale:`.
   - Omit `<span class="wait">` (and ` · `) entirely when there is no clear starting year people waited from.

3. **Categories (`data-tags`):**
   - Space-separated list of one or more exact tokens from the 6 `<nav>` categories:
     `테크` `음악` `영상` `게임` `서브컬쳐` `사회`
   - Watch the spelling of `서브컬쳐` (`쳐`, not `처`). Do not invent new tags; the filter script matches these 6 strings strictly.

4. **Added timestamp (`data-added`):**
   - Set to the current KST time formatted `YYYY-MM-DDTHH:MM`:
     ```sh
     TZ=Asia/Seoul date '+%Y-%m-%dT%H:%M'
     ```
   - Never add `<span class="new">NEW</span>` manually; the inline script tags the five newest `data-added` entries automatically.

5. **Negative entries (`class="neg"`):**
   - Rare (`오살볼(negative)` only). Add `class="neg"` on `<li>` so `.wait` renders in muted gray instead of the accent color. Leave `class` off for normal entries.

### 4. Edit `public/index.html` and `records/STATUS.md`

1. Insert the new `<li>` into `<ol>` in **strict reverse chronological order** by `<time datetime="...">` (newest on top). A `YYYY-MM` entry sits after exact dates in that same month and before earlier months.
2. Match the exact 6-line indentation shape:

   Normal entry with wait label:
   ```html
       <li data-tags="영상 음악" data-added="2026-11-20T22:17">
         <time datetime="2026-12-01">2026-12-01</time>
         <div>
           <h2>〈슈퍼스타K〉 부활</h2>
           <p><span class="wait">10년 만</span> · <a href="https://www.youtube.com/watch?v=48f1iMjhIW8">출처</a></p>
         </div>
       </li>
   ```

   Without wait label:
   ```html
       <li data-tags="음악 게임" data-added="2026-11-19T00:26">
         <time datetime="2026-11-16">2026-11-16</time>
         <div>
           <h2>Underscores 〈Music〉 그래미 노미네이트, 〈Do&nbsp;It〉 GTA 6 수록</h2>
           <p><a href="https://www.grammy.com/news/2027-grammys-full-nominations-full-winners-nominees-list/">출처</a></p>
         </div>
       </li>
   ```

   Negative entry:
   ```html
       <li class="neg" data-tags="사회" data-added="2026-11-18T19:05">
         <time datetime="2027-03-31">2027-03-31</time>
         <div>
           <h2>JR 동일본의 Suica 마스코트 펭귄 은퇴</h2>
           <p><span class="wait">26년 만</span> · <a href="https://www.sankei.com/article/20261118-CHFHVM67NNLTJM2RI6GB2ATOY4/">출처</a></p>
         </div>
       </li>
   ```

3. When adding or removing entries, update the entry count (`with N entries`) in `records/STATUS.md` so it matches `public/index.html`. (Pure wording edits to an existing entry do not change the count.)

### 5. Run the structural check

```sh
python3 skills/add-entry/scripts/check-entries.py
```

Fix any reported ordering, tag, timestamp, escaping, or `STATUS.md` count mismatch before moving on.

### 6. Visual check with the operator

Unless the operator explicitly waived visual review:

1. Serve `public/` locally (e.g., `python3 -m http.server 0 --directory public`) and capture a **mobile viewport (`~390px` wide)** screenshot showing the new or edited entry in context.
2. Check date rendering, title line wrapping, wait label color/text, `NEW` badge, and category chip counts. If a short `〈...〉` title wraps awkwardly, adjust with `&nbsp;` or wording and re-capture.
3. Attach the screenshot in chat and wait for operator approval before committing and deploying.

### 7. Commit and push

Follow [../commit-generator/SKILL.md](../commit-generator/SKILL.md) — never use `git commit -m`.

1. Stage `public/index.html` (and `records/STATUS.md` if the count changed).
2. Generate a fresh commit message skeleton, always passing `--project osalbol` (important in temporary worktrees, where the script defaults `--project` to the directory basename):
   ```sh
   sh scripts/new-commit-message.sh --subject "Add ..." --agent <agent-id> --project osalbol
   ```
3. Fill in the `TODO` bullets:
   - `changes:` — added/edited entry (title, date, wait label or `no wait label`, tags, negative if applicable) and `STATUS: entry count N` when changed
   - `rationale:` — source of suggestion, why this date and wait baseline were chosen, and why any prefixed wait label was needed
   - `checks:` — primary sources verified, `check-entries.py` result, and operator screenshot review
   - If you change the subject or any trailer after generating the skeleton, regenerate it — `prepare-commit-msg` rejects mismatches.
4. Validate and commit:
   ```sh
   sh scripts/check-commit-standards.sh <msg-file>
   git commit -F <msg-file>
   rm <msg-file>
   ```
5. Push directly to `main` (if working in a `parallel-tree` worktree, rebase onto `main`, fast-forward merge in the shared checkout, push, and remove/prune the worktree).

### 8. Deploy to `osalbol.com` and verify live

Pushing to GitHub does **not** auto-deploy `osalbol.com`; Cloudflare Workers Static Assets (`wrangler.jsonc`) must be deployed explicitly.

1. Deploy from the repo root with `CLOUDFLARE_API_TOKEN` set:
   ```sh
   zsh -c 'npx wrangler deploy'
   ```
   - `CLOUDFLARE_API_TOKEN` is exported in `~/.zshenv` on this machine, so non-login `bash` subshells miss it unless run through `zsh` (or after sourcing `~/.zshenv`).
   - On a machine without `CLOUDFLARE_API_TOKEN` in the environment, fetch `CF_MASTER_TOKEN` from Passage (`infra`).
2. Verify live:
   ```sh
   curl -fsS https://osalbol.com | grep -F '<distinctive title snippet>'
   ```
   `-f` fails on non-2xx responses and `grep -F` confirms the new or edited entry is in the served HTML.

## Escalation Triggers

Ask the operator before editing or committing when:

- Multiple plausible dates exist (e.g., announcement vs. release/premiere, global vs. Korea date) and the milestone is unclear.
- The wait-label starting point is ambiguous, or a bare `N년 만` would mislead and seems to need a prefix.
- It is unclear whether a borderline event should be marked `class="neg"` or normal.
- Official English/original vs. Korean title wording is a taste call.
- No verifiable public source backs the claimed date or detail.
