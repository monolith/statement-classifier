---
title: Instrument bake-off — fourteen designs on one corpus
date: 2026-08-11
status: COMPLETE
verdict: >
  Best design measured is fine α 0.898 — a flat single-choice prompt with 35
  pairwise rules, two sharpened definitions, and a `scope` field. Codebook
  quality is worth +0.045; tiering is worth +0.007; the spec's own boolean-
  battery mechanism is worth −0.092. Three families is the optimum coarse tier
  (0.918), better than two (0.874) or five (0.902). Interior tiers are strictly
  harmful. `principle` reached 0.962 from a single rewrite that anchored it on
  visible wording.
---

# Instrument Bake-off

Fourteen designs, all measured on the **same 160 statements** with **four blind
raters** each, so every comparison is like-for-like. Roughly 250 agents.

## Leaderboard

| design | fine α |
|---|---|
| **arm E — 35 rules + sharpened definitions + `scope` (flat)** | **0.898** |
| cascade-3 — 3 families → fine, baseline codebook | 0.884 |
| single choice of 15 + status | 0.877 |
| cascade — 5 families, thin coarse book | 0.877 |
| arm B — 35 pairwise rules only (flat) | 0.875 |
| arm C — sharpened definitions only (flat) | 0.871 |
| arm D — `scope` field only (flat) | 0.865 |
| cascade — 5 families, rich coarse book | 0.858 |
| arm A — current spec baseline (flat) | 0.853 |
| two-tier — 2 families → fine | 0.833 |
| boolean battery, best of six resolution rules | 0.829 |
| funnel-3 — 3×3×3, max 3 choices per node | 0.788 |
| boolean battery, §4.1 priority order | 0.785 |
| funnel-2 — 2×3×3 | 0.726 |

## Finding 1 — codebook quality is the dominant lever

Measured against a common baseline (arm A, 0.853), on identical items:

| change | gain |
|---|---|
| 19 → 35 pairwise rules | **+0.023** |
| sharpened `distinction` + `principle` definitions | **+0.018** |
| add a `scope` field (`instance`/`system`/`world`) | **+0.012** |
| **all three together** | **+0.045** |

Close to additive (0.053 predicted, 0.045 observed), so they compose.

This is the `[VERIFIED]` codebook-depth result reproduced in-house: published
work measured κ moving **.15–.36** from codebook depth on identical documents
with an identical label set. We had 19 rules against the 75 shipped by the scheme
that reached κ 0.71.

## Finding 2 — surface anchoring is worth more per label than anything else

The sharpened definitions name the literal wording to look for and tell the
rater to abandon the label if they cannot point at it:

> **Cue.** A causal connective linking two named things — *because*, *so*,
> *drives*, *leads to*, *is why*, *accounts for*, *predicts*.
> **Surface first.** Look for the connective and the two things it joins. If you
> cannot point at both, this is probably not a `principle`.

| label | before | after |
|---|---|---|
| `principle` | 0.831 | **0.962** |
| `distinction` | 0.579 | **0.765** |

`principle` — the label responsible for more disagreement than any other in this
project — cleared the 0.95 target on its own from one rewrite.

**But the gains interfere.** `distinction` reaches 0.765 in arm C alone and falls
back to 0.604 in arm E, which contains arm C. The new
`distinction`/`observation` and `distinction`/`principle` rules pull against the
definition they were meant to support. More rules is not monotonically better.

## Finding 3 — three coarse families is an optimum, not a waypoint

Tier-1 α, asked directly:

| families | α |
|---|---|
| **3** — `meaning` / `action` / `assertion` | **0.918** |
| 5 — thin book | 0.902 |
| 5 — rich book | 0.880 |
| 2 — `practice` / `claim` | 0.874 |
| 2 — `practice` / `claim`, second run | 0.865 |

Two is worse than three, measured twice independently. With only two families
the definitional statements have nowhere clean to go and the single boundary runs
through ambiguous territory; `meaning` absorbs them and leaves `action`/`assertion`
a sharper cut.

**A methodological warning.** `practice`/`claim` was selected by searching
partitions to maximise *derived* coarse α — rolling up single-choice fine labels
— where it scored **0.948**, the best of any cut at any k. Asked directly it
scores **0.874**. A 0.074 collapse. **Groupings optimised on roll-up statistics
do not transfer to direct questioning**, because a rater choosing among fifteen
labels reasons nothing like a rater answering a two-way question.

## Finding 4 — interior tiers are strictly harmful

| design | tier 1 | tier 2 | end-to-end | errors born t1/t2/t3 |
|---|---|---|---|---|
| cascade-3 (2 tiers) | 0.918 | — | **0.884** | 14 / — / 13 |
| funnel-3 (3 tiers) | 0.910 | 0.815 | 0.788 | 16 / **25** / 9 |
| funnel-2 (3 tiers) | 0.874 | 0.752 | 0.726 | 18 / **39** / 9 |

Both interior tiers were the dominant error source. They replaced a concrete
1-of-7 choice (13 errors in cascade-3) with an abstract 1-of-3 choice (25 and 39
errors) — narrower, and much worse.

**A tier only pays for itself if it is more reliable than the decision it
replaces.** Fewer options per decision is not the governing principle;
**concreteness beats narrowness**. A question about labels with real definitions
and lexical markers is easier than a question about families invented to group
them.

## Finding 5 — thin beats rich at abstract tiers, rich beats thin at concrete ones

The five-family coarse book was written twice: once as one-line questions plus a
gloss list, once with cues, exclusions, surface tests, exemplars and ten
separation rules.

| coarse book | tier-1 α | end-to-end |
|---|---|---|
| **thin** | **0.902** | **0.877** |
| rich | 0.880 | 0.858 |

The thin book won by 0.022. Meanwhile at the fine stage, where full definitions
are used, cascade-3 produced only 13 errors once the family was agreed.

Working explanation: **exclusions name the competitor.** "Excludes: a standing
relation that holds beyond the occasion → `model`" tells a rater to consider
`model` on a sentence where they might never have thought of it. At a concrete
decision that trade is worth it. At an abstract one it is not.

## Finding 6 — the spec's own mechanism loses

Covered fully in `2026-08-11-boolean-battery-test.md`. §4.1's independent
booleans plus priority resolution measured **0.785** against 0.877 for single
choice, and the §4.1 priority order is worse than resolving alphabetically. Per-
test agreement is good (eleven of fifteen above 0.87); the loss is entirely in
recombination.

Retained for the one thing it does that nothing else can: **38% of statements
fire two or more tests**, and asked separately raters say yes to both.

## What did not work, recorded so it is not retried

| attempt | result |
|---|---|
| generality test on `principle` (arm C, earlier) | 17 → 19 collisions, reverted |
| authority recut of `evidenced`/`settled` | 21 → 56 collisions, reverted |
| base-rate hint in the battery prompt | 27% no-fire, run discarded |
| rich coarse codebook | −0.022 against thin |
| interior tier, 3 sub-groups | −0.096 against no interior tier |
| two-family root | −0.044 against three families |
| `background` rewritten as a last-resort residual | arm A 0.853 vs 0.877 before the change — **needs isolated testing** |

Six of these seven are elaborations that made the instrument reason *more*.
Every one lost.

## Honest position on the 0.95 target

Best measured: **0.898**.

Ruled out as routes to 0.95, with measurements rather than opinion:

- **Fewer labels** — the best single merge buys +0.007; collapsing 15 → 9
  reaches 0.927 and destroys the taxonomy's usefulness
  (`2026-08-11-what-limits-agreement.md`).
- **Splitting compound statements** — compound sentences score *higher* than
  simple ones (0.881 vs 0.871), and 45+ word sentences score 0.943 against 0.850
  for 20–30 word ones. Splitting removes the surface cues that make statements
  classifiable.
- **Regrouping the coarse tier** — three families is the optimum and it is
  already in use.
- **Tiering** — worth +0.007 at best, negative beyond two tiers.
- **The boolean battery** — worth −0.092.

The single unexhausted lever is **surface anchoring**, which took one label from
0.831 to 0.962. Whether it generalises to all fifteen is the open question; a run
applying it to every cue is in flight at time of writing.

If it does not generalise, the honest conclusion is that ~0.90 is the ceiling for
a fifteen-label scheme on conversational and documentary prose, and the target
should move rather than the taxonomy.
