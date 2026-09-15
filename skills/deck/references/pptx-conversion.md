# PPTX Conversion Path

When a `.pptx` file is provided:

### Extract Content

```python
# Install if needed: pip install python-pptx Pillow
from pptx import Presentation
from pptx.util import Inches, Pt
import json, os

prs = Presentation("input.pptx")
slides = []
deck_dir = ".octave-decks/<deck-name>-<date>"
os.makedirs(f"{deck_dir}/assets", exist_ok=True)

for i, slide in enumerate(prs.slides):
    slide_data = {"index": i, "shapes": []}
    for shape in slide.shapes:
        if shape.has_text_frame:
            slide_data["shapes"].append({
                "type": "text",
                "text": shape.text_frame.text,
                "paragraphs": [
                    {"text": p.text, "level": p.level}
                    for p in shape.text_frame.paragraphs
                ]
            })
        elif shape.shape_type == 13:  # Picture
            img = shape.image
            ext = img.content_type.split("/")[-1]
            fname = f"{deck_dir}/assets/slide{i}_img{len(slide_data['shapes'])}.{ext}"
            with open(fname, "wb") as f:
                f.write(img.blob)
            slide_data["shapes"].append({"type": "image", "path": fname})
    slides.append(slide_data)
```

### Conversion Flow

1. Extract text and images from PPTX using python-pptx
2. Save images to the `assets/` subdirectory inside the deck folder (`.octave-decks/<deck-name>-<date>/assets/`)
3. Show extracted content structure to the user for review
4. **Still run Step 1** (purpose/goal) — the content comes from the PPTX but context matters
5. **Still offer Step 3** (brand) — the original PPTX style is lost in conversion
6. Proceed to Steps 4-6 as normal, using extracted content instead of Octave-generated content

> **Note:** Images from the PPTX are saved as separate files referenced by the HTML. The output is still a single HTML file, but images are external assets. Mention this to the user.

---


Verify the produced file opens, slide count matches and no text/images are lost. A converter command completing is not format fidelity verification. Resolve root helpers from the installed package root per host-runtime guidance.
