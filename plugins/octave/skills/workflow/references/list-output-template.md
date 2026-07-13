# List Output Template

Build the list dynamically: read every `.workflow.md` file in the plugin's `workflows/` directory (TEMPLATES) and in `~/.octave/workflows/` (MY WORKFLOWS), parse each file's front matter, and render one entry per workflow. Never hardcode the inventory — new template files should appear automatically.

```
AVAILABLE WORKFLOWS
===================

TEMPLATES (N)
-------------

1. [Workflow Name]
   [One-line description from front matter]
   Inputs: [input names, marking required ones]
   Run: /octave:workflow run "[Workflow Name]" [--flags for required inputs]

2. [Workflow Name]
   ...

[One entry per .workflow.md file found in the plugin's workflows/ directory]

---

MY WORKFLOWS (N)
-----------------

1. [Workflow Name]
   [One-line description from front matter]
   Inputs: [input names, marking required ones]
   Run: /octave:workflow run "[Workflow Name]" [--flags for required inputs]

[One entry per .workflow.md file found in ~/.octave/workflows/]

---

Use /octave:workflow show <name> for details.
Use /octave:workflow create to build a new workflow.
```

Example entry, fully rendered:

```
1. Full Outbound Pipeline
   Research, qualify, and generate personalized outreach for a target company
   Inputs: company_domain (required), persona, motion, num_contacts
   Run: /octave:workflow run "Full Outbound Pipeline" --company <domain>
```
