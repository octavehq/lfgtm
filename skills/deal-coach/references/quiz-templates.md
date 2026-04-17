# Interactive Quiz Templates (QZ-1 through QZ-4)

## QZ-1: Quiz Setup

```
AskUserQuestion({
  questions: [{
    question: "What type of coaching quiz do you want?",
    header: "Quiz Type",
    options: [
      { label: "Stage Recognition", description: "Buyer says X — which coaching stage? Tests deal diagnosis." },
      { label: "Methodology Application", description: "You're in [Stage] — what's the right approach? Tests methodology." },
      { label: "Talk Track Completion", description: "Buyer raises objection — what's your methodology-backed response?" },
      { label: "Full Review", description: "Mix of all categories across Resonate, Elevate, and Compel." }
    ],
    multiSelect: false
  },
  {
    question: "How many questions?",
    header: "Length",
    options: [
      { label: "Quick (5)", description: "5-10 minutes" },
      { label: "Standard (10)", description: "15-20 minutes" },
      { label: "Deep (15)", description: "25-30 minutes" }
    ],
    multiSelect: false
  }]
})
```

## QZ-2: Question Bank Structure

Load coaching content from reference files. Ground in deal data (deal-specific) or playbook data (generic).

### Stage Recognition
- Present buyer quote/scenario → ask which stage
- Use findings and CRM data for realistic scenarios
- Include red herrings (scenarios that seem like one stage but are another)

### Methodology Application
- Name a stage → ask for the right approach
- E.g., "You're in Elevate. What are the three beats of the Case for Change?"
- Test Buyer Mindset → Value Props → Talking Points mapping

### Talk Track Completion
- Present buyer statement → ask for methodology-backed response
- E.g., "Buyer: 'We're happy with what we have.' Using Elevate methodology, what next?"
- Score on methodology adherence AND natural delivery

### Full Review
- Mix all categories, weight toward selected/inferred stage
- Ensure coverage across all three stages

## QZ-3: Question Presentation

```
QUESTION [N]/[Total]
Category: [Stage Recognition / Methodology Application / Talk Track Completion]
Stage: [Resonate / Elevate / Compel]
[If deal-grounded: "Based on your [Company] deal"]

[Question text]
[Multiple choice: 4 options | Open-ended: free response]
```

After each answer:
```
[Correct / Partially Correct / Incorrect]
[Explanation referencing coaching elements + deal application]
Score so far: [X]/[N]
```

## QZ-4: Results Template

```
COACHING QUIZ RESULTS
=====================
Score: [X]/[Total] ([Percentage]%)
Category: [Quiz Type]
Grounding: [Company Name / Generic Practice]

BREAKDOWN BY COACHING STAGE
| Stage | Questions | Correct | Score | Assessment |
|-------|-----------|---------|-------|------------|
| Resonate | [N] | [N] | [X]% | [Strong/Adequate/Needs Work] |
| Elevate  | [N] | [N] | [X]% | [Strong/Adequate/Needs Work] |
| Compel   | [N] | [N] | [X]% | [Strong/Adequate/Needs Work] |

BREAKDOWN BY COACHING DIMENSION
| Dimension | Questions | Correct | Score |
|-----------|-----------|---------|-------|
| Buyer Mindset | [N] | [N] | [X]% |
| Value Propositions | [N] | [N] | [X]% |
| Talking Points | [N] | [N] | [X]% |

BREAKDOWN BY CATEGORY
| Category | Questions | Correct | Score |
|----------|-----------|---------|-------|
| Stage Recognition | [N] | [N] | [X]% |
| Methodology Application | [N] | [N] | [X]% |
| Talk Track Completion | [N] | [N] | [X]% |

STRENGTHS
[2-3 areas of strong knowledge with examples]

GAPS TO FOCUS ON
[2-3 areas needing improvement with coaching references]
Per gap: recommended practice mode, study section, exercise suggestion.

RECOMMENDED NEXT STEPS
1. [Primary] 2. [Secondary] 3. [Optional stretch]
```

## Post-Quiz Options

```
Want to:
1. Retake this quiz
2. Take a quiz focused on your weakest area ([Stage])
3. Practice a role play for your weakest area
4. Get a coaching microsite for your weakest area
5. Try a different output mode
6. Done
```
