# Prediction dashboard

Render the schema 0.3 evaluation output without recalculating status or changing its boundaries.

- Scope strip: verified workspace, platform/child account, currency, timezone, source/window/watermark.
- Status counts: PENDING, CONFIRMED, REFUTED, INCONCLUSIVE; show tentative separately.
- Final comparable results: confirmed, refuted, inconclusive, strict hit rate and evaluability; zero denominator is unavailable, not 0%.
- Per-card table: immutable claim/units/window, metric result, status/reason, direction, tentative flag, source freshness and evaluation history.
- Recommendations: bounded proposed tests, owners and prerequisites. No executable mutation controls.

Use neutral descriptive bars with actual denominators; no N=10/80%/30% confidence coloring or automatic promotion. A 4-confirmed/6-refuted final comparable set shows 40% strict hit rate everywhere. Use [HTML document format](../../shared/formats/html-document.md), inherited brand and the shared readiness checks.
