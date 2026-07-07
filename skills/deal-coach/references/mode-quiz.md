# Mode 4: Interactive Quiz (QZ-1 through QZ-4)

Test coaching methodology knowledge with deal-grounded scenarios. Scoring breaks down by Resonate/Elevate/Compel.

The quiz runs on the shared quiz engine — see [roleplay-mechanics.md](../../shared/roleplay-mechanics.md) for question pacing, per-answer grading, and results mechanics. This file defines the methodology-specific quiz types and question construction.

## QZ-1: Choose Quiz Type

```
AskUserQuestion({
  questions: [{
    question: "What type of coaching quiz do you want?",
    header: "Quiz Type",
    options: [
      {
        label: "Stage Recognition",
        description: "A buyer says X — which coaching stage? Tests your ability to diagnose where a deal is."
      },
      {
        label: "Methodology Application",
        description: "You're in [Stage] — what's the right Buyer Mindset, Value Props, and Talking Points approach? Tests methodology knowledge."
      },
      {
        label: "Talk Track Completion",
        description: "Buyer says [objection/question]. Using the coaching methodology, what's your response?"
      },
      {
        label: "Full Review",
        description: "Mix of all categories covering Resonate, Elevate, and Compel. Comprehensive assessment."
      }
    ],
    multiSelect: false
  },
  {
    question: "How many questions?",
    header: "Length",
    options: [
      { label: "Quick (5 questions)", description: "Fast check — 5-10 minutes" },
      { label: "Standard (10 questions)", description: "Thorough assessment — 15-20 minutes" },
      { label: "Deep (15 questions)", description: "Comprehensive review — 25-30 minutes" }
    ],
    multiSelect: false
  }]
})
```

## QZ-2: Load Quiz Material

Load coaching content from the reference files. If deal-specific, ground questions in actual deal data. If generic, use Motion ICP narrative data (the Default Motion Playbook).

Build the question bank by category:

**Stage Recognition:**
- Present a buyer quote or scenario → ask which stage
- Use findings and CRM data for realistic scenarios
- Include red herrings (scenarios that seem like one stage but are actually another)

**Methodology Application:**
- Name a stage → ask for the right approach
- E.g., "You're in Elevate. What are the three beats of the Case for Change?"
- E.g., "A buyer says they're evaluating competitors. Which coaching output fields should you focus on, and what goes in each?"
- Include application questions that test Buyer Mindset → Value Props → Talking Points mapping

**Talk Track Completion:**
- Present a buyer statement → ask for the methodology-backed response
- E.g., "Buyer: 'We're happy with what we have.' Using the Elevate methodology, what do you say next?"
- Score on methodology adherence AND natural delivery

**Full Review:**
- Mix all categories
- Weight toward the selected/inferred stage
- Ensure coverage across all three stages

## QZ-3: Run the Quiz

Present questions one at a time per the shared quiz engine, labeling each with category and stage:

```
QUESTION [N]/[Total]
Category: [Stage Recognition / Methodology Application / Talk Track Completion]
Stage: [Resonate / Elevate / Compel]
[If deal-grounded: "Based on your [Company] deal"]

[Question text]
```

After each answer, grade it (Correct / Partially Correct / Incorrect) with a brief explanation referencing specific coaching elements — and, if deal-grounded, how it applies to their specific deal — plus the running score.

## QZ-4: Quiz Results

See [mode-output-templates.md](mode-output-templates.md) for the full quiz results template with breakdowns by stage, dimension, and category.

After results:

```
Want to:
1. Retake this quiz
2. Take a quiz focused on your weakest area ([Stage])
3. Practice a role play for your weakest area
4. Get a coaching microsite for your weakest area
5. Try a different output mode
6. Done
```
