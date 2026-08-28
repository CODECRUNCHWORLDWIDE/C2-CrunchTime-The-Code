"""portfolio-scaffold-solution.py — build and audit your interview-prep portfolio.

The mini-project asks for a repository with a particular shape. This program
is that shape, written down once so a machine can build it and check it.

Two things live here, and keeping them apart is the whole design:

  * PLAN — the required layout, as data. One list of entries.
  * build() and audit() — two functions that read PLAN. One creates what is
    missing; the other reports what is there.

Because both read the same list, the checker can never drift away from the
builder. Add a folder to PLAN and both of them learn about it at once.

Run it with no arguments and it does a rehearsal: it builds the tree inside a
temporary folder, audits it, prints the report, then deletes the folder again
so nothing is left behind. That is what the output below shows.

Run it with a path and it builds there for real:

    python portfolio-scaffold-solution.py --into ~/code/crunchtime-interview-prep-yourhandle

It never overwrites a file that already exists, so it is safe to re-run on a
repository you have been working in for weeks. Re-running is the point: it is
how you find out which week-14 folder you forgot to create.
"""

from __future__ import annotations

import shutil
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

HANDLE_PLACEHOLDER = "<yourhandle>"


@dataclass(frozen=True)
class Entry:
    """One required path in the portfolio, and what should be in it.

    Attributes:
        path: Where it lives, relative to the repository root.
        is_dir: True for a folder, False for a file.
        seed: First line to write into a new file, so the file is never
            empty and always says what it is for. Ignored for folders.
    """

    path: str
    is_dir: bool
    seed: str = ""


PLAN: list[Entry] = [
    Entry("README.md", False, "# CrunchTime Interview Prep"),
    Entry("LICENSE", False, "Choose CC-BY-4.0 or MIT and paste the full text here."),
    Entry(".gitignore", False, "__pycache__/"),
    Entry("progress.md", False, "# Progress dashboard"),
    Entry("frame-writeups", True),
    Entry("frame-writeups/c2-week-01", True),
    Entry("mocks", True),
    Entry("mocks/README.md", False, "# Mock interviews"),
    Entry("system-design", True),
    Entry("system-design/notes-week-01.md", False, "# System design - week 1 warm-up"),
    Entry("behavioral", True),
    Entry("behavioral/story-01.md", False, "# Story 1 - a hard bug I debugged"),
    Entry("recruiter-prep", True),
    Entry("recruiter-prep/README.md", False, "# Recruiter prep - populated in week 15"),
    Entry("study-plan", True),
    Entry("study-plan/week-01-reflection.md", False, "# Week 1 reflection"),
    Entry("study-plan/pre-onsite-template.md", False, "# Pre-onsite plan - four weeks out"),
    Entry("badges", True),
    Entry("badges/README.md", False, "# Badges earned"),
]


def build(root: Path) -> list[str]:
    """Create every missing entry under `root`. Never overwrite.

    Args:
        root: The repository root. Created if it does not exist.

    Returns:
        The paths that were created, in PLAN order.
    """
    created: list[str] = []
    root.mkdir(parents=True, exist_ok=True)

    for entry in PLAN:
        target = root / entry.path
        if entry.is_dir:
            if not target.is_dir():
                target.mkdir(parents=True)
                created.append(entry.path + "/")
        else:
            if not target.exists():
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(entry.seed + "\n", encoding="utf-8")
                created.append(entry.path)

    return created


def audit(root: Path) -> list[tuple[str, bool]]:
    """Report whether each planned entry exists, and is the right kind.

    Args:
        root: The repository root to inspect.

    Returns:
        One (path, ok) pair per PLAN entry, in PLAN order. `ok` is False
        when the entry is missing, and also when a file is standing where a
        folder belongs or the other way round.
    """
    findings: list[tuple[str, bool]] = []
    for entry in PLAN:
        target = root / entry.path
        ok = target.is_dir() if entry.is_dir else target.is_file()
        findings.append((entry.path, ok))
    return findings


def render(findings: list[tuple[str, bool]]) -> list[str]:
    """Turn audit findings into printable lines, folders marked with a slash."""
    lines: list[str] = []
    for path, ok in findings:
        entry = next(item for item in PLAN if item.path == path)
        shown = path + "/" if entry.is_dir else path
        lines.append(f"  {'ok     ' if ok else 'MISSING'}  {shown}")
    return lines


def main(argv: list[str]) -> int:
    """Build the portfolio, audit it, and print the report.

    Args:
        argv: Command-line arguments after the program name. `--into PATH`
            builds at PATH. With no arguments the program rehearses in a
            temporary folder and cleans up afterwards.

    Returns:
        0 when every planned entry is present afterwards, 1 otherwise.
    """
    rehearsing = "--into" not in argv
    if rehearsing:
        root = Path(tempfile.mkdtemp(prefix="crunchtime-portfolio-"))
        print("Rehearsing in a temporary folder. Nothing is written to your disk.")
    else:
        root = Path(argv[argv.index("--into") + 1]).expanduser()
        print(f"Building in {root}")

    print(f"Repository name: crunchtime-interview-prep-{HANDLE_PLACEHOLDER}")
    print()

    try:
        created = build(root)
        print(f"Created {len(created)} of {len(PLAN)} planned entries.")
        print()

        findings = audit(root)
        print("Audit after building:")
        for line in render(findings):
            print(line)
        print()

        # The second build proves the program is safe to re-run: everything
        # already exists, so nothing is created and nothing is overwritten.
        again = build(root)
        print(f"Second run created {len(again)} entries - re-running is safe.")

        missing = [path for path, ok in findings if not ok]
        if missing:
            print(f"Still missing: {missing}")
            return 1
        print("Portfolio skeleton complete.")
        return 0
    finally:
        if rehearsing:
            shutil.rmtree(root, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
