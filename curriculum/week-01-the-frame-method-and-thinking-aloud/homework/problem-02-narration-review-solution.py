"""problem-02-narration-review-solution.py — counting the fillers in your own narration.

Listening back is the assignment. Counting is the part a program does better
than an ear, because an ear stops noticing "um" after the third one.

Single-word fillers are counted from the token list. Two-word fillers are
counted from the pairs of neighbouring tokens, and the words they use are
then not counted again on their own.

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""

SINGLE_FILLERS = {"um", "uh", "er", "erm", "basically", "actually", "literally", "right"}
PAIR_FILLERS = {("you", "know"), ("sort", "of"), ("kind", "of"), ("i", "mean")}

PUNCTUATION = ".,!?;:—-\"'()[]"


def tokenise(transcript: str) -> list[str]:
    """Split a transcript into lowercase words with punctuation removed.

    Args:
        transcript: What you said, typed out or auto-transcribed.

    Returns:
        The words, lowercased and stripped of surrounding punctuation, with
        anything that stripped down to nothing dropped.
    """
    words = []
    for raw in transcript.split():
        word = raw.strip(PUNCTUATION).lower()
        if word:
            words.append(word)
    return words


def count_fillers(words: list[str]) -> dict[str, int]:
    """Count filler words and filler phrases in a token list.

    Args:
        words: The output of tokenise.

    Returns:
        A dict from filler to how many times it occurred. Fillers that never
        occurred are absent. A word swallowed by a two-word filler is not
        counted again on its own.
    """
    counts: dict[str, int] = {}
    index = 0
    while index < len(words):
        pair = (words[index], words[index + 1]) if index + 1 < len(words) else None
        if pair in PAIR_FILLERS:
            phrase = f"{pair[0]} {pair[1]}"
            counts[phrase] = counts.get(phrase, 0) + 1
            index += 2
            continue
        if words[index] in SINGLE_FILLERS:
            counts[words[index]] = counts.get(words[index], 0) + 1
        index += 1
    return counts


def filler_rate(counts: dict[str, int], seconds: int) -> float:
    """Return fillers per minute, rounded to one decimal place.

    Args:
        counts: The output of count_fillers.
        seconds: How long the recording ran. Zero returns 0.0 rather than
            raising, because a zero-length recording has no rate.

    Returns:
        Fillers per minute, to one decimal place.
    """
    if seconds <= 0:
        return 0.0
    return round(sum(counts.values()) * 60 / seconds, 1)


# ---- Self-check ----
if __name__ == "__main__":
    TRANSCRIPT = (
        "Um, so the row is sorted, right, and I basically need two containers "
        "that, uh, add up to the correction figure. You know, I could sort of "
        "check every pair, but actually that's quadratic and, um, the bound "
        "rules it out. So, uh, two pointers. I mean, one at each end, and the "
        "sum tells me which one to move. Right. Let me trace it."
    )
    SECONDS = 45

    words = tokenise(TRANSCRIPT)
    counts = count_fillers(words)

    for filler in sorted(counts, key=lambda f: (-counts[f], f)):
        print(f"{counts[filler]:>2}  {filler}")

    print()
    print(f"{sum(counts.values())} fillers in {len(words)} words over {SECONDS}s")
    print(f"{filler_rate(counts, SECONDS)} fillers per minute")

    assert tokenise("Um, so-") == ["um", "so"]
    assert tokenise("") == []
    assert count_fillers(["um", "um", "hello"]) == {"um": 2}
    assert count_fillers(["you", "know", "right"]) == {"you know": 1, "right": 1}
    assert count_fillers(["you"]) == {}
    assert count_fillers([]) == {}
    assert filler_rate({"um": 3}, 60) == 3.0
    assert filler_rate({"um": 3}, 45) == 4.0
    assert filler_rate({}, 0) == 0.0
    print("All checks passed.")
