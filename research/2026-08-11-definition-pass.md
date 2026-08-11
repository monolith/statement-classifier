---
title: The definition pass — α 0.844 → 0.934, and why the measurements could not have found it
date: 2026-08-11
status: COMPLETE
verdict: >
  Fourteen definitions rewritten in domain terms moved fine α from 0.844 to
  0.934 on 160 statements with 8 raters, winning 100% of paired resamples. That
  is an order of magnitude larger than any of the sixteen structural designs
  tested the night before, all of which landed within noise or lost. A second
  round of nine further rulings added nothing (0.954 → 0.947). On real published
  documents the codebook reaches 0.894.
---

# The Definition Pass

## Result

**160 statements, 8 raters, same protocol throughout:**

| | fine α | unanimity |
|---|---|---|
| codebook before | 0.844 | 0.72 |
| **codebook after** | **0.934** | **0.86** |

95% CI [0.905, 0.956]. Paired bootstrap: the new codebook wins **400 of 400**
resamples.

On a 40-statement subset, **0.947–0.954**.

**Secondary fields:** `form` **1.000**, `scope` 0.940, `status` 0.861.

## What changed

Fourteen definitions, rewritten from domain knowledge rather than from the
confusion data:

| label | the change |
|---|---|
| `procedure` | an established operational instruction — what could be pasted into a user manual unchanged and read as always-followed |
| `recommendation` | prescribes a course of action; **anything put forward is a recommendation, whatever it proposes** |
| `prohibition` | the negative case of `procedure`; separated from advice by whether someone could be in *breach* |
| `obligation` | what is owed to a **third party**; internal requirements are `procedure` |
| `architecture` | the construction of a physical or software system — actual, not proposed; the implementation, against `principle` as the theory behind it |
| `distinction` | a **proven** qualifier between multiple options, resting on established differences rather than one occasion's measurement |
| `observation` | **anecdotal** — insight extrapolated across multiple events, not definitive enough to be followed |
| `event` | **what happened**: a single occurrence reported as fact; quantity does not disqualify it |
| `background` | historical enrichment that **defines nothing** — strip it out and the topic is still defined |
| `definition` | fixes a **key** topic; remove it and the reader cannot follow |
| `assumption` | a **leap of faith** — taken on trust, without evidence, and the sentence knows it |
| `formula` | mathematical or scientific in nature; **no opinions in a formula** |
| `dependency` | a **hard** established requirement, not a casual note about something missing |
| `principle` | the theory or rule behind an implementation; first principles, not comparison and not measurement |

Structural changes in the same pass: `rule` dissolved into `method`; `system`
created for `architecture` and `dependency`; `formula` moved to `model`; a
`form` field added for `statement` / `question` / `answer`.

## The `form` field closed a hidden failure

Four statements in the corpus were **questions**. They produced roughly **50
disagreeing rater-pairs** scattered across six different label pairs —
`background`/`observation`, `background`/`event`, `background`/`general`,
`dependency`/`observation`, `general`/`observation`, `event`/`general`.

Raters had no way to record that a statement was a question, so each was filed
by its *subject matter*: a question about a data vendor landed near `dependency`,
a question about history landed near `event`, and no two raters chose alike.

With `form` available, questions type by what they are *about* and record that
they are questions. `form` reaches **α 1.000** on both corpora — the most
reliable field in the system.

## Real documents

85 statements extracted from three published sources, deliberately chosen to be
unlike the eight generated sources:

| source | n | α |
|---|---|---|
| De Bondt & Thaler, *Does the Stock Market Overreact?* (1985) | 30 | 0.892 |
| Sharpe, *The Arithmetic of Active Management* (1991) | 30 | 0.878 |
| Goldman Sachs market note via Yahoo Finance | 25 | 0.809 |
| **all** | **85** | **0.894** |

95% CI [0.840, 0.942]. Real published prose costs about **0.05** against
generated statements, and the intervals overlap.

**The label mix is the finding:**

| label | share |
|---|---|
| `observation` | **44%** |
| `principle` | **32%** |
| everything else combined | 24% |

Two labels carry three-quarters of real financial writing, and
`observation`/`principle` alone is **42% of all disagreement** on these
documents.

`scope` falls to 0.799 here from 0.940 on generated statements — raters cannot
agree whether an academic claim about markets is `world` or `system`, because a
paper *argues* it is universal while *demonstrating* it on one sample.

## Why the measurements could not have produced this

The night before, sixteen structural designs were tested on the same corpus:
boolean batteries, two- three- and five-family cascades, three-tier funnels,
regrouped coarse types, deeper rule sets, a `scope` field, confidence
thresholds. Every one landed within the ±0.05 noise floor or lost outright. The
best of them reached 0.898 in one run and 0.844 when repeated.

The definition pass moved **+0.090** on the full corpus and **+0.149** on a
subset, and every change came from a judgment about what these things *are*:

> a procedure belongs in a user manual · a prohibition is the negative of a
> procedure · an obligation is owed to a third party · architecture is physical
> or software construction · an assumption is a leap of faith · there are no
> opinions in a formula · an event is what happened, an observation reads across
> several

**None of that is derivable from a confusion matrix.** The measurements were
excellent at locating damage — they identified `procedure` as the collision hub,
`distinction` as the weakest label, and questions as ~50 invisible splits. They
were useless at saying what the definitions should be.

## Diminishing returns are sharp

A second round of nine further rulings of the same quality — the third-party
obligation rule, single-versus-multiple for event/observation, implementational
design for architecture, leap of faith for assumption, and others — produced
**no measurable gain**:

| | α |
|---|---|
| first definition pass | 0.954 |
| plus nine further rulings | 0.947 |

The second version wins in 36% of resamples: indistinguishable. The first pass
fixed definitions that were *broken*; the second adjusted definitions that
already worked.

## The ceiling

**≈0.95 on generated statements, ≈0.89 on real documents**, and the residue is
genuinely ambiguous sentences rather than bad definitions:

- a compatibility commitment that is both a `decision` and an `architecture`
- an incident report that is both an `event` and a reading of it
- a market claim that is both `principle` and `observation`, because the genre
  derives and demonstrates in the same breath

`observation`/`principle` survived seven separate attempts across two days: a
rename, the strip test, the generality test (reverted), a `scope` field, the
anecdotal-versus-theoretical cut, the multiple-events rule, and first-principles
narrowing. It was the largest collision in every corpus tested. On real
documents it is 42% of all remaining disagreement.

That is not a definitional failure. Finance writing is overwhelmingly claims
about how markets behave, supported by measurement, and the genre does not
separate the two.

## Data

- `2026-08-11-definition-pass-data/v4-raw.json` — 160 statements, 8 raters, two arms
- `2026-08-11-definition-pass-data/v5-raw.json` — 40 statements, batches of 10 and 5
- `2026-08-11-definition-pass-data/batchsize-raw.json` — batch-size control
- `2026-08-11-definition-pass-data/papers-raw.json` — 85 statements from three published documents
- `2026-08-11-definition-pass-data/*.js` — the workflow scripts that produced each
