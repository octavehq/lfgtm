# Meeting Prep — Document Sections (10 total)

The full specification for each section of the prep document. Weight sections per the meeting-type emphasis table in SKILL.md.

## 1. Header
Meeting title, generation date, meeting type badge (pill like "Discovery Prep" or "Executive Prep"), duration badge, and the attendee list — each attendee **linked to their verified LinkedIn**, with role. Company name links to their website; use the company logo if `get_external_brand_logo` returned one. Any unconfirmed attendee carries a ⚠ flag.

## 2. Snapshot
The whole situation in one place. This consolidates the opportunity summary and the deal state into a single section **so deal context is never repeated lower in the document**:
- 2-3 sentence situation: who they are, what's at stake, the play.
- A compact deal-state strip — show only the fields that are actually known, omit empties: **Stage · Compelling event · Champion · Economic buyer · Competition · Next milestone** (from `get_deal_deep_dive` / `list_deal_health` / `list_events`). For a brand-new prospect, say so and note what to uncover.
- **What we want out of this meeting** — the single, specific advance/outcome. One line. For a higher-stakes meeting, sharpen this into a 3-part **positioning directive**: *Position us as* … / *Mitigate* … (the risk or competitor to neutralize) / *Advance* … (the specific next step). Outcome-driven, never a minute-by-minute clock.

## 3. Why This Company, Why Now
Make the case that this is a real, well-fit opportunity — grounded, dated, linked:
- **Fit** — segment/ICP match and the 3-5 fit reasons (`qualify_company`). **Show the composite score *and* the breakdown**, because `qualify_company` returns sub-scores (product fit vs segment fit) and the composite can mislead: an account can be a strong *product* fit but score low because it's **out of the segment definition by size or model** (e.g. too large, or B2C). Say which it is — "out-of-segment-by-size, but strong product fit" reads very differently from "bad fit," and a marquee logo deserves the nuance. If it's a genuine strong fit, say so plainly; conviction is persuasive.
- **Why now** — the trigger or compelling event (signals from enrichment, findings, or news).
- **What's happening now** — 1-2 board-level **macro themes** for the company this year (e.g. "path to profitability", "first international expansion"), plus **2-4 recent news items, each with a date and a source link** and the *so-what* for this meeting (`deep_web_research`, `scrape_website`). Macro themes are strategic narratives a board member would care about, not product announcements.
- **Their market** — segment-level intel: what's moving in their category that maps to our value. Keep only what's relevant to the conversation.
- **Similar customers** — 2-3 of our **reference customers** that look most like them (industry, size, use case) and the outcome each saw, selected from the library's `reference` (and `proof_point`) entities. Pick by similarity to this account; don't use `find_similar_companies` (it returns lookalike prospects, not customers). Real references only — no invented logos.

## 4. Stakeholders
A card per **verified, customer-side** attendee or known contact (the internal rep / deal owner belongs in the header's "Prepared for," **not** in this list):
- Name (linked to their real LinkedIn), title, and a deal-role badge: **Economic Buyer**, **Champion**, **Evaluator**, **Influencer**, or **Blocker**.
- What they care about (persona priorities — what this role is measured on), and one note on how to engage them.
- **Unconfirmed people** get a clear ⚠ badge and a "verify before the call" note — never presented as established fact. **But run the internal-vs-customer check first:** a name that resolves to your own team (deal owner / AE / SE) is *internal* — surface it as the deal owner in the header, never as an unconfirmed customer contact. If attendees are unknown, build a *likely* committee from `find_person`, labeled as inferred.

## 5. Why [Product] for Each Persona
A multi-stakeholder meeting (e.g. an eng lead + a head of finance + a head of product) is three different buyers — **don't blur them into one pitch.** For each persona type at the table:
- **Why they care** — their world and the pains this role feels (Motion ICP *Pains and consequences*; `persona` entity).
- **Why [Product] for them** — the value framed for *that role's* outcome, not a feature list (Motion ICP *Benefits and impacts* — the current source for value props; `list_value_props` is deprecated).
- **How we make them the hero** — one line on how our positioning makes *this person* look good in their org (the one who solved the problem / freed the team). Sourced from the Motion ICP cell.
- **Don't lead with** — one thing to avoid with this persona and why (a finance lead doesn't want the developer-velocity pitch).
- **Top use cases** — the 2-3 use cases that matter most to that persona (`use_case` entities; Motion ICP Methodology).

Close with a short **Top use cases for this company** list — the use cases most relevant to *this* account across all personas.

## 6. The Winning Story
The narrative arc to carry through the meeting, grounded in *their* business pain — a story, not a script. Five beats:
1. **Their world today** — how they operate now (the status quo / real alternative, in their language where you have it).
2. **What's breaking** — the business problem and the cost of standing still.
3. **Why now** — the trigger that makes this urgent.
4. **Why [Product]** — the differentiated reason we're the answer for *their* situation (category framing + the one or two things only we do that matter here).
5. **Proof** — a similar customer and the outcome.

One tight paragraph or five short beats. This is the through-line for the whole conversation.

## 7. How to Run the Conversation
**Talking points and beats — not a scripted pitch, and not a minute-by-minute timeline.** No timed phases, no word-for-word lines. Three lanes:
- **Talking points / beats** — the 4-6 moments you want to hit, in rough order. Each is a point or idea, *not a quote*. Lead with their business pain and why-[Product] — not closing language. The seller phrases it in their own voice.
- **Listen for** — the signals, phrases, and reactions that tell you where they really are (buying signals, hesitation, the alternative they're comparing against).
- **Ask for** — the specific advance you want, framed around *their* problem and the logical next step — not your internal process.

Scale the number of beats to the meeting length (more for 60/90 min, fewer for 30). Keep the tone consultative, not salesy.

## 8. Discovery Questions
Questions that **uncover the business problem and the pain unique to their situation** — not your sales process.
- Focus on: how the work happens today and where it breaks; the cost/consequences of the status quo; the outcomes and use cases they'd want; who's involved and how the business decides (because it reveals the org, not to qualify your forecast).
- **Avoid process-forcing questions** — budget/legal/procurement timing, "what would it take to sign this week," "what do you need from billing to move forward." Buyers are allergic to them and they surface no pain. Save logistics for after value is established, and keep them out of this prep.
- 8-12 questions, grouped by theme or persona, each with a one-line note on what a good answer reveals.

## 9. Objections & Competitors
- **Likely objections** — 3-5 objections this buyer is likely to raise, each with a grounded, non-defensive response framed around their business outcome (`objection` entities + real ones from `list_findings`).
- **Competitors & alternatives** — who else is likely in the deal, **including the status-quo / do-nothing / build-in-house alternative** (the "competitive alternative" — often the real one to beat). For each: where they win, where we win, the one differentiator that matters here, and a **trap question** that exposes their weakness without naming them. Mark competition as confirmed vs speculative ("Unknown — potential: …", never "Likely: …"). Sources: `get_competitive_insights`, `competitor` entities, COMPETITIVE Motion Playbooks. For a full displacement plan, point to `/octave:battlecard`.
- **Watch-outs** — one or two landmines or traps to avoid in *this specific* conversation.

## 10. The Line
One memorable sentence that captures the strategic essence of this meeting — the thing you'd write on a sticky note before the call. It distills the whole prep into a single actionable insight.

Examples:
- "They believe the problem exists but don't believe anyone's solved it — that's your opening."
- "The VP is bought in; the Director needs proof it won't break their workflow."
- "This is a displacement deal — lead with what they lose by staying, not what they gain by switching."
