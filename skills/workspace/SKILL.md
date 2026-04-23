---
name: workspace
description: Show current Octave MCP server connection and status. Use when user says "which workspace", "show connection", "what server", or asks about Octave setup.
---

# /octave:workspace - Workspace Status

Show which Octave MCP server is connected.

## Instructions

1. **Find the Octave MCP server** by looking at your available tools for ones like `verify_connection`, `get_entity`, `list_all_entities`.

2. **Call `verify_connection`** to confirm the API key is valid and to fetch the authoritative workspace/organization names. This is the canonical probe.

3. **Show the server name and workspace info** from the `verify_connection` response:
```
   Current Octave Workspace
   ========================
   MCP Server:   <mcpServerName>
   Workspace:    <workspaceName> (<workspaceOId>)
   Organization: <organizationSlug> (<organizationOId>)
```

4. **If no Octave tools found:**
```
   No Octave MCP server detected.

   Add one with: claude mcp add octave-<workspaceName> --transport http <url>
```

5. **If `verify_connection` fails** (invalid API key, network error): surface the error message and suggest re-running `claude mcp add` with a fresh API key.

6. **If user asks to switch:** Explain they need to configure a different MCP server in their Claude settings.