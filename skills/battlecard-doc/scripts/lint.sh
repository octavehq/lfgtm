#!/bin/bash
# Battlecard-doc mechanical lint — deterministic checks that don't need LLM judgment.
# Usage: bash lint.sh <path-to-output.html>
# Returns non-zero exit code if any violations found.

FILE="$1"
if [ -z "$FILE" ] || [ ! -f "$FILE" ]; then
  echo "Usage: bash lint.sh <path-to-output.html>"
  exit 1
fi

VIOLATIONS=0

echo "MECHANICAL LINT"
echo "==============="
echo "File: $FILE"
echo ""

# --- Em-dashes (U+2014) and en-dashes (U+2013) ---
EMDASH_COUNT=$(grep -o '—' "$FILE" 2>/dev/null | wc -l | tr -d ' ')
[ -z "$EMDASH_COUNT" ] && EMDASH_COUNT=0
if [ "$EMDASH_COUNT" -gt 0 ]; then
  echo "FAIL: $EMDASH_COUNT em-dash(es) found (U+2014). Replace with commas, periods, or \"to\"."
  grep -n '—' "$FILE" | head -10
  echo ""
  VIOLATIONS=$((VIOLATIONS + EMDASH_COUNT))
fi
ENDASH_COUNT=$(grep -o '–' "$FILE" 2>/dev/null | wc -l | tr -d ' ')
[ -z "$ENDASH_COUNT" ] && ENDASH_COUNT=0
if [ "$ENDASH_COUNT" -gt 0 ]; then
  echo "FAIL: $ENDASH_COUNT en-dash(es) found (U+2013). Replace with commas, periods, or \"to\"."
  grep -n '–' "$FILE" | head -10
  echo ""
  VIOLATIONS=$((VIOLATIONS + ENDASH_COUNT))
fi

# --- Double-hyphens used as dashes ---
# Exclude HTML comments (<!--) and CSS properties
DOUBLEDASH=$(grep -n '\-\-' "$FILE" | grep -v '<!--' | grep -v '\-\-kit' | grep -v '\-\-brand' | grep -v '\-\-bg' | grep -v '\-\-text' | grep -v '\-\-font' | grep -v '\-\-border' | grep -v '\-\-accent' | grep -v '\-\-on-' | grep -v 'var(--' | grep -v '<style' | grep -v 'css' | grep -c '' 2>/dev/null || echo 0)
# This check is noisy with CSS custom properties, so skip it for now

# --- Tier 1 banned words ---
BANNED_WORDS="delve landscape robust comprehensive leverage seamless seamlessly cutting-edge pivotal underscores meticulous meticulously utilize holistic holistically actionable impactful learnings synergy synergies game-changer game-changing tapestry realm paradigm embark beacon"
for WORD in $BANNED_WORDS; do
  # Case-insensitive search in text content (skip CSS/JS/HTML tags)
  COUNT=$(grep -ioP "(?<=>)[^<]*\b${WORD}\b[^<]*(?=<)" "$FILE" 2>/dev/null | wc -l | tr -d ' ')
  if [ "$COUNT" -gt 0 ]; then
    echo "FAIL: Banned word '$WORD' found $COUNT time(s)."
    grep -inP "(?<=>)[^<]*\b${WORD}\b[^<]*(?=<)" "$FILE" | head -5
    echo ""
    VIOLATIONS=$((VIOLATIONS + COUNT))
  fi
done

# --- Banned phrases ---
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
  COUNT=$(grep -ioP "(?<=>)[^<]*${PHRASE}[^<]*(?=<)" "$FILE" 2>/dev/null | wc -l | tr -d ' ')
  if [ "$COUNT" -gt 0 ]; then
    echo "FAIL: Banned phrase '$PHRASE' found $COUNT time(s)."
    grep -inP "(?<=>)[^<]*${PHRASE}[^<]*(?=<)" "$FILE" | head -3
    echo ""
    VIOLATIONS=$((VIOLATIONS + COUNT))
  fi
done

# --- Text density: single <p> tags with 3+ sentences ---
# Count periods followed by a space and uppercase letter (rough sentence boundary)
DENSE_BLOCKS=$(grep -oP '<p[^>]*>[^<]{100,}</p>' "$FILE" 2>/dev/null | while read -r line; do
  SENTENCES=$(echo "$line" | grep -oP '\. [A-Z]' | wc -l | tr -d ' ')
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
INTERNAL_TERMS="the library|source of truth|entity type|objection entities|use case entities|no .* entities|library says|library doesn.t|Octave internals|findings show|field data indicates|the data shows"
INTERNAL_COUNT=$(grep -ioP "(?<=>)[^<]*(${INTERNAL_TERMS})[^<]*(?=<)" "$FILE" 2>/dev/null | wc -l | tr -d ' ')
if [ "$INTERNAL_COUNT" -gt 0 ]; then
  echo "FAIL: $INTERNAL_COUNT internal reference(s) leaked into reader-facing text."
  grep -inP "(?<=>)[^<]*(${INTERNAL_TERMS})[^<]*(?=<)" "$FILE" | head -5
  echo ""
  VIOLATIONS=$((VIOLATIONS + INTERNAL_COUNT))
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
