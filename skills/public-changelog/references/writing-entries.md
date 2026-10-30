# Writing a public changelog entry

A public entry is a title and three short fields, plus whether it is new or an improvement.
Octave's release-notes ingestion builds a Core Feature out of exactly these parts and drops
anything it cannot define, so the shape is not a style preference.

## The fields

| Field | Holds | Becomes |
|---|---|---|
| `title` | The **named capability**: a proper name you would put on a slide, used identically forever | the feature's name |
| `description` | **3–4 sentences**, 4 for a feature that does more: what it does (present tense, "X does Y", never "we shipped X"), how it works (specific enough to be non-generic), and who feels it and what changes for them | what it does, how it works, what it impacts |
| `useCase` | **One sentence that opens "A <role> can now…"** and names what that person can now do, in a concrete moment: "A solutions engineer can now ask how a renewal quote handles invoice owners and get the answer from the product docs." Never "helps teams be more efficient" | what it impacts |
| `problem` | **What the user did, or could not do, before** this shipped | why it exists |
| `novelty` | `"net-new"` (a capability that did not exist) or `"improvement"` (an existing one changed) | not read: drawn as a badge |

The page shows the description as a paragraph, then two labeled lines, `Use case: …` and
`Problem it solves: …`. The labels are part of each line Octave reads, so they never change.
The New / Improvement badge is drawn by the stylesheet rather than written as text, because
"New" on every other entry would be a repeated line, and the crawl swallows repeated lines.

**Novelty sets the framing.** An `improvement` leads its description with what changed about
the existing capability, under its existing name. A capability that was gated and is now open
to everyone is `net-new` to customers: they could not use it before.

**Self-test:** could you name the capability, say what it does, how it works, who feels it and
what problem it removes, from these fields alone, without the ticket or the pull request? If any
would be empty, it is a line item, not an entry. Leave it off the page.

**The pitch test**, for deciding whether something belongs at all: a rep pitched last week.
After this shipped, what do they say differently? If the answer is "nothing", it belongs on an
internal log, not here.

## Never on the page

- An availability qualifier ("beta", "early access", "for select customers"). Only work every
  customer can use today reaches this page; reaching for a qualifier means it is not ready.
- Ticket ids, pull request numbers, flag or entitlement names, file paths, internal codenames.
- "Coming soon", process narration, numbers you cannot verify.
- Links of any kind. Page safety refuses them.
- A field starting with `#`, `-`, `*`, `>`, `|` or `1.`, or containing a line break. Each field
  is one paragraph.

## Voice

The fields fix what an entry says; these keep it from reading like a press release.

- **No em dashes in any field.** Use a comma, a full stop or parentheses. The dated heading is
  the one place they stay.
- **Banned words:** improved, enhanced, better, faster, various, several, under the hood,
  leverage, robust, seamless, comprehensive, cutting-edge, game-changer, pivotal, impactful,
  delve, landscape, realm. None of them gives a buyer, or the extraction, anything to act on.
- **Say "is" and "has".** "Serves as", "features", "boasts", "represents" leave the extraction
  guessing.
- **Cut significance inflation.** No "marks a step change", "a new era for", "fundamentally
  rethinks". Delete the clause; if the sentence still works, it was filler.
- **Name the capability.** "A significant step towards better GTM infrastructure" reads the same
  with any noun dropped in.
- **Vary sentence length.** Sentences of equal length are the loudest tell. One can be short.
- **Don't repeat the description in the other two fields.** The use case is one person's new move,
  the problem is the before; neither restates what the feature does.

## Worked example

> **2026-08-20 — Motion Playbooks** `New`
>
> Motion Playbooks let a sequence agent pick an outreach motion and write every step against it,
> instead of filling one generic template per prospect. The agent matches a prospect's segment
> and buying trigger to a playbook, then plans the whole sequence from that playbook's steps and
> proof points. Reps stop hand-selecting a template per account. A segment's sequences stay on
> one motion across the team.
>
> **Use case:** An SDR can now launch a five-step sequence into a new segment and have every step
> argue the same motion, with that segment's proof points, without picking a template.
>
> **Problem it solves:** Generic multi-step sequences drifted off-message after the first touch,
> which is where reply rates flattened.

As entry JSON:

```json
{ "date": "2026-08-20", "title": "Motion Playbooks", "novelty": "net-new", "availability": "ga",
  "description": "Motion Playbooks let a sequence agent pick an outreach motion…",
  "useCase": "An SDR can now launch a five-step sequence into a new segment…",
  "problem": "Generic multi-step sequences drifted off-message after the first touch…" }
```
