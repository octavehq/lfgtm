# Channel Content Templates

Detailed output formats and MCP tool calls for each campaign channel. The main skill workflow references this file — use these templates when generating content for each channel.

## Email Sequence

**MCP Tool Call:**
```
generate_email({
  person: { firstName: "[Persona Name]", jobTitle: "[Persona Title]" },
  numEmails: 4,
  sequenceType: "COLD_OUTBOUND",  // or WARM_OUTBOUND based on campaign type
  allEmailsContext: "<campaign angle, persona pain points, competitive positioning, proof points>",
  allEmailsInstructions: "Campaign: [name]. Angle: [strategic angle]. Each email should build on the previous. Use proof points progressively."
})
```

**Output Format:**
```
EMAIL SEQUENCE (4 emails)
=========================

EMAIL 1: [Subject Line]
Timing: Day 1
Purpose: [Hook with primary pain point]
---
[Email body]

---

EMAIL 2: [Subject Line]
Timing: Day 3
Purpose: [Social proof / value prop]
---
[Email body]

---

EMAIL 3: [Subject Line]
Timing: Day 6
Purpose: [Differentiator / insight]
---
[Email body]

---

EMAIL 4: [Subject Line]
Timing: Day 10
Purpose: [Direct ask / breakup]
---
[Email body]
```

---

## LinkedIn Messages

**MCP Tool Call:**
```
generate_content({
  instructions: "Generate LinkedIn outreach for a campaign targeting [persona]. Create:
    1. Connection request note (300 char max)
    2. Follow-up message after connection (short, value-add)
    3. LinkedIn post draft that the sales rep can publish (thought leadership angle)
    All grounded in: [value props, pain points, proof points]",
  customContext: "<library intelligence gathered>"
})
```

**Output Format:**
```
LINKEDIN CONTENT
================

CONNECTION REQUEST (300 chars)
------------------------------
[Message]

FOLLOW-UP MESSAGE
-----------------
[Message after they accept]

LINKEDIN POST (for rep to publish)
-----------------------------------
[Post draft — thought leadership angle related to campaign theme]

ENGAGEMENT COMMENTS (templates)
-------------------------------
If they post about [topic]: "[Comment]"
If they share [content type]: "[Comment]"
```

---

## Ad Copy

**MCP Tool Call:**
```
generate_content({
  instructions: "Generate 3 ad copy variants for a campaign targeting [persona].
    Each variant needs: Headline (30 chars), Body (90 chars), CTA (15 chars).
    Variant 1: Pain-point led. Variant 2: Social-proof led. Variant 3: Curiosity/insight-led.
    All grounded in: [value props, differentiators, proof points]",
  customContext: "<library intelligence>"
})
```

**Output Format:**
```
AD COPY VARIANTS
================

VARIANT 1: Pain-Led
Headline: [30 chars]
Body: [90 chars]
CTA: [15 chars]

VARIANT 2: Proof-Led
Headline: [30 chars]
Body: [90 chars]
CTA: [15 chars]

VARIANT 3: Insight-Led
Headline: [30 chars]
Body: [90 chars]
CTA: [15 chars]
```

---

## Social Posts

**MCP Tool Call:**
```
generate_content({
  instructions: "Generate 5 social media posts for a campaign targeting [persona].
    Mix of: 1 stat/insight post, 1 question post, 1 mini case study, 1 hot take, 1 educational tip.
    All connect back to: [campaign theme and value props].
    Include hashtag suggestions.",
  customContext: "<library intelligence>"
})
```

**Output Format:**
```
SOCIAL POSTS
============

POST 1: Stat/Insight
[Post body]
#hashtag1 #hashtag2

POST 2: Question
[Post body]

POST 3: Mini Case Study
[Post body]

POST 4: Hot Take
[Post body]

POST 5: Educational Tip
[Post body]
```

---

## Blog Post

**MCP Tool Call:**
```
generate_content({
  instructions: "Generate a full blog post for a campaign targeting [persona].
    Topic: [campaign theme]. Angle: [strategic angle].
    Structure: Title, meta description, intro (hook), 3-4 main sections with subheadings,
    conclusion with CTA. Weave in proof points naturally.
    Length: 1200-1800 words. Tone: [brand voice].",
  customContext: "<library intelligence, proof points, competitive positioning>"
})
```

**Output Format:**
```
BLOG POST
=========

Title: [Title]
Meta Description: [155 chars]
Target Persona: [Persona]

---

[Full blog post content with sections]

---

Internal CTA: [What to link to / landing page]
```

---

## Landing Page

**MCP Tool Call:**
```
generate_content({
  instructions: "Generate landing page copy for a campaign targeting [persona].
    Sections: Hero (headline, subheadline, CTA), Problem statement, Solution overview,
    3 key benefits with descriptions, Social proof section (quotes, logos, metrics),
    FAQ (3-4 questions), Final CTA.
    Tone: [brand voice]. Focus: [campaign angle].",
  customContext: "<library intelligence, proof points, differentiators>"
})
```

**Output Format:**
```
LANDING PAGE COPY
=================

HERO
----
Headline: [Headline]
Subheadline: [Subheadline]
CTA Button: [CTA text]

PROBLEM
-------
[Problem statement copy]

SOLUTION
--------
[Solution overview]

KEY BENEFITS
------------
✓ [Benefit 1]: [Description]
✓ [Benefit 2]: [Description]
✓ [Benefit 3]: [Description]

SOCIAL PROOF
------------
"[Customer quote]" — [Name, Title, Company]
Metrics: [Key stats]
Logos: [Suggest which reference customers]

FAQ
---
Q: [Question 1]
A: [Answer]

Q: [Question 2]
A: [Answer]

FINAL CTA
---------
Headline: [Closing headline]
CTA Button: [CTA text]
Supporting: [Urgency/value text]
```
