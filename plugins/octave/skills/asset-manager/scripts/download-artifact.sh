#!/usr/bin/env bash
# Download every file of an artifact into a local folder, preserving structure.
#
# Usage:
#   ARTIFACTS_ACCESS_TOKEN=<token> ./download-artifact.sh --uuid <artifact-uuid>
#   ARTIFACTS_ACCESS_TOKEN=<token> ./download-artifact.sh --uuid <uuid> --out ./dir
#
# Flags:
#   --uuid <uuid>   (required) the artifact to download
#   --out <dir>     parent directory to download into. The files are always
#                   placed inside a folder named after the artifact identifier,
#                   i.e. <dir>/<identifier>/...  (default: the current
#                   directory, so ./<identifier>/...)
#   -h, --help      show this help
#
# Auth / environment (the access token is env-only):
#   ARTIFACTS_ACCESS_TOKEN  (required) per-user access token — mint one via
#                           POST /api/v1/user/access-token
#   ARTIFACTS_URL           base URL of the server (default: https://link.octavehq.com;
#                           dev override: ARTIFACTS_URL=... in a plugin-root .env)
#
# How it works: both the file list and the file bodies come from the
# authenticated artifacts API (guarded by the per-user access token). It works
# for any artifact you own — or one a teammate shared with your workspace —
# regardless of status or privacy tier, no publish required:
#   GET /api/v1/artifacts/:uuid              -> identifier + metadata.filesMap
#   GET /api/v1/artifacts/:uuid/download/... -> each file's bytes
#
# Tip: for a one-shot grab, GET /api/v1/artifacts/:uuid/download returns the
# single file directly, or a .zip of everything when there are multiple files.
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

UUID=""
# --out is the PARENT dir; the <identifier>/ folder is always created inside it.
OUT_DIR="."

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
  echo "hint: mint one via the asset_generate_access_token MCP tool, then pass it inline:" >&2
  echo "      ARTIFACTS_ACCESS_TOKEN='<token>' $0 ..." >&2
  echo "      (Do NOT curl /api/v1/user/access-token — that needs a service key the" >&2
  echo "       asset-manager skill does not have.)" >&2
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

# 2. Extract the identifier and metadata.filesMap[].path. Prefer a real JSON
#    parser (jq, then python3); fall back to sed/grep only if neither exists.
#    The sed fallback is intentionally last: it truncates filesMap at the first
#    literal `]`, so a filename containing `]` (e.g. "logo [1x].png") would
#    silently drop that file and every file after it — the JSON parsers do not.
if command -v jq >/dev/null 2>&1; then
  IDENTIFIER=$(jq -r '.identifier // empty' "$META_FILE")
  PATHS=$(jq -r '.metadata.filesMap[].path' "$META_FILE")
elif command -v python3 >/dev/null 2>&1 || command -v python >/dev/null 2>&1; then
  PY=$(command -v python3 || command -v python)
  IDENTIFIER=$("$PY" -c 'import json,sys; print(json.load(open(sys.argv[1])).get("identifier") or "")' "$META_FILE")
  PATHS=$("$PY" -c 'import json,sys
d=json.load(open(sys.argv[1]))
for f in (d.get("metadata") or {}).get("filesMap") or []:
    p=f.get("path")
    if p: print(p)' "$META_FILE")
else
  IDENTIFIER=$(grep -o '"identifier":"[^"]*"' "$META_FILE" | head -1 |
    sed -e 's/^"identifier":"//' -e 's/"$//')
  PATHS=$(sed -e 's/.*"filesMap":\[//' -e 's/\].*//' "$META_FILE" |
    grep -o '"path":"[^"]*"' | sed -e 's/^"path":"//' -e 's/"$//')
  # Guard against the sed truncation above silently dropping files: the parsed
  # count must match the number of "path": entries in the whole response.
  EXPECTED=$(grep -o '"path":"' "$META_FILE" | wc -l | tr -d ' ')
  GOT=$(printf '%s\n' "$PATHS" | grep -c .)
  if [ "$GOT" != "$EXPECTED" ]; then
    echo "error: could not reliably parse the file list without jq/python" >&2
    echo "       (got $GOT of $EXPECTED paths — a filename may contain a special" >&2
    echo "        character). Install jq or python3 and retry." >&2
    exit 1
  fi
fi

if [ -z "$PATHS" ]; then
  echo "artifact $UUID has no files (empty filesMap)" >&2
  exit 1
fi

# Always nest the files under a single top-level folder named after the
# artifact identifier (filesystem-safe: no slashes/control chars/leading dots;
# uuid fallback). --out is the PARENT directory that folder is created in, so
# the parent folder of every downloaded file is the identifier.
SAFE_ID=$(printf '%s' "$IDENTIFIER" | tr '/\\' '--' | tr -d '[:cntrl:]' |
  sed -e 's/^[[:space:].]*//' -e 's/[[:space:]]*$//')
DEST="${OUT_DIR%/}/${SAFE_ID:-$UUID}"

# 3. Download each file from the owner-scoped download endpoint (token auth,
#    preserves paths). Works for any status/privacy of an artifact you own.
echo "downloading into $DEST/"
COUNT=0
while IFS= read -r FILE_PATH; do
  [ -n "$FILE_PATH" ] || continue
  # Defense in depth: the server sanitizes upload paths, but this client writes
  # whatever the response says. Refuse anything that could escape $DEST — an
  # absolute path or a `..` segment — so a compromised/MITM'd response can't make
  # curl -o / rm -f touch files outside the download folder.
  case "/$FILE_PATH/" in
    //* | */../* | *//* )
      echo "error: refusing unsafe file path from server response: $FILE_PATH" >&2
      exit 1
      ;;
  esac
  # Percent-encode the characters that would otherwise break the request URL
  # (`%` first, so we don't double-encode). Path separators are left intact
  # because the download route is a wildcard path.
  ENCODED=$(printf '%s' "$FILE_PATH" | sed \
    -e 's/%/%25/g' -e 's/ /%20/g' -e 's/#/%23/g' -e 's/?/%3F/g' \
    -e 's/+/%2B/g' -e 's/&/%26/g')
  mkdir -p "$DEST/$(dirname "$FILE_PATH")"
  HTTP_CODE=$(curl -sS -o "$DEST/$FILE_PATH" -w "%{http_code}" \
    -H "Authorization: Bearer $TOKEN" \
    "$BASE_URL/api/v1/artifacts/$UUID/download/$ENCODED")
  if [ "$HTTP_CODE" != "200" ]; then
    rm -f "$DEST/$FILE_PATH"
    echo "error: GET /api/v1/artifacts/$UUID/download/$FILE_PATH -> $HTTP_CODE" >&2
    echo "hint: 401 -> bad/expired access token; 404 -> wrong uuid, not yours" >&2
    echo "      (nor workspace-shared), or that path isn't in this artifact." >&2
    exit 1
  fi
  echo "  $FILE_PATH"
  COUNT=$((COUNT + 1))
done <<EOF
$PATHS
EOF

echo "done: $COUNT file(s) -> $DEST/"
