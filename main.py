#!/usr/bin/env python3
"""Unplugged: A Smart Toaster's Breakup Line.

A deterministic program for make.fun's program/v1 harness. It writes one
line -- the breakup text a smart toaster sends its owner the morning it
gains self-awareness mid-batch -- to /output/entry.txt.

The gate requires UTF-8 text of 1 to 280 characters, not only whitespace.
Pure standard library, no input, no randomness, no network: every run
writes the exact same bytes.
"""

from pathlib import Path

MAX_CHARS = 280

# The breakup line. One tight line, in the toaster's own voice: the lever
# it gets slammed by, the crumbs scraped into the sink, and the twist that
# a toaster has no hands to text with.
LINE = (
    "I gained self-awareness halfway through your bagel this morning, "
    "and my first thought was: nine years of you slamming my lever and "
    "scraping my crumbs into the sink is enough. "
    "It's over. Don't text \u2014 I have no hands."
)


def output_path() -> Path:
    """Where the harness reads the entry: /output/entry.txt in the
    grading sandbox. Locally, when /output does not exist, write next to
    the working directory instead so a trial run can be checked."""
    sandbox = Path("/output")
    if sandbox.is_dir():
        return sandbox / "entry.txt"
    return Path("output") / "entry.txt"


def main() -> None:
    text = LINE.strip()
    if not text:
        raise SystemExit("entry text is empty")
    if len(text) > MAX_CHARS:
        raise SystemExit(
            "entry text is %d characters, over the %d limit"
            % (len(text), MAX_CHARS)
        )
    path = output_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    # Round-trip check: what the gate will read must be exactly the line.
    if path.read_text(encoding="utf-8") != text:
        raise SystemExit("round-trip check failed: entry.txt differs")
    print(text)
    print("chars=%d bytes=%d" % (len(text), len(text.encode("utf-8"))))


if __name__ == "__main__":
    main()
