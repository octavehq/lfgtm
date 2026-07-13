#!/usr/bin/env bash
# Update an existing artifact: replace its files and/or patch its metadata
# (identifier, description, entry point, visibility, status).
#
# Usage:
#   # Replace the site AND switch the entry point, in one atomic request:
#   ARTIFACTS_ACCESS_TOKEN=<token> ./update-artifact.sh --uuid <uuid> \
#     --src /path/to/site --entry-point serve.html
#
#   # Metadata only (no upload) — e.g. make it private:
#   ARTIFACTS_ACCESS_TOKEN=<token> ./update-artifact.sh --uuid <uuid> \
#     --visibility private
#
# Flags:
#   --uuid <uuid>         (required) artifact to update
#   --src <path>          site folder or .zip to upload. FULL REPLACE — any file
#                         not included is pruned. Omit to change metadata only.
#   --identifier <id>     new identifier
#   --description <d>     new description
#   --entry-point <path>  new entry point (website only). Without --src the file
#                         must already exist in the artifact, or the site 404s.
#   --visibility <v>      public | private
#   --status <s>          draft | published | archived
#   --share-workspace <b> true | false — share/unshare with the workspace
#   -h, --help            show this help
#
# With --src the upload and any metadata flags are sent together as one atomic
# multipart request to POST /:uuid/files; without it, the metadata flags go as a
# JSON PATCH /:uuid. Pass at least --src or one metadata flag.
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

# Defaults — empty means "not provided" (every field here is optional).
UUID=""
SRC=""
IDENTIFIER=""
DESCRIPTION=""
ENTRY_POINT=""
VISIBILITY=""
STATUS=""
SHARE_WORKSPACE=""

while [ $# -gt 0 ]; do
  case "$1" in
    --uuid)        UUID="${2:?--uuid requires a value}"; shift 2 ;;
    --src)         SRC="${2:?--src requires a value}"; shift 2 ;;
    --identifier)  IDENTIFIER="${2:?--identifier requires a value}"; shift 2 ;;
    --description) DESCRIPTION="${2:?--description requires a value}"; shift 2 ;;
    --entry-point) ENTRY_POINT="${2:?--entry-point requires a value}"; shift 2 ;;
    --visibility)  VISIBILITY="${2:?--visibility requires a value}"; shift 2 ;;
    --status)      STATUS="${2:?--status requires a value}"; shift 2 ;;
    --share-workspace) SHARE_WORKSPACE="${2:?--share-workspace requires a value}"; shift 2 ;;
    -h|--help)     usage; exit 0 ;;
    *) echo "error: unexpected argument: $1" >&2; usage; exit 1 ;;
  esac
done

if [ -z "$UUID" ]; then
  echo "error: --uuid is required" >&2
  usage
  exit 1
fi
SRC="${SRC%/}"

if [ -z "$TOKEN" ]; then
  echo "error: no access token — set ARTIFACTS_ACCESS_TOKEN" >&2
  echo "hint: mint one via the asset_generate_access_token MCP tool, then pass it inline:" >&2
  echo "      ARTIFACTS_ACCESS_TOKEN='<token>' $0 ..." >&2
  echo "      (Do NOT curl /api/v1/user/access-token — that needs a service key the" >&2
  echo "       asset-manager skill does not have.)" >&2
  exit 1
fi

# Fail fast on typo'd enums (the server validates too, but this saves a round-trip).
if [ -n "$VISIBILITY" ]; then
  case "$VISIBILITY" in public | private) ;; *) echo "error: --visibility must be public|private" >&2; exit 1 ;; esac
fi
if [ -n "$STATUS" ]; then
  case "$STATUS" in draft | published | archived) ;; *) echo "error: --status must be draft|published|archived" >&2; exit 1 ;; esac
fi
if [ -n "$SHARE_WORKSPACE" ]; then
  case "$SHARE_WORKSPACE" in true | false) ;; *) echo "error: --share-workspace must be true|false" >&2; exit 1 ;; esac
fi

# Assemble a metadata patch from only the flags that were passed. Values are
# interpolated as-is, so reject embedded double quotes/backslashes: they would
# break the JSON, and (since entryPoint can be appended before visibility/status)
# a crafted value could inject overriding keys. Same guard as upload-artifact.sh.
for _field in "identifier=$IDENTIFIER" "description=$DESCRIPTION" "entry-point=$ENTRY_POINT"; do
  case "${_field#*=}" in
    *\"* | *\\*)
      echo "error: --${_field%%=*} must not contain double quotes or backslashes" >&2
      exit 1
      ;;
  esac
done

META_PARTS=()
if [ -n "$IDENTIFIER" ];  then META_PARTS+=("\"identifier\":\"$IDENTIFIER\""); fi
if [ -n "$DESCRIPTION" ]; then META_PARTS+=("\"description\":\"$DESCRIPTION\""); fi
if [ -n "$ENTRY_POINT" ]; then META_PARTS+=("\"entryPoint\":\"$ENTRY_POINT\""); fi
if [ -n "$VISIBILITY" ];  then META_PARTS+=("\"visibility\":\"$VISIBILITY\""); fi
if [ -n "$STATUS" ];      then META_PARTS+=("\"status\":\"$STATUS\""); fi
# shareWithWorkspace is a boolean -> no surrounding quotes.
if [ -n "$SHARE_WORKSPACE" ]; then META_PARTS+=("\"shareWithWorkspace\":$SHARE_WORKSPACE"); fi

METADATA=""
if [ "${#META_PARTS[@]}" -gt 0 ]; then
  OLD_IFS="$IFS"; IFS=","; METADATA="{${META_PARTS[*]}}"; IFS="$OLD_IFS"
fi

if [ -z "$SRC" ] && [ -z "$METADATA" ]; then
  echo "error: nothing to update — pass --src and/or a metadata flag" >&2
  usage
  exit 1
fi

RESP_FILE="$(mktemp)"
trap 'rm -f "$RESP_FILE"' EXIT

if [ -n "$SRC" ]; then
  # Upload path: replace the whole file set, patching metadata in the same
  # atomic request when any metadata flag was passed.
  FORM_ARGS=()
  if [ -n "$METADATA" ]; then FORM_ARGS+=("-F" "metadata=$METADATA"); fi
  if [ -d "$SRC" ]; then
    FILE_COUNT=0
    while IFS= read -r FILE; do
      REL="${FILE#"$SRC"/}"
      # curl's `-F files=@path;filename=REL` shorthand parses `;` `,` and `"`
      # specially, so a file whose relative path contains any of them corrupts
      # the part or aborts the upload. Reject with a clear, per-file message.
      case "$REL" in
        *\;* | *,* | *\"*)
          echo "error: file path contains an unsupported character (; , or \"): $REL" >&2
          echo "       rename the file and retry (curl multipart cannot encode these)." >&2
          exit 1
          ;;
      esac
      FORM_ARGS+=("-F" "files=@$FILE;filename=$REL")
      FILE_COUNT=$((FILE_COUNT + 1))
    done < <(find "$SRC" -type f ! -path '*/.*' ! -name '.*' | sort)
    if [ "$FILE_COUNT" -eq 0 ]; then
      echo "error: no files found under $SRC (dotfiles are skipped)" >&2
      exit 1
    fi
    echo "replacing files with $FILE_COUNT file(s) from $SRC/"
  elif [ -f "$SRC" ] && [[ "$SRC" == *.zip ]]; then
    FORM_ARGS+=("-F" "site=@$SRC;type=application/zip")
    echo "replacing files with zip $SRC"
  else
    echo "error: $SRC is neither a directory nor a .zip file" >&2
    exit 1
  fi
  if [ -n "$METADATA" ]; then
    echo "patching metadata: $METADATA"
  fi

  ENDPOINT="POST /api/v1/artifacts/$UUID/files"
  HTTP_CODE=$(curl -sS -o "$RESP_FILE" -w "%{http_code}" \
    -X POST "$BASE_URL/api/v1/artifacts/$UUID/files" \
    -H "Authorization: Bearer $TOKEN" \
    "${FORM_ARGS[@]}")
else
  # Metadata-only path: JSON PATCH, no upload.
  echo "patching metadata: $METADATA"
  ENDPOINT="PATCH /api/v1/artifacts/$UUID"
  HTTP_CODE=$(curl -sS -o "$RESP_FILE" -w "%{http_code}" \
    -X PATCH "$BASE_URL/api/v1/artifacts/$UUID" \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -d "$METADATA")
fi

if [ "$HTTP_CODE" != "200" ]; then
  echo "error: $ENDPOINT -> $HTTP_CODE" >&2
  cat "$RESP_FILE" >&2
  echo >&2
  exit 1
fi

# Read a string field from the artifact response (jq when available, else grep).
json_field() {
  if command -v jq >/dev/null 2>&1; then
    jq -r --arg k "$1" '.[$k] // empty' "$RESP_FILE"
  else
    grep -o "\"$1\":\"[^\"]*\"" "$RESP_FILE" | head -1 | sed -e "s/^\"$1\":\"//" -e 's/"$//'
  fi
}

if command -v jq >/dev/null 2>&1; then
  jq . "$RESP_FILE"
else
  cat "$RESP_FILE"
  echo
fi

IDENT=$(json_field identifier)
TYPE=$(json_field type)
STATUS_OUT=$(json_field status)
VIS_OUT=$(json_field visibility)
# previewUrl is present for any non-public artifact — private, draft, or archived
# (json_field yields "" for the null it becomes once published + public).
PREVIEW_URL=$(json_field previewUrl)

echo
echo "updated: $UUID"
if [ "$STATUS_OUT" != "published" ] || [ "$VIS_OUT" != "public" ]; then
  echo "note:     not yet public. Via the asset-manager skill, publish with the" >&2
  echo "          asset_update MCP tool (status=published, visibility=public)." >&2
fi
if [ "$TYPE" = "storage" ]; then
  echo "download: $BASE_URL/download/$UUID"
else
  echo "serve:    $BASE_URL/sites/$IDENT-$UUID/"
fi
# Non-public artifacts (private, draft, or archived) return a tokenized preview
# link (owner + same workspace) that renders without making them public.
if [ -n "${PREVIEW_URL:-}" ]; then
  echo "preview:  $PREVIEW_URL"
fi
