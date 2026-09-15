# Asset script usage

Use connected `asset_*`/`assets_list` tools as tool calls, never shell commands. Mint a fresh access token using the active supported tool immediately before the script batch. Keep the token in `ARTIFACTS_ACCESS_TOKEN` for the process only; no logging, registry or shell-profile storage. Resolve token expiry/rotation from the current contract; an authentication error permits refresh, but a write timeout/malformed success requires reconciliation first.

`ARTIFACTS_URL` explicitly selects the service base; default `https://link.octavehq.com`. Scripts do not source `.env` or arbitrary shell files. Reuse an explicitly selected environment. Python 3.10+ and curl are required; jq/zip/sips are not.

- `upload-artifact.sh` or `zip-and-upload-artifact.sh --src <folder-or-zip> --identifier <name> --description <text> --type website|storage --privacy only_me|workspace|public --status published|unpublished --entry-point index.html`
- `update-artifact.sh --uuid <returned-uuid> --src <folder-or-zip> [--expected-version N] [--note <version-note>]`; file replacement replaces the whole bundle. Metadata-only updates omit --src.
- `download-artifact.sh --uuid <returned-uuid> --out <parent> [--version N] [--overwrite]`. Current files use the service manifest. Historical bundles use .zip when identified as ZIP, otherwise .bin; inspect the returned content before choosing a more specific extension.

Public uploads (including updates of already-public artifacts) require `--manifest <approved-files.json>` containing an explicit array of bundle-relative paths. Public ZIP members must exactly match it. Keep source notes, raw evidence, private input and review outputs outside that manifest. Directory traversal and symlinks are rejected; dotfile filtering applies to members, not dotted ancestors. Metadata quotes and Unicode are serialized with JSON; no manual quote stripping.

Exit 0 means metadata/version/file-manifest readback passed; it is not an access or rendered-page test. Exit 3 means the write may have happened: reconcile by UUID/identifier, version and checksum before retrying. No blind retry. Updates snapshot and reread immediately before writing; this detects observed concurrent changes but is not an atomic compare-and-swap and cannot eliminate the remaining server race.

Verify the actual final URL, intended access and links before saying publication is verified. Keep access claims conservative until the service matrix is tested: owner, other workspace member, explicit share recipient and anonymous × only_me/workspace/public × published/unpublished. Existing share grants may have separate semantics; do not assume a privacy change revokes them.
