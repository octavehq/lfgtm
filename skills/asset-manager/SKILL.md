---
name: asset-manager
description: Publish and manage hosted assets (HTML sites, docs, file bundles) on the Octave assets service - upload, visibility, private share links, and a persistent registry of everything published. Acts as a cache - always checks the asset store for an existing match before creating anything new, so the same work is never done twice. Use when the user says "publish this", "host this html", "store these files" (storage type), "share this with the team / workspace / with an email", "make it public/private", "who has access to", "update the published site", "list my published assets", "what assets are available", "is there already a ... published", "do we have a ...", or wants a shareable URL for something they built locally. Do NOT use for Vercel deploys of microsites (that is /octave:microsite's own deploy step) or for generating the content itself (use the Document Builder skills).
---

# /octave:asset-manager - Publish & Manage Hosted Assets

Manage the full lifecycle of hosted assets on the Octave assets service: upload local sources (HTML sites, markdown, file bundles), control visibility, create and manage private share links, and keep a persistent registry of everything published.

## Usage

```
/octave:asset-manager                       # Interactive - asks what to do
/octave:asset-manager publish <path>        # Publish a folder, file, or .zip
/octave:asset-manager update <identifier>   # Replace files or change metadata
/octave:asset-manager share <identifier>    # Create/manage share links
/octave:asset-manager list                  # List published assets (from registry)
/octave:asset-manager download <identifier> # Download an asset's files locally
/octave:asset-manager delete <identifier>   # Delete an asset (confirms first)
```

## The One Decision Rule

Every operation routes through exactly one of two backends. Never mix them up:

| Operation | Route |
|-----------|-------|
| Upload new files, replace files, download files | Bash scripts in `${CLAUDE_PLUGIN_ROOT:-.}/skills/asset-manager/scripts/` |
| Everything else: metadata, status, visibility, shares, tokens, listing | MCP `asset_*` / `assets_list` tools |

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
3. **Plausible matches found** → AskUserQuestion with up to 3 candidates. Each option shows the identifier, and its description says what it is, **who owns it** (`owner`: "me" or a teammate's name), plus the link (siteUrl, previewUrl for non-public, or download URL). Always include a final option: `No — this is new, create it`. A teammate-owned match can be reused and downloaded, but never modified — to change one, create the user's own copy.
   - User picks a match → show its link, then ask what next: nothing / update its files / change metadata / manage shares.
   - User says it's new → proceed to publish, choosing an identifier distinct from the matches (avoids a 409).
4. **No match** → proceed directly, mentioning that nothing similar was found.

Ordering constraint: `assets_list` is an MCP asset call and **rotates the access token** — always do this check BEFORE minting the upload token.

## Workspace Sharing & Preview Links

Assets are **shared with the workspace by default** (`shareWithWorkspace`, default `true` at create): teammates can READ them through the API (list/get/download) — even private or draft ones. All mutations and share management stay owner-only.

- Every asset response carries `owner`: `"me"` for your own, otherwise the teammate's `"First Last <email>"`. **Teammate-owned assets are read-only** — never call `asset_update`, `asset_delete`, or any share tool on them; if the user wants changes, create their own copy.
- Non-public assets (private, draft, or archived) carry a **`previewUrl`**: a tokenized link that renders the site/download for the owner and workspace members without making it public. It is `null` once the asset is published + public (use `siteUrl` then). It is **short-lived and minted per read — NEVER store it in the registry**; fetch a fresh one with `asset_get_by_id` when someone needs it.
- **Always include the link.** Every time you list, upload, update, or otherwise mention an asset, include its link:
  - published + public → `Public — anyone with the link can view: <siteUrl>` (websites) or `<base>/download/<uuid>` (storage)
  - private, draft, or archived → `Preview (you + workspace members): <previewUrl>` — taken fresh from the response in hand (list/get) or the script's `preview:` output line, never from the registry. Add a share link for people outside the workspace when relevant.

## MCP Server Detection

Refer to tools by bare name (`asset_update`, `assets_list`, ...). The live server is named `mcp__octave-<workspace>__*` — the workspace suffix varies per user. Detect the active Octave MCP server from the available tool list; never hardcode a prefix.

Available asset tools: `asset_generate_access_token`, `asset_refresh_access_token`, `assets_list`, `asset_get_by_id`, `asset_update`, `asset_delete`, `asset_share_create`, `asset_shares_list`, `asset_share_revoke`, `asset_share_add_recipients`, `asset_share_remove_recipients`, `asset_share_add_domains`, `asset_share_remove_domains`.

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
| `zip-and-upload-artifact.sh` | Zip a folder locally, upload as one request (default for folders; zip fallback chain: zip → powershell → python) | `--src <folder> --identifier --description --type --visibility --status --share-workspace --entry-point` |
| `upload-artifact.sh` | Upload a ready `.zip`, or a folder as per-file multipart (fallback if zipping fails; skips dotfiles) | same as above, `--src` accepts folder or `.zip` |
| `update-artifact.sh` | Replace an asset's files (FULL REPLACE) | `--uuid <u> --src <path>` |
| `download-artifact.sh` | Download all files of an owned or workspace-shared asset | `--uuid <u> --out <parent-dir>` — files always land in `<parent-dir>/<identifier>/` |

Script gotcha: metadata values are interpolated into JSON **without escaping** — `--identifier`, `--description`, and `--entry-point` values must contain no double quotes or backslashes (the scripts now reject them rather than corrupt the payload). If the description needs them, upload with a plain placeholder and set the real text afterward via `asset_update` (which is JSON-safe).

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
   - Second — one call with three questions:
     - Visibility: `Public` ("Anyone with the URL can view") vs `Private` ("Only via share links; workspace members via preview").
     - Workspace sharing: `Share with workspace (Recommended)` ("Teammates can find and reuse it — this is what makes the asset cache work") vs `Owner-only`.
     - Status: `published (Recommended)` vs `draft` ("Uploaded but not served yet"). `archived` also exists — set later via `asset_update`.
5. **Draft the description.** 1-2 sentences saying what the asset is and who it's for (e.g. "Interactive use-case explorer for Acme's platform, built for the Q3 ABM campaign"). Sanitize for the script (no `"` or `\`).
6. **Mint the token** (`asset_generate_access_token`) and resolve the base URL. Do this AFTER steps 1-5 — the step-2 `assets_list` already rotated any earlier token, and no MCP asset calls may follow the mint before the upload runs.
7. **Upload.**
   - Source is already a `.zip` → `upload-artifact.sh --src <file>.zip ...`
   - Source is a folder → `zip-and-upload-artifact.sh --src <folder> ...` (fall back to `upload-artifact.sh` per-file multipart only if zipping fails)
   - Always pass explicitly: `--type`, `--identifier`, `--description`, `--visibility`, `--status`, `--share-workspace`, and `--entry-point` for websites. Never rely on script defaults — `--type` in particular defaults to `website`, and `type` is immutable after create, so a storage bundle uploaded without it can only be fixed by delete-and-recreate.
8. **Record and report.** Update the registry (uuid, identifier, description, type, visibility, status, workspace sharing, url). Then ALWAYS report the link:
   - Published + public → `Public — anyone with the link can view: <siteUrl>` (website) or `<base>/download/<uuid>` (storage)
   - Private, draft, or archived → `Preview (you + workspace members): <previewUrl>` from the upload output's `preview:` line, and **offer a share link now** for people outside the workspace (see Shares workflow)

**The Exact Publish Sequence** — the ENTIRE publish is these actions and nothing else:

```
1. assets_list                    ← MCP tool call (Cache Rule)
2. AskUserQuestion (identifier)   ← offer suggestion + alternates
3. AskUserQuestion (one call)     ← visibility + workspace sharing + status
4. asset_generate_access_token    ← MCP tool call; capture accessToken from the result
5. ONE bash command               ← ARTIFACTS_ACCESS_TOKEN='<accessToken>' \
                                      bash "${CLAUDE_PLUGIN_ROOT:-.}"/skills/asset-manager/scripts/zip-and-upload-artifact.sh \
                                      --src … --type … --identifier … --description … --visibility … --status … --share-workspace … [--entry-point …]
6. Update the registry, report the link
```

A publish that creates more than one asset, or runs any script outside the bundled four, is off the rails — stop and restart from this sequence. (The documented recoveries are NOT off the rails: the `zip → upload-artifact.sh` per-file fallback when zipping fails, and a single 401/502 retry, each stay within this one publish.)

## Workflow: Update an Asset's Files

1. Resolve the asset (registry first; `asset_get_by_id` / `assets_list` if unsure).
2. **Warn: full replace.** Files not included in `--src` are pruned from the asset. Confirm with the user if the source folder looks partial.
3. Mint token, then: `update-artifact.sh --uuid <uuid> --src <folder-or-zip>`.
4. Update the registry (`updated` date, any changed url) and report.

## Workflow: Metadata & Visibility (MCP only)

For identifier, description, entry point, visibility, or status changes use `asset_update` (`type` is immutable). Notes:

- Changing the identifier changes the public URL — tell the user the old link breaks.
- Status: `draft` and `archived` are never served; `published` is the live state.
- **When flipping visibility to `private`**, explain what private means, then ask who keeps access:
  1. The public URL stops working for everyone — a private asset is never globally reachable, even with the link.
  2. People **outside the workspace** need a share link and get access after validating their email.
  3. **Workspace members** keep access without a share link via the asset's `previewUrl` (as long as it stays workspace-shared).
  Then ask WHO to share with (emails and/or allowed domains) and HOW LONG (`expiresInDays`, or never) → Shares workflow. Report the fresh `previewUrl` for teammates alongside the share link.
- **When flipping to `public`**, mention existing share links keep working but are no longer needed.
- **Workspace sharing** (`shareWithWorkspace` on `asset_update`): toggles whether teammates can read the asset at all; turning it off also kills their preview access.

## Workflow: Shares (private assets)

Create a share:

1. Ask who gets access (AskUserQuestion): `Specific emails` / `Whole domains` ("everyone @company.com — avoids listing every address") / `Both`. Then collect the comma-separated emails and/or domains as free text.
2. Ask expiry: `Never expires` / `30 days` / `90 days` (maps to `expiresInDays: null | 30 | 90`; accepts 1-3650 via Other).
3. Call `asset_share_create` (uuid, expiresInDays, emails?, domains?). At least one email or domain is required.
4. **The response `url` is shown exactly once and can never be retrieved again.** Write it to the registry in the same turn, BEFORE replying to the user. Then give the user the share URL.

Manage existing shares (share uuids come from the registry or `asset_shares_list`):

- Add people: `asset_share_add_recipients` (emails) / `asset_share_add_domains` (domains)
- Remove people: `asset_share_remove_recipients` / `asset_share_remove_domains` — a share must keep ≥1 email or domain; to remove the last one, suggest `asset_share_revoke` instead
- Revoke: `asset_share_revoke` — confirm first (cuts off active viewer sessions immediately, irreversible)

Update the registry after every share mutation.

## Workflow: Download / List / Delete

- **Download**: mint token, then `download-artifact.sh --uuid <uuid> --out <parent-dir>` — files always land in `<parent-dir>/<identifier>/`. Works for any asset the user owns or a teammate workspace-shared, regardless of status/visibility.
- **List**: "what assets are available / do we have X?" → run a fresh `assets_list` and show EVERY asset with its identifier, owner ("me" vs teammate), and link — no row without a link: published + public → the public URL ("anyone with the link"); private/draft/archived → the `previewUrl` from that same list response. Reconcile the registry while you're at it. The registry alone is only enough for quick recall of what was published from this project.
- **Delete**: `asset_delete` — irreversible, deletes the files too. Always confirm with the user first. Then remove the entry from the registry.

## Error Handling

| Signal | Meaning | Action |
|--------|---------|--------|
| 401 from a script | Token rotated or expired | `asset_refresh_access_token`, retry the script once |
| 409 `identifier_conflict` | Identifier already used by one of the user's assets | Ask: rename (suggest a variant) vs update the existing asset's files instead |
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
- type: website — status/visibility: published/private
- workspace: shared — owner: me
- url: <siteUrl | <base>/download/<uuid> | (non-public — fetch a fresh previewUrl via asset_get_by_id)>
- description: <one line>
- updated: <YYYY-MM-DD>
- shares:
  - <shareUuid> | url: <one-time share url> | expires: <date|never> | emails: a@x.com | domains: y.com
```

**Update rules:**

- After EVERY successful mutation (upload, file update, metadata change, share create/add/remove/revoke, delete, token mint) update the registry in the same turn, before the user-facing report.
- Store only the token `prefix` + `expiresAt` — never the plaintext token.
- The share `url` exists nowhere else after creation — losing it means revoking and re-creating the share.
- Never store `previewUrl` — it is short-lived and minted per read; fetch a fresh one with `asset_get_by_id` when needed.
- The registry is a **local, per-project cache** — assets created from other projects or sessions won't be in it. It is never sufficient for the Cache Rule's dedup check; that always uses a fresh `assets_list`.

**Reconciliation:**

- Answer read questions ("what have I published?") from the registry.
- Run `assets_list` and reconcile when: `last_reconciled` is more than 7 days old, a tool result contradicts the registry, or a known uuid returns 404.
- Reconcile = add assets missing from the registry, drop entries missing from the API (note "deleted outside this skill"), refresh status/visibility/url, bump `last_reconciled`.
- A share found via `asset_shares_list` with no url in the registry → mark `url: lost — revoke and re-create to get a new link`.

## Output Style

- Always end a publish/share operation by presenting the working URL plus a one-line summary of identifier, visibility, and status. Label public links `Public — anyone with the link can view`; for private/draft/archived assets give the fresh `previewUrl` instead.
- Report every assumption made (e.g. auto-detected entry point) so the user can correct it.
