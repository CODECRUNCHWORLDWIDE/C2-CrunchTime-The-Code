"""problem-04-radio-tail-watch-solution.py — watching the tail of a stream.

A harbour radio desk receives letters one at a time, forever. Certain words
are call words the duty officer must be told about, and a call word counts
only when it lands at the very end of what has arrived so far.

Because the interesting end of the stream is the newest letter, the tree is
built out of the call words spelled backwards. Then a walk from the newest
letter backwards is an ordinary walk down a prefix tree.

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""

END = "*"

CallTree = dict

CALL_WORDS: list[str] = ["PAN", "PANPAN", "MAY", "MAYDAY"]

STREAM = "QPANPANZMAYDAY"


class TailWatch:
    """A radio tail watch over a fixed list of call words."""

    def __init__(self, call_words: list[str]) -> None:
        """Build the reversed tree and the buffer.

        Args:
            call_words: The words to watch for. Must not be empty, and no word
                may be the empty string.

        Raises:
            ValueError: If the list is empty or holds an empty word.
        """
        if not call_words:
            raise ValueError("a tail watch needs at least one call word")
        self._root: CallTree = {}
        for word in call_words:
            if not word:
                raise ValueError("a call word cannot be the empty string")
            node = self._root
            for letter in reversed(word):
                node = node.setdefault(letter, {})
            node[END] = True
        self._longest = max(len(word) for word in call_words)
        self._tail: list[str] = []

    def feed(self, letter: str) -> str:
        """Take one more letter and report the longest call word ending here.

        Args:
            letter: Exactly one character from the stream.

        Returns:
            The longest call word that ends at this letter, or "" when none
            does.

        Raises:
            ValueError: If `letter` is not exactly one character.
        """
        if len(letter) != 1:
            raise ValueError("feed takes exactly one letter at a time")
        self._tail.append(letter)
        if len(self._tail) > self._longest:
            self._tail.pop(0)

        node = self._root
        best = ""
        spelled = 0
        for back in reversed(self._tail):
            if back not in node:
                break
            node = node[back]
            spelled += 1
            if END in node:
                best = "".join(self._tail[-spelled:])
        return best


# ---- Self-check ----
if __name__ == "__main__":
    watch = TailWatch(CALL_WORDS)
    heard: list[str] = []
    for letter in STREAM:
        call = watch.feed(letter)
        heard.append(call)
        print(f"{letter}  {call or '-'}")

    print()
    print(f"call words heard  {[call for call in heard if call]}")

    assert [call for call in heard if call] == ["PAN", "PANPAN", "MAY", "MAYDAY"]
    assert heard[3] == "PAN"
    assert heard[6] == "PANPAN"
    assert heard[13] == "MAYDAY"

    quiet = TailWatch(["TIDE"])
    assert [quiet.feed(letter) for letter in "TIDAL"] == ["", "", "", "", ""]

    try:
        TailWatch([])
    except ValueError as problem:
        assert str(problem) == "a tail watch needs at least one call word"
    else:
        raise AssertionError("an empty watch list should have been rejected")

    try:
        TailWatch(CALL_WORDS).feed("AB")
    except ValueError as problem:
        assert str(problem) == "feed takes exactly one letter at a time"
    else:
        raise AssertionError("a two-letter feed should have been rejected")

    print()
    print("All checks passed.")
