---
title: Codebook collision test — do the eighteen definitions separate?
date: 2026-08-10
status: COMPLETE
verdict: fine α 0.778, coarse α 0.866. `mechanism` is fine; the `claim` triple is the problem.
---

# Codebook Collision Test

Measures whether the eighteen definitions in `docs/SPECIFICATION.md` §3.2 can be
applied consistently, and which pairs actually collide.

## Method

- **72 statements**, generated in six batches of twelve by agents that never saw
  the taxonomy. Sampled by SOURCE, not by category — a quant paper's results, a
  hedge-fund risk policy, a Slack backtest-debugging thread, an ML paper, an ML
  platform runbook/ADR, and an ML training-run Slack thread. Generating items
  from the label set would have manufactured the separation being measured.
- **4 blind raters**, each given the shipped §3.2 + §3.3 codebook verbatim
  (12,906 chars) and nothing else. No answer key exists, so none could leak.
- **Item order rotated per rater** to keep position bias from inflating agreement.
- **Primary metric: inter-rater Krippendorff α.** Per-label figures are
  one-vs-rest binary collapses — the same method CoreSC used for its published
  per-category numbers, and comparable to them.
- Coverage 100%: every rater labelled every item.

## Headline

| tier | α | unanimity | pairwise agreement |
|---|---|---|---|
| **fine (18 labels)** | **0.778** | 0.67 | 0.81 |
| **coarse (6 types)** | **0.866** | 0.82 | 0.90 |

For scale: the argumentative-zoning scheme reached κ 0.71 with seven categories
and a 111-page codebook; CoreSC reached 0.50–0.57 with eleven.

The coarse tier scores **+0.088 above** the fine tier on the same annotations
with the mapping fixed in advance — which is the experiment §7.3 of the spec
says does not exist in the literature. It now exists for this taxonomy, on this
item set.

## Per-label reliability

| label | assigned | 1-vs-rest α | most confused with |
|---|---|---|---|
| `obligation` | 42 | 0.944 | procedure (2) |
| `mechanism` | 55 | **0.933** | recommendation (5), observation (3) |
| `prohibition` | 9 | 0.886 | decision (3) |
| `decision` | 16 | 0.868 | observation (3), prohibition (1) |
| `procedure` | 17 | 0.813 | obligation (6), recommendation (1) |
| `observation` | 19 | 0.757 | finding (3) |
| `recommendation` | 20 | 0.750 | finding (3), procedure (3), mechanism (2) |
| `finding` | 68 | 0.680 | fact (14), conclusion (9), observation (5) |
| `conclusion` | 19 | 0.607 | finding (11) |
| `fact` | 15 | 0.556 | finding (5), conclusion (2) |
| `technique` | 5 | 0.527 | finding (2), definition (1) |
| `definition` | 1 | — | technique (3) |
| `distinction` | 1 | — | fact (2) |
| `background` | 1 | — | conclusion (2) |
| `event` | 0 | — | never assigned |
| `study` | 0 | — | never assigned |
| `permission` | 0 | — | never assigned |
| `tradeoff` | 0 | — | never assigned |

## Findings

**1. `mechanism` should NOT be dropped.** It scored α **0.933**, third highest
of eighteen, on 55 assignments — the second most-used label. Its anchor category
(CoreSC `Model`) measured 0.43, the worst in that scheme, and §2.3 of the spec
predicted it would be the weak point. It is not. The surface-test definition —
requiring a causal or structural connective between named things, and explicitly
refusing to fire because a subject is *called* a model — appears to be doing the
work the anchor's weakness predicted it could not. This is the strongest single
piece of evidence in this project for the "definitions dominate" finding.

**2. The real collision is inside `claim`.** `finding` 0.680, `conclusion`
0.607, `fact` 0.556 are the three weakest measured labels, and they collide with
each other: conclusion↔finding (11 co-occurrences), fact↔finding (14),
fact↔conclusion (2). All three roll up to `claim`, which is precisely why the
coarse tier scores higher — the two-tier design is absorbing this specific
failure.

**3. `finding` is absorbing.** 68 of 288 assignments (24%), nearly double the
next label. It is behaving as the de-facto residual even though `general` exists
for that purpose. Either its definition is too broad or the raters reach for it
under uncertainty.

**4. `obligation`/`procedure` is a genuine cross-coarse leak.** `procedure` drew
6 `obligation` confusions — a rule/method boundary problem, not a within-family
one, so the coarse tier does not absorb it.

**5. Four labels were never assigned:** `event`, `study`, `permission`,
`tradeoff`. Their α of 1.000 is an artifact of non-use, not evidence of quality.

## Limitations — read before acting on the numbers

- **The four unused labels are an ITEM-SET gap, not proof they are dead.** The
  six sources skewed heavily toward results, policy and debugging; they produced
  almost no dated events, no study designs, no permissions and no explicit
  two-directional tradeoffs. `definition`, `distinction` and `background` drew
  one assignment each for the same reason and their α values are meaningless.
  Retesting requires an item set that deliberately exercises all eighteen.
- **Four raters, one model family.** This measures within-family consistency
  under order variation, not cross-vendor agreement.
- **No human gold set.** This is reproducibility, not correctness. High
  agreement is compatible with everyone being wrong the same way.
- **72 items, no confidence intervals.** The per-label figures for labels with
  fewer than ~10 assignments are not resolvable.
- One-vs-rest collapses are mechanically higher than the full 18-way α and are
  comparable to CoreSC's per-category numbers, not to its 11-way figure.

## Implied changes

1. Keep `mechanism`. Keep `model`.
2. Sharpen `finding` / `conclusion` / `fact`, or merge two of them. This is the
   only cluster where the data shows a real problem.
3. Tighten `finding`'s definition against absorption, and monitor its share.
4. Add an explicit `obligation` / `procedure` separation to §3.3.
5. Re-run against an item set that exercises `event`, `study`, `permission` and
   `tradeoff` before deciding whether they survive.
