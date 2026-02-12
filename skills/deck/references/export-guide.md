# Deck Export Guide

## Export Options

When the user selects "Export to another format," present options:

```
EXPORT OPTIONS
==============

                        Styling  Editable  Notes
1. PDF              *****  No        Print of HTML — full visual fidelity
2. LinkedIn Carousel*****  No        Portrait PDF (1080x1350) — full fidelity
3. PPTX             **     Yes       Text + basic colors only (no gradients/animations/clamp)
4. Google Slides    **     Yes       Via PPTX import — same limitations
5. Gamma            *      Yes       Text outline only — Gamma applies its own styling
6. Markdown         *      Yes       Plain text structure only
7. Keep as HTML     *****  Yes       Already saved, full fidelity + editable

Your choice:
```

---

## PDF Export

Use browser-use if available, otherwise instruct the user:

**With browser-use:**
```
1. browser-use open [presentation-file-path]
2. browser-use eval "window.print()"
   # User selects "Save as PDF" in the print dialog
```

**Without browser-use:**
```
To save as PDF:
1. Open [file path] in your browser
2. Press Cmd+P (Mac) or Ctrl+P (Windows)
3. Select "Save as PDF" as the destination
4. Set margins to "None" for best results
```

---

## LinkedIn Carousel Export

LinkedIn carousels are document posts — a portrait-oriented PDF where each page is one "card." Dimensions: **1080x1350px** (4:5 ratio).

**Approach:** Re-render each slide as a portrait card, then combine into a single PDF.

**With browser-use:**
```
1. Create a temporary carousel HTML file at .octave-decks/<deck-name>-<date>/<name>-carousel.html
   - Same slide content, but CSS overridden:
     width: 1080px; height: 1350px; (portrait)
     font sizes scaled up ~20% for mobile readability
     one <section> per page, no scroll-snap (vertical stack)
     each section has page-break-after: always for print
   - Simplify: remove animations, progress bar, navigation dots
   - Keep: brand colors, typography, layout structure
   - Limit to 10 cards max (LinkedIn carousel limit)
   - First card = hook/title, last card = CTA with profile handle

2. browser-use open [carousel-html-path]
3. browser-use eval "window.print()"
   # User selects "Save as PDF"
   # Set paper size to Custom: 1080x1350px (or 8.5x10.6in at 127dpi)
   # Margins: None
```

**Without browser-use:**
```
LINKEDIN CAROUSEL EXPORT
========================

I've created a carousel-optimized version at:
  .octave-decks/<deck-name>-<date>/<name>-carousel.html

To save as PDF:
1. Open the file in your browser
2. Press Cmd+P (Mac) or Ctrl+P (Windows)
3. Set paper size to Custom: 1080x1350 (or select a 4:5 ratio)
4. Set margins to "None"
5. Select "Save as PDF"

To post on LinkedIn:
1. Create a new LinkedIn post
2. Click the document icon or "Add a document"
3. Upload the PDF
4. Add a title (this appears as the document name)
5. Write your post copy — first 2 lines are the hook
```

**Carousel content adaptation tips** (present to user):
```
CAROUSEL OPTIMIZATION
=====================
Your deck has [N] slides. LinkedIn carousels work best at 5-10 cards.

Adjustments made:
- Landscape layouts -> reformatted for portrait (4:5)
- Grid/comparison slides -> split into individual cards if needed
- Text density reduced for mobile readability
- Card 1 = attention-grabbing hook
- Last card = CTA (follow, link, comment prompt)

Review the carousel HTML before exporting to PDF.
```

---

## PPTX Export

Generate a Python script using `python-pptx` that recreates the slides as a PowerPoint file:

```python
# Install if needed: pip install python-pptx
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

prs = Presentation()
prs.slide_width = Inches(13.333)  # 16:9 widescreen
prs.slide_height = Inches(7.5)

# Extract brand colors from the HTML CSS variables
bg_color = RGBColor(0xXX, 0xXX, 0xXX)      # --bg
text_color = RGBColor(0xXX, 0xXX, 0xXX)     # --text-primary
brand_color = RGBColor(0xXX, 0xXX, 0xXX)    # --brand-primary

# For each slide in the HTML, create a corresponding PPTX slide:
# - Title slides -> blank layout + centered text boxes
# - Content slides -> title + body text boxes
# - Metric slides -> title + large number text boxes
# - Grid slides -> title + arranged text boxes
# - Quote slides -> centered italic text box
# Apply brand colors to backgrounds and text

prs.save(".octave-decks/<deck-name>-<date>/<deck-name>.pptx")
```

Run the script and present the file:
```
PPTX exported: .octave-decks/<deck-name>-<date>/<deck-name>.pptx

Note: The PPTX preserves text content, slide structure, and solid brand
colors. What doesn't transfer: gradients, animations, clamp() responsive
typography, backdrop-filter effects, custom CSS, rounded corners, and
scroll-snap navigation. For full visual fidelity, use PDF or keep HTML.
```

---

## Google Slides Export

```
For Google Slides:

1. I'll export as PPTX first (same as above)
2. Go to slides.google.com -> File -> Import slides
3. Upload the PPTX file
4. Google Slides will preserve text, layout, and colors

The PPTX file is at: .octave-decks/<deck-name>-<date>/<deck-name>.pptx
```

If a Google Drive MCP server is connected, offer to upload directly:
```
I see you have Google Drive connected. Want me to upload the PPTX
directly to your Drive? You can then open it in Google Slides.
```

---

## Gamma Export

Format the slide content as a numbered outline optimized for Gamma's "Generate" input:

```
GAMMA-READY OUTLINE
====================

Slide 1: [Title]
- [Subtitle]

Slide 2: [Section Heading]
- [Bullet 1]
- [Bullet 2]
- [Bullet 3]

Slide 3: [Heading]
- [Key metric]: [Value]
- [Key metric]: [Value]

[Continue for all slides...]

---

To use in Gamma:
1. Go to gamma.app -> Create -> Paste
2. Paste the outline above
3. Gamma will generate styled slides from the structure
```

---

## Markdown Export

Export slide content as structured markdown:

```markdown
# [Deck Title]

---

## Slide 1: [Title]
[Subtitle]

---

## Slide 2: [Heading]
- [Point 1]
- [Point 2]
- [Point 3]

---

[Continue for all slides...]
```

Save to file: `.octave-decks/<deck-name>-<date>/<deck-name>-content.md`
