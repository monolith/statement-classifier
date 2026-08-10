# Statement Classifier — Specification v1.0

Assigns a knowledge type to a short statement. One statement in, one
classification record out. Works on statements extracted from documents and on
statements taken from conversation.

**Evidence convention.** Every claim marked `[VERIFIED]` survived three-vote
adversarial verification against a primary source; the study, the number, and
the sample are named inline. Claims marked `[MEASURED]` come from the in-house
collision test in `research/`, which measured this codebook rather than a
published one. Claims marked `[DESIGN]` are engineering decisions
with no supporting measurement — they are labelled that way deliberately, and
§9 lists every one of them in a single place. Nothing here is presented as
evidence-backed unless a number is attached to it.

The research this cites ships in `research/`.

---

## 1. Contract

```
classify(statement: str, context?: str) -> Classification
```

**Input.** One statement. Optional surrounding context, used only to resolve
references — never to reclassify the neighbours.

**Output.** A classification record:

```json
{
  "statement_sha256": "…",
  "fine": "observation",
  "coarse": "case",
  "tests": {"is_observation": true, "is_result": false, "…": false},
  "tests_fired": 1,
  "multi_fire": false,
  "modality": null,
  "flags": ["negative_result"],
  "taxonomy_version": "sc-v1",
  "prompt_version": "sc-v1-classify-0001",
  "classifier_model": "<model id>",
  "classified_at": "2026-08-10T00:00:00Z"
}
```

**Append, never overwrite.** A classification is a pure function of
`(statement, prompt_version, classifier_model)`. Re-running with a different
triple appends a new record; it does not replace the old one. Consumers pick
the record whose stamps they trust.

**The classifier does not judge truth.** It answers "what kind of statement is
this", never "is this correct". Epistemic status lives elsewhere.

---

## 2. The taxonomy

Six coarse types. Fifteen fine labels, each mapping to exactly one coarse
type. The mapping is a lookup table, not a judgment.

### 2.1 Coarse types

| Coarse | The question it answers |
|---|---|
| `case` | What happened, on one occasion? |
| `rule` | What must, may, or must not happen? |
| `method` | How is something done? |
| `concept` | What does this term mean? |
| `model` | What drives this, how is it built, what does it take for granted? |
| `general` | — assigned by code when no test fires |

### 2.2 Fine labels, with measured reliability where it exists

Each fine label is anchored, where possible, on a category that has a published
inter-annotator agreement figure. `κ` below is the measured agreement for the
*anchor* category in the cited scheme — not for this label as written here.

| Fine label | Coarse | Anchor κ | Anchored on |
|---|---|---|---|
| `observation` | case | **0.79** | CoreSC `Observation` [VERIFIED] |
| `event` | case | — | [DESIGN] — concrete by construction (actor + time) |
| `obligation` | rule | — | [DESIGN] — deontic modal is a surface cue |
| `prohibition` | rule | — | [DESIGN] — deontic modal is a surface cue |
| `decision` | rule | — | [DESIGN] — a settled choice governs what happens next; note it is the one `rule` label with NO deontic modal to key on (§3.3) |
| `procedure` | method | **0.74** | CoreSC `Method` [VERIFIED] |
| `recommendation` | method | — | [DESIGN] |
| `definition` | concept | **0.81** | CoreSC `Object` [VERIFIED] |
| `distinction` | concept | — | [DESIGN] |
| `background` | concept | **0.87** | CoreSC `Background` [VERIFIED] |
| `principle` | model | — | [DESIGN] — the causal idea the model runs on; carries `status` (§2.6) |
| `architecture` | model | — | [DESIGN] — compositional cue (*is composed of*) |
| `formula` | model | — | [DESIGN] — an equation is the most surface-detectable cue in the set |
| `assumption` | model | — | [DESIGN] — marker words (*assumes*, *conditional on*) |
| `dependency` | model | — | [DESIGN] — marker words (*requires*, *depends on*) |

Source for all CoreSC figures: Liakata et al., LREC 2010, per-category
one-vs-rest Cohen's κ, 41 chemistry/biochemistry papers, expert annotators.
AZ-II: Teufel et al., EMNLP 2009, 15 categories, three annotators, N=3745.
Both in `research/2026-08-10-annotation-taxonomy-research-runA.md`.

### 2.3 What the reliability spread means for this design

`[VERIFIED]` Within a single annotation scheme, per-category reliability varies
by a factor of two, and the abstract categories are systematically the worst:
CoreSC measured `Conclusion` 0.89, `Background` 0.87, `Object` 0.81,
`Observation` 0.79, `Result` 0.78, `Method` 0.74 — against `Hypothesis` 0.46,
`Motivation` 0.46, `Model` 0.43.

Three consequences, all binding on this spec:

1. The `model` coarse type is the known weak point. Its anchor is the lowest
   measured category in the scheme. §3 therefore defines `principle` primarily as
   a surface test — does the statement contain a causal or structural connective
   linking two named things — rather than as a judgment about explanatory intent.
   `[MEASURED]` This was tested directly. A non-surface criterion — the
   **generality test**, asking whether a causal claim outlives the occasion it
   describes — was written for `principle` and measured *worse* than the surface
   definition it replaced (§2.9). The prediction above held on this codebook,
   on the label the prediction named.
2. Any category that cannot be written as a surface test should be expected to
   land near 0.45 regardless of codebook quality.
3. Per-category agreement must be reported separately in evaluation. A single
   aggregate number hides exactly the failure this spread predicts.

### 2.4 `general`

`general` is assigned **by code**, when no fine test fires. It is never offered
to the model, never named in the prompt, and has no definition the model can see.

`[VERIFIED]` This is not stylistic. A study of four frontier models given a
named fallback plus the instruction "assign it for unknown cases" recorded a
96.1% full-agreement ratio with Fleiss κ of **−0.001**, and the four models
jointly identified the minority class **zero** times, missing 75% of it against
a human reference (MultiSoc-4D, 58k+ comments; ChatGPT, Gemini, Claude, Grok).
The paper ran no ablation, so the *causal* reading was refuted 0-3 in
verification — treat this as a strong warning rather than a proven mechanism.
Details in `research/2026-08-10-classifier-design-research-runC.md`.

`general`'s share of the corpus is a standing health metric (§7).

### 2.5 What was cut, and the two gaps it leaves

`[MEASURED]` Four labels were removed after the collision test
(`research/2026-08-10-codebook-collision-test.md`):

- `conclusion` merged into `finding`. They were the worst-colliding pair in the
  set (11 co-occurrences; α 0.607 and 0.680) and the measured-versus-inferred
  distinction between them did not survive contact with real statements.
- `study`, `permission`, `tradeoff` dropped as not carrying their weight for this
  corpus. Note honestly: all three also drew **zero** assignments in the test, but
  that was an item-set coverage gap, so the test did not independently show them
  to be weak — the decision is editorial.
- `event` retained deliberately, for historical recording, despite also drawing
  zero assignments for the same coverage reason.

Two gaps this leaves, both routed to `general`:

1. **`model` now has exactly one fine label.** For that branch the fine and
   coarse tiers carry identical information — a degenerate tier, harmless but
   worth knowing. (Superseded: `model` now carries five labels — see §2.7.)
2. **Permission-shaped statements have no home.** "Analysts may exceed the
   intraday limit provided the book is flat at close" carries a deontic modal but
   is neither required nor prohibited. It will land in `general`, or be pulled
   into `obligation` by the modal. Watch `general`'s share for permission-heavy
   corpora such as policy documents.

`[DESIGN]` Merging `conclusion` into `finding` cuts against the other change in
this revision — `finding` already took 24% of all assignments and was behaving
as a de-facto residual, and widening it increases that risk. The merged
definition below therefore tightens its exclusions against `fact` and
`observation` rather than loosening them. Whether that holds is a re-test, not a
claim.

### 2.6 `status`, and why `claim` no longer exists

`[DESIGN]` §1 says this classifier does not judge truth and that epistemic
status lives elsewhere. An earlier revision nonetheless had a `claim` coarse type
whose three labels — `fact`, `finding`, `proposition` — differed mainly by *how
established* a statement was. That contradicted the contract.

They are now one field on `principle`:

```
status: proposition | finding | fact
```

- `proposition` — put forward, not established. Hedged: *might*, *could*, *we
  propose*, *worth testing*.
- `finding` — established by the work at hand. Carries its own evidence.
- `fact` — settled outside this work.

The gain is that a principle's lifecycle stops being a retyping. "More cars in the
lot predicts stronger same-store sales" begins as `proposition`, becomes
`finding` when the backtest holds, and may harden to `fact`. As three separate
types that path required changing what the statement *is*; as a status it is an
update, which is what actually happened — and it makes "show me every principle
still at `proposition`" a query rather than an archaeology exercise.

`[DESIGN]` **One field, not two.** `fact` and `finding` differ by provenance
(settled elsewhere versus established here) as much as by maturity, so there is
an argument for splitting `status` and `provenance` into separate fields.
`[VERIFIED]` Against that: the closest published two-axis design assumed its
axes were orthogonal and measured them statistically dependent (Fisher's exact,
p<0.0001), collapsing into a few dominant cells. Start with one field; split only
if the data demands it.

**`[MEASURED]` Known gap, and it is worse than predicted.** A measured result
that drives nothing — "the signal earned 0.82 Sharpe net of costs over the full
sample" — has no obvious home now. `claim`/`finding` was where it used to go.
This was expected to fall to `general`; the control run shows it does not.
Raters do not reach for the escape hatch (0 of 288). They split, 37 disagreeing
rater-pairs between `observation` and `principle`, the largest collision
measured in any run — and on a research corpus these statements are roughly a
quarter of the text. So `general`'s share is **not** the metric that surfaces
this. Fine-tier α on a results-dense corpus is. See §2.7 and
`research/2026-08-10-codebook-collision-control.md`.

### 2.7 What the second collision test changed

`[MEASURED]` The restructure in §2.5–2.6 was re-tested on 80 fresh statements
with four blind raters
(`research/2026-08-10-codebook-collision-test-v2.md`). Agreement rose on both
tiers: fine α 0.778 → **0.858**, coarse α 0.866 → **0.927**, unanimity 0.67 →
0.78. No statement fell outside the taxonomy (0 of 320).

**`[MEASURED]` That comparison was confounded, and a control says the gain was
not the taxonomy.** The first test and the second used *different item sets*, so
the headline moved for two reasons at once. Re-running the first test's 72 items
through the second codebook holds the items fixed and isolates the taxonomy
(`research/2026-08-10-codebook-collision-control.md`):

| | fine α | coarse α |
|---|---|---|
| headline, v1 → v2 (taxonomy **and** items changed) | +0.080 | +0.061 |
| **taxonomy alone** (v1 items, both codebooks) | **+0.009** | **−0.075** |
| item set alone (v2 codebook, both item sets) | +0.071 | +0.136 |

The restructure bought approximately nothing on a fixed item set, and *lost*
ground at the coarse tier. The claim that dissolving `claim` "cost nothing" was
read off the second item set, which happens to contain few of the statements
that make it costly. On the first item set the cost is plain: `principle` and
`observation` disagreed on **37** rater pairs, the largest collision in any test
so far, concentrated entirely on empirical research results — sentences that
report a measurement *in order to* assert a generalization. `claim`/`finding`
had absorbed those. With it gone they scatter across two coarse types.

`[DESIGN]` The response is a mechanical tie-break rather than a restored label:
the **strip test** in §3.2 assigns a measured result to `observation` even when
the author generalizes from it, and reserves `principle` for the explanation
stated without its measurement. `[DESIGN]` A second contributing cause is
established: through v2 the codebook's `observation` definition still pointed
raters at `finding`, `study`, and `conclusion` — labels the restructure had
removed. Eleven such dangling pointers were found and repaired. How much of the
37 was the missing label and how much was the broken codebook is not yet
separated.

Three changes follow from that test:

- **`technique` removed**, merged into `procedure`. It measured α 0.588, the
  weakest label, with six confusions against `procedure`. This is the one change
  the data made on its own.
- **`driver` → `principle`.** `driver` measured α 0.623 and collided with
  `structure` seventeen times — the largest collision in that test. `[DESIGN]` The
  likely cause is the same ambiguity that sank `mechanism`: in engineering, a
  *driver* is a component, so the label read as machinery rather than as the
  causal idea. `principle` has no such reading. Whether the rename fixes the
  boundary is a re-test, not a claim.
- **`structure` → `architecture`.** `[DESIGN]` Naming only. `architecture` is
  the native word in ML model cards; `structure` was the more neutral term for
  portfolios. The ML reading was judged to carry more weight for this corpus.

`[DESIGN]` One risk this revision introduces: `principle` can be read
normatively. "Prefer small reversible steps" is a principle in ordinary English
but is advice, not an explanation — §3.3 now carries an explicit
`principle`/`obligation` separation for exactly that.

### 2.8 What the third collision test measured

`[MEASURED]` The changes in §2.7, plus the strip test and the eleven repaired
pointers from the control, were tested on **both** earlier item sets at once —
152 statements, four blind raters, two arms differing only in whether the strip
test was present (`research/2026-08-10-codebook-collision-test-v3.md`).

Holding the items fixed, in both directions:

| | fine α | coarse α |
|---|---|---|
| 72 results-dense items, v2 codebook (the control) | 0.787 | 0.791 |
| the same 72, v3 codebook | **0.883** | **0.874** |
| 80 mixed items, v2 codebook | 0.858 | 0.927 |
| the same 80, v3 codebook | **0.930** | 0.927 |

**+0.096 and +0.072 fine α, with the item set held fixed in each pair.** This is
what §2.7 claimed and could not show. The two renames account for most of it:

| v2 | α | v3 | α |
|---|---|---|---|
| `driver` | 0.623 | `principle` | **0.910** |
| `structure` | 0.727 | `architecture` | **0.851** |
| `procedure` | 0.760 | `procedure`, absorbing `technique` | 0.834 |

`[CAVEAT]` The renames are confounded with the pointer repair; both shipped in
the same revision and this experiment cannot separate them.

**The strip test does its job locally and disappears in aggregate.** On the
`principle`/`observation` boundary it targets: 37 disagreeing rater-pairs under
the control, 17 once the pointers and names were fixed, **11** with the strip
test — a further 35%. On aggregate α its effect is ±0.012, which four raters
cannot distinguish from noise. It is retained because the boundary it fixes is
*cross-coarse*, and the coarse tier is the one consumers read.

`[MEASURED]` Two collisions this test surfaced are new, both cross-coarse, and
both are one sentence doing two jobs — the same shape the strip test addresses.
§3.3 now carries a rule for each:

- **`principle` / `recommendation`**, 12 rater-pairs. *"training/serving skew
  here is almost always the tokenizer version, check that before you go looking
  at the data"* — an explanation with an instruction attached.
- **`decision` / `procedure`**, 7 rater-pairs. *"Models are versioned by the
  SHA-256 of the serialized artifact, not by a semantic version string"* — a
  settled choice stated as how the thing is done.

`[MEASURED]` **`event` has not been exercised by three consecutive item sets**
(2 of 608 assignments, α ≈ 0 on those two; `background` drew zero across 152
items). `event` is retained deliberately for historical recording. It is
untested, not disproven — but three item sets drawn from six source types
failing to produce it is itself a statement about how often it will fire.

### 2.9 A change that was tested and rejected

`[MEASURED]` `principle`'s three remaining collisions were reviewed after §2.8.
Two were judged genuine semantic overlap that no wording fixes
(`principle`/`recommendation`, `principle`/`architecture`). The third,
`principle`/`observation`, was traced to a specific gap: the strip test resolves
a *measurement that also generalizes*, but says nothing about a **causal
diagnosis with no measurement in it** — "groupby stopped preserving row order
after the 2.1 upgrade, which is why the ranks shifted" explains one incident and
has no numbers to strip.

A **generality test** was written for `principle` to close it: being causal is
not enough, the claim must still apply to the next case. It was tested as a
fourth arm — same 152 items, same rotation, one paragraph different
(`research/2026-08-10-codebook-collision-test-v3c.md`).

**It was rejected.** It resolved five of the six items it was written for, and
broke five others that had been unanimous:

| | with strip test only | + generality test |
|---|---|---|
| `principle`/`observation` collisions | 17 | **19** |
| fine α, all 152 | 0.904 | 0.901 |
| fine α, results-dense subset | 0.871 | **0.848** |
| fine α, mixed subset | 0.930 | 0.943 |
| `principle` α | 0.861 | **0.797** |
| `principle` assignments | 123 | **77** |

It cut both ways, which is the tell. Two previously-unanimous *measured results*
were pulled toward `principle` ("Factor momentum spans stock-level momentum…"),
because a measured relation is also a standing one — the two tests point
opposite ways on the same sentence. Three previously-unanimous *system-behaviour
claims* were pulled toward `observation` ("the gpu autoscaler scales on queue
depth, not utilization…"), because raters disagreed whether a claim about *our*
autoscaler generalizes. 51 assignments migrated from `principle` to
`observation` in total.

`[MEASURED]` **This is the §2.3 prediction confirmed on this codebook, on the
label §2.3 named.** A criterion that cannot be checked against the surface of
the sentence introduces a judgment, and the judgment does not converge — even
when the criterion is correct in every individual case. The causal-diagnosis gap
identified above is real and remains **open**; it is not worth a scope judgment
to close it.

---

## 3. Definitions

`[VERIFIED]` This section, not the label count, is what determines whether the
classifier works. Codebook depth and annotator training moved κ by **.15–.36**
on identical documents with an identical label set — trained coders with a
17-page codebook, a decision tree and four training papers reached
κ .65/.85/.87; untrained coders given one page reached .35/.49/.72. Growing the
label set from 3 to 7 cost only **.07** (Teufel & Moens, EACL 1999).

`[VERIFIED]` Definitions must be written as surface tests, not judgment calls.
Concretely-described features reached F1 **> 0.60**; features requiring
interpretive inference fell **below 0.30**, and model difficulty tracked human
inter-coder difficulty at **r = 0.61** — so human disagreement is the practical
ceiling (7 models × 121 features × 567 excerpts, arXiv 2601.12099).

`[VERIFIED]` Codebook depth is necessary but not sufficient: a 45-page codebook
with a decision tree, category semantics, pairwise-distinction rules and worked
examples still yielded only κ 0.50–0.57 (CoreSC).

### 3.1 Required shape for every definition

Each of the fifteen fine labels carries:

- **Cue** — the surface pattern, stated so a reader can check it without
  inferring intent.
- **Excludes** — at least two explicit non-firing conditions.
- **Exemplars** — one document-style statement, one conversational.

Exemplars are drawn from quantitative finance and LLM/ML research, because
those are the domains this classifier runs on. `[DESIGN]` Note the drift: the
anchor categories in §2.2 were measured on chemistry and computational-
linguistics *papers*, so the κ figures transfer to these definitions only as far
as the category shapes do. §9 records this as a weakness in the evidence base,
not as something the exemplars fix.

Pairwise separations live in §3.3, not inside each definition, so that a
boundary is stated once rather than twice and cannot drift between two entries.

### 3.2 The fifteen definitions

---

#### `observation` → `case` · anchor κ 0.79

> **Cue.** Reports something seen or measured on a particular occasion, without
> claiming it holds in general. Usually carries a time, a run, a period, or a
> named instance.
>
> **Excludes:** an explanation of why an effect exists, stated without the
> measurement behind it (→ `principle`); the description of how a measurement
> was set up (→ `procedure`).
>
> **Strip test.** An empirical result is an `observation` *even when the author
> generalizes from it*. Delete the numbers and the sample from the sentence: if
> nothing of substance survives, it was an `observation`; if a causal claim
> survives on its own, it is a `principle`.
>
> **Doc.** "Realized volatility on the book exceeded the model's 99th-percentile
> band on three consecutive sessions in March 2026."
> **Chat.** "loss spiked right after we bumped LR to 3e-4, twice in a row"

#### `event` → `case`

> **Cue.** Something happened, with a time and an actor or subject. No choice is
> being reported and nothing is being measured.
>
> **Excludes:** a settled choice (→ `decision`); a measurement taken (→
> `observation`); a recurring or generally accepted state of affairs (→
> `background`).
>
> **Doc.** "The prime broker raised margin requirements on the fund's short book
> on 14 March 2026."
> **Chat.** "training run 47 OOM'd overnight on node 3"


---

#### `obligation` → `rule`

> **Cue.** A deontic modal of requirement — *must*, *shall*, *is required to* —
> with someone accountable to it.
>
> **Excludes:** a requirement stated in the negative (→ `prohibition`); advice
> with no accountability (→ `recommendation`). A statement that merely *permits*
> rather than requires has no label of its own and falls to `general`.
>
> **Doc.** "Positions must be marked to market daily before 17:00 ET."
> **Chat.** "every eval run has to log its seed and commit hash"

#### `prohibition` → `rule`

> **Cue.** A deontic modal of forbidding — *must not*, *may not*, *never*, *is
> prohibited from*.
>
> **Excludes:** a positively-stated requirement, even where the effect is
> similar (→ `obligation`); a warning about consequences with no forbidding
> force (→ `principle`).
>
> **Doc.** "The desk may not carry overnight exposure in names below $50m ADV."
> **Chat.** "never train on anything that overlaps the eval split"


#### `decision` → `rule`

> **Cue.** A choice reported as settled, which governs what happens after it.
> Typically past-tense and agentive: *adopted*, *chose*, *approved*,
> *standardised on*, *agreed to*. This is the one `rule` label with no deontic
> modal to key on.
>
> **Excludes:** something that merely occurred, with no choice made (→ `event`);
> a choice still being proposed (→ `recommendation`); a statement carrying an
> explicit modal, which the deontic labels take instead.
>
> **Doc.** "The committee standardised on daily rebalancing after the turnover
> analysis."
> **Chat.** "we went with LoRA instead of a full fine-tune"

---

#### `procedure` → `method` · anchor κ 0.74

> **Cue.** How something is done — either ordered steps to follow, or a named
> approach used to achieve an end. `[MEASURED]` These were two labels
> (`procedure` and `technique`) until the second collision test measured
> `technique` at α 0.588, the weakest in the set, colliding with `procedure`
> six times. Merged.
>
> **Excludes:** why the approach works (→ `principle`); how a thing is assembled
> or sourced (→ `architecture`); the arithmetic that computes a value (→
> `formula`); one investigation that was run (→ `observation`); a constraint
> someone is accountable to (→ `obligation`); advice about which approach to
> pick (→ `recommendation`).
>
> **Doc.** "To build the factor: winsorize at 1%, z-score cross-sectionally,
> then neutralize by sector and size."
> **Chat.** "we use gradient checkpointing to fit the batch on one node"


#### `recommendation` → `method`

> **Cue.** Advice on what ought to be done, with no requirement force and no
> report that it was settled. Hedged: *should*, *prefer*, *is worth*, *probably
> want to*.
>
> **Excludes:** a requirement someone is accountable to (→ `obligation`); a
> choice already made (→ `decision`); a bare description of an approach (→
> `procedure`).
>
> **Doc.** "Practitioners should prefer shrinkage estimators when the sample
> covariance matrix is near-singular."
> **Chat.** "you probably want to warm up the LR over the first 2k steps"

---

#### `definition` → `concept` · anchor κ 0.81

> **Cue.** Fixes what a term means. The grammatical centre is *X is / means /
> refers to / is defined as Y*.
>
> **Excludes:** a contingent statement that could turn out false, which fixes no
> terminology (→ `principle`); a contrast drawn between two terms (→
> `distinction`).
>
> **Doc.** "The Sharpe ratio is excess return divided by the standard deviation
> of excess return."
> **Chat.** "perplexity is just exp of the mean negative log-likelihood"

#### `distinction` → `concept`

> **Cue.** Contrasts two or more terms in order to fix the boundary between
> them. Both sides are named and the difference is the payload.
>
> **Excludes:** a single term being defined (→ `definition`); two quantities
> moving against each other, or a claim that one option is better (→
> `principle`).
>
> **Doc.** "Realized volatility is measured from past returns; implied
> volatility is backed out of option prices."
> **Chat.** "RAG retrieves at query time; fine-tuning bakes it into the weights"

#### `background` → `concept` · anchor κ 0.87

> **Cue.** Context a reader needs, presented as generally accepted and not as
> the author's own contribution or measurement.
>
> **Excludes:** a term being defined (→ `definition`); a checkable claim
> advanced as the author's own (→ `principle`); a measured result from the
> present work (→ `observation`).
>
> **Doc.** "Cross-sectional momentum has been documented in equity markets since
> Jegadeesh and Titman."
> **Chat.** "transformers displaced RNNs for sequence modelling around 2018"

---

#### `principle` → `model`

> **Cue.** Asserts that one thing causes, predicts, or explains another, as the
> reason a model or conclusion works. Answers "why should this hold?"
>
> **Excludes:** how the thing is built or sourced (→ `architecture`); the equation
> that computes it (→ `formula`); what must be true for it to hold (→
> `assumption`); what it needs in order to run (→ `dependency`); a single
> measured occasion (→ `observation`).
>
> **Carries `status`** (§2.6): `proposition` when hedged or untested, `finding`
> when this work established it, `fact` when settled elsewhere. The status is not
> part of choosing this label — a principle is a principle whether or not it is proven.
>
> **Doc.** "Parking-lot vehicle counts predict same-store sales, so changes in
> counts lead reported revenue by roughly one quarter."
> **Chat.** "the whole thesis is more cars means the store is doing better"

#### `architecture` → `model`

> **Cue.** How the thing is composed, assembled, or sourced — named parts and
> how they fit. *Is composed of*, *consists of*, *is built from*, *comes from*.
>
> **Excludes:** why it works (→ `principle`); the arithmetic (→ `formula`); steps a
> reader should follow (→ `procedure`); something the build merely needs present
> (→ `dependency`).
>
> **Doc.** "Parking-lot counts are derived from daily satellite imagery, matched
> to store locations by geofence and aggregated to ticker level."
> **Chat.** "signal's built from the vendor feed plus our own geofences"

#### `formula` → `model`

> **Cue.** States how a quantity is computed — an equation, or an explicit
> arithmetic definition in prose.
>
> **Excludes:** a term's meaning with no computation given (→ `definition`); a
> reported value rather than the rule producing it (→ `observation`); ordered
> instructions to a reader (→ `procedure`).
>
> **Doc.** "Signal = z-score of the trailing 30-day change in vehicle count,
> winsorized at 1% and neutralized by sector."
> **Chat.** "it's just zscore(30d delta) then sector demean"

#### `assumption` → `model`

> **Cue.** States something taken for granted for the thing to hold. Marker
> words: *assumes*, *presupposes*, *conditional on*, *holds only if*, *provided
> that*.
>
> **Excludes:** something needed to run rather than to be true (→ `dependency`);
> a limit on where it applies, stated as a result (→ `observation` or `principle`);
> a rule someone must follow (→ `obligation`).
>
> **Doc.** "The signal assumes foot traffic converts to revenue at a stable rate
> across store formats."
> **Chat.** "this only works if the conversion rate is roughly constant"
>
> `[DESIGN]` High value for this corpus specifically: quantitative models fail
> at their assumptions far more often than at their arithmetic, and assumptions
> are usually the least recorded part of a model.

#### `dependency` → `model`

> **Cue.** States that something is required, relied on, or a prerequisite.
> Marker words: *requires*, *depends on*, *needs*, *is a prerequisite for*.
>
> **Excludes:** something taken to be true rather than needed to run (→
> `assumption`); a component the thing is made of (→ `architecture`); a rule
> compelling someone to supply it (→ `obligation`).
>
> **Doc.** "Signal construction requires the earnings calendar in order to
> suppress positions into scheduled announcements."
> **Chat.** "needs the earnings cal, otherwise we trade straight into prints"




### 3.3 Pairwise separations

`[VERIFIED]` Pairwise distinction rules are the bulk of a working codebook, not
a garnish: the scheme that reached κ 0.71 shipped **75** of them alongside a
decision tree, in 111 pages of guidelines.

`[DESIGN]` The nineteen rules below cover the pairs judged to genuinely collide.
Pairs not listed were judged non-colliding — that judgment is mine and is worth
challenging; a pair that turns out to collide in practice should be added here
rather than patched into a definition.

| Pair | The test that separates them |
|---|---|
| `observation` / `event` | Was anything measured? An observation records a quantity or behaviour; an event records that something occurred. |
| `event` / `decision` | Was a choice made? An event happened to you; a decision was chosen and constrains later action. |
| `decision` / `obligation` | Is there a modal? An obligation states a standing requirement in modal form; a decision states one was established. If both fit, the modal wins. |
| `decision` / `recommendation` | Settled or proposed? A decision is closed; a recommendation is still advice. |
| `obligation` / `prohibition` | Polarity of the modal. Requirement versus forbidding. |
| `recommendation` / `obligation` | Is anyone accountable? Advice can be ignored without violation; an obligation cannot. |
| `principle` / `architecture` | `[MEASURED]` The largest collision in the second test (17 disagreeing rater-pairs, when these were `driver`/`structure`). WHY it works versus HOW it is built. If deleting the sentence would leave you unable to explain the idea, it is a principle; if it would leave you unable to rebuild the thing, it is architecture. |
| `principle` / `obligation` | Explanatory or normative? A principle says why something holds; an obligation says someone must do something. "Prefer small reversible steps" is normative — it is a `recommendation` or `obligation`, not a principle. |
| `principle` / `recommendation` | `[MEASURED]` 12 disagreeing rater-pairs in the third test, across two coarse types. `[DESIGN]` **If the statement contains an instruction the reader could act on, it is a `recommendation` — even when it also explains why.** The explanation is context for the advice. "Overlapping returns inflate Sharpe by autocorrelation, so use Newey-West at lag 19" is a `recommendation`; drop the second clause and it becomes a `principle`. This is the mirror of the strip test: a sentence doing two jobs gets one deterministic home. |
| `decision` / `procedure` | `[MEASURED]` 7 disagreeing rater-pairs in the third test, across two coarse types. `[DESIGN]` **Does the sentence name what was chosen *instead of* something else?** Surface cues: *rather than*, *not X but Y*, *instead of*, *we standardised on*. Naming the rejected alternative makes it a `decision`; stating only how the thing is done makes it a `procedure`. "Models are versioned by artifact SHA-256, not by semantic version" names the alternative — `decision`. |
| `principle` / `assumption` | Is it the reason it works, or a precondition for it working? A principle explains; an assumption is what must hold for the explanation to survive. |
| `principle` / `observation` | `[MEASURED]` The largest collision measured in any run (37 rater-pairs in the control, 17 after repair and renaming, 11 with the strip test). Apply the **strip test** from §3.2 `observation`: delete the numbers and the sample from the sentence. If nothing of substance survives, it is an `observation` — *even if the author generalizes from it*. If a causal claim stands on its own without any measurement, it is a `principle`. `[MEASURED]` A second, scope-judging test was written for this boundary and measured worse (§2.9); do not reintroduce one without re-testing. |
| `architecture` / `formula` | Parts or arithmetic? Architecture names components; a formula computes a value. |
| `architecture` / `dependency` | Inside or outside? Architecture is what the thing is made of; a dependency is something separate it needs. |
| `assumption` / `dependency` | Must be TRUE, or must be PRESENT? An assumption is a belief the model rests on; a dependency is an input it consumes. |
| `formula` / `definition` | Does it compute? A formula produces a number; a definition fixes a meaning. |
| `definition` / `background` | Fixing a term or setting the scene? A definition pins meaning; background situates the reader. |
| `definition` / `distinction` | One term or two? A definition fixes one; a distinction separates two. |
| `obligation` / `procedure` | `[MEASURED]` A cross-coarse leak in the first test (6 disagreeing rater-pairs). A procedure tells you the steps; an obligation tells you that doing it is required. A numbered list with a *must* in it is an obligation. |

---

## 4. Mechanism

### 4.1 Independent boolean tests, resolved in code

The model answers **one independent yes/no question per fine label**, in a
single call. It is never asked to pick one of fifteen.

`[VERIFIED]` Multiclass framing measured **90% lower odds** of correct
detection than binary presence/absence framing (OR 0.10, 95% CI 0.03–0.35,
p<.001, mixed-effects model over 1.1M+ annotations, arXiv 2601.12099).

`[DESIGN]` The specific tactic of decomposing *this* label set into fifteen
binary probes is an inference from that finding, not a tested design. The cited
study compared natively-binary features against natively-multiclass ones; it did
not decompose one set into the other. A claim asserting a tested decomposition
design was refuted 1-2 in verification.

Resolution is a fixed priority order over the coarse types, applied by code:

```
case → rule → method → concept → model → claim
```

Most surface-recognizable first. `[DESIGN]` One consequence worth naming: a
dated decision fires both `is_event` and `is_decision`, and because `rule`
outranks `case`, it resolves to `decision`. That is intended — the reason to
store a decision is that it governs later action, not that it occurred — but it
means dated decisions leave the `case` bucket entirely, and `multi_fire` is the
only record that the event reading existed. Within a coarse type, the fine label whose test
fired; if several fired, the first in the table order.

- **No test fires** → `general`.
- **Two or more coarse types fire** → resolve by priority, set `multi_fire`.
  A multi-fire statement is a candidate for splitting into two statements.

### 4.2 Prompt is a frozen, versioned artifact

`[VERIFIED]` Prompt wording alone swung classification accuracy by **26–36
points** on an interpretive six-class task with temperature 0 and formatting
held constant — 20 semantically equivalent prompts produced 0.546–0.808 on one
model and 0.392–0.756 on another (arXiv 2604.16413). The same study found
interpretive tasks far more prompt-sensitive than knowledge-anchored ones.

Any change to the prompt string is a `prompt_version` bump. Records carry the
version they were produced under. Re-wording without bumping is a defect.

### 4.3 Emit label names, never letters

`[VERIFIED]` Presenting options as A/B/C/D inherits selection bias, and most of
the effect comes from the option-ID tokens rather than position: removing the
IDs cut recall standard deviation from **5.5 to 1.0** on MMLU. Shuffling does
**not** fix it (5.9 vs 5.5 baseline; worse on ARC), and a debiasing instruction
barely helps (Zheng et al., arXiv 2309.03882, 20 models).

Tests are emitted as named boolean fields. No lettered options, no ordered menu.

### 4.4 Ensembling

`[VERIFIED]` Majority voting over three models from *different* families
improved agreement with human consensus (κ 0.62 ± 0.01 vs 0.56–0.62 for
individual models); expanding to five **reduced** it (arXiv 2602.11962).

`[DESIGN]` Three-model voting is optional and off by default. When enabled, the
three must come from different families.

---

## 5. Secondary fields

### 5.1 `modality` — on rules

`required` / `permitted` / `prohibited`, populated whenever a deontic modal is
present, independent of which type test fired. Validated only on statements that
resolved to `rule`; otherwise retained but not enforced.

`[DESIGN]` No measured evidence. Deontic modals are surface cues, which is the
property associated with reliable categories (§3), but this specific field has
not been evaluated.

### 5.2 Flags

`negative_result` — the statement reports an absence, null, or no-effect
finding. `caveat` — the statement limits, scopes, or excepts something else.

`[DESIGN]` No measured evidence for either flag. `negative_result` exists
because a null finding is not distinguishable from a positive one by embedding
similarity — "X does not work" and "X works" are near neighbours — so without an
explicit marker it is unrecoverable downstream. That is a mechanism argument,
not a measurement.

### 5.3 What this classifier does not produce

- **No confidence score.** `[VERIFIED]` Verbalized confidence reliability
  depends strongly on how the model is asked, with no universal best method
  across 17 prompt methods × 10 datasets × 11 models spanning 2B–110B; the best
  method is model-dependent and small models' confidence is near-independent of
  their accuracy (arXiv 2412.14737). All of it was measured on closed-book QA,
  never on classification. Uncertainty is expressed structurally instead:
  `tests_fired == 0` is abstention, `tests_fired >= 2` is ambiguity.
- **No truth judgment, no epistemic status, no relationships between
  statements.** Out of scope by §1.

---

## 6. Conversational statements

`[VERIFIED]` Conversational text is measurably harder. Six frontier models
classifying classroom utterances into seven categories reached Cohen's κ
**0.38–0.58**, where human expert annotators on the same data exceeded **0.90**
(Vanacore & Kizilcec, arXiv 2512.19903, 800 stratified utterances). A separate
study on support conversations found expert-model weighted κ median 0.60 against
expert-expert 0.58 — comparable, but on ordinal ratings rather than single-label
classification (arXiv 2506.10150).

`[VERIFIED]` Few-shot exemplars help, but model-dependently in both size **and
sign**: across six models, κ gains ranged from +19 points to *negative* — one
model peaked at three examples then declined with more, another ended below its
zero-shot score (Vanacore & Kizilcec, Table 2). Exemplar count is therefore a
per-model tuning parameter, which conflicts directly with a single prompt used
across families.

**No evidence was found** on: resolving pronouns and ellipsis before
classification, splitting one message into several statements, or how much
surrounding context a conversational statement needs. Three separate research
angles returned nothing that survived verification. The only context datapoint
anywhere in the evidence base is a 20–30 line window used as an unablated design
choice.

`[DESIGN]` Consequently:

- Conversational input may carry an optional context window, used only for
  reference resolution.
- A statement whose references cannot be resolved is classified `general` rather
  than guessed.
- Splitting a multi-statement message is **out of scope for v1**. The caller
  supplies one statement.
- Expect conversational accuracy materially below document accuracy, and measure
  the two separately (§7).

---

## 7. Evaluation

### 7.1 Human gold set first

`[VERIFIED]` Inter-model agreement is not evidence of correctness. Two
independent demonstrations: four models agreed on 96.1% of labels with Fleiss κ
−0.001 while missing 75% of the minority class; and in a separate study models
reached inter-model Krippendorff α 0.85 against human-human 0.65 while
diverging significantly from human judgment (t(49.42)=3.615, p<.001,
Cohen's d=0.88).

The acceptance test is agreement with human labels. Cross-model agreement is a
stability check only.

Gold set requirements:

- Both strata sampled separately: document-derived and conversational.
- Rare fine labels deliberately oversampled — otherwise `general` absorbs them
  invisibly.
- At least two independent human coders, adjudicated. **Report human–human
  agreement first**; it is the ceiling, and model numbers are uninterpretable
  without it.

### 7.2 Metrics

- Krippendorff's α at the **fine** tier and the **coarse** tier, reported
  separately. `[VERIFIED]` Raw percentage agreement is biased toward schemes
  with fewer categories, so tiers cannot be compared without chance correction —
  and chance-corrected measures are themselves distorted by skew, which a
  taxonomy with a residual bucket will certainly have (Artstein & Poesio,
  Computational Linguistics 34(4)).
- **Per-category** agreement, not just aggregate. §2.3 predicts a twofold
  spread; an aggregate hides it.
- `general` share, `multi_fire` rate, per-model divergence.

### 7.3 The rollup question is open

`[MEASURED]` The in-house collision test ran exactly this experiment on this
codebook: same annotations, mapping fixed in advance, agreement measured at both
tiers. Coarse scored **0.866** against fine **0.778**. That settles it for this
taxonomy on that item set — not in general.

`[DESIGN]` It remains unestablished in the literature. The direct experiment — one
annotation set, a mapping fixed in advance, agreement measured at both tiers —
does not exist in the reviewed literature. What exists is mixed: one scheme's
collapse from 15 labels to 2 moved κ 0.65 → 0.65 (zero gain), another moved
0.71 → 0.78, and the canonical survey warns that post-hoc merging is not
equivalent to designing the coarse scheme up front, since merges are typically
chosen exactly where coders disagreed.

Measuring both tiers on the gold set answers this for this taxonomy. Until then,
the two-tier design is a bet.

### 7.4 Kill criterion, pre-registered

`[VERIFIED]` The strongest direct evidence about typed information is negative
and human. Two controlled experiments on a shipped information-typing scheme
found **no effect on task performance** — n=65 process operators, effectiveness
F(2,62)=1.16 p=.32, efficiency F(2,62)=2.02 p=.14; and n=76, "no significant
effects on accuracy, speed or evaluation scores at all." The only significant
effect was subjective preference, and even that did not beat the incumbent text
(Jansen, Korzilius, le Pair & Roest, IEEE IPCC 2002 / Document Design 4(1)).

Scope limit, raised by all three verifiers: those studies were powered for large
effects only, and typing was bundled with six other principles — so this is
absence of a large effect, not proof that typing is inert.

`[VERIFIED]` No source in the reviewed evidence isolates type labels from
anything else. Every system claiming a typing benefit bundles it with linking,
extraction, reranking, or temporal invalidation; the counterfactual — same
corpus, same retriever, labels stripped — has never been run. The one payoff
that replicates across three independent agent-memory systems is **temporal
validity**, not typing.

Therefore, before this classifier is treated as load-bearing:

1. Run the ablation. Same corpus, same retriever, same ranking; type labels
   present versus stripped. Pre-register the query classes and the minimum
   effect size.
2. **User preference does not count as a gain.** Written here before results
   exist, because the one scheme that shipped on preference failed on task.
3. If no query class improves, the classifier is decoration. Keep temporal
   validity, drop the rest.

---

## 8. Versioning

`taxonomy_version` changes when labels or their mappings change.
`prompt_version` changes on any prompt edit. `classifier_model` records what
produced the record. All three are stamped on every record, and consumers may
filter on them.

Changing the taxonomy does not invalidate stored statements — classifications
are appended, and a statement may carry several from different versions.

---

## 9. Evidence register

Everything in this spec, sorted by what backs it.

### Measured, verified, cited above

| Claim | Number |
|---|---|
| Definitions dominate label count | κ .15–.36 vs .07 |
| Surface-observable beats interpretive | F1 >0.60 vs <0.30; r=0.61 to human difficulty |
| Binary framing beats multiclass | OR 0.10 (CI 0.03–0.35) |
| Prompt wording swings accuracy | 26–36 points |
| Option-ID letters cause selection bias | SD 5.5 → 1.0 when removed |
| Named escape hatch coincides with minority collapse | 96.1% agreement, κ −0.001, 75% missed |
| Agreement ≠ correctness | two independent demonstrations |
| Three-model vote helps, five does not | κ 0.62 vs 0.56–0.62 |
| Per-category reliability varies twofold; abstract worst | 0.89 … 0.43 |
| Conversational is harder | κ 0.38–0.58 vs human >0.90 |
| Few-shot gain is model-dependent in sign | +19 points to negative |
| Verbalized confidence is prompt-dependent | 17 methods × 10 datasets × 11 models |
| Percentage agreement is biased by category count | Artstein & Poesio |
| Typed documentation showed no task benefit | n=65, n=76, both null |
| Temporal validity is the replicated payoff | across three memory systems |

### Measured on this codebook, in-house

Four runs, all 4 blind raters per arm, codebook verbatim, no answer key in
existence: **v1** (72 statements × the 18-label codebook), **v2** (80 fresh
statements × the 16-label codebook), **control** (v1's 72 × the 16-label
codebook), **v3** (all 152 × the 15-label codebook, in two arms differing only
in the strip test). 2112 assignments in total.

| Claim | Number |
|---|---|
| **v3 improves on v2 with the item set held fixed, in both directions** | fine **+0.096** (72 results-dense items), **+0.072** (80 mixed items) |
| `driver` → `principle` fixed the weakest label | α 0.623 → **0.910**, same 80 items |
| `structure` → `architecture` fixed the second-weakest | α 0.727 → **0.851**, same 80 items |
| Merging `technique` into `procedure` helped `procedure` | α 0.760 → 0.834, same 80 items |
| The strip test moves its target boundary | `principle`/`observation` 37 → 17 (repair + renames) → **11** (strip test) |
| The strip test's aggregate effect is within noise | fine −0.005, coarse +0.012, over 152 items |
| Two new cross-coarse collisions surfaced | `principle`/`recommendation` 12, `decision`/`procedure` 7; both now in §3.3 |
| **A scope-judging criterion on `principle` was tested and made things worse** | `principle`/`observation` 17 → **19**; `principle` α 0.861 → **0.797**; rejected (§2.9) |
| Non-surface criteria do not converge, even when individually correct | 5 target items resolved, 5 unanimous items broken |
| `event` is unexercised, not disproven | 2 of 608 assignments across three item sets, α ≈ 0 |
| The definitions separate at all | fine α 0.778 → **0.910**, coarse α 0.791 → **0.915**, across four runs |
| Coarse tier beats fine on the same annotations | +0.088 (v1), +0.069 (v2); mapping fixed in advance |
| **The v2 restructure did NOT improve reliability** | taxonomy alone: fine **+0.009**, coarse **−0.075** |
| **The +0.080 v1→v2 headline was the item set, not the taxonomy** | 89% of the fine-tier gain |
| Dissolving `claim` has a cost, concealed by the v2 item set | `principle`/`observation` 37 rater-pairs on v1 items, 0 on v2 items |
| `technique` was the weakest label and collided with `procedure` | α 0.588, 6 confusions; merged |
| `driver`/`structure` was v2's largest collision | 17 confusions; both since renamed |
| `mechanism` (v1, since removed) was reliable despite its 0.43 anchor | α 0.933 |
| `finding`/`conclusion` were v1's worst pair | 17 confusions; merged, then removed |
| A results-shaped label absorbs a quarter of a research corpus | `finding` 24% (v1), `observation` 23% (v2) |
| Raters do not reach for the escape hatch even when the right label is absent | 0 of 320 (v2), 0 of 288 (control) |

That last row is the methodological correction this register exists to record.
A zero escape-hatch rate was first read as evidence that no label was missing.
It is not: a missing label surfaces as a **collision**, not an escape. The
control found the collision the escape rate could not.

Caveats on all of the above: four raters per arm from one model family, no human
gold set, 72–152 items per run, no confidence intervals, and item sets that
never exercised every label. It measures reproducibility, not correctness.

Two confounds remain unresolved. The renames shipped in the same revision as the
eleven repaired pointers, so v3's +0.096/+0.072 cannot be attributed between
them. And every effect at the ±0.01 scale — the strip test's aggregate figure
in particular — is below what four raters can distinguish from noise; only the
per-boundary collision counts move far enough to read.

### Design decisions with no supporting measurement

- The five coarse types and their names.
- The fifteen fine labels, their names, and which coarse type each maps to. The
  `driver` → `principle` and `structure` → `architecture` renames are motivated
  by a measured collision but are not themselves measured.
- The strip test separating `observation` from `principle`. Its effect on the
  target boundary is measured (37 → 11); its effect on aggregate α is not
  distinguishable from noise. The decision to keep it rests on the boundary
  being cross-coarse, which is a judgment. Its proposed companion, the
  generality test, WAS measured and was rejected (§2.9).
- The `principle`/`recommendation` and `decision`/`procedure` rules in §3.3. The
  collisions are measured; the separators are not.
- Retaining `event` after three item sets failed to exercise it.
- The priority order used to resolve multiple firing tests.
- Decomposing this label set into fifteen binary probes specifically.
- `modality`, `negative_result`, `caveat`.
- Treating `general` as a code-assigned residual rather than a model-visible label
  (the *hazard* is measured; this *mitigation* is not).
- Splitting multi-statement messages being out of scope.

### Contradicted or unsupported by the evidence

- That typing improves retrieval. No source isolates it. Zero measured evidence.
- That fine→coarse rollup buys reliability. Direct experiment does not exist;
  existing evidence is mixed and confounded.
- That type-matched pairing improves contradiction detection. Zero evidence in
  either direction.
- Structured-output reliability across model families. Zero confirmed claims
  despite being explicitly researched — the largest open risk for a classifier
  that must return parseable output from several vendors.

### Known weaknesses in the evidence itself

- The annotation-reliability figures trace largely to one research lineage; this
  is not independent replication.
- All annotation evidence is humans labelling sentences inside full documents.
  This classifier types short statements shown without their document. Whether
  agreement transfers up or down is untested — a claim pointing one way was
  refuted 0-3.
- The definitions in §3.2 use quantitative-finance and LLM/ML exemplars, while
  every anchor category in §2.2 was measured on chemistry and computational-
  linguistics papers. The κ figures transfer only as far as the category
  shapes do; they were not measured on these exemplars or these domains.
- The nineteen pairwise separations in §3.3 cover the pairs judged to collide.
  That judgment is unmeasured. The scheme that reached κ 0.71 shipped 75 rules.
- The reliability numbers in §2.2 are one-vs-rest binary collapses, mechanically
  higher than the full multi-way agreement of the same scheme (κ 0.50–0.57).
  They rank categories against each other reliably; they are not absolute
  targets.
