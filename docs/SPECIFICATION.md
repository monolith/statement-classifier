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

Six coarse types. Sixteen fine labels, each mapping to exactly one coarse
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
| `technique` | method | **0.76** | AZ-II `OWNMTHD` [VERIFIED] |
| `recommendation` | method | — | [DESIGN] |
| `definition` | concept | **0.81** | CoreSC `Object` [VERIFIED] |
| `distinction` | concept | — | [DESIGN] |
| `background` | concept | **0.87** | CoreSC `Background` [VERIFIED] |
| `driver` | model | — | [DESIGN] — replaces `mechanism`; carries `status` (§2.6) |
| `structure` | model | — | [DESIGN] — compositional cue (*is composed of*) |
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
   measured category in the scheme. §3 therefore defines `mechanism` as a
   surface test (does the statement contain a causal or structural connective
   linking two named things) rather than as a judgment about explanatory intent.
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
   worth knowing. If `mechanism` is ever cut, `model` goes with it.
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

They are now one field on `driver`:

```
status: proposition | finding | fact
```

- `proposition` — put forward, not established. Hedged: *might*, *could*, *we
  propose*, *worth testing*.
- `finding` — established by the work at hand. Carries its own evidence.
- `fact` — settled outside this work.

The gain is that a driver's lifecycle stops being a retyping. "More cars in the
lot predicts stronger same-store sales" begins as `proposition`, becomes
`finding` when the backtest holds, and may harden to `fact`. As three separate
types that path required changing what the statement *is*; as a status it is an
update, which is what actually happened — and it makes "show me every driver
still at `proposition`" a query rather than an archaeology exercise.

`[DESIGN]` **One field, not two.** `fact` and `finding` differ by provenance
(settled elsewhere versus established here) as much as by maturity, so there is
an argument for splitting `status` and `provenance` into separate fields.
`[VERIFIED]` Against that: the closest published two-axis design assumed its
axes were orthogonal and measured them statistically dependent (Fisher's exact,
p<0.0001), collapsing into a few dominant cells. Start with one field; split only
if the data demands it.

**Known gap.** A measured result that drives nothing — "the signal earned 0.82
Sharpe net of costs over the full sample" — has no obvious home now. It is not a
single-occasion `observation`, and `claim` was where it used to go. Such
statements will fall to `general`. `general`'s share is the metric that will
show whether this matters (§7).

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

Each of the sixteen fine labels carries:

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

### 3.2 The sixteen definitions

---

#### `observation` → `case` · anchor κ 0.79

> **Cue.** Reports something seen or measured on a particular occasion, without
> claiming it holds in general. Usually carries a time, a run, a period, or a
> named instance.
>
> **Excludes:** a statement that generalizes past the instance (→ `finding`);
> the description of how an investigation was set up (→ `study`); a judgment
> drawn from what was seen (→ `conclusion`).
>
> **Doc.** "Realized volatility on the book exceeded the model's 99th-percentile
> band on three consecutive sessions in March 2026."
> **Chat.** "loss spiked right after we bumped LR to 3e-4, twice in a row"

#### `event` → `case`

> **Cue.** Something happened, with a time and an actor or subject. No choice is
> being reported and nothing is being measured.
>
> **Excludes:** a settled choice (→ `decision`); a measurement taken (→
> `observation`); a recurring or general state of affairs (→ `fact`).
>
> **Doc.** "The prime broker raised margin requirements on the fund's short book
> on 14 March 2026."
> **Chat.** "training run 47 OOM'd overnight on node 3"


---

#### `obligation` → `rule`

> **Cue.** A deontic modal of requirement — *must*, *shall*, *is required to* —
> with someone accountable to it.
>
> **Excludes:** a requirement stated in the negative (→ `prohibition`); an
> option rather than a requirement (→ `permission`); advice with no
> accountability (→ `recommendation`).
>
> **Doc.** "Positions must be marked to market daily before 17:00 ET."
> **Chat.** "every eval run has to log its seed and commit hash"

#### `prohibition` → `rule`

> **Cue.** A deontic modal of forbidding — *must not*, *may not*, *never*, *is
> prohibited from*.
>
> **Excludes:** a positively-stated requirement, even where the effect is
> similar (→ `obligation`); a warning about consequences with no forbidding
> force (→ `mechanism` or `finding`).
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

> **Cue.** Ordered steps for bringing something about, meant to be repeated.
> Imperative or sequential.
>
> **Excludes:** a named approach with no steps given (→ `technique`); one
> investigation that was run (→ `study`); a constraint on how something may be
> done (→ `obligation`).
>
> **Doc.** "To build the factor: winsorize at 1%, z-score cross-sectionally,
> then neutralize by sector and size."
> **Chat.** "to repro: pull the 40k checkpoint, run eval.py with --temp 0"

#### `technique` → `method` · anchor κ 0.76

> **Cue.** Names an approach, method or device used to achieve something,
> without laying out steps.
>
> **Excludes:** an ordered step list (→ `procedure`); an explanation of *why*
> the approach works (→ `mechanism`); advice to adopt it (→ `recommendation`).
>
> **Doc.** "Volatility targeting scales position size inversely to trailing
> realized volatility."
> **Chat.** "we use gradient checkpointing to fit the batch on one node"

#### `recommendation` → `method`

> **Cue.** Advice on what ought to be done, with no requirement force and no
> report that it was settled. Hedged: *should*, *prefer*, *is worth*, *probably
> want to*.
>
> **Excludes:** a requirement someone is accountable to (→ `obligation`); a
> choice already made (→ `decision`); a bare description of an approach (→
> `technique`).
>
> **Doc.** "Practitioners should prefer shrinkage estimators when the sample
> covariance matrix is near-singular."
> **Chat.** "you probably want to warm up the LR over the first 2k steps"

---

#### `definition` → `concept` · anchor κ 0.81

> **Cue.** Fixes what a term means. The grammatical centre is *X is / means /
> refers to / is defined as Y*.
>
> **Excludes:** a contingent statement that could turn out false (→ `fact`); an
> explanation of why something works (→ `mechanism`); a contrast drawn between
> two terms (→ `distinction`).
>
> **Doc.** "The Sharpe ratio is excess return divided by the standard deviation
> of excess return."
> **Chat.** "perplexity is just exp of the mean negative log-likelihood"

#### `distinction` → `concept`

> **Cue.** Contrasts two or more terms in order to fix the boundary between
> them. Both sides are named and the difference is the payload.
>
> **Excludes:** a single term being defined (→ `definition`); two quantities
> moving against each other (→ `tradeoff`); a claim that one is better (→
> `finding` or `conclusion`).
>
> **Doc.** "Realized volatility is measured from past returns; implied
> volatility is backed out of option prices."
> **Chat.** "RAG retrieves at query time; fine-tuning bakes it into the weights"

#### `background` → `concept` · anchor κ 0.87

> **Cue.** Context a reader needs, presented as generally accepted and not as
> the author's own contribution or measurement.
>
> **Excludes:** a term being defined (→ `definition`); a specific checkable
> proposition (→ `fact`); a result from the present work (→ `finding`).
>
> **Doc.** "Cross-sectional momentum has been documented in equity markets since
> Jegadeesh and Titman."
> **Chat.** "transformers displaced RNNs for sequence modelling around 2018"

---

#### `driver` → `model`

> **Cue.** Asserts that one thing causes, predicts, or explains another, as the
> reason a model or conclusion works. Answers "why should this hold?"
>
> **Excludes:** how the thing is built or sourced (→ `structure`); the equation
> that computes it (→ `formula`); what must be true for it to hold (→
> `assumption`); what it needs in order to run (→ `dependency`); a single
> measured occasion (→ `observation`).
>
> **Carries `status`** (§2.6): `proposition` when hedged or untested, `finding`
> when this work established it, `fact` when settled elsewhere. The status is not
> part of choosing this label — a driver is a driver whether or not it is proven.
>
> **Doc.** "Parking-lot vehicle counts predict same-store sales, so changes in
> counts lead reported revenue by roughly one quarter."
> **Chat.** "the whole thesis is more cars means the store is doing better"

#### `structure` → `model`

> **Cue.** How the thing is composed, assembled, or sourced — named parts and
> how they fit. *Is composed of*, *consists of*, *is built from*, *comes from*.
>
> **Excludes:** why it works (→ `driver`); the arithmetic (→ `formula`); steps a
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
> a limit on where it applies, stated as a result (→ `observation` or `driver`);
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
> `assumption`); a component the thing is made of (→ `structure`); a rule
> compelling someone to supply it (→ `obligation`).
>
> **Doc.** "Signal construction requires the earnings calendar in order to
> suppress positions into scheduled announcements."
> **Chat.** "needs the earnings cal, otherwise we trade straight into prints"




### 3.3 Pairwise separations

`[VERIFIED]` Pairwise distinction rules are the bulk of a working codebook, not
a garnish: the scheme that reached κ 0.71 shipped **75** of them alongside a
decision tree, in 111 pages of guidelines.

`[DESIGN]` The eighteen rules below cover the pairs judged to genuinely collide.
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
| `procedure` / `technique` | Are there steps? A procedure gives an order to follow; a technique names an approach. |
| `recommendation` / `obligation` | Is anyone accountable? Advice can be ignored without violation; an obligation cannot. |
| `driver` / `assumption` | Is it the reason it works, or a precondition for it working? A driver explains; an assumption is what must hold for the explanation to survive. |
| `driver` / `observation` | Does it generalize? A driver claims a standing relation; an observation reports one occasion. |
| `structure` / `formula` | Parts or arithmetic? Structure names components; a formula computes a value. |
| `structure` / `dependency` | Inside or outside? Structure is what the thing is made of; a dependency is something separate it needs. |
| `assumption` / `dependency` | Must be TRUE, or must be PRESENT? An assumption is a belief the model rests on; a dependency is an input it consumes. |
| `formula` / `definition` | Does it compute? A formula produces a number; a definition fixes a meaning. |
| `definition` / `background` | Fixing a term or setting the scene? A definition pins meaning; background situates the reader. |
| `definition` / `distinction` | One term or two? A definition fixes one; a distinction separates two. |
| `obligation` / `procedure` | `[MEASURED]` The largest cross-coarse leak in the collision test (6 confusions). A procedure tells you the steps; an obligation tells you that doing it is required. A numbered list with a *must* in it is an obligation. |

---

## 4. Mechanism

### 4.1 Independent boolean tests, resolved in code

The model answers **one independent yes/no question per fine label**, in a
single call. It is never asked to pick one of eighteen.

`[VERIFIED]` Multiclass framing measured **90% lower odds** of correct
detection than binary presence/absence framing (OR 0.10, 95% CI 0.03–0.35,
p<.001, mixed-effects model over 1.1M+ annotations, arXiv 2601.12099).

`[DESIGN]` The specific tactic of decomposing *this* label set into eighteen
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

| Claim | Number |
|---|---|
| The fourteen definitions separate | fine α 0.778, coarse α 0.866, 4 blind raters, 72 statements |
| Coarse tier beats fine on the same annotations | +0.088, mapping fixed in advance |
| `mechanism` is reliable despite its 0.43 anchor | α 0.933, third of eighteen |
| `finding`/`conclusion` were the worst-colliding pair | 11 co-occurrences; merged |
| `finding` absorbs | 24% of all assignments |
| `obligation`/`procedure` leak across coarse types | 6 confusions |

Caveats on all of the above: four raters from one model family, no human gold
set, 72 items, no confidence intervals, and an item set that never exercised
four of the labels. It measures reproducibility, not correctness.

### Design decisions with no supporting measurement

- The seven coarse types and their names.
- The eighteen fine labels, their names, and which coarse type each maps to.
- The priority order used to resolve multiple firing tests.
- Decomposing this label set into eighteen binary probes specifically.
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
- The eighteen pairwise separations in §3.3 cover the pairs judged to collide.
  That judgment is unmeasured. The scheme that reached κ 0.71 shipped 75 rules.
- The reliability numbers in §2.2 are one-vs-rest binary collapses, mechanically
  higher than the full multi-way agreement of the same scheme (κ 0.50–0.57).
  They rank categories against each other reliably; they are not absolute
  targets.
