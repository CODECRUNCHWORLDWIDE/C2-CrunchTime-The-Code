# Homework Problem 5 — Counting the Top Queries

> **Topic:** the week's second system-design warm-up — a 300-word answer to "count the ten most frequent search queries in real time", written before you look anything up
> **Lecture:** [01 — Mental Models for Big-O](../lecture-notes/01-mental-models-for-big-o.md)
> **Difficulty:** the writing is short; resisting the urge to look it up first is the work
> **Target time:** 45 minutes
> **Why this one:** the design round asks you to reason about scale out loud, and the honest way to get good at it is to answer badly first, in writing, and then find out what you missed. This particular question is also this week's material at a different size — a frequency map is the right first answer, and every interesting part of the problem is what happens when the map no longer fits in memory.

<!-- no-runnable-file: the deliverable is a 300-word design answer written in your own words, plus your notes on one article read afterwards. A program cannot write either, and writing code here would replace the reasoning this problem exists to build. -->

## The Brief

Here is a jar of marbles and a question: which colour is commonest? Easy — tip
them out, sort them into piles, count the piles.

Now the jar is a firehose. Marbles arrive a hundred thousand a second, forever,
in a thousand colours you have never seen before, and you have one shelf that
holds a few thousand piles. You still have to answer the same question, and you
have to answer it *now*, not at the end, because there is no end.

That is real-time top-K, and it is one of the most-asked system design warm-ups
there is.

**The prompt:** *"How would you design a system that counts the ten most
frequent search queries in real time?"*

Write 300 words answering it. Then — and only then — go and read about it.

The rule that makes this exercise work: **do not look up a canonical answer
first.** Write what you would actually say in an interview today, with what you
currently know. That draft is the measurement. If you read first, you will
produce a summary of somebody else's design, learn very little, and have no idea
which parts you would have reached on your own.

You already know more than you think. This week gave you a frequency map — a
`dict` from query to count — and that genuinely is the right first answer. It is
`O(1)` average per query and `O(d)` space for `d` distinct queries. Say so.
Then the interesting question arrives on its own: *what happens when `d` is a
hundred million and the map does not fit in memory?* Everything worth
discussing lives there.

Some things to think about while you draft, none of which you have to resolve:

- What does "real time" mean here — this second, this minute, the last hour?
- Does the count reset, or is it forever? A rolling window is a different system
  from a running total.
- One machine or many? If many, the counts for one query are spread across all
  of them.
- How wrong is the answer allowed to be? Tenth place being wrong occasionally
  might be completely fine, and that permission buys you enormous savings.

## Starter

Create `system-design/notes-week-02.md` in your portfolio repo and paste this
in. Fill in the sections. Write the answer **before** you touch the reading
section.

```markdown
# System design warm-up 02 — Top 10 search queries in real time

**Prompt:** "How would you design a system that counts the ten most frequent
search queries in real time?"

## My answer, written cold

*Written before any reading. [today's date].*

[300 words. What you would say in an interview right now. Cover: what you
would build first, what "real time" means in your design, where it breaks
as traffic grows, and what you would give up to keep it working.]

## What I read afterwards

[Title and link of one free article, after searching something like
"top-K real-time frequency counting".]

## Three things I would add

1. [_]
2. [_]
3. [_]

## What I got right without reading

[One or two sentences. Be honest -- this is the measurement, and reporting
it accurately is the whole point of writing cold.]
```

Two notes before you start.

**Timebox the draft to twenty minutes.** It is a warm-up, not a design
document. Twenty minutes of writing, ten of reading, fifteen of notes.

**Ambiguity is the point, not a problem.** "Real time" is undefined on purpose,
and so is the scale. In a real interview you would ask; here, write down the
assumption you are making and carry on. Naming an assumption out loud is itself
a mark.

## Requirements

1. A file at `system-design/notes-week-02.md` in your portfolio repo.
2. The prompt is quoted at the top.
3. The cold answer is between 250 and 350 words and is dated.
4. The cold answer was written **before** any reading, and says so.
5. It names at least one explicit assumption — what "real time" means, or the
   scale you are designing for.
6. It says where the design breaks as traffic grows, not just what it does when
   it works.
7. It names at least one thing you would give up — exact accuracy, memory,
   freshness — and why that trade is acceptable.
8. One free article read afterwards, with its title and link recorded.
9. Three specific things you would add, each a sentence rather than a phrase.
10. An honest note on what you got right without reading.

## Constraints

- **250 to 350 words for the cold answer.** That is about two minutes spoken,
  which is the length of an opening answer before an interviewer starts asking
  questions. A design answer is a conversation, and your job in the first two
  minutes is to establish a shape they can push on, not to cover everything.

- **Do not read first.** This is the constraint that makes the whole exercise
  work, and it is the one that will feel wrong. If you read first you will write
  a competent summary of somebody else's design and learn nothing about your own
  reasoning. The gap between your draft and the article *is* the lesson; reading
  first closes it for free and leaves you with a false sense of having
  understood.

- **One article, not five.** You are calibrating, not researching. One good
  free article and three specific additions beats an afternoon of reading that
  produces a paragraph of vocabulary you cannot use.

- **Name at least one thing you would give up.** Every real answer to this
  question trades something. A design that claims exact counts, unbounded query
  variety, low memory and instant answers all at once is a design that has not
  been thought about. Saying "tenth place can be wrong sometimes, and here is
  why that is acceptable" is the mark.

- **Your own words.** Nothing copied from the article, including its phrasing.
  If a term is worth using — "sketch", "heavy hitters", "sliding window" —
  define it in your own sentence, which is also how you find out whether you
  understood it.

## Expected output

There is no program here, so the output is the note. This is what a finished one
looks like — yours will differ, and the differences are the interesting part:

```text
# System design warm-up 02 -- Top 10 search queries in real time

**Prompt:** "How would you design a system that counts the ten most frequent
search queries in real time?"

## My answer, written cold

*Written before any reading. 2026-02-27.*

First I would pin down "real time". I will assume the last five minutes,
refreshed every few seconds, rather than an all-time total -- a trending
list, not a leaderboard.

The simplest thing that works: one process, a dict from query string to a
count, and a loop that reads queries off a stream and increments. Every
query is O(1) average. To answer "top ten" I would not sort the dict, since
that is O(d log d) on however many distinct queries there are; I would keep
a min-heap of ten entries and compare each updated count against its
smallest, which is O(log 10) per update -- effectively constant.

Where it breaks is memory. Distinct queries are close to unbounded --
typos, timestamps pasted into the box, whole sentences -- so the dict grows
without limit and eventually will not fit. The five-minute window helps: I
would keep counts in per-minute buckets and drop buckets older than five,
so the map only ever holds what recent traffic contains.

It also breaks on one machine. Real traffic needs many, and then one
query's count is spread across all of them. I would shard by hashing the
query text, so every occurrence of one query lands on the same machine and
each machine's top ten is exact for its own shard, then merge the shards'
candidates.

What I would give up is exactness at the bottom of the list. Merging shard
top-tens can miss a query that was eleventh everywhere and first overall. I
would take a slightly wrong tenth place over a design that has to count
everything exactly.

## What I read afterwards

"Heavy Hitters and the Count-Min Sketch" -- [link]

## Three things I would add

1. Count-min sketch: a fixed-size table of counters, several hash functions
   per query, and you read a count as the smallest of the cells it hashes
   to. Fixed memory regardless of how many distinct queries arrive, and it
   over-counts rather than under-counts, which is the safe direction for
   "find the frequent ones".
2. The name for this problem is "heavy hitters", and knowing the term makes
   the literature findable.
3. Sharding by query hash is right, but merging top-tens is not -- each
   shard should send its top *K times some factor* so the merge has enough
   candidates to be right more often.

## What I got right without reading

The dict-plus-heap core and the per-minute bucketing were both right, and I
reached the sharding idea on my own. What I did not have was any concept of
trading exactness for *fixed* memory -- I assumed memory had to grow with
distinct queries and only argued about how fast.
```

Read what makes that work. It names its assumption in the first sentence. It
starts with the simplest thing that works and then attacks it. It says where
memory breaks and where the single machine breaks, separately. It names what it
gives up. And the honest note at the end reports a real gap rather than
congratulating itself.

## Steps

1. Set a twenty-minute timer. Do not open a browser.
2. Write the assumption sentence first: what does "real time" mean in your
   design? Everything else follows from it.
3. Describe the simplest thing that works. A dict and a loop is a completely
   respectable opening, and starting simple then attacking your own design is
   the standard shape of a good design answer.
4. Now attack it. Where does memory go? What happens on one machine when traffic
   is a hundred thousand a second? What happens when you need many machines?
5. Name one thing you would give up and say why that is acceptable.
6. Stop at 350 words even if you were not finished. Being cut off is realistic.
7. *Now* search — "top-K real-time frequency counting" or "heavy hitters
   streaming" — and read one free article.
8. Write your three additions, each as a full sentence you could say out loud.
   "Count-min sketch" is a phrase; the sentence explaining what it buys you is
   the note.
9. Write the honest note on what you got right. Do not inflate it and do not
   deflate it; the value of this exercise is entirely in that number being
   accurate.

## The Solution

The finished note is the block under **Expected output** above. Yours will reach
different conclusions, and that is expected — what transfers is the five moves
below.

**Start with the simplest thing that works, then attack it yourself.** A design
answer that opens with sharding and sketches sounds rehearsed and gives the
interviewer nothing to push on. Opening with "a dict and a loop, and here is
exactly where that stops working" shows the reasoning, and the attack is the
part they are listening to. This is the same instinct as *Assess options* in
FRAME: describe the simple approach, then the better ones and their tradeoffs.

**Name the assumption in the first sentence.** "Real time" could mean the last
five minutes or all time since launch, and those are genuinely different
systems — one needs expiry and one does not. In a real interview you would ask.
On paper, write it down. An unstated assumption is the most common way a design
answer and its listener end up discussing different problems for ten minutes.

**Separate the two failure modes, because they have different fixes.** Memory
growth is about *distinct queries* and is fixed by windowing or by sketching.
Throughput is about *queries per second* and is fixed by sharding. Candidates
who blur them tend to propose sharding for a memory problem, which does help but
for a reason they cannot articulate. Say which is which.

**The heap detail is where this week's material shows up.** "Top ten" does not
need a sort. Sorting the map is `O(d log d)` on however many distinct queries you
have, and it throws away all but ten of them. A ten-element min-heap costs
`O(log 10)` per update, which is a constant, and it is the same move as
Exercise 1's `max` versus `sorted(...)[0]`: do not order everything to read one
end. You do not need to have met heaps yet — Week 8 is where they get built —
but noticing that sorting is the wrong shape is available to you now.

**The thing you give up is the answer, not a concession.** Every viable design
here trades something: exactness at the bottom of the list, freshness, or
memory. A candidate who names the trade and defends it is doing the job. A
candidate who claims exact counts over unbounded distinct queries in bounded
memory has described something that cannot exist, and an interviewer will
usually just ask "how much memory?" and wait.

**And on writing cold.** The honest note at the end is the only part of this
exercise that measures anything. Most people find they had the core right and
were missing one specific idea — usually the one that trades exactness for
*fixed* memory rather than growing memory. That is a good outcome and a useful
thing to know about yourself: your instincts are sound and your vocabulary is
short, which is a much easier gap to close than the other way round.

## Download and run

There is no file to download. The deliverable is a design answer in your own
words and your notes on one article.

The check that matters is a speaking test. Close the file and say the answer out
loud from memory, timed:

```bash
# a phone voice memo is fine
```

Two minutes. Then ask yourself three questions. Did you state the assumption
before designing anything? Did you say where it breaks, or only what it does?
Did you name what you gave up?

If you want a second check, hand the note to somebody who has not read it and
ask them what the system would do when a million distinct queries arrive in one
minute. If they can answer from your note, the note is specific enough.

## Common bugs to catch

- **You read first.** The single failure that makes this exercise worthless. You
  will produce a fluent summary of somebody else's design and have no idea which
  parts you would have reached alone. If it happened, say so in the file and do
  the next warm-up cold — the note is only useful if it is true.

- **No assumption stated.** The answer describes a system without ever saying
  what "real time" means, and so it is unclear whether counts expire. Every
  memory argument downstream depends on that.

- **Describing only the happy path.** "I'd use a hash map to count and then take
  the top ten" is where the answer *starts*. If your 300 words never say where
  it stops working, you have described a program rather than a system.

- **Nothing given up.** Exact counts, unbounded distinct queries, bounded
  memory, instant answers — pick three. A design that claims all four has not
  been examined.

- **Sorting the map to get the top ten.** `O(d log d)` to read ten values, and
  it is the same instinct Exercise 1 warned about. A small heap, or a running
  top-ten kept by comparison, is the shape.

- **Additions that are phrases, not sentences.** "Count-min sketch" recorded as
  three words is vocabulary you will not be able to use under pressure. The
  sentence that says what it buys and what it costs is the note.

- **An inflated "what I got right".** The note is a measurement of your own
  reasoning, and a measurement you fudge is worse than no measurement — you will
  carry a false picture of your own gaps into the next four warm-ups.

- **Reading five articles.** You are calibrating, not researching. One article,
  three additions, and back to the drills.

## Under the hood

<details>
<summary>Under the hood — why exact top-K in bounded memory is impossible, and what a sketch trades for it</summary>

**The impossibility, stated plainly.** Suppose you want the exact top-K over a
stream with an unbounded number of distinct items, using memory that does not
grow. You cannot have it, and the reason is short: any item you have stopped
tracking might be about to arrive a million times, and any item you never
started tracking might already have arrived a million times. To be exactly
right you need a counter for anything that could still turn out to matter, and
in an unbounded stream that is everything.

So every real system gives up one of three things: exactness, bounded memory, or
unbounded distinct items. Windowing gives up the third — it only counts what is
recent, which bounds the distinct items in practice. Sketching gives up the
first. Knowing that the choice is forced is what turns a design answer from a
list of techniques into an argument.

**What a count-min sketch actually does.** Imagine a fixed grid of counters, say
four rows of a few thousand columns. Each row has its own hash function. To
record a query, hash it once per row and increment the cell it lands in. To read
its count, hash it the same way and take the **smallest** of the four cells.

Collisions mean other queries have been added into those cells too, so every
cell is an over-count. Taking the minimum picks the cell that suffered least
collision, so the estimate is never *under* — you can only over-report a query's
frequency, never under-report it. That is the safe direction when hunting
frequent items: you might promote something that does not deserve it, but you
will never miss something genuinely huge.

The memory is a constant you chose, regardless of whether ten distinct queries
arrive or ten billion. The accuracy degrades gracefully as the stream gets more
varied, rather than the whole thing falling over. And crucially, the *frequent*
items are the ones estimated best, because their true count dwarfs the collision
noise — which is exactly the regime you care about.

This is genuinely out of scope for Week 2 and it is worth knowing the shape of,
because it is the answer to "but what if the map does not fit", which is the
follow-up this question always has.

**Why sharding by hash and not round-robin.** If you spread queries across
machines arbitrarily, one query's occurrences land everywhere and no machine
knows its true count. Hash the query text and every occurrence of `"weather"`
goes to the same machine, so that machine's count for it is exact. The merge
then only has to combine per-machine candidates.

The subtlety in the worked example is real: merging each shard's *top ten* can
miss a query that was eleventh on every shard and first overall. The standard
fix is to have each shard send more candidates than you need — its top `K` times
some factor — so the merge has enough to work with. It makes the answer more
often right rather than always right, which is the same trade in a different
place.

**Where this connects back to the week.** The one-machine core of this system is
Exercise 2's `Counter` and Challenge 1's frequency map, at a size where `O(d)`
space stops being an abstraction and becomes a bill. Every interesting design
decision here is a consequence of the space bound you have been asked to say out
loud on every page this week. That is the point of the warm-up: the sentence
"`O(n)` space, where `n` is the number of distinct items" is where a system
design begins.

</details>

## Acceptance checklist

- [ ] `system-design/notes-week-02.md` exists in your portfolio repo.
- [ ] The prompt is quoted at the top.
- [ ] The cold answer is dated and says it was written before any reading.
- [ ] It is between 250 and 350 words.
- [ ] It names an explicit assumption about what "real time" means.
- [ ] It starts with the simplest thing that works.
- [ ] It says where the design breaks on memory **and** where it breaks on
      throughput, as two separate points.
- [ ] It names at least one thing you would give up, with a reason.
- [ ] It does not sort the map to find the top ten.
- [ ] One article is recorded with its title and link.
- [ ] Three additions, each a full sentence.
- [ ] The "what I got right" note is honest.
- [ ] Committed with a message like `Add system design warm-up 02: top queries`.

## Stretch

- **Answer the same prompt again in a week, without re-reading your note.** Then
  compare the two. The second answer is usually noticeably better, and seeing
  that is more motivating than being told it would be. It also tells you which
  of your three additions actually stuck and which were vocabulary.

- **Design the *one-machine* version properly, in code.** A dict of counts, a
  deque of per-minute buckets, and a function that returns the current top ten.
  It is about forty lines and it is entirely within what this week taught you.
  Building the simple version makes the arguments about the hard version much
  more concrete, and it gives you something to point at when an interviewer asks
  what you would build first.

- **Work out how much memory the naive version needs at a realistic scale.**
  Assume ten million distinct queries in five minutes, an average query of
  twenty characters, and a Python dict entry. Get to a number in gigabytes. That
  number is the entire argument for everything else in this problem, and having
  computed it yourself is the difference between "it might not fit" and "it needs
  about this much, on a box that has that much".

Next: [Homework Problem 6 — Week 2 Reflection](./problem-06-week-02-reflection.md).
