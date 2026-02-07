---
name: generate
description: Generate GTM content (emails, LinkedIn messages, call prep) using saved agents, Octave AI, or Claude direct — your choice
---

# /octave:generate - GTM Content Generator

Generate GTM content using your Octave library context. Choose how to generate: run a saved agent for consistency, use Octave's built-in AI, or have Claude draft it directly with Octave context.

## Usage

```
/octave:generate <type> [options] [--mode agent|octave|claude]
```

## Content Types

### Email Sequences
```
/octave:generate email --to "<person>" --about "<topic>" [--persona "<persona>"] [--playbook "<playbook>"]
```

Example:
```
/octave:generate email --to "John Smith, VP Engineering at Acme" --about "reducing deployment time"
```

### LinkedIn Messages
```
/octave:generate linkedin --to "<person>" --about "<topic>" [--type connection|inmail|follow-up]
```

Example:
```
/octave:generate linkedin --to "Sarah Chen, CTO" --about "DevOps automation" --type connection
```

### Call Prep
```
/octave:generate call-prep --for "<person/company>" [--playbook "<playbook>"] [--focus "<topics>"]
```

Example:
```
/octave:generate call-prep --for "Meeting with Acme Corp engineering team" --focus "security, scalability"
```

### General Content
```
/octave:generate content --type "<content-type>" --about "<topic>" [--persona "<persona>"]
```

Example:
```
/octave:generate content --type "objection handling" --about "pricing concerns" --persona "CFO"
```

## Generation Modes

Three ways to generate content, each with different trade-offs:

| Mode | Best For | How |
|------|----------|-----|
| Saved Agent | Consistency, team standards, repeatable sequences | `list_agents` → `run_*_agent` |
| Octave Default | Balanced quality + library grounding | `generate_email` / `generate_content` / `generate_call_prep` |
| Claude Direct | Maximum control, rapid iteration, custom formats | Fetch Octave context, Claude generates directly |

### Smart Inference Rules

Skip the mode question when intent is obvious:

- **"Run my cold outreach agent"** / **"use the enterprise agent"** → Saved Agent
- **"Generate an email for..."** / **"create a sequence"** → Octave Default
- **"Write me an email using our playbook"** / **"draft this yourself"** / **"I want more control"** → Claude Direct

### When Ambiguous, Ask (via AskUserQuestion tool)

When the mode is not obvious from the request, **always use the `AskUserQuestion` tool** to present the three options as a UI selector. Never silently default to one mode — let the user choose.

## Instructions

When the user runs `/octave:generate`:

### Step 1: Parse the Request

Identify:
- Content type (email, linkedin, call-prep, content)
- Target person/company if specified
- Topic or context
- Optional constraints (persona, playbook, etc.)
- Generation mode (if `--mode` flag or clear intent)

### Step 2: Determine Generation Mode

Apply smart inference rules from the request wording:
- **"Run my cold outreach agent"** / **"use the enterprise agent"** → Saved Agent (skip the question)
- **"Draft this yourself"** / **"I want more control"** / **"write it yourself"** → Claude Direct (skip the question)

**If mode is not obvious from the request, use the `AskUserQuestion` tool** to ask — do NOT default silently:

```
AskUserQuestion({
  questions: [{
    question: "How should I generate this?",
    header: "Gen mode",
    options: [
      { label: "Use a saved agent", description: "I'll find matching agents from your library for consistency and team standards" },
      { label: "Generate with Octave (Recommended)", description: "Octave AI generates using your library context — balanced quality" },
      { label: "I'll draft it directly", description: "I'll pull Octave context, then write it myself — maximum control" }
    ],
    multiSelect: false
  }]
})
```

IMPORTANT: Do not skip this question by defaulting to Octave. If the user didn't explicitly indicate a mode, you MUST ask using AskUserQuestion.

### Step 3: Generate (branch by mode)

---

#### Mode A: Saved Agent

Map the content type to an agent type and find matching agents:

| Content Type | Agent Type |
|---|---|
| email | EMAIL |
| linkedin | CONTENT |
| call-prep | CALL_PREP |
| content | CONTENT |

```
# Find matching agents
list_agents({ type: "<mapped_type>" })
```

If agents found, present them:
```
MATCHING AGENTS
===============

1. [Agent Name] — [Description]
   Run: Select this agent

2. [Agent Name] — [Description]
   Run: Select this agent

Which agent? (or switch to Octave default / Claude direct):
```

Run the selected agent:

**For Email Agents:**
```
run_email_agent({
  agent: "<agent name or oId>",
  person: {
    firstName: "<first name>",
    lastName: "<last name>",
    email: "<email>",
    linkedInProfile: "<linkedin url>",
    companyName: "<company>",
    companyDomain: "<domain>",
    jobTitle: "<title>"
  },
  allEmailsContext: "<additional context>",
  allEmailsInstructions: "<instructions>"
})
```

**For Content Agents:**
```
run_content_agent({
  agent: "<agent name or oId>",
  person: { ... },
  company: { ... },
  runtimeContext: "<additional context>"
})
```

**For Call Prep Agents:**
```
run_call_prep_agent({
  agent: "<agent name or oId>",
  person: { ... },
  meetingContext: "<meeting details>"
})
```

If no agents found:
```
No [type] agents found in your library.

Options:
1. Generate with Octave (default AI)
2. I'll draft it directly (Claude + Octave context)
3. Browse all agents: /octave:explore-agents

Your choice:
```

---

#### Mode B: Octave Default

Gather context, then call Octave's generation tools directly.

**Gather Context:**
- If person specified, use `find_person` to get details
- If company specified, use `find_company` to get company info
- Use `search_knowledge_base` to get relevant messaging
- Match to appropriate persona and playbook

**For Email Sequences:**
```
generate_email({
  person: {
    firstName: "<first name>",
    lastName: "<last name>",
    email: "<email>",
    linkedInProfile: "<linkedin url>",
    companyName: "<company>",
    title: "<job title>"
  },
  allEmailsContext: "<context for all emails>",
  allEmailsInstructions: "<instructions for all emails>",
  numEmails: 4
})
```

**For General Content (including LinkedIn):**
```
generate_content({
  instructions: "<detailed instructions for content generation>",
  customContext: "<additional context>",
  person: { /* optional person details */ },
  company: { /* optional company details */ }
})
```

**For Call Prep:**
```
generate_call_prep({
  person: {
    firstName: "<first name>",
    lastName: "<last name>",
    email: "<email>",
    linkedInProfile: "<linkedin url>",
    companyName: "<company>",
    jobTitle: "<job title>"
  },
  meetingContext: "<meeting details and focus areas>"
})
```

---

#### Mode C: Claude Direct

Gather the same Octave context, but Claude generates the content itself — no `generate_*` MCP calls.

**Gather Context (same as Octave Default):**
```
# Get persona details
search_knowledge_base({ query: "<topic> <persona>", entityTypes: ["persona"] })
get_entity({ oId: "<persona_oId>" })

# Get product details
list_all_entities({ entityType: "product" })
get_entity({ oId: "<product_oId>" })

# Get matching playbook and value props
search_knowledge_base({ query: "<topic>", entityTypes: ["playbook"] })
get_playbook({ oId: "<playbook_oId>", includeValueProps: true })

# Get proof points
search_knowledge_base({ query: "<topic>", entityTypes: ["proof_point", "reference"] })

# Get brand voice
list_brand_voices()

# Get competitive positioning if relevant
search_knowledge_base({ query: "<topic>", entityTypes: ["competitor"] })
```

**Generate directly:**
- Apply brand voice guidelines to tone and style
- Use value props as messaging anchors
- Incorporate proof points as evidence
- Structure based on content type (email format, LinkedIn format, call prep format, etc.)
- Claude has full control over structure, length, and approach

**Label the output:**
```
[Content here]

---

Generated by Claude (with Octave context)
Sources: [persona name], [playbook name], [proof points used], [brand voice]
```

### Step 4: Present Generated Content

Format the output clearly with:
- The generated content
- Context used (persona, playbook, brand voice, etc.)
- Generation mode used
- Suggestions for customization

### Step 5: Offer Refinement

```
What would you like to do?

1. Adjust tone or messaging
2. Add more proof points
3. Create version for a different persona
4. Try a different generation mode
5. Done

Your choice:
```

## Tips

- Provide as much context as possible for better results
- Specify the persona if you know who you're targeting
- Use `/octave:research` first if you need more info about the recipient
- Use `--mode agent` for repeatable, team-standard sequences
- Use `--mode claude` when you want maximum control over the output

## Examples

### Quick Email
```
/octave:generate email --to "engineering leader" --about "reducing CI/CD pipeline time"
```

### Using a Saved Agent
```
/octave:generate email --to "john@acme.com" --mode agent
```

### Claude Direct with Full Control
```
/octave:generate email --to "Sarah Chen, CTO at TechCorp" --about "DevOps automation" --mode claude
```

### Detailed Email with Context
```
/octave:generate email --to "Mike Johnson, VP Eng at TechCorp (500 employees, Series B)" --about "improving developer productivity" --persona "Engineering Leader" --playbook "Enterprise DevOps"
```

### Call Prep
```
/octave:generate call-prep --for "Discovery call with Acme Corp" --focus "security compliance, scalability"
```

## MCP Tools Used

### Agent Discovery & Execution
- `list_agents` - Find matching saved agents by type
- `run_email_agent` - Run a saved email sequence agent
- `run_content_agent` - Run a saved content generation agent
- `run_call_prep_agent` - Run a saved call prep agent

### Context Gathering
- `find_person` / `find_company` - Research recipients
- `search_knowledge_base` - Find relevant messaging, proof points, personas
- `get_entity` - Get full entity details (persona, product, competitor)
- `get_playbook` - Get playbook with value props
- `list_brand_voices` - Get brand voice for consistency

### Octave Generation
- `generate_email` - Email sequence generation (Octave Default mode)
- `generate_content` - General content generation (Octave Default mode)
- `generate_call_prep` - Call preparation generation (Octave Default mode)

## Related Skills

- `/octave:explore-agents` - Browse and manage all saved agents
- `/octave:research` - Research recipients before generating
- `/octave:library` - Save successful messaging patterns back to library
- `/octave:campaign` - Multi-channel campaign content (emails, social, ads, blog)
- `/octave:pmm` - Deep-dive collateral (case studies, one-pagers, decks)
- `/octave:messaging` - Build messaging frameworks to inform outreach
