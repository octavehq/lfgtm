#!/usr/bin/env bash
# Zip a site folder and upload it as a new artifact in a single zip part.
# Falls back through zip -> PowerShell -> Python so it works on macOS, Linux,
# and Windows (Git Bash) without extra tooling.
#
# Usage:
#   ARTIFACTS_ACCESS_TOKEN=<token> ./zip-and-upload-artifact.sh --src /path/to/artifact
#   ARTIFACTS_ACCESS_TOKEN=<token> ./zip-and-upload-artifact.sh --src ./site \
#     --type storage --privacy public --identifier docs
#
# Flags:
#   --src <folder>        (required) site folder to zip and upload
#   --type <t>            website | storage        (default: website)
#   --privacy <p>         only_me | workspace | public  (default: workspace)
#                         One ladder: only_me = owner only; workspace = owner +
#                         workspace members (the default); public = anyone with
#                         the URL. External people get access via share links
#                         on any non-public asset.
#   --status <s>          published | unpublished  (default: published)
#   --identifier <id>     artifact identifier      (default: --src basename)
#   --description <d>     description              (default: "Uploaded via curl-templates")
#   --entry-point <path>  entry point (website only; sent only when set)
#   -h, --help            show this help
#
# Auth / environment (the access token is env-only):
#   ARTIFACTS_ACCESS_TOKEN  (required) per-user access token — mint one via
#                           POST /api/v1/user/access-token
#   ARTIFACTS_URL           base URL of the server (default: https://link.octavehq.com;
#                           dev override: ARTIFACTS_URL=... in a plugin-root .env)
set -euo pipefail

# Base URL: ARTIFACTS_URL env > plugin-root .env (development) > production default.
# Marketplace installs never ship a .env (gitignored), so they always use production.
if [[ -z "${ARTIFACTS_URL:-}" ]]; then
  ENV_FILE="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)/.env"
  if [[ -f "$ENV_FILE" ]]; then
    ARTIFACTS_URL="$(grep -E '^ARTIFACTS_URL=' "$ENV_FILE" | tail -1 | cut -d= -f2- | tr -d "\"' \r" || true)"
  fi
fi
BASE_URL="${ARTIFACTS_URL:-https://link.octavehq.com}"
TOKEN="${ARTIFACTS_ACCESS_TOKEN:-}"

usage() {
  # Reuse the header comment block above as the single source of help text.
  awk 'NR==1 { next } /^#/ { sub(/^# ?/, ""); print; next } { exit }' "$0" >&2
}

# Defaults (all overridable by flags).
SRC=""
TYPE="website"
PRIVACY="workspace"
STATUS="published"
IDENTIFIER=""
DESCRIPTION="Uploaded via curl-templates"
ENTRY_POINT=""

while [ $# -gt 0 ]; do
  case "$1" in
    --src)         SRC="${2:?--src requires a value}"; shift 2 ;;
    --type)        TYPE="${2:?--type requires a value}"; shift 2 ;;
    --privacy)     PRIVACY="${2:?--privacy requires a value}"; shift 2 ;;
    --status)      STATUS="${2:?--status requires a value}"; shift 2 ;;
    --identifier)  IDENTIFIER="${2:?--identifier requires a value}"; shift 2 ;;
    --description) DESCRIPTION="${2:?--description requires a value}"; shift 2 ;;
    --entry-point) ENTRY_POINT="${2:?--entry-point requires a value}"; shift 2 ;;
    -h|--help)     usage; exit 0 ;;
    *) echo "error: unexpected argument: $1" >&2; usage; exit 1 ;;
  esac
done

if [ -z "$SRC" ]; then
  echo "error: --src is required (a folder to zip)" >&2
  usage
  exit 1
fi
SRC="${SRC%/}"
if [ ! -d "$SRC" ]; then
  echo "error: --src $SRC is not a directory" >&2
  exit 1
fi

if [ -z "$TOKEN" ]; then
  echo "error: no access token — set ARTIFACTS_ACCESS_TOKEN" >&2
  echo "hint: mint one via the asset_generate_access_token MCP tool, then pass it inline:" >&2
  echo "      ARTIFACTS_ACCESS_TOKEN='<token>' $0 ..." >&2
  echo "      (Do NOT curl /api/v1/user/access-token — that needs a service key the" >&2
  echo "       asset-manager skill does not have.)" >&2
  exit 1
fi

# Fail fast on typo'd enums (the server validates too, but this saves a round-trip).
case "$TYPE" in website | storage) ;; *) echo "error: --type must be website|storage" >&2; exit 1 ;; esac
case "$PRIVACY" in only_me | workspace | public) ;; *) echo "error: --privacy must be only_me|workspace|public" >&2; exit 1 ;; esac
case "$STATUS" in published | unpublished) ;; *) echo "error: --status must be published|unpublished" >&2; exit 1 ;; esac

NAME=$(basename "$SRC")
IDENTIFIER="${IDENTIFIER:-$NAME}"

# These string fields are interpolated into the metadata JSON without escaping.
# A `"` or `\` in any of them would break the JSON — and because entryPoint is
# appended last, a crafted value there can inject overriding keys (e.g.
# `...","privacy":"public`) that silently defeat --privacy/--status. Reject
# rather than try to escape. (--identifier defaults to the folder basename, which
# can legally contain these, so this must run after the default is applied.)
for _field in "identifier=$IDENTIFIER" "description=$DESCRIPTION" "entry-point=$ENTRY_POINT"; do
  case "${_field#*=}" in
    *\"* | *\\*)
      echo "error: --${_field%%=*} must not contain double quotes or backslashes" >&2
      exit 1
      ;;
  esac
done

METADATA=$(printf '{"identifier":"%s","description":"%s","type":"%s","privacy":"%s","status":"%s"' \
  "$IDENTIFIER" "$DESCRIPTION" "$TYPE" "$PRIVACY" "$STATUS")
# entryPoint is website-only; storage artifacts ignore it.
if [ "$TYPE" = "website" ] && [ -n "$ENTRY_POINT" ]; then
  METADATA="$METADATA,\"entryPoint\":\"$ENTRY_POINT\""
fi
METADATA="$METADATA}"

TMP_ZIP="${TMPDIR:-/tmp}/artifact-$NAME-$$.zip"
STAGE_DIR="${TMPDIR:-/tmp}/artifact-stage-$NAME-$$"
RESP_FILE="$(mktemp)"
trap 'rm -rf "$STAGE_DIR"; rm -f "$TMP_ZIP" "$RESP_FILE"' EXIT

# Stage a clean copy containing only the non-dotfile files, preserving structure.
# Two reasons: (1) the server rejects any dotfile path segment, and the three zip
# backends below differ in whether they exclude dotfiles (zip's -x does; python's
# `./*` and PowerShell's Compress-Archive do NOT), so zipping the staged copy
# makes every backend upload the exact same, server-valid file set; (2) it gives
# a single empty-folder guard, so we never silently upload a zero-file zip.
rm -rf "$STAGE_DIR"
FILE_COUNT=0
while IFS= read -r FILE; do
  REL="${FILE#"$SRC"/}"
  mkdir -p "$STAGE_DIR/$(dirname "$REL")"
  cp "$FILE" "$STAGE_DIR/$REL"
  FILE_COUNT=$((FILE_COUNT + 1))
done < <(find "$SRC" -type f ! -path '*/.*' ! -name '.*' | sort)
if [ "$FILE_COUNT" -eq 0 ]; then
  echo "error: no files found under $SRC (dotfiles are skipped)" >&2
  exit 1
fi

# Zip the staged copy (already dotfile-free) with the first available backend.
if command -v zip >/dev/null 2>&1; then
  (cd "$STAGE_DIR" && zip -r -q "$TMP_ZIP" .)
elif command -v powershell.exe >/dev/null 2>&1; then
  # Windows Git Bash: cygpath converts POSIX paths for PowerShell. Single quotes
  # in the path are doubled so they can't break out of the PowerShell string.
  WIN_SRC=$(cygpath -w "$STAGE_DIR")
  WIN_ZIP=$(cygpath -w "$TMP_ZIP")
  WIN_SRC_ESC=${WIN_SRC//\'/\'\'}
  WIN_ZIP_ESC=${WIN_ZIP//\'/\'\'}
  powershell.exe -NoProfile -Command \
    "Compress-Archive -Path '$WIN_SRC_ESC\\*' -DestinationPath '$WIN_ZIP_ESC' -Force"
elif command -v python3 >/dev/null 2>&1 || command -v python >/dev/null 2>&1; then
  PY=$(command -v python3 || command -v python)
  (cd "$STAGE_DIR" && "$PY" -m zipfile -c "$TMP_ZIP" ./*)
else
  echo "error: need one of: zip, powershell.exe, python3/python to create a zip" >&2
  exit 1
fi

SIZE=$(wc -c <"$TMP_ZIP" | tr -d ' ')
echo "zipped $SRC/ -> $SIZE bytes, uploading as \"$IDENTIFIER\""

HTTP_CODE=$(curl -sS -o "$RESP_FILE" -w "%{http_code}" \
  -X POST "$BASE_URL/api/v1/artifacts" \
  -H "Authorization: Bearer $TOKEN" \
  -F "metadata=$METADATA" \
  -F "site=@$TMP_ZIP;type=application/zip")

if [ "$HTTP_CODE" != "201" ]; then
  echo "error: POST /api/v1/artifacts -> $HTTP_CODE" >&2
  cat "$RESP_FILE" >&2
  echo >&2
  exit 1
fi

if command -v jq >/dev/null 2>&1; then
  jq . "$RESP_FILE"
  UUID=$(jq -r '.uuid' "$RESP_FILE")
  PREVIEW_URL=$(jq -r '.previewUrl // empty' "$RESP_FILE")
else
  cat "$RESP_FILE"
  echo
  UUID=$(grep -o '"uuid":"[^"]*"' "$RESP_FILE" | head -1 | sed -e 's/^"uuid":"//' -e 's/"$//')
  # previewUrl is a string for any non-public artifact (only_me, workspace, or
  # unpublished); it is JSON null (→ no match) only once published + public.
  PREVIEW_URL=$(grep -o '"previewUrl":"[^"]*"' "$RESP_FILE" | head -1 | sed -e 's/^"previewUrl":"//' -e 's/"$//')
fi

echo
echo "created: $UUID"
if [ "$PRIVACY" != "public" ] || [ "$STATUS" != "published" ]; then
  echo "note:     not public. To open it to anyone with the URL, set" >&2
  echo "          privacy=public via the asset_update MCP tool." >&2
fi
if [ "$TYPE" = "storage" ]; then
  echo "download: $BASE_URL/download/$UUID"
else
  echo "serve:    $BASE_URL/sites/$IDENTIFIER-$UUID/"
fi
# Non-public artifacts (only_me, workspace, or unpublished) return a tokenized
# preview link (owner + same workspace) that renders without making them public.
if [ -n "${PREVIEW_URL:-}" ]; then
  echo "preview:  $PREVIEW_URL"
fi
# Owner download (any status/privacy), names the folder after the identifier.
echo "fetch:    ./download-artifact.sh --uuid $UUID"
