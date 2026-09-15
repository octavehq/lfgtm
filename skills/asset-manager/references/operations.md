# Versions and management

Discover the current asset tools and verify their actual schemas. Reuse exact workspace/artifact identity; apply scoped mutation/readback rules from [task-method.md](task-method.md).

## Versions & Rollback

Every file update mints an **immutable version** — an upload never overwrites history. Two fields on every asset response tell the story:

- `currentVersion` — what the bare URL serves right now
- `latestVersion` — the mint high-water mark; higher than `currentVersion` exactly when the asset has been rolled back

The operations (all MCP tools, except the version download):

- **History**: `asset_versions_list` — every version with its note (from `--note` at update time).
- **Rollback**: `asset_version_restore` — instant: repoints the bare URL at the chosen version, no bytes move. Newer versions stay restorable (roll forward the same way), and the next file update mints from the high-water mark (`latestVersion + 1`) — a rollback never loses work.
- **Pin a version in a URL**: append `@vN/` after the `/sites` slug or a vanity slug — e.g. `<base>/sites/<identifier>-<uuid>/@v2/` or `/s/acme/q3-deck/@v2/`. The bare URL always serves `currentVersion`.
- **Download a version's files**: mint token, then `download-artifact.sh --uuid <uuid> --version <N> --out <parent-dir>` — arrives as ONE download, the version's single file or a `.zip` of everything, saved as `<parent-dir>/<identifier>-v<N>[.zip|.<ext>]` (not unpacked).
- **Cleanup**: `asset_version_delete` frees an old version's storage. The CURRENT version can never be deleted (400) — restore a different version first if that is really the goal.

Retention: the service auto-prunes versions past ~20, so history is a rollback safety net, not an archive — download anything that must be kept forever.

## Workflow: Metadata & Privacy (MCP only)

For identifier, description, entry point, privacy, status, or vanity slug changes use `asset_update` (`type` is immutable). Notes:

- Changing the identifier changes the public URL — tell the user the old link breaks.
- Status: `unpublished` hides the asset from the workspace gallery (it stays viewable via preview/workspace links); `published` is the discoverable state. Status never changes who can access — that's `privacy`.
- **When moving DOWN the ladder** (public → workspace, or anything → only_me), explain who loses access, then ask who keeps it:
  1. `workspace`: the URL stops working for the outside world; workspace members still open it after verifying their work email, and teammates keep API access.
  2. `only_me`: everyone but the owner loses access — teammates too (no API read, no preview).
  3. Anyone else needs a **share link** (emails and/or allowed domains, email-verified) — works on any non-public tier.
  Then ask WHO to share with (emails/domains) and whether the link should ever expire (default: never) → Shares workflow. Report the fresh `previewUrl` for teammates alongside the share link.
- **When flipping to `public`**, mention existing share links keep working but are no longer needed. For website assets, run the same unfurl check as publish step 5b first: grep for the og tags and the og:image file, and if anything is missing offer to add the share block and `assets/og.png` via a file update before the flip — public is the only tier where cards render.

## Workflow: Vanity URLs

`asset_update` accepts `vanitySlug` (a string sets it, `null` clears it) to give an asset a pretty URL: `/s/<workspace-handle>/<slug>/`.

- **Slug rules**: lowercase `[a-z0-9-]`, ≤63 chars, no reserved words (the server rejects those). Unique per **workspace** (not per user) — a taken slug returns 409: pick another (suggest a variant).
- The response's `vanityUrl` carries the resulting pretty URL — it appears only when the workspace has a handle. Slug set but `vanityUrl` null → the workspace has no handle yet; the slug is stored and the URL lights up once an admin sets one in Octave.
- `@vN` after the slug pins a version: `/s/acme/q3-deck/@v2/` (see Versions & Rollback).
- **Renaming a slug retires the old URL** — like an identifier change, tell the user the old vanity link breaks. Clearing (`null`) does the same.
- Record `vanitySlug` in the registry and, whenever an asset has a `vanityUrl`, report it alongside the canonical link — it is the one to hand out.

## Workflow: Shares (non-public assets)

Share links grant specific outside people access to any non-`public` asset (both `only_me` and `workspace` tiers) after they verify their email. Create a share:

1. Ask who gets access (AskUserQuestion): `Specific emails` / `Whole domains` ("everyone @company.com — avoids listing every address") / `Both`. Then collect the comma-separated emails and/or domains as free text.
2. Expiry defaults to **never** — don't ask unless the user raises it (or the content is obviously time-boxed); a share accepts `expiresInDays` 1-3650 when they want one.
3. Call `asset_share_create` (uuid, emails?, domains?, expiresInDays only if chosen). At least one email or domain is required.
4. **The response `url` is shown exactly once and can never be retrieved again.** Write it to the registry in the same turn, BEFORE replying to the user. Then give the user the share URL.

Manage existing shares (share uuids come from the registry or `asset_shares_list`):

- Add people: `asset_share_add_recipients` (emails) / `asset_share_add_domains` (domains)
- Remove people: `asset_share_remove_recipients` / `asset_share_remove_domains` — a share must keep ≥1 email or domain; to remove the last one, suggest `asset_share_revoke` instead
- Revoke: `asset_share_revoke` — confirm first (cuts off active viewer sessions immediately, irreversible)

Update the registry after every share mutation.

## Workflow: Access Requests

An access request is a knock on the door: a code-verified viewer opened an asset they can't access (workspace or share flow) and asked to be let in. Requests are owner-only to act on.

1. **The inbox**: `asset_access_requests_list` — a cross-asset rollup; filter `status: pending` for what needs action (other statuses: granted, dismissed). Each entry embeds the asset uuid + identifier plus the requester's verified email, so no per-asset lookup is needed.
2. **Grant**: `asset_access_request_grant` mints a fresh single-recipient, never-expiring share for the requester's email. **The response's share URL appears exactly once and NO email is sent** — same one-time rule as `asset_share_create`: write it to the registry in the same turn, then ALWAYS give the URL to the user to forward to the requester; without that hand-off the grant reaches no one. Granting an already-granted request → 409 (the share exists; find it via `asset_shares_list`).
3. **Dismiss**: `asset_access_request_dismiss` is "not now", not a block — the requester can knock again, which flips the request back to pending. Dismissing a granted request → 409; to take access away, revoke the share instead (Shares workflow).

Surface pending requests whenever the user asks anything like "who wants access" / "any requests on my deck?", and offer grant/dismiss per request.

## Workflow: Who Opened It (Stats & Visitors)

Two owner-only reads answer "how is my asset doing" — pick by the question:

- **How many** → `asset_stats_get`: per-day unique visit and download counts. Trends, not names.
- **Who** → `asset_visitors_list`: the identified viewers — share recipients who code-verified (`via: share`) and workspace members who verified their work email (`via: workspace`).

Anonymous public visitors are **counted in stats but never identified** — never imply the visitor list is complete for a `public` asset. The honest phrasing: "N visits, of which these verified viewers: …".

## Workflow: Download / List / Delete

- **Download**: mint token, then `download-artifact.sh --uuid <uuid> --out <parent-dir>` — files always land in `<parent-dir>/<identifier>/`. Works for any asset the user owns or any non-only_me asset in their workspace, regardless of status/privacy. Add `--version <N>` for a historical version's files (see Versions & Rollback).
- **List**: "what assets are available / do we have X?" → run a fresh `assets_list` and show EVERY asset with its identifier, owner ("me" vs teammate), and link — no row without a link: published + public → the public URL ("anyone with the link"); everything else → the `previewUrl` from that same list response. Reconcile the registry while you're at it. The registry alone is only enough for quick recall of what was published from this project.
- **Delete**: `asset_delete` — irreversible, deletes the files too. Always confirm with the user first. Then remove the entry from the registry.
