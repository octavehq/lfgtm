# Format: HTML Document

Long-form scrollable HTML documents with section-based structure. The most common Octave output format.

**Skills that produce this format:** research (HTML mode), positioning, meeting-prep, battlecard (HTML mode), win-loss (HTML mode), proposal

These principles supplement the universal visual rules in `presentation-principles.md` (one directory up). The universal principles are the floor; these add format-specific requirements.

## Principles

1. **Scroll-based reading flow.** The document reads top-to-bottom. Sections should have enough vertical breathing room that scrolling feels like turning pages, not wading through a wall.

2. **Sticky navigation for orientation.** Long documents need a nav bar that stays visible as the reader scrolls. Jump links to each major section. Hidden in print.

3. **Section headings anchor the structure.** Each major section gets a full-width heading visually distinct enough to signal "new topic" during a scroll. The reader should always know what section they're in.

4. **Card-based containers for discrete ideas.** Individual insights, findings, or content units live in visually distinct cards. Cards create natural chunking boundaries: the reader processes one card at a time.

5. **Tabbed interfaces for parallel categories.** When content splits into parallel tracks (personas, segments, competitors), use tabs rather than stacking everything vertically. Max ~5 tabs per bar; beyond that, consolidate categories.

6. **Modal overlays for expandable detail.** When a card has expandable content, use a modal overlay with backdrop blur, not inline expand/collapse. Modals separate the summary view from the detail view cleanly.

7. **Print flattens interactive elements.** Tabs expand to labeled blocks. Modals expand inline. Dark themes invert to light. Navigation hides. Cards avoid page breaks. The printed version must be fully readable without any interactivity.

8. **Footer with provenance.** Data window, generation date, confidentiality notice, branding. The reader should know when the document was made and what data it covers.

---

## Review Checklist

Format-specific audit for scrollable HTML documents. Run alongside the universal presentation checklist.

- [ ] **Sticky nav present.** `<nav>` element with jump links, `position: sticky`, backdrop-filter for frosted glass. Links match existing sections only: no dead links, no missing links.
- [ ] **Section headings visible on scroll.** Each `<section>` starts with a heading large enough to signal section change during scrolling.
- [ ] **Cards used for discrete content.** Individual insights/findings are in card containers, not floating paragraphs.
- [ ] **Tabs (if present) max ~5.** Tab bars don't overflow on desktop. Tabs have `role="tablist"`, `role="tab"`, `aria-selected`.
- [ ] **Modals (if present) accessible.** Close on Escape, close on backdrop click, `aria-label` on close button, `body` overflow hidden when open.
- [ ] **Print flattens.** `@media print` block: tabs become labeled blocks via `data-tab-label`, modals expand inline, dark inverts to light, nav hidden, cards get `break-inside: avoid`.
- [ ] **Footer complete.** Data window, generation date, confidentiality notice, branding: all present and consistent with header.
