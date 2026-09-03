"""README-solution.py - both Week 9 mini-project problems, worked.

The prefix tree and the linear-time matcher, written to the two starters'
contracts. Together they are the week's whole recognition question: is this a
PREFIX problem or an EXACT SUBSTRING problem? The two structures answer
different questions and are not interchangeable, which is the thing a write-up
has to say out loud.

Problem 1 - the seed index. A trie, because the counter asks "anything starting
with these letters?" on every keystroke. A set answers that only by walking
every key it holds.

Problem 2 - the tide log. KMP, because the naive scanner restarts the pattern at
every position and the failure function removes the restart. The text pointer
never moves backward; that is the sentence the defence rests on.

Labels are printed in plain capitals rather than Markdown headings: this output
is published inside a fenced block on the page, and a "##" line inside that fence
reads as a new page section to anything splitting the page on headings.

Run it and the self-checks assert every case both harnesses state. When they pass
it prints "All checks passed."
"""

END = "\0end"


# ------------------------------------------------------------ the trie ----


class SeedIndex:
    """A prefix tree over packet codes.

    Dicts all the way down: each node maps one character to the node beneath it,
    and carries END when a complete code stops there.

    Cost, for a code of length L over an alphabet of size A:
        insert       O(L) time, O(L) new nodes worst case
        search       O(L) time, O(1) space
        starts_with  O(P) time for a prefix of length P

    None of the three depends on how many codes are stored, which is the whole
    argument for the structure.
    """

    def __init__(self) -> None:
        self.root: dict = {}

    def insert(self, code: str) -> None:
        """File one packet code."""
        node = self.root
        for ch in code:
            node = node.setdefault(ch, {})
        # END is set on the node the code STOPS at. Without it "sag" would count
        # as stocked merely because "sage" is.
        node[END] = True

    def _descend(self, text: str) -> dict | None:
        """Walk the tree; return the node arrived at, or None if the walk broke."""
        node = self.root
        for ch in text:
            node = node.get(ch)
            if node is None:
                return None
        return node

    def search(self, code: str) -> bool:
        """Is this exact code stocked?"""
        node = self._descend(code)
        # Arriving is not enough. The END check is the difference between this
        # and starts_with, and it is the only difference.
        return node is not None and END in node

    def starts_with(self, prefix: str) -> bool:
        """Is anything stocked under this prefix?"""
        return self._descend(prefix) is not None


# ------------------------------------------------------------- the KMP ----


def failure_function(pattern: str) -> list[int]:
    """Longest proper prefix of pattern[:i+1] that is also a suffix of it.

    Args:
        pattern: The signature being searched for.

    Returns:
        A list the same length as pattern.
    """
    fail = [0] * len(pattern)
    matched = 0
    for i in range(1, len(pattern)):
        # Fall back through the table rather than resetting to zero. Resetting
        # is what makes the naive scanner quadratic; this loop is what makes the
        # whole build linear, because `matched` only ever decreases here and it
        # only ever rose once per character.
        while matched and pattern[i] != pattern[matched]:
            matched = fail[matched - 1]
        if pattern[i] == pattern[matched]:
            matched += 1
        fail[i] = matched
    return fail


def find_first(text: str, pattern: str) -> int:
    """Index of the first occurrence of pattern in text, or -1.

    Args:
        text: The log to scan.
        pattern: The signature to find. An empty pattern matches at 0.

    Returns:
        The starting index, or -1.
    """
    if not pattern:
        return 0
    if len(pattern) > len(text):
        return -1

    fail = failure_function(pattern)
    matched = 0
    for i, ch in enumerate(text):
        while matched and ch != pattern[matched]:
            matched = fail[matched - 1]
        if ch == pattern[matched]:
            matched += 1
        if matched == len(pattern):
            # i is the LAST character of the match, so the start is behind it.
            return i - len(pattern) + 1
    return -1


# ---- Self-check ----
if __name__ == "__main__":
    print("1 - the seed index (trie)")
    index = SeedIndex()
    for code in ("sage", "sag", "salsify", "borage", "beet"):
        index.insert(code)
    for code in ("sage", "sag", "sa", "salsify", "beetroot", ""):
        print(f"    search {code!r:<10} -> {index.search(code)}")
    for prefix in ("sa", "sal", "b", "z", "", "sages"):
        print(f"    prefix {prefix!r:<10} -> {index.starts_with(prefix)}")

    print("2 - the tide log (KMP)")
    for pattern in ("abab", "aaaa", "abcd", "aabaaab", ""):
        print(f"    failure {pattern!r:<10} -> {failure_function(pattern)}")
    for text, pattern in (("tide gauge tide", "gauge"), ("aaaaab", "aab"),
                          ("abababc", "ababc"), ("abc", "abcd"),
                          ("abc", ""), ("", "a"), ("", ""), ("aaa", "aaa")):
        print(f"    find {pattern!r:<8} in {text!r:<18} -> {find_first(text, pattern)}")

    # ---- Problem 1: every case the starter's harness states.
    assert index.search("sage") is True
    assert index.search("sag") is True
    assert index.search("sa") is False          # a prefix is not a code
    assert index.search("salsify") is True
    assert index.search("beetroot") is False    # runs past the end of the tree
    assert index.search("") is False            # nothing was filed empty
    assert index.starts_with("sa") is True
    assert index.starts_with("sal") is True
    assert index.starts_with("b") is True
    assert index.starts_with("z") is False
    assert index.starts_with("") is True        # everything starts with nothing
    assert index.starts_with("sages") is False

    # The discriminator, stated as an assertion: same argument, different answer.
    assert index.starts_with("sa") and not index.search("sa")

    # ---- Problem 2: the table by hand, then the matcher.
    assert failure_function("abab") == [0, 0, 1, 2]
    assert failure_function("aaaa") == [0, 1, 2, 3]
    assert failure_function("abcd") == [0, 0, 0, 0]
    assert failure_function("aabaaab") == [0, 1, 0, 1, 2, 2, 3]
    assert failure_function("") == []

    assert find_first("tide gauge tide", "gauge") == 5
    assert find_first("aaaaab", "aab") == 3
    assert find_first("abababc", "ababc") == 2   # needs the fallback
    assert find_first("abc", "abcd") == -1       # pattern longer than text
    assert find_first("abc", "") == 0            # empty pattern
    assert find_first("", "a") == -1             # empty text
    assert find_first("", "") == 0               # both empty
    assert find_first("aaa", "aaa") == 0         # whole text

    print()
    print("All checks passed.")
