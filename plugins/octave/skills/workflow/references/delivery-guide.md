# Delivering Workflow Results

When the user selects "Deliver to your tools", follow this MCP-first approach.

## Phase 1: Detect likely destination from workflow output

Map the workflow output type to a recommended destination:
- Email sequences → Email sequencer (Outreach, Apollo, Salesloft, Instantly)
- Account research / call prep → CRM (Salesforce, HubSpot, Pipedrive)
- Content / collateral → Documents (Google Docs, Notion, Confluence)
- Presentations → Slides (Gamma, Google Slides, PowerPoint)
- Reports / data → File export (CSV, markdown, HTML)

## Phase 2: Check for MCP connectors

Inspect your available tools for connected MCP servers that match the destination:
- Google Drive MCP → can write docs directly
- Salesforce/HubSpot MCP → can create CRM records
- Slack MCP → can post to channels
- Notion MCP → can create pages
- Any other connected MCP server whose tools fit the output type

## Phase 3: Branch based on what's available

**If matching MCP server found:**
```
I can push these results directly to [Tool] via your connected MCP server.

Detected: [MCP Server Name] connected
Destination: [specific location — e.g., Drive folder, CRM object, Slack channel]

Ready to push? (yes / choose a different destination)
```

Use the MCP server's tools to write/push the output directly.

**If no matching MCP server found, ask for destination:**
```
Where should these results go?

OUTREACH & SEQUENCERS
1. Outreach / Apollo / Salesloft / Instantly

CRM
2. Salesforce / HubSpot / Pipedrive

DOCUMENTS
3. Google Docs / Notion / Confluence

PRESENTATIONS
4. Gamma / Google Slides / PowerPoint

COMMUNICATION
5. Slack / Email

MARKETING AUTOMATION
6. Marketo / Pardot / Mailchimp

FILE EXPORT
7. Local file (markdown, HTML, CSV, plain text)

8. Keep in conversation (already displayed)

Your choice (or name your tool):
```

After the user picks a destination, check for MCP:
```
Do you have an MCP server for [Tool] connected?

If yes → Connect it and I'll push directly.
If no → I'll format the output for easy import.
```

## Phase 4: Format for import (when no MCP connector)

Recommend the best format based on destination, then generate:

| Destination | Recommended Format | Why |
|---|---|---|
| Outreach / Apollo / Salesloft / Instantly | CSV (Step, Subject, Body, Wait Days) | Direct sequence import |
| Salesforce / HubSpot / Pipedrive | Structured text (Account Summary, Stakeholders, Next Steps) | Paste into notes/activity fields |
| Google Docs | Clean markdown with headers | Import or paste preserves structure |
| Notion | Markdown with toggles/callouts | Native Notion markdown support |
| Confluence | Markdown or HTML | Paste into Confluence editor |
| Gamma | Numbered slide outline (Title + bullets per slide) | Paste into Gamma "Generate" |
| Google Slides / PowerPoint | Slide outline with speaker notes | Copy into slide builder |
| Slack | Formatted message blocks | Post as Slack message |
| Email (direct) | HTML email or plain text | Send or paste into email client |
| Marketo / Pardot | HTML email templates | Import as email template |
| Mailchimp | HTML email with merge tags | Import as campaign |
| Local file | User choice: `.md`, `.html`, `.csv`, `.txt` | Write to `./octave-output/<workflow>-<date>.<ext>` |

Present as:
```
For [Tool], I recommend: [Format]
[Brief reason why this format works best]

Other options:
- [Alternative format 1]
- [Alternative format 2]

Which format? (or press Enter for recommended):
```

Write the formatted output using the Write tool (for files) or display inline (for paste targets).
