# The definition pass — raw data

See `../2026-08-11-definition-pass.md` for the analysis.

| file | what it is | fine α |
|---|---|---|
| `e8-raw.json` | the codebook BEFORE the pass, 160 statements, 8 raters | 0.844 |
| `v4-raw.json` | after the first definition pass, 160 statements, 8 raters, two arms | **0.934** |
| `batchsize-raw.json` | 40 statements, batches of 10 vs all 40 | 0.954 / 0.949 |
| `v5-raw.json` | plus nine further rulings, batches of 10 and 5 | 0.947 / 0.932 |
| `papers-raw.json` | 85 statements from three published documents | **0.894** |

`v4-raw.json` carries two arms: `P` (pick one label) and `C` (score all fifteen
0–100). The `C` arm is the evidence that self-reported confidence cannot drive
`general` — at threshold 90, 86% of assignments fall through and α collapses to
0.605.

`papers-raw.json` covers Sharpe's *The Arithmetic of Active Management* (1991),
De Bondt & Thaler's *Does the Stock Market Overreact?* (1985) and a Goldman
Sachs market note. Statements were extracted for classification, not reproduced;
the source documents are not redistributed here.

Every run rotates item order per rater against position bias, and no answer key
exists for any of them — the metric throughout is inter-rater Krippendorff α,
never agreement with a key.
