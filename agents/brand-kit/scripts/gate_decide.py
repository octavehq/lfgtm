#!/usr/bin/env python3
"""gate_decide.py — the fidelity gate's decision, computed from the round's files instead of in prose.

  gate_decide.py --round <r> --scorecards <judge-*.md ...> --gates <gate.json> <gate-onepager.json> [--json <out>]

Reads the judges' scorecards (total, the eight dimension rows, hard_fail, looks_good, fixes) and the two
pre-gate reports, applies the thresholds, and prints one JSON decision. Exit codes: 0 pass, 1 repair,
2 stop (round 3 failed, or inputs incomplete), 3 tiebreak (one gallery judge in the borderline band: add a
second gallery judge and run again). The thresholds live here and nowhere else.
"""
import argparse
import json
import pathlib
import re
import sys

PASS_TOTAL = 34
DIM_FLOOR = 3
BORDERLINE = (33, 35)
MAX_ROUNDS = 3
DIMS = ("Typography", "Color/palette", "Emphasis", "Contrast/legibility", "Spacing and rhythm", "Depth", "Edges/containers", "Logo/assets")


def parse_scorecard(text):
    """One judge scorecard -> dict, or None when the file is not a scorecard."""
    head = re.search(r"BRAND KIT SCORECARD\s*[—-]+\s*(.*?)\s*[—-]+\s*(gallery|one-pager)", text, re.I)
    total = re.search(r"^total:\s*([\d.]+)\s*/\s*40", text, re.M | re.I)
    if not head or not total:
        return None
    dims = {}
    for m in re.finditer(r"^\|\s*(\d)\s*\|\s*([^|]+?)\s*\|\s*([\d.]+)\s*\|", text, re.M):
        dims[DIMS[int(m.group(1)) - 1] if 1 <= int(m.group(1)) <= 8 else m.group(2)] = float(m.group(3))
    hard = re.search(r"^hard_fail:\s*(yes|no)", text, re.M | re.I)
    looks = re.search(r"^looks_good:\s*(yes|no)", text, re.M | re.I)
    fixes_block = re.search(r"^fixes:\s*(.*?)(?:\n\s*\n|\Z)", text, re.M | re.I | re.S)
    fixes = [ln.strip(" -*") for ln in (fixes_block.group(1).splitlines() if fixes_block else []) if ln.strip()]
    return {"artifact": head.group(2).lower(), "total": float(total.group(1)), "dimensions": dims,
            "hardFail": bool(hard and hard.group(1).lower() == "yes"),
            "looksGood": None if not looks else looks.group(1).lower() == "yes",
            "fixes": fixes, "rendererFixes": [f for f in fixes if re.search(r"\brenderer\b", f, re.I)]}


def read_gate(path):
    try:
        g = json.loads(pathlib.Path(path).read_text())
    except (OSError, ValueError) as e:
        return {"file": str(path), "pass": False, "notRun": f"unreadable: {e}"}
    return {"file": str(path), "pass": bool(g.get("pass")), "notRun": g.get("notRun")}


def decide(cards, gates, rnd):
    gallery = [c for c in cards if c["artifact"] == "gallery"]
    onepager = [c for c in cards if c["artifact"] == "one-pager"]
    out = {"round": rnd, "galleryJudges": len(gallery), "onepagerJudges": len(onepager), "preGate": gates}
    if not gallery:
        out.update({"next": "stop", "reason": "no gallery scorecard"}); return out
    mean = lambda xs: round(sum(xs) / len(xs), 2)
    out["gallery"] = mean([c["total"] for c in gallery])
    out["onepager"] = mean([c["total"] for c in onepager]) if onepager else None
    dims = {d: mean([c["dimensions"][d] for c in gallery if d in c["dimensions"]]) for d in DIMS if any(d in c["dimensions"] for c in gallery)}
    out["dimensions"] = dims
    out["failingDimensions"] = sorted(d for d, v in dims.items() if v < DIM_FLOOR)
    out["hardFail"] = any(c["hardFail"] for c in cards)
    out["looksGood"] = "no" if gallery and all(c["looksGood"] is False for c in gallery) else "yes"
    out["rendererFixes"] = sorted({f for c in cards for f in c["rendererFixes"]})
    out["fixes"] = [f for c in cards for f in c["fixes"]]
    out["borderline"] = len(gallery) == 1 and BORDERLINE[0] <= out["gallery"] <= BORDERLINE[1]
    gates_ok = bool(gates) and all(g["pass"] and not g.get("notRun") for g in gates)
    out["preGatePass"] = gates_ok
    out["pass"] = (out["gallery"] >= PASS_TOTAL and not out["failingDimensions"] and not out["hardFail"]
                   and out["looksGood"] == "yes" and gates_ok)
    if out["borderline"] and not out["hardFail"] and gates_ok and not out["failingDimensions"]:
        out["next"] = "tiebreak"  # one judge within a point of the bar, either side: a second opinion before any decision
    elif out["pass"]:
        out["next"] = "pass"
    elif rnd >= MAX_ROUNDS:
        out["next"] = "stop"
    else:
        out["next"] = "repair"
    blocks = []
    if out["gallery"] < PASS_TOTAL: blocks.append(f"gallery {out['gallery']} < {PASS_TOTAL}")
    if out["failingDimensions"]: blocks.append("dimensions below 3: " + ", ".join(out["failingDimensions"]))
    if out["hardFail"]: blocks.append("hard fail (logo)")
    if out["looksGood"] == "no": blocks.append("gallery judges say it does not look good")
    if not gates_ok: blocks.append("pre-gate not passed: " + "; ".join(g.get("notRun") or pathlib.Path(g["file"]).name for g in gates if not g["pass"] or g.get("notRun")) or "pre-gate files missing")
    out["blocking"] = blocks
    return out


def merge_feedback(path, fixes):
    """Append renderer fixes to the maintainers' feedback file, one line each, deduplicated case-insensitively
    across judges and rounds. Returns the lines added."""
    path = pathlib.Path(path)
    norm = lambda s: re.sub(r"\s+", " ", s.strip().lower())
    existing = path.read_text().splitlines() if path.is_file() else []
    seen = {norm(ln) for ln in existing if ln.strip()}
    added = []
    for f in fixes:
        key = norm(f)
        if key and key not in seen:
            seen.add(key); added.append(f.strip())
    if added:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a") as fh:
            fh.write("\n".join(added) + "\n")
    return added


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--round", type=int, required=True)
    ap.add_argument("--scorecards", nargs="+", required=True)
    ap.add_argument("--gates", nargs="*", default=[])
    ap.add_argument("--json", type=pathlib.Path)
    ap.add_argument("--feedback", type=pathlib.Path, help="renderer-feedback file for the plugin maintainers; the round's `renderer` fixes are merged in, deduplicated")
    a = ap.parse_args()
    cards = []
    for f in a.scorecards:
        try:
            c = parse_scorecard(pathlib.Path(f).read_text())
        except OSError:
            c = None
        if c: c["file"] = f; cards.append(c)
    out = decide(cards, [read_gate(g) for g in a.gates], a.round)
    if a.feedback and out.get("rendererFixes"):
        out["feedbackAdded"] = merge_feedback(a.feedback, out["rendererFixes"])
    text = json.dumps(out, indent=1)
    if a.json: a.json.write_text(text)
    print(text)
    sys.exit({"pass": 0, "repair": 1, "stop": 2, "tiebreak": 3}[out["next"]])


if __name__ == "__main__":
    main()
