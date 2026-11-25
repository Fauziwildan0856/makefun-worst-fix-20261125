"""Emit the worst-fix commit message as entry.txt.

A single commit message for a bug fix that made everything worse is
held in this file. Running the program writes that message to
$MAKEFUN_OUTPUT_DIR/entry.txt and then reads the file back, so the
output is proven to hold exactly the message and nothing else. The
program uses only the Python standard library, which is all the
grader's bare interpreter provides.
"""

import os
import sys

# The kit's gate: one line, 1 to 100 characters, not only whitespace.
LIMIT = 100

COMMIT_MESSAGE = (
    "fix: resolved the crash by deleting the users; "
    "zero crashes reported since"
)


def reject(message):
    print("cannot publish entry: %s" % message, file=sys.stderr)
    return 1


def publish(message):
    if message.strip() != message:
        return reject("the message starts or ends with whitespace")
    if any(sep in message for sep in ("\n", "\r")):
        return reject("the message must be a single line")
    if len(message) < 1 or len(message) > LIMIT:
        return reject("the message must be 1 to %d characters" % LIMIT)
    if not any(char.isalnum() for char in message):
        return reject("the message needs at least one letter or digit")
    if not message.startswith("fix:"):
        return reject("the message must read as a fix commit message")

    target_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not target_dir:
        return reject("MAKEFUN_OUTPUT_DIR is not set")
    os.makedirs(target_dir, exist_ok=True)
    target = os.path.join(target_dir, "entry.txt")
    with open(target, "w", encoding="utf-8") as out:
        out.write(message)
    with open(target, encoding="utf-8") as check:
        if check.read() != message:
            return reject("the file on disk differs from the message")
    print("entry written: %d characters" % len(message))
    return 0


if __name__ == "__main__":
    sys.exit(publish(COMMIT_MESSAGE))
