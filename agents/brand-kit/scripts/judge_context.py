#!/usr/bin/env python3
"""judge_context.py — build a judge-context file from the capture reports, so no one retypes it by hand.

  judge_context.py --design <analyst report.md> --logo <verifier report.md> --gate <gate.json> \
                   --top <home top frame.png> --strips <home-strip*.png ...> [--bottom <home-bottom.png>] \
                   --artifact gallery|one-pager --out <judge-context.md> \
                   [--hero-visual none|chips|masonry|image] [--domain acme.com] [--round 1] [--version 2]

One context per artifact and candidate: the gallery and the one-pager have their own gate.json, and a
re-rendered best version is not the repaired one. The judges must not read the evidence pack, so this file
carries the few facts they need: the devices the brand uses and lacks (the analyst's Emphasis and Devices
sections, verbatim), the hero decision, that artifact's pre-gate measurements, which source strip each block
maps to (the dedicated bottom strip for CTA and footer when the miner cut one), and the rules against
inventing devices and docking for imagery tokens cannot express. Strips with almost no pixel variance are
marked near-blank.
"""
import argparse
import json
import pathlib
import re

SECTION_RE = re.compile(r"^(\d+)\.\s", re.M)


def sections(report_text):
    """{number: text} for a numbered findings report ("1. Fonts ...", "2. Palette ...")."""
    out = {}
    starts = [(m.start(), int(m.group(1))) for m in SECTION_RE.finditer(report_text)]
    for i, (pos, num) in enumerate(starts):
        end = starts[i + 1][0] if i + 1 < len(starts) else len(report_text)
        out.setdefault(num, report_text[pos:end].strip())
    return out


def first_line(text):
    return text.strip().splitlines()[0] if text.strip() else ""


def near_blank(path):
    """True when a strip is almost one flat color (a lazy section that never mounted)."""
    try:
        from PIL import Image, ImageStat
        im = Image.open(path).convert("L")
        im.thumbnail((320, 320))
        return max(ImageStat.Stat(im).stddev) < 6
    except Exception:
        return False


def build(design, logo, gate, top, strips, hero_visual=None, domain="", rnd=None, bottom=None, artifact="gallery", version=None):
    d = sections(design)
    l_lines = [ln for ln in logo.splitlines() if ln.lower().lstrip().startswith("hero imagery")]
    m = re.search(r"heroVisual\s+(\w+)", " ".join(l_lines))
    hero = hero_visual or (m.group(1) if m else "unknown")
    head = f"# Judge context: {domain}, {artifact}" + (f", kit v{version}" if version else "") + (f", round {rnd}" if rnd else "")
    lines = [head, ""]
    lines += ["## Devices the brand uses and lacks (from the design analyst, verbatim)", ""]
    lines += [d.get(3, "3. Emphasis mechanism: not reported"), "", d.get(7, "7. Devices: not reported"), ""]
    pal = first_line(d.get(2, ""))
    if pal:
        lines += ["Palette note: " + pal, ""]
    lines += ["## heroVisual", "", f"`{hero}`. " + (" ".join(l_lines) if l_lines else "No hero imagery line in the logo report."),
              "When it is `none` or `chips`, product shots, diagrams and animations cannot come from tokens: do not dock depth for them.", ""]
    lines += [f"## Pre-gate measurements ({artifact})", ""]
    if gate and gate.get("notRun"):
        lines.append(f"NOT RUN: {gate['notRun']}")
    elif gate:
        lines.append(f"pass: {gate.get('pass')}")
        for c in gate.get("checks", []):
            lines.append(f"- {c['name']}: {c['value']} (want {c['want']})" + (f"; {c['note']}" if c.get("note") else ""))
    else:
        lines.append("NOT RUN (no gate.json)")
    lines.append("")
    lines += ["## Block-to-source map", ""]
    lines.append(f"- Hero and nav -> {top} (top frame)")
    if strips:
        mids = strips[1:-1] if len(strips) > 2 else strips[1:]
        if mids:
            lines.append(f"- Stats, cards, comparison, quote -> {', '.join(mids)}")
    if bottom:
        lines.append(f"- CTA and footer -> {bottom} (the page's last 1600px)")
    elif strips:
        last = strips[-1]
        prev = strips[-2] if len(strips) > 1 else None
        if near_blank(last) and prev:
            lines.append(f"- CTA and footer -> {prev} ({last} is near-blank: the page's last section had not mounted, compare against the strip before it)")
        else:
            lines.append(f"- CTA and footer -> {last}")
    lines.append("")
    lines += ["## Rules", "",
              "- Do not invent a device the brand lacks: the sections above are the evidence; a treatment not listed as `yes` is not a fix to ask for.",
              "- Do not dock depth for product imagery when heroVisual is `none` or `chips`.",
              "- Use the measurements above for contrast and spacing instead of guessing from pixels; they are for this artifact.",
              "- Ignore cookie dialogs, chat widgets and promo toasts in the source. Judge the visual system, not the placeholder copy.", ""]
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--design", type=pathlib.Path, required=True)
    ap.add_argument("--logo", type=pathlib.Path, required=True)
    ap.add_argument("--gate", type=pathlib.Path)
    ap.add_argument("--top", required=True)
    ap.add_argument("--strips", nargs="*", default=[])
    ap.add_argument("--bottom")
    ap.add_argument("--artifact", choices=["gallery", "one-pager"], default="gallery")
    ap.add_argument("--hero-visual")
    ap.add_argument("--domain", default="")
    ap.add_argument("--round", type=int)
    ap.add_argument("--version", type=int)
    ap.add_argument("--out", type=pathlib.Path, required=True)
    a = ap.parse_args()
    gate = json.loads(a.gate.read_text()) if a.gate and a.gate.is_file() else None
    text = build(a.design.read_text(), a.logo.read_text(), gate, a.top, a.strips, a.hero_visual, a.domain, a.round, a.bottom, a.artifact, a.version)
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(text)
    print(f"{a.out} ({len(text.splitlines())} lines)")


if __name__ == "__main__":
    main()
