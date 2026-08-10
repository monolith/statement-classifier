"""v3 two-arm analysis.

Arm A : v3 codebook, dangling pointers repaired, NO strip test
Arm B : identical, PLUS the observation/principle strip test

Both arms rate the same 152 items (v1's 72 `S###` + v2's 80 `T###`), so
B - A isolates the strip test and the S-subset is directly comparable to the
control run.
"""

from __future__ import annotations

import itertools
import json
import sys
from pathlib import Path
from collections import Counter, defaultdict

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "2026-08-09-reliability-data"))
from analyze import krippendorff_alpha

COARSE_V3 = {
    "observation": "case", "event": "case",
    "obligation": "rule", "prohibition": "rule", "decision": "rule",
    "procedure": "method", "recommendation": "method",
    "definition": "concept", "distinction": "concept", "background": "concept",
    "principle": "model", "architecture": "model", "formula": "model",
    "assumption": "model", "dependency": "model",
    "general": "general",
}

raw = json.load(open(Path(__file__).resolve().parent / "rater-responses-and-items.json"))
TEXT = {i["id"]: i["text"] for i in raw["items"]}


def matrix(arm, subset=None):
    fine = defaultdict(list)
    for r in raw["raters"]:
        if r["arm"] != arm:
            continue
        for row in r["labels"]:
            if subset and not row["id"].startswith(subset):
                continue
            fine[row["id"]].append(row["fine"])
    return dict(fine)


def coarse(fine):
    return {i: [COARSE_V3.get(v, "?" + v) for v in vs] for i, vs in fine.items()}


def unan(r):
    full = [vs for vs in r.values() if len(vs) == 4]
    return sum(1 for vs in full if len(set(vs)) == 1) / len(full)


def per_label(fine):
    out = {}
    for lab in sorted({v for vs in fine.values() for v in vs}):
        binary = {i: [("Y" if v == lab else "N") for v in vs] for i, vs in fine.items()}
        n = sum(1 for vs in fine.values() for v in vs if v == lab)
        out[lab] = (krippendorff_alpha(binary), n)
    return out


def confusions(fine, top=10):
    pairs = Counter()
    for vs in fine.values():
        for a, b in itertools.combinations(sorted(vs), 2):
            if a != b:
                pairs[(a, b)] += 1
    return pairs.most_common(top)


def block(name, arm, subset=None):
    f = matrix(arm, subset)
    c = coarse(f)
    fa, ca = krippendorff_alpha(f), krippendorff_alpha(c)
    off = sum(1 for vs in f.values() for v in vs if v not in COARSE_V3)
    tot = sum(len(vs) for vs in f.values())
    gen = sum(1 for vs in f.values() for v in vs if v == "general")
    print(f"\n--- {name}  ({len(f)} items) ---")
    print("  fine %.3f   coarse %.3f   unanimity %.2f/%.2f   general %d/%d   off-taxonomy %d"
          % (fa, ca, unan(f), unan(c), gen, tot, off))
    return fa, ca, f


print("=" * 66)
print("ARM A (no strip test)  vs  ARM B (strip test)")
print("=" * 66)
res = {}
for arm in ("A", "B"):
    res[(arm, "all")] = block(f"arm {arm} — all 152", arm)
    res[(arm, "S")] = block(f"arm {arm} — v1 subset (72 S###)", arm, "S")
    res[(arm, "T")] = block(f"arm {arm} — v2 subset (80 T###)", arm, "T")

print("\n=== strip test effect (B - A) ===")
for sub, lbl in (("all", "all 152"), ("S", "v1 subset"), ("T", "v2 subset")):
    a, b = res[("A", sub)], res[("B", sub)]
    print("  %-12s fine %+.3f   coarse %+.3f" % (lbl, b[0] - a[0], b[1] - a[1]))

print("\n=== the boundary under test: principle / observation ===")
for arm in ("A", "B"):
    for sub in ("all", "S", "T"):
        f = res[(arm, sub)][2]
        n = sum(1 for vs in f.values()
                for x, y in itertools.combinations(sorted(vs), 2)
                if {x, y} == {"principle", "observation"})
        items = sum(1 for vs in f.values() if {"principle", "observation"} <= set(vs))
        print("  arm %s %-4s  %2d disagreeing rater-pairs across %2d items" % (arm, sub, n, items))

print("\n=== per-label, arm B, all 152 ===")
for lab, (a, n) in sorted(per_label(res[("B", "all")][2]).items(), key=lambda kv: -(kv[1][0] or 0)):
    print("  %-16s %.3f   n=%d" % (lab, a, n))

print("\n=== top confusions ===")
for arm in ("A", "B"):
    print("  arm", arm)
    for (x, y), c in confusions(res[(arm, "all")][2]):
        print("    %-16s %-16s %d" % (x, y, c))
