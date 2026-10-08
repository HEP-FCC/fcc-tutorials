#!/usr/bin/env python3
"""Fail when a page converted by jupytext contains no code cells.

Executing such a notebook succeeds trivially, so its test would pass without
running anything from the page. This happens, for example, when a ``:::`` line
(a MyST directive) makes jupytext read the page as pandoc markdown, which turns
ordinary code fences into markdown rather than code cells.
"""

import json
import sys


def main(path):
    with open(path) as stream:
        cells = json.load(stream)["cells"]
    code = sum(cell["cell_type"] == "code" for cell in cells)
    print(f"{path}: {len(cells)} cells, {code} code")
    if not code:
        print("FAILED: notebook has no code cells; the page test would execute nothing",
              file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
