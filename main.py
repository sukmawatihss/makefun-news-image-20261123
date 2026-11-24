#!/usr/bin/env python3
"""THE WORLD IN A DAY - entry program for news-image-20261123 (akun15).

The entry image is a one-page newspaper front sheet for Monday
23 November 2026: 45 stories from that single day, led by the ICJ ruling
that Myanmar is guilty of genocide against the Rohingya. This program is
the delivery vehicle only - it copies the finished entry.png sitting next
to it into the output directory, after checking the file is intact.

Standard library only (hashlib, os, sys). No imaging libraries: the PNG
bytes are copied verbatim, so two runs always produce identical output.
"""

import hashlib
import os
import sys

EXPECTED_BYTES = 289403
EXPECTED_SHA256 = "5472d510d9a48fda0fd3b3179ab74ae33a3a5c944643ef2a3a7d96e5f0d4e856"
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
HARD_LIMIT = 1048576  # competition ceiling: 1 MiB


def read_entry(path):
    with open(path, "rb") as fh:
        return fh.read()


def check_dimensions(data):
    """Second, independent guard: the IHDR header must say 1024 x 1024.

    Width and height sit at byte offsets 16-19 and 20-23 of a PNG, big
    endian, right after the 8-byte signature and the IHDR chunk header.
    """
    if len(data) < 24:
        raise SystemExit("entry.png too short to hold an IHDR header")
    width = int.from_bytes(data[16:20], "big")
    height = int.from_bytes(data[20:24], "big")
    if (width, height) != (1024, 1024):
        raise SystemExit("entry.png is %dx%d, expected 1024x1024" % (width, height))


def check_entry(data):
    """Refuse to ship anything that is not the exact verified PNG."""
    if not data:
        raise SystemExit("entry.png is empty")
    if data[:8] != PNG_SIGNATURE:
        raise SystemExit("entry.png fails the PNG signature check")
    if len(data) > HARD_LIMIT:
        raise SystemExit("entry.png exceeds the 1 MiB limit: %d bytes" % len(data))
    if len(data) != EXPECTED_BYTES:
        raise SystemExit(
            "entry.png size drifted: %d bytes, expected %d"
            % (len(data), EXPECTED_BYTES)
        )
    digest = hashlib.sha256(data).hexdigest()
    if digest != EXPECTED_SHA256:
        raise SystemExit("entry.png sha256 mismatch: %s" % digest)
    return digest


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    dst = os.path.join(out_dir, "entry.png")

    data = read_entry(src)
    digest = check_entry(data)
    check_dimensions(data)

    os.makedirs(out_dir, exist_ok=True)
    with open(dst, "wb") as fh:
        fh.write(data)

    sys.stderr.write("entry.png copied: %d bytes sha256=%s\n" % (len(data), digest))


if __name__ == "__main__":
    main()
