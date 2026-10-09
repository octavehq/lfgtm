---
name: public-changelog
description: "Create or append the workspace's public product changelog, a permanent public page that Octave's release-notes ingestion re-reads to propose Product and Core Feature updates. Takes the entries approved for a period (pasted from a changelog staging page, or described in plain words), checks them against publish rules, and adds them without changing any line already live. Use when the user says \"publish to the changelog\", \"add these to the public changelog\", \"start a public changelog\", or pastes approved changelog entries."
---

# /octave:public-changelog - Publish the Public Changelog

The public changelog is one permanent public page per workspace. Octave re-reads it on a
schedule, converts it to markdown and diffs it **as a set of lines**: every line it has not seen
before is read as a newly shipped capability and becomes a library suggestion. Two rules follow,
and everything in this skill exists to keep them:

1. **A live line is never re-worded.** Changing an old entry's text makes it read as brand new
   and re-mints suggestions for something that shipped months ago. The only correction is a
   newer entry that supersedes it.
2. **Whatever goes on the page teaches the library, and so every rep's messaging.** Only work
   every customer can use today belongs there: no fixes, infrastructure, betas or gated features.

So the page is **rendered by a script from a state file, never written by hand.** You supply a
title and one paragraph per entry; [changelog.py](scripts/changelog.py) owns the markup, and
refuses to produce a bundle unless every line already live comes out byte-identical. The live
page is the lock. It stays readable to someone outside engineering: keep messages plain, never
show a stack trace, and when something needs an engineer, say so and stop.

## Usage

```
/octave:public-changelog                  # asks for the entries to publish
/octave:public-changelog <pasted entries> # the JSON a staging page copied, or plain text
```

## What the page holds

The asset is a `website` asset named `public-changelog-<company-slug>` (lowercase), privacy
`public`, status `published`, entry point `index.html`. Its bundle is exactly two files:

| File | Holds |
|---|---|
| `index.html` | The rendered page. Its lines are what the crawl diffs. |
| `changelog.json` | The page title, dek and footer, and every published entry (`id`, `date`, `title`, `body`, `publishedAt`). Public text only. |

**The `public-changelog-` prefix is load-bearing.** Only `/sites/public-changelog-…` is open to
the ingestion crawler, and the path is case-sensitive; a page named anything else publishes
fine and is never read.

## Input

**From a staging page** (for example Octave's own `/product-changelog` routine), the paste is:

```json
{ "schemaVersion": 2, "kind": "changelog-entries", "runId": "2026-09-22",
  "entries": [ { "id": "2026-09-18-motion-playbooks", "date": "2026-09-18",
                 "title": "Motion Playbooks", "availability": "ga",
                 "body": "Motion Playbooks let a sequence agent…" } ] }
```

Keep every `id` as given. The source system matches ids when it reads the page back, to mark
its own records as published.

**In plain words** ("add these three for Sept 1–15"): turn each item into the same shape.
Draft each paragraph with [writing entries](references/writing-entries.md), set `date` to the
ship date (ask if you cannot tell), and set `availability: "ga"` **only after the user confirms
every customer can use it today**. Omit `id`; the script derives one. Show the user each title and
paragraph and get their approval on the wording **before** rendering. Once live, it is final.

## Run it

Work in a scratch directory. Resolve every path below from this installed skill directory.

### 1. Find the page

Call `verify_connection` and say which workspace you are publishing to. Then `assets_list` with
`search: "public-changelog"`. A match is an asset whose identifier starts with `public-changelog`.

- **Several matches:** ask which one. Never guess. Declaring the wrong one splits the history.
- **A match with `canManage: false`:** stop, name its owner, and say that person must transfer
  it or publish themselves. Every write would fail.
- **No match:** this is a first publish. Go to step 2b.

### 2a. Existing page: load its state

Mint the access token now (see step 5 for how), then download the current bundle:

```bash
bash <plugin-root>/skills/asset-manager/scripts/download-artifact.sh --uuid <uuid> --out current
```

- If `current/changelog.json` exists, that is the state.
- If only `current/index.html` exists (a page published before this skill kept state), rebuild it:
  `python3 scripts/changelog.py bootstrap --html current/index.html --out current/changelog.json`.
  It refuses a page it cannot reproduce exactly. If it does, stop: publishing on top of a page
  you cannot reproduce risks changing live lines.

### 2b. New page: fix its chrome once

Resolve the company with `get_workspace_company`. Propose a title, a one-sentence dek and a
footer line, for example "Acme Changelog" / "What we shipped, and what it means for teams using
Acme." / "Acme, <their positioning line>". **Tell the user these three lines are permanent:**
changing one later re-extracts it as a release entry. Then:

```bash
python3 scripts/changelog.py init --title '…' --dek '…' --footer '…' --out current/changelog.json
```

Style it with the workspace brand, following [brand kit usage](../shared/brand-kit-usage.md):
pass the kit's `tokens.css` as `--tokens` and its verified logo files as `--logo-light` /
`--logo-dark` in step 4. The kit's `--brand-*` tokens drive the layout; without a kit the page
falls back to a neutral palette. Never hotlink a font or image. Page safety refuses an external
fetch, because fetched content becomes part of what the crawl reads.

### 3. Write the entries file

Write the entries to `new.json` as `{ "entries": [ … ] }`. For a staging paste, write it as
pasted. Apply any spoken amendments on top ("drop the second one"), then read back one line per
entry (date, title, first words) for confirmation.

### 4. Render and check

```bash
python3 scripts/changelog.py add --state current/changelog.json --entries new.json \
  --html current/index.html --out bundle        # omit --html on a first publish
```

It refuses the **whole** batch on any problem, never part of it. A partial publish would hide
an attempt to touch a live entry. Read each refusal back in plain words. The common ones:

| Refusal | Meaning | Fix |
|---|---|---|
| not marked generally available | an entry is gated, beta or unchecked | drop it; it publishes once it is GA |
| N-character paragraph | outside 200–900 characters | rewrite it (one paragraph, five beats) |
| already live with different text | an id that is live was re-worded | leave it; publish a new superseding entry |
| `✗ history` | a live line would change | stop, an engineer is needed; never edit the state to force it |
| `✗ delta` under the floor | too little new text to trigger ingestion | add the paragraph, or hold until there is more |
| `✗ line-uniqueness` | a line repeats an existing one | reword the new entry's title or paragraph |

On an existing page the stylesheet is carried over from the live page. Pass `--tokens` only
when the user asks to restyle; styling is not crawled, so restyling is safe.

On success it prints the exact lines this publish adds. **Show them to the user and get an
explicit go before step 5.** This is a permanent public write.

### 5. Upload

Mint a fresh token with `asset_generate_access_token` immediately before the script batch, per
[asset script usage](../asset-manager/references/script-usage.md): token in
`ARTIFACTS_ACCESS_TOKEN`, host in `ARTIFACTS_URL` from the mint's `apiBaseUrl`, never on the
command line or in a file. Minting rotates the user's token, so mint after every other asset
tool call.

Existing page (the upload replaces the whole bundle, which is why both files go every time):

```bash
bash <plugin-root>/skills/asset-manager/scripts/update-artifact.sh --uuid <uuid> --src bundle \
  --manifest bundle.manifest.json --expected-version <current version> --note 'Changelog: +N entries'
```

First publish:

```bash
bash <plugin-root>/skills/asset-manager/scripts/upload-artifact.sh --src bundle \
  --manifest bundle.manifest.json --identifier public-changelog-<company-slug> \
  --description '<Company> public product changelog' --type website --privacy public \
  --status published --entry-point index.html
```

Exit 3 means the write may have happened. Reconcile by uuid and version before any retry;
never blind-retry a public write. If an existing page is `unpublished` or not `public` (some
earlier setups held the page back until its first real entry), set it to `published` + `public`
with `asset_update` now that real content is on it.

### 6. Confirm it is really public

Fetch the `siteUrl` **with no cookie or token** and check it against the state:

```bash
curl -sS -f '<siteUrl>' -o live.html && python3 scripts/changelog.py lines --html live.html --expect-state bundle/changelog.json
```

The crawler has no session, so a page that redirects to a login is one nothing downstream reads.
If this fails, report it and escalate. Do not republish.

### 7. Report

What went live, the public `siteUrl`, and anything skipped as already live. On a **first
publish**, also say what only a person can do in the app:

1. **A workspace owner declares the URL as release notes on exactly one Product**
   (Product → release notes → Connect release notes). Use the `/sites/public-changelog-…` URL,
   **not** a vanity `/s/` URL: vanity paths are closed to the crawler, so the declaration
   succeeds and nothing is ever read. One Product only, because the first declared offering
   becomes the parent of every Core Feature the page produces.
2. If suggestions never appear after a crawl, release-notes ingestion may not be enabled for the
   workspace. Ask Octave support.

Mention that Octave re-reads the page on its own schedule; no further step is needed.

## Never

- Hand-edit `index.html` or a live entry in `changelog.json`, or delete a live entry.
- Enable asset↔resource sync on this asset. It would register the page a second time, extracted
  without the release-notes handling.
- Publish a workspace-only log, a staging page, or anything with customer names, deal values or
  internal ticket ids to this asset.
