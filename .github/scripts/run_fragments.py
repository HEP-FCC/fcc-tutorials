#!/usr/bin/env python3
"""Run tagged shell fragments of a tutorial page exactly as written, then check outputs.

Mark each fence to run with an HTML comment on the line before it (invisible in
the rendered page):

    <!-- ci-fragment: pythia8 -->
    ```bash
    k4run pythia.py -n 500 ...
    ```

All fragments with the same tag run, in page order, in ONE fresh bash shell inside
an empty directory, so `cd` and variables carry over as they would for a reader.
Afterwards every `--validate FILE:EVENTS` output is checked with key4hep-validate.
"""

import argparse
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

MARKER = re.compile(r"^\s*<!--\s*ci-fragment:\s*([\w.-]+)\s*-->\s*$")
FENCE = re.compile(r"^\s*```\s*(bash|sh|shell)?\s*$")


def extract(page, tag):
    lines = page.read_text().splitlines()
    fragments = []
    for number, line in enumerate(lines):
        match = MARKER.match(line)
        if not match or match.group(1) != tag:
            continue
        opening = lines[number + 1] if number + 1 < len(lines) else ""
        if not FENCE.match(opening) or not FENCE.match(opening).group(1):
            sys.exit(f"{page}:{number + 1}: ci-fragment marker must precede a ```bash fence")
        body = []
        for inner in lines[number + 2 :]:
            if FENCE.match(inner):
                break
            body.append(inner)
        else:
            sys.exit(f"{page}:{number + 2}: unterminated fence")
        fragments.append((number + 3, "\n".join(body)))
    if not fragments:
        # Never pass vacuously: a renamed tag or reformatted page must fail loudly.
        sys.exit(f"No fragments tagged {tag!r} in {page}")
    return fragments


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("page", type=Path)
    parser.add_argument("tag")
    parser.add_argument("--validate", action="append", default=[], metavar="FILE:EVENTS")
    parser.add_argument("--print", action="store_true", help="Print the script and exit")
    args = parser.parse_args()
    page = args.page.resolve()
    script = ["set -euo pipefail"]
    for line, body in extract(page, args.tag):
        script += [f"echo '+++ {page.name}:{line}' >&2", body]
    script = "\n".join(script) + "\n"
    if args.print:
        print(script, end="")
        return 0
    with tempfile.TemporaryDirectory(prefix=f"fragments-{args.tag}-") as work:
        work = Path(work)
        (work / "fragments.sh").write_text(script)
        status = subprocess.run(["bash", "fragments.sh"], cwd=work).returncode
        if status:
            print(
                f"FAILED: fragment exited with status {status}; the failing fence is the "
                f"last '+++ {page.name}:LINE' marker above",
                file=sys.stderr,
            )
            return 1
        failed = False
        for item in args.validate:
            name, events = item.rsplit(":", 1)
            proc = subprocess.run(
                [sys.executable, "-m", "mcp_server_key4hep.cli", "validate",
                 str(work / name), "--events", events],
                capture_output=True, text=True,
            )
            result = json.loads(proc.stdout) if proc.stdout.strip() else {"error": proc.stderr}
            print(f"{name}: {json.dumps(result, sort_keys=True)}")
            failed |= proc.returncode != 0
        return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
