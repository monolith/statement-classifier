---
title: Collision control — was the v2 gain the taxonomy or the item set?
date: 2026-08-10
status: COMPLETE
verdict: >
  The item set. Holding items fixed, the restructured taxonomy gained +0.009
  fine α and LOST 0.075 coarse α. The +0.080 headline was 89% item-set effect.
  Dissolving `claim` has a measurable cost that the v2 item set concealed:
  37 rater-pairs disagree between `principle` and `observation` on empirical
  research results.
---

# Collision Control

The v1 and v2 collision tests changed two things at once — the codebook *and*
the statements. This run holds the statements fixed at v1's and swaps only the
codebook, so the difference is the taxonomy alone.

## Design

| run | items | codebook |
|---|---|---|
| v1 | 72 (`S###`) | v1, 18 labels |
| v2 | 80 (`T###`) | v2, 16 labels |
| **control** | **72 (`S###`)** | **v2, 16 labels** |

Everything else identical: 4 blind raters, codebook verbatim and nothing else,
per-rater item rotation, Krippendorff α (nominal) as the primary metric, no
answer key in existence. Coverage 100% (288 of 288).

## Result

| tier | v1 | control | v2 |
|---|---|---|---|
| fine α | 0.778 | **0.787** | 0.858 |
| coarse α | 0.866 | **0.791** | 0.927 |
| unanimity (fine) | 0.67 | 0.69 | 0.78 |

Decomposed:

| effect | fine α | coarse α |
|---|---|---|
| headline v1 → v2 (taxonomy **and** items) | +0.080 | +0.061 |
| **taxonomy alone** (items held at v1) | **+0.009** | **−0.075** |
| item set alone (codebook held at v2) | +0.071 | +0.136 |

**The restructure bought essentially nothing on a fixed item set, and went
backwards at the coarse tier.** 89% of the fine-tier headline was the item set.

## Why the coarse tier got worse

v1 grouped `finding`, `conclusion`, and `fact` under a `claim` coarse type.
Those three collided heavily with each other — `conclusion`/`finding` 17,
`fact`/`finding` 14 — but *within* one coarse type, so the collisions were
invisible at the coarse tier and coarse α stayed high at 0.866.

v2 dissolved `claim`. The same statements now have to go to `observation`
(coarse `case`) or `driver` (coarse `model`). The disagreement did not go away;
it moved across a coarse boundary, where it costs coarse α directly.

## The collision the v2 item set concealed

| pair | control | v2 |
|---|---|---|
| `driver` / `observation` | **37** | 0 |
| `driver` / `recommendation` | 12 | 0 |
| `driver` / `structure` | 0 | 17 |

37 disagreeing rater-pairs is the largest collision measured in any run. It is
not spread across the corpus — it concentrates on one statement shape: **an
empirical result reported in order to assert a generalization.** Twelve of the
72 items split this way. Examples, with the four raters' labels:

| item | labels | text (abridged) |
|---|---|---|
| S000 | obs, obs, obs, driver | "Sorting U.S. common stocks into deciles on trailing twelve-month idiosyncratic volatility yields a long-short spread of −0.62% per month (t = −3.41) over 1996–2023…" |
| S001 | obs, driver, driver, driver | "The variance risk premium… averages 1.9 volatility points and predicts index excess returns at the one-month horizon with an adjusted R² of 4.7%." |
| S005 | obs, obs, obs, driver | "We estimate that dealer inventory imbalances in on-the-run Treasuries mean-revert with a half-life of 2.3 business days…" |
| S007 | obs, driver, driver, driver | "Order-flow imbalance accounts for 68% of contemporaneous variation in one-minute returns among large-capitalization names…" |
| S403 | obs, obs, driver, driver | "We observe that calibration degrades substantially faster than top-line accuracy under covariate shift, which implies that accuracy monitoring alone is an insufficient trigger for retraining." |

Every one is simultaneously a measurement on a sample and a general claim. v1
had a label for exactly this — `finding`, which took 68 of 288 assignments, 24%
of the corpus. v2 has none, so they scatter.

The v1 item set is dense with these because it was sampled from quant research
papers and ML papers. The v2 item set is not, which is why the v2 run showed
`observation` at α 0.983 and no sign of trouble. **Neither item set is wrong;
the v2 run simply could not see this failure mode.**

## A second, unseparated cause

Through v2 the codebook's `observation` definition still instructed raters:
*"Excludes: a statement that generalizes past the instance (→ `finding`); the
description of how an investigation was set up (→ `study`); a judgment drawn
from what was seen (→ `conclusion`)."*

`finding`, `study`, and `conclusion` had all been removed by the restructure.
The definition of the label at the centre of the largest collision was pointing
raters at three labels that were not on their list. Eleven such dangling
pointers were found across §3.2 and repaired after this run.

How much of the 37 is a genuinely missing label and how much is a broken
codebook is **not separated by this experiment**. Both are live.

## Consequence for the spec

The strip test added to `observation` in §3.2 is the response: a mechanical
tie-break assigning measured results to `observation` even when the author
generalizes, and reserving `principle` for the explanation stated without its
measurement. Whether it works is a re-test, not a claim.

## Data

- `2026-08-10-codebook-collision-data-control/experiment-workflow.js` — the run
- `2026-08-10-codebook-collision-data-control/rater-responses-and-items.json` —
  all 288 assignments and all 72 items verbatim
- `2026-08-10-codebook-collision-data/analyze.py` — statistics
- `2026-08-10-codebook-collision-data/compare.py` — the three-way decomposition
  that produced every number on this page
