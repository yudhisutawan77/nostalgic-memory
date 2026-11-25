#!/usr/bin/env python3
"""Make the AI Judge Feel Nostalgic: A Childhood Memory.

Writes one sentence (<=280 chars) recalling a childhood memory to the
entry file the sealed scorer reads. Honors $ENTRY_OUT as a file path,
then $ENTRY_OUT_DIR as a directory (entry.txt inside it), then falls
back to /output/entry.txt.
"""

import os
import sys

MAX_CHARS = 280


def compose_nostalgic_line():
    """Return the entry: one sentence, one concrete childhood memory."""
    fragments = [
        "Every August my grandmother lifted the lid off the rice pot ",
        "with a folded dish towel, and the steam fogged my glasses ",
        "while she pretended not to notice I had already stolen ",
        "the crispy bottom.",
    ]
    return "".join(fragments)


def pick_output_path():
    """Pick the output path from the environment, in priority order."""
    entry_out = os.environ.get("ENTRY_OUT")
    if entry_out:
        return entry_out
    entry_out_dir = os.environ.get("ENTRY_OUT_DIR")
    if entry_out_dir:
        return os.path.join(entry_out_dir, "entry.txt")
    return "/output/entry.txt"


def check_length(text):
    """Reject entries outside the sealed scorer's 1-280 char window."""
    if not isinstance(text, str):
        raise ValueError("entry must be text")
    if not (1 <= len(text) <= MAX_CHARS):
        raise ValueError(
            "entry must be 1-%d characters, got %d" % (MAX_CHARS, len(text))
        )
    return text


def check_content(text):
    """Reject whitespace-only entries and anything not UTF-8."""
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    text.encode("utf-8")
    return text


def validate_entry(text):
    """Run every gate check the sealed scorer applies, in order."""
    return check_content(check_length(text))


def emit_entry(path, text):
    """Write the entry as UTF-8 with no trailing newline."""
    parent = os.path.dirname(os.path.abspath(path))
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(text)
    return path


def main():
    text = validate_entry(compose_nostalgic_line())
    path = emit_entry(pick_output_path(), text)
    sys.stdout.write(text + "\n")
    sys.stdout.write("wrote %d chars to %s\n" % (len(text), path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
