# Data Structures

## Entity qualifyingQuestions Structure

Each entity's `qualifyingQuestions[]` array contains objects with:
- `question` (string) - The question text
- `weight` (string) - "HIGH" | "MEDIUM" | "LOW" | "INSTANT_DISQUALIFIER"
- `fitType` (string) - "GOOD" (should answer Yes for good fits) | "BAD" (should answer Yes for bad fits)
- `rationale` (string) - Guides the agent's interpretation of the question
- `archivedAt` (string|null) - null = active, timestamp = archived (used as negative example)

## Qualification Response Structure

Each qualification response includes per-section results. Each section contains:
- `oId`, `name`, `description` - The selected entity
- `qualification.score` (number 1-10) - Section score
- `qualification.rationale` (string) - Section-level explanation
- `qualification.answers[]` - Per-question breakdown:
  - `question` (string) - Question text
  - `answer` (string) - "Yes" or "No"
  - `rationale` (string) - Why the agent answered this way
  - `confidence` (string) - "HIGH" | "MEDIUM" | "LOW"
  - `weight` (string) - "HIGH" | "MEDIUM" | "LOW" | "INSTANT_DISQUALIFIER"

## Agent Configuration Reference

Saved qualification agents have these tuning-relevant settings:
- `data.commonContext.entities.{type}.strategy` - "BEST_MATCH" (active) or "NONE" (disabled)
- `data.scoringContext.{section}.skipContributingToOverallScore` - Exclude from overall score
- `data.tools.parallelWebSearch.enabled` - Deep research (checks news, articles, job postings)
- `data.tools.highEffortMode.enabled` - More compute for matching/scoring
- `data.model` - NOTE/PULSE/ECHO/HARMONY/CHORUS/SYMPHONY
