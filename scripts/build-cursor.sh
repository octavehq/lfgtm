#!/usr/bin/env bash
# Generate a Cursor-compatible plugin from this Claude Code plugin.
# Output: build/cursor/  (gitignored — pushed to the lfgtm-cursor repo by CI)
#
# Run locally:   ./scripts/build-cursor.sh
# In CI:         same, then commit build/cursor/ to the lfgtm-cursor repo.
#
# Cursor plugins (https://cursor.com/docs/reference/plugins) are very close to
# Claude Code plugins: same skills/ + SKILL.md format, and — unlike Codex —
# Cursor natively supports agents/. So this build is almost a 1:1 mirror. The
# only translations are:
#   • .claude-plugin/  → .cursor-plugin/   (manifest schema)
#   • workflows/*.workflow.md → commands/*.md  (Cursor's agent-executable actions)
# Skill names and /octave: namespacing are preserved verbatim, since Cursor
# namespaces plugin skills the same way Claude Code does.

set -euo pipefail

SRC_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT="$SRC_ROOT/build/cursor"

command -v jq >/dev/null || { echo "jq required"; exit 1; }

echo "→ cleaning $OUT"
rm -rf "$OUT"
mkdir -p "$OUT/.cursor-plugin" "$OUT/skills" "$OUT/agents" "$OUT/commands"

# ----- NOTE on MCP config -----
# Cursor reads mcp.json at the plugin root, but — matching the Claude/Codex
# plugins — we ship none. Each user adds their own workspace-specific Octave
# MCP server. Skills detect the Octave server from the available tools.

# 1. .cursor-plugin/plugin.json — preserve name/version/description/author,
#    add Cursor component pointers. (Folder discovery would find these anyway,
#    but being explicit documents the layout.)
echo "→ .cursor-plugin/plugin.json"
jq '{
  name, version,
  description: "Octave GTM knowledge base integration for Cursor — grounded access to personas, Motions, messaging, and positioning as skills, agents, and commands.",
  author: { name: .author.name },
  homepage: "https://octavehq.com",
  repository: "https://github.com/octavehq/lfgtm-cursor",
  license: "MIT",
  skills: "./skills/",
  agents: "./agents/",
  commands: "./commands/"
}' "$SRC_ROOT/.claude-plugin/plugin.json" \
  > "$OUT/.cursor-plugin/plugin.json"

# 2. .cursor-plugin/marketplace.json — Cursor schema differs from Claude's
#    (owner{name,email?}, plugins[].source is a string path).
echo "→ .cursor-plugin/marketplace.json"
jq '{
  name: .name,
  owner: { name: .owner.name },
  metadata: { description: .metadata.description },
  plugins: [
    .plugins[] | { name, source: "./", description, version }
  ]
}' "$SRC_ROOT/.claude-plugin/marketplace.json" \
  > "$OUT/.cursor-plugin/marketplace.json"

# 3. skills/ — identical format, copy verbatim (names + /octave: refs preserved)
echo "→ skills/"
cp -R "$SRC_ROOT"/skills/. "$OUT/skills/"

# 4. agents/ — Cursor supports agents natively, copy verbatim
echo "→ agents/"
cp "$SRC_ROOT"/agents/*.md "$OUT/agents/"

# 5. workflows/ → commands/ — strip the .workflow suffix from the filename so
#    they surface as /<name> commands. Content (incl. frontmatter) copied as-is.
echo "→ commands/ (from workflows/)"
for f in "$SRC_ROOT"/workflows/*.workflow.md; do
  base="$(basename "$f" .workflow.md)"
  cp "$f" "$OUT/commands/$base.md"
done

# 6. LICENSE
cp "$SRC_ROOT/LICENSE" "$OUT/LICENSE"

# 7. README — Cursor-specific
cat > "$OUT/README.md" <<'EOF'
# Octave Cursor Plugin

> Generated from [octavehq/lfgtm](https://github.com/octavehq/lfgtm). Do not edit directly — changes will be overwritten. File issues and PRs on the upstream repo.

GTM knowledge base integration for [Cursor](https://cursor.com). Provides grounded access to your Octave personas, Motions, messaging, positioning, and more — as skills, agents, and commands.

## Install

Add this plugin from the Cursor marketplace, or point Cursor at this repository:

```
https://github.com/octavehq/lfgtm-cursor
```

See Cursor's [plugins documentation](https://cursor.com/docs/reference/plugins) for installation details.

## Configure your Octave MCP server

This plugin ships no MCP config — add your workspace's Octave server (one per workspace) to Cursor's MCP settings:

```json
{
  "mcpServers": {
    "octave-acme": {
      "url": "https://mcp.octavehq.com/mcp?ctx=<context>"
    }
  }
}
```

Use any name starting with `octave-`. Skills detect the Octave server from the available tools.

## What's included

- **Skills** (`/octave:research`, `/octave:library`, `/octave:generate`, `/octave:battlecard`, …) — the full upstream skill set, invoked the same way as in Claude Code.
- **Agents** (`octave-assistant`, `pmm-strategist`, `sdr-coach`, `revenue-strategist`) — Octave's specialist GTM personas.
- **Commands** — multi-step GTM playbooks (account-based research, competitive deal prep, full outbound pipeline, …) adapted from the upstream workflows.

See the [upstream README](https://github.com/octavehq/lfgtm#skills) for full descriptions.
EOF

# 8. Summary
echo
echo "✓ Built Cursor artifact at $OUT"
echo "  skills:    $(find "$OUT/skills" -name SKILL.md | wc -l | tr -d ' ')"
echo "  agents:    $(find "$OUT/agents" -name '*.md' | wc -l | tr -d ' ')"
echo "  commands:  $(find "$OUT/commands" -name '*.md' | wc -l | tr -d ' ')"
