#!/usr/bin/env bash
# Download every file of an artifact into a local folder, preserving structure.
#
# Usage:
#   ARTIFACTS_ACCESS_TOKEN=<token> ./download-artifact.sh --uuid <artifact-uuid>
#   ARTIFACTS_ACCESS_TOKEN=<token> ./download-artifact.sh --uuid <uuid> --out ./dir
#
# Flags:
#   --uuid <uuid>   (required) the artifact to download
#   --out <dir>     where to write the files (default: ./<artifact-identifier>)
#   -h, --help      show this help
#
# Auth / environment (the access token is env-only):
#   ARTIFACTS_ACCESS_TOKEN  (required) per-user access token — mint one via
#                           POST /api/v1/user/access-token
#   ARTIFACTS_URL           base URL of the server (default: http://localhost:3015)
#
# How it works: both the file list and the file bodies come from the
# authenticated, owner-scoped artifacts API (guarded by the per-user access
# token), so this works for any artifact you own regardless of status or
# visibility — no publish required:
#   GET /api/v1/artifacts/:uuid              -> identifier + metadata.filesMap
#   GET /api/v1/artifacts/:uuid/download/... -> each file's bytes
#
# Tip: for a one-shot grab, GET /api/v1/artifacts/:uuid/download returns the
# single file directly, or a .zip of everything when there are multiple files.
set -euo pipefail

BASE_URL="${ARTIFACTS_URL:-http://localhost:3015}"
TOKEN="${ARTIFACTS_ACCESS_TOKEN:-}"

usage() {
  # Reuse the header comment block above as the single source of help text.
  awk 'NR==1 { next } /^#/ { sub(/^# ?/, ""); print; next } { exit }' "$0" >&2
}

UUID=""
OUT_DIR=""

while [ $# -gt 0 ]; do
  case "$1" in
    --uuid) UUID="${2:?--uuid requires a value}"; shift 2 ;;
    --out)  OUT_DIR="${2:?--out requires a value}"; shift 2 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "error: unexpected argument: $1" >&2; usage; exit 1 ;;
  esac
done

if [ -z "$UUID" ]; then
  echo "error: --uuid is required" >&2
  usage
  exit 1
fi

if [ -z "$TOKEN" ]; then
  echo "error: no access token — set ARTIFACTS_ACCESS_TOKEN" >&2
  echo "mint one: curl -X POST $BASE_URL/api/v1/user/access-token \\" >&2
  echo '  -H "Authorization: Bearer <service-key>" -H "Content-Type: application/json" \' >&2
  echo '  -d '"'"'{"userOId":"...","workspaceOId":"..."}'"'" >&2
  exit 1
fi

META_FILE="$(mktemp)"
trap 'rm -f "$META_FILE"' EXIT

# 1. Fetch artifact metadata (owner-scoped) for the identifier + file list.
HTTP_CODE=$(curl -sS -o "$META_FILE" -w "%{http_code}" \
  -H "Authorization: Bearer $TOKEN" \
  "$BASE_URL/api/v1/artifacts/$UUID")
if [ "$HTTP_CODE" != "200" ]; then
  echo "error: GET /api/v1/artifacts/$UUID -> $HTTP_CODE" >&2
  cat "$META_FILE" >&2
  echo >&2
  exit 1
fi

# 2. Extract the identifier and metadata.filesMap[].path — jq when available,
#    sed/grep fallback (the filesMap array contains no nested arrays, so the
#    first ] ends it).
if command -v jq >/dev/null 2>&1; then
  IDENTIFIER=$(jq -r '.identifier // empty' "$META_FILE")
  PATHS=$(jq -r '.metadata.filesMap[].path' "$META_FILE")
else
  IDENTIFIER=$(grep -o '"identifier":"[^"]*"' "$META_FILE" | head -1 |
    sed -e 's/^"identifier":"//' -e 's/"$//')
  PATHS=$(sed -e 's/.*"filesMap":\[//' -e 's/\].*//' "$META_FILE" |
    grep -o '"path":"[^"]*"' | sed -e 's/^"path":"//' -e 's/"$//')
fi

if [ -z "$PATHS" ]; then
  echo "artifact $UUID has no files (empty filesMap)" >&2
  exit 1
fi

# Default output dir = the identifier as a filesystem-safe folder name (no
# slashes/control chars/leading dots); fall back to the uuid.
if [ -z "$OUT_DIR" ]; then
  SAFE_ID=$(printf '%s' "$IDENTIFIER" | tr '/\\' '--' | tr -d '[:cntrl:]' |
    sed -e 's/^[[:space:].]*//' -e 's/[[:space:]]*$//')
  OUT_DIR="./${SAFE_ID:-$UUID}"
fi

# 3. Download each file from the owner-scoped download endpoint (token auth,
#    preserves paths). Works for any status/visibility of an artifact you own.
echo "downloading into $OUT_DIR/"
COUNT=0
while IFS= read -r FILE_PATH; do
  [ -n "$FILE_PATH" ] || continue
  ENCODED=$(printf '%s' "$FILE_PATH" | sed 's/ /%20/g')
  mkdir -p "$OUT_DIR/$(dirname "$FILE_PATH")"
  HTTP_CODE=$(curl -sS -o "$OUT_DIR/$FILE_PATH" -w "%{http_code}" \
    -H "Authorization: Bearer $TOKEN" \
    "$BASE_URL/api/v1/artifacts/$UUID/download/$ENCODED")
  if [ "$HTTP_CODE" != "200" ]; then
    rm -f "$OUT_DIR/$FILE_PATH"
    echo "error: GET /api/v1/artifacts/$UUID/download/$FILE_PATH -> $HTTP_CODE" >&2
    echo "hint: 401 -> bad/expired access token; 404 -> wrong uuid, not your" >&2
    echo "      artifact, or that path isn't in this artifact." >&2
    exit 1
  fi
  echo "  $FILE_PATH"
  COUNT=$((COUNT + 1))
done <<EOF
$PATHS
EOF

echo "done: $COUNT file(s) -> $OUT_DIR/"
