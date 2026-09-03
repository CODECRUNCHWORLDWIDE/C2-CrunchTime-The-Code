"""problem-01-trie-starter.py - the prefix tree, to fill in.

A seed library files every packet code it stocks. The counter needs two
questions answered fast, and they are not the same question:

    "do we stock exactly this code?"        -> search
    "do we stock anything starting with?"   -> starts_with

The second is why this is a trie and not a set. A set answers the first in O(1)
and the second only by walking every key it holds, which is O(n L) - and the
counter asks the second one on every keystroke.

Fill in the three method bodies. Do not change the signatures, the END sentinel
or the harness: the harness is the spec.

Run it and it will tell you which cases still fail. When they all pass it prints
"All checks passed."
"""

# One shared sentinel object marks "a code ends here". A plain string key would
# collide with a real character; this cannot, because nothing else is it.
END = "\0end"


class SeedIndex:
    """A prefix tree over packet codes.

    The tree is dicts all the way down. Each node maps one character to the node
    beneath it, and carries END when a complete code stops there.
    """

    def __init__(self) -> None:
        self.root: dict = {}

    def insert(self, code: str) -> None:
        """File one packet code.

        Walk the code character by character, creating the node under each
        character if it is not already there, and mark the last node with END.

        Args:
            code: The code to file. May be empty, which files the empty code.
        """
        # TODO: descend from self.root, creating levels as needed, then mark END.
        raise NotImplementedError

    def search(self, code: str) -> bool:
        """Is this exact code stocked?

        Args:
            code: The code to look for.

        Returns:
            True only when the code was filed AND ends where it stops. "sag" is
            not stocked merely because "sage" is.
        """
        # TODO: descend; return whether you arrived AND the node carries END.
        raise NotImplementedError

    def starts_with(self, prefix: str) -> bool:
        """Is anything stocked under this prefix?

        Args:
            prefix: The characters typed so far.

        Returns:
            True when the descent completes, whether or not a code ends there.
            This is the method a set cannot answer cheaply, and the reason the
            whole structure exists.
        """
        # TODO: descend; return whether you arrived. END is irrelevant here.
        raise NotImplementedError


# ---- Harness. This is the spec - do not edit. ----
if __name__ == "__main__":
    index = SeedIndex()
    for code in ("sage", "sag", "salsify", "borage", "beet"):
        index.insert(code)

    checks: list[tuple[str, bool, bool]] = [
        ("search sage", index.search("sage"), True),
        ("search sag", index.search("sag"), True),
        ("search sa", index.search("sa"), False),          # a prefix is not a code
        ("search salsify", index.search("salsify"), True),
        ("search beetroot", index.search("beetroot"), False),  # past the end
        ("search ''", index.search(""), False),            # nothing filed empty
        ("prefix sa", index.starts_with("sa"), True),
        ("prefix sal", index.starts_with("sal"), True),
        ("prefix b", index.starts_with("b"), True),
        ("prefix z", index.starts_with("z"), False),
        ("prefix ''", index.starts_with(""), True),        # everything starts with nothing
        ("prefix sages", index.starts_with("sages"), False),
    ]

    failed = 0
    for label, got, want in checks:
        flag = "ok " if got == want else "FAIL"
        if got != want:
            failed += 1
        print(f"    {flag} {label:<18} got {got!r:<6} want {want!r}")

    print()
    print("All checks passed." if failed == 0 else f"{failed} check(s) still failing.")
