---
title: What actually limits agreement — three levers tested by analysis, all closed
date: 2026-08-11
status: COMPLETE (analysis only, no agents spent)
verdict: >
  Neither the label count nor sentence complexity is the binding constraint.
  Merging the single best pair of labels buys +0.007; collapsing 15 labels to 9
  reaches only 0.927. Compound sentences score HIGHER than simple ones (0.881 vs
  0.871) and long sentences higher than short (0.943 vs 0.850), so splitting
  compound statements would make things worse, not better. If 0.95 is reachable
  it has to come from the instrument — how the question is asked — not from the
  taxonomy or the corpus.
---

# What Limits Agreement

Three candidate levers, all testable against ratings already collected, none
requiring a single agent. All three turned out to be dead ends, which is worth
more than it sounds: each would have cost hours to test with agents.

Baseline for everything below: **fine α 0.891** over 312 statements × 4 raters,
pooled from the 160-item and 152-item corpora.

## Lever 1 — fewer labels. Closed.

**Best single merge: `observation` + `principle`, worth +0.007.** That is the
largest collision in the entire project — 31 rater-pairs — and erasing the
distinction entirely buys seven thousandths.

| merge | α | gain |
|---|---|---|
| `observation` + `principle` | 0.898 | +0.007 |
| `event` + `observation` | 0.898 | +0.007 |
| `principle` + `recommendation` | 0.895 | +0.004 |
| `background` + `event` | 0.895 | +0.004 |
| `decision` + `procedure` | 0.894 | +0.003 |

Dropping a label into `general` is no better: the best is `dependency` at
+0.002, and dropping `observation` — 383 assignments, the highest-volume label
in the taxonomy — moves α by **+0.001**.

Greedily merging the best available pair, six times over:

| labels | after merging | α |
|---|---|---|
| 14 | observation + principle | 0.898 |
| 13 | + event | 0.906 |
| 12 | + distinction | 0.912 |
| 11 | + background | 0.918 |
| 10 | decision + procedure | 0.922 |
| **9** | + architecture | **0.927** |

**Collapsing the taxonomy by 40% still does not reach 0.95.** And the resulting
9-label scheme has a single blob containing `observation`, `principle`, `event`,
`distinction` and `background` — it would be useless for a wiki.

The gains are diffuse: no label is dragging the score down. That is the
signature of genuinely ambiguous *sentences*, not of a broken label.

## Lever 2 — split compound statements. Closed, and it points the other way.

The spec puts multi-statement splitting out of scope for v1, and several of the
worst-scoring items are visibly two statements in one sentence. The obvious
inference is that splitting would help. It would not.

**By sentence length:**

| words | n | α |
|---|---|---|
| 20–30 | 43 | 0.850 |
| 30–45 | 95 | 0.877 |
| **45+** | 15 | **0.943** |

**By compound structure** (semicolon, *while*, *whereas*, *but*, *so that*):

| | n | α |
|---|---|---|
| simple | 83 | 0.871 |
| **compound** | 77 | **0.881** |

Longer and more complex statements are classified *more* consistently, not less.
The mechanism is straightforward once seen: more text means more surface cues,
and every reliable rule in this codebook keys on a surface cue. A terse chat line
— *"found it. we compute the signal on the 16:00 close and fill at that same
close"* — is ambiguous precisely because it is terse.

**Consequence:** splitting compound statements into atoms would strip the context
that makes them classifiable. The v1 decision to leave splitting out of scope is
right, and for a better reason than the one recorded in §6.

## Lever 3 — regroup the coarse tier. Partially open.

Covered in full in `2026-08-11-coarse-grouping-search.md`. Summary: the shipped
five-family cut scores 0.907; the best cut found, a two-way `practice`/`claim`
split, scores **0.948** — at the unconstrained overfit ceiling. Worth ~0.04 at
the coarse tier, nothing at the fine tier.

## What is left

Only the **instrument** — how the question is put to the model.

Everything measured so far asked a rater to pick one label from fifteen. The
spec has never specified that; §4.1 specifies independent boolean tests resolved
in code, and the strongest verified finding in the research base is that
multiclass framing measured **90% lower odds** of correct detection than binary
(OR 0.10, CI 0.03–0.35, 1.1M+ annotations).

So the untested space is: boolean batteries, tiered cascades, and funnels that
never put more than three options in front of the model at once. Those runs are
in flight.

**If the instrument does not deliver it, 0.95 is not reachable on this corpus**,
and the honest answer is to report the ceiling rather than to keep cutting the
taxonomy until the number looks right.
