---
name: workspace
description: Show current Octave MCP server
---

# /octave:workspace - Workspace Status

Show which Octave MCP server is connected.

## Instructions

1. **Find the Octave MCP server** by looking at your available tools for ones like `verify_connection`, `get_entity`, `list_all_entities`

2. **Show the server name** (e.g. `octave-acme`):
```
   Current Octave Workspace
   ========================
   MCP Server: <mcpServerName>
```

3. **If no Octave tools found:**
```
   No Octave MCP server detected.

   Add one with: claude mcp add octave-<workspaceName> --transport http <url>
```

4. **If user asks to switch:** Explain they need to configure a different MCP server in their Claude settings.