#!/bin/bash
# verify-logos.sh — pixel-level logo verification for a cached brand kit.
#
# WHY: a white (onDark) logo is invisible on a white preview and the manifest
# metadata can lie (it may say wordmark "Octave" while the actual file is a
# stray customer logo, e.g. WorkSpan scraped from a "trusted by" wall). The only
# thing that catches this is rendering BOTH variants on their intended
# backgrounds and eyeballing them. This script forces that.
#
# Usage: bash verify-logos.sh <slug>            (looks in ~/.octave/brands/<slug>)
#        bash verify-logos.sh <path-to-kit-dir>
#
# It: resolves onLight/onDark from manifest.render.logo, checks the files exist,
# compares aspect ratios (a big mismatch means one is a different logo), then
# builds a swatch showing onLight on white and onDark on dark with the expected
# wordmark, and opens it so you confirm each actually reads the company name.

set -euo pipefail
ARG="${1:-}"
if [ -z "$ARG" ]; then echo "Usage: bash verify-logos.sh <slug|kit-dir>"; exit 1; fi

if [ -d "$ARG" ]; then KIT="$ARG"; else KIT="$HOME/.octave/brands/$ARG"; fi
MAN="$KIT/manifest.json"
if [ ! -f "$MAN" ]; then echo "FAIL: no manifest at $MAN"; exit 1; fi

# Pull logo fields (top-level logo{} or render.logo{})
read -r COMPANY ONLIGHT ONDARK WORDMARK < <(python3 - "$MAN" <<'PY'
import json,sys
d=json.load(open(sys.argv[1]))
lg=d.get("logo") or d.get("render",{}).get("logo",{}) or {}
lk=lg.get("lockup",{}) or {}
def g(x): return (x or "-")
print(g(d.get("company")), g(lg.get("onLight")), g(lg.get("onDark")), g(lk.get("wordmark")))
PY
)

echo "LOGO VERIFICATION — $COMPANY"
echo "================================"
echo "Kit:      $KIT"
echo "onLight:  $ONLIGHT"
echo "onDark:   $ONDARK"
echo "wordmark (claimed): $WORDMARK"
echo ""

FAIL=0
check_file () { # name file
  if [ "$2" = "-" ]; then echo "WARN: no $1 logo declared in manifest"; return; fi
  if [ ! -f "$KIT/$2" ]; then echo "FAIL: $1 file missing: $2"; FAIL=1; return; fi
  local dims; dims=$(sips -g pixelWidth -g pixelHeight "$KIT/$2" 2>/dev/null | awk '/pixel/{print $2}' | paste -sd'x' -)
  echo "  $1: $2  ($dims)"
}
echo "Files:"
check_file onLight "$ONLIGHT"
check_file onDark "$ONDARK"
echo ""

# Aspect-ratio consistency: onLight and onDark should be the same logo, different color.
if [ "$ONLIGHT" != "-" ] && [ "$ONDARK" != "-" ] && [ -f "$KIT/$ONLIGHT" ] && [ -f "$KIT/$ONDARK" ]; then
  RATIOS=$(python3 - "$KIT/$ONLIGHT" "$KIT/$ONDARK" <<'PY'
import subprocess,sys
def ar(p):
    out=subprocess.run(["sips","-g","pixelWidth","-g","pixelHeight",p],capture_output=True,text=True).stdout
    w=h=0
    for line in out.splitlines():
        if "pixelWidth" in line: w=float(line.split()[-1])
        if "pixelHeight" in line: h=float(line.split()[-1])
    return (w/h) if h else 0
a,b=ar(sys.argv[1]),ar(sys.argv[2])
diff=abs(a-b)/max(a,b) if max(a,b) else 1
print(f"{a:.2f} {b:.2f} {diff*100:.0f}")
PY
)
  set -- $RATIOS
  echo "Aspect ratios: onLight=$1  onDark=$2  (diff ${3}%)"
  if [ "$3" -gt 15 ]; then
    echo "FAIL: aspect ratios differ by ${3}% (>15%). onLight and onDark are likely DIFFERENT logos, one is probably a stray/customer asset. Inspect before shipping."
    FAIL=1
  fi
  echo ""
fi

# Build the two-surface swatch and open it for eyeball confirmation.
SWATCH="$KIT/.logo-verify.html"
cat > "$SWATCH" <<HTML
<!doctype html><meta charset="utf-8"><title>Logo check — $COMPANY</title>
<style>
 body{margin:0;font:14px -apple-system,sans-serif;background:#f4f4f5;color:#111}
 h1{font-size:15px;padding:16px 20px;margin:0;border-bottom:1px solid #ddd}
 .row{display:flex;gap:0;min-height:200px}
 .cell{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:14px;padding:32px}
 .light{background:#ffffff}.dark{background:#0c0f2d;color:#fff}
 .cell img{max-width:70%;max-height:90px;object-fit:contain}
 .tag{font:11px ui-monospace,monospace;letter-spacing:.05em;text-transform:uppercase;opacity:.6}
 .ask{padding:14px 20px;background:#fffaeb;border-top:1px solid #f0c48a;font-size:13px}
 code{background:#eee;padding:1px 5px;border-radius:4px}
</style>
<h1>Logo check &middot; $COMPANY &mdash; each logo must read <code>$WORDMARK</code></h1>
<div class="row">
  <div class="cell light"><span class="tag">onLight / light surface</span><img src="$ONLIGHT" alt="onLight"></div>
  <div class="cell dark"><span class="tag">onDark / dark band</span><img src="$ONDARK" alt="onDark"></div>
</div>
<div class="ask">Confirm BOTH marks are <b>$COMPANY</b> (not a customer/partner logo, not a stale asset). The onDark one is the usual culprit: it is often scraped from a dark "trusted by" logo wall. If either shows the wrong company, do not ship, re-source from the footer/nav or recolor the verified onLight.</div>
HTML

echo "Swatch: $SWATCH"
if command -v open >/dev/null 2>&1; then open "$SWATCH"; fi
echo ""
echo "MANUAL GATE (both must be true before this kit ships a logo):"
echo "  [ ] onLight reads \"$WORDMARK\" and is $COMPANY (not a customer)"
echo "  [ ] onDark  reads \"$WORDMARK\" and is $COMPANY (not a customer)"
echo ""
[ "$FAIL" -eq 0 ] && echo "Mechanical checks passed. Eyeball the swatch to finish." || { echo "Mechanical checks FAILED (see above)."; exit 1; }
