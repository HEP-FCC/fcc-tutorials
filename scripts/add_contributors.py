#!/usr/bin/env python3

"""
Insert a "Page contributors" block at the top of tutorial pages.

Reads the git history of each Markdown page, compiles the contributor names, and inserts
(or refreshes) a collapsible MyST admonition right after the page's H1 title:

    <!-- contributors:start -->
    :::{admonition} Page contributors
    :class: callout dropdown

    Name One, Name Two, ...
    :::
    <!-- contributors:end -->

The HTML-comment markers make that the script replaces the existing block instead of adding a second one.

Usage:
    python3 scripts/add_contributors.py <file.md> [...]
    python3 scripts/add_contributors.py --all [--max-names 8] [--dry-run]
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

GITHUB_HISTORY_URL = "https://github.com/HEP-FCC/fcc-tutorials/commits/main/{path}"

# Delimit the location of the contributors admonition
START_MARKER = "<!-- contributors:start -->"
END_MARKER = "<!-- contributors:end -->"

# Non-page Markdown files never given a contributors block. The top-level
# README.md is excluded because index.md is a symlink to it.
EXCLUDED_DIRS = ("archive/", ".github/")
EXCLUDED_FILES = {
    "README.md",
    "CLAUDE.md",
    "CONTRIBUTING.md",
    "CODE_OF_CONDUCT.md",
    "CONDUCT.md",
    "LICENSE.md",
    "TODO.md",
    "TESTS.md",
    "FIXME.md",
}

BOT_PATTERNS = re.compile(r"\[bot\]$|github-actions|dependabot", re.IGNORECASE)


def repo_root():
    """
    Return the root of the repository.
    """
    out = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        capture_output=True, text=True, check=True,
    )
    return Path(out.stdout.strip())


def page_contributors(root, rel_path):
    """
    Return contributor names for a file, ordered for display.

    The author of the very first commit comes first; the remaining names
    are sorted by number of commits (ties broken by first contribution).
    """
    out = subprocess.run(
        ["git", "log", "--follow", "--no-merges",
         "--format=%aN%x09%aE", "--", str(rel_path)],
        capture_output=True, text=True, check=True, cwd=root,
    )
    # git log is newest-first; reverse to walk the history chronologically.
    commits = [line.split("\t") for line in reversed(out.stdout.splitlines()) if line]

    by_email = {}    # email (lower) -> canonical name
    by_name = {}     # name (lower) -> canonical name
    counts = {}      # canonical name -> commit count
    order = []       # canonical names in order of first contribution
    for name, email in commits:
        if BOT_PATTERNS.search(name) or BOT_PATTERNS.search(email):
            continue
        canonical = by_email.get(email.lower()) or by_name.get(name.lower())
        if canonical is None:
            canonical = name
            order.append(canonical)
        by_email[email.lower()] = canonical
        by_name[name.lower()] = canonical
        counts[canonical] = counts.get(canonical, 0) + 1

    if not order:
        return []
    original_author, rest = order[0], order[1:]
    rest.sort(key=lambda n: (-counts[n], order.index(n)))
    return [original_author] + rest


def render_block(names, rel_path, max_names):
    """
    Takes the list of names and renders the text to be added on top of the page.

    If len(names) > max_names, the list is truncated and a link to the full git history is added.
    """
    if len(names) > max_names:
        shown = ", ".join(names[:max_names])
        url = GITHUB_HISTORY_URL.format(path=rel_path.as_posix())
        listing = (f"{shown}, and {len(names) - max_names} more"
                   f" — [full history]({url})")
    else:
        listing = ", ".join(names)
    return (
        f"{START_MARKER}\n"
        ":::{admonition} Page contributors\n"
        ":class: callout dropdown\n"
        "\n"
        f"{listing}\n"
        ":::\n"
        f"{END_MARKER}"
    )


def insert_block(content, block):
    """
    Replace an existing marked block, or insert after the first H1.
    """
    if START_MARKER in content and END_MARKER in content:
        pattern = re.escape(START_MARKER) + r".*?" + re.escape(END_MARKER)
        return re.sub(pattern, block, content, count=1, flags=re.DOTALL), None

    lines = content.splitlines(keepends=True)
    in_fence = False
    for i, line in enumerate(lines):
        if re.match(r"^(```|~~~)", line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        # ATX H1 (# Title), or setext H1 (Title followed by a ==== line).
        is_h1 = re.match(r"^# ", line)
        if not is_h1 and line.strip() and i + 1 < len(lines) \
                and re.match(r"^=+\s*$", lines[i + 1]):
            is_h1 = True
            i += 1
        if is_h1:
            head = "".join(lines[: i + 1])
            tail = "".join(lines[i + 1:])
            return f"{head}\n{block}\n\n{tail.lstrip(chr(10))}", None

    return f"{block}\n\n{content}", "no H1 heading found, block inserted at top"


def eligible_pages(root):
    out = subprocess.run(
        ["git", "ls-files", "*.md"],
        capture_output=True, text=True, check=True, cwd=root,
    )
    pages = []
    for rel in out.stdout.splitlines():
        if rel.startswith(EXCLUDED_DIRS) or rel in EXCLUDED_FILES:
            continue
        if (root / rel).is_symlink():
            continue
        pages.append(Path(rel))
    return pages


def main():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("files", nargs="*", type=Path,
                        help="Markdown pages to process")
    parser.add_argument("--all", action="store_true",
                        help="process every eligible tracked .md page")
    parser.add_argument("--max-names", type=int, default=8, metavar="N",
                        help="names shown before truncating (default: 8)")
    parser.add_argument("--dry-run", action="store_true",
                        help="report what would change without writing")
    args = parser.parse_args()

    if bool(args.files) == args.all:
        parser.error("give either file paths or --all")

    root = repo_root()
    if args.all:
        pages = eligible_pages(root)
    else:
        pages = [p.resolve().relative_to(root) for p in args.files]

    changed = 0
    for rel_path in pages:
        path = root / rel_path
        names = page_contributors(root, rel_path)
        if not names:
            print(f"skip  {rel_path} (no git history)")
            continue
        content = path.read_text(encoding="utf-8")
        block = render_block(names, rel_path, args.max_names)
        new_content, warning = insert_block(content, block)
        if warning:
            print(f"warn  {rel_path}: {warning}", file=sys.stderr)
        if new_content == content:
            print(f"ok    {rel_path} (up to date)")
            continue
        if not args.dry_run:
            path.write_text(new_content, encoding="utf-8")
        changed += 1
        verb = "would update" if args.dry_run else "update"
        print(f"{verb}  {rel_path} ({len(names)} contributor"
              f"{'s' if len(names) != 1 else ''})")

    print(f"\n{changed} page(s) {'to update' if args.dry_run else 'updated'}.")


if __name__ == "__main__":
    main()
