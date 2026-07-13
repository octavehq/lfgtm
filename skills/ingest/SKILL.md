---
name: ingest
description: Ingest a GTM source (case study, positioning brief, launch doc, URL, or pasted text) into the Octave library — diff against existing entities, then apply or queue adds/refines. Use when the user explicitly wants to update the library from a source — e.g. "ingest this case study", "update the library from this URL", "promote this into Octave", "/octave:ingest". Do NOT use for conversation scoring (/octave:analyzer), content rewrite (/octave:repurpose), casual paste-and-chat, or library health with no source document (/octave:audit).
argument-hint: "[<url> | <file-path>] [--apply]"
---

# /octave:ingest — Canonicalize a Source Into Your GTM Library

Ingest a first-party GTM source against your Octave library. Returns a structured breakdown of:

- **Library Gaps** — what to add or refine based on what the document surfaces
- **Contradictions** — where the document disagrees with what the library says
- **Aligned** — where the document confirms and reinforces existing library content

Then write the gaps: **apply directly** (preferred when the user is ready) or **queue as suggestions** when review in Octave is the better fit.

**Core operating principle:** A source updates the library only through an explicit write path. Diff first; never silent mutation. First-party published GTM content is high-trust — after the user reviews the report, make apply easy and prominent. External or contested sources stay evidence until a human accepts.

## Usage

```
/octave:ingest [<url> | <file-path>] [--apply]
```

## Options

- `--apply` - Skip the post-report chooser and write gaps with `create_entity` / `update_entity` after a quick confirm of the list

## Examples

```
/octave:ingest https://www.octavehq.com/customers/workspan
/octave:ingest ~/Downloads/q3-positioning-brief.pdf
/octave:ingest                    # ask for source; a follow-up URL is fetched, not analyzed as a string
/octave:ingest <url> --apply      # confirm gaps, write directly
```

## Instructions

When the user runs `/octave:ingest`:

### Step 1: Identify the Source

**Resolve the Octave MCP server first:** it provides `list_entities`, `search_knowledge_base`, `create_suggestion`, and the rest. From your tool list, get the server name.

Then resolve whatever the user provided — slash-command argument **or** a follow-up reply after you asked for a source. Same rules either way; never treat a URL or file path as text to analyze.

**Source resolution (in order):**

1. **Looks like a URL** (`http://` / `https://`, or a bare domain like `octavehq.com/customers/workspan`) — fetch it. Prefer `scrape_website` / Firecrawl when available (better extraction on marketing sites); else `WebFetch`. Normalize bare domains to `https://`. Extract the full page text; do not summarize. **Never analyze the URL string itself as the document.**
2. **Looks like a file path** (`~/…`, `/…`, `./…`, or a path ending in a known doc extension) — read it with the `Read` tool.
3. **Longer prose / markdown / pasted body** — use as-is (this is the paste path).
4. **Ambiguous short string** (no scheme, no path shape, not enough text to be a document) — ask: is this a URL, a file path, or should they paste the content?
5. **Nothing provided** — ask for a URL, file path, or paste.

A URL sent alone in a follow-up after `/octave:ingest` is still a URL — fetch it. Same for a path. Only fall through to “pasted text” when the content is clearly document body, not a locator.

**Keep the raw source.** Every write tool in Step 5 accepts a `sources` array, so the document itself gets passed to Octave and grounds the generated entity. When you fetched a URL, keep that URL for `{ type: "url", content }` even though you also hold the scraped text for analysis. For paste/file text, use `{ type: "text", content }`. Do not discard the locator after analysis.

Give the document a short descriptive title if the user didn't provide one (e.g. "Q3 Positioning Brief", "WorkSpan Customer Story").

### Step 2: Load the Library Snapshot

`list_entities` takes a single required `entityType` — there is no call that returns the whole library. Build the snapshot with one call per type. Pass `all: true` to get every entity in one response instead of paginating; the default response is slim (name + oId), which is all the snapshot needs.

```
1. list_entities({ entityType: "persona", all: true })
2. list_entities({ entityType: "segment", all: true })
3. list_entities({ entityType: "use_case", all: true })
4. list_entities({ entityType: "competitor", all: true })
5. list_entities({ entityType: "alternative", all: true })
6. list_entities({ entityType: "buying_trigger", all: true })
7. list_entities({ entityType: "objection", all: true })
8. list_entities({ entityType: "proof_point", all: true })
9. list_entities({ entityType: "reference", all: true })
```

> `list_all_entities` was merged into `list_entities` (July 2026) and no longer exists on the MCP server — do not call it.

Skip `product`, `service`, `solution`, `core_feature`, and `brand_voice` unless the document specifically discusses your own offering — they are rarely what an outside document is diffed against.

Then narrow with the document's own language:

```
search_knowledge_base({ query: "<a key claim or theme from the document>" })
```

Semantic search is how you find the *specific* entity a passage relates to; the lists above only tell you what exists. See [../shared/octave-research-toolkit.md](../shared/octave-research-toolkit.md) → "List vs Search". Once you have a candidate match, `get_entity({ oId })` for the full picture before proposing a refine — you cannot judge whether a passage is new information without reading what the entity already says.

**Also load the pending suggestion queue** — it is part of the library state you're diffing against:

```
list_suggestions()    # defaults to pending, last 14 days
```

If a gap you find is already covered by a pending suggestion (same target entity for refines, same proposed name/concept for adds), that's not a reason to drop the finding — it's a finding in its own right. Carry the match into Step 4 as an "already queued" annotation.

### Step 3: Classify the Findings

You are acting as a GTM analyst. Compare the document against the snapshot.

**Quality bar — apply to every finding:**
> "Would a PMM or AE actually reach for this entity in a real deal or campaign?"

If not, exclude it. Do not flag generic business goals, vague endorsements, or content that appears only in hypothetical scenarios, metaphors, or illustrative examples ("imagine a company called Tandem", "say your persona is a CFO named Controller").

**Entity types:** the canonical list of `entityType` values, oId prefixes, and what each type is for lives in [../shared/entity-model.md](../shared/entity-model.md). Use those names exactly.

**Discriminators for the pairs that get misclassified.** These are the calls that go wrong in practice:

| If the document mentions… | It's a… | Not a… |
|---|---|---|
| A named company being evaluated head-to-head — including a named incumbent as status quo | Competitor | Alternative |
| Spreadsheets, manual process, "we'd build it ourselves", doing nothing | Alternative | Competitor |
| A specific event that starts an evaluation — a funding round, a new hire, a board mandate, a realized gap | Buying Trigger | Use Case |
| An ongoing goal or desire ("we want to grow faster") | Nothing — exclude it | Buying Trigger |
| A distinct customer problem the product solves | Use Case | Product feature |
| A citable number, award, benchmark, or concrete result | Proof Point | Reference |
| A nameable customer with a story and outcomes | Reference | Proof Point |
| A concern a buyer raises that must be pre-handled | Objection | Competitor |
| Someone who merely appeared on a call | Nothing — exclude it | Persona |

A Persona must be an archetype the business actively pursues. A Segment is firmographic — not a behavioral descriptor ("companies that care about security").

**Three dimensions.** For each finding, capture:

- **Library Gaps** — surfaced by the document, missing from the library or incomplete in it.
  - `changeType`: `"add"` or `"refine"` (Octave's vocabulary — never "update")
  - `entityType`, `name` (for adds), `oId` (for refines, from Step 2)
  - `instructions`: what to add or change **and why**, as one natural-language paragraph
  - `sourceExcerpt`: verbatim quote, max 100 words
- **Contradictions** — the document asserts a specific claim that conflicts with a specific library entity. Informational only. Omission or different emphasis is not a contradiction.
- **Aligned** — the document makes a substantive claim that confirms a library entity. Informational only. A bare name-drop is not alignment.

### Step 4: Present the Analysis

Follow the output structure in [analysis-report-template.md](references/analysis-report-template.md). Present all three sections, with "None found." where a section is empty.

Stop here and show the user the analysis before writing anything. End with the **Next step** chooser from the template — lead with **Apply now**.

### Step 5: Act on the Gaps

Only **Library Gaps** are actionable. Contradictions and Aligned items never produce writes — a contradiction is for the user to adjudicate, not for you to resolve.

**Gaps already queued (from Step 2) are actioned differently, not dropped.** Never call `create_suggestion` for a gap that matches a pending suggestion — that double-queues. Instead, offer the existing suggestion's actions: `get_suggestion({ oId })` to preview it, `update_suggestion({ oId, instructions })` to fold in anything new this document adds (e.g. a fresh source or a sharper excerpt), or `accept_suggestion` / `reject_suggestion` to resolve it now. A re-run on the same document should end with "N gaps already queued — want to review them?", never with empty output.

#### Choose the write path — Apply is the easy path

After the report, do **not** silently queue. Offer a clear chooser and bias toward apply when the user is ready to update the library:

1. **Apply now** (lead with this) — write gaps with `create_entity` / `update_entity`. Best when the source is first-party / trusted (case study you published, positioning brief, launch doc) and the user already reviewed the report in this chat. One generation pass; library is current when the turn ends.
2. **Queue for review** — `create_suggestion` per gap. Use when suggestions earn their keep (see below) — not as busywork after the user already signed off on the report.
3. **Selective** — "apply the reference and proof points", "queue the competitor", "adds only". Respect the selection; mix paths per gap if asked.

If the user passed `--apply`, confirm the gap list once, then write — no second chooser.

**When suggestions are worth it** (queue only in these cases, and say why):

| Use suggestions when… | Why it beats apply |
|---|---|
| Another stakeholder should accept in the Octave inbox (not this chat) | Async review without re-running the skill |
| Source is external, contested, or low-trust | Park proposals without mutating the live library |
| You want to park gaps and decide later | Inbox is durable; chat context is not |
| A refine is speculative and you want a reversible proposal | Suggestion can be rejected with no entity rewrite |

**When queueing is wasted work** (prefer apply):

- The user already reviewed the report and said to update the library — queueing then accepting doubles LLM cost (generate suggestion → accept generates again) and adds a trip through the inbox for no second opinion.
- First-party published content the user brought specifically to ingest.

Be explicit in the chooser: *"Apply writes the library in one pass. Queue is for when someone else should review in Octave, or the source isn't trusted enough to commit yet."*

#### Apply path

Confirm the list first, then:

```
create_entity({
  entityType: "competitor",
  name: "Tandem",
  instructions: "<same natural-language description of what to create and why>",
  keyContext: "<document title and verbatim excerpt>",
  sources: [{ type: "url", content: "<document url>" }]
})

update_entity({
  entityType: "persona",
  oId: "pe_abc123",
  instructions: "<what to change on this persona and why>",
  keyContext: "<document title and verbatim excerpt>",
  sources: [{ type: "text", content: "<document text>" }]
})
```

These are generation endpoints — they take instructions and sources, not field values. `create_entity` defaults to `linkingStrategy: { mode: "ALL" }`, which links the new entity to every active offering; pass `{ mode: "SPECIFIC", offeringOIds: [...] }` when the document is clearly about one offering.

Pass the document through in `sources` — `{ type: "url", content }` for a URL (Octave fetches it) or `{ type: "text", content }` for pasted text. This grounds the generated entity in the real source instead of your paraphrase of it, and it is the single highest-leverage thing this skill does.

> `create_entity({ autoAccept: false })` is a third path — it generates the entity but leaves it PENDING. Reach for it only when the user wants a *fully drafted* entity to review rather than a proposal; `create_suggestion` is the review route that can also propose a refine.

#### Queue path

Call `create_suggestion` once per new gap. Each one lands as a PENDING suggestion in the Octave suggestions inbox and changes nothing until a human accepts it.

```
create_suggestion({
  changeType: "add",                    // or "refine"
  entityType: "competitor",
  name: "Tandem",                       // required when changeType is "add"
  oId: "cp_abc123",                     // required when changeType is "refine"
  instructions: "Add Tandem as a competitor. The post describes them as the incumbent this
                 buyer replaced, citing a 6-week implementation and no SOC 2. Sales is
                 hitting them in mid-market deals with no battlecard today.",
  keyContext: "Source: Acme blog, 'Why We Switched', published March 2026",
  sources: [{ type: "url", content: "https://acme.com/blog/why-we-switched" }]
})
```

Put the verbatim excerpt and document title in `instructions` / `keyContext` so the reviewer can judge the suggestion without reopening the document.

After queuing, report how many suggestions were created and offer the review path both ways:
- `get_suggestion({ oId })` — preview a suggestion in full (proposed entity + current-vs-after diff) right here in the conversation
- `update_suggestion({ oId, instructions })` — revise a pending suggestion in natural language ("make the pain points more specific") before accepting
- `accept_suggestion({ oId })` / `reject_suggestion({ oId })` — apply or dismiss without leaving Claude
- Or point them at the Suggestions inbox in the Octave app

### Step 6: Offer to File the Document as a Resource

The analysis is a snapshot; the document can keep working. Offer to add it to the library:

```
create_resource({ mode: "url", url: "<document url>", name: "<document title>" })
create_resource({ mode: "text", text: "<document text>", name: "<document title>" })
```

This does two things the one-off analysis cannot:

1. **Permanent recall** — the document becomes searchable via `search_knowledge_base` / `search_resources`, and entities gain provenance links back to it (`get_entity({ includeSources: true })`).
2. **Continuous mining** — Octave's own analytics pipeline extracts findings from indexed resources (use cases, proof points, competitors, personas) and its scheduled GENERATE/REFINE suggestion flows keep proposing library improvements from them over time. This skill is the interactive, immediate version of that same loop; filing the resource hands the document to the automated one.

The pipeline may later propose suggestions overlapping the ones written in Step 5 — that's expected, and overlaps are easy to reject in the inbox.

Skip this step if the document is external content the user wouldn't want in their library (e.g. a competitor's blog post being analyzed for intel — ask when unsure).

## MCP Tools Used

| Tool | Step | Purpose |
|------|------|---------|
| `list_entities` | 2 | Library snapshot — one call per `entityType`, with `all: true` |
| `search_knowledge_base` | 2 | Find the specific entities a passage relates to |
| `get_entity` | 2 | Full detail on a candidate match before proposing a refine |
| `list_suggestions` | 2 | Load the pending queue as part of the snapshot — powers "already queued" annotations |
| `create_entity` / `update_entity` | 5 | Direct write — preferred apply path |
| `create_suggestion` | 5 | Queue a PENDING add/refine when async/inbox review is needed |
| `get_suggestion` / `update_suggestion` | 5 | Preview a queued suggestion; revise it in natural language |
| `accept_suggestion` / `reject_suggestion` | 5 | Apply or dismiss a queued suggestion |
| `create_resource` | 6 | File the document into the library for search + continuous mining |

Document fetching: `scrape_website` or Firecrawl when available, else `WebFetch`. Local files: `Read`.

Tool selection and standard error responses: [../shared/octave-research-toolkit.md](../shared/octave-research-toolkit.md).

## Error Handling

Standard responses (connection failed, empty results): see [../shared/octave-research-toolkit.md](../shared/octave-research-toolkit.md) → Standard error handling. Skill-specific:

**Empty library:**
> Your library has no entities yet, so there's nothing to diff against. I can still extract what this document *would* add as a starting library — or run `/octave:audit` first to design the library deliberately rather than letting one document shape it.

**Document unreachable (404 / fetch error):**
> I couldn't fetch that URL. Paste the text directly, or check that the page is publicly accessible.

**No findings:**
> No gaps, contradictions, or aligned items found. Either the document is already reflected in your library, or it has no GTM-relevant signal (a technical doc, a legal page, unrelated content).

**Document is about a Motion-level narrative:** this skill writes flat library entities only. If the document's real contribution is strategic narrative, pains and consequences, or benefits and impacts for a persona × segment cell, say so and point the user at `/octave:messaging` or `/octave:icp-refine`, which write to Motion Playbook narratives.

## Related Skills

- `/octave:library` — Browse, create, and update library entities directly
- `/octave:audit` — Full library health check (gaps, staleness, duplicates, design quality)
- `/octave:icp-refine` — Refine ICP definitions and Motion ICP narratives from deal outcomes
- `/octave:messaging` — Build messaging frameworks and write them into Motion Playbook narratives
- `/octave:analyzer` — Score a conversation (call, email) for resonance and adherence
- `/octave:repurpose` — Rewrite existing content for a different audience (does not update the library)
