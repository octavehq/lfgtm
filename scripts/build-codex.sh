#!/usr/bin/env bash
# Generate a Codex-compatible plugin from this Claude Code plugin.
# Output: build/codex/  (gitignored — pushed to the lfgtm-codex repo by CI)
#
# Run locally:   ./scripts/build-codex.sh
# In CI:         same, then commit build/codex/ to the lfgtm-codex repo.

set -euo pipefail

SRC_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT="$SRC_ROOT/build/codex"

# ---- toggles ----------------------------------------------------------------
NAMESPACE_PREFIX="octave-"   # "" to keep bare names; "octave-" to rename skills/foo → octave-foo
CONVERT_AGENTS="drop"        # "drop" | "skills" (convert agents/*.md to skills)
# -----------------------------------------------------------------------------

command -v jq >/dev/null || { echo "jq required"; exit 1; }

echo "→ cleaning $OUT"
rm -rf "$OUT"
mkdir -p "$OUT/.codex-plugin" "$OUT/skills" "$OUT/workflows" "$OUT/.agents/plugins"

# ----- NOTE on MCP config -----
# Codex's MCP config is TOML (~/.codex/config.toml with [mcp_servers.<name>] tables).
# Users add their own workspace-specific Octave server via `codex mcp add`. The plugin
# itself ships no MCP file — matching the Claude plugin's pattern.

# 1. plugin.json: preserve name/version/description/author, add Codex pointers
echo "→ .codex-plugin/plugin.json"
jq '{
  name, version, description, author,
  skills: "./skills/",
  interface: {
    displayName: "Octave GTM",
    shortDescription: .description,
    category: "Productivity"
  }
}' "$SRC_ROOT/.claude-plugin/plugin.json" \
  > "$OUT/.codex-plugin/plugin.json"

# 2. marketplace.json: Codex schema is different from Claude's — rebuild from scratch
echo "→ .agents/plugins/marketplace.json"
jq '{
  name: .name,
  interface: { displayName: "Octave GTM Plugins" },
  plugins: [
    .plugins[] | {
      name, description,
      source: { source: "local", path: "./" },
      policy: { installation: "AVAILABLE", authentication: "ON_INSTALL" },
      category: "Productivity"
    }
  ]
}' "$SRC_ROOT/.claude-plugin/marketplace.json" \
  > "$OUT/.agents/plugins/marketplace.json"

# 3. skills/: copy and optionally rename + rewrite inline refs
echo "→ skills/ (prefix='$NAMESPACE_PREFIX')"
for dir in "$SRC_ROOT"/skills/*/; do
  src_name="$(basename "$dir")"
  dst_name="${NAMESPACE_PREFIX}${src_name}"
  cp -R "$dir" "$OUT/skills/$dst_name"

  skill_md="$OUT/skills/$dst_name/SKILL.md"

  # Rewrite the frontmatter name field
  if [[ -n "$NAMESPACE_PREFIX" ]]; then
    # YAML name: field (first occurrence, inside frontmatter)
    awk -v new="$dst_name" '
      BEGIN { in_fm=0; done=0 }
      /^---$/ { in_fm = !in_fm; print; next }
      in_fm && !done && /^name:/ { print "name: " new; done=1; next }
      { print }
    ' "$skill_md" > "$skill_md.tmp" && mv "$skill_md.tmp" "$skill_md"
  fi

  # Rewrite inline references: /octave:foo → /octave-foo
  sed -i.bak 's#/octave:\([a-z][a-z0-9-]*\)#/octave-\1#g' "$skill_md"
  rm -f "$skill_md.bak"
done

# 4. workflows/: plain markdown, safe to copy as-is
echo "→ workflows/"
cp -R "$SRC_ROOT"/workflows/*.md "$OUT/workflows/"

# 5. agents/: no Codex equivalent
case "$CONVERT_AGENTS" in
  drop)
    echo "→ agents/ dropped (no Codex equivalent)"
    ;;
  skills)
    echo "→ agents/ converted to skills/ (invocation semantics differ — see README note)"
    mkdir -p "$OUT/skills"
    for f in "$SRC_ROOT"/agents/*.md; do
      base="$(basename "$f" .md)"
      dst="$OUT/skills/${NAMESPACE_PREFIX}${base}"
      mkdir -p "$dst"
      cp "$f" "$dst/SKILL.md"
    done
    ;;
esac

# 6. README: Codex-specific install instructions
cat > "$OUT/README.md" <<EOF
# Octave Codex Plugin

> Generated from [octavehq/lfgtm](https://github.com/octavehq/lfgtm). Do not edit directly — changes will be overwritten. File issues and PRs on the upstream repo.

GTM knowledge base integration for OpenAI Codex CLI.

## Install

\`\`\`bash
codex plugin marketplace add https://github.com/octavehq/lfgtm-codex
codex plugin install octave@lfgtm
\`\`\`

## Configure your Octave MCP server

Add your workspace's MCP server (one per workspace):

\`\`\`bash
codex mcp add octave-acme --url https://mcp.octavehq.com/mcp?ctx=<context>
\`\`\`

Use any name starting with \`octave-\`. Skills detect the Octave server from available tools.

## Skills

All upstream skills are available, renamed with the \`octave-\` prefix to avoid collisions in the Codex skill namespace:

- \`/octave-research\` (was \`/octave:research\` in Claude Code)
- \`/octave-library\`, \`/octave-generate\`, \`/octave-battlecard\`, …

See the [upstream README](https://github.com/octavehq/lfgtm#skills) for full descriptions.

## Not included

The upstream plugin ships four subagent personas (\`octave-assistant\`, \`pmm-strategist\`, \`sdr-coach\`, \`revenue-strategist\`). Codex has no subagent concept, so these are not available in this build. Use the corresponding skills directly.
EOF

# 8. Summary
echo
echo "✓ Built Codex artifact at $OUT"
echo "  skills:    $(find "$OUT/skills" -name SKILL.md | wc -l | tr -d ' ')"
echo "  workflows: $(find "$OUT/workflows" -name '*.md' | wc -l | tr -d ' ')"
