# Statement Classifier — Specification v1.0

Assigns a knowledge type to a short statement. One statement in, one
classification record out. Works on statements extracted from documents and on
statements taken from conversation.

**Evidence convention.** Every claim marked `[VERIFIED]` survived three-vote
adversarial verification against a primary source; the study, the number, and
the sample are named inline. Claims marked `[DESIGN]` are engineering decisions
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

Seven coarse types. Eighteen fine labels, each mapping to exactly one coarse
type. The mapping is a lookup table, not a judgment.

### 2.1 Coarse types

| Coarse | The question it answers |
|---|---|
| `case` | What happened, on one occasion? |
| `rule` | What must, may, or must not happen? |
| `method` | How is something done? |
| `concept` | What does this term mean? |
| `model` | How do these things relate? |
| `claim` | What is asserted to be so? |
| `general` | — assigned by code when no test fires |

### 2.2 Fine labels, with measured reliability where it exists

Each fine label is anchored, where possible, on a category that has a published
inter-annotator agreement figure. `κ` below is the measured agreement for the
*anchor* category in the cited scheme — not for this label as written here.

| Fine label | Coarse | Anchor κ | Anchored on |
|---|---|---|---|
| `observation` | case | **0.79** | CoreSC `Observation` [VERIFIED] |
| `event` | case | — | [DESIGN] — concrete by construction (actor + time) |
| `decision` | case | — | [DESIGN] — concrete by construction (actor + time + choice) |
| `study` | case | **0.65** | CoreSC `Experiment` [VERIFIED] |
| `obligation` | rule | — | [DESIGN] — deontic modal is a surface cue |
| `prohibition` | rule | — | [DESIGN] — deontic modal is a surface cue |
| `permission` | rule | — | [DESIGN] — deontic modal is a surface cue |
| `procedure` | method | **0.74** | CoreSC `Method` [VERIFIED] |
| `technique` | method | **0.76** | AZ-II `OWNMTHD` [VERIFIED] |
| `recommendation` | method | — | [DESIGN] |
| `definition` | concept | **0.81** | CoreSC `Object` [VERIFIED] |
| `distinction` | concept | — | [DESIGN] |
| `background` | concept | **0.87** | CoreSC `Background` [VERIFIED] |
| `mechanism` | model | **0.43** | CoreSC `Model` [VERIFIED] — **weakest measured category** |
| `tradeoff` | model | — | [DESIGN] |
| `finding` | claim | **0.78** | CoreSC `Result` [VERIFIED] |
| `conclusion` | claim | **0.89** | CoreSC `Conclusion` [VERIFIED] — highest measured |
| `fact` | claim | — | [DESIGN] |

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

Each of the eighteen fine labels carries:

- **Cue** — the surface pattern, stated so a reader can check it without
  inferring intent.
- **Does not fire when** — at least two explicit exclusions.
- **Two exemplars** — one from a document-style statement, one conversational.
- **Pairwise rules** — an explicit "how to tell this from X" for every label it
  is confusable with.

`[DESIGN]` Pairwise rules are required for at least these pairs, which are the
predictable collisions in this label set: `observation`/`finding`,
`finding`/`conclusion`, `definition`/`background`, `mechanism`/`tradeoff`,
`procedure`/`technique`, `recommendation`/`obligation`, `event`/`decision`,
`fact`/`finding`.

### 3.2 Worked example — `mechanism`, the weakest category

> **Cue.** The statement links two or more named things with a causal or
> structural connective — *because, causes, leads to, is composed of, trades
> off against* — such that removing the connective would lose the point.
>
> **Does not fire when:** the statement names only one thing and says what it
> means (→ `definition`); the connective joins a condition to an instruction
> (→ `procedure`); the subject is merely *called* a model — a pricing model, a
> data model — since the word in the name is not the test; the statement asserts
> a single proposition with no relation between parts (→ `fact` or `finding`).
>
> **Exemplars.** "Larger batches raise throughput but lengthen tail latency,
> because queued requests wait for the slowest member." / "the reason onboarding
> drags is that every new hire re-derives the same context"
>
> **vs `tradeoff`:** `tradeoff` requires two named quantities moving in
> *opposite* directions. If only one direction is stated, it is `mechanism`.
>
> **Expected reliability:** lowest in the set. Its anchor category measured
> κ 0.43. Treat disagreement here as expected, not as a defect.

The remaining seventeen definitions follow this shape.

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

Most surface-recognizable first. Within a coarse type, the fine label whose test
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

`[DESIGN]` This spec assumes fine labels rolling up to coarse types is worth
doing. That assumption is **not** established. The direct experiment — one
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
- The reliability numbers in §2.2 are one-vs-rest binary collapses, mechanically
  higher than the full multi-way agreement of the same scheme (κ 0.50–0.57).
  They rank categories against each other reliably; they are not absolute
  targets.
