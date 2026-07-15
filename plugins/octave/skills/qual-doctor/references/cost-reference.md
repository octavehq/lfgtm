# Cost Reference

Credits per qualification run = sum of active components. For saved agents, read each component's state from the agent config; for raw tools, only the base applies unless the user has enabled extras.

| Component | Credits | How to check (saved agent config) |
|-----------|---------|-----------------------------------|
| Base (includes product/offering) | 1 | Always included |
| + Segment section | +1 | `entities.segment.strategy === "BEST_MATCH"` |
| + Persona section | +1 | `entities.persona.strategy === "BEST_MATCH"` |
| + Motion section | +1 | `entities.motion.strategy === "BEST_MATCH"` |
| + High effort mode | +4 | `tools.highEffortMode.enabled === true` |
| + Deep research | +8 | `tools.parallelWebSearch.enabled === true` |
| + CRM activity | +10 | `tools.crmActivity.enabled === true` |
| + Custom task | +5 | `tools.customTask.enabled === true` |

`update_entity` is free (no credit cost).

**Example**: Agent with product + segment active, no tools = 2 credits/run. 7 cases × 2 rounds = 28 credits.

Always calculate and show exact cost before executing test runs.
