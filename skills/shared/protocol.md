# Octave Review Protocol

Standard review loop for all Octave-generated content. Any content-generating skill can invoke this protocol at its review step.

This protocol is a **MANDATORY GATE** for any shippable HTML deliverable. The artifact is NOT opened in the browser, delivered, or summarized until the pipeline has run and produced a scorecard. The principles (editorial, information, presentation, octave-value) are baked into generation; this gate is the verification pass that catches what slipped through. There is no opt-out: skills do not ask permission, and the reviewer pass is not skippable.

## How to Invoke

The gate runs automatically after generation. In interactive mode, say so at intake, before generation starts, so it isn't a surprise:

```
I'll generate this and run the review gate before handing it back.
```

The pipeline has two parts: a deterministic **preflight** (Step 1) and then the **reviewer pass** (Step 2 onward), two dedicated reviewer subagents in parallel. Do NOT open the file, present a summary, or tell the user it is ready until Step 5 has printed the combined scorecard.

---

## Step 1: Preflight (Always Runs)

Before spawning reviewers, before anything else, run a deterministic sweep of the rendered output. This is not a re-read; it's a literal scan for a fixed set of mechanical defects that generation drifts into constantly. Fix every hit in place. This step is not skippable.

Check for:

- **Em dashes.** Ban `—` and `&mdash;` from asset copy. Replace with a comma, colon, period, or two sentences. Sweep the actual rendered text, don't rely on memory of what you wrote.
- **Broken or failed images and logos.** No `<img>` that fails to load or embed, no broken-image box. Prefer a brand-kit SVG or a clean wordmark. If a logo can't be sourced cleanly, fall back to text: never ship a broken mark.
- **Links.** Every external `<a>` carries `target="_blank" rel="noopener noreferrer"`. In-page `#` anchors are exempt.
- **Scrollbars.** Themed, never the bare default OS scrollbar on a styled surface.
- **Leaked internals and placeholders.** No tool or function names, version or stream IDs, or unfilled `[…]` brackets anywhere in the rendered output.

Then run any skill-specific lint script. These are deterministic checks (banned words, text density) that don't need LLM judgment and cost nothing.

```bash
bash <skill-dir>/scripts/lint.sh <path-to-file>
```

Fix every violation the lint surfaces before proceeding. If no lint script exists for this skill, skip straight to Step 2.

## Step 2: Spawn Reviewers (Parallel)

Use the Task tool to spawn **two reviewers in parallel** (both calls in a single message).

**Edit safety:** The two reviewers edit the same file concurrently. They avoid conflicts by staying in their lanes:
- The editorial reviewer only edits **reader-facing text content** (headlines, body copy, implications, labels).
- The presentation reviewer only edits **CSS, HTML structure, attributes, and layout**.
- Neither rewrites content in the other's domain. If they spot an issue outside their scope, they note it in the scorecard.
- The cycle mechanism (Step 4) catches any residual conflicts: if one reviewer's fix introduces a violation in the other's domain, the next cycle picks it up.

### Editorial Reviewer

The editorial reviewer owns **language quality** and **information quality**. (Content accuracy is the orchestrator's own check: see Groundedness & Verification below.)

```
Task tool:
  subagent_type: "octave-editorial-reviewer"
  prompt: "Review the file at [FILE PATH].
           Read these principle docs and run each Review Checklist:
           1. [plugin-root]/skills/shared/editorial-rules.md (language quality)
           2. [plugin-root]/skills/shared/information-principles.md (information structure)
           [If skill has its own editorial blueprint or regression-checklist: 3. that file]
           Fix violations inline. Return scorecard."
```

If the skill has its own editorial blueprint, pass it as an additional file. The shared rules are universal; the skill-specific rules add context.

### Groundedness & Verification (the orchestrator's own check)

The reviewer subagents own language and visual quality; **content accuracy is the orchestrator's job** (yours), so run this check yourself as part of the gate, before delivery. It is the highest-stakes dimension in the whole pipeline. A confident model fabricates silently, and a fabrication that ships reads exactly like a fact until someone downstream gets burned by it. Treat every claim as guilty until traced to a source.

- **Every metric, quote, customer name, and capability traces to real source material** (the Octave MCP data gathered for this asset, or the brand kit's real assets). Nothing invented, nothing rounded up from a hunch. Flag anything that can't be traced.
- **Named people and titles must be VERIFIED, not assumed.** Trace every named person to a real result via `resolve_profile_from_email`, `enrich_person`, or `find_person`: don't carry a name forward just because it appeared in a prompt or an earlier draft. A fabricated contact (a hallucinated seller, a guessed buyer, a wrong title) is the single most damaging defect an asset can ship. If a person can't be confirmed, flag them as unverified in the scorecard rather than stating them as fact in the asset.
- **News and "recently..." claims carry a date and a source link.** Anything time-sensitive needs to trace back to `deep_web_research` or `scrape_website` output, not to model memory.
- **Internal entity deep-links are context-dependent, not universally wrong.** A link like `app.octavehq.com/entity/{oId}` is correct in internal or seller-facing assets (briefs, call prep, meeting prep). In customer-facing assets (deck, one-pager, microsite, proposal), that same link is a DEFECT: flag it as internal-tooling leakage and strip it.
- **No hallucinated proof points, fake logos, paraphrases passed off as verbatim quotes, or capabilities not present in the product data.** If a quote can't be matched to source text verbatim, it's a paraphrase: label it as one or cut it.

### Presentation Reviewer

The presentation reviewer owns **visual design**: universal principles, format-specific rules, and skill-specific blueprints. Critically, this reviewer doesn't just read CSS and markup: it **renders the real output and looks at the pixels**. Many of the worst defects (overflow and clipping, white-on-white text, a corrupted SVG logo path, an image that silently fails to embed) are invisible from source and only show up once the asset is actually painted.

```
Task tool:
  subagent_type: "octave-presentation-reviewer"
  prompt: "Review the file at [FILE PATH].
           Read these principle docs and run each Review Checklist:
           1. [plugin-root]/skills/shared/presentation-principles.md (universal visual rules)
           2. [plugin-root]/skills/shared/formats/[format].md (format-specific visual rules)
           3. [skill-dir]/references/<skill CSS/scaffold ref>
           4. [skill-dir]/references/<skill section/template ref>
           Render the output and inspect it visually per the Render & Inspect steps below.
           Fix violations inline. Re-render to verify each fix. Return scorecard."
```

**Format mapping:** Use the format file that matches the skill's output type:
- `html-document.md`: abm, battlecard-doc, champion-deal-room, deal-coach, meeting-prep, positioning, proposal, research (HTML mode), train, win-loss-report
- `slide-deck.md`: deck, train (deck mode)
- `one-pager.md`: one-pager
- `microsite.md`: microsite

Adjust the skill-specific blueprint paths for the skill being reviewed. Some skills may have more or fewer blueprints, so pass all that are relevant.

#### Render & Inspect

Read the actual pixels, not just the source. This step is invoked from inside a skill (`skills/<skill>/`), so paths below are skill-relative.

- **Documents** (one-pager, microsite, brief, proposal, battlecard-doc, etc.): render to PNG with
  ```bash
  ../get-brand-components/scripts/render.py --file <out.html> --out <png>
  ```
  then inspect the image for overflow, alignment, scaling artifacts, and logo integrity.
- **Decks:** measure each slide's content height before screenshotting: set the slide to `position: static; height: auto` and read `.inner scrollHeight`. Anything over 1080 is clipped and needs a fix (shrink content, split the slide, or tighten spacing). Drive headless capture with a virtual-time budget (e.g., Chrome `--virtual-time-budget=2500`) so reveal animations don't get caught half-faded mid-transition.
- **On every render:** check for overflow/clipping, misalignment, incorrect scaling, and broken or corrupted logo/image assets. Fix the source, re-render, and re-verify before moving on: a fix isn't done until the re-render confirms it.

## Step 3: Read Scorecards

Both reviewers return scorecards. Read both.

## Step 4: Loop Decision

| Cycle | 0 fixes | 1-2 fixes | 3+ fixes |
|---|---|---|---|
| **Cycle 1** | CLEAN → Step 5 | Apply, loop | Apply, loop |
| **Cycle 2** | CLEAN → Step 5 | Apply, STOP (diminishing returns) | Apply, loop |
| **Cycle 3 (hard cap)** | CLEAN → Step 5 | Apply, STOP | Apply, STOP |

**Max 3 cycles.** Cycles continue until clean or capped. The threshold at cycle 2 is whether reviewers are still finding multiple issues: if 3+, the file needs another pass. After cycle 3, deliver with any remaining issues noted in the scorecard.

## Step 5: Output Combined Scorecard

Present the combined scorecard to the user. This is proof the pipeline ran.

```
REVIEW COMPLETE
=========================
Preflight (Mechanical, always runs):
  Em dashes:      [N fixes / PASS]
  Images/logos:   [N fixes / PASS]
  Links:          [N fixes / PASS]
  Scrollbars:     [N fixes / PASS]
  Leaked internals: [N fixes / PASS]

Editorial (Language + Information):
  Mechanical:     [N fixes / PASS]
  Structural:     [N fixes / PASS]
  Quality:        [N fixes / PASS]
  Information:    [N fixes / PASS]

Groundedness (orchestrator's own check):
  Claims/people:  [N fixes / PASS / N unverified, flagged]

Presentation (Visual Design + Render Inspection):
  Visual Rules:   [N fixes / PASS]
  Format Rules:   [N fixes / PASS]
  Design System:  [N fixes / PASS]
  Structure:      [N fixes / PASS]
  Rendered Check: [N fixes / PASS]

Total fixes: [N]
Cycles: [1-3]
Status: [CLEAN / N remaining issues]

[Fix log from both reviewers]
```

---

## Notes for Skill Authors

- **The protocol is the same for every skill.** Don't customize the loop logic. Customize what the reviewers check by writing skill-specific blueprints with Review Checklist sections.
- **The review is a mandatory gate.** Skills don't ask permission: they announce the review at intake (interactive mode) and run it automatically after generation. There is no opt-out. The artifact is not opened, summarized, or delivered until the combined scorecard (Step 5) has printed.
- **The preflight is non-negotiable.** Em dashes, broken images, unsafe external links, unthemed scrollbars, and leaked internals are cheap to catch and never worth shipping.
- **Four review dimensions, two reviewers plus the orchestrator.** The editorial reviewer handles language (editorial-rules.md) and information structure (information-principles.md). The presentation reviewer handles visual design (presentation-principles.md + format file + skill blueprints) and actually renders the output to check it, rather than inferring from source alone. Groundedness & verification (fabrication, unverified people, internal-link leakage) is the orchestrator's own check, run as part of the gate. Language, information, and groundedness don't vary by format. Visual design does.
- **Groundedness is the highest-stakes dimension.** A hallucinated contact, an invented metric, or a paraphrase dressed up as a verbatim quote does more damage than any layout bug. When in doubt, flag a claim as unverified in the scorecard rather than letting it ship as fact.
- **Format files are shared across skills.** If your skill produces an HTML document, it uses `formats/html-document.md`. If it produces a deck, it uses `formats/slide-deck.md`. Don't duplicate format rules in skill-specific blueprints.
- **Skill-specific blueprints add the most specific layer.** They handle CSS component systems, HTML scaffolds, and structural requirements unique to your skill. These sit on top of the universal + format layers.
- **The lint script is optional but recommended.** Deterministic checks beyond the preflight (banned words, text density) are cheaper and faster as a shell script than as LLM inference. If your skill generates HTML, write a lint script.
- **Principles are baked into generation.** The review pass catches what slipped through. It's not the only quality gate: it's the verification gate.
