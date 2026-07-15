# One-Pager Testing Protocol

How to improve this skill through real output. Two phases: tear one apart, then verify changes generalize.

This is a **skill development** protocol — it improves the skill definition, principles, and templates. It's separate from the [review protocol](../../shared/protocol.md), which is a post-generation QA pass on individual outputs.

---

## Phase 1: Deep Iteration

Pick one real target. Generate a full one-pager. Then tear it apart with the user.

### Setup

1. **Choose a target that exercises the skill.** Real company, real person, real product. Ideally one with a brand kit or where brand fidelity matters — that stress-tests the visual pipeline too.
2. **Brand kit first.** If the one-pager should be branded, run `/octave:get-brand-components <domain>` to completion *before* generating. Verify the font and logo are correct. Generating with wrong brand tokens (wrong font family, placeholder logo) wastes iteration cycles on problems that aren't the skill's fault.
3. **Generate from the skill.** Run `/octave:one-pager` end-to-end. Don't hand-build the output — the point is to test what the skill actually produces.

### Iteration loop

```
OPEN in browser
 → USER reacts (what's wrong, what's off, what they don't like)
 → FIX the output HTML directly (fast, visible)
 → OPEN again for next reaction
 → REPEAT until the user is satisfied with this output
```

**During iteration, track every fix in two categories:**

| Category | Example | Where it goes |
|---|---|---|
| **Principle violation** | Text wall in a `<p>`, orphan word, cheeky label | `shared/` files |
| **Template/skill gap** | Section template missing a pattern, wrong default label, missing brand-kit step | `skills/one-pager/` files |

### After iteration: push upstream

For every fix applied to the output:

1. **Does a principle already cover this?** If yes, the skill failed to follow it — check why (missing reference in SKILL.md? unclear wording in the principle?).
2. **Is this a new principle?** If no existing rule covers it, add one to the appropriate file (editorial, information, presentation, or format).
3. **Does the template need updating?** If the fix changes section structure, labels, or HTML patterns, update `document-sections.md` and `html-architecture.md`.
4. **Does SKILL.md need updating?** If the fix changes the generation flow, content density rules, or style guidance, update the skill definition.
5. **Add to the regression checklist.** Every issue found goes on the [regression checklist](regression-checklist.md) so it's verified in Phase 2.

---

## Phase 2: Cross-Target Verification

Generate 2-3 more one-pagers for different targets. The goal is to verify that Phase 1 changes generalize — they fix the problem without introducing new ones, and they work across different brands, industries, and occasions.

### Target selection

Pick targets that vary on the dimensions that matter:

| Dimension | Why it matters | Example variation |
|---|---|---|
| **Brand personality** | A dark-navy brand vs a light-minimal brand stress-tests color/contrast rules | Crexi (dark hero) vs a healthcare SaaS (light, airy) |
| **Industry/vertical** | Different verticals surface different jargon and proof-point patterns | CRE vs fintech vs developer tools |
| **Occasion** | Demo follow-up vs intro vs renewal changes tone and section emphasis | `--for demo-followup` vs `--for intro` |
| **Data richness** | A target with full Octave intel vs one with sparse data tests fallback paths | Well-known account vs cold prospect |

You don't need to iterate deeply on each. The bar is: **does the first-draft output pass the regression checklist?**

### Verification process

For each test target:

1. Generate from the skill (don't hand-edit first).
2. Open in browser.
3. Run through every item on the [regression checklist](regression-checklist.md).
4. Note any failures — these are either:
   - **Regressions** from Phase 1 changes (the fix broke something else)
   - **New issues** the first target didn't surface (add to the checklist)
5. Fix and push upstream if needed.

### Done when

- The regression checklist passes on at least 2 targets across different brand personalities.
- No Phase 1 fix has introduced a new problem.
- The user has seen the outputs and signed off.

---

## When to run this protocol

- **After any significant skill change** (new section structure, new default labels, new style logic).
- **Periodically** as a health check — pick a random target and generate. If the output looks off, start Phase 1.
- **When a user reports an issue** with a generated one-pager — reproduce it, fix it, run Phase 2 to verify.
