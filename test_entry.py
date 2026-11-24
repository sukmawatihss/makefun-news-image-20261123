import os
import struct

HERE = os.path.dirname(os.path.abspath(__file__))

FRESH_WORDS = [
    "cop31", "hormuz", "kyiv", "albanese", "benghazi", "lisbon",
    "rohingya", "alcaraz", "miley", "fbi", "democrats", "ufo",
    "nepal", "tata steel", "spicejet", "gold", "myanmar", "finland",
    "zverev", "morando", "iowa", "schumer", "modi", "asean",
    "houthi", "patriot", "bahrain", "indonesia", "wellington",
    "antalya", "10.2.0",
]


def main():
    path = os.path.join(HERE, "entry.png")
    size = os.path.getsize(path)
    assert size <= 1048576, "entry.png too large: %d" % size
    with open(path, "rb") as fh:
        head = fh.read(24)
    assert head[:8] == b"\x89PNG\r\n\x1a\n", "not a PNG"
    width, height = struct.unpack(">II", head[16:24])
    assert (width, height) == (1024, 1024), "bad dimensions %dx%d" % (width, height)
    texts = ""
    for name in ("compose.py", "test_entry.py"):
        with open(os.path.join(HERE, name), "r", encoding="utf-8") as fh:
            texts += fh.read().lower() + "\n"
    for word in FRESH_WORDS:
        assert word in texts, "fresh word missing: %s" % word
    print("all checks passed; entry.png is %d bytes at %dx%d" % (size, width, height))


if __name__ == "__main__":
    main()
