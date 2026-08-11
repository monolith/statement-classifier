---
title: The status ladder — does it separate, and does asking for it cost type agreement?
date: 2026-08-11
status: COMPLETE — both changes accepted
verdict: >
  Status reaches α 0.896, higher than the type taxonomy on the same items
  (0.877). Asking for status IMPROVED type agreement rather than degrading it
  (+0.036 fine, +0.056 coarse). `floated`/`proposed` — predicted to be the weak
  boundary — is the least confused pair in the ladder at 2 rater-pairs. Both
  predictions going in were wrong, in the same direction.
---

# The Status Ladder

Two things were unknown and neither could be answered from the existing corpora:

1. **Does `floated` separate from `proposed`?** They differ only by degree of
   specification, and every boundary this project has lost has been a degree
   boundary — `fact`/`finding` collided 14 times on exactly that shape in v1.
2. **Does asking for status degrade type agreement?** Every number in the spec
   to this point came from type-only runs. If a second question costs 0.05 of
   type α, the two-field design is far more expensive than it looks.

## Design

**160 fresh statements, eight sources, generated blind.** Generators were told
what the *source* is and to write it faithfully; they never saw the taxonomy or
the status vocabulary. Sampling by source rather than by category is what keeps
an item set from manufacturing the separation being measured.

Three sources were chosen specifically because their natural content is a label
no earlier item set had exercised:

| source | 20 items each | reaches |
|---|---|---|
| desk brainstorm (Slack, alt-data ideas) | | `floated` |
| internal RFC / design document | | `proposed` |
| quant research results section | | `evidenced` |
| platform reference doc + glossary | | `settled` |
| ML team channel during a training run | | mixed register |
| **incident postmortem** | | `event` |
| **new-analyst onboarding handbook** | | `background` |
| **two-way comparison memo** | | `distinction` |

**Two arms over the same items, four blind raters each:**

- **arm T** — type only. The baseline *for these items*.
- **arm TS** — type and status together.

Arm T exists because comparing arm TS against α 0.904 from a different corpus is
the confound that wrecked the v1→v2 comparison. Rotation offset 37 (prime
against 160). Coverage 100%: 640 + 640 assignments.

`n/a` was on the status ballot deliberately. Some statements — "positions must be
marked to market daily" — are not the kind of thing that gets more or less
established, and forcing a rung would add noise. The control run established that
raters do not reach for an escape hatch even when they should, so a *used* `n/a`
would mean something.

## Result 1: asking for status improves type agreement

| | fine α | coarse α | unanimity |
|---|---|---|---|
| arm T — type only | 0.841 | 0.840 | 0.77 |
| arm TS — type + status | **0.877** | **0.896** | 0.82 |
| | **+0.036** | **+0.056** | |

The main risk in the two-field design inverted. Both tiers moved in the same
direction and the coarse effect is the larger one.

**Likely mechanism, unproven:** with nowhere to record how established a
statement is, raters fold that judgment into the type choice — is this an
`observation` or a `principle`? Given a field for it, the type decision gets
cleaner. This is a hypothesis the experiment does not test.

**Honest scale:** +0.036 is roughly three times the arm C effect that was
correctly called noise, and the coarse figure is larger again. Four raters, no
confidence intervals. The direction is more solid than the magnitude.

## Result 2: the ladder separates, and the weak boundary was not the predicted one

**Status α 0.896** over five values including `n/a` — higher than the fifteen-label
type taxonomy manages on the same statements (0.877).

| rung | assigned | α |
|---|---|---|
| `floated` | 34 | **0.938** |
| `settled` | 193 | 0.914 |
| `evidenced` | 319 | 0.906 |
| `proposed` | 85 | 0.851 |
| `n/a` | 9 | 0.662 |

Confusions:

| pair | rater-pairs |
|---|---|
| `evidenced` / `settled` | 21 |
| `evidenced` / `proposed` | 20 |
| `proposed` / `settled` | 11 |
| `floated` / `proposed` | **2** |

`floated`/`proposed` was flagged as the boundary most likely to fail. It is the
*least* confused pair in the ladder. Merging the two moves α from 0.896 to
0.897 — the fourth rung costs nothing measurable and buys real resolution, so it
stays.

The genuine difficulty is at the top, between `evidenced` and `settled`: "backed
by evidence" versus "indisputable" is a degree boundary with no surface cue, and
it behaves like one.

## Result 3: status is dependent on type but does not collapse

§2.6 of the spec cites a published two-axis design that failed because its axes
proved statistically dependent and collapsed into a few dominant cells. The same
test, run here over all 640 type/status pairs:

- **Cramér's V = 0.595** (χ² = 905.1, 16 types × 5 rungs)
- **Mutual information 0.845 bits** of status's 1.721 bits of entropy
- **49% of status is predictable from type; 51% is not**

Dependent, but not collapsed. Where the independent half lives, as residual
entropy of status given type:

| type | n | bits |
|---|---|---|
| `dependency` | 7 | 1.84 |
| `procedure` | 48 | 1.74 |
| `recommendation` | 94 | 1.73 |
| `principle` | 44 | 1.72 |
| `architecture` | 18 | 1.53 |
| `distinction` | 9 | 1.39 |
| `decision` | 29 | 1.18 |
| `general` | 14 | 1.00 |
| `formula` | 3 | 0.92 |
| `obligation` | 44 | 0.85 |
| `event` | 43 | 0.82 |
| `prohibition` | 12 | 0.65 |
| `background` | 35 | 0.50 |
| `observation` | 196 | 0.19 |
| `assumption` | 4 | 0.00 |
| `definition` | 40 | **0.00** |

Status carries almost everything on proposals, approaches and causal claims —
exactly where a wiki needs it. It is a constant on `definition` (100% `settled`)
and near-constant on `observation` (97% `evidenced`). An argument for scoping the
field, not for dropping it.

**`n/a` was used 9 times in 640 (1.4%).** Status applies to nearly every
statement, including rules and events. The exception is `general`, 50% `n/a`,
which is consistent with `general` being a residual rather than a kind.

## Result 4: coverage, for the first time

All fifteen labels were exercised. The three that had never fired:

| label | across the earlier 152 items | here |
|---|---|---|
| `event` | 2 | **45** |
| `background` | **0** | **35** |
| `distinction` | 7 | **17** |

The new sources did their job, and none of them was told what to produce.

## What the new coverage exposed

Type α on these 160 items is **0.841** (arm T), against 0.904 on the earlier 152.
The item set is broader and harder, and two collisions appear that no previous
run could have seen because the labels had never fired:

| pair | rater-pairs | note |
|---|---|---|
| `observation` / `principle` | 14 | the known one |
| **`background` / `event`** | **11** | new — a handbook's "how the desk got here" prose reads as both |
| `distinction` / `principle` | 7 | new |
| `distinction` / `observation` | 7 | new |
| `architecture` / `definition` | 6 | new |

Type α by source, arm T:

| source | α |
|---|---|
| rfc-doc | 0.899 |
| postmortem | 0.873 |
| ml-chat | 0.854 |
| onboarding-handbook | 0.854 |
| comparison-memo | 0.773 |
| reference-doc | 0.767 |
| brainstorm-desk | 0.675 |
| **research-results** | **0.642** |

Research results are the hardest source, again, on a fourth independent item
set. That is the `observation`/`principle` boundary and it has now survived every
attempt to fix it.

Status α by source shows the mirror image — the ladder is near-perfect where a
source sits at one rung and hardest where a source mixes:

| source | status α | dominant rungs |
|---|---|---|
| reference-doc | **1.000** | settled 80/80 |
| research-results | **1.000** | evidenced 76/80 |
| ml-chat | 0.929 | evidenced, proposed, settled |
| brainstorm-desk | 0.871 | evidenced, floated, proposed |
| rfc-doc | 0.858 | proposed, evidenced |
| postmortem | 0.854 | evidenced |
| onboarding-handbook | 0.735 | settled |
| **comparison-memo** | **0.460** | evidenced 65/80 |

The comparison memo is the outlier worth watching: raters agreed it was mostly
`evidenced` but disagreed heavily at the margin, and it is also the source where
`distinction` first appeared in volume.

## Data

- `2026-08-11-status-ladder-data/experiment-workflow.js` — generation and both arms
- `2026-08-11-status-ladder-data/rater-responses-and-items.json` — all 1280
  assignments and all 160 items verbatim
- `2026-08-11-status-ladder-data/analyze-status.py` — every number above
