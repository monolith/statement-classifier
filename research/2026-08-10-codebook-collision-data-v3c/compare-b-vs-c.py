"""Arm B vs arm C. Same 152 items, same rotation, one paragraph different."""

from __future__ import annotations

import itertools
import json
import sys
from pathlib import Path
from collections import Counter, defaultdict

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "2026-08-09-reliability-data"))
from analyze import krippendorff_alpha

COARSE = {
    "observation": "case", "event": "case",
    "obligation": "rule", "prohibition": "rule", "decision": "rule",
    "procedure": "method", "recommendation": "method",
    "definition": "concept", "distinction": "concept", "background": "concept",
    "principle": "model", "architecture": "model", "formula": "model",
    "assumption": "model", "dependency": "model", "general": "general",
}

B = json.load(open(Path(__file__).resolve().parent.parent / "2026-08-10-codebook-collision-data-v3" / "rater-responses-and-items.json"))
C = json.load(open(Path(__file__).resolve().parent / "rater-responses-and-items.json"))
TEXT = {i["id"]: i["text"] for i in C["items"]}


def mat(raw, arm, subset=None):
    f = defaultdict(list)
    for r in raw["raters"]:
        if r["arm"] != arm:
            continue
        for row in r["labels"]:
            if subset and not row["id"].startswith(subset):
                continue
            f[row["id"]].append(row["fine"])
    return dict(f)


def crs(f):
    return {i: [COARSE.get(v, "?" + v) for v in vs] for i, vs in f.items()}


def unan(r):
    full = [vs for vs in r.values() if len(vs) == 4]
    return sum(1 for vs in full if len(set(vs)) == 1) / len(full)


def pl(f):
    out = {}
    for lab in sorted({v for vs in f.values() for v in vs}):
        b = {i: [("Y" if v == lab else "N") for v in vs] for i, vs in f.items()}
        out[lab] = (krippendorff_alpha(b), sum(1 for vs in f.values() for v in vs if v == lab))
    return out


def conf(f, pair):
    return sum(1 for vs in f.values()
               for x, y in itertools.combinations(sorted(vs), 2) if {x, y} == set(pair))


ARMS = [("B", B, "B"), ("C", C, "C")]
print("%-28s %8s %8s %8s %8s" % ("", "fine", "coarse", "unan-f", "unan-c"))
res = {}
for name, raw, arm in ARMS:
    for sub, lbl in ((None, "all 152"), ("S", "S subset (72)"), ("T", "T subset (80)")):
        f = mat(raw, arm, sub)
        c = crs(f)
        res[(name, sub)] = (krippendorff_alpha(f), krippendorff_alpha(c), f)
        print("arm %s  %-20s %8.3f %8.3f %8.2f %8.2f"
              % (name, lbl, res[(name, sub)][0], res[(name, sub)][1], unan(f), unan(c)))

print("\n=== C - B ===")
for sub, lbl in ((None, "all 152"), ("S", "S subset"), ("T", "T subset")):
    b, c = res[("B", sub)], res[("C", sub)]
    print("  %-14s fine %+.3f   coarse %+.3f" % (lbl, c[0] - b[0], c[1] - b[1]))

print("\n=== the boundary under test ===")
for pair in (("principle", "observation"), ("principle", "recommendation"),
             ("principle", "architecture"), ("decision", "procedure")):
    row = "  %-28s" % ("/".join(pair))
    for name in ("B", "C"):
        row += "  %s=%2d" % (name, conf(res[(name, None)][2], pair))
    print(row)

print("\n=== per-label, all 152 ===")
plb, plc = pl(res[("B", None)][2]), pl(res[("C", None)][2])
print("  %-16s %8s %8s %8s   n(B)  n(C)" % ("label", "B", "C", "delta"))
for lab in sorted(set(plb) | set(plc)):
    ab, nb = plb.get(lab, (None, 0))
    ac, nc = plc.get(lab, (None, 0))
    d = "" if ab is None or ac is None else "%+.3f" % (ac - ab)
    print("  %-16s %8s %8s %8s   %4d  %4d"
          % (lab, "%.3f" % ab if ab is not None else "-",
             "%.3f" % ac if ac is not None else "-", d, nb, nc))

print("\n=== the six items the generality test was written for ===")
for i in ("S201", "S210", "S411", "S504", "T506", "T605"):
    fb = res[("B", None)][2][i]
    fc = res[("C", None)][2][i]
    flag = "  <-- resolved" if len(set(fc)) == 1 and len(set(fb)) > 1 else ""
    print("  %s  B=%-42s C=%s%s" % (i, "/".join(sorted(set(fb))), "/".join(sorted(set(fc))), flag))
    print("       %s" % TEXT[i][:120])
