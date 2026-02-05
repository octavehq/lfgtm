---
name: generate
description: Generate GTM content (emails, LinkedIn messages, call prep) using your Octave library context
---

# Octave Generate Skill

Generate GTM content using your Octave library context.

## Usage

```
/octave:generate <type> [options]
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

## Instructions

When the user runs `/octave:generate`:

1. **Parse the Request**
   Identify:
   - Content type (email, linkedin, call-prep, content)
   - Target person/company if specified
   - Topic or context
   - Optional constraints (persona, playbook, etc.)

2. **Gather Context**
   Before generating, collect relevant context using MCP tools:

   **For Email:**
   - If person specified, use `find_person` to get details
   - If company specified, use `find_company` to get company info
   - Use `search_knowledge_base` to get relevant messaging
   - Match to appropriate persona and playbook

   **For LinkedIn:**
   - Use `find_person` to research the recipient
   - Use `search_knowledge_base` for relevant talking points
   - Consider connection context (mutual connections, shared interests)

   **For Call Prep:**
   - Use `find_company` and `find_person` for attendee research
   - Use `get_playbook` if specified
   - Use `search_knowledge_base` for relevant proof points and use cases

3. **Generate Content Using MCP Tools**

   Call the tools directly (they're pre-loaded, no ToolSearch needed).

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

   **For General Content:**
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

4. **Present Generated Content**
   Format the output clearly with:
   - The generated content
   - Context used (persona, playbook, etc.)
   - Suggestions for customization

5. **Offer Refinement Options**
   - "Would you like me to adjust the tone?"
   - "Should I add more proof points?"
   - "Want a version for a different persona?"

## Tips

- Provide as much context as possible for better results
- Specify the persona if you know who you're targeting
- Use `/octave:research` first if you need more info about the recipient

## Examples

### Quick Email
```
/octave:generate email --to "engineering leader" --about "reducing CI/CD pipeline time"
```

### Detailed Email with Context
```
/octave:generate email --to "Mike Johnson, VP Eng at TechCorp (500 employees, Series B)" --about "improving developer productivity" --persona "Engineering Leader" --playbook "Enterprise DevOps"
```

### Call Prep
```
/octave:generate call-prep --for "Discovery call with Acme Corp" --focus "security compliance, scalability"
```

## Related Skills

- `/octave:research` - Research recipients before generating
- `/octave:library` - Save successful messaging patterns back to library
