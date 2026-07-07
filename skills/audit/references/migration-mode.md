# MIGRATION MODE — Legacy Playbooks → Motions

When the user selects migration (or uses `--migrate`), the audit reads the full current state — legacy playbooks and Motions alike — identifies the gap, and works interactively to translate the old setup into the new world.

**Auto-detect hint:** If the library has legacy playbooks but zero Motions, default-suggest migration.

Migration has two parts:
1. **Preserve and migrate your playbooks** — map legacy playbooks to the Motions world, carry over nuance
2. **Re-wire your agents** — update agent configurations from old playbook references to Motion references

## Step 1-M: Gather State

Add to the standard library fetch:
```
- list_motions() — all Motions in workspace
- For each Motion: list_motion_icps({ motionOId }) — Motion ICP cell state
- list_all_entities({ entityType: "playbook" }) — all standalone playbooks
- get_playbook({ oId }) for each standalone playbook — linked personas, segments, value props, type
- list_agents() — all saved agents with their configurations
```

## Step 2-M: Read & Categorize Old Playbooks

Categorize each standalone playbook against the Motion Playbook narrative types:
- **Sector-based** (linked to specific segments) → covered by Default Motion Playbook (segments are columns)
- **Persona-based** (linked to specific personas) → covered by Default Motion Playbook (personas are rows)
- **Sector × Persona combos** → covered by Default Motion Playbook (specific Motion ICP cells in the matrix)
- **Competitive** → Custom Motion Playbook with narrative type `COMPETITIVE`
- **Milestone / trigger-based** → Custom Motion Playbook with narrative type `MILESTONE`
- **Account-specific** → Custom Motion Playbook with narrative type `ACCOUNT`
- **Solution / general theme** → either covered by Default if the angle is broad enough, or a Custom Motion Playbook with narrative type `THEMATIC`

## Step 3-M: Present Current State

```
Here's your setup:

OLD WORLD (Standalone Playbooks):
  [X] playbooks:
  - [X] sector-based (targeting specific segments)
  - [X] persona-based (targeting specific personas)
  - [X] sector × persona combos
  - [X] competitive (vs [competitor names])
  - [X] milestone ([trigger names])
  - [X] solution/general

NEW WORLD (Motions):
  [What they've already created, or "No Motions yet"]

THE GAP:
  [What's covered only by legacy playbooks, what's already in Motions]
```

## Step 4-M: Playbook Migration — Default Motion Playbook

The bulk of migration. Most legacy playbooks (sector, persona, combos) are absorbed by the Default Motion Playbook.

Key coaching points:
- "Most of your playbooks are sector or persona combinations. All of that becomes one Default Motion Playbook per Motion. Every persona × segment intersection becomes a Motion ICP cell with its own tailored narrative."
- "The critical thing is making sure any nuance from your legacy playbooks — especially ones you've manually edited or refined — makes it into the Motion ICP narratives."
- **For each legacy playbook that maps to default:** compare its value props and key messaging to the corresponding Motion ICP narrative (use `find_motion_icp({ motionIcpOId, includeLearnings: true })`). Each cell has structured sections — Target ICP overview, Operating landscape, Strategic narrative, Pains and consequences, Benefits and impacts, Methodology, References. Map old playbook value props to the right section. An old value prop about compliance probably belongs in Strategic narrative or Benefits and impacts. Surface anything the old playbook captured that the auto-generated narrative missed. Offer to edit the specific cell via `update_motion_playbook` to incorporate it.
- "If your 'Enterprise Sales' playbook had a specific value prop about compliance that your VP Sales × Enterprise cell doesn't mention — check the Strategic narrative and Benefits and impacts sections. That's where positioning and outcome claims live."
- **Auto-update caveat:** if Learning Loop is enabled with auto-update ON, manually edited cells may be refreshed in the next learning cycle. If the user is pulling critical nuance into cells, recommend turning auto-update OFF for those specific cells so the refinements persist. Otherwise the system may overwrite their work.

## Step 5-M: Playbook Migration — Custom Motion Playbooks

For playbooks with specific angles that don't collapse into the default:

**Competitive playbooks → Custom Motion Playbook (narrative type `COMPETITIVE`):**
- Walk through each: which grid coordinates should this target? Not all of them — where do you actually encounter this competitor?
- What's the displacement angle?
- Use `create_motion_playbook({ motionOId, narrativeType: "COMPETITIVE", ... })`

**Milestone playbooks → Custom Motion Playbook (narrative type `MILESTONE`):**
- What's the trigger event?
- Which segments/personas does this event actually change the conversation for?
- Use `create_motion_playbook({ motionOId, narrativeType: "MILESTONE", ... })`

**Account playbooks → Custom Motion Playbook (narrative type `ACCOUNT`):**
- Which named accounts?
- What grid slice?
- Use `create_motion_playbook({ motionOId, narrativeType: "ACCOUNT", ... })`

**Solution/general playbooks → evaluate:**
- Is this angle broad enough that the default covers it?
- Or is it a specific enough lens that it deserves a custom playbook with narrative type `THEMATIC`?

## Step 6-M: Agent Re-wiring

Pull all agents (`list_agents`) and analyze how they're configured:
- What playbooks are they referencing?
- What selection mode (Best Match / Best Of / Manual)?

**New agent config flow:** Agents configure in layers: offering (or auto-offering-select) → motion type (`NET_NEW`, `UPSELL`, `CROSS_SELL`, etc.) → that narrows to available Motions → if multiple Motion Playbooks exist, selection mode (auto / subset / fixed). The motion type selection is the new step — Net New, Upsell, Cross Sell agents are separated at the config level, not just by which playbooks they reference.

**Selection mode mapping (old → new):**
- Best Match → auto (agent picks the best Motion Playbook per target at runtime)
- Best Of → subset (you select which Motion Playbooks are eligible, agent picks among them)
- Manual → fixed (you link one specific Motion Playbook)

Map each to the Motions world:
- **Agents using sector/persona playbooks with Best Match** → set offering + motion type → Default Motion Playbook handles the rest. The matrix does the persona × segment matching automatically.
- **Agents using competitive/milestone playbooks** → set offering + motion type → narrow to the specific custom Motion Playbook (`COMPETITIVE` / `MILESTONE` / `ACCOUNT`) via fixed selection.
- **Agents using Best Of across mixed playbooks** → set offering + motion type → if multiple Motion Playbooks exist, use subset selection across the relevant ones.
- **Agents using Manual with a single playbook** → set offering + motion type → fixed selection on the corresponding Motion Playbook (or just the default).
- **Agents with no clear motion type distinction** → default to `NET_NEW` unless the agent is explicitly for expansion / upsell / cross-sell / renewal / displacement.

Present recommendations per agent:
```
AGENT RE-WIRING
===============

Agent: "Outbound SDR"
  Currently: Best Match across 6 playbooks (3 sector, 2 persona, 1 general)
  Recommendation: Offering → [Offering] / Motion Type → NET_NEW / Default Playbook
  Why: The default covers all of this automatically. Every prospect
  gets matched to the right persona × segment Motion ICP. The motion type
  ensures narratives are calibrated for net-new acquisition.

Agent: "Competitive Takeout"
  Currently: Manual → "vs [Competitor]" playbook
  Recommendation: Offering → [Offering] / Motion Type → NET_NEW / Fixed → Custom Motion Playbook (COMPETITIVE) "vs [Competitor]"
  Why: Same angle, same targeting, Motion-native. Motion type matters
  here — competitive displacement is usually a net-new play (or use
  DISPLACE_INCUMBENT if you're explicitly going after an incumbent).

Agent: "Expansion AE"
  Currently: Best Match across expansion playbooks
  Recommendation: Offering → [Offering] / Motion Type → UPSELL / Default Playbook
  Why: Upsell motion type generates fundamentally different narratives —
  different objections, different value framing, different buyer mindset.
  This wasn't possible before without building separate upsell playbooks.

Agent: "Enterprise AE Prep"
  Currently: Best Of → 3 enterprise playbooks
  Recommendation: Offering → [Offering] / Motion Type → NET_NEW / Default Playbook
  Why: The matrix already differentiates by persona within Enterprise segment.
  If you need themed angles too, use subset selection across relevant Motion Playbooks.
```

## Step 7-M: Coverage Gain Summary

After mapping, show what they gain:
```
COVERAGE SUMMARY
================

Old world: X playbooks covered ~Y persona × segment × angle combos
New world: Default Motion Playbook covers Z base combos (every intersection
           in the matrix) + custom Motion Playbooks for COMPETITIVE /
           MILESTONE / ACCOUNT / THEMATIC angles

Coverage gains:
- [X] Motion ICP cells that no legacy playbook covered (persona × segment
  combos that fell through the cracks)
- Structured methodology, pains/benefits, and references in every cell
- Learning Loop refinement over time (KEY_LANGUAGE, INDUSTRY_TREND,
  PAIN_POINT, VALUE_PROP, OBJECTION learnings accumulate per cell)

Nuance preserved:
- [X] value props / angles from legacy playbooks verified in Motion ICPs
- [X] custom Motion Playbooks carrying competitive/milestone/account angles
```

## Step 8-M: Interactive Build (--fix)

In fix mode, walk through interactively:
1. For each legacy playbook mapped to default: pull the Motion ICP via `find_motion_icp`, compare to playbook value props, offer to edit the cell via `update_motion_playbook` if nuance is missing
2. For each competitive/milestone/account angle: co-create the custom Motion Playbook via `create_motion_playbook` (targeting, narrative type, optional additions)
3. For each agent: walk through the re-wiring recommendation, confirm or adjust
