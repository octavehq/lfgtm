# Claude Tag overlay

`octave.mcp.json` is the credential-less Octave MCP server declaration. It is **not**
part of the installable `octave` plugin — Claude Code installs the plugin straight from
the repo, and a credential-less MCP server there resolves to a workspace-less, failing
`octave` server (in Claude Code you add your own workspace with `claude mcp add`).

Instead, the [publish-claude-tag-zip](../.github/workflows/publish-claude-tag-zip.yml)
workflow copies this file to `plugins/octave/.mcp.json` **only when building the Claude Tag
upload zip**, where an access bundle injects the API-key credential at the network layer so
the declaration works. See the README's "Claude Tag" section.
