"""problem-01-portfolio-setup-solution.py — grading your own commit log.

The portfolio repo's value is its history, so the history is worth checking.
Four rules, each one a thing a reviewer would actually notice, applied to the
subject line of every commit.

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""

VAGUE = {"wip", "stuff", "update", "updates", "fix", "fixes", "changes", "final", "misc"}

MIN_LENGTH = 15
MAX_LENGTH = 72


def judge_subject(subject: str) -> str:
    """Judge one commit subject line against the four rules.

    Args:
        subject: The first line of a commit message, as Git stores it.

    Returns:
        "ok", or the first rule it breaks, in the order the rules are
        checked. One reason per subject keeps the report readable.
    """
    trimmed = subject.strip()
    if trimmed.lower().rstrip(".!") in VAGUE:
        return "says nothing"
    if len(trimmed) < MIN_LENGTH:
        return "too short"
    if len(trimmed) > MAX_LENGTH:
        return "too long for one line"
    if trimmed.endswith("."):
        return "trailing full stop"
    return "ok"


def audit_commit_subjects(subjects: list[str]) -> list[tuple[str, str]]:
    """Judge every commit subject, keeping the log's own order.

    Args:
        subjects: Commit subject lines, newest last, as `git log` prints
            them with --format=%s --reverse.

    Returns:
        One (subject, verdict) pair per subject, in the same order.
    """
    return [(subject, judge_subject(subject)) for subject in subjects]


def pass_rate(findings: list[tuple[str, str]]) -> float:
    """Return the share of subjects judged "ok", as a percentage.

    Args:
        findings: The output of audit_commit_subjects.

    Returns:
        A percentage from 0.0 to 100.0. An empty log scores 0.0, because a
        repository with no commits has not demonstrated anything.
    """
    if not findings:
        return 0.0
    good = sum(1 for _, verdict in findings if verdict == "ok")
    return good * 100 / len(findings)


# ---- Self-check ----
if __name__ == "__main__":
    LOG = [
        "Initial commit",
        "Add .gitignore and CC-BY-4.0 licence",
        "wip",
        "Add Week 1 exercise 1 FRAME write-up",
        "Add Week 1 exercise 1 solution: reverse the siding",
        "stuff",
        "Fix the swap count in exercise 1 so a refused order bills zero.",
        "Add Week 1 exercise 2 FRAME write-up and solution",
        "Rewrite the portfolio cover so it answers all five questions a recruiter asks before they scroll",
        "Add behavioral story 1: the overnight cache bug",
    ]

    findings = audit_commit_subjects(LOG)
    for subject, verdict in findings:
        flag = "ok " if verdict == "ok" else "BAD"
        shown = subject if len(subject) <= 52 else subject[:49] + "..."
        print(f"{flag}  {shown:<52}  {verdict}")

    print()
    print(f"{pass_rate(findings):.0f}% of {len(findings)} commits would survive a reviewer.")

    assert judge_subject("wip") == "says nothing"
    assert judge_subject("WIP.") == "says nothing"
    assert judge_subject("Fix typo") == "too short"
    assert judge_subject("x" * 80) == "too long for one line"
    assert judge_subject("Add Week 1 exercise 1 solution.") == "trailing full stop"
    assert judge_subject("Add Week 1 exercise 1 FRAME write-up") == "ok"
    assert audit_commit_subjects([]) == []
    assert pass_rate([]) == 0.0
    assert pass_rate([("a", "ok"), ("b", "too short")]) == 50.0
    print("All checks passed.")
