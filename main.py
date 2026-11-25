"""Write the worst-fix commit message to entry.txt.

The program holds one commit message for a bug fix that made everything
worse, writes it to $MAKEFUN_OUTPUT_DIR/entry.txt, and reads the file
back to prove the written text is exactly the message. Only the Python
standard library is used, so the grader's bare interpreter can run it.
"""

import os
import sys

MAX_CHARS = 100

MESSAGE = "fix: resolved the crash by deleting the users; zero crashes reported since"


def fail(reason):
    print("entry rejected: " + reason, file=sys.stderr)
    return 1


def main():
    text = MESSAGE
    if text != text.strip():
        return fail("message must not start or end with whitespace")
    if "\n" in text or "\r" in text:
        return fail("message must be a single line")
    if not 1 <= len(text) <= MAX_CHARS:
        return fail("message must be 1 to %d characters" % MAX_CHARS)
    if not any(ch.isalnum() for ch in text):
        return fail("message must contain a letter or a digit")
    if not text.startswith("fix:"):
        return fail("message must read as a fix commit message")

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        return fail("MAKEFUN_OUTPUT_DIR is not set")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(text)
    with open(path, encoding="utf-8") as handle:
        if handle.read() != text:
            return fail("read-back does not match the message")
    print("wrote %d characters to %s" % (len(text), path))
    return 0


if __name__ == "__main__":
    sys.exit(main())
