---
title: The boolean battery — the spec's own mechanism, measured and beaten
date: 2026-08-11
status: COMPLETE
verdict: >
  §4.1 specifies independent yes/no tests per label resolved in code by priority.
  Measured against single-choice on the same 160 items, it scores fine α 0.785
  versus 0.877 — and the spec's priority order is WORSE than resolving
  alphabetically (0.801). No alternative resolution rule closes the gap; the best
  found reaches 0.829. Per-test agreement is high (0.87–0.96 for eleven of
  fifteen); the loss is entirely in the resolution step.
---

# The Boolean Battery

## What was tested and why

The spec's §4.1 describes a mechanism that has never been measured:

> The model answers **one independent yes/no question per fine label**, in a
> single call. It is never asked to pick one of fifteen.

Every reliability number in this spec, by contrast, came from asking a rater to
pick one label out of fifteen. Those are different tasks, and §4.1's is the one
we claim to ship.

The reasoning behind §4.1 is `[VERIFIED]`: multiclass framing measured **90%
lower odds** of correct detection than binary presence/absence (OR 0.10, CI
0.03–0.35, 1.1M+ annotations). But the spec already flags the leap — that study
compared *natively* binary features against *natively* multiclass ones, and did
not decompose one label set into the other. A claim asserting a tested
decomposition design was refuted 1-2 in verification at the time.

This run tests the decomposition directly.

## Design

**Five coarse families × four raters = 20 agents.** Each agent sees **one
family's definitions and nothing else** — an agent asked "is this an
`observation`?" cannot see `principle` as an alternative, which is what makes
the framing binary rather than multiclass. Same 160 items, same rotations as the
single-choice run.

**A handicap, stated up front.** Nine of the nineteen pairwise rules are
cross-family (`observation`/`principle`, `background`/`event`,
`principle`/`recommendation`). Every one names the competing label, so none can
be shown without leaking the alternatives. The battery therefore runs with only
the ten within-family rules. It is binary framing stripped of half its
disambiguation, against multiclass with all of it.

**A first attempt was discarded.** The prompt contained "most statements will
fire none of these tests, because they belong to categories you are not being
shown" — true in aggregate and a direct instruction to under-fire. It produced a
27% no-fire rate and `general` dominated the residual disagreement. Removing that
one sentence and nothing else dropped no-fire to 12%. The numbers below are the
corrected run.

## Result

| | fine α | coarse α | unanimity |
|---|---|---|---|
| single choice of fifteen | **0.877** | **0.896** | 0.82 |
| boolean battery + §4.1 priority | 0.785 | 0.805 | 0.67 |
| | **−0.092** | **−0.091** | |

## The loss is entirely in the resolution step

Per-test agreement is good. Eleven of fifteen tests exceed 0.87:

| test | α | fired |
|---|---|---|
| `prohibition` | 0.958 | 25/640 |
| `event` | 0.944 | 59 |
| `definition` | 0.938 | 34 |
| `background` | 0.932 | 15 |
| `observation` | 0.925 | 179 |
| `obligation` | 0.915 | 42 |
| `decision` | 0.904 | 33 |
| `recommendation` | 0.904 | 88 |
| `formula` | 0.876 | 43 |
| `principle` | 0.770 | 146 |
| `architecture` | 0.754 | 88 |
| `dependency` | 0.749 | 22 |
| `procedure` | 0.723 | 64 |
| `assumption` | 0.696 | 18 |
| `distinction` | **0.505** | 23 |

Raters largely agree on *whether each label applies*. They disagree on the final
answer because they fire slightly different **sets**, and priority resolution
turns a small difference in the set into a different label.

**27 of 160 items had all four raters fire a label in common and still resolve
to different answers.** Rater A fires `{observation, principle}`, rater B fires
`{principle}`; `case` outranks `model`, so A resolves to `observation` and B to
`principle` — despite both agreeing that `principle` applies.

## No resolution rule rescues it

Same fired sets, six different rules:

| resolution rule | fine α | coarse α |
|---|---|---|
| single choice (reference) | **0.877** | 0.896 |
| most reliable test wins | 0.829 | 0.840 |
| reverse priority (model first) | 0.806 | 0.824 |
| **alphabetical (null control)** | **0.801** | 0.820 |
| commonest test wins | 0.793 | 0.796 |
| rarest test wins (most specific) | 0.787 | 0.825 |
| **§4.1 priority order** | **0.785** | 0.805 |

**The spec's priority order performs worse than sorting the labels
alphabetically.** That is not a subtle finding. `case → rule → method → concept
→ model` was `[DESIGN]`, chosen as "most surface-recognizable first"; on this
evidence the ordering is actively harmful, and the whole resolve-by-priority
step is the weak link rather than the boolean framing.

## What the battery gives that single choice cannot

**38% of statements fire two or more tests.** Dual-nature is not an edge case:

| co-firing pair | count |
|---|---|
| `principle` / `recommendation` | 36 |
| `architecture` / `procedure` | 33 |
| `observation` / `principle` | 26 |
| `architecture` / `recommendation` | 21 |
| `formula` / `procedure` | 17 |
| `decision` / `principle` | 17 |

Asked separately, raters say *yes to both*. The sentence really is doing two
jobs. Under single choice this appears as disagreement; here it appears as
information.

That is the one durable argument for keeping the battery: not agreement, but
**multi-label output**. If the wiki wants to know that a statement both explains
and instructs, the battery says so and single choice cannot.

## Consequences for the spec

1. `[MEASURED]` §4.1's mechanism, as specified, is **0.092 worse** than the
   simplest alternative. It should not be presented as the design without this
   number attached.
2. `[MEASURED]` The §4.1 priority order is worse than alphabetical. If a
   priority order is retained, "most reliable test wins" is the best of the six
   tried (0.829) and is derivable from measured per-test α.
3. `[MEASURED]` `distinction` scores **0.505** as an isolated test — by far the
   worst — confirming from a second direction that its definition, not its
   boundaries, is the problem.
4. The comparison is not perfectly clean: the battery ran without the nine
   cross-family rules. They cannot be given to it without destroying the binary
   condition, so this handicap is intrinsic to the design rather than an
   artefact of the test.

## Data

- `2026-08-11-boolean-battery-data/experiment-workflow.js`
- `2026-08-11-boolean-battery-data/rater-responses-and-items.json` — 3200 rows,
  20 agents
- `2026-08-11-boolean-battery-data/analyze-battery.py`
