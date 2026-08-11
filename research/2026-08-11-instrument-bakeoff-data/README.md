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

| `bestof-raw.json` | arm E codebook inside the 3-family cascade | 0.872 |
| `surface-raw.json` | all fifteen cues surface-anchored | 0.857 |
| `hybrid-raw.json` | arm E + anchors on four labels only | 0.853 |
| `e8-raw.json` | **arm E again with 8 raters** | **0.844** |

`e8-raw.json` is the most important file here. It is a straight replication of
the arm E condition in `bakeoff2-raw.json` — same codebook, same items, same
first four rotation offsets — and it scores 0.844 where the original scored
0.898. All 70 four-rater subsets of it fall between 0.824 and 0.864. Read
`../2026-08-11-FINDINGS.md` before trusting any single-run comparison in this
directory.

The boolean-battery run lives in `../2026-08-11-boolean-battery-data/`.

The `.js` files are the workflow scripts that produced each run, kept verbatim.
Every run rotates item order per rater (offset 37, prime against 160) to control
position bias, and no answer key exists for any of them — the metric throughout
is inter-rater Krippendorff α, not agreement with a key.
