<div align="center">

# `dsa-blueprint`

**Day 000. Zero problems solved. Starting now.**

<br>

![Day](https://img.shields.io/badge/day-000-7C3AED?style=for-the-badge&labelColor=0B1120)
![Solved](https://img.shields.io/badge/solved-0-2563EB?style=for-the-badge&labelColor=0B1120)
![Language](https://img.shields.io/badge/python-3.12-06B6D4?style=for-the-badge&labelColor=0B1120)

</div>

---

## Where this is right now

Empty. That's the honest state of it, and this README is the plan rather than the
proof — the numbers above go up as the work happens, not before.

I build backends for a living already. What I don't have yet is the reflex where a
problem statement reads as *"that's a hash map"* before I've finished the second
paragraph. That reflex is the only thing this repo exists to build.

---

## How it's organised

By **pattern**, not by day. `Day-047` tells me nothing six weeks later;
`patterns/03-sliding-window/` tells me exactly where to look when I'm stuck.

```
dsa-blueprint/
├── patterns/
│   ├── 01-arrays-hashing/
│   │   ├── _pattern.md              ← what this pattern is, when it fires
│   │   ├── 0217-contains-duplicate/
│   │   │   ├── solution.py
│   │   │   └── notes.md
│   │   └── 0001-two-sum/
│   ├── 02-two-pointers/
│   └── 03-sliding-window/
├── templates/
│   └── NOTES_TEMPLATE.md
└── README.md
```

Folder names use the real LeetCode ID so they sort right and map back to the source.

---

## Month one: six patterns, fourteen problems

Not a random daily-challenge grind. Six foundational patterns, in dependency order,
with a small set of problems that are *known* to teach each one. Everything harder
is a variation on these.

### `01` Arrays & Hashing
> The core question: *have I seen this before?* If you're checking membership or
> counting occurrences, you want a hash map. This is the most-reused idea in DSA.

| # | Problem | Difficulty | Why this one |
| :-: | :--- | :-: | :--- |
| 1 | [Contains Duplicate](https://leetcode.com/problems/contains-duplicate/) | Easy | The purest possible "set beats nested loop" |
| 2 | [Valid Anagram](https://leetcode.com/problems/valid-anagram/) | Easy | Frequency counting, first appearance |
| 3 | [Two Sum](https://leetcode.com/problems/two-sum/) | Easy | Trading space for time — the whole trick, in miniature |
| 4 | [Group Anagrams](https://leetcode.com/problems/group-anagrams/) | Medium | Designing a *key*, not just using one |
| 5 | [Top K Frequent Elements](https://leetcode.com/problems/top-k-frequent-elements/) | Medium | Count, then rank — two ideas stacked |

### `02` Two Pointers
> Fires when the input is **sorted** (or can be). Two indices moving toward each
> other turn an O(n²) search into a single pass.

| # | Problem | Difficulty | Why this one |
| :-: | :--- | :-: | :--- |
| 6 | [Valid Palindrome](https://leetcode.com/problems/valid-palindrome/) | Easy | Converging pointers, simplest form |
| 7 | [Two Sum II](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/) | Medium | Same problem as #3, different tool — feel the difference |
| 8 | [3Sum](https://leetcode.com/problems/3sum/) | Medium | Fix one, two-point the rest. Dedup is the real lesson |

### `03` Sliding Window
> Fires on *"longest / shortest / max subarray or substring with property X."*
> A window that grows on the right and shrinks on the left.

| # | Problem | Difficulty | Why this one |
| :-: | :--- | :-: | :--- |
| 9 | [Best Time to Buy and Sell Stock](https://leetcode.com/problems/best-time-to-buy-and-sell-stock/) | Easy | The gentlest possible window |
| 10 | [Longest Substring Without Repeating](https://leetcode.com/problems/longest-substring-without-repeating-characters/) | Medium | Window + hash set. The canonical one |

### `04` Stack
> Fires on nesting, matching pairs, and "the most recent thing I saw."

| # | Problem | Difficulty | Why this one |
| :-: | :--- | :-: | :--- |
| 11 | [Valid Parentheses](https://leetcode.com/problems/valid-parentheses/) | Easy | Why a stack exists, in twelve lines |
| 12 | [Min Stack](https://leetcode.com/problems/min-stack/) | Medium | Designing a structure, not just using one |

### `05` Binary Search
> Fires on sorted input — *and*, later, on any monotonic answer space. Halve
> the search space every step.

| # | Problem | Difficulty | Why this one |
| :-: | :--- | :-: | :--- |
| 13 | [Binary Search](https://leetcode.com/problems/binary-search/) | Easy | Get the boundary conditions right. They are always the bug |
| 14 | [Search a 2D Matrix](https://leetcode.com/problems/search-a-2d-matrix/) | Medium | Same algorithm, unfamiliar shape |

**After these fourteen:** the full map below. Problem lists for each pattern get
written into this file as I reach them — not before, because a curriculum I haven't
started is a wishlist, not a plan.

---

## How to solve one (the actual loop)

```
1.  Restate the problem in one sentence, in my own words.
    Can't do it → I haven't read it properly.

2.  Say the brute force out loud. State its complexity.
    The naive answer isn't failure, it's the baseline to beat.

3.  Ask: what is the brute force computing twice?
    Every optimisation is the answer to that one question.

4.  Code it. Dry-run one tiny input by hand BEFORE hitting submit.

5.  Timebox 30 minutes. Then read the editorial — no shame in it,
    but the problem gets tagged [assisted] and re-solved in 7 days.
```

On day one, most problems will hit step 5. That's expected and it isn't a
problem — the re-solve is where the learning actually lands.

---

## What gets committed

A `solution.py` and a `notes.md`. Both, every time.

```markdown
# 1. Two Sum · Easy · Arrays & Hashing

## Signal
Unsorted array, find a pair summing to a target. Repeated "does the
complement exist?" lookups → hash map.

## First try
Nested loops, O(n²). Correct but slow.

## The insight
The inner loop is re-scanning to answer "is target - x in the array?"
A dict answers that in O(1). Store as you go — one pass.

Time O(n) · Space O(n)

## Cost me
Stored the value as the key and the index as the value, then tried to
return the key. Twenty minutes on a naming mistake.
```

That last section — **Cost me** — is the reason this repo is worth keeping.
Bugs repeat. Written-down bugs don't.

---

## Progress

| # | Date | Problem | Pattern | Difficulty | Solo | Notes |
| :-: | :--- | :--- | :--- | :-: | :-: | :--- |
| — | — | *first row lands here* | — | — | — | — |

---

## The full map

Thirty-seven patterns, ordered by dependency. A box fills when I can solve a *new*
problem from that pattern cold — no notes, no editorial. Boxes, not problem counts,
because grinding forty array questions teaches less than four solved properly.

```
TIER 1 — FOUNDATIONS  (start here, everything else assumes these)

01  Arrays & Hashing ................. ◻◻◻◻◻
02  Two Pointers ..................... ◻◻◻
03  Sliding Window ................... ◻◻◻◻
04  Prefix Sum ....................... ◻◻◻
05  Strings .......................... ◻◻◻◻
06  Binary Search .................... ◻◻◻◻
07  Stack ............................ ◻◻◻
08  Queue & Deque .................... ◻◻
09  Matrix / Grid .................... ◻◻◻◻
10  Sorting & Comparators ............ ◻◻◻
11  Math & Simulation ................ ◻◻◻
12  Bit Manipulation ................. ◻◻◻

TIER 2 — STRUCTURES  (build and bend the containers themselves)

13  Linked Lists ..................... ◻◻◻◻
14  Heap / Priority Queue ............ ◻◻◻◻
15  Monotonic Stack .................. ◻◻◻
16  Intervals ........................ ◻◻◻
17  Trie ............................. ◻◻◻
18  Design (LRU, iterators) .......... ◻◻◻

TIER 3 — TREES & GRAPHS  (where recursion stops being optional)

19  Recursion & Divide-Conquer ....... ◻◻◻
20  Binary Trees — DFS ............... ◻◻◻◻◻
21  Binary Trees — BFS ............... ◻◻◻
22  Binary Search Trees .............. ◻◻◻
23  Backtracking ..................... ◻◻◻◻
24  Graphs — BFS / DFS ............... ◻◻◻◻◻
25  Topological Sort ................. ◻◻◻
26  Union-Find ....................... ◻◻◻
27  Shortest Path (Dijkstra) ......... ◻◻◻
28  Minimum Spanning Tree ............ ◻◻

TIER 4 — OPTIMISATION  (the interview-hard tier)

29  Greedy ........................... ◻◻◻◻
30  1-D Dynamic Programming .......... ◻◻◻◻◻
31  2-D / Grid DP .................... ◻◻◻◻
32  Knapsack DP ...................... ◻◻◻
33  DP on Strings .................... ◻◻◻
34  DP on Trees ...................... ◻◻
35  Bitmask DP ....................... ◻◻
36  Segment Tree / Fenwick ........... ◻◻
37  Number Theory .................... ◻◻
```

<sub>`◻` open · `◼` filled · **0 / 122**</sub>

**Read it top to bottom.** Tier 3 without Tier 1 is how people end up memorising
graph templates they can't debug. Union-Find is easy *after* you've internalised
hashing; it's incomprehensible before. Same story for every DP row — those are
recursion plus a dictionary, and skipping ahead to them just means learning
recursion later and slower, under more pressure.

---

## Reference

**Read the constraints first.** `n` tells you the shape of the answer before you
write a line:

| n ≤ | Budget | Likely approach |
| :--- | :--- | :--- |
| 20 | O(2ⁿ) | Subsets, backtracking, bitmask |
| 10³ – 10⁴ | O(n²) | Nested loops, 2D DP |
| 10⁵ – 10⁶ | O(n log n) | Sort, heap, binary search |
| 10⁷+ | O(n) or better | Single pass, pointers, math |

**Pick the structure by the question it answers:**

| The question | The structure | Cost |
| :--- | :--- | :-: |
| Have I seen this? / How many times? | Hash map / set | O(1)* |
| What's the most recent thing? | Stack | O(1) |
| What's the smallest right now? | Heap | O(log n) |
| What's at position i? | Array | O(1) |
| First in, first out? | Deque | O(1) |

<sub>`*` amortised</sub>

---

## Rules

```
→  Brute force gets said out loud before the clever one gets written.
→  30-minute timebox, then editorial — and a re-solve seven days later.
→  No commit without notes.md.
→  Skipped days get logged as skipped. The table doesn't lie.
→  Understood > solved. An accepted submission I can't explain is a zero.
```

---

<div align="center">
<sub>

**Muhammad Abdul Rafay Khan** · Software Engineering, ITU Lahore
[GitHub](https://github.com/rafayykhan) · [LeetCode](https://leetcode.com/u/rafayykhan)

*Starting at zero, in public.*

</sub>
</div>
