#!/bin/bash
# Shared mechanical lint for Octave skill HTML outputs — deterministic checks that
# don't need LLM judgment. Word/phrase lists mirror shared/editorial-rules.md.
# Usage: bash lint.sh <path-to-output.html>
# Returns non-zero exit code if any violations found.
# Portable across BSD (macOS) and GNU userlands: no grep -P.

FILE="$1"
if [ -z "$FILE" ] || [ ! -f "$FILE" ]; then
  echo "Usage: bash lint.sh <path-to-output.html>"
  exit 1
fi

# Extract reader-facing text: drop <script>/<style> blocks and all tags, but keep
# every newline so grep -n line numbers below match the original file.
TEXT="$(mktemp)"
trap 'rm -f "$TEXT"' EXIT
perl -0777 -pe '
  s{<(script|style)\b[^>]*>.*?</\1\s*>}{ join("", $& =~ /\n/g) }gesi;
  s{(<[^>]*>)}{ " " . join("", $1 =~ /\n/g) }ges;
' "$FILE" > "$TEXT"

VIOLATIONS=0

echo "MECHANICAL LINT"
echo "==============="
echo "File: $FILE"
echo ""

# --- Em-dashes (U+2014) and en-dashes (U+2013) in reader-facing text ---
EMDASH_COUNT=$(grep -o '—' "$TEXT" 2>/dev/null | wc -l | tr -d ' ')
[ -z "$EMDASH_COUNT" ] && EMDASH_COUNT=0
if [ "$EMDASH_COUNT" -gt 0 ]; then
  echo "FAIL: $EMDASH_COUNT em-dash(es) found (U+2014). Replace with commas, periods, or \"to\"."
  grep -n '—' "$TEXT" | head -10
  echo ""
  VIOLATIONS=$((VIOLATIONS + EMDASH_COUNT))
fi
ENDASH_COUNT=$(grep -o '–' "$TEXT" 2>/dev/null | wc -l | tr -d ' ')
[ -z "$ENDASH_COUNT" ] && ENDASH_COUNT=0
if [ "$ENDASH_COUNT" -gt 0 ]; then
  echo "FAIL: $ENDASH_COUNT en-dash(es) found (U+2013). Replace with commas, periods, or \"to\"."
  grep -n '–' "$TEXT" | head -10
  echo ""
  VIOLATIONS=$((VIOLATIONS + ENDASH_COUNT))
fi

# --- Tier 1 banned words (whole-word, case-insensitive) ---
BANNED_WORDS="delve landscape robust comprehensive leverage seamless seamlessly cutting-edge pivotal underscores meticulous meticulously utilize holistic holistically actionable impactful learnings synergy synergies game-changer game-changing tapestry realm paradigm embark beacon"
for WORD in $BANNED_WORDS; do
  COUNT=$(grep -o -i -w -- "$WORD" "$TEXT" 2>/dev/null | wc -l | tr -d ' ')
  if [ "$COUNT" -gt 0 ]; then
    echo "FAIL: Banned word '$WORD' found $COUNT time(s)."
    grep -i -n -w -- "$WORD" "$TEXT" | head -5
    echo ""
    VIOLATIONS=$((VIOLATIONS + COUNT))
  fi
done

# --- Banned phrases (case-insensitive; . matches any apostrophe variant) ---
BANNED_PHRASES=(
  "best practices"
  "deep dive"
  "dive into"
  "at its core"
  "in order to"
  "due to the fact that"
  "serves as"
  "testament to"
  "it.s worth noting"
  "when it comes to"
  "at the end of the day"
  "let.s explore"
  "let.s take a look"
  "let.s break this down"
  "here.s what.s interesting"
  "in today.s"
  "in an era"
)
for PHRASE in "${BANNED_PHRASES[@]}"; do
  COUNT=$(grep -o -i -- "$PHRASE" "$TEXT" 2>/dev/null | wc -l | tr -d ' ')
  if [ "$COUNT" -gt 0 ]; then
    echo "FAIL: Banned phrase '$PHRASE' found $COUNT time(s)."
    grep -i -n -- "$PHRASE" "$TEXT" | head -3
    echo ""
    VIOLATIONS=$((VIOLATIONS + COUNT))
  fi
done

# --- Text density: single <p> tags with 4+ sentences ---
DENSE_BLOCKS=$(grep -oE '<p[^>]*>[^<]{100,}</p>' "$FILE" 2>/dev/null | while read -r line; do
  SENTENCES=$(echo "$line" | grep -oE '\. [A-Z]' | wc -l | tr -d ' ')
  SENTENCES=$((SENTENCES + 1))
  if [ "$SENTENCES" -ge 4 ]; then
    echo "$line" | head -c 120
    echo "... ($SENTENCES sentences)"
  fi
done)
if [ -n "$DENSE_BLOCKS" ]; then
  DENSE_COUNT=$(echo "$DENSE_BLOCKS" | wc -l | tr -d ' ')
  echo "WARN: $DENSE_COUNT text block(s) with 4+ sentences in a single <p>. Consider splitting."
  echo "$DENSE_BLOCKS" | head -5
  echo ""
fi

# --- Library/Octave internals leaked into reader-facing text ---
# Phrase-shaped terms: safe to match anywhere.
INTERNAL_TERMS="the library|source of truth|entity type|objection entities|use case entities|no .* entities|library says|library doesn.t|Octave internals|findings show|field data indicates|the data shows|receipt set|call extractions|extraction type"
INTERNAL_COUNT=$(grep -o -i -E -- "(${INTERNAL_TERMS})" "$TEXT" 2>/dev/null | wc -l | tr -d ' ')
if [ "$INTERNAL_COUNT" -gt 0 ]; then
  echo "FAIL: $INTERNAL_COUNT internal reference(s) leaked into reader-facing text."
  grep -i -n -E -- "(${INTERNAL_TERMS})" "$TEXT" | head -5
  echo ""
  VIOLATIONS=$((VIOLATIONS + INTERNAL_COUNT))
fi

# Single words that are also ordinary English ("finding", "navigation") must be
# whole-word matched, or the lint cries wolf and gets ignored.
INTERNAL_WORDS="corpus extractions snippetText oId oIds"
for WORD in $INTERNAL_WORDS; do
  COUNT=$(grep -o -i -w -- "$WORD" "$TEXT" 2>/dev/null | wc -l | tr -d ' ')
  if [ "$COUNT" -gt 0 ]; then
    echo "FAIL: Internal term '$WORD' found $COUNT time(s) in reader-facing text."
    grep -i -n -w -- "$WORD" "$TEXT" | head -3
    echo ""
    VIOLATIONS=$((VIOLATIONS + COUNT))
  fi
done

# Raw Octave record ids (evt_, ex_, crmo_, op_, px_, pe_, sg_, uu_, oj_, rr_)
ID_COUNT=$(grep -o -E -- '\b(evt|ex|crmo|op|px|pe|sg|uu|oj|rr|cn|wa|wz)_[A-Za-z0-9]{8,}' "$TEXT" 2>/dev/null | wc -l | tr -d ' ')
if [ "$ID_COUNT" -gt 0 ]; then
  echo "FAIL: $ID_COUNT raw record id(s) exposed in reader-facing text."
  grep -n -E -- '\b(evt|ex|crmo|op|px|pe|sg|uu|oj|rr|cn|wa|wz)_[A-Za-z0-9]{8,}' "$TEXT" | head -3
  echo ""
  VIOLATIONS=$((VIOLATIONS + ID_COUNT))
fi

# --- Emoji / pictographs (banned outright by presentation-principles.md) ---
EMOJI_COUNT=$(perl -CSD -ne 'print "$&\n" while /[\x{1F000}-\x{1FAFF}\x{2600}-\x{27BF}\x{FE0F}\x{2190}-\x{21FF}\x{2B00}-\x{2BFF}]/g' "$TEXT" 2>/dev/null | wc -l | tr -d ' ')
if [ "$EMOJI_COUNT" -gt 0 ]; then
  echo "FAIL: $EMOJI_COUNT emoji/pictograph character(s) in reader-facing text."
  perl -CSD -ne 'print "$.: $_" if /[\x{1F000}-\x{1FAFF}\x{2600}-\x{27BF}\x{FE0F}\x{2190}-\x{21FF}\x{2B00}-\x{2BFF}]/' "$TEXT" | head -3
  echo ""
  VIOLATIONS=$((VIOLATIONS + EMOJI_COUNT))
fi

# --- Standalone-document structure ---
# A skill artifact is served as-is by the asset service, not wrapped in a host
# page. Without a doctype the browser renders in quirks mode, where tables do
# NOT inherit `color` from an ancestor: a correct dark-spread stylesheet then
# paints ink-on-ink and the text silently disappears. This check is cheap and
# catches a class of bug that looks like nothing in the CSS.
if ! head -c 2000 "$FILE" | grep -q -i -- '<!doctype html'; then
  echo "FAIL: No <!DOCTYPE html>. The browser falls back to quirks mode, where tables"
  echo "      do not inherit color and dark-surface text can render invisibly."
  echo ""
  VIOLATIONS=$((VIOLATIONS + 1))
fi
if ! grep -q -i -E -- '<html[^>]*\blang=' "$FILE"; then
  echo "WARN: No lang attribute on <html>. Add lang=\"en\" for screen readers."
  echo ""
fi
if ! grep -q -i -E -- '<meta[^>]*charset=' "$FILE"; then
  echo "WARN: No <meta charset>. Add charset=\"utf-8\" so quotes and symbols render."
  echo ""
fi

# --- Self-containment: no external requests ---
# A hosted artifact runs behind a strict CSP and may be opened offline. Remote
# fonts, scripts, and images are the most common way a shipped asset degrades.
# Anchors to external pages are legitimate; only fetched subresources fail.
# <link href> counts even without a file extension: the single most common
# offender is a Google Fonts URL like /css2?family=Inter, which has none.
EXT_ASSET_REFS=$(grep -o -i -E -- '<link[^>]*href="https?://[^"]*"|src="https?://[^"]*"|href="https?://[^"]*\.(css|woff2?|ttf|otf|js|png|jpe?g|svg|webp|gif)"|@import[[:space:]]*(url\()?[[:space:]]*[\x27"]?https?:' "$FILE" 2>/dev/null | head -10)
if [ -n "$EXT_ASSET_REFS" ]; then
  EXT_COUNT=$(echo "$EXT_ASSET_REFS" | wc -l | tr -d ' ')
  echo "FAIL: $EXT_COUNT external asset reference(s). Inline or base64-embed them."
  echo "$EXT_ASSET_REFS" | head -5
  echo ""
  VIOLATIONS=$((VIOLATIONS + EXT_COUNT))
fi

# --- Fonts declared must actually be delivered ---
# Naming a face in font-family does not load it. A declared-but-unloaded brand
# font silently falls back to a system face, which reads as "generic template".
if grep -q -i -- '@font-face' "$FILE"; then
  if ! grep -q -i -E -- 'src:[^;]*(data:(font|application)/[^;]*;base64|url\([\x27"]?data:)' "$FILE"; then
    echo "FAIL: @font-face present but no embedded base64 src. A hosted artifact"
    echo "      cannot rely on a remote font URL; embed the woff2 as a data URI."
    echo ""
    VIOLATIONS=$((VIOLATIONS + 1))
  fi
fi

# --- Summary ---
echo "─────────────────"
if [ "$VIOLATIONS" -eq 0 ]; then
  echo "PASS: Zero mechanical violations."
  exit 0
else
  echo "TOTAL VIOLATIONS: $VIOLATIONS"
  echo "Fix all violations before proceeding to editorial review."
  exit 1
fi
