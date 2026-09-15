# Cache operations

Use [brand_cache.py](../scripts/brand_cache.py) for canonical hostname/workspace
identity, validation, resolution and promotion. Carry the selected brand through
downstream rendering; a name match alone is not identity.

- **Default:** reuse a validated matching capture. Build only when absent or
  when refresh is requested. Read [capture workflow](capture-workflow.md).
- **Refresh:** capture in a unique staging directory, verify assets and visual
  fidelity, then promote atomically. Failed validation retains the current kit.
- **List:** show current captures in the verified workspace with company/domain,
  capture date and readiness. Do not scan other workspace contents to fill gaps.
- **Show:** resolve the exact selected capture and open its components or visual
  specification. Distinguish mechanical validation from completed visual review.
- **Export:** bundle only approved kit files/assets with allowed-use decisions.
  Include the manifest, tokens, components and visual rules as needed; omit raw
  source captures, diagnostic output and private notes. For hosting use an explicit
  publish manifest and asset-manager’s audience/access checks.
- **Delete:** an explicit delete request authorizes the identified local cache
  entry. Verify exact workspace/domain/capture scope, prefer reversible removal
  where supported, and preserve unrelated captures and aliases. An ambiguous
  label needs resolution before deletion. Deleting a local kit does not imply
  deletion of separately hosted artifacts.

Legacy name-based directories remain usable as explicitly supplied paths, but
reuse as a workspace brand requires matching verified manifest identity. Bind
missing identity from actual evidence before migration; never guess the domain
from a company-name slug. The renderer accepts `--domain` and `--workspace` to
assert the expected identity when loading a kit.
