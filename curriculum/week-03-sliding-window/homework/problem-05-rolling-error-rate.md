# Problem 5 — The Rolling Error Rate

> **Topic:** the same window, moved from positions in a list to seconds on a clock — the bridge from the algorithm to the system-design idea that shares its name
> **Lecture:** [01 — The Sliding Window Pattern](../lecture-notes/01-the-sliding-window-pattern.md)
> **Difficulty:** Medium
> **Target time:** 45 minutes
> **Why this one:** "sliding window" means two different things in an interview, and this is where they meet. The algorithms half is what you have drilled all week. The systems half — a window over *time*, fed by a live stream — is what gets asked in a design round. They are the same two rules, and building the second one yourself is much more convincing than reading about it.

## The Brief

Every algorithm this week slid a window over a **list**. The window's left and
right edges were positions, the data sat still, and you moved past it.

Production monitoring asks a question with the same shape and a different axis:

> *"What fraction of the requests in the last sixty seconds failed?"*

The window is still two edges and a running total. What has changed is that the
edges are **times**, the data arrives while you are watching, and you never get
to see the whole list — there is no whole list. Requests keep coming.

The brute-force version is exactly as tempting and exactly as wrong as it was
on Exercise 1. Keep every request in a list, and each time somebody asks for
the rate, walk backwards through the list adding up the ones inside the last
sixty seconds. It works, and on a service doing forty requests a second it
means walking 2,400 entries to answer a question you are asked every second.
That is Exercise 1's rescan on a different axis.

The fix is the same fix. Keep a running total, add on the right, subtract on
the left.

The one new idea is **bucketing**. Requests do not arrive at tidy moments, and
storing one entry per request is more state than you need. So group them by
whole second: one bucket per second, each holding how many requests that second
served and how many failed. Now the window holds at most sixty buckets whatever
the traffic, and the "drop what has fallen out of the window" step is popping
buckets off the front until the oldest is inside the horizon.

That gives you the whole design:

- a **queue** of buckets, oldest at the front, newest at the back;
- two **running integers** — total requests and total failures in the window;
- **add** on the right when a second's traffic arrives;
- **drop** from the left while the front bucket is older than the horizon;
- **answer** by dividing two integers you already have.

**One thing the algorithm cannot tell you.** A window holding one request that
failed reports a hundred per cent failure rate. That is arithmetically correct
and operationally useless — it would page somebody every quiet night. So the
alert needs a second condition: the window must hold at least a minimum number
of requests before its rate is trusted at all. That is not a hack; it is the
difference between a statistic and a measurement, and it is the sort of
judgement a design round is actually looking for.

**Your job.** Build the rolling window, and use it to find the first second at
which a scripted five-minute traffic stream crosses a one per cent failure
rate.

## Starter

Create `problem-05-rolling-error-rate.py` and paste this in. Fill in every
`TODO`.

```python
"""problem-05-rolling-error-rate.py — a window over time, not over a list.

Keep a failure rate over the most recent N seconds of traffic, and find the
first moment it crosses a threshold.

Fill in every TODO, then run the file. The self-checks at the bottom print
"All checks passed." when the module is correct.
"""

from collections import deque


class RollingRate:
    """A failure rate over the most recent `horizon` seconds of traffic."""

    def __init__(self, horizon: int) -> None:
        """Create an empty window.

        Args:
            horizon: How many seconds of traffic the window covers.
        """
        # TODO: the horizon, a deque of buckets, and two running integers.
        ...

    def record(self, second: int, requests: int, failures: int) -> None:
        """Fold one second of traffic into the window.

        Args:
            second: The whole second the traffic belongs to, non-decreasing
                across calls.
            requests: How many requests that second served.
            failures: How many of them failed.
        """
        # TODO: append the bucket, add to both totals, then evict what has
        #       fallen out. Adding before evicting is what keeps the window
        #       correct when a big gap in traffic arrives.
        ...

    def _drop_stale(self, now: int) -> None:
        """Remove buckets that have fallen out of the horizon.

        Args:
            now: The current second.
        """
        # TODO: while the oldest bucket is too old, pop it and SUBTRACT its
        #       counts. A while, not an if — a gap can strand several at once.
        ...

    def rate(self) -> float:
        """Return the failure rate over the window, as a fraction of one.

        Returns:
            failures / requests, or 0.0 when the window saw no requests.
        """
        # TODO: guard the division, then divide.
        ...


def first_alert(
    traffic: list[tuple[int, int, int]],
    horizon: int = 60,
    threshold: float = 0.01,
    minimum_requests: int = 100,
) -> tuple[int, float] | None:
    """Return the first second at which the rolling failure rate trips.

    Args:
        traffic: (second, requests, failures) triples, in time order.
        horizon: How many seconds the window covers.
        threshold: The failure rate that must be exceeded, as a fraction.
        minimum_requests: How many requests the window needs before the rate
            is trusted. Without this, one failed request out of one is a
            hundred per cent and every quiet minute pages somebody.

    Returns:
        (second, rate) for the first second whose window is over threshold, or
        None when the window never trips.
    """
    # TODO: one window, fed in order. After each second, check BOTH conditions.
    ...


def scripted_traffic() -> list[tuple[int, int, int]]:
    """Return five minutes of made-up but entirely predictable traffic.

    Forty requests a second throughout. For the first three minutes one
    request fails every twenty-five seconds — background noise, well under
    one per cent. From second 180 a bad deploy fails two requests a second,
    which is five per cent, and the rolling window has to notice.

    Returns:
        (second, requests, failures) triples for seconds 0 to 299.
    """
    # TODO: build 300 triples following the docstring exactly. No randomness —
    #       the whole point is that the answer is the same every run.
    ...


# ---- Self-check ----
if __name__ == "__main__":
    traffic = scripted_traffic()
    alert = first_alert(traffic)
    second, rate = alert

    print("five minutes of traffic, 40 requests a second")
    print("  bad deploy starts at second 180, failing 2 requests a second")
    print(f"  first alert at second {second}, rolling rate {rate * 100:.2f}%")
    print(f"  that is {second - 180} seconds after the deploy went out")
    print()

    quiet = RollingRate(60)
    for tick in range(120):
        quiet.record(tick, 40, 0)
    print(f"a clean window holds {quiet.requests} requests and reports {quiet.rate() * 100:.2f}%")
    print(f"buckets kept in memory: {len(quiet.buckets)}, not {120}")
    print()

    assert alert == (191, 26 / 2400)
    assert first_alert(traffic[:180]) is None
    assert first_alert([]) is None
    # One failure out of one request is 100%, and must not page anyone.
    assert first_alert([(0, 1, 1)]) is None
    # The same burst with the minimum lowered does trip, immediately.
    assert first_alert([(0, 1, 1)], minimum_requests=1) == (0, 1.0)

    # The window really only ever holds `horizon` buckets.
    assert len(quiet.buckets) == 60
    assert quiet.requests == 60 * 40
    assert quiet.rate() == 0.0

    # Running totals agree with a from-scratch count of the buckets kept.
    window = RollingRate(60)
    for row in traffic[:250]:
        window.record(*row)
    assert window.requests == sum(bucket[1] for bucket in window.buckets)
    assert window.failures == sum(bucket[2] for bucket in window.buckets)

    print("All checks passed.")
```

Two things you need before you start.

**`deque`.** A list you can add to and remove from at *both* ends cheaply.
Removing from the front of a normal Python list is `O(n)`, because everything
behind it shifts down — do that once a second on a long list and you have
re-invented the rescan. `collections.deque` makes `popleft()` `O(1)`, which is
the whole reason it is the right container here.

**Horizon.** How far back the window looks. Sixty seconds here. A bucket is
inside the horizon when its second is greater than `now - horizon`, which is
sixty buckets: `now`, and the fifty-nine before it.

**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C2-CrunchTime-The-Code/curriculum/week-03-sliding-window/homework/problem-05-rolling-error-rate.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `RollingRate` keeps a `deque` of buckets plus two running integers.
2. `record` adds to the totals and then evicts, in that order.
3. `_drop_stale` is a `while` loop and subtracts each evicted bucket's counts.
4. `rate()` returns `0.0` on an empty window rather than raising.
5. The window never holds more than `horizon` buckets.
6. `first_alert` requires **both** conditions — enough requests and a rate over
   threshold — before it reports.
7. `first_alert` returns `(second, rate)` or `None`.
8. `scripted_traffic` is deterministic. No randomness anywhere.
9. Every function and method keeps its type hints and its docstring.

## Constraints

- **Traffic arrives with non-decreasing seconds.** Real event streams can
  deliver out of order, and handling that properly needs either a reordering
  buffer or a tolerance for late data — a genuinely hard problem that this page
  deliberately excludes. Stating the assumption is the point: an assumption
  named in the brief is a design decision, and the same assumption left
  unnamed is a bug waiting for production traffic.

- **One bucket per whole second, at most 3,600 seconds of horizon.** Bucketing
  is what bounds the memory: without it the window holds one entry per request,
  which on a busy service is unbounded in exactly the wrong dimension. With it,
  memory is `O(horizon)` regardless of traffic — sixty small lists whether the
  service does forty requests a second or forty thousand.

- **`minimum_requests` defaults to 100, and the default matters.** A rate
  computed over three requests is noise, and an alert that fires on noise gets
  muted, and a muted alert is worse than no alert at all. The number is a
  judgement call that depends on the service; what is not a judgement call is
  that *some* such floor has to exist.

- **The threshold is exceeded strictly.** A rate landing exactly on one per
  cent does not trip. That is an arbitrary choice, it is written down, and
  writing it down is the difference between a specification and a habit — the
  scripted stream crosses through exactly 1.00% on its way up, so the choice is
  observable in the output rather than theoretical.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2:

```text
$ python problem-05-rolling-error-rate.py
five minutes of traffic, 40 requests a second
  bad deploy starts at second 180, failing 2 requests a second
  first alert at second 191, rolling rate 1.08%
  that is 11 seconds after the deploy went out

a clean window holds 2400 requests and reports 0.00%
buckets kept in memory: 60, not 120

All checks passed.
```

Eleven seconds of detection delay is the interesting number, and it is not a
flaw — it is the horizon doing its job. The window is averaging over sixty
seconds, so a burst starting at second 180 has to accumulate enough failures to
drag the whole minute's average over one per cent. At two failures a second
against 2,400 requests a minute, that takes until second 191.

That trade is the entire design conversation. A shorter horizon detects faster
and fires on transient blips; a longer one is calm and slow. Being able to say
which you want, and why, is what the question is for.

The second block is the memory point. Two minutes of traffic went in and sixty
buckets came out — the other sixty were dropped as they aged past the horizon.

## Steps

1. Create the file, paste the starter, and run it. Correct starting point.
2. Write `__init__`. Four attributes and nothing clever.
3. Write `record`: append, add to both totals, then call `_drop_stale`. Add
   before you evict — the new bucket defines what "now" means.
4. Write `_drop_stale` as a `while`, not an `if`. If traffic goes quiet for
   five minutes and then resumes, several buckets fall out at once.
5. Get the eviction condition right: `self.buckets[0][0] <= now - self.horizon`.
   Draw it on paper for `horizon = 3` and `now = 10` before you type it — you
   want seconds 8, 9 and 10 kept, and 7 dropped.
6. Write `rate()` with its zero guard. Dividing by zero on an empty window is
   the first thing that will happen to you otherwise.
7. Write `first_alert`. Both conditions, in one `if`, checked after each
   `record`.
8. Write `scripted_traffic` exactly as its docstring says. Determinism is a
   requirement: a test that sometimes passes is not a test.
9. Run it, then go back and change the horizon to 10 and to 300, and watch the
   detection second move. Predict the direction before you run it.

## The Solution

```python
"""problem-05-rolling-error-rate-solution.py — a window over time, not over a list.

The algorithmic sliding window moves over positions in a list. A production
alerting system moves a window over the clock: "what fraction of the last
sixty seconds of requests failed?" Same idea, different axis, and the same two
rules — add on the right, drop on the left, keep the totals rather than
recounting.

The state here is a queue of one-second buckets plus two running integers. A
bucket that falls out of the sixty-second horizon is popped and subtracted, so
answering "what is the rate right now" is a division, not a scan.

The self-checks are the starter's, unchanged. When they all pass the file
prints "All checks passed."
"""

from collections import deque


class RollingRate:
    """A failure rate over the most recent `horizon` seconds of traffic."""

    def __init__(self, horizon: int) -> None:
        """Create an empty window.

        Args:
            horizon: How many seconds of traffic the window covers.
        """
        self.horizon = horizon
        self.buckets: deque[list[int]] = deque()  # [second, requests, failures]
        self.requests = 0
        self.failures = 0

    def record(self, second: int, requests: int, failures: int) -> None:
        """Fold one second of traffic into the window.

        Args:
            second: The whole second the traffic belongs to, non-decreasing
                across calls.
            requests: How many requests that second served.
            failures: How many of them failed.
        """
        self.buckets.append([second, requests, failures])
        self.requests += requests
        self.failures += failures
        self._drop_stale(second)

    def _drop_stale(self, now: int) -> None:
        """Remove buckets that have fallen out of the horizon.

        Args:
            now: The current second.
        """
        while self.buckets and self.buckets[0][0] <= now - self.horizon:
            _, requests, failures = self.buckets.popleft()
            self.requests -= requests
            self.failures -= failures

    def rate(self) -> float:
        """Return the failure rate over the window, as a fraction of one.

        Returns:
            failures / requests, or 0.0 when the window saw no requests.
        """
        if self.requests == 0:
            return 0.0
        return self.failures / self.requests


def first_alert(
    traffic: list[tuple[int, int, int]],
    horizon: int = 60,
    threshold: float = 0.01,
    minimum_requests: int = 100,
) -> tuple[int, float] | None:
    """Return the first second at which the rolling failure rate trips.

    Args:
        traffic: (second, requests, failures) triples, in time order.
        horizon: How many seconds the window covers.
        threshold: The failure rate that must be exceeded, as a fraction.
        minimum_requests: How many requests the window needs before the rate
            is trusted. Without this, one failed request out of one is a
            hundred per cent and every quiet minute pages somebody.

    Returns:
        (second, rate) for the first second whose window is over threshold, or
        None when the window never trips.
    """
    window = RollingRate(horizon)
    for second, requests, failures in traffic:
        window.record(second, requests, failures)
        if window.requests >= minimum_requests and window.rate() > threshold:
            return (second, window.rate())
    return None


def scripted_traffic() -> list[tuple[int, int, int]]:
    """Return five minutes of made-up but entirely predictable traffic.

    Forty requests a second throughout. For the first three minutes one
    request fails every twenty-five seconds — background noise, well under
    one per cent. From second 180 a bad deploy fails two requests a second,
    which is five per cent, and the rolling window has to notice.

    Returns:
        (second, requests, failures) triples for seconds 0 to 299.
    """
    traffic = []
    for second in range(300):
        if second >= 180:
            failures = 2
        elif second % 25 == 0:
            failures = 1
        else:
            failures = 0
        traffic.append((second, 40, failures))
    return traffic


# ---- Self-check ----
if __name__ == "__main__":
    traffic = scripted_traffic()
    alert = first_alert(traffic)
    second, rate = alert

    print("five minutes of traffic, 40 requests a second")
    print("  bad deploy starts at second 180, failing 2 requests a second")
    print(f"  first alert at second {second}, rolling rate {rate * 100:.2f}%")
    print(f"  that is {second - 180} seconds after the deploy went out")
    print()

    quiet = RollingRate(60)
    for tick in range(120):
        quiet.record(tick, 40, 0)
    print(f"a clean window holds {quiet.requests} requests and reports {quiet.rate() * 100:.2f}%")
    print(f"buckets kept in memory: {len(quiet.buckets)}, not {120}")
    print()

    assert alert == (191, 26 / 2400)
    assert first_alert(traffic[:180]) is None
    assert first_alert([]) is None
    # One failure out of one request is 100%, and must not page anyone.
    assert first_alert([(0, 1, 1)]) is None
    # The same burst with the minimum lowered does trip, immediately.
    assert first_alert([(0, 1, 1)], minimum_requests=1) == (0, 1.0)

    # The window really only ever holds `horizon` buckets.
    assert len(quiet.buckets) == 60
    assert quiet.requests == 60 * 40
    assert quiet.rate() == 0.0

    # Running totals agree with a from-scratch count of the buckets kept.
    window = RollingRate(60)
    for row in traffic[:250]:
        window.record(*row)
    assert window.requests == sum(bucket[1] for bucket in window.buckets)
    assert window.failures == sum(bucket[2] for bucket in window.buckets)

    print("All checks passed.")
```

**Add first, then evict, and the order is not arbitrary.**

```python
self.buckets.append([second, requests, failures])
self.requests += requests
self.failures += failures
self._drop_stale(second)
```

The bucket you just added is what defines "now". Evicting first would use the
*previous* second as the horizon's anchor, so the window would lag by one
bucket — a small error that never raises and quietly makes every rate slightly
stale. Appending first also means the window is never empty when `_drop_stale`
runs, which removes a guard you would otherwise need.

**`while`, not `if`, in the eviction.**

```python
while self.buckets and self.buckets[0][0] <= now - self.horizon:
```

Traffic has gaps. A service that goes quiet for two minutes and then resumes
delivers a second whose horizon strands *every* bucket currently held, and they
all have to go in one call. An `if` drops one and leaves fifty-nine stale
buckets contributing to the totals, which means the very first rate after a
quiet period is computed over data from before it. That is the kind of bug that
only appears at 3 a.m.

The `self.buckets and` guard is what makes it safe to drain the deque
completely.

**Subtract on the way out, always.**

```python
_, requests, failures = self.buckets.popleft()
self.requests -= requests
self.failures -= failures
```

This is Exercise 1's `window_total += arrivals[right] - arrivals[right - k]`,
split across two methods. The running totals are only meaningful if every
bucket that enters is eventually subtracted exactly once. The self-check
verifies precisely that, by recounting the buckets from scratch and comparing —
which is the right way to test a running total, and cheap enough to leave in.

**`rate()` guards the division rather than the caller.**

```python
if self.requests == 0:
    return 0.0
```

An empty window has no rate. Returning `0.0` is a choice — `None` would also be
defensible — and it is chosen because callers overwhelmingly want to compare
the rate against a threshold, and a zero compares harmlessly where a `None`
raises. Putting the decision in one place means no caller has to remember it.

**Both conditions, or the alert is useless.**

```python
if window.requests >= minimum_requests and window.rate() > threshold:
```

The minimum-requests condition is doing more work than it looks. Without it,
the very first second of the scripted stream — forty requests, zero failures —
is fine, but a service starting up with one request that happens to fail is at
a hundred per cent and pages somebody instantly. The self-check tests exactly
that with `[(0, 1, 1)]`, and tests that lowering the minimum makes it fire, so
the guard is demonstrably the thing doing the work rather than a coincidence.

**Bucketing is what bounds the memory, and it is the design decision.** Storing
one entry per request makes memory depend on traffic, which is precisely
backwards: the busier the service, the more likely it is to be in trouble, and
the worse a moment that is to start allocating. One bucket per second makes
memory depend on the *horizon* — sixty entries, forever, at any traffic level.
The cost is resolution: you cannot ask about half a second. That trade is worth
stating out loud, because it is the same trade every real
metrics system makes.

**What this shares with the algorithm, and what it does not.** Shared: two
edges, a running total, add on the right and subtract on the left, and each
piece of data enters and leaves exactly once. Not shared: there is no list, no
`right` index, and no end — the stream does not finish, so there is no "after
the loop" in which to compute an answer. Every answer has to be available at
every moment, which is why the state is an object rather than a local variable.

Being able to say that in an interview — *"it is the same two rules, but the
axis is time and the data is unbounded, so the state has to live somewhere that
outlives a loop"* — is what the question is really asking.

## Download and run

Download
[problem-05-rolling-error-rate-solution.py](./problem-05-rolling-error-rate-solution.py)
and run it:

```bash
python problem-05-rolling-error-rate-solution.py
```

It is the same program you are writing, under a name that will not collide with
your own `problem-05-rolling-error-rate.py`.

## Common bugs to catch

- **`ZeroDivisionError: division by zero`.**

  ```text
  Traceback (most recent call last):
      return self.failures / self.requests
             ~~~~~~~~~~~~~~^~~~~~~~~~~~~~~
  ZeroDivisionError: division by zero
  ```

  You called `rate()` on an empty window. It happens immediately with
  `first_alert([])`, and it is the reason the guard is in the method rather
  than left to callers.

- **`IndexError: deque index out of range`.**

  ```text
  Traceback (most recent call last):
      while self.buckets[0][0] <= now - self.horizon:
            ~~~~~~~~~~~~^^^
  IndexError: deque index out of range
  ```

  Your eviction loop drained the deque and then looked at the front of an empty
  one. Add the `self.buckets and` guard to the condition.

- **The totals drift away from the buckets.** The self-check catches it:

  ```text
  Traceback (most recent call last):
      assert window.requests == sum(bucket[1] for bucket in window.buckets)
  AssertionError
  ```

  You popped a bucket without subtracting it, or subtracted the wrong field.
  This is the running-total invariant, and it is worth testing exactly this way
  in real code too.

- **The window keeps growing.** `len(quiet.buckets)` comes out at 120 instead
  of 60. Either `_drop_stale` is never called, or its comparison uses `<`
  instead of `<=` and holds one bucket too many, or the horizon arithmetic is
  the wrong way round.

- **The alert fires at second 180.** You dropped the `minimum_requests`
  condition, or you compared with `>=` instead of `>`. Check the exact-1.00%
  moment: the stream passes through it on the way up, and the constraint says
  it does not trip.

- **The alert never fires.** Usually `first_alert` checks the condition before
  calling `record`, so the last second's traffic is never considered. Order
  matters: record, then check.

- **The scripted stream uses `random`.** Now the expected output changes every
  run and the test is worthless. Determinism is Requirement 8 for a reason.

- **Using a list instead of a deque.** `list.pop(0)` is `O(n)`. It gives the
  right answers and reintroduces exactly the cost the design was avoiding,
  which is a nicely ironic way to fail this particular page.

## Under the hood

<details>
<summary>Under the hood — why real systems bucket, and the three windows a design round might mean</summary>

**Three things "sliding window" can mean in an interview.**

1. **The algorithm.** A window over positions in an array. This week's drills.
2. **The rate limiter.** Allow at most `N` requests per client per window. Same
   structure, and the interesting part is what happens at the boundary between
   two windows.
3. **The metric.** A statistic over recent time. This page.

They share the two rules and they are asked about in different rounds, by
different people, with different follow-ups. Recognising which one you are
being asked about — and saying so — is worth doing explicitly, because
answering the wrong one confidently is a bad look.

**Fixed windows versus sliding windows, and the doubling problem.**

The cheapest rate limiter keeps one counter per fixed calendar minute and
resets it on the minute. It is one integer per client and it has a real flaw: a
client sending its whole allowance in the last second of one minute and again
in the first second of the next has sent double the limit in two seconds, and
every counter says it behaved.

The sliding version fixes it and costs more state. The usual production
compromise is a **sliding window counter**: keep only the current and previous
fixed windows, and estimate the sliding rate by weighting the previous window
by how much of it still overlaps. Two integers per client, no boundary
doubling, and an answer that is approximate in a bounded way.

That "approximate in a bounded way" move is the most transferable idea in this
whole footnote. Exact answers over unbounded streams are expensive; almost
every real system trades a known, small error for a large drop in state.

**Why buckets, in one line each.**

- Memory becomes `O(horizon)` rather than `O(traffic)`.
- Eviction becomes `O(1)` amortised — one pop per bucket, ever.
- The rate is two integer reads and a division.
- The cost is resolution: sub-second questions cannot be answered.

A production metrics system does exactly this, usually with a **ring buffer**
of fixed size instead of a deque, because the bucket count is known in advance
and a fixed array avoids allocation entirely. Same algorithm, tighter
implementation. Naming the ring buffer in a design round is a cheap and
genuine signal.

**What this design does not handle, and would need to.**

- **Out-of-order events.** Real streams deliver late. Fixes: a small
  reordering buffer, a watermark that says "no more data before time T", or
  accepting some loss. All three are real answers; not mentioning the problem
  is not.
- **Multiple processes.** Each holds its own window and none sees the whole
  picture. Fixes: a shared store, or aggregate at the collector.
- **Clock skew.** Two machines disagree about the current second. Fixes:
  timestamps from a single source, or tolerance windows.
- **Restarts.** The window is empty after a deploy, so the service is briefly
  blind precisely when it is most likely to be broken.

Each of those is one sentence in a design round and each one is worth more than
another paragraph about the deque. Interviewers are listening for whether you
know what your design assumes.

**On the detection delay.** Eleven seconds is a consequence of the horizon, not
a defect. A one-minute average cannot react faster than a fraction of a minute
by construction, and that is a fact about averages rather than about this code.
Systems that need faster detection use a shorter horizon and accept more false
alarms, or run two windows at once — a short one for pages and a long one for
trends. That last one is a genuinely good answer to "how would you make it
faster?" and it costs nothing to remember.

</details>

## Acceptance checklist

- [ ] `python problem-05-rolling-error-rate.py` prints both blocks then `All checks passed.`
- [ ] The output matches the Expected output block character for character.
- [ ] `record` adds to the totals before evicting.
- [ ] `_drop_stale` is a `while` and guards against an empty deque.
- [ ] `rate()` returns `0.0` on an empty window.
- [ ] The window never holds more than 60 buckets after 120 seconds of traffic.
- [ ] `first_alert` requires both conditions, and `[(0, 1, 1)]` does not trip it.
- [ ] `scripted_traffic` uses no randomness.
- [ ] You changed the horizon to 10 and to 300 and can explain which way the detection second moved.
- [ ] You can name three things this design does not handle.
- [ ] Every function and method has type hints and a docstring.
- [ ] Committed to Git with a message like `Add Week 3 homework 5: the rolling error rate`.

## Stretch

- **Write the 300-word design answer.** This is the original homework
  deliverable and it is still worth doing: a file
  `system-design/notes-week-03.md` answering *"how would you design a system
  that detects, in real time, when a service's error rate exceeds 1% over the
  most recent 60 seconds?"* Write it before you look anything up. Then read one
  article on time-bucketed counters and note three things you would add —
  especially if it mentions ring buffers or the fixed-versus-sliding boundary
  problem. You have now built the thing, so the article will read differently.

- **Two horizons at once.** A ten-second window for pages and a five-minute one
  for trends, sharing one stream.

  ```python
  def dual_alert(traffic: list[tuple[int, int, int]]) -> tuple[int | None, int | None]:
      """Return the first alert second for a fast window and a slow one."""
      fast, slow = RollingRate(10), RollingRate(300)
      fast_at = slow_at = None
      for second, requests, failures in traffic:
          fast.record(second, requests, failures)
          slow.record(second, requests, failures)
          if fast_at is None and fast.requests >= 100 and fast.rate() > 0.01:
              fast_at = second
          if slow_at is None and slow.requests >= 100 and slow.rate() > 0.01:
              slow_at = second
      return (fast_at, slow_at)
  ```

  ```text
  scripted_traffic() -> (183, 187)
  ```

  Predict which fires first and by how much before you run it. Then work out
  why the slow window is not as far behind as you might expect.

- **Break the ordering assumption.** Feed the window a stream with one event
  arriving two seconds late and watch what happens. Then decide, in writing,
  which of the three fixes from *Under the hood* you would pick and why. The
  decision is the deliverable, not the code.

Next: [Problem 6 — Week 3 Reflection](./problem-06-week-03-reflection.md).
