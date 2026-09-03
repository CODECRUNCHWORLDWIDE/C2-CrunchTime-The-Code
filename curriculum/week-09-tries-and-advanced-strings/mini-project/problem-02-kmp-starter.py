"""problem-02-kmp-starter.py - linear-time substring matching, to fill in.

A tide gauge writes one character per reading into a long log. An operator wants
the first position at which a given fault signature appears.

The naive scanner restarts the pattern at every position in the text, which is
O(n*m). The failure function removes the restart: when a comparison fails after
matching k characters, the pattern already tells you the longest prefix of itself
that is also a suffix of what matched, so the pattern slides forward and the TEXT
POINTER NEVER MOVES BACKWARD. That sentence is the whole defence, and the reason
the total is O(n + m).

Fill in the two functions. Do not change the signatures or the harness: the
harness is the spec.

Run it and it will tell you which cases still fail. When they all pass it prints
"All checks passed."
"""


def failure_function(pattern: str) -> list[int]:
    """Longest proper prefix of pattern[:i+1] that is also a suffix of it.

    fail[i] answers: "if a comparison fails just past position i, how many
    characters are still legitimately matched?" It is computed from the pattern
    alone, before the text is ever read.

    Worked by hand on "abab":

        i=0  "a"     -> 0   a proper prefix cannot be the whole thing
        i=1  "ab"    -> 0   "a" != "b"
        i=2  "aba"   -> 1   "a"
        i=3  "abab"  -> 2   "ab"

    Args:
        pattern: The signature being searched for.

    Returns:
        A list the same length as pattern.
    """
    # TODO: two pointers over the pattern. On a mismatch, fall back through
    # fail[] rather than resetting to zero - that fallback is the algorithm.
    raise NotImplementedError


def find_first(text: str, pattern: str) -> int:
    """Index of the first occurrence of pattern in text, or -1.

    Args:
        text: The log to scan.
        pattern: The signature to find. An empty pattern matches at 0, which is
            the convention every standard library uses and the one the harness
            expects.

    Returns:
        The starting index, or -1 when the pattern does not occur.
    """
    # TODO: walk text once, holding how many pattern characters currently match.
    # On a mismatch, fall back through the failure function. Never decrease the
    # text index.
    raise NotImplementedError


# ---- Harness. This is the spec - do not edit. ----
if __name__ == "__main__":
    fail_checks: list[tuple[str, list[int]]] = [
        ("abab", [0, 0, 1, 2]),
        ("aaaa", [0, 1, 2, 3]),
        ("abcd", [0, 0, 0, 0]),
        ("aabaaab", [0, 1, 0, 1, 2, 2, 3]),
        ("", []),
    ]
    find_checks: list[tuple[str, str, int]] = [
        ("tide gauge tide", "gauge", 5),
        ("aaaaab", "aab", 3),
        ("abababc", "ababc", 2),      # needs the fallback; a reset scanner misses it
        ("abc", "abcd", -1),          # pattern longer than the text
        ("abc", "", 0),               # empty pattern
        ("", "a", -1),                # empty text
        ("", "", 0),                  # both empty
        ("aaa", "aaa", 0),            # whole text
    ]

    failed = 0
    print("failure function")
    for pattern, want in fail_checks:
        got = failure_function(pattern)
        ok = got == want
        failed += not ok
        print(f"    {'ok ' if ok else 'FAIL'} {pattern!r:<10} got {got} want {want}")

    print("find_first")
    for text, pattern, want in find_checks:
        got = find_first(text, pattern)
        ok = got == want
        failed += not ok
        print(f"    {'ok ' if ok else 'FAIL'} {pattern!r:<8} in {text!r:<18} got {got:<3} want {want}")

    print()
    print("All checks passed." if failed == 0 else f"{failed} check(s) still failing.")
