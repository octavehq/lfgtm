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

Each step is an `### Step N: Name` heading followed by key-value fields. A step may contain multiple `tool:` blocks when several related calls belong to one logical step (run them in order, each with its own `params:` / `save_as:`). Prose lines between fields are execution guidance — follow them.

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

**Decision step** (prompt form — options embedded in the prompt text):
```markdown
### Step N: Step Name
type: decision
condition: "result_name.field < threshold"   # optional — when present, only pause if true
prompt: |
  Explanation of the decision.
  Options:
  1. First option
  2. Second option
  3. Third option
save_as: chosen_option
```

**Decision step** (present/options form — structured options):
```markdown
### Step N: Step Name
type: decision
description: What is being decided
present: |
  SUMMARY SHOWN TO THE USER
  Key data: {{saved_result.field}}
options:
  - label: Human-readable choice
    value: machine_value
  - label: Another choice
    value: other_value
save_as: chosen_option
```

Both decision forms behave the same: show the material, wait for the user's choice (unless `--auto`), and store the choice in the context map under `save_as` so later steps can reference it (e.g. `{{chosen_option}}`).

**Skill step** (invoke another plugin skill as a step):
```markdown
### Step N: Step Name
type: skill
skill: /octave:positioning
inputs:
  product: "{{product_detail.name}}"
  style: "{{style}}"
save_as: skill_output
description: What the skill should produce. Pass gathered context from the context map.
```

Run the named skill with the given inputs plus any relevant saved context, then store its primary output (e.g. a generated file path) under `save_as`.

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

**Derived variables:**

Some `{{variables}}` are computed at run time rather than saved by a step:

| Variable | Meaning |
|----------|---------|
| `{{current_date}}` | Today's date |
| `{{N_days_ago}}` (e.g. `{{90_days_ago}}`, `{{365_days_ago}}`) | ISO date N days before today — used for `startDate` filters |
| `{{period_start}}` | Today minus the `period_days` input (when the workflow defines one) |

Any other derived value (e.g. `{{persona_titles}}` from a persona lookup, or an oId the user picks from a listed result) must be introduced by a step — either a tool step's `save_as`, a decision step's `save_as`, or an explicit instruction in a step's description saying how to resolve it. Don't reference variables that nothing defines.

**Available MCP Tools for Steps:**

Any MCP tool from the Octave server can be used in a workflow step:

| Phase | Tools |
|-------|-------|
| Research | `find_company`, `find_person`, `find_similar_companies`, `find_similar_people`, `enrich_company`, `enrich_person` |
| Qualify | `qualify_company`, `qualify_person` |
| Library | `list_all_entities`, `list_entities`, `get_entity`, `list_motions`, `list_motion_playbooks`, `get_motion_playbook`, `list_motion_icps`, `find_motion_icp`, `search_knowledge_base` |
| Conversation data | `list_events`, `list_findings`, `get_event_detail` |
| Generate | `generate_email`, `generate_content`, `generate_call_prep` |
| Agents | `run_email_agent`, `run_content_agent`, `run_call_prep_agent`, `run_enrich_person_agent`, `run_enrich_company_agent`, `run_qualify_person_agent`, `run_qualify_company_agent` |
| Write | `create_entity`, `create_motion_playbook`, `update_entity`, `update_motion_playbook` |
| Deliver | Any connected MCP server whose tools match the destination (Google Drive, Salesforce, Slack, etc.) — inspect your available tools to see what's connected — plus the Write tool for local files |
