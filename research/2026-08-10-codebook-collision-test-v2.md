---
title: Codebook collision test v2 — does the restructured taxonomy separate better?
date: 2026-08-10
status: COMPLETE — but see the control, which reverses the headline reading
verdict: >
  fine α 0.858, coarse α 0.927 on 80 fresh statements. Read on its own this
  looks like a large win over v1 (0.778 / 0.866). It is not: the item set
  changed at the same time as the taxonomy, and the control run
  (2026-08-10-codebook-collision-control.md) attributes almost all of the gain
  to the items.
---

# Codebook Collision Test — v2

Measures whether the sixteen definitions of the restructured taxonomy (§2.5–2.6
of `docs/SPECIFICATION.md`, the revision that dissolved `claim`, promoted
`driver`, and split `mechanism` into `architecture`-shaped parts) can be applied
consistently, and which pairs collide.

**Read this file together with the control.** On its own it supports a
conclusion the control refutes.

## Method

Identical to the v1 test, so the two are comparable in everything except the
codebook and the items:

- **80 statements** (`T000`–`T5xx`), generated in batches by agents that never
  saw the taxonomy, sampled by SOURCE rather than by category: quant strategy
  documentation, fund risk policy, a backtest-debugging thread, ML papers, an ML
  platform runbook, an ML training-run thread.
- **4 blind raters**, each given the shipped §3.2 + §3.3 codebook verbatim and
  nothing else. No answer key exists.
- **Item order rotated per rater** (offset 17) against position bias.
- **Primary metric: inter-rater Krippendorff α (nominal).** Per-label figures
  are one-vs-rest binary collapses, the CoreSC method.
- Coverage 100%: 320 of 320 assignments made.

## Headline

| tier | α | unanimity |
|---|---|---|
| **fine (16 labels)** | **0.858** | 0.78 |
| **coarse (5 types + general)** | **0.927** | 0.90 |

Zero statements fell outside the taxonomy (0 of 320) — no rater reached for the
escape hatch.

## Per-label reliability

| label | assigned | 1-vs-rest α |
|---|---|---|
| `assumption` | 24 | 1.000 |
| `background` | 4 | 1.000 |
| `obligation` | 20 | 1.000 |
| `prohibition` | 16 | 1.000 |
| `observation` | 75 | 0.983 |
| `recommendation` | 17 | 0.938 |
| `formula` | 13 | 0.920 |
| `decision` | 18 | 0.883 |
| `dependency` | 21 | 0.848 |
| `definition` | 13 | 0.760 |
| `procedure` | 13 | 0.760 |
| `structure` | 31 | 0.727 |
| `distinction` | 7 | 0.660 |
| `driver` | 38 | **0.623** |
| `technique` | 10 | **0.588** |

`event` was never assigned on this item set.

## Collisions

| pair | rater-pairs disagreeing |
|---|---|
| `driver` / `structure` | **17** |
| `procedure` / `technique` | 6 |
| `dependency` / `driver` | 6 |
| `definition` / `driver` | 4 |
| `formula` / `procedure` | 3 |
| `dependency` / `structure` | 3 |
| `driver` / `technique` | 3 |
| `definition` / `distinction` | 3 |

## What this test supported

One change outright:

- **`technique` merged into `procedure`.** Weakest label at α 0.588, with six
  confusions against `procedure` and three against `driver`. Two labels for one
  boundary that raters could not hold apart.

Two changes it motivated without confirming — both renames, both hypotheses for
the next test rather than fixes:

- **`driver` → `principle`.** The `driver`/`structure` collision at 17 is the
  largest in the test, and `driver` is the weakest surviving label. In
  engineering usage a *driver* is a component, which is a reading that competes
  directly with `structure`.
- **`structure` → `architecture`.** Naming only; `architecture` is the native
  word in ML model cards.

## What this test did NOT support, though it was read that way at the time

The zero-escape-hatch result (0 of 320) was reported as evidence that dissolving
the `claim` coarse type "cost nothing measurable." That inference does not hold.
Raters were instructed to use the escape hatch only when *no* label applies —
not when the right label is missing but a wrong one is available. A missing
label shows up as a **collision**, not as an escape. On this item set it did not
show up at all, because this item set contains few of the statements that make
it visible. See the control.

## Data

- `2026-08-10-codebook-collision-data-v2/experiment-workflow.js` — the run
- `2026-08-10-codebook-collision-data-v2/rater-responses-and-items.json` — all
  320 assignments and all 80 items verbatim
- `2026-08-10-codebook-collision-data/analyze.py` — statistics, shared across
  all three runs
