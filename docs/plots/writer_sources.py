"""Plot which code answers each writer of each language.

Run from the repository root:

    .venv/bin/python docs/plots/writer_sources.py

With --table it prints the table and writes no image.

It needs matplotlib (`uv pip install matplotlib`). The script calls each
public writer for each language with probe values and records which source
file ran: the language module, the shared Romance engine in util.py, the
generic fallback in __init__.py, or unicode-rbnf (CLDR data). It writes
docs/img/writer_sources.png.
"""
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch

from ovos_number_parser import (pronounce_fraction, pronounce_number,
                                pronounce_ordinal)
import importlib

import ovos_number_parser
from ovos_number_parser import numtag_readers
from ovos_number_parser.numtag_readers import NUMTAG_LANGS

ROOT = Path(ovos_number_parser.__file__).parent
NONE, OWN, ENGINE, GENERIC, RBNF, NUMTAG = range(6)
LABELS = {NUMTAG: "numtag (reading)", OWN: "language module",
          ENGINE: "shared Romance engine", GENERIC: "generic fallback",
          RBNF: "CLDR rules (unicode-rbnf)", NONE: "none"}
COLORS = ["#eeeeee", "#2a9d8f", "#8ab17d", "#e9c46a", "#e76f51", "#457b9d"]

PROBES = {
    "pronounce_number": (pronounce_number, [1, 21, 100, 1234, 1000000]),
    "pronounce_ordinal": (pronounce_ordinal, [1, 2, 21, 100, 1234]),
    "pronounce_fraction": (lambda value, lang: pronounce_fraction(value, lang), ["3/4"]),
}


def sources(call, values, lang):
    """The sources that answered the probe values: a set of source codes."""
    found = set()
    for value in values:
        seen = []

        def trace(frame, event, arg):
            if event == "call":
                seen.append((frame.f_code.co_filename, frame.f_code.co_name))

        sys.setprofile(trace)
        try:
            call(value, lang)
        except (NotImplementedError, ValueError, OverflowError):
            pass
        finally:
            sys.setprofile(None)
        calls = {(Path(name).name, function) for name, function in seen}
        files = {name for name, _ in calls}
        if ("__init__.py", "_pronounce_rbnf") in calls:
            found.add(RBNF)
        elif ("__init__.py", "_pronounce_fraction_generic") in calls:
            found.add(GENERIC)
        elif {("util.py", "pronounce_number"), ("util.py", "pronounce_ordinal"),
              ("util.py", "pronounce_fraction")} & calls:
            found.add(ENGINE)
        elif f"numbers_{lang}.py" in files or lang == "ms" and "numbers_id.py" in files:
            found.add(OWN)
        else:
            found.add(GENERIC)
    return found


def nice_number_source(lang):
    """OWN when a language module defines nice_number_<code>, else NONE."""
    module = importlib.import_module(
        "ovos_number_parser.numbers_" + ("id" if lang == "ms" else lang))
    return OWN if hasattr(module, f"nice_number_{lang}") else NONE


def main():
    langs = sorted(NUMTAG_LANGS)
    columns = ["extract_number", *PROBES, "nice_number"]
    grid = []
    for lang in langs:
        row = [NUMTAG if numtag_readers.routed(lang) else NONE]
        for call, values in PROBES.values():
            row.append(max(sources(call, values, lang)))
        row.append(nice_number_source(lang))
        grid.append(row)

    print("language", *columns, sep="\t")
    for lang, row in zip(langs, grid):
        print(lang, *(LABELS[value] for value in row), sep="\t")
    if "--table" in sys.argv:
        return

    fig, axis = plt.subplots(figsize=(5.4, 11))
    axis.imshow(grid, cmap=ListedColormap(COLORS), vmin=0, vmax=5, aspect="auto")
    axis.set_xticks(range(len(columns)), columns, rotation=30, ha="right")
    axis.set_yticks(range(len(langs)), langs)
    axis.set_xticks([x - 0.5 for x in range(1, len(columns))], minor=True)
    axis.set_yticks([y - 0.5 for y in range(1, len(langs))], minor=True)
    axis.grid(which="minor", color="white", linewidth=1.5)
    axis.tick_params(which="minor", length=0)
    axis.set_title("Source of each writer, per language")
    axis.legend(handles=[Patch(color=COLORS[key], label=LABELS[key]) for key in sorted(LABELS, reverse=True)],
                loc="upper center", bbox_to_anchor=(0.5, -0.12), frameon=False)
    out = Path(__file__).resolve().parent.parent / "img" / "writer_sources.png"
    fig.savefig(out, dpi=110, bbox_inches="tight")


if __name__ == "__main__":
    main()
