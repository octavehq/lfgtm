# Workflow File Format Reference

Workflows are `.workflow.md` files with YAML front matter and markdown step definitions.

**Front Matter (YAML):**
```yaml
---
name: Workflow Display Name
description: One-line description of what the workflow does
author: username          # optional
tags: [tag1, tag2]        # optional
inputs:
  - name: variable_name
    type: string          # string, number, or boolean
    required: true        # or false
    description: Human-readable description
    default: value        # optional, for non-required inputs
delivery:                 # optional — where to deliver results
  destination: outreach | apollo | salesloft | instantly | salesforce | hubspot | pipedrive | google_docs | notion | confluence | gamma | google_slides | slack | email | marketo | mailchimp | local_file | conversation
  format: csv | markdown | html | plain_text | slide_outline | crm_notes
---
```

**Steps (Markdown):**

Each step is an `### Step N: Name` heading followed by key-value fields:

**Tool step:**
```markdown
### Step N: Step Name
tool: mcp_tool_name
params:
  paramName: "{{variable_or_literal}}"
  otherParam: "literal value"
save_as: result_name
description: What this step does and why.
```

**Decision step:**
```markdown
### Step N: Step Name
type: decision
condition: "result_name.field < threshold"
prompt: |
  Explanation of the decision.
  Options:
  1. First option
  2. Second option
  3. Third option
```

**Output step:**
```markdown
### Step N: Step Name
type: output
template: |
  WORKFLOW RESULTS
  ================
  Key result: {{saved_result.field}}
  Other data: {{another_result.field}}
```

**Available MCP Tools for Steps:**

Any MCP tool from the Octave server can be used in a workflow step:

| Phase | Tools |
|-------|-------|
| Research | `find_company`, `find_person`, `find_similar_companies`, `find_similar_people`, `enrich_company`, `enrich_person` |
| Qualify | `qualify_company`, `qualify_person` |
| Library | `list_all_entities`, `get_entity`, `get_playbook`, `search_knowledge_base`, `list_value_props` |
| Generate | `generate_email`, `generate_content`, `generate_call_prep` |
| Agents | `run_email_agent`, `run_content_agent`, `run_call_prep_agent`, `run_enrich_person_agent`, `run_enrich_company_agent`, `run_qualify_person_agent`, `run_qualify_company_agent` |
| Write | `create_entity`, `create_playbook`, `update_entity`, `update_playbook` |
| Deliver | `ListMcpResourcesTool` (discover connected MCP servers), any connected MCP server tools (Google Drive, Salesforce, Slack, etc.), Write tool (local files) |
