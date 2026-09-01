# Problem 2 — Narration Review

> **Topic:** listening back to your own FRAME narration, and counting the fillers with a program because your ear stops noticing them
> **Lecture:** [02 — The FRAME Method](../lecture-notes/02-the-frame-method.md)
> **Difficulty:** Easy
> **Target time:** 30 minutes
> **Why this one:** the whole course rests on being able to think out loud, and the only way to get better at that is to hear yourself doing it. Listening back is uncomfortable and it is the assignment. The program is here because an ear stops noticing "um" after the third one, and a count does not.

## The Brief

Take the recording you made while solving
[Exercise 1 — Reverse the Siding](../exercises/exercise-01-reverse-the-siding.md).
Listen to it at 1.5× speed. Write down three things you notice about your own
narration and one specific habit to work on in Exercise 2.

Then measure the part that can be measured.

A **filler** is a sound or phrase that occupies the space where a word would
go without carrying any meaning — `um`, `uh`, `you know`, `basically`,
`I mean`. Everybody uses them. They are not a moral failing and the goal is
not zero. The goal is *knowing your rate*, because a filler every four
seconds reads as nervous and a filler every twenty seconds reads as thinking.

Write a program that takes a transcript and the length of the recording, and
reports which fillers you used, how many times, and your rate per minute.

Three pieces:

**Tokenise.** Split the transcript into words, lowercase them, and strip the
punctuation stuck to their edges. `"Um,"` and `"um"` are the same filler.

**Count.** Some fillers are one word and some are two. `you know`, `sort of`,
`kind of` and `I mean` have to be spotted as *pairs of neighbouring words*,
and a word swallowed by a pair must not then be counted again on its own.

**Rate.** Fillers per minute, to one decimal place. A recording of zero
seconds has no rate, so it reports `0.0` rather than raising.

## Starter

Save this as `problem-02-narration-review.py` and fill in the `TODO`s.

```python
"""problem-02-narration-review.py — counting the fillers in your own narration.

Tokenise the transcript, count single-word and two-word fillers, and report
a rate per minute.

Fill in every TODO, then run the file. The self-checks at the bottom print
"All checks passed." when the module is correct.
"""

SINGLE_FILLERS = {"um", "uh", "er", "erm", "basically", "actually", "literally", "right"}
PAIR_FILLERS = {("you", "know"), ("sort", "of"), ("kind", "of"), ("i", "mean")}

PUNCTUATION = ".,!?;:—-\"'()[]"


def tokenise(transcript: str) -> list[str]:
    """Split a transcript into lowercase words with punctuation removed."""
    # TODO: split on whitespace, strip PUNCTUATION from both ends of each
    #       word, lowercase it, and drop anything that stripped to nothing
    ...


def count_fillers(words: list[str]) -> dict[str, int]:
    """Count filler words and filler phrases in a token list."""
    # TODO: walk the list with an index rather than a for-loop, because a
    #       two-word filler consumes TWO positions
    # TODO: look at the pair (words[index], words[index + 1]) first — but
    #       only when there IS an index + 1
    # TODO: a pair that matched advances the index by two, so neither of its
    #       words is counted again on its own
    ...


def filler_rate(counts: dict[str, int], seconds: int) -> float:
    """Return fillers per minute, rounded to one decimal place."""
    # TODO: zero or negative seconds returns 0.0 and must not divide by zero
    ...


# ---- Self-check ----
if __name__ == "__main__":
    print(count_fillers(tokenise("Um, you know, basically.")))

    assert tokenise("Um, so-") == ["um", "so"]
    assert count_fillers(["you"]) == {}
    assert filler_rate({"um": 3}, 45) == 4.0
    assert filler_rate({}, 0) == 0.0
    print("All checks passed.")
```

**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C2-CrunchTime-The-Code/curriculum/week-01-the-frame-method-and-thinking-aloud/homework/problem-02-narration-review.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `tokenise` returns lowercase words with edge punctuation removed, and
   drops anything that stripped to nothing.
2. `count_fillers` returns a dict from filler to count. Fillers that never
   occurred are absent from the dict, not present with a zero.
3. Two-word fillers are counted as one filler, and their words are not
   counted again individually.
4. A pair at the very end of the transcript with only one word left does not
   raise.
5. `filler_rate` rounds to one decimal place and returns `0.0` for a
   non-positive duration.
6. The report lists fillers most frequent first, breaking ties
   alphabetically, so the same transcript always prints the same table.
7. Every function keeps its type hints and its docstring.

## Constraints

- **Fillers are matched on whole tokens, never on substrings.** `"um" in word`
  would match `"drum"`, `"number"` and `"maximum"`. Splitting into words first
  and comparing whole words is what makes the count mean anything, and it is
  the reason `tokenise` exists as its own function rather than being inlined.

- **Punctuation is stripped from the edges only.** `strip` removes characters
  from both ends and stops at the first character that is not in the set, so
  `"don't"` survives intact while `"Um,"` becomes `"um"`. Removing punctuation
  everywhere would turn `"don't"` into `"dont"` for no benefit, and would
  quietly merge two different words in some transcripts.

- **The pair check comes before the single check, and consumes two
  positions.** Otherwise `you know` is counted as `know` — or worse, `right`
  is counted inside `all right`. Whenever a longer pattern and a shorter one
  can both match at the same place, the longer one has to be tried first. This
  is the same rule that makes a tokeniser check `>=` before `>`.

- **The rate is per minute, not per word.** Both are defensible and they
  measure different things. Per minute captures pace, which is what a listener
  experiences. Per hundred words would normalise away the fact that you talk
  faster when you are nervous, which is precisely the thing you are trying to
  hear.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13:

```text
$ python problem-02-narration-review-solution.py
 2  right
 2  uh
 2  um
 1  actually
 1  basically
 1  i mean
 1  sort of
 1  you know

11 fillers in 65 words over 45s
14.7 fillers per minute
All checks passed.
```

Fourteen and a bit per minute is roughly one every four seconds, which is a
realistic first recording and is high enough to hear. It is also worth
noticing what the table does *not* say: it does not say the narration was
bad. The transcript being counted contains a correct pattern match, a rejected
alternative with a reason, and a plan — all the right content, delivered with
a filler every four seconds.

Note `i mean` in the table rather than `I mean`. Tokenising lowercases
everything, so that is what the count is keyed on. Prettifying it for display
would be a reasonable thing to add and is deliberately not done here, because
the display key and the counting key being the same thing is one fewer place
for them to disagree.

## Steps

1. Listen to your Exercise 1 recording at 1.5×. Note the total length in
   seconds — you will need it.
2. Write down three observations and one habit to drill. Do this *before* you
   write the program, so your notes are about what you heard rather than about
   what the count said.
3. Save the starter and run it. `AssertionError`.
4. Write `tokenise`. Test it on `"Um, so-"` before going further.
5. Write `count_fillers` with a `while` loop and an explicit index. A
   `for word in words` loop cannot skip ahead, and skipping ahead is exactly
   what a two-word filler needs.
6. Guard the pair lookup: only build the pair when `index + 1 < len(words)`.
7. Write `filler_rate`, zero guard first.
8. Type out sixty seconds of your own transcript and run it on that. You do
   not need the whole recording; the first minute is representative and
   transcribing more than that is not a good use of your half hour.

## The Solution

```python
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
```

**The `while` loop with an explicit index is not old-fashioned, it is
required.** A `for word in words` loop advances by exactly one every time and
gives you no way to say "I consumed two of those." Two-word fillers need to
consume two. Whenever the number of items you handle per step is not fixed,
the index has to be yours to move — and this is the same reason Exercise 2's
skip loops manage their own pointers.

**The pair is built defensively and compared as a tuple.**
`(words[index], words[index + 1]) if index + 1 < len(words) else None` reads
as "the pair, when there is one". Building it unconditionally raises
`IndexError` on the last word of every transcript that ends in a filler. Using
`None` for "no pair" is safe here because `None` can never be in
`PAIR_FILLERS`, so the membership test simply fails and the code falls through
to the single-word check.

**`continue` after a pair match is what stops the double count.** The
`index += 2` skips past both words, and `continue` jumps back to the top
without running the single-word check on `words[index]` — which by then is a
word we have already moved past. Drop the `continue` and `right` in
`you know, right` gets counted twice.

**`counts.get(phrase, 0) + 1` rather than a `defaultdict`.** Both work.
`.get` with a default is the one that keeps the dict a plain dict, so a caller
who prints it does not see `defaultdict(<class 'int'>, {...})` and wonder what
they are looking at. Week 2 has more to say about this trade.

**Absent rather than zero.** A filler you never said is not in the dict at
all. That is why the report needs no filter — `sorted(counts, ...)` already
only sees what happened. Storing zeros would mean every report listed eleven
fillers, most of them empty, and the reader would have to do the filtering
with their eyes.

**The sort key is `(-counts[f], f)`.** Most frequent first, and alphabetical
inside a tie. Without the second half, two fillers with the same count would
come out in dictionary insertion order, which depends on what you happened to
say first — so the same transcript would give the same numbers in a different
order, and you could not diff two reports. This is the same tuple-key trick as
C1's leaderboard, and it is worth recognising as the same trick.

## Download and run

Download
[problem-02-narration-review-solution.py](./problem-02-narration-review-solution.py)
and run it:

```bash
python problem-02-narration-review-solution.py
```

Replace `TRANSCRIPT` and `SECONDS` with your own and run it again.

## Common bugs to catch

- **`IndexError: list index out of range` on a transcript ending in a
  filler.** You built the pair without checking there was a next word:

  ```text
  Traceback (most recent call last):
      count_fillers(["um", "you"])
      pair = (words[index], words[index + 1])
                            ~~~~~^^^^^^^^^^^
  IndexError: list index out of range
  ```

  Every transcript that ends mid-thought hits this, which is most real
  transcripts. The guard is `if index + 1 < len(words)`.

- **`ZeroDivisionError: division by zero` on a zero-second recording.**

  ```text
  Traceback (most recent call last):
      filler_rate({}, 0)
      return round(sum(counts.values()) * 60 / seconds, 1)
                   ~~~~~~~~~~~~~~~~~~~~~~~~~~^~~~~~~~~
  ZeroDivisionError: division by zero
  ```

  You will hit this the first time you run the program before you have
  filled in the duration.

- **`you know` counted, and `know` counted again.** You matched the pair but
  forgot `continue`, so the single-word check then ran on the second half.
  Nothing raises; the total is simply too high. If your counts look inflated
  and the inflation is exactly the number of pairs, this is it.

- **`right` never counted, because `all right` ate it.** The opposite
  problem, and it appears the moment you add a longer phrase to
  `PAIR_FILLERS`. Longer patterns first is the rule; but be sure the longer
  pattern is one you actually meant to match.

- **`"drum"` counted as `"um"`.** You searched for the filler inside the
  transcript string instead of comparing whole tokens. `"um" in transcript`
  is a substring test and it is `True` for almost any English text.

- **`"Um,"` and `"um"` counted separately.** You lowercased but did not
  strip, or stripped but did not lowercase. Both, on both sides, once, in
  `tokenise`.

## Under the hood

<details>
<summary>Under the hood — what a tokeniser really is, and why filler rate is only half the story</summary>

**You just wrote a tokeniser.**

Splitting text into meaningful units is the first stage of every compiler,
every search engine and every natural-language pipeline, and it is called
**tokenisation**. The version here is about as simple as one gets: split on
whitespace, normalise the edges, lowercase. Real ones handle contractions,
hyphenated words, numbers with decimal points, and the fact that `"U.S."` is
one token and `"end."` is two.

The structural thing worth carrying away is the shape: **normalise, then
compare against normalised data.** Every filler in the two sets is already
lowercase and already punctuation-free, so the comparison is a plain equality
test. The alternative — comparing raw text against a set of every spelling
you can think of — grows without limit and still misses cases.

**Maximal munch.**

Trying the two-word filler before the one-word filler has a name in
compiler-writing: **maximal munch**, or the longest-match rule. A tokeniser
reading `>=` must not decide it has seen `>` and then be surprised by `=`. The
rule generalises: when several patterns can match at one position, take the
longest.

Our version handles pairs only. Extending it to three-word phrases means
checking triples first, then pairs, then singles — and at that point you would
stop hand-writing the ladder and drive it from a list of phrases sorted by
length, which is what a real tokeniser does.

**Rate is one number, and it is not the interesting one.**

Fillers cluster. Ten "um"s spread evenly across a five-minute narration reads
as ordinary speech. Ten in the fifteen seconds after the interviewer asks
"what's the complexity?" reads as panic, and they are the same rate.

So when you listen back, listen for *where* they fall. The moment before a
filler burst is a moment you did not know what to say, and that moment is data
about your preparation, not about your speech. This is why the written half of
this problem is not decoration: the count tells you how much, and only your
own ear tells you when.

**Three things worth noting that no program can count:** whether you finished
your sentences, whether you said the number out loud when you traced, and
whether you ever asked a question. Those go in your notes.

</details>

## Acceptance checklist

- [ ] You listened to the full Exercise 1 recording at 1.5×.
- [ ] `frame-writeups/c2-week-01/exercise-01-self-review.md` exists in your portfolio repo and holds the recording length, three observations, and one habit to drill in Exercise 2.
- [ ] `python problem-02-narration-review.py` prints `{'um': 1, 'you know': 1, 'basically': 1}`, then `All checks passed.`
- [ ] Tokenising happens once, and the fillers are compared as whole words.
- [ ] A transcript ending in `you` does not raise.
- [ ] A pair match does not also count its second word.
- [ ] `filler_rate({}, 0)` returns `0.0`.
- [ ] The table is sorted most-frequent first with an alphabetical tie-break, so two runs of the same transcript print identically.
- [ ] You ran it on at least sixty seconds of your own transcript.
- [ ] Every function has type hints and a docstring.

If listening back makes you cringe, that is data. Write it down.

## Stretch

- **Find where the fillers cluster, not just how many there are.**

  ```python
  def filler_positions(words: list[str]) -> list[int]:
      """Return the token index of every filler, in order."""
      positions: list[int] = []
      index = 0
      while index < len(words):
          pair = (words[index], words[index + 1]) if index + 1 < len(words) else None
          if pair in PAIR_FILLERS:
              positions.append(index)
              index += 2
              continue
          if words[index] in SINGLE_FILLERS:
              positions.append(index)
          index += 1
      return positions
  ```

  ```text
  [0, 6, 9, 14, 21, 25, 31, 35, 42, 45, 60]
  ```

  Look at the gaps rather than the list. Two fillers three tokens apart is a
  stall; two fillers twenty tokens apart is speech. Then work out what you
  would have to change for this function and `count_fillers` to stop being
  two copies of the same loop.

- **Report the longest run of words with no filler in it.** That number is the
  one that improves as you get better, and it improves visibly.

- **Count sentence fragments.** Split on `.` and `?`, and report how many
  "sentences" are under four words. Trailing off mid-thought is a habit that
  costs more in an interview than "um" does, and it is invisible until you
  count it.

Next: [Problem 3 — A Problem You Have Never Seen](./problem-03-wild-problem.md).
