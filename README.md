# Statement Classifier

Assigns a knowledge type to a short statement — one statement in, one
classification record out. Works on statements taken from documents and on
statements taken from conversation.

- **[docs/SPECIFICATION.md](docs/SPECIFICATION.md)** — the spec.
- **[research/](research/)** — the evidence it cites, shipped whole.

Seven coarse types (`case`, `rule`, `method`, `concept`, `model`, `claim`,
`general`) over eighteen fine labels. Fine labels are anchored, where such a
figure exists, on annotation categories with published inter-annotator
agreement; the anchor and its κ are named per label in §2.2.

Every claim in the spec is marked `[VERIFIED]` — three-vote adversarially
verified against a primary source, with the number and sample named — or
`[DESIGN]` — an engineering decision with no supporting measurement. §9 lists
every design decision, every contradicted assumption, and every known weakness
in the evidence base in one place.

Two of those are worth knowing before reading anything else:

- There is **no measured evidence that type labels improve retrieval.** No
  reviewed source isolates typing from linking, extraction, or reranking.
- The spec therefore carries a **pre-registered kill criterion** (§7.4): run the
  typed-vs-untyped ablation, and if no query class improves, the classifier is
  decoration.
