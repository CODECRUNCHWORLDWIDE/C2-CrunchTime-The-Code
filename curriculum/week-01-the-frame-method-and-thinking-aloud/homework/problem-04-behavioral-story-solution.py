"""problem-04-behavioral-story-solution.py — checking a STAR story's shape.

A behavioural story is graded on structure before it is graded on content, so
the structure is worth checking mechanically: four headings, in order, none of
them empty, and a length somebody will sit through.

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""

STAR = ["Situation", "Task", "Action", "Result"]
MIN_WORDS = 200
MAX_WORDS = 400


def split_sections(story: str) -> dict[str, str]:
    """Split a Markdown story into its `## Heading` sections.

    Args:
        story: The story file's text. Headings are `## ` lines.

    Returns:
        A dict from heading text to the body under it. Text before the first
        `## ` heading is discarded, because a STAR story's content lives
        under its headings.
    """
    sections: dict[str, str] = {}
    heading = None
    body: list[str] = []
    for line in story.splitlines():
        if line.startswith("## "):
            if heading is not None:
                sections[heading] = "\n".join(body).strip()
            heading = line[3:].strip()
            body = []
        elif heading is not None:
            body.append(line)
    if heading is not None:
        sections[heading] = "\n".join(body).strip()
    return sections


def word_count(story: str) -> int:
    """Count words in the story's section bodies, ignoring headings.

    Args:
        story: The story file's text.

    Returns:
        How many whitespace-separated words sit under the headings. The
        headings themselves are structure, not story, so they do not count.
    """
    return sum(len(body.split()) for body in split_sections(story).values())


def check_story(story: str) -> list[tuple[str, bool, str]]:
    """Run every structural check over a STAR story.

    Args:
        story: The story file's text.

    Returns:
        One (check name, passed, detail) triple per check, in a fixed order:
        the four headings present, the headings in STAR order, no empty
        section, and the word count inside its budget.
    """
    sections = split_sections(story)
    found = [name for name in sections if name in STAR]
    results: list[tuple[str, bool, str]] = []

    missing = [name for name in STAR if name not in sections]
    results.append(("four headings present", not missing, f"missing {missing}" if missing else "all four"))

    results.append(("headings in STAR order", found == STAR, " then ".join(found) if found else "none found"))

    empty = [name for name in STAR if name in sections and not sections[name]]
    results.append(("no empty section", not empty, f"empty {empty}" if empty else "all four have text"))

    count = word_count(story)
    in_budget = MIN_WORDS <= count <= MAX_WORDS
    results.append((f"{MIN_WORDS}-{MAX_WORDS} words", in_budget, f"{count} words"))

    return results


# ---- Self-check ----
if __name__ == "__main__":
    # Built by joining, not as one triple-quoted block, so that no line of
    # this file begins with "## " at column 0 - a heading marker in column 0
    # inside a code block confuses tools that scan Markdown for sections.
    STORY = "\n\n".join(
        [
            "# Story 1 - a hard bug I debugged",
            "## Situation",
            "word " * 60,
            "## Task",
            "word " * 60,
            "## Action",
            "word " * 80,
            "## Result",
            "word " * 60,
        ]
    )

    for name, passed, detail in check_story(STORY):
        print(f"{'pass' if passed else 'FAIL'}  {name:<24}  {detail}")

    assert split_sections("## Task\nhello") == {"Task": "hello"}
    assert split_sections("no headings here") == {}
    assert word_count("## Task\none two three") == 3
    assert word_count("# Title only") == 0

    checks = check_story(STORY)
    assert [passed for _, passed, _ in checks] == [True, True, True, True]

    out_of_order = "## Task\nx\n## Situation\ny\n## Action\nz\n## Result\nw"
    assert check_story(out_of_order)[1][1] is False

    stub = "## Situation\n\n## Task\nx\n## Action\ny\n## Result\nz"
    assert check_story(stub)[2][1] is False
    assert check_story(stub)[3][1] is False
    print("All checks passed.")
