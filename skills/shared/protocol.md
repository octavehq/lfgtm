# Octave Review Protocol

Standard review loop for all Octave-generated content. Any content-generating skill can invoke this protocol at its review step.

Use [output readiness](output-readiness.md) for the requested audience and purpose. Text, native-generation, saved-agent, and HTML routes share factual and commercial checks. HTML adds actual visual inspection. Clearly labeled drafts and previews may be shown while inputs or checks are pending; do not call an unchecked artifact ready.

Read [host runtime](host-runtime.md) before choosing tools or delegation. Preserve inherited scope and approvals. Use the same content schema for generation and review.

## Step 1: Preflight (Always Runs)

Before spawning reviewers, before anything else, run a deterministic sweep of the rendered output. This is not a re-read; it's a literal scan for a fixed set of mechanical defects that generation drifts into constantly. Fix hard failures; review style advisories in context. Missing dependencies mean NOT RUN, not PASS.

Check for:

- **Authored prose.** Review decoded reader-facing text. Apply customer voice and necessary domain language; preserve exact quotes and names. Punctuation/style preferences are advisories, not grounds to corrupt evidence.
- **Broken or failed images and logos.** No `<img>` that fails to load or embed, no broken-image box. Prefer a brand-kit SVG or a clean wordmark. If a logo can't be sourced cleanly, fall back to text: never ship a broken mark.
- **Links.** Preserve intended destinations and targets. New-tab links carry `rel="noopener noreferrer"`; same-tab and in-page navigation remain valid.
- **Scrollbars.** Check usability and brand fit; scrollbar styling is an advisory preference.
- **Audience and completeness.** Keep private notes and inaccessible internal links out of external artifacts. Allow intentional draft/planning fields; accidental missing required seller inputs prevent final readiness.

For HTML, run the shared source lint: policy-aware placeholders, resource locations, internal links/IDs and public share metadata, plus authored-wording advisories. It does not measure density, factual truth or rendering. Plain text receives the applicable factual/editorial checks without pretending it is HTML.

```bash
bash <skill-dir>/../shared/scripts/lint.sh <path-to-file> --policy <policy.json>
```

Fix hard failures; resolve advisories with the actual audience, terminology and source fidelity in mind. If a skill ships additional source checks, run those where applicable.

### Step 1b: Render Gate (any output with a fixed-viewport or themed surface)

The lint reads source. Some defects only exist once the page is painted, and four of them are deterministic enough that a browser can decide them without a human eye: whether the intended fonts actually loaded, whether text has contrast against the background it landed on, whether text stayed inside its content box, and whether it slid under fixed chrome.

The invocation depends only on the output's shape, and the format doc for that shape gives it verbatim:

| Output shape | Panes | Typical chrome | Format doc |
|---|---|---|---|
| Swipe magazine | `.spread` | `#nav,.folio` | [magazine.md](formats/magazine.md) |
| Slide deck | `.slide` | `.deck-nav,.pager,.slide-number` | [slide-deck.md](formats/slide-deck.md) |
| Scrolling document | none | `nav,.toc,.sticky-nav` | [html-document.md](formats/html-document.md) |
| Microsite | none | `nav,.sticky-nav,.cta-bar` | [microsite.md](formats/microsite.md) |
| One-pager | none | none | [one-pager.md](formats/one-pager.md) |

```bash
node <skill-dir>/../shared/scripts/render-gate.js <path-to-file> \
  --panes ".spread"      `# fixed-viewport surfaces; omit for scrolling documents` \
  --chrome "#nav,.folio" `# fixed or absolutely-positioned page furniture` \
  --viewports 1600x900,1680x1050,2560x1080,1180x820
```

Panes only affect the content-box and chrome-collision checks. **Contrast and font loading run either way**, and on a scrolling document those are the two that pay: a light card nested in a dark band inherits the band's text colour and paints near-white on near-white, and a brand font that was declared but never delivered falls back to a system face silently.

Two rules make this worth the run:

- **Run it before you open a screenshot.** Screenshot review is the most expensive step in this protocol. Spend it on judgment — hierarchy, pacing, whether a composition feels finished — not on hunting defects a script decides in one pass.
- **Never substitute `scrollHeight - clientHeight` for the overflow check.** Every fixed-viewport pane sets `overflow: hidden`, which makes that difference 0 while content is visibly cut off. A gate built on it reports a confident pass over broken output. The script measures element rectangles against the content box instead.

If playwright is unavailable the script exits 2 and the gate did not run: say so in the scorecard rather than implying the checks passed.

## Step 2: Review an immutable version

Use the host's supported delegation with the packaged reviewer instructions, or run the same checks sequentially when delegation is unavailable. The Claude Task examples below describe roles, not a mandatory portable API. Both reviewers inspect the same immutable version and return findings. One author applies edits and reruns affected checks; reviewers never edit the artifact concurrently.

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
           Return findings and a scorecard without editing; the author applies fixes and rechecks."
```

If the skill has its own editorial blueprint, pass it as an additional file. The shared rules are universal; the skill-specific rules add context.

### Groundedness & Verification (the orchestrator's own check)

The reviewer subagents own language and visual quality; **content accuracy is the orchestrator's job** (yours), so run this check yourself as part of the gate, before delivery. It is the highest-stakes dimension in the whole pipeline. A confident model fabricates silently, and a fabrication that ships reads exactly like a fact until someone downstream gets burned by it. Treat every claim as guilty until traced to a source.

- **Every metric, quote, customer name, and capability traces to real source material** (the Octave MCP data gathered for this asset, or the brand kit's real assets). Nothing invented, nothing rounded up from a hunch. Flag anything that can't be traced.
- **Named people and titles need attributable evidence.** CRM records and operator-supplied names are valid inputs. Enrichment is useful for missing identities or material conflicts, not mandatory re-verification of every supplied name. Distinguish identity from demonstrated buying role.
- **Preserve source meaning.** Use [evidence and inputs](evidence-and-inputs.md). Keep uncertainty, scope, counterevidence, quote fidelity, and buyer/seller/strategy attribution through final edits. Recheck load-bearing claims after changes.
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
           Return findings without editing; the author applies fixes and re-renders the final version."
```

**Format mapping:** Use the format file that matches the skill's output type:
- `html-document.md`: abm, battlecard-doc, champion-deal-room, deal-coach, meeting-prep, positioning, proposal, research (HTML mode), win-loss-report
- `slide-deck.md`: deck, train
- `magazine.md`: digest (magazine mode), any skill producing a swipe-magazine leave-behind
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

## Step 4: Apply findings and recheck

Bound optional polishing to three cycles. The cap does not clear fabricated claims, wrong-audience content, broken primary actions, or missing required sections. Fix the concrete blocker, collect missing input, or accurately deliver an agreed draft with its limitation. One author applies edits, then reruns affected checks on the final file/version.

## Step 5: Output Combined Scorecard

Present the combined scorecard to the user. This is proof the pipeline ran.

```
REVIEW COMPLETE
=========================
Preflight (Mechanical, always runs):
  Em dashes:      [PASS / FAIL / NOT RUN / N/A]
  Images/logos:   [PASS / FAIL / NOT RUN / N/A]
  Links:          [PASS / FAIL / NOT RUN / N/A]
  Scrollbars:     [PASS / FAIL / NOT RUN / N/A]
  Leaked internals: [PASS / FAIL / NOT RUN / N/A]

Editorial (Language + Information):
  Mechanical:     [PASS / FAIL / NOT RUN / N/A]
  Structural:     [PASS / FAIL / NOT RUN / N/A]
  Quality:        [PASS / FAIL / NOT RUN / N/A]
  Information:    [PASS / FAIL / NOT RUN / N/A]

Groundedness (orchestrator's own check):
  Claims/people:  [N fixes / PASS / N unverified, flagged]

Presentation (Visual Design + Render Inspection):
  Visual Rules:   [PASS / FAIL / NOT RUN / N/A]
  Format Rules:   [PASS / FAIL / NOT RUN / N/A]
  Design System:  [PASS / FAIL / NOT RUN / N/A]
  Structure:      [PASS / FAIL / NOT RUN / N/A]
  Rendered Check: [PASS / FAIL / NOT RUN / N/A]

Total fixes: [N]
Cycles: [1-3]
Status: [ready for the requested purpose / draft with stated limitations]

[Fix log from both reviewers]
```

---

## Notes for Skill Authors

- The shared procedure applies across hosts and formats. Use [output readiness](output-readiness.md); final factual/commercial checks apply even to text and saved-agent output.
- Reviewers return findings against an immutable file. One author edits and repeats affected checks. Report actual tested viewports, interactions and exported page/slide counts.
- Missing browser/exporter means NOT RUN. A geometric/contrast pass is not an accessibility certificate.
- Use the requested customer language and brand. Preserve exact quotes, names and necessary technical terms; generic style preferences are advisory.
- Social metadata and remote assets follow the declared audience/deployment policy in [social metadata](social-meta.md). Public sharing needs a verified image URL; internal drafts need not generate a public preview.
- Source notes and private account strategy stay outside external publish bundles. Publishing requires authorized scope and readback of the actual artifact/version/access.
