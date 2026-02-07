---
name: train
description: Practice selling with role-play simulations and quiz yourself on your GTM knowledge — personas, objections, competitive positioning, and more
---

# /octave:train - Sales Training Ground

Practice and learn your GTM playbook through interactive role-play simulations and knowledge quizzes — all grounded in your real library data. Role-play against buyer personas with realistic objections, or quiz yourself on value props, competitive positioning, and discovery techniques.

## Usage

```
/octave:train [mode] [--persona <name>] [--competitor <name>] [--difficulty easy|medium|hard]
```

## Modes

```
/octave:train                                          # Interactive - pick a mode
/octave:train roleplay                                 # Simulate a buyer conversation
/octave:train roleplay --persona "CTO"                 # Role-play with a specific persona
/octave:train roleplay --scenario discovery            # Practice discovery calls
/octave:train quiz                                     # Test your GTM knowledge
/octave:train quiz --topic objections                  # Quiz on objection handling
/octave:train quiz --competitor "Acme"                 # Competitive knowledge check
```

## Instructions

When the user runs `/octave:train`:

### Step 1: Choose Mode

If no mode specified, ask:

```
AskUserQuestion({
  questions: [{
    question: "What do you want to practice?",
    header: "Train mode",
    options: [
      { label: "Role-Play", description: "Simulate a sales conversation — I'll play the buyer and give you feedback" },
      { label: "Quiz", description: "Test your knowledge of personas, objections, value props, and competitive positioning" },
      { label: "Guided Learning", description: "Walk me through a topic from your playbook — teach me like I'm a new hire" }
    ],
    multiSelect: false
  }]
})
```

---

### Mode: Role-Play

Simulate realistic buyer conversations using persona data from the library.

#### Step RP-1: Setup the Scenario

Ask for scenario parameters (use `AskUserQuestion` for structured choices):

```
AskUserQuestion({
  questions: [
    {
      question: "What scenario do you want to practice?",
      header: "Scenario",
      options: [
        { label: "Discovery call", description: "First conversation — qualify the opportunity and uncover pain" },
        { label: "Objection handling", description: "Practice responding to tough objections mid-deal" },
        { label: "Demo pitch", description: "Present your product's value to a skeptical buyer" },
        { label: "Competitive displacement", description: "Sell against a competitor the buyer currently uses" }
      ],
      multiSelect: false
    },
    {
      question: "How tough should I be?",
      header: "Difficulty",
      options: [
        { label: "Friendly", description: "Interested buyer, open to learning — good for building confidence" },
        { label: "Skeptical (Recommended)", description: "Realistic buyer who pushes back and needs convincing" },
        { label: "Hostile", description: "Tough buyer — time-pressed, has objections, hard to impress" }
      ],
      multiSelect: false
    }
  ]
})
```

If no persona specified, present available personas:
```
# Get personas from library
list_all_entities({ entityType: "persona" })
```

Ask:
```
AskUserQuestion({
  questions: [{
    question: "Which buyer persona should I play?",
    header: "Persona",
    options: [
      { label: "[Persona 1 name]", description: "[Title] — [key concern]" },
      { label: "[Persona 2 name]", description: "[Title] — [key concern]" },
      { label: "[Persona 3 name]", description: "[Title] — [key concern]" }
    ],
    multiSelect: false
  }]
})
```

#### Step RP-2: Load Persona Intelligence

```
# Get full persona details
get_entity({ oId: "<persona_oId>" })

# Get matching playbook with value props
search_knowledge_base({ query: "<persona name> <scenario>", entityTypes: ["playbook"] })
get_playbook({ oId: "<playbook_oId>", includeValueProps: true })

# Get real objections from conversations (to make role-play realistic)
list_findings({
  query: "objections pushback concerns",
  startDate: "<180 days ago>",
  eventFilters: {
    personas: ["<persona_oId>"]
  }
})

# Get product details
list_all_entities({ entityType: "product" })
get_entity({ oId: "<product_oId>" })

# Get competitor details (for competitive scenarios)
get_entity({ oId: "<competitor_oId>" })  // if competitive scenario

# Get proof points (to evaluate if rep uses them)
search_knowledge_base({ query: "<persona> results metrics", entityTypes: ["proof_point", "reference"] })
```

#### Step RP-3: Set the Scene

Present the scenario context, then begin:

```
ROLE-PLAY: [Scenario] with [Persona Name]
==========================================

THE SCENE
---------
You're on a [scenario type] with [Persona Name], [Title] at [fictional company].

About the buyer:
- Role: [Title and responsibilities]
- Company: [Brief fictional company description relevant to your ICP]
- Situation: [Scenario-specific context]
- Mood: [Based on difficulty level]

About their company:
- Industry: [From persona's typical segment]
- Size: [Typical company size for this persona]
- Current challenge: [Key pain point from persona data]

[If competitive scenario:]
- Currently using: [Competitor name]
- Their satisfaction level: [Mixed/frustrated/somewhat happy]

RULES
-----
- I'll respond as the buyer would — using real objections from your conversation data
- The conversation will last 8-12 exchanges
- I'll end the conversation naturally when it reaches a conclusion
- After the role-play, I'll give you a detailed scorecard

---

The call starts now. [Persona Name] says:

"[Opening line based on scenario and difficulty]"
```

**How to play the buyer:**

Use the loaded persona data to respond realistically:
- Reference real pain points from the persona entity
- Raise real objections from conversation findings data
- React based on difficulty level:
  - **Friendly**: Engaged, asks questions, shares information willingly
  - **Skeptical**: Needs proof, challenges claims, asks "why should I care?"
  - **Hostile**: Short answers, pushes on price, questions ROI, brings up competitors
- Respond naturally to what the user says — don't just cycle through objections
- If the user makes a strong point, acknowledge it (even skeptical buyers respond to good selling)
- If the user fumbles, the buyer gets more distant/disengaged

**End the conversation after 8-12 exchanges** with a natural conclusion:
- Friendly: "This sounds interesting, let's set up a follow-up"
- Skeptical: "I need to think about it" or "Send me some materials"
- Hostile: "I don't think this is for us" (unless the user sold well)

#### Step RP-4: Scorecard

After the role-play ends, provide detailed feedback:

```
ROLE-PLAY SCORECARD
====================

Overall: [Score /100]
Difficulty: [Friendly/Skeptical/Hostile]
Scenario: [Type]

---

WHAT YOU DID WELL
-----------------
1. [Specific thing they did well with quote from the conversation]
2. [Another strong moment]
3. [Good technique used]

---

AREAS TO IMPROVE
-----------------
1. [Missed opportunity] — You could have said: "[Better response]"
2. [Weak moment] — Here's why: [Explanation]
3. [Technique to try] — "[Example of better approach]"

---

ELEMENT SCORES
--------------
| Element | Score | Notes |
|---------|-------|-------|
| Opening / rapport | [1-5] | [Brief feedback] |
| Discovery questions | [1-5] | [Brief feedback] |
| Pain identification | [1-5] | [Brief feedback] |
| Value articulation | [1-5] | [Brief feedback] |
| Proof point usage | [1-5] | [Brief feedback] |
| Objection handling | [1-5] | [Brief feedback] |
| Competitive positioning | [1-5] | [Brief feedback, if applicable] |
| Call control | [1-5] | [Brief feedback] |
| Next steps / CTA | [1-5] | [Brief feedback] |

---

KEY MOMENTS
-----------

Moment: "[Quote from the conversation]"
Assessment: [What worked or didn't, with reference to playbook guidance]

Moment: "[Another quote]"
Assessment: [Feedback]

---

OBJECTIONS ENCOUNTERED
-----------------------
| Objection | Your Response | Ideal Response (from playbook) |
|-----------|--------------|-------------------------------|
| "[Objection 1]" | [What they said] | [What the playbook suggests] |
| "[Objection 2]" | [What they said] | [Better approach] |

---

PROOF POINTS YOU COULD HAVE USED
----------------------------------
- [Proof point from library that was relevant but not mentioned]
- [Another unused proof point]

---

Want to:
1. Try again (same scenario, apply the feedback)
2. Try a harder difficulty
3. Try a different persona
4. Practice a specific objection from this session
5. Switch to quiz mode
6. Done
```

---

### Mode: Quiz

Test knowledge of the user's own GTM library.

#### Step Q-1: Choose Topic

```
AskUserQuestion({
  questions: [{
    question: "What do you want to be quizzed on?",
    header: "Quiz topic",
    options: [
      { label: "Personas", description: "Pain points, priorities, buying triggers, and how to sell to each persona" },
      { label: "Objection handling", description: "Common objections and how to respond — from your playbook and real conversations" },
      { label: "Competitive positioning", description: "Differentiators, trap questions, and counters for each competitor" },
      { label: "Full GTM review", description: "Mix of everything — personas, products, value props, objections, competitors" }
    ],
    multiSelect: false
  }]
})
```

Also ask for quiz format:
```
AskUserQuestion({
  questions: [{
    question: "What format?",
    header: "Format",
    options: [
      { label: "Rapid fire (Recommended)", description: "Quick question-answer, 10 questions, scored at the end" },
      { label: "Scenario-based", description: "Situational questions — 'A prospect says X, what do you do?'" },
      { label: "Deep dive", description: "Fewer questions but explain your reasoning — I'll coach you on each answer" }
    ],
    multiSelect: false
  }]
})
```

#### Step Q-2: Load Quiz Material

```
# Load based on topic
# For Personas:
list_all_entities({ entityType: "persona" })
get_entity({ oId: "<persona_oId>" })  // for each persona

# For Objections:
list_findings({
  query: "objections pushback concerns pricing",
  startDate: "<180 days ago>"
})
get_playbook({ oId: "<playbook_oId>", includeValueProps: true })

# For Competitive:
list_all_entities({ entityType: "competitor" })
get_entity({ oId: "<competitor_oId>" })  // for each competitor

# For Full GTM:
list_all_entities({ entityType: "persona" })
list_all_entities({ entityType: "product" })
list_all_entities({ entityType: "competitor" })
search_knowledge_base({ query: "value propositions proof points" })
list_all_entities({ entityType: "use_case" })
```

#### Step Q-3: Run the Quiz

**Rapid Fire Format (10 questions):**

Ask each question one at a time. After the user answers, score immediately, then move on.

Question types per topic:

**Personas:**
- "What are the top 3 pain points for [Persona]?"
- "What's the primary KPI that [Persona] is measured on?"
- "Which value prop resonates most with [Persona]?"
- "What's the best discovery question to open with for [Persona]?"
- "What proof point would you use with [Persona]?"

**Objections:**
- "A prospect says '[Real objection from data]'. How do you respond?"
- "What's the biggest pricing objection you'll face, and what's the counter?"
- "A [Persona] says 'We're happy with what we have.' What do you say?"
- "How do you handle 'It's too expensive' without discounting?"
- "What reframe do you use when they say '[Feature] is missing'?"

**Competitive:**
- "What are our top 3 differentiators vs [Competitor]?"
- "A prospect says '[Competitor] is cheaper.' How do you respond?"
- "What trap question exposes [Competitor]'s weakness in [area]?"
- "When should you NOT try to displace [Competitor]?"
- "What proof point works best in a head-to-head against [Competitor]?"

**Full GTM:**
- Mix of all the above, rotating through topics

Present each question as:
```
QUESTION [N]/10
===============

[Question text]

Your answer:
```

After the user answers:
```
[Correct / Partially correct / Needs work]

Your answer: "[Their answer summarized]"
Best answer: "[From library data]"
[Brief coaching note if needed]

---

Next question...
```

**Scenario-Based Format (5 scenarios):**

```
SCENARIO [N]/5
==============

You're on a [call type] with [Persona Name], [Title] at a [company description].

[Setup: 2-3 sentences of context]

They say: "[Realistic statement or objection from conversation data]"

What do you do? (Describe your response and reasoning)
```

After the user answers, provide detailed coaching:
```
YOUR RESPONSE
-------------
[Summary of what they said]

ASSESSMENT: [Strong / Good / Needs work]

What worked:
- [Specific positive element]

What to improve:
- [Specific gap with coaching]

Ideal approach:
"[Best response from playbook + conversation evidence]"

Why this works better:
[Explanation tied to persona pain points and value props]
```

**Deep Dive Format (3 questions):**

Same as rapid fire, but after each answer, enter a coaching dialogue:
- Ask follow-up questions
- Challenge their reasoning
- Share what works from conversation data
- Connect to playbook guidance

#### Step Q-4: Quiz Results

```
QUIZ RESULTS
=============

Score: [X]/[Total] ([Percentage]%)
Topic: [Topic]
Format: [Format]

---

BREAKDOWN
---------
| # | Question | Score | Notes |
|---|----------|-------|-------|
| 1 | [Brief question] | [Correct/Partial/Wrong] | [One-line note] |
| 2 | [Brief question] | [Correct/Partial/Wrong] | [One-line note] |
| ... | ... | ... | ... |

---

STRENGTHS
---------
- [Area where they scored well]
- [Another strength]

GAPS TO FOCUS ON
-----------------
- [Topic they struggled with] — Review: [specific library entity or playbook section]
- [Another gap] — Practice: [specific recommendation]

---

RECOMMENDED NEXT STEPS
-----------------------
1. Review [specific entity] in your library: /octave:library show [entity]
2. Role-play [specific scenario] to practice: /octave:train roleplay --scenario [type]
3. Read the [playbook name] playbook for [gap area]

---

Want to:
1. Retake this quiz
2. Try a different topic
3. Switch to role-play mode
4. Deep dive on a question I got wrong
5. Done
```

---

### Mode: Guided Learning

Walk through a topic from the library like a training session.

#### Step GL-1: Choose Topic

```
AskUserQuestion({
  questions: [{
    question: "What do you want to learn about?",
    header: "Topic",
    options: [
      { label: "A persona", description: "Deep walkthrough of how to sell to a specific buyer type" },
      { label: "A competitor", description: "Learn competitive positioning, differentiators, and counters" },
      { label: "A playbook", description: "Walk through a playbook's strategy, value props, and objection handling" },
      { label: "Your product", description: "Master your product's capabilities, use cases, and proof points" }
    ],
    multiSelect: false
  }]
})
```

#### Step GL-2: Load and Teach

Fetch the relevant entity and present it as a structured training walkthrough:

```
# Load the entity
get_entity({ oId: "<entity_oId>" })

# Load related playbook
get_playbook({ oId: "<playbook_oId>", includeValueProps: true })

# Load real conversation examples
list_findings({
  query: "<topic>",
  startDate: "<180 days ago>"
})

# Load proof points
search_knowledge_base({ query: "<topic>", entityTypes: ["proof_point", "reference"] })
```

Present as an interactive lesson:

```
TRAINING: Selling to [Persona Name]
=====================================

LESSON 1: Who They Are
-----------------------
[Overview of the persona — role, responsibilities, what they care about]

Quick check: Can you name their top 3 priorities? (Try before scrolling down)

Answer:
1. [Priority 1]
2. [Priority 2]
3. [Priority 3]

---

LESSON 2: Their Pain Points
-----------------------------
[Detailed pain points with context]

From real conversations:
- "[Quote from conversation findings]" — shows [insight]

---

LESSON 3: How to Open
-----------------------
[Best discovery questions for this persona]
[What to listen for]
[Common mistakes to avoid]

---

LESSON 4: Value Props That Work
---------------------------------
[Top value props from playbook, with proof points]

From the field:
- [What's been resonating in real conversations]
- [What's NOT working]

---

LESSON 5: Objections to Expect
---------------------------------
[Common objections with responses]

From real deals:
- [Objections from won deals and how they were handled]
- [Objections from lost deals and what went wrong]

---

LESSON 6: Competitive Angles
------------------------------
[If competitors exist]
[Key differentiators vs each competitor for this persona]

---

SUMMARY CARD
--------------
[Condensed reference card — everything above in 10 lines]

---

Ready to test yourself?
1. Quick quiz on this persona
2. Role-play as this persona (I'll play the buyer)
3. Learn about a different topic
4. Done
```

## MCP Tools Used

### Library Context
- `list_all_entities` - List personas, products, competitors, use cases
- `get_entity` - Full entity details (persona pain points, competitor weaknesses, etc.)
- `get_playbook` - Playbook with value props, discovery questions, objection handling
- `list_value_props` - Value propositions by persona
- `search_knowledge_base` - Proof points, references, messaging

### Conversation Evidence
- `list_findings` - Real objections, pain points, and signals from calls/emails
- `list_events` - Deal outcomes (win/loss evidence for coaching)
- `get_event_detail` - Specific interaction details for training examples

### Content Generation
- `generate_content` - Generate scenario descriptions, coaching feedback

## Error Handling

**No Personas in Library:**
> No personas found in your library.
>
> Role-play and quizzes work best with persona data.
> Add personas first: `/octave:library create persona`
>
> I can still run a general sales quiz using your product info.

**No Conversation Data:**
> No conversation data available yet.
>
> I'll use your library data for role-play and quizzes.
> As your team logs calls and emails, training will get richer
> with real-world objections and patterns.

**No Competitors:**
> No competitors in your library.
>
> Competitive quizzes and displacement role-plays need competitor data.
> Add competitors: `/octave:library create competitor`
>
> I can still quiz you on personas, value props, and general objection handling.

**Sparse Library:**
> Your library has limited data for a full training session.
>
> Start with:
> 1. `/octave:library create product` - Add your product
> 2. `/octave:library create persona` - Add buyer personas
> 3. `/octave:library create competitor` - Add competitors
>
> Even with just a product and one persona, I can run basic training.

## Related Skills

- `/octave:enablement` - Generate training materials (cheat sheets, objection guides, discovery banks)
- `/octave:battlecard` - Deep competitive intelligence for competitive training
- `/octave:insights` - Surface real field intelligence to inform training
- `/octave:wins-losses` - Win/loss patterns to learn from
- `/octave:research` - Research a real prospect before a live call
- `/octave:generate` - Generate real outreach after practicing
