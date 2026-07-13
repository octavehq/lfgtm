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
#   • workflows/*.workflow.md → thin commands/*.md wrappers that invoke the
#     workflow engine skill (the workflow templates themselves ship verbatim
#     in workflows/, where the workflow skill discovers them)
# Skill names and /octave: namespacing are preserved verbatim, since Cursor
# namespaces plugin skills the same way Claude Code does.

set -euo pipefail

SRC_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT="$SRC_ROOT/build/cursor"

command -v jq >/dev/null || { echo "jq required"; exit 1; }

echo "→ cleaning $OUT"
rm -rf "$OUT"
mkdir -p "$OUT/.cursor-plugin" "$OUT/skills" "$OUT/agents" "$OUT/commands" "$OUT/workflows"

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
}' "$SRC_ROOT/plugins/octave/.claude-plugin/plugin.json" \
  > "$OUT/.cursor-plugin/plugin.json"

# 2. .cursor-plugin/marketplace.json — Cursor schema differs from Claude's
#    (owner{name,email?}, plugins[].source is a string path).
#    Only the octave plugin is mirrored: octave-claude-tag is a Claude-Tag-only
#    server declaration (plugins/octave-claude-tag/), and mapping every marketplace
#    entry to source "./" would advertise it as a phantom copy of this repo.
echo "→ .cursor-plugin/marketplace.json"
jq '{
  name: .name,
  owner: { name: .owner.name },
  metadata: { description: .metadata.description },
  plugins: [
    .plugins[] | select(.name == "octave") | { name, source: "./", description, version }
  ]
}' "$SRC_ROOT/.claude-plugin/marketplace.json" \
  > "$OUT/.cursor-plugin/marketplace.json"

# 3. skills/ — identical format, copy verbatim (names + /octave: refs preserved;
#    includes skills/shared/, the cross-skill reference dir that skills read)
echo "→ skills/"
cp -R "$SRC_ROOT"/plugins/octave/skills/. "$OUT/skills/"

# 4. agents/ — Cursor supports agents natively, copy verbatim
echo "→ agents/"
cp "$SRC_ROOT"/plugins/octave/agents/*.md "$OUT/agents/"

# 5. workflows/ — ship the templates verbatim so the workflow engine skill
#    (/octave:workflow) can discover and run them, same as in Claude Code.
echo "→ workflows/"
cp "$SRC_ROOT"/plugins/octave/workflows/*.workflow.md "$OUT/workflows/"

# 6. commands/ — one thin wrapper per workflow. The wrapper hands off to the
#    workflow engine skill rather than embedding the workflow DSL, so command
#    execution and /octave:workflow runs share a single source of truth.
echo "→ commands/ (wrappers for workflows/)"
for f in "$SRC_ROOT"/plugins/octave/workflows/*.workflow.md; do
  base="$(basename "$f" .workflow.md)"
  wf_name="$(awk '/^name:/{sub(/^name:[[:space:]]*/,""); print; exit}' "$f")"
  wf_desc="$(awk '/^description:/{sub(/^description:[[:space:]]*/,""); print; exit}' "$f")"
  cat > "$OUT/commands/$base.md" <<CMD
---
description: ${wf_desc}
---

Run the "${wf_name}" Octave workflow using the workflow engine skill:

/octave:workflow run "${wf_name}"

Before starting, read the template at \`workflows/${base}.workflow.md\` in this
plugin for the workflow's inputs, collect any required inputs from the user
(or from arguments passed to this command), then execute the workflow step by
step with the human-in-the-loop checkpoints it defines.
CMD
done

# 7. LICENSE
cp "$SRC_ROOT/LICENSE" "$OUT/LICENSE"

# 8. README — Cursor-specific
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
- **Workflows** — multi-step GTM playbooks (account-based research, competitive deal prep, full outbound pipeline, …) run via `/octave:workflow`.
- **Commands** — one shortcut per workflow, so each playbook is also directly invocable as a command.

See the [upstream README](https://github.com/octavehq/lfgtm#skills) for full descriptions.
EOF

# 9. Summary
echo
echo "✓ Built Cursor artifact at $OUT"
echo "  skills:    $(find "$OUT/skills" -name SKILL.md | wc -l | tr -d ' ')"
echo "  agents:    $(find "$OUT/agents" -name '*.md' | wc -l | tr -d ' ')"
echo "  workflows: $(find "$OUT/workflows" -name '*.workflow.md' | wc -l | tr -d ' ')"
echo "  commands:  $(find "$OUT/commands" -name '*.md' | wc -l | tr -d ' ')"
