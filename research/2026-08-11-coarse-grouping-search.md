---
title: Which coarse grouping? Derived from the confusion data rather than designed
date: 2026-08-11
status: COMPLETE (analysis only — no agents; needs direct testing to confirm)
verdict: >
  The shipped five-family cut scores α 0.907. A two-way `practice` / `claim`
  split scores **0.948** — higher than every three-, four-, five- or six-way cut
  tried, and within 0.001 of an unconstrained overfit optimum. The structure is
  stable across 120 random restarts: what is DONE or BUILT versus what IS THE
  CASE. Two labels leak across any tier-1 boundary at >50%: `distinction` and
  `background`.
---

# Coarse Grouping Search

## Why

A tiered classifier decides coarse first and refines second, so its ceiling is
its first stage: a wrong family cannot be repaired downstream. That makes the
question "which coarse families?" quantitative rather than aesthetic, and it can
be answered from data already collected without spending a single agent.

**Method.** 312 statements × 4 raters, pooled from the 160-item and 152-item
corpora, single-choice fine labels. For any proposed grouping, map each rater's
fine label to its family and compute Krippendorff α over the mapped values. Then
search the space of partitions.

**Caveat, stated first.** This is *derived* coarse agreement — what the coarse
tier would have scored if raters had been asked the fine question and their
answers rolled up. A rater asked the coarse question **directly** may do better
or worse. Nothing here substitutes for testing the cut directly; it only says
which cuts are worth testing.

## Per-label leak rate

How often a label sat opposite a label from a *different* family, under the
`meaning` / `action` / `assertion` cut:

| label | leak | family |
|---|---|---|
| `distinction` | **62.5%** | meaning |
| `background` | **54.3%** | meaning |
| `architecture` | 43.8% | assertion |
| `dependency` | 29.2% | assertion |
| `formula` | 20.0% | assertion |
| `recommendation` | 15.5% | action |
| `principle` | 13.8% | assertion |
| `event` | 13.3% | assertion |
| `assumption` | 11.1% | assertion |
| `procedure` | 10.9% | action |
| `definition` | 8.3% | meaning |
| `decision` | 5.1% | action |
| `obligation` | 3.2% | action |
| `observation` | 2.9% | assertion |
| `prohibition` | **0.0%** | action |

Two of `meaning`'s three members leak more than half the time. `meaning` is not
a real family — only `definition` behaves like one, and it is also the most
reliable label in the taxonomy (α 1.000 as an isolated boolean test).

## Candidate cuts, measured

| cut | k | α |
|---|---|---|
| **`practice` \| `claim`** | **2** | **0.948** |
| `definition` \| `practice` \| `claim` | 3 | 0.947 |
| `practice` \| `claim`, formula → claim | 2 | 0.947 |
| `practice` \| `claim`, formula → practice | 2 | 0.946 |
| unconstrained optimum (overfit, unusable) | 3 | 0.947 |
| `meaning` \| `action` \| `assertion` | 3 | 0.927 |
| declarative \| procedural \| episodic (cognitive) | 3 | 0.920 |
| `definition` as its own family, rest split 2 ways | 4 | 0.916 |
| 4-way: case \| normative \| concept \| model | 4 | 0.912 |
| **shipped: case \| rule \| method \| concept \| model** | **5** | **0.907** |

## The structure that keeps reappearing

A hill-climb over three-group partitions, 120 random restarts, converges on the
same shape every time, with the top solutions differing only in which single
label is pulled out as a singleton — which is the optimizer scraping the last
0.005 out of noise. Discard the singleton and what remains is a **two-way
split**:

**`practice` — what is done, required, chosen, or assembled**
`obligation`, `prohibition`, `decision`, `procedure`, `recommendation`,
`architecture`, `dependency`, `formula`

**`claim` — what is the case**
`observation`, `event`, `principle`, `assumption`, `definition`, `distinction`,
`background`

Exact membership of the ambiguous few (`definition`, `formula`) moves α by
±0.001 — noise. They should be placed on semantics, not on this number.

**Why it beats the shipped cut.** The largest collision in every run,
`observation`/`principle` at 31 rater-pairs, is *cross-coarse* under
`case`/`model` — so it is paid for at both tiers. Under `practice`/`claim` both
sit inside `claim`, and it is paid for once. The same holds for
`background`/`event` (11) and `procedure`/`recommendation` (6).

## What this does and does not establish

**Established:** on this data, coarse agreement is maximised by a two-way cut at
~0.948, and the shipped five-way cut leaves ~0.04 on the table.

**Not established:** that a rater asked the two-way question directly achieves
0.948. That is a different task from rolling up fine labels, and the whole point
of a cascade is that the direct question should be *easier*. It could go either
way and must be measured.

**Not established:** that any of this survives a fresh corpus. Groupings were
selected on the same data they are scored on. The margin between the best
principled cut (0.948) and the unconstrained overfit optimum (0.947 at k=3) is
zero, which is reassuring — the principled cut is not leaving overfit headroom
unclaimed — but a held-out corpus is the only real test.

**Ceiling note.** 0.948 is the highest coarse figure obtainable from this label
set on this data by *any* regrouping, overfit search included. If a target of
0.95 end-to-end is to be met, regrouping alone cannot deliver it; it has to come
from a better instrument (direct questioning, tiering), from fewer labels, or
from splitting compound statements.
