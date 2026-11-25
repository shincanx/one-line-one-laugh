"""One Line, One Laugh -- make.fun entry.

Writes a single funny line of text (at most 200 characters) to entry.txt
in the output directory. Deterministic, no network, no randomness, no
input.

The joke: "My cat pushed my glass off the table, then stared at me like
gravity owed him money."
A concrete image (cat, glass, table) with the twist landing on the last
words: the cat doesn't look guilty, it stares like gravity is the debtor.
"Pushed" beats "knocked" — deliberate, feline, unhurried — and "stared"
beats "looked": the blame is transferred to physics with the confidence
of a creature that has never once paid for anything it broke.
"""

import os

# The entry: one original funny line. 84 characters, under the 200 cap.
JOKE = "My cat pushed my glass off the table, then stared at me like gravity owed him money."


def resolve_out_dir() -> str:
    """Pick the output directory: $MAKEFUN_OUTPUT_DIR, else /output,
    else a local output/ folder if neither is usable."""
    candidates = []
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env_dir:
        candidates.append(env_dir)
    candidates.append("/output")
    candidates.append("output")
    for candidate in candidates:
        try:
            os.makedirs(candidate, exist_ok=True)
            probe = os.path.join(candidate, ".write-test")
            with open(probe, "w", encoding="utf-8") as f:
                f.write("ok")
            os.remove(probe)
            return candidate
        except OSError:
            continue
    raise OSError("no writable output directory found")


def main() -> None:
    if len(JOKE) > 200:
        raise ValueError(f"joke is {len(JOKE)} characters, over the 200 cap")
    if not JOKE.strip():
        raise ValueError("entry must not be only whitespace")
    if "\n" in JOKE or "\r" in JOKE:
        # Craft: a single funny line is a single line -- no hidden second setup.
        raise ValueError("entry must be a single line")
    if not JOKE.endswith("."):
        raise ValueError("entry must end with a full stop, the punchline's landing")

    out_dir = resolve_out_dir()
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(JOKE + "\n")

    # Round-trip check: what landed on disk is exactly the joke.
    with open(path, encoding="utf-8") as f:
        written = f.read().rstrip("\n")
    if written != JOKE:
        raise ValueError("entry.txt does not match the joke")

    print(f"wrote {len(JOKE)} characters to {path}")


if __name__ == "__main__":
    main()
