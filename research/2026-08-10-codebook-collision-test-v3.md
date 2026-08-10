---
title: Codebook collision test v3 — controlled, two arms, both item sets
date: 2026-08-10
status: COMPLETE
verdict: >
  v3 improves reliability on BOTH item sets with the items held fixed, so unlike
  the v1→v2 comparison this one is not confounded: fine α +0.096 on the v1 items
  and +0.072 on the v2 items. `principle` (α 0.910) and `architecture` (0.851)
  fix the two labels the renames targeted. The strip test does what it was
  designed to do on its target boundary (37 → 11 rater-pairs) but its effect on
  aggregate α is within noise.
---

# Codebook Collision Test — v3

Tests the fifteen-label taxonomy (§2.7 of `docs/SPECIFICATION.md`: `driver` →
`principle`, `structure` → `architecture`, `technique` merged into `procedure`,
plus eleven repaired pointers) and, separately, the strip test added to
`observation` after the control run.

## Design

Two things are being asked at once, so the run has two arms over one item set:

| | items | codebook |
|---|---|---|
| **arm A** | 152 | v3, pointers repaired, **no** strip test |
| **arm B** | 152 | v3, pointers repaired, **plus** the strip test |

The 152 items are the union of the two earlier item sets — v1's 72 (`S###`) and
v2's 80 (`T###`) — kept individually addressable. That gives three comparisons,
each with the items held fixed:

- **arm A vs the control**, on the S subset → the effect of the v3 changes
- **arm A vs the v2 run**, on the T subset → the same, on the other item set
- **arm B vs arm A**, on everything → the effect of the strip test alone

4 blind raters per arm, codebook verbatim and nothing else, per-rater rotation
(offset 31), Krippendorff α (nominal). Coverage 100%: 1216 of 1216 assignments.

## Headline: v3 beats v2 on both item sets, items held fixed

| | fine α | coarse α |
|---|---|---|
| **S subset (72 items)** — control (v2 codebook) | 0.787 | 0.791 |
| **S subset** — v3 arm A | **0.883** | **0.874** |
| | **+0.096** | **+0.083** |
| **T subset (80 items)** — v2 run | 0.858 | 0.927 |
| **T subset** — v3 arm A | **0.930** | 0.927 |
| | **+0.072** | +0.000 |

This is the comparison v1→v2 failed to be. The item set is identical within each
pair, so the gain is the codebook.

Full-set figures, arm A: fine α 0.910, coarse α 0.903, unanimity 0.86.
Arm B: fine α 0.904, coarse α 0.915, unanimity 0.86 fine / 0.89 coarse.

## The renames worked

Measured on the T subset, which is exactly the item set the v2 numbers came
from:

| v2 label | α | v3 label | α | change |
|---|---|---|---|---|
| `driver` | 0.623 | `principle` | **0.910** | **+0.287** |
| `structure` | 0.727 | `architecture` | **0.851** | **+0.124** |
| `procedure` | 0.760 | `procedure` (absorbed `technique`) | 0.834 | +0.074 |
| `technique` | 0.588 | — removed — | | |

`driver` was the weakest surviving label in v2 and the participant in v2's
largest collision. As `principle` it is the fourth-strongest of the fifteen.
`driver`/`structure` collided 17 times in v2; `principle`/`architecture` collide
5 times in v3 on twice the items.

`[CAVEAT]` The rename is confounded with the pointer repair — eleven dangling
cross-references were fixed in the same revision, and one of them sat inside the
`observation` definition. The two cannot be separated by this experiment.

## The strip test: works on its target, invisible in aggregate

The boundary it was written for, `principle` / `observation`:

| run | S subset | T subset | all |
|---|---|---|---|
| control (v2 codebook) | **37** | — | — |
| v3 arm A (no strip test) | 17 | 6 | 23 |
| v3 arm B (strip test) | **11** | 6 | 17 |

37 → 17 is the pointer repair and the renames. 17 → 11 is the strip test, a
further 35% on the subset where the boundary is actually exercised.

Aggregate effect of the strip test (arm B − arm A):

| subset | fine α | coarse α |
|---|---|---|
| all 152 | −0.005 | +0.012 |
| S (results-dense) | −0.012 | +0.016 |
| T | +0.000 | +0.008 |

**Honest reading: within noise.** Four raters, no confidence intervals, effects
of ±0.01. What is *not* within noise is the target boundary, which moves 35%.
The direction of the aggregate split is consistent with the mechanism —
`principle`/`observation` is a *cross-coarse* collision (model vs case), so
resolving it helps the coarse tier, while the disagreement it displaces lands
inside the fine tier. Suggestive, not established.

## Per-label, arm B, all 152 items

| label | assigned | α |
|---|---|---|
| `definition` | 8 | 1.000 |
| `formula` | 12 | 1.000 |
| `obligation` | 50 | 0.971 |
| `prohibition` | 25 | 0.958 |
| `dependency` | 17 | 0.940 |
| `observation` | 187 | 0.931 |
| `procedure` | 62 | 0.916 |
| `decision` | 30 | 0.883 |
| `recommendation` | 48 | 0.880 |
| `assumption` | 23 | 0.865 |
| `principle` | 123 | 0.861 |
| `distinction` | 7 | 0.856 |
| `architecture` | 14 | 0.757 |
| `event` | 2 | **−0.002** |
| `background` | 0 | never assigned |

Nothing fell outside the taxonomy: 0 of 1216 assignments went to `general`.

**`event` has now failed to be exercised by three consecutive item sets** (2 of
608 assignments in arm B, and no agreement on those two). It was retained
deliberately for historical recording. It remains untested rather than
disproven — but three item sets sampled from six different source types have not
produced it, which is itself information about how often it will fire.

`background` drew zero assignments across all 152 items in both arms.

## New collisions worth codifying

| pair | rater-pairs (arm B) | coarse types |
|---|---|---|
| `principle` / `observation` | 17 | model / case |
| `principle` / `recommendation` | 12 | model / method |
| `decision` / `procedure` | 7 | rule / method |
| `assumption` / `observation` | 6 | model / case |
| `architecture` / `principle` | 5 | model / model |

Two of these are new and cross coarse types, so they cost the coarse tier
directly. Both have a clean surface separator, and both are the same shape of
problem the strip test solves — a sentence doing two jobs at once:

**`principle` / `recommendation`** — an explanation with advice attached:

> "sharpe on 20d overlapping returns is inflated roughly 1.8x by autocorrelation
> — newey-west at lag 19, or just resample to non-overlapping windows"
> *(2 raters `principle`, 2 raters `recommendation`)*

> "training/serving skew here is almost always the tokenizer version, check that
> before you go looking at the data" *(2/2)*

**`decision` / `procedure`** — a settled choice stated as how it is done:

> "Models are versioned by the SHA-256 of the serialized artifact, not by a
> semantic version string, because two training runs with identical code, data,
> and seed must be provably identical" *(2 raters `decision`, 2 `procedure`)*

> "Implementation shortfall is measured here against the decision price rather
> than the arrival price…" *(1 `decision`, 3 `procedure`)*

Both patterns are dense in conversational sources, which is where this
classifier is meant to work.

## Data

- `2026-08-10-codebook-collision-data-v3/experiment-workflow.js` — both arms
- `2026-08-10-codebook-collision-data-v3/rater-responses-and-items.json` — all
  1216 assignments, both arms, and all 152 items verbatim
- `2026-08-10-codebook-collision-data-v3/analyze-v3.py` — every number above
