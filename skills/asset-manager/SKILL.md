---
name: asset-manager
description: Publish and manage hosted assets (HTML sites, docs, file bundles) on the Octave assets service - upload, visibility, private share links, and a persistent registry of everything published. Acts as a cache - always checks the asset store for an existing match before creating anything new, so the same work is never done twice. Use when the user says "publish this", "host this html", "share this with the team / with an email", "make it public/private", "who has access to", "update the published site", "list my published assets", "what assets are available", "is there already a ... published", "do we have a ...", or wants a shareable URL for something they built locally. Do NOT use for Vercel microsite deploys (use /octave:microsite deploy) or for generating the content itself (use the Document Builder skills).
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

## Check Before Create (Cache Rule)

The asset store doubles as a cache: the asset the user wants may already exist (created in another project, another session — or, as scoping widens, by a teammate). **Never create a new asset without checking first.**

Before ANY new upload:

1. Run a **fresh `assets_list`**. Never trust the local registry alone for this — it is per-project and lags behind assets created elsewhere.
2. Match the intended asset against existing ones: normalize identifiers (kebab-case → words) and compare against the intended name/topic keywords; scan descriptions; weigh `type` (website vs storage).
3. **Plausible matches found** → AskUserQuestion with up to 3 candidates. Each option shows the identifier, and its description says what it is plus the link (siteUrl, download URL, or "private — share required"). Always include a final option: `No — this is new, create it`.
   - User picks a match → show its link, then ask what next: nothing / update its files / change metadata / manage shares.
   - User says it's new → proceed to publish, choosing an identifier distinct from the matches (avoids a 409).
4. **No match** → proceed directly, mentioning that nothing similar was found.

Ordering constraint: `assets_list` is an MCP asset call and **rotates the access token** — always do this check BEFORE minting the upload token.

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

Script invocation form (inline env only — never `export` into the profile, never echo the token, never write it to any file):

```bash
ARTIFACTS_ACCESS_TOKEN='<token>' ARTIFACTS_URL='<base_url>' \
  bash "${CLAUDE_PLUGIN_ROOT:-.}"/skills/asset-manager/scripts/<script>.sh <flags>
```

In the registry, record only the token `prefix` and `expiresAt` — **never the plaintext token**.

## Base URL Resolution

Resolve `<base_url>` in this order:

1. `$ARTIFACTS_URL` already set in the environment → use it.
2. `base_url` recorded in the registry (see Memory Registry below).
3. Default: `http://localhost:3015` (current dev setup; when the service moves to production, update `base_url` in the registry — nothing else changes).

Always pass `ARTIFACTS_URL` explicitly to scripts.

## The Bundled Scripts

All in `${CLAUDE_PLUGIN_ROOT:-.}/skills/asset-manager/scripts/` (bash + curl; jq optional; works on macOS/Linux/Windows via Git Bash or WSL):

| Script | Purpose | Key flags |
|--------|---------|-----------|
| `zip-and-upload-artifact.sh` | Zip a folder locally, upload as one request (default for folders; zip fallback chain: zip → powershell → python) | `--src <folder> --identifier --description --type --visibility --status --entry-point` |
| `upload-artifact.sh` | Upload a ready `.zip`, or a folder as per-file multipart (fallback if zipping fails; skips dotfiles) | same as above, `--src` accepts folder or `.zip` |
| `update-artifact.sh` | Replace an asset's files (FULL REPLACE) | `--uuid <u> --src <path>` |
| `download-artifact.sh` | Download all files of an owned asset | `--uuid <u> --out <dir>` |

Script gotcha: metadata values are interpolated into JSON **without escaping** — `--identifier` and `--description` values must contain no double quotes or backslashes. If the description needs them, upload with a plain placeholder and set the real text afterward via `asset_update` (which is JSON-safe).

## Workflow: Publish a New Asset

1. **Identify the source.** Confirm the path exists. Classify:
   - Contains HTML → `--type website`. Determine the entry point (default `index.html`; if the main file has another name, pass `--entry-point <file>`).
   - Loose files / binaries / docs meant for download, not viewing → `--type storage` (no entry point; delivered via `/download/<uuid>`, never served as a site).
2. **Check for existing work — apply the Cache Rule** (see above). If the user confirms an existing asset is what they meant, switch to that asset (show link, then update/share/etc.) instead of publishing. Only continue here once it's confirmed new.
3. **Suggest an identifier.** The identifier is user-facing — it appears in the public URL `<base_url>/sites/<identifier>-<uuid>/`. Heuristics:
   - kebab-case, lowercase, ≤50 chars, no quotes/backslashes
   - Prefer the HTML `<title>` or H1 if meaningful; else the source folder basename
   - Strip dates, `tmp`/`final`/`v2` noise suffixes
   - Must not collide with existing identifiers — reuse the `assets_list` result from step 2 (no second call); identifiers are unique per user
4. **Ask the user** (AskUserQuestion, one question at a time):
   - Identifier: offer your suggestion first (`<suggestion> (Recommended)`), 1-2 sensible alternates; the user can always type their own via Other.
   - Visibility: `Public` ("Anyone with the URL can view") vs `Private` ("Only people you share a link with").
5. **Draft the description.** 1-2 sentences saying what the asset is and who it's for (e.g. "Interactive use-case explorer for Acme's platform, built for the Q3 ABM campaign"). Sanitize for the script (no `"` or `\`).
6. **Mint the token** (`asset_generate_access_token`) and resolve the base URL. Do this AFTER steps 1-5 — the step-2 `assets_list` already rotated any earlier token, and no MCP asset calls may follow the mint before the upload runs.
7. **Upload.**
   - Source is already a `.zip` → `upload-artifact.sh --src <file>.zip ...`
   - Source is a folder → `zip-and-upload-artifact.sh --src <folder> ...` (fall back to `upload-artifact.sh` per-file multipart only if zipping fails)
   - Always pass explicitly: `--identifier`, `--description`, `--visibility`, `--status published`, and `--entry-point` for websites. Never rely on script defaults.
8. **Record and report.** Update the registry (uuid, identifier, description, type, visibility, status, url). Then report:
   - Public website → the live `siteUrl`
   - Private → explain the URL will 404 for others until they get a share link, and **offer to create one now** (see Shares workflow)
   - Storage → the `/download/<uuid>` link (public) or share-link note (private)

## Workflow: Update an Asset's Files

1. Resolve the asset (registry first; `asset_get_by_id` / `assets_list` if unsure).
2. **Warn: full replace.** Files not included in `--src` are pruned from the asset. Confirm with the user if the source folder looks partial.
3. Mint token, then: `update-artifact.sh --uuid <uuid> --src <folder-or-zip>`.
4. Update the registry (`updated` date, any changed url) and report.

## Workflow: Metadata & Visibility (MCP only)

For identifier, description, entry point, visibility, or status changes use `asset_update` (`type` is immutable). Notes:

- Changing the identifier changes the public URL — tell the user the old link breaks.
- Status: `draft` and `archived` are never served; `published` is the live state.
- **When flipping visibility to `private`**, proactively ask: "The public URL will stop working for others. Want to create a share link so specific people keep access?" If yes → Shares workflow.
- **When flipping to `public`**, mention existing share links keep working but are no longer needed.

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

- **Download**: mint token, then `download-artifact.sh --uuid <uuid> --out <dir>` (works for any owned asset regardless of status/visibility).
- **List**: "what assets are available / do we have X?" → run a fresh `assets_list`, show the results with links, and reconcile the registry while you're at it. The registry alone is only enough for quick recall of what was published from this project.
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
.claude/agent-memory/asset-manager/MEMORY.md
```

Create it (and parent directories) on first use. Format:

```markdown
# Asset Registry
base_url: http://localhost:3015
token: prefix=atk_7f3c expires=2026-08-06
last_reconciled: 2026-07-07

## Assets
### <identifier> (<uuid>)
- type: website — status/visibility: published/private
- url: <siteUrl | <base>/download/<uuid> | (private — share required)>
- description: <one line>
- updated: <YYYY-MM-DD>
- shares:
  - <shareUuid> | url: <one-time share url> | expires: <date|never> | emails: a@x.com | domains: y.com
```

**Update rules:**

- After EVERY successful mutation (upload, file update, metadata change, share create/add/remove/revoke, delete, token mint) update the registry in the same turn, before the user-facing report.
- Store only the token `prefix` + `expiresAt` — never the plaintext token.
- The share `url` exists nowhere else after creation — losing it means revoking and re-creating the share.
- The registry is a **local, per-project cache** — assets created from other projects or sessions won't be in it. It is never sufficient for the Cache Rule's dedup check; that always uses a fresh `assets_list`.

**Reconciliation:**

- Answer read questions ("what have I published?") from the registry.
- Run `assets_list` and reconcile when: `last_reconciled` is more than 7 days old, a tool result contradicts the registry, or a known uuid returns 404.
- Reconcile = add assets missing from the registry, drop entries missing from the API (note "deleted outside this skill"), refresh status/visibility/url, bump `last_reconciled`.
- A share found via `asset_shares_list` with no url in the registry → mark `url: lost — revoke and re-create to get a new link`.

## Output Style

- Always end a publish/share operation by presenting the working URL (or the explicit reason there isn't one yet) plus a one-line summary of identifier, visibility, and status.
- Report every assumption made (e.g. auto-detected entry point) so the user can correct it.
