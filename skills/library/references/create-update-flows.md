# Interactive Create and Update Flows

Detailed interactive flows for the `create` and `update` subcommands of `/octave:library`.

## Create — Custom Motion Playbooks

A **Motion** is the top-level container for a go-to-market motion (e.g., "Enterprise Outbound — Platform"). Creating a Motion is done in the Motion builder UI — it automatically generates a **Default Motion Playbook** covering the persona × segment matrix as Motion ICP cells. Once a Motion exists, this skill can layer **Custom Motion Playbooks** on top for specific angles (Thematic, Milestone, Account, Competitive).

Custom Motion Playbooks always sit under an existing Motion and have a narrative type.

1. **List available Motions:**
   ```
   list_motions()
   ```

2. **Ask user to select a Motion:**
   ```
   Which Motion is this Custom Motion Playbook layered on?

   1. Enterprise Outbound — Platform (mo_abc123)
   2. PLG Activation — Self-Serve (mo_def456)
   3. Renewal & Expansion — Tier 1 (mo_ghi789)

   Your choice:
   ```

3. **Ask for the narrative type:**
   ```
   What narrative type fits this Motion Playbook?

   1. THEMATIC — built around a theme, trend, or shared pain (e.g., "Q1 Cost Pressure")
   2. MILESTONE — built around an event or trigger (e.g., "Post-Funding Outreach")
   3. ACCOUNT — built around a specific named account or tight account list
   4. COMPETITIVE — built around displacing a specific competitor

   Your choice:
   ```

4. **Gather Motion Playbook details:**
   ```
   Creating Custom Motion Playbook: "Q1 Outbound — Cost Pressure"
   Under Motion: [Selected Motion]
   Narrative type: THEMATIC

   Please provide details to generate this Motion Playbook:

   1. What's the angle (theme / milestone / account / competitor)?
   2. Which personas / segments from the Motion ICP matrix does this lean into?
   3. Any supporting context, proof, or competitive framing?
   4. Any source materials? (URLs or text to inform generation)
   ```

5. **Call `create_motion_playbook`:**
   ```
   create_motion_playbook({
     motionOId: "mo_abc123",
     narrativeType: "THEMATIC",
     name: "Q1 Outbound — Cost Pressure",
     instructions: "<detailed instructions from user input>",
     keyContext: "<any additional context>",
     sources: [{ type: "url", content: "https://..." }]
   })
   ```

6. **Report success:**
   ```
   Created Custom Motion Playbook: Q1 Outbound — Cost Pressure
   oId: mp_new123
   Under Motion: Enterprise Outbound — Platform (mo_abc123)
   Narrative type: THEMATIC

   The Motion Playbook has been generated and saved.
   Use /octave:library show mp_new123 to view the full details.
   ```

## Create — Other Entities

1. **Gather basic info:**
   ```
   Creating new persona: "VP of Product"

   Please provide details to generate this persona:

   1. What industry or company type? (e.g., B2B SaaS, Enterprise Tech)
   2. What are their main responsibilities?
   3. Any specific pain points or priorities to focus on?
   4. Any source materials? (URLs or text to inform generation)
   ```

2. **Confirm and create:**
   ```
   I'll create a VP of Product persona with:
   - Focus: B2B SaaS companies
   - Key responsibilities: Product strategy, roadmap, GTM alignment
   - Pain points: Prioritization, cross-functional alignment, metrics

   Proceed? (yes/no)
   ```

3. **Call `create_entity`:**
   ```
   create_entity({
     entityType: "persona",
     name: "VP of Product",
     instructions: "<detailed instructions from user input>",
     keyContext: "<any additional context>",
     sources: [{ type: "url", content: "https://..." }]
   })
   ```

4. **Report success:**
   ```
   Created persona: VP of Product
   oId: pe_new123

   The persona has been generated and saved to your library.
   Use /octave:library show pe_new123 to view the full details.
   ```

## Update — Interactive Flow

1. **Fetch current entity:**
   ```
   Fetching: CTO - Enterprise Tech (pe_abc123)
   ```

2. **Show current state and ask for changes:**
   ```
   Current Persona: CTO - Enterprise Tech

   Key sections:
   - Pain Points: [list current]
   - Objectives: [list current]
   - Responsibilities: [list current]

   What would you like to update?
   (Describe the changes in natural language)
   ```

3. **Confirm changes:**
   ```
   I'll update the CTO persona with:
   - Add AI/ML adoption as a key objective
   - Include "evaluating AI tools" in responsibilities
   - Add "AI readiness" to pain points

   Proceed? (yes/no)
   ```

4. **Apply the update:**

   **For Motion Playbooks** (oId starts with `mp_`), use `update_motion_playbook`:
   ```
   update_motion_playbook({
     motionPlaybookOId: "mp_xyz789",
     instructions: "Sharpen the Strategic narrative for the [persona] × [segment] cell to address security concerns...",
     keyContext: "<any additional context>"
   })
   ```

   **For other library entities**, use `update_entity`:
   ```
   update_entity({
     entityType: "persona",
     oId: "pe_abc123",
     instructions: "Add AI/ML adoption as a key objective...",
     keyContext: "<any additional context>"
   })
   ```

5. **Report success:**
   ```
   Updated persona: CTO - Enterprise Tech

   Changes applied:
   - Added AI/ML adoption objective
   - Updated responsibilities
   - Added AI readiness pain point

   Use /octave:library show pe_abc123 to see the updated version.
   ```
