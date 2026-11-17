# Catalog fields

`catalog.json` lists every skill this repo publishes. Beside the release fields (`version`, `changelog`, `requiredTools`, `runtimes`, `default`), each entry says how the skill is offered. Octave reads these when it syncs the catalog. All of them are optional and none limits what a run may do.

| Field | What it holds | Example |
| --- | --- | --- |
| `title` | The name people read, written as the thing that gets done | `"Prepare for a meeting"` |
| `kind` | `job` or `output` (below) | `"job"` |
| `about` | What a run is usually about, most likely first | `["deal", "company", "person"]` |
| `pillars` | The GTM areas it belongs to, home first | `["deal-execution"]` |
| `outputs` | The documents it makes, default first | `["html-document", "slide-deck"]` |

## Kinds

- **job**: gathers evidence about a subject and decides what to say. Most skills.
- **output**: says how something is shaped and styled, for any subject. Run it alone ("make a deck about X") or let a job use it. `deck`, `one-pager`, `microsite`, `document` and `magazine` are outputs: they hold narrative patterns and the rules for the shape, and no opinion about which evidence a subject needs.

## Pillars

`pillars` uses these ids: `outbound`, `deal-execution`, `messaging`, `revenue-intelligence`, `octave-setup`.

`octave-setup` holds the jobs for running Octave itself (the library, the audit, brand kits, assets, qualification, the changelog). It sorts last, after the GTM areas.

## Outputs and the default

`outputs` uses these ids: `html-document`, `one-pager`, `slide-deck`, `magazine`, `microsite`.

The first entry is the default. A request that names a format ("as a deck") gets that one when the skill lists it; a request that names none gets the default. A skill with no `outputs` writes its page from its own references, as before.

List a format only after running the skill in it and reading the result. A skill whose page depends on its own markup (an interactive lesson, a calculator) should leave `outputs` out.

## About

Use these words where they fit, so skills can be offered on the right page: `deal`, `company`, `person`, `call`, `competitor`, `persona`, `segment`, `product`, `topic`, `period`, `team`, `library`.

## Changing these fields

A change to these fields alone needs no version bump: it describes the skill and does not change its files. A change to any file under the skill's folder does, with a changelog entry.
