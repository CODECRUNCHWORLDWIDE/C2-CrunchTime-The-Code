# Homework Problem 6 — Autocomplete at Scale

> **Topic:** system-design warm-up #5 — the top ten completions for any prefix, a hundred thousand times a second
> **Lecture:** [02 — Binary Search on the Answer](../lecture-notes/02-binary-search-on-the-answer.md)
> **Difficulty:** Easy to attempt, and it stays interesting for years
> **Target time:** 45 minutes
> **Why this one:** the answer has a binary search hiding in it, and most people never see it. A sorted list of terms turns "every completion of this prefix" into two boundary searches — the same two you wrote in [Exercise 2](../exercises/exercise-02-scan-window.md), on strings instead of minutes. Meeting the idea here, in a design question, is what makes it stick as a tool rather than a puzzle.

<!-- no-runnable-file: the deliverable here is a written design note in your portfolio repo, plus your own reading afterwards. There is no program to run — a three-hundred-word answer to a design prompt is the artifact, and the worked example under The Solution is a model to compare yours against, not something to submit. -->

## The Brief

The prompt:

> **"How would you design an autocomplete service that returns the top ten
> completions for any prefix a user types, at a hundred thousand queries per
> second?"**

Write **three hundred words**, in your own words, from what you know today.
**Do not look up the canonical answer first.** The point of the exercise is to
find out what you would actually say in a room, and you cannot find that out
by reading someone else's answer and agreeing with it.

Then — and only then — search for "autocomplete trie" and "autocomplete
service architecture", read one free article on each, and write down three
things you would add.

Some vocabulary so that nothing in the prompt is an unexplained term.

**Prefix.** The letters typed so far. Type `pyth` and the completions might be
`python`, `pythagoras`, `pythons`.

**QPS.** Queries per second. A hundred thousand of them is a large number: it
means about ten microseconds of a single machine's time per query, so the real
answer is many machines, and each one has to be fast and mostly independent of
the others.

**Trie.** A tree where each step down spells one more letter, so all the words
starting `pyth` live under one node. Pronounced "try". Looking up a prefix
costs one step per letter typed and nothing per word stored — which is the
property that makes it the standard answer.

**Top ten.** Not any ten. The ten most popular, by whatever score the product
cares about — search volume, recency, the user's own history.

That last word is where the interesting part is. Finding *all* completions is
easy. Finding the *best ten* out of a hundred thousand of them, in
microseconds, is the actual problem, and there are only a few honest answers:
precompute them, keep a small heap per node, or keep the candidates in score
order and take the first ten.

## Starter

There is no file to run. Create `system-design/notes-week-05.md` in your
portfolio repo and paste this skeleton in.

```markdown
# Week 5 — System design warm-up: autocomplete at 100K QPS

**Prompt:** Design an autocomplete service returning the top ten completions
for any prefix, at 100,000 queries per second.

## My answer, before reading anything

<!-- TODO: ~300 words. Cover, roughly in this order:
     - what one query has to do, end to end
     - where the terms live, and in what shape
     - how you get from a prefix to its candidate completions
     - how you get from candidates to the best ten
     - what you replicate, what you cache, and what happens on an update -->

## Three things I would add after reading

<!-- TODO: one line each, after reading one article on tries and one on
     autocomplete architecture. Name the source. -->

1.
2.
3.

## The binary-search connection

<!-- TODO: 1-2 sentences. Where could a sorted list plus two boundary searches
     replace the tree, and what would that cost you? -->

---

Written before reading: <!-- TODO: date -->  |  Revised after: <!-- TODO: date -->
```

Write the first section in one sitting, without stopping to check anything.
Thirty minutes, then stop.

## Requirements

1. A file `system-design/notes-week-05.md` exists in your portfolio repo and is
   committed.
2. The first section is about three hundred words, written **before** you read
   anything.
3. It says what happens on one query, end to end, in order.
4. It names a data structure for the prefix lookup and says why that one.
5. It says explicitly how the top ten are chosen, not just how the candidates
   are found.
6. It says what happens when the term list is updated.
7. The second section has three specific additions, each naming the source you
   got it from.
8. The last section names where a binary search could do the prefix job, and
   what that trades away.

## Constraints

- **Three hundred words, written cold.** The bound is the exercise. A design
  answer in a real interview is delivered in a few minutes without notes, and
  the only way to find out whether yours holds together is to produce one under
  the same conditions.

- **Read only after writing.** Reading first turns this into a comprehension
  exercise, and comprehension is not what is being trained. The gap between
  what you wrote and what you read is the measurement, and you only get it once
  per prompt.

- **One query, end to end, in order.** A list of technologies is not a design.
  "The request arrives at X, which does Y, which returns Z" is a design, and it
  is what an interviewer can ask questions about.

- **Say how the top ten are chosen.** Almost every first answer describes how to
  find the candidates and then goes quiet about the ranking. The ranking is the
  hard half and the interesting half, and skipping it is the single most common
  weakness in answers to this prompt.

- **A hundred thousand QPS is a real number, not decoration.** It rules things
  out: a per-query scan over a large term list, a database round trip per
  keystroke, anything that recomputes rankings on the fly. Say what it rules
  out — the rejections are as informative as the choices.

## Expected output

There is no program. What finished looks like at the terminal — your word
count and commit hash will differ:

```text
$ wc -w system-design/notes-week-05.md
     412 system-design/notes-week-05.md
$ git add system-design/notes-week-05.md
$ git commit -m "Add week 5 system design note: autocomplete at scale"
```

The count is over three hundred because it includes the three additions and
the closing section. The first section, on its own, should land near three
hundred.

## Steps

1. **Set a timer for thirty minutes** and write the first section. No tabs, no
   searching, no editing as you go.
2. **Start with one query.** A user has typed `pyth`. Follow that single
   request from the keyboard to the ten strings that come back, naming each
   thing it touches.
3. **Decide where the terms live** before you decide anything else. In memory,
   on every machine, in one shape? That decision fixes most of the rest.
4. **Now do the hard half.** You have the candidates for `pyth` — possibly
   thousands. How do the best ten come out, in microseconds? Write down what
   you would precompute and what you would compute per query.
5. **Handle writes.** Terms and scores change. Say whether the structure is
   rebuilt, patched, or swapped, and how often. "It is read-only and rebuilt
   hourly" is a legitimate and strong answer if you say it deliberately.
6. **Count the words.** Cut to about three hundred. Stop.
7. **Now read.** One article on tries, one on autocomplete architecture. Write
   the three additions, naming each source.
8. **Write the binary-search sentence** and commit.

## The Solution

A worked example of the shape — a model answer at roughly the right length and
depth. Read it after you have written your own, not before.

```markdown
## My answer, before reading anything

A query is one prefix and one user, and it has to come back in a few
milliseconds, so it cannot touch a database. Everything it needs sits in
memory on the machine that answers it.

I would keep the terms in a **trie**: a tree where each edge is one letter, so
walking `p`, `y`, `t`, `h` lands on the single node holding every term that
starts `pyth`. That walk costs four steps and does not care whether the service
holds a million terms or ten. A hash map of prefix to completions would also be
`O(1)`, but it has to store an entry for every prefix of every term, which is a
lot of duplication, and it cannot answer a prefix nobody has stored.

Finding the candidates is the easy half. Ranking them is not, so I would not
rank at query time at all: at each trie node I would **precompute and store the
top ten** completions beneath it, in order. Then a query is a walk down four
nodes and a read of a ten-element list, with no sorting and no heap on the hot
path. It costs memory — ten pointers per node — and that is the trade I would
make first.

Updates change the scores, so the structure is not written live. I would build
the whole trie offline, hourly, ship it to every machine as an immutable blob,
and swap it in atomically. That makes every server independent and read-only,
which is what lets a hundred thousand queries a second scale by adding
machines. Personalised results, if the product wants them, are a small
per-user overlay merged on top of the ten, not a rebuild of the tree.

If the top-ten lists are too big to hold, the fallback is a small heap per node
computed at build time over the subtree.
```

**Why this answer works, part by part.**

**It starts with one query and a budget.** "A few milliseconds, so it cannot
touch a database" is a rejection with a reason attached, in the first two
sentences. Interviewers score the rejections you can justify at least as highly
as the choices you make.

**It names the structure and immediately says what it beat.** The trie is the
expected answer, and the hash-map comparison is what shows the choice was made
rather than recalled. Two clauses, one alternative, one reason.

**It separates finding from ranking, out loud.** "Finding the candidates is the
easy half" is the sentence that most first answers are missing entirely. Once
it is said, the rest of the paragraph has an obvious job to do.

**It moves the expensive work off the query path.** Precomputing the top ten at
each node converts a per-query sort into a per-build one. That is the central
move in most read-heavy designs, and being able to name it as a move — rather
than arriving at it by accident — generalises far beyond autocomplete.

**It states the cost of its own choice.** Ten pointers per node, and it says so
before being asked. An answer that volunteers its own price is much harder to
attack than one that presents a design as free.

**It answers the write path without being prompted.** Immutable, built offline,
swapped atomically. That single decision is what makes the scaling story true —
independent read-only replicas — so it belongs in the answer rather than in the
follow-up.

**It leaves a thread for the interviewer to pull.** The last line offers the
heap fallback in one sentence. Ending with a named alternative invites the
conversation to continue on ground you have already thought about.

## Download and run

There is no file to download, and no program to run. The deliverable is the
note and your own reading afterwards.

What you can run is the check that it is finished and committed:

```bash
wc -w system-design/notes-week-05.md
git add system-design/notes-week-05.md
git commit -m "Add week 5 system design note: autocomplete at scale"
```

## Common bugs to catch

- **The answer is a list of technologies.** A stack is not a design. If your
  note names four products and never follows a single query from one end to the
  other, rewrite it around that query.

- **The ranking is never explained.** You described how to find every
  completion of `pyth` and then quietly assumed the best ten appear. This is the
  most common weakness on this prompt, and it is the first thing an interviewer
  will probe.

- **The hundred thousand QPS never appears in the reasoning.** If the answer
  would be identical at ten queries a second, the number was decoration. Say
  what it ruled out.

- **Writes are not mentioned.** Every structure in the answer is a read
  structure, and terms and scores change constantly. Even "it is rebuilt hourly
  and swapped" is a complete answer — silence is not.

- **You read first and wrote afterwards.** The note will be better and the
  exercise will have measured nothing. There is no fix except to use the next
  prompt properly.

- **The three additions are vague.** "Caching is important" is not an addition.
  "The article suggests keeping the last N queries per user in a small local
  cache, because repeat prefixes dominate" is.

- **The binary-search section is left blank.** It is the reason this prompt sits
  in this week. Two boundary searches over a sorted term list give you every
  completion of a prefix without a tree at all — write down what that costs
  before you decide it is worse.

## Under the hood

<details>
<summary>Under the hood — the binary search hiding in autocomplete, and what it trades</summary>

**Every completion of a prefix is a contiguous run in a sorted list.**

Sort the terms alphabetically and all the terms starting `pyth` sit together,
in one unbroken block — because sorting puts them there. So the block's start
is the first term that is at least `"pyth"`, and its end is the first term that
is at least `"pyth" + chr(0x10FFFF)` — or, more practically, the first term
that does not start with the prefix. Two boundary searches, exactly the two you
wrote in [Exercise 2](../exercises/exercise-02-scan-window.md), with strings in
place of minutes:

```python
import bisect

def completions(terms: list[str], prefix: str) -> tuple[int, int]:
    """Return the half-open slice bounds of every term starting with `prefix`."""
    start = bisect.bisect_left(terms, prefix)
    end = bisect.bisect_left(terms, prefix + "￿")
    return start, end
```

Python compares strings letter by letter, so all of Exercise 2's reasoning
carries over unchanged. `end - start` is the number of completions, and a miss
gives an empty slice at the insertion point.

**What that trades against the trie.**

| | Sorted list + two searches | Trie |
| --- | --- | --- |
| Prefix lookup | `O(log n)` string comparisons | `O(prefix length)` steps |
| Memory | the terms, once | a node per shared prefix, plus per-node data |
| Update | re-sort or insert into an array | patch one path |
| Top ten | still needs ranking | can be precomputed per node |
| Complexity to build | almost none | real |

The sorted list is dramatically simpler, its memory is tight and predictable,
and for a term list that fits in cache it can be faster in practice than
chasing pointers through a tree — a comparison is cheap and a cache miss is
not. What it does not give you is a natural place to hang the precomputed top
ten, because there are no prefix nodes to hang them on.

That is the real reason production systems reach for the trie: not the
lookup speed, which was never the bottleneck, but the **place to store the
ranking**. Being able to say that sentence in an interview is worth more than
naming either structure.

**Where else this shape appears.**

The same "sorted keys make a prefix a contiguous range" idea is what makes
range scans work in a B-tree index, what lets a key-value store answer
`scan(prefix)`, and what makes lexicographic key design matter so much in
those systems. It is one idea with a great many costumes, and you now have it
from two directions — a scan log in Exercise 2 and a term list here.

</details>

## Acceptance checklist

- [ ] `system-design/notes-week-05.md` exists in your portfolio repo and is
      committed.
- [ ] The first section was written before you read anything, and the file
      records both dates.
- [ ] It is about three hundred words and follows one query end to end.
- [ ] It names the prefix structure and says what that choice beat.
- [ ] It says explicitly how the best ten are chosen.
- [ ] It says what happens on an update.
- [ ] Three specific additions are listed, each naming its source.
- [ ] The binary-search section names the two boundary searches and what the
      sorted list trades away.

## Stretch

- **Write the sorted-list version as working code** against a real word list —
  the `completions` function above plus a ranking pass over the returned slice
  — and time it on ten thousand terms. Then say which of the two designs you
  would ship for a term list that size. Small `n` changes answers, and knowing
  that it does is a senior instinct.

- **Cost the memory.** For a million terms averaging twelve characters, work
  out roughly what the sorted list costs and what a trie with ten precomputed
  completions per node costs. You will not get the number exactly right; the
  point is to produce an estimate you can defend within a factor of two, which
  is what design interviews actually ask for.

- **Design the update path properly.** Terms arrive continuously and scores
  drift hourly. Sketch what changes if the product asks for new terms to appear
  within a minute rather than within an hour. The hourly-blob answer stops
  working, and what replaces it — a small live overlay merged over an immutable
  base — is a pattern worth knowing by name.

That is the homework. Take the [quiz](../quiz.md) if you have not, then ship
the [mini-project](../mini-project/README.md) — five binary-search write-ups
and a working toolkit.
