# Lecture 1 — What Interviewers Actually Score

> **Duration:** ~2 hours.
> **Outcome:** You can name the four dimensions of an interview score, prioritize them correctly, and explain why "passed the test cases" is *one quarter* of the rubric, not all of it.

If you remember nothing else this week, remember this: **the interviewer is grading four things, not one.**

Most candidates think there's one thing being graded: "did I solve the problem?" That's wrong, and treating it as right is the single biggest reason promising candidates fail. We'll explain what's actually happening, then build the UMPIRE Method around it in Lecture 2.

---

## 1. The four dimensions

Pull up any large-company interview rubric (Google's, Meta's, Stripe's — leaked versions circulate openly). They all look approximately like this:

| Dimension | What it measures | Weight (typical) |
|-----------|------------------|:-:|
| **Problem-solving** | Did you arrive at a correct approach? Did you reach it through structured reasoning or guessing? | ~30% |
| **Coding** | Is the code clean, readable, idiomatic? Does it compile and run? Does it handle edge cases? | ~30% |
| **Communication** | Did you think out loud? Did you state assumptions? Did you respond to hints gracefully? | ~25% |
| **Engineering judgment** | Did you choose appropriate data structures? Reason about complexity? Test your code before submitting? | ~15% |

(Exact weights vary by company and level. Senior interviews shift more toward communication and judgment. Junior interviews lean harder on coding and problem-solving. The four dimensions stay.)

**The implication:** even if you arrive at the correct working solution, **you can fail** by:

- Silently typing while the interviewer has no idea what you're doing (kills *communication*).
- Picking a hash map without justifying why over a list (hurts *judgment*).
- Producing code with three nested ternaries that "works" but no one can read (kills *coding*).
- Solving the problem but never tracing it on a test input (hurts *judgment*).

And the inverse: you can **partially pass** an interview where you didn't quite finish the code, if you:

- Verbally walked through the right approach.
- Wrote clean, well-named code as far as you got.
- Identified the correct complexity bounds.
- Caught your own bug before the interviewer pointed it out.

I have personally hired candidates whose final code did not compile. They got the offer because they were *demonstrably reasoning* in real time, made the right structural choices, and behaved like a colleague.

---

## 2. The "silent grinder" failure mode

The most common interview disaster looks like this:

> **Candidate:** [reads problem silently for 90 seconds]
>
> **Candidate:** [starts typing]
>
> **Candidate:** [3 minutes of silent typing, occasional `Ctrl-Z`]
>
> **Interviewer:** What are you doing there?
>
> **Candidate:** Just a moment, I'm thinking.
>
> **Candidate:** [2 more minutes of silent typing]
>
> **Candidate:** OK done. The function returns `[1, 2, 3]`.
>
> **Interviewer:** Why does it return `[1, 2, 3]`?

Even if the answer is correct, the interview has **already failed** on communication and judgment. The interviewer cannot help the candidate (because they don't know what direction to nudge), cannot evaluate the reasoning (because none was shown), and has watched a black box for 5 minutes. They will write "failed to communicate" on the feedback form.

UMPIRE prevents this. Every step of UMPIRE *requires* you to speak.

---

## 3. The "I just did Leetcode 200 times" failure mode

The opposite failure: candidates who have *memorized* solutions to the popular problems. The interview goes:

> **Interviewer:** Given two sorted arrays, return the median.
>
> **Candidate:** Oh, I've done this. [types fast for 90 seconds, produces a binary-search-on-the-smaller-array solution]
>
> **Candidate:** Done. O(log min(m,n)).
>
> **Interviewer:** Can you walk me through *why* the binary-search-on-the-smaller-array works?
>
> **Candidate:** Uh… because it's the optimal solution. The classic approach.
>
> **Interviewer:** What if we changed the constraint — what if the arrays aren't sorted?
>
> **Candidate:** [silence]

This candidate produced the optimal solution and **failed the interview** because they could not reason about their own code. They demonstrated memorization, not problem-solving.

The fix is not to study less. The fix is to study with *understanding*, using UMPIRE. Every problem you write up forces you to articulate the *why*, not just the *what*.

---

## 4. What the interviewer is doing

It helps to know what's happening on the other side of the table.

The interviewer is:

1. **Listening for structured thinking.** They're checking that your steps follow from each other. They're looking for "I noticed X, which means Y, so I'll try Z" structures.
2. **Probing your assumptions.** When they ask "what about negative numbers?" they're testing whether you'd considered edge cases yourself or only after prompting.
3. **Measuring your code-review readiness.** Would they want to read your PR? Would they trust your naming?
4. **Calibrating against past candidates.** Often they have a mental ranking: this candidate is between candidate X (who got a hire) and candidate Y (who got a no-hire).
5. **Looking for collaboration signals.** When given a hint, do you incorporate it gracefully or get flustered?

Notice that **most of these are observable only if you talk.** Silent solving denies the interviewer the data they need to grade you favorably.

---

## 5. Translating to four habits

The four dimensions translate to four concrete habits we'll drill all week:

| Dimension | Drill |
|-----------|-------|
| Problem-solving | **The U-M-P steps of UMPIRE.** Always before code. |
| Coding | **Write code one English sentence at a time.** "First I'll initialize two pointers, one at each end…" then write that line. |
| Communication | **Every action narrated.** No silent typing for more than 10 seconds. |
| Engineering judgment | **The R and E steps of UMPIRE.** Trace + complexity, every time. |

UMPIRE is not arbitrary. It is structured around what the rubric actually measures.

---

## 6. The "interviewer is your collaborator" reframe

Many candidates come in adversarial — "the interviewer is trying to fail me." This is wrong both factually and tactically.

**Factually wrong:** in most companies, the interviewer is the engineer the candidate would *work with*. They are looking for a colleague. Most interviewers feel disappointed when a strong candidate fails an interview — it means they have to interview more people.

**Tactically wrong:** the adversarial frame makes you defensive. You don't ask clarifying questions because you're afraid of looking dumb. You don't ask for hints because you don't want to lose points. You don't push back on the interviewer's hint when you think it's wrong because you don't want to seem combative.

The correct frame: **the interviewer is the most senior colleague you've ever had, and they're helping you scope a small project in 45 minutes.** In that frame:

- Clarifying questions are *expected*. Real engineers ask them constantly.
- Asking "would it be okay if I assumed input is non-empty?" is *what real engineers do*.
- Pushing back on a hint with "I want to try X first because Y" *demonstrates judgment* — the senior colleague will let you try if your reasoning is sound, and respect you for it.

You don't have to like your interviewer. But model them as your collaborator. Your output will be measurably better.

---

## 7. A worked vignette

Same problem, two candidates. Both arrive at the same answer. One gets the offer.

**Problem:** Given a sorted array of integers and a target, return the indices of two numbers that add to the target.

### Candidate A (silent solver)

> [reads silently, 60 seconds]
> [types]
>
> ```python
> def two_sum(arr, target):
>     l, r = 0, len(arr) - 1
>     while l < r:
>         s = arr[l] + arr[r]
>         if s == target: return [l, r]
>         if s < target: l += 1
>         else: r -= 1
>     return []
> ```
>
> Done. Returns the indices.
>
> Interviewer: "Can you walk me through how you arrived at this?"
> Candidate A: "Two pointers."

Score:

- Problem-solving: ✓ (arrived correctly)
- Coding: ✓ (clean enough)
- Communication: ✗ (silent for 60s, terse answer)
- Engineering judgment: ✗ (no complexity discussed, no edge cases mentioned)

Net: **borderline hire / leaning no-hire** depending on company.

### Candidate B (UMPIRE)

> Reading aloud: "OK, given a sorted array of integers and a target. I want to return the indices of two numbers that add up to the target.
>
> A couple of clarifying questions: should I assume there's always exactly one solution, or could there be no solution, or multiple? And: can I use the same element twice?"
>
> [Interviewer: "Exactly one solution exists. You can't use the same element twice."]
>
> "Great. So I'll work with `arr = [2, 7, 11, 15]`, `target = 9`. I should return `[0, 1]` because `arr[0] + arr[1] == 9`.
>
> Now — this is a sorted array, two indices summing to a target. That immediately reminds me of the **two-pointer pattern** — left at start, right at end, and we move based on whether our sum is too low or too high.
>
> My plan: initialize `left = 0`, `right = len - 1`. Loop while `left < right`. Compute the sum. If it equals target, return. If less than target, move left forward (we need a bigger sum). If more, move right backward. If the loop exits, return an empty list — but the prompt says one solution exists, so we should never hit that case.
>
> Let me code it up." [types the same code as Candidate A, but narrating each line]
>
> "Let me trace this on `[2, 7, 11, 15], target=9`. l=0, r=3, sum=2+15=17, too big, r=2. l=0, r=2, sum=2+11=13, too big, r=1. l=0, r=1, sum=2+7=9, match, return `[0, 1]`. Good.
>
> Complexity: each iteration moves one pointer at least one step toward the other. So at most n-1 iterations. **Time O(n), space O(1).**
>
> Edge cases worth checking: array of length 2, both elements summing to target — works because l=0, r=1, sum matches. What about an array of length 1 — well, can we even form a pair? No. So we should probably return early. Let me add that check.
> [adds `if len(arr) < 2: return []`]
>
> Anything else you'd like me to consider?"

Score:

- Problem-solving: ✓✓ (explicit, structured)
- Coding: ✓ (same code, but each line was reasoned)
- Communication: ✓✓ (continuous narration, asked clarifying questions, asked for feedback)
- Engineering judgment: ✓✓ (complexity discussed, edge cases caught, traced before declaring done)

Net: **strong hire.** Same code; different outcome.

---

## 8. Self-check

You should be able to answer all of these without looking back:

1. What are the four dimensions an interviewer is grading?
2. Why is "silently solving the problem correctly" often not enough?
3. Why is it bad to have a memorized solution to a problem the interviewer asks?
4. Name three concrete habits that map to the *Communication* dimension.
5. Reframe the interviewer in non-adversarial terms — what role are they playing?

If those are clear, move on to Lecture 2.

---

## Further reading

- **"What does Google look for in a candidate?"** — leaked rubric discussions on r/cscareerquestions and on engineer-authored blogs. Search "Google interview rubric."
- **"How to interview at Stripe"** — Patrick McKenzie's free blog post: <https://www.kalzumeus.com/>
- **"On being a senior engineer"** — John Allspaw (free): <https://www.kitchensoap.com/2012/10/25/on-being-a-senior-engineer/>

Next: [Lecture 2 — The UMPIRE Method](./02-the-umpire-method.md).
