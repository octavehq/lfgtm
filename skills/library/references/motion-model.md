# Motion / Motion Playbook / Motion ICP — Model and Update Flows

The Motion era replaces the standalone playbook model. A Motion is the top-level container; under it live one or more Motion Playbooks (a Default Motion Playbook is auto-generated covering the persona × segment matrix, plus any Custom Motion Playbooks). Each Motion Playbook is composed of **Motion ICP cells** — one narrative per persona × segment intersection.

## Structure

- **Motion** — top-level container, tied to an offering (product/service) and a motion type (Outbound, PLG, Renewal, etc.)
- **Motion Playbook** — Default (auto-generated) or Custom (`THEMATIC` / `MILESTONE` / `ACCOUNT` / `COMPETITIVE`)
- **Motion ICP cell** — per persona × segment narrative inside a Motion Playbook: Target ICP overview, Operating landscape, Strategic narrative, Pains and consequences, Benefits and impacts, Methodology, References

## Decision Logic

| User Request | Tools to Use |
|--------------|--------------|
| "Show me all Motions" | `list_motions` |
| "List the playbooks under the Enterprise Outbound motion" | `list_motion_playbooks({ motionOId })` |
| "Show me the full Default Motion Playbook for that Motion" | `get_motion_playbook` |
| "What's in the CTO × Mid-Market cell?" | `find_motion_icp({ motionIcpOId, includeLearnings: true })` |
| "Sharpen the Strategic narrative for the CFO × Enterprise cell" | `update_motion_playbook` |
| "Add a Custom Motion Playbook for displacing [competitor]" | `create_motion_playbook` with `narrativeType: "COMPETITIVE"` |
| "Rework the whole Default Motion Playbook" | `update_motion_playbook` on the Default Motion Playbook |

## Reading Flow

1. `list_motions()` — find the relevant Motion for the offering / motion type
2. `list_motion_playbooks({ motionOId })` — see Default + any Custom playbooks under it
3. `list_motion_icps({ motionOId })` — see the persona × segment matrix
4. `find_motion_icp({ motionIcpOId, includeLearnings: true })` — full narrative for a cell, plus Learning Loop learnings

## Editing Flow

Narrative edits (Strategic narrative, Pains and consequences, Benefits and impacts, Methodology, etc.) are all done through `update_motion_playbook`. The tool re-generates affected narrative sections based on your instructions.

```
update_motion_playbook({
  motionPlaybookOId: "mp_xyz789",
  instructions: "Sharpen Strategic narrative and Benefits and impacts for the CFO × Enterprise cell. Emphasize cost-savings framing over efficiency framing. Keep Pains and consequences unchanged.",
  keyContext: "<any supporting context>"
})
```

`update_motion_playbook` edits the narrative sections (Target ICP overview, Operating landscape, Strategic narrative, Pains and consequences, Benefits and impacts, Methodology, References) inside the Motion Playbook's Motion ICP cells.

## Example — Reframing a Cell's Value Narrative

```
User: "Make the CFO cell focus more on cost savings"

1. Find the Motion: list_motions()
2. List the Motion's playbooks: list_motion_playbooks({ motionOId: "mo_abc123" })
3. Confirm the cell exists: list_motion_icps({ motionOId: "mo_abc123" })  # check for CFO × <segment> cells
4. Update: update_motion_playbook({
     motionPlaybookOId: "mp_xyz789",
     instructions: "Reframe the CFO × Enterprise cell's Strategic narrative and Benefits and impacts to lead with cost savings rather than efficiency. Leave other cells unchanged."
   })
```

## Example — Adding a Custom Motion Playbook for a New Angle

```
User: "Add a competitive displacement Motion Playbook for [Competitor] under our Enterprise Outbound motion"

1. Confirm the Motion: list_motions()
2. Create: create_motion_playbook({
     motionOId: "mo_abc123",
     narrativeType: "COMPETITIVE",
     name: "Displace [Competitor] — Enterprise",
     instructions: "Generate a competitive displacement Motion Playbook targeting current [Competitor] customers. Cells should focus on switching pain, ROI of migration, and proof from prior displacements."
   })
```
