"""Boolean battery vs single-choice, same 160 items.

Each rater r is reconstructed by joining the five family agents at index r,
then resolving by the spec's priority order in code -- which is the shipping
design. Compared against arm TS (single choice out of fifteen).
"""

from __future__ import annotations

import itertools
import json
import sys
from pathlib import Path
from collections import Counter, defaultdict

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "2026-08-09-reliability-data"))
from analyze import krippendorff_alpha

# Table order within each coarse type, coarse types in priority order.
PRIORITY = [
    ("case", ["observation", "event"]),
    ("rule", ["obligation", "prohibition", "decision"]),
    ("method", ["procedure", "recommendation"]),
    ("concept", ["definition", "distinction"]),          # background handled last
    ("model", ["principle", "architecture", "formula", "assumption", "dependency"]),
]
COARSE = {lab: c for c, labs in PRIORITY for lab in labs}
COARSE["background"] = "concept"
COARSE["general"] = "general"
VALID = set(COARSE)

bat = json.load(open(Path(__file__).resolve().parent / "rater-responses-and-items.json"))
TS = json.load(open(Path(__file__).resolve().parent.parent / "2026-08-11-status-ladder-data" / "rater-responses-and-items.json"))
TEXT = {i["id"]: i["text"] for i in bat["items"]}
IDS = [i["id"] for i in bat["items"]]

# fired[rater][item] = set of labels whose test fired
fired = defaultdict(lambda: defaultdict(set))
for res in bat["results"]:
    for row in res["rows"]:
        for lab in row["fired"]:
            lab = lab[3:] if lab.startswith("is_") else lab   # agents echo the test name
            if lab in VALID:
                fired[res["rater"]][row["id"]].add(lab)


def resolve(labels: set[str]) -> str:
    """The spec's §4.1 resolution, applied in code."""
    for _, labs in PRIORITY:
        for lab in labs:
            if lab in labels:
                return lab
    if "background" in labels:          # background is last of all
        return "background"
    return "general"                    # no test fired


resolved = {i: [resolve(fired[r][i]) for r in range(4)] for i in IDS}
nfired = {i: [len(fired[r][i]) for r in range(4)] for i in IDS}

single = defaultdict(list)
for r in TS["raters"]:
    if r["arm"] != "TS":
        continue
    for x in r["labels"]:
        single[x["id"]].append(x["fine"])
single = dict(single)


def crs(f):
    return {i: [COARSE.get(v, "?") for v in vs] for i, vs in f.items()}


def unan(f):
    full = [vs for vs in f.values() if len(vs) == 4]
    return sum(1 for vs in full if len(set(vs)) == 1) / len(full)


print("=" * 70)
print("THE HEADLINE — same 160 items, same taxonomy")
print("=" * 70)
print("  single choice of 15 (arm TS)   fine %.3f   coarse %.3f   unanimity %.2f"
      % (krippendorff_alpha(single), krippendorff_alpha(crs(single)), unan(single)))
print("  boolean battery + priority     fine %.3f   coarse %.3f   unanimity %.2f"
      % (krippendorff_alpha(resolved), krippendorff_alpha(crs(resolved)), unan(resolved)))
print("  DELTA                          fine %+.3f  coarse %+.3f"
      % (krippendorff_alpha(resolved) - krippendorff_alpha(single),
         krippendorff_alpha(crs(resolved)) - krippendorff_alpha(crs(single))))

print("\n=== per-TEST agreement (did each boolean fire consistently?) ===")
rows = []
for lab in sorted(VALID - {"general"}):
    b = {i: [("Y" if lab in fired[r][i] else "N") for r in range(4)] for i in IDS}
    n = sum(1 for i in IDS for r in range(4) if lab in fired[r][i])
    rows.append((krippendorff_alpha(b), lab, n))
for a, lab, n in sorted(rows, reverse=True):
    print("  %-16s %.3f   fired %d/640" % (lab, a, n))

print("\n=== how many tests fire per statement? ===")
c = Counter(k for v in nfired.values() for k in v)
tot = sum(c.values())
for k in sorted(c):
    print("  %d test(s): %4d  (%2.0f%%)" % (k, c[k], 100 * c[k] / tot))
multi = sum(v for k, v in c.items() if k >= 2) / tot
print("  multi_fire rate: %.0f%%   no-fire (-> general): %.0f%%" % (100 * multi, 100 * c.get(0, 0) / tot))

print("\n=== which pairs co-fire? (dual-nature, NOT disagreement) ===")
co = Counter()
for i in IDS:
    for r in range(4):
        for a, b in itertools.combinations(sorted(fired[r][i]), 2):
            co[(a, b)] += 1
for (a, b), n in co.most_common(12):
    x = "cross-coarse" if COARSE[a] != COARSE[b] else ""
    print("  %-16s %-16s %3d   %s" % (a, b, n, x))

print("\n=== residual DISAGREEMENT after resolution ===")
dis = Counter()
for vs in resolved.values():
    for a, b in itertools.combinations(sorted(vs), 2):
        if a != b:
            dis[(a, b)] += 1
print("  total disagreeing rater-pairs: %d of %d" % (sum(dis.values()), 6 * len(IDS)))
for (a, b), n in dis.most_common(10):
    print("  %-16s %-16s %3d" % (a, b, n))

print("\n=== single-choice disagreement, for comparison ===")
dis2 = Counter()
for vs in single.values():
    for a, b in itertools.combinations(sorted(vs), 2):
        if a != b:
            dis2[(a, b)] += 1
print("  total disagreeing rater-pairs: %d of %d" % (sum(dis2.values()), 6 * len(IDS)))
for (a, b), n in dis2.most_common(6):
    print("  %-16s %-16s %3d" % (a, b, n))
