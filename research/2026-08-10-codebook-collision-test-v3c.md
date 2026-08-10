---
title: Arm C — the generality test, written for principle and rejected
date: 2026-08-10
status: COMPLETE — change reverted
verdict: >
  Rejected. It resolved 5 of the 6 items it was written for and broke 5 that had
  been unanimous, so the target collision went 17 → 19. Fine α on the
  results-dense subset fell 0.871 → 0.848 and `principle`'s own α fell
  0.861 → 0.797. This is the §2.3 prediction — non-surface criteria do not
  converge — confirmed on this codebook, on the label §2.3 named.
---

# Arm C — the Generality Test

## What was changed and why

After the v3 test, `principle` had three surviving collisions. Two were judged
genuine semantic overlap no wording fixes:

- `principle` / `recommendation` (12 rater-pairs) — sentences that explain *and*
  instruct: *"training/serving skew here is almost always the tokenizer version,
  check that before you go looking at the data"*
- `principle` / `architecture` (5) — small, and already down from 17 before the
  rename

The third, `principle` / `observation` (17), was traced to a specific gap. The
strip test resolves **a measurement that also generalizes**: delete the numbers
and the sample, see what survives. It says nothing about **a causal diagnosis
with no measurement in it** — there is nothing to strip:

> "groupby().apply() stopped preserving row order after the 2.1 upgrade — that's
> why the ranks shifted with no code change."

Causal, so `principle`'s surface cue fires. But it explains one incident and
nothing beyond it, so it belongs in `case`.

The **generality test** was written to close that gap:

> Being causal is not enough; the claim must outlive its sentence. Ask whether
> it still applies to the *next* case or only to the one described.

`principle`'s cue was rewritten to lead with "standing relation" rather than
"causes, predicts, or explains", and its Excludes clause extended to name "the
diagnosis of one [occasion]".

**This was known to violate a design rule when it was made.** §2.3 records the
research finding that categories which cannot be written as a *surface* test —
something visible in the words — land near 0.45 regardless of codebook quality,
and that `principle` sits on the lowest-scoring anchor category in the published
literature (CoreSC `Model`, κ 0.43). The generality test asks the rater to judge
scope, which is not a surface property. The trade was made deliberately and
flagged in the spec before the run.

## Design

One arm, four blind raters, **the same 152 items and the same rotation offsets
as arm B**, codebook differing by one paragraph (9,516 → 10,081 chars).
Coverage 100%: 608 of 608 assignments. Arm B is the comparison throughout.

## Result: rejected

| | arm B (strip test only) | arm C (+ generality test) |
|---|---|---|
| `principle`/`observation` collisions | 17 | **19** |
| fine α, all 152 | 0.904 | 0.901 |
| coarse α, all 152 | 0.915 | 0.911 |
| fine α, results-dense subset (72) | 0.871 | **0.848** |
| coarse α, results-dense subset | 0.890 | **0.859** |
| fine α, mixed subset (80) | 0.930 | 0.943 |
| coarse α, mixed subset | 0.935 | 0.955 |
| `principle` α | 0.861 | **0.797** |
| `principle` assignments | 123 | **77** |
| `observation` assignments | 187 | **241** |

The change was made to fix one boundary. That boundary got worse.

## It worked on its targets and broke other things

Five of the six disputed items it was written for resolved to unanimity:

| item | arm B | arm C |
|---|---|---|
| S201 *"we compute the signal on the 16:00 close and fill at that same close"* | observation/principle | **observation** |
| S210 *"groupby stopped preserving row order after 2.1 — that's why the ranks shifted"* | event/observation/principle | **observation** |
| S411 *"ablations indicate the gain derives from recency weighting rather than capacity"* | observation/principle | **principle** |
| T506 *"mmlu is flat noise until roughly 1e21 flops then steps up"* | observation/principle | **principle** |
| T605 *"Capacity is the binding constraint: at $2bn the price impact consumes the gross spread"* | observation/principle | **observation** |
| S504 *"z-loss at 1e-4 kills the logit magnitude drift"* | observation/principle | observation/principle |

And five items that had been unanimous in arm B became disputed:

| item | arm B | arm C | has a number? |
|---|---|---|---|
| S004 *"Factor momentum spans stock-level momentum: … the intercept falls to 0.08%/month"* | observation | observation/principle | yes |
| S009 *"Dispersion in sell-side forecasts is a better predictor of realized volatility than of returns…"* | observation | observation/principle | yes |
| S402 *"the gpu autoscaler scales on queue depth, not utilization — one wedged job pins the pool…"* | principle | observation/principle | yes |
| S410 *"the retraining dag has no dedupe on the upstream label table, so a backfill will double-weight…"* | principle | observation/principle | no |
| T406 *"adjusted close is back-adjusted for splits and dividends both, so any threshold signal on it is contaminated"* | principle | observation/principle | no |

## Why it failed

**It cut both ways.** That is the diagnosis, and it is visible in the table
above.

*Toward `principle`* (S004, S009): a measured research result **is** a standing
relation. "Factor momentum spans stock-level momentum" describes something
general about markets *and* reports a regression intercept. The strip test says
`observation` (numbers and sample are the substance); the generality test says
`principle` (the claim outlives the sample). **Two tests, same sentence,
opposite answers.** Raters picked different ones.

*Toward `observation`* (S402, S410, T406): system-behaviour claims with no
numbers at all. Does "the gpu autoscaler scales on queue depth, not utilization"
apply to the next case, or only to *our* autoscaler? That question has no
correct answer available from the sentence, and raters split on it.

51 assignments migrated `principle` → `observation` across the run; only 6 went
the other way. `principle` lost 37% of its volume and 0.064 of its α.

## The finding

`[MEASURED]` **A criterion that cannot be checked against the surface of the
sentence introduces a judgment, and the judgment does not converge — even when
the criterion is correct in every individual case.** Every one of the five
resolutions was arguably the *right* answer. The aggregate still got worse,
because reliability is about whether independent raters land in the same place,
not about whether a careful rater can reach the right one.

This is §2.3's prediction, drawn from CoreSC's per-category spread, reproduced
in-house on the exact label §2.3 identified as most at risk.

## What remains open

The causal-diagnosis gap is real. *"groupby stopped preserving row order after
2.1, which is why the ranks shifted"* still lands in `principle` under the
reverted codebook, and it is a `case`. Closing it needs a **surface** cue — a
tense, a named artifact, a version number, something visible — not a scope
judgment. No such cue has been found yet. Recorded as open rather than solved.

## Data

- `2026-08-10-codebook-collision-data-v3c/experiment-workflow.js`
- `2026-08-10-codebook-collision-data-v3c/rater-responses-and-items.json` — all
  608 assignments and all 152 items verbatim
- `2026-08-10-codebook-collision-data-v3c/compare-b-vs-c.py` — every number above
