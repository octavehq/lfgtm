# Writing a public changelog entry

A public entry is a title and one paragraph. Octave's release-notes ingestion builds a Core
Feature out of exactly the parts below and drops anything it cannot define, so the shape is
not a style preference.

## Five beats, one paragraph, 200–900 characters

| Beat | Becomes |
|---|---|
| The **named capability**: a proper name you would put on a slide, used identically forever | the feature's name |
| **What it does**, present tense: "X does Y", never "we shipped X" | what it does |
| **How it works**, one clause, specific enough to be non-generic | how it works |
| **Who feels it** and what changes for them | what it impacts |
| **The problem it removes** | why it exists |

**Self-test:** could you write all five beats from the paragraph alone, without the ticket or
the pull request? If any would be empty, it is a line item, not an entry. Leave it off the page.

**The pitch test**, for deciding whether something belongs at all: a rep pitched last week.
After this shipped, what do they say differently? If the answer is "nothing", it belongs on an
internal log, not here.

## Never on the page

- An availability qualifier ("beta", "early access", "for select customers"). Only work every
  customer can use today reaches this page; reaching for a qualifier means it is not ready.
- Ticket ids, pull request numbers, flag or entitlement names, file paths, internal codenames.
- "Coming soon", process narration, numbers you cannot verify.
- Links of any kind. Page safety refuses them.
- A paragraph starting with `#`, `-`, `*`, `>`, `|` or `1.`, or containing a line break.

## Voice

The beats fix what an entry says; these keep it from reading like a press release.

- **No em dashes in the paragraph.** Use a comma, a full stop or parentheses. The dated heading
  is the one place they stay.
- **Banned words:** improved, enhanced, better, faster, various, several, under the hood,
  leverage, robust, seamless, comprehensive, cutting-edge, game-changer, pivotal, impactful,
  delve, landscape, realm. None of them gives a buyer, or the extraction, anything to act on.
- **Say "is" and "has".** "Serves as", "features", "boasts", "represents" leave the extraction
  guessing.
- **Cut significance inflation.** No "marks a step change", "a new era for", "fundamentally
  rethinks". Delete the clause; if the sentence still works, it was filler.
- **Name the capability.** "A significant step towards better GTM infrastructure" reads the same
  with any noun dropped in.
- **Vary sentence length.** Five sentences of equal length is the loudest tell. One beat can be a
  short sentence.

## Worked example

> **2026-08-20 — Motion Playbooks**
> Motion Playbooks let a sequence agent pick an outreach motion and write every step against it,
> instead of filling one generic template per prospect. The agent matches a prospect's segment
> and buying trigger to a playbook, then plans the whole sequence from that playbook's steps and
> proof points. Reps stop hand-selecting a template per account, and a segment's sequences stay
> on one motion across the team. It exists because generic multi-step sequences were the biggest
> reason reply rates flattened after the first touch.
