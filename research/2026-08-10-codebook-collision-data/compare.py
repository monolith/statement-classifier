"""Compare three collision runs on the same footing.

  v1       : 72 items (S###)  x v1 codebook (18 fine labels)
  v2       : 80 items (T###)  x v2 codebook (16 fine labels)
  control  : 72 items (S###)  x v2 codebook (16 fine labels)

v1 vs v2 confounds two changes at once: the taxonomy AND the item set. The
control holds the item set at v1's and swaps only the codebook, so
control - v1 is the taxonomy effect alone.
"""

from __future__ import annotations

import itertools
import json
import sys
from pathlib import Path
from collections import Counter, defaultdict

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "2026-08-09-reliability-data"))
from analyze import krippendorff_alpha

HERE = Path(__file__).resolve().parent.parent
RUNS = {
    "v1": HERE / "2026-08-10-codebook-collision-data" / "rater-responses-and-items.json",
    "v2": HERE / "2026-08-10-codebook-collision-data-v2" / "rater-responses-and-items.json",
    "control": HERE / "2026-08-10-codebook-collision-data-control" / "rater-responses-and-items.json",
}

# Extracted from the codebook headings the raters actually saw, not from memory.
COARSE_V1 = {
    "observation": "case", "event": "case", "study": "case",
    "obligation": "rule", "prohibition": "rule", "permission": "rule", "decision": "rule",
    "procedure": "method", "technique": "method", "recommendation": "method",
    "definition": "concept", "distinction": "concept", "background": "concept",
    "mechanism": "model", "tradeoff": "model",
    "finding": "claim", "conclusion": "claim", "fact": "claim",
}
COARSE_V2 = {
    "observation": "case", "event": "case",
    "obligation": "rule", "prohibition": "rule", "decision": "rule",
    "procedure": "method", "technique": "method", "recommendation": "method",
    "definition": "concept", "distinction": "concept", "background": "concept",
    "driver": "model", "structure": "model", "formula": "model",
    "assumption": "model", "dependency": "model",
}


def load(path, coarse):
    raw = json.load(open(path))
    fine = defaultdict(list)
    for r in raw["raters"]:
        for row in r["labels"]:
            fine[row["id"]].append(row["fine"])
    ids = [i["id"] for i in raw["items"]]
    fine = {i: fine[i] for i in ids if fine.get(i)}
    crs = {i: [coarse.get(v, "?" + v) for v in vs] for i, vs in fine.items()}
    return raw, fine, crs


def unanimity(ratings):
    full = [vs for vs in ratings.values() if len(vs) == 4]
    return sum(1 for vs in full if len(set(vs)) == 1) / len(full)


def per_label(fine):
    """One-vs-rest collapse per label (the CoreSC method)."""
    labels = sorted({v for vs in fine.values() for v in vs})
    out = {}
    for lab in labels:
        binary = {i: [("Y" if v == lab else "N") for v in vs] for i, vs in fine.items()}
        n = sum(1 for vs in fine.values() for v in vs if v == lab)
        out[lab] = (krippendorff_alpha(binary), n)
    return out


def confusions(fine, top=8):
    pairs = Counter()
    for vs in fine.values():
        for a, b in itertools.combinations(sorted(vs), 2):
            if a != b:
                pairs[(a, b)] += 1
    return pairs.most_common(top)


def report(name, path, coarse):
    raw, fine, crs = load(path, coarse)
    fa, ca = krippendorff_alpha(fine), krippendorff_alpha(crs)
    nontax = sum(1 for vs in fine.values() for v in vs if v not in coarse)
    total = sum(len(vs) for vs in fine.values())
    print(f"\n=== {name}  ({len(fine)} items x {len(raw['raters'])} raters) ===")
    print("  fine alpha   %.3f" % fa)
    print("  coarse alpha %.3f" % ca)
    print("  unanimity    %.2f (fine)   %.2f (coarse)" % (unanimity(fine), unanimity(crs)))
    print("  off-taxonomy %d / %d" % (nontax, total))
    print("  per-label alpha (one-vs-rest), weakest last:")
    for lab, (a, n) in sorted(per_label(fine).items(), key=lambda kv: -(kv[1][0] or 0)):
        print("    %-16s %.3f   n=%d" % (lab, a if a is not None else float("nan"), n))
    print("  top confusions:")
    for (a, b), c in confusions(fine):
        print("    %-16s %-16s %d" % (a, b, c))
    print("  per-rater label spread:")
    for r in raw["raters"]:
        c = Counter(x["fine"] for x in r["labels"])
        print("    rater%s: %d distinct, top=%s" % (r["rater"], len(c), c.most_common(3)))
    return fa, ca


if __name__ == "__main__":
    v1 = report("v1: v1 items x v1 codebook (18 labels)", RUNS["v1"], COARSE_V1)
    v2 = report("v2: v2 items x v2 codebook (16 labels)", RUNS["v2"], COARSE_V2)
    ct = report("CONTROL: v1 items x v2 codebook (16 labels)", RUNS["control"], COARSE_V2)

    print("\n=== decomposition ===")
    print("  headline v1 -> v2      fine %+.3f  coarse %+.3f  (taxonomy + item set)"
          % (v2[0] - v1[0], v2[1] - v1[1]))
    print("  taxonomy alone         fine %+.3f  coarse %+.3f  (v1 items, both codebooks)"
          % (ct[0] - v1[0], ct[1] - v1[1]))
    print("  item set alone         fine %+.3f  coarse %+.3f  (v2 codebook, both item sets)"
          % (v2[0] - ct[0], v2[1] - ct[1]))
