---
name: asset-manager
description: Publish and manage hosted assets (HTML sites, docs, file bundles) on the Octave assets service - upload, privacy (only_me/workspace/public), share links, versions/rollback, access requests, visit stats, vanity URLs, and a persistent registry of everything published. Acts as a cache - always checks the asset store for an existing match before creating anything new, so the same work is never done twice. Use when the user says "publish this", "host this html", "store these files" (storage type), "share this with the team / workspace / with an email", "make it public/private", "who has access to", "who opened / viewed my deck", "any access requests", "roll back / restore the previous version", "transfer this asset to", "hand this over to", "take over my teammate's asset", "give it a nicer URL / vanity URL", "update the published site", "list my published assets", "what assets are available", "is there already a ... published", "do we have a ...", or wants a shareable URL for something they built locally. Do NOT use for Vercel deploys of microsites (that is /octave:microsite's own deploy step) or for generating the content itself (use the Document Builder skills).
---

# /octave:asset-manager - Publish & Manage Hosted Assets

Manage the full lifecycle of hosted assets on the Octave assets service: upload local sources (HTML sites, markdown, file bundles), control who can see them, create and manage share links, and keep a persistent registry of everything published.

## The Privacy Model (one ladder)

Every asset has exactly one `privacy` tier — each is strictly more open than the last:

| `privacy` | Who can open the link |
|-----------|----------------------|
| `only_me` | The owner only (plus anyone given an explicit share link) |
| `workspace` *(default)* | Owner + workspace members — a teammate opening the link verifies their work email once, then sees everything their team has shared |
| `public` | Anyone with the URL |

Four more facts complete the model:

- `status` is a separate axis: `published` (default; discoverable in the workspace gallery) vs `unpublished` (hidden, but still viewable via preview/workspace links). Status never affects the privacy tier.
- **"Externally shared" is not a tier.** Share links (emails/domains + verification) work on any non-`public` asset; the API reports the derived `externallyShared: true` on an asset that has at least one share link. Creating or revoking shares never changes `privacy`.
- **Locked-out viewers can knock.** A code-verified visitor who hits an asset they can't open (workspace or share flow) can request access; those requests land in the owner's inbox (see Access Requests workflow).
- **Workspace admins/owners can manage the team's assets.** Every asset response carries computed `canEdit` / `canManage` booleans: true for your own assets, and for any non-`only_me` asset in your workspace when your role is admin/owner. When `canManage` is true you may update files, metadata, shares, versions, stats, and transfer ownership — even for a teammate-owned asset. Never re-derive this from roles yourself; trust the fields on the response. `only_me` stays a true personal drawer: no admin override, ever.

**Link lifetimes:** share links never expire by default (expiry is opt-in per share); a viewer's verified session and a `previewUrl` each last ~30 days. Rule of thumb: hand out a `previewUrl` for a teammate's quick look, a share link for an external "review this deck" — neither will rot mid-conversation. Revoking a share still cuts access immediately.

## Usage

```
/octave:asset-manager                       # Interactive - asks what to do
/octave:asset-manager publish <path>        # Publish a folder, file, or .zip
/octave:asset-manager update <identifier>   # Replace files or change metadata
/octave:asset-manager share <identifier>    # Create/manage share links
/octave:asset-manager versions <identifier> # Version history, rollback, pinned URLs
/octave:asset-manager transfer <identifier> # Transfer ownership to a teammate
/octave:asset-manager requests              # Access-request inbox (grant / dismiss)
/octave:asset-manager stats <identifier>    # Visits, downloads, who opened it
/octave:asset-manager list                  # List published assets (from registry)
/octave:asset-manager download <identifier> # Download an asset's files locally
/octave:asset-manager delete <identifier>   # Delete an asset (confirms first)
```

## The One Decision Rule

Every operation routes through exactly one of two backends. Never mix them up:

| Operation | Route |
|-----------|-------|
| Upload new files, replace files, download files (current or a pinned `--version`) | Bash scripts in `${CLAUDE_PLUGIN_ROOT:-.}/skills/asset-manager/scripts/` |
| Everything else: metadata, status, privacy, vanity slugs, shares, tokens, listing, versions (list/restore/delete), access requests, stats & visitors | MCP `asset_*` / `assets_list` tools |

- **Never** use `update-artifact.sh` for metadata-only changes — that is `asset_update`'s job.
- **Never** try to upload files via MCP — no such tool exists (intentionally).

## MCP Tools Are Tool Calls (never bash)

`assets_list`, `asset_generate_access_token`, `asset_update`, and every other `asset_*` tool are **tool calls**. You cannot reach them through bash or python.

- **Never** write a script that echoes, simulates, curls, or "assumes" the result of an MCP tool. A check whose tool result is not in your transcript **did not happen**.
- **Never** print "assuming no duplicates found" or "ready to proceed once token is available" — each of those is the signal that the next action is the missing tool call itself, right now.
- The script headers mention `POST /api/v1/user/access-token` — that endpoint is for service operators with a service key. **You cannot call it.** Your ONLY token source is the `asset_generate_access_token` / `asset_refresh_access_token` tool calls.
- **No helper scripts.** The 4 bundled scripts are the only shell this skill needs; the single permitted extra shell is the one-line staging `cp`/`rm` documented where it's used. Do not write wrappers, staging helpers, or scripts that print status instead of performing an action.

## Check Before Create (Cache Rule)

The asset store doubles as a cache: the asset the user wants may already exist — created by you in another project or session, **or by a workspace teammate** (workspace-shared assets appear in `assets_list` with their `owner`). **Never create a new asset without checking first.**

Before ANY new upload:

1. Run a **fresh `assets_list`**. Never trust the local registry alone for this — it is per-project and lags behind assets created elsewhere.
2. Match the intended asset against existing ones: normalize identifiers (kebab-case → words) and compare against the intended name/topic keywords; scan descriptions; weigh `type` (website vs storage).
3. **Plausible matches found** → AskUserQuestion with up to 3 candidates. Each option shows the identifier, and its description says what it is, **who owns it** (`owner`: "me" or a teammate's name), plus the link (siteUrl, previewUrl for non-public, or download URL). Always include a final option: `No — this is new, create it`. A teammate-owned match can be reused and downloaded; whether it can be MODIFIED is answered by its `canManage` field (true for workspace admins/owners on non-`only_me` assets) — when false, create the user's own copy instead.
   - User picks a match → show its link, then ask what next: nothing / update its files / change metadata / manage shares.
   - User says it's new → proceed to publish, choosing an identifier distinct from the matches (avoids a 409).
4. **No match** → proceed directly, mentioning that nothing similar was found.

Ordering constraint: `assets_list` is an MCP asset call and **rotates the access token** — always do this check BEFORE minting the upload token.

## Workspace Sharing & Preview Links

Assets default to the **`workspace` tier**: teammates can READ them through the API (list/get/download) — even unpublished ones — and can open the live `/sites` link itself by verifying their work email once. All mutations and share management stay owner-only. Set `privacy: only_me` at create (or later) to keep an asset owner-only.

- Every asset response carries `owner`: `"me"` for your own, otherwise the teammate's `"First Last <email>"` (plus a structured `ownerEmail`). **Whether a teammate-owned asset is modifiable is decided by its `canManage` field**, computed from the caller's workspace role: false → strictly read-only (never call `asset_update`, `asset_delete`, or any share tool on it; create the user's own copy instead); true (workspace admins/owners, non-`only_me` assets) → the full management surface works, including machine-published assets like pre-captured brand kits.
- Every asset response also carries `externallyShared` (derived): true when a non-`public` asset has at least one share link — a quick "who else can see this" signal.
- Non-public assets (`only_me`, `workspace`, or `unpublished`) carry a **`previewUrl`**: a tokenized link that renders the site/download for the owner and workspace members without making it public. It is `null` once the asset is published + public (use `siteUrl` then). It lasts ~30 days but is **minted per read — NEVER store it in the registry**; fetch a fresh one with `asset_get_by_id` when someone needs it.
- **Always include the link.** Every time you list, upload, update, or otherwise mention an asset, include its link:
  - published + public → `Public — anyone with the link can view: <siteUrl>` (websites) or `<base>/download/<uuid>` (storage)
  - workspace tier → the `siteUrl` works for teammates directly (they verify their work email once); include the `previewUrl` too for a zero-friction open.
  - only_me or unpublished → `Preview (you + workspace members): <previewUrl>` — taken fresh from the response in hand (list/get) or the script's `preview:` output line, never from the registry. Add a share link for people outside the workspace when relevant.

## MCP Server Detection

Refer to tools by bare name (`asset_update`, `assets_list`, ...). The live server is named `mcp__octave-<workspace>__*` — the workspace suffix varies per user. Detect the active Octave MCP server from the available tool list; never hardcode a prefix.

Available asset tools: `asset_generate_access_token`, `asset_refresh_access_token`, `assets_list`, `asset_get_by_id`, `asset_update`, `asset_delete`, `asset_share_create`, `asset_shares_list`, `asset_share_revoke`, `asset_share_add_recipients`, `asset_share_remove_recipients`, `asset_share_add_domains`, `asset_share_remove_domains`, `asset_transfer`, `asset_versions_list`, `asset_version_restore`, `asset_version_delete`, `asset_access_requests_list`, `asset_access_request_grant`, `asset_access_request_dismiss`, `asset_stats_get`, `asset_visitors_list`.

## Token Lifecycle (CRITICAL)

The access token authorizes the bash scripts. Its lifecycle has one hard rule:

> **Every MCP asset call rotates the token.** Any `asset_*` / `assets_list` call internally mints a fresh token for this user+workspace and **invalidates the previous one**. A token you got a minute ago is dead the moment any other asset MCP tool runs.

Therefore:

1. Mint the token via `asset_generate_access_token` **immediately before** each batch of bash script calls — after all MCP calls for this step are done.
2. If any asset MCP call happens mid-flow, re-mint before the next script call.
3. If a script returns 401: call `asset_refresh_access_token`, retry the script once.
4. **STOP precondition:** before running ANY script you must hold an `accessToken` value returned by a tool call **in this conversation**. If you don't have one, the next action is the `asset_generate_access_token` tool call — not a script, not a question to the user.

Script invocation form (inline env only — never `export` into the profile, never echo the token, never write it to any file):

```bash
ARTIFACTS_ACCESS_TOKEN='<token>' \
  bash "${CLAUDE_PLUGIN_ROOT:-.}"/skills/asset-manager/scripts/<script>.sh <flags>
```

(The scripts resolve the base URL themselves — see Base URL Resolution. Prefix `ARTIFACTS_URL='<url>'` only when the user explicitly targets a different environment.)

In the registry, record only the token `prefix` and `expiresAt` — **never the plaintext token**.

## Base URL Resolution

**The scripts resolve the base URL themselves** — do not compute or pass it unless the user explicitly targets a different environment. Resolution order (built into every script):

1. `ARTIFACTS_URL` environment variable (explicit override — set it only when the user asks for a specific environment)
2. `.env` at the plugin root (development clones only — never present in marketplace installs)
3. Production default: `https://link.octavehq.com`

Record the base URL the API reports back (e.g. from `siteUrl`) as `base_url` in the registry — it's a record of where the assets live, not an input.

## The Bundled Scripts

All in `${CLAUDE_PLUGIN_ROOT:-.}/skills/asset-manager/scripts/` (bash + curl; jq optional; works on macOS/Linux/Windows via Git Bash or WSL):

| Script | Purpose | Key flags |
|--------|---------|-----------|
| `zip-and-upload-artifact.sh` | Zip a folder locally, upload as one request (default for folders; zip fallback chain: zip → powershell → python) | `--src <folder> --identifier --description --type --privacy --status --entry-point` |
| `upload-artifact.sh` | Upload a ready `.zip`, or a folder as per-file multipart (fallback if zipping fails; skips dotfiles) | same as above, `--src` accepts folder or `.zip` |
| `update-artifact.sh` | Replace an asset's files (FULL REPLACE — mints a new immutable version) | `--uuid <u> --src <path> --note <text>` (`--note` = "what changed" on the minted version; only valid with `--src`) |
| `download-artifact.sh` | Download all files of an owned or workspace-shared asset, or one historical version | `--uuid <u> --out <parent-dir>` — files always land in `<parent-dir>/<identifier>/`; add `--version <N>` to grab version N as a single file or zip at `<parent-dir>/<identifier>-v<N>[.zip\|.<ext>]` |

Script gotcha: metadata values are interpolated into JSON **without escaping** — `--identifier`, `--description`, `--entry-point`, and `--note` values must contain no double quotes or backslashes (the scripts now reject them rather than corrupt the payload). If the description needs them, upload with a plain placeholder and set the real text afterward via `asset_update` (which is JSON-safe).

## Workflow: Publish a New Asset

1. **Identify the source.** Confirm the path exists. Classify:
   - Contains HTML → `--type website`. Determine the entry point (default `index.html`; if the main file has another name, pass `--entry-point <file>`).
   - Files for storage/distribution rather than viewing (docs, zips, datasets, binaries) → `--type storage`: no entry point, never served as a site; delivered via `<base>/download/<uuid>` when public, or via previewUrl/share link when private.
2. **Check for existing work — apply the Cache Rule** (see above). If the user confirms an existing asset is what they meant, switch to that asset (show link, then update/share/etc.) instead of publishing. Only continue here once it's confirmed new.
3. **Suggest an identifier.** The identifier is user-facing — it appears in the public URL `<base_url>/sites/<identifier>-<uuid>/`. Heuristics:
   - kebab-case, lowercase, ≤50 chars, no quotes/backslashes
   - Prefer the HTML `<title>` or H1 if meaningful; else the source folder basename
   - Strip dates, `tmp`/`final`/`v2` noise suffixes
   - Must not collide with existing identifiers — reuse the `assets_list` result from step 2 (no second call); identifiers are unique per user
4. **Ask the user** (two AskUserQuestion calls):
   - First — identifier: offer your suggestion first (`<suggestion> (Recommended)`), 1-2 sensible alternates; the user can always type their own via Other.
   - Second — one question: **privacy**.
     - `Workspace (Recommended)` — "Your team can find, open, and reuse it — this is what makes the asset cache work."
     - `Public` — "Anyone with the URL can view."
     - `Only me` — "Just you; others need a share link."
     Status is NOT asked — default `published`. Only mention `unpublished` if the user says "draft"/"not ready yet" (set it via `--status unpublished` or later via `asset_update`).
5. **Draft the description.** 1-2 sentences saying what the asset is and who it's for (e.g. "Interactive use-case explorer for Acme's platform, built for the Q3 ABM campaign"). Sanitize for the script (no `"` or `\`).
6. **Mint the token** (`asset_generate_access_token`) and resolve the base URL. Do this AFTER steps 1-5 — the step-2 `assets_list` already rotated any earlier token, and no MCP asset calls may follow the mint before the upload runs.
7. **Upload.**
   - Source is already a `.zip` → `upload-artifact.sh --src <file>.zip ...`
   - Source is a folder → `zip-and-upload-artifact.sh --src <folder> ...` (fall back to `upload-artifact.sh` per-file multipart only if zipping fails)
   - Always pass explicitly: `--type`, `--identifier`, `--description`, `--privacy`, `--status`, and `--entry-point` for websites. Never rely on script defaults — `--type` in particular defaults to `website`, and `type` is immutable after create, so a storage bundle uploaded without it can only be fixed by delete-and-recreate.
8. **Record and report.** Update the registry (uuid, identifier, description, type, privacy, status, url). Then ALWAYS report the link:
   - Published + public → `Public — anyone with the link can view: <siteUrl>` (website) or `<base>/download/<uuid>` (storage)
   - Workspace tier → the `siteUrl` (teammates verify their work email once) plus `Preview: <previewUrl>` from the upload output's `preview:` line
   - Only me or unpublished → `Preview (you + workspace members): <previewUrl>` from the upload output's `preview:` line, and **offer a share link now** for anyone else (see Shares workflow)

**The Exact Publish Sequence** — the ENTIRE publish is these actions and nothing else:

```
1. assets_list                    ← MCP tool call (Cache Rule)
2. AskUserQuestion (identifier)   ← offer suggestion + alternates
3. AskUserQuestion (privacy)      ← workspace (recommended) | public | only_me
4. asset_generate_access_token    ← MCP tool call; capture accessToken from the result
5. ONE bash command               ← ARTIFACTS_ACCESS_TOKEN='<accessToken>' \
                                      bash "${CLAUDE_PLUGIN_ROOT:-.}"/skills/asset-manager/scripts/zip-and-upload-artifact.sh \
                                      --src … --type … --identifier … --description … --privacy … --status published [--entry-point …]
6. Update the registry, report the link
```

A publish that creates more than one asset, or runs any script outside the bundled four, is off the rails — stop and restart from this sequence. (The documented recoveries are NOT off the rails: the `zip → upload-artifact.sh` per-file fallback when zipping fails, and a single 401/502 retry, each stay within this one publish.)

## Workflow: Update an Asset's Files

1. Resolve the asset (registry first; `asset_get_by_id` / `assets_list` if unsure).
2. **Warn: full replace.** Files not included in `--src` are pruned from the asset's current file set. The previous set survives as a restorable version (see Versions & Rollback), but the live URL changes immediately — confirm with the user if the source folder looks partial.
3. Mint token, then: `update-artifact.sh --uuid <uuid> --src <folder-or-zip> --note "<what changed>"`. Every file update mints an immutable version and `--note` is its changelog line — always pass one (sanitized like the other metadata flags: no `"` or `\`).
4. Update the registry (`updated` date, any changed url) and report.

## Workflow: Versions & Rollback

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
- **When flipping to `public`**, mention existing share links keep working but are no longer needed.

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

Two reads answer "how is my asset doing" — available to the owner and to workspace admins/owners (anyone whose `canManage` is true for the asset). Pick by the question:

- **How many** → `asset_stats_get`: per-day unique visit and download counts. Trends, not names.
- **Who** → `asset_visitors_list`: the identified viewers — share recipients who code-verified (`via: share`) and workspace members who verified their work email (`via: workspace`).

Anonymous public visitors are **counted in stats but never identified** — never imply the visitor list is complete for a `public` asset. The honest phrasing: "N visits, of which these verified viewers: …".

## Workflow: Transfer Ownership

`asset_transfer` (uuid + `targetUserOId`) reassigns an asset to another member of its workspace. Use it when an asset should outlive its author's involvement: handing a deck to the teammate now running the campaign, adopting a departed colleague's asset, or claiming a machine-published asset (e.g. an auto-captured brand kit) so a human owns it.

1. Allowed when you own the asset, or its `canManage` reads true (workspace admin/owner, non-`only_me`).
2. The target is an Octave user oId; they must have used assets at least once (the tool returns a clear error otherwise — have them open the asset gallery or run any asset call, then retry).
3. Versions and share links ride along unchanged; the previous owner keeps whatever access the privacy tier grants everyone else.
4. Update the registry (`owner` changes; your own registry entry may now belong to someone else — note it rather than delete it) and report the asset's link.

Note: offboarding is automatic — when a member is removed from the workspace, their assets (all tiers, including `only_me`) transfer to a workspace owner. Manual transfer is for everything short of that.

## Workflow: Download / List / Delete

- **Download**: mint token, then `download-artifact.sh --uuid <uuid> --out <parent-dir>` — files always land in `<parent-dir>/<identifier>/`. Works for any asset the user owns or any non-only_me asset in their workspace, regardless of status/privacy. Add `--version <N>` for a historical version's files (see Versions & Rollback).
- **List**: "what assets are available / do we have X?" → run a fresh `assets_list` and show EVERY asset with its identifier, owner ("me" vs teammate), and link — no row without a link: published + public → the public URL ("anyone with the link"); everything else → the `previewUrl` from that same list response. Reconcile the registry while you're at it. The registry alone is only enough for quick recall of what was published from this project.
- **Delete**: `asset_delete` — irreversible, deletes the files too. Always confirm with the user first. Then remove the entry from the registry.

## Error Handling

| Signal | Meaning | Action |
|--------|---------|--------|
| 401 from a script | Token rotated or expired | `asset_refresh_access_token`, retry the script once |
| 409 `identifier_conflict` | Identifier already used by one of the user's assets | Ask: rename (suggest a variant) vs update the existing asset's files instead |
| 409 on `vanitySlug` | Slug already taken in the workspace | Pick another slug (suggest a variant), retry `asset_update` |
| 409 from `asset_access_request_grant` | Request already granted | Nothing to mint — find the existing share via `asset_shares_list`; if its URL is lost, revoke and re-create |
| 400 from `asset_version_delete` | Tried to delete the CURRENT version | The served version is undeletable — restore a different version first, or leave it |
| 502 `storage_upload_failed` | Transient storage error | Retry once, then report |
| Connection refused / DNS failure | Wrong base URL or backend not running | Re-check the base URL cascade; ask the user |
| 404 on a known uuid | Deleted outside this skill | Reconcile the registry, tell the user |

## Memory Registry

Persistent registry shared with the `asset-manager` agent, at:

```
<project root>/.claude/agent-memory/asset-manager/MEMORY.md
```

This is the `.claude` directory of the **current project** (where you are working) — **NEVER `~/.claude/...` in the home directory**. Before creating a registry anywhere, READ the project path first: if it exists, use it — it may already hold published assets and the token prefix. Never maintain two registries. Create it (and parent directories) only when the project path genuinely has none. Format:

```markdown
# Asset Registry
base_url: https://link.octavehq.com
token: prefix=atk_7f3c expires=2026-08-06
last_reconciled: 2026-07-07

## Assets
### <identifier> (<uuid>)
- type: website — status/privacy: published/workspace
- owner: me
- url: <siteUrl | <base>/download/<uuid> | (non-public — fetch a fresh previewUrl via asset_get_by_id)>
- vanity: <vanityUrl — omit when no slug is set>
- description: <one line>
- updated: <YYYY-MM-DD>
- shares:
  - <shareUuid> | url: <one-time share url> | expires: <date|never> | emails: a@x.com | domains: y.com
```

**Update rules:**

- After EVERY successful mutation (upload, file update, metadata change, vanity slug change, share create/add/remove/revoke, access-request grant/dismiss, version restore/delete, delete, token mint) update the registry in the same turn, before the user-facing report.
- Store only the token `prefix` + `expiresAt` — never the plaintext token.
- The share `url` (from `asset_share_create` or `asset_access_request_grant`) exists nowhere else after creation — losing it means revoking and re-creating the share.
- Never store `previewUrl` — it is short-lived and minted per read; fetch a fresh one with `asset_get_by_id` when needed.
- The registry is a **local, per-project cache** — assets created from other projects or sessions won't be in it. It is never sufficient for the Cache Rule's dedup check; that always uses a fresh `assets_list`.

**Reconciliation:**

- Answer read questions ("what have I published?") from the registry.
- Run `assets_list` and reconcile when: `last_reconciled` is more than 7 days old, a tool result contradicts the registry, or a known uuid returns 404.
- Reconcile = add assets missing from the registry, drop entries missing from the API (note "deleted outside this skill"), refresh status/privacy/url, bump `last_reconciled`.
- A share found via `asset_shares_list` with no url in the registry → mark `url: lost — revoke and re-create to get a new link`.

## Output Style

- Always end a publish/share operation by presenting the working URL plus a one-line summary of identifier, privacy, and status. Label public links `Public — anyone with the link can view`; label workspace links `Workspace — teammates verify their work email once`; for only_me/unpublished assets give the fresh `previewUrl` instead.
- When an asset has a `vanityUrl`, show it alongside the canonical link labeled `Vanity:` — it is the memorable one to hand out.
- Report every assumption made (e.g. auto-detected entry point) so the user can correct it.
