# Health Score Calculation

```
Base Score: 100

Deductions:
- Critical issue: -15 points each (max -45)
- Warning: -5 points each (max -30)
- Language & Voice issue: -3 points each (max -15)
- Qualifying Question issue: -3 points each (max -15)
- Info: -1 point each (max -10)
- No Motions when offering exists: -10
- Agents still on legacy playbooks when Motions cover same offering: -3 each (max -9)

Bonuses:
- All entity types have content: +5
- No stale content (>90 days): +5
- Clean language/voice (no issues found): +5
- Qualifying questions use varied weights: +5
- All offerings have Motions: +5
- Learning Loop enabled: +3
- No legacy playbook agent references remaining: +3

Minimum score: 0
Maximum score: 100
```

**Note:** Design Review observations do NOT affect the health score. They are strategic prompts, not errors.

**Score Interpretation:**
- 90-100: Excellent - Library is well-maintained
- 70-89: Good - Minor issues to address
- 50-69: Fair - Several gaps need attention
- Below 50: Needs Work - Significant gaps affecting effectiveness
