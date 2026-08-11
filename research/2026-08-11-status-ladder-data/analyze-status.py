"""Arm T (type only) vs arm TS (type + status), same 160 items.

Two questions:
  1. Does `floated` separate from `proposed`?
  2. Does asking for status degrade TYPE agreement? (arm T is the baseline)
"""

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
RUNGS = ["floated", "proposed", "evidenced", "settled", "n/a"]

raw = json.load(open(Path(__file__).resolve().parent / "rater-responses-and-items.json"))
TEXT = {i["id"]: i["text"] for i in raw["items"]}
SRC = {i["id"]: i["id"].rsplit("-", 1)[0] for i in raw["items"]}


def mat(arm, field="fine", src=None):
    f = defaultdict(list)
    for r in raw["raters"]:
        if r["arm"] != arm:
            continue
        for row in r["labels"]:
            if src and SRC[row["id"]] != src:
                continue
            f[row["id"]].append(row.get(field, "?"))
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


def conf(f, top=10):
    p = Counter()
    for vs in f.values():
        for a, b in itertools.combinations(sorted(vs), 2):
            if a != b:
                p[(a, b)] += 1
    return p.most_common(top)


print("=" * 72)
print("Q2 — does asking for status cost type agreement?")
print("=" * 72)
tT, tTS = mat("T"), mat("TS")
print("  arm T  (type only)      fine %.3f   coarse %.3f   unanimity %.2f"
      % (krippendorff_alpha(tT), krippendorff_alpha(crs(tT)), unan(tT)))
print("  arm TS (type + status)  fine %.3f   coarse %.3f   unanimity %.2f"
      % (krippendorff_alpha(tTS), krippendorff_alpha(crs(tTS)), unan(tTS)))
print("  DELTA                   fine %+.3f  coarse %+.3f"
      % (krippendorff_alpha(tTS) - krippendorff_alpha(tT),
         krippendorff_alpha(crs(tTS)) - krippendorff_alpha(crs(tT))))

print("\n" + "=" * 72)
print("Q1 — does the status ladder separate?")
print("=" * 72)
st = mat("TS", "status")
print("  status alpha (5 rungs incl n/a)  %.3f   unanimity %.2f" % (krippendorff_alpha(st), unan(st)))
merged = {i: [("floated/proposed" if v in ("floated", "proposed") else v) for v in vs]
          for i, vs in st.items()}
print("  with floated+proposed MERGED     %.3f   unanimity %.2f" % (krippendorff_alpha(merged), unan(merged)))
print("\n  per-rung:")
for lab, (a, n) in sorted(pl(st).items(), key=lambda kv: -(kv[1][0] or 0)):
    print("    %-12s %.3f   n=%d" % (lab, a, n))
print("\n  rung confusions:")
for (a, b), c in conf(st):
    print("    %-12s %-12s %d" % (a, b, c))

print("\n" + "=" * 72)
print("coverage — did the new sources reach the unexercised labels?")
print("=" * 72)
prev = {"event": 2, "background": 0, "distinction": 7}
cnt = Counter(v for vs in tT.values() for v in vs)
for lab in sorted(COARSE):
    if lab == "general" and not cnt.get(lab):
        continue
    note = "   (was %d across all 152 earlier items)" % prev[lab] if lab in prev else ""
    print("  %-15s %3d%s" % (lab, cnt.get(lab, 0), note))

print("\n=== type alpha per source (arm T) ===")
for s in sorted(set(SRC.values())):
    f = mat("T", "fine", s)
    print("  %-20s fine %.3f   n=%d" % (s, krippendorff_alpha(f), len(f)))

print("\n=== status alpha per source (arm TS) ===")
for s in sorted(set(SRC.values())):
    f = mat("TS", "status", s)
    print("  %-20s %.3f   mix=%s" % (s, krippendorff_alpha(f),
          dict(Counter(v for vs in f.values() for v in vs).most_common(3))))

print("\n=== does status apply to every type? (n/a rate by type, arm TS) ===")
by_type = defaultdict(Counter)
for r in raw["raters"]:
    if r["arm"] != "TS":
        continue
    for row in r["labels"]:
        by_type[row["fine"]][row["status"]] += 1
for t, c in sorted(by_type.items(), key=lambda kv: -sum(kv[1].values())):
    tot = sum(c.values())
    print("  %-15s n=%-4d n/a %2d%%   %s"
          % (t, tot, round(100 * c.get("n/a", 0) / tot),
             ", ".join("%s %d" % kv for kv in c.most_common(3))))

print("\n=== top type confusions, arm T ===")
for (a, b), c in conf(tT, 8):
    print("  %-16s %-16s %d" % (a, b, c))
