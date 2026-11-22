#!/usr/bin/env python3
"""Validate public/index.html entries and records/STATUS.md entry count."""

from pathlib import Path
import re
import sys

ALLOWED_TAGS = {"테크", "음악", "영상", "게임", "서브컬쳐", "사회"}


def main() -> int:
    root = Path(__file__).resolve().parents[3]
    html = (root / "public/index.html").read_text(encoding="utf-8")
    status = (root / "records/STATUS.md").read_text(encoding="utf-8")

    ol_match = re.search(r"<ol>(.*?)</ol>", html, re.S)
    if not ol_match:
        print("ERROR: <ol>...</ol> not found in public/index.html", file=sys.stderr)
        return 1

    items = re.findall(r"<li([^>]*)>(.*?)</li>", ol_match.group(1), re.S)
    errors: list[str] = []
    dates: list[tuple[str, str, int]] = []

    for idx, (attrs, body) in enumerate(items, 1):
        m_tags = re.search(r'data-tags="([^"]+)"', attrs)
        if not m_tags:
            errors.append(f"#{idx}: missing data-tags")
        else:
            tags = m_tags.group(1).split()
            invalid = [t for t in tags if t not in ALLOWED_TAGS]
            if not tags or invalid:
                errors.append(f"#{idx}: invalid data-tags {m_tags.group(1)!r}")

        m_added = re.search(r'data-added="([^"]+)"', attrs)
        if not m_added or not re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}", m_added.group(1)):
            errors.append(f"#{idx}: invalid data-added {m_added and m_added.group(1)!r}")

        m_time = re.search(r'<time datetime="([^"]+)">([^<]+)</time>', body)
        if not m_time:
            errors.append(f"#{idx}: missing <time datetime=...>")
        elif m_time.group(1) != m_time.group(2):
            errors.append(f"#{idx}: <time> attr {m_time.group(1)!r} != text {m_time.group(2)!r}")
        else:
            dt = m_time.group(1)
            if not re.fullmatch(r"\d{4}-\d{2}(-\d{2})?", dt):
                errors.append(f"#{idx}: invalid datetime {dt!r}")
            else:
                # YYYY-MM sorts after exact days in the same month, before earlier months.
                key = dt if len(dt) == 10 else f"{dt}-00"
                dates.append((key, dt, idx))

        if 'class="new"' in body:
            errors.append(f"#{idx}: do not hand-add <span class=\"new\">; the script adds it")

        for href in re.findall(r'href="([^"]+)"', body):
            if re.search(r"&(?!amp;|lt;|gt;|quot;|#\d+;|#x[0-9a-fA-F]+;)", href):
                errors.append(f"#{idx}: unescaped '&' in href {href!r}")

    for (k1, d1, i1), (k2, d2, i2) in zip(dates, dates[1:]):
        if k1 < k2:
            errors.append(f"order: #{i1} ({d1}) appears before newer #{i2} ({d2})")

    m_cnt = re.search(r"with (\d+) entries", status)
    if not m_cnt:
        errors.append("records/STATUS.md: could not find 'with N entries'")
    elif int(m_cnt.group(1)) != len(items):
        errors.append(f"records/STATUS.md count ({m_cnt.group(1)}) != HTML entry count ({len(items)})")

    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1

    print(f"OK: {len(items)} entries verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
