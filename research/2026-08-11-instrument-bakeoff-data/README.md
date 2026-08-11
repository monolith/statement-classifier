# Instrument bake-off — raw data

Fourteen designs, same 160 statements, four blind raters each. See
`../2026-08-11-instrument-bakeoff.md` for the analysis.

| file | design | fine α |
|---|---|---|
| `bakeoff2-raw.json` | five flat codebook variants, arms A–E | 0.853 → 0.898 |
| `cascade3-raw.json` | 3 families → fine | 0.884 |
| `cascade-thin-raw.json` | 5 families, thin coarse book | 0.877 |
| `cascade-rich-raw.json` | 5 families, rich coarse book | 0.858 |
| `two-tier-raw.json` | 2 families → fine | 0.833 |
| `funnel3-raw.json` | 3×3×3, max 3 choices per node | 0.788 |
| `funnel2-raw.json` | 2×3×3 | 0.726 |

The boolean-battery run lives in `../2026-08-11-boolean-battery-data/`.

The `.js` files are the workflow scripts that produced each run, kept verbatim.
Every run rotates item order per rater (offset 37, prime against 160) to control
position bias, and no answer key exists for any of them — the metric throughout
is inter-rater Krippendorff α, not agreement with a key.
