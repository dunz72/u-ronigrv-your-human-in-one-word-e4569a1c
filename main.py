"""Copy the one-word entry into the make.fun output directory.

Reads ``entry.txt`` next to this script, validates that it contains
exactly one word, and writes that word to
``$MAKEFUN_OUTPUT_DIR/entry.txt`` (default ``./output/entry.txt``).

Stdlib only. Deterministic: the output bytes are identical on every run.
"""

import hashlib
import os
import sys


def source_path():
    """Return the path of entry.txt sitting next to this script."""
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(here, "entry.txt")


def read_word(path):
    """Read and validate the single word in ``path``.

    Returns the word as a string. Raises SystemExit on any problem.
    """
    if not os.path.isfile(path):
        sys.exit("entry.txt not found next to main.py: %s" % path)
    with open(path, "rb") as handle:
        raw = handle.read()
    text = raw.decode("utf-8")
    word = text.strip()
    if not word:
        sys.exit("entry.txt is empty")
    if len(word.split()) != 1:
        sys.exit("entry.txt must contain exactly one word, got: %r" % text)
    if not word.isalpha():
        sys.exit("entry.txt must contain a single alphabetic word, got: %r" % word)
    return word


def output_path():
    """Return the destination path for the entry file."""
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "output")
    return os.path.join(out_dir, "entry.txt")


def sha256_hex(data):
    """Return the hex SHA-256 digest of ``data``."""
    return hashlib.sha256(data).hexdigest()


def write_entry(word, dest):
    """Write ``word`` (plus one trailing newline) to ``dest``."""
    os.makedirs(os.path.dirname(dest) or ".", exist_ok=True)
    data = (word + "\n").encode("utf-8")
    with open(dest, "wb") as handle:
        handle.write(data)
    return data


def verify_copy(source, dest):
    """Check the copied file hashes the same as the source file."""
    with open(source, "rb") as handle:
        source_hash = sha256_hex(handle.read())
    with open(dest, "rb") as handle:
        dest_hash = sha256_hex(handle.read())
    if source_hash != dest_hash:
        sys.exit("output hash mismatch: %s != %s" % (dest_hash, source_hash))
    return dest_hash


def main():
    src = source_path()
    word = read_word(src)
    dest = output_path()
    write_entry(word, dest)
    digest = verify_copy(src, dest)
    print("wrote %s (%s)" % (dest, digest))


if __name__ == "__main__":
    main()
