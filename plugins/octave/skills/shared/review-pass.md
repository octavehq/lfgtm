# Review pass (runs by default)

The canonical post-generation QA flow for every Octave skill that produces an HTML asset (deck, one-pager, proposal, microsite, brief, meeting-prep, positioning, battlecard doc, wins-losses report, etc.). Consuming skills link here instead of restating it.

After generating, **run the review pass by default** — don't wait to be asked. In interactive mode, tell the user at intake that you'll review before finishing (recommended) and that they can opt out with `--skip-review` or "skip review". Follow [asset-review.md](asset-review.md):

- The always-on **preflight** — em dashes, broken images/logos, link `target`, themed scrollbars, leaked internals.
- The **visual pass** — render/screenshot, inspect the pixels across the five dimensions (groundedness/verification matters most), report a short located scorecard, fix, re-verify.

The visual pass defaults off only in a fast research run (`--research fast`, in skills that support the flag); the preflight always runs.

When generating (before the review), follow the output rules in [presentation-principles.md](presentation-principles.md) — the generation-time companion to the review pass: label every value, no tool names in the output, confirmed vs hypothesized, lean and deal-specific.
