# Octave Entity Model — Canonical Taxonomy and oId Prefixes

The single source of truth for Octave entity types, their `entityType` values, and their oId prefixes. Skills that list, create, update, or audit library entities should use these names and prefixes consistently.

## Fetching entities

`list_entities` lists the entity types accepted by its current schema. Writing styles and Motion-era objects use dedicated tools. It returns **slim rows** (oId, name, description) by default for cheap discovery — start there and escalate only when a step needs more:

- `search: "<name>"` — filter by name/description (resolve an entity by name)
- `all: true` — return every match in one response instead of paginating
- `includeDetails: true` — include each entity's full body (narrow with `search` or a small page first)
- `get_entity({ oId })` — full detail for a single entity once you have its oId

## Library Entities

| Entity type | `entityType` value | oId prefix | Notes |
|-------------|-------------------|------------|-------|
| Persona | `persona` | `pe_` | Buyer roles — who discovers, evaluates, champions |
| Product | `product` | `px_` | An offering (see also Service, Solution) |
| Service | `service` | `sc_` | Professional service offerings — own table, own prefix |
| Solution | `solution` | `sv_` | Packaged solution combining products/services into one buyer-facing narrative |
| Core Feature | `core_feature` | `cf_` | A named piece of an offering (NOT its own offering) — links under a Product/Service/Solution via `offeringOId`. Body carries `whyThisExists` / `whatItDoes` / `howItWorks` / `whatItImpacts`. Use for a distinctly-named feature that isn't its own go-to-market motion (independent commercial or delivery identity); shared quota, buyer, or meeting alone does not determine commercial identity. |
| Segment | `segment` | `sg_` | Company types where the offering fits differently |
| Use Case | `use_case` | `uu_` | Customer outcomes, not internal processes |
| Competitor | `competitor` | `cp_` | Named rivals encountered in deals |
| Alternative | `alternative` | `ao_` | Behavioral patterns — what teams do instead of buying (build internally, status quo) |
| Buying Trigger | `buying_trigger` | `bq_` | Organizational moments that create urgency (funding, new hire, key departure) |
| Objection | `objection` | `oj_` | Recurring concerns to pre-handle — distinct from competitors and alternatives |
| Proof Point | `proof_point` | `pp_` | Sourced substantiation or outcomes; preserve measured/reported status, applicability and external-use limits. Quantify only when supported. |
| Reference | `reference` | `re_` | Reference narrative; verify actual customer relationship, claim scope and approved use before treating it as a customer example. |
| Brand Voice | `brand_voice` | `bv_` | Tone and voice guidelines for generation |


## Dedicated tools and returned identities

Use `list_writing_styles` for writing-style discovery. Writing style is separate from visual branding and is not a `list_entities` type. Prefixes are explanatory only: use IDs returned by tools, never construct one. Read support does not imply write support. Validate examples against the connected tool schema before execution.

## Motions and Motion Playbooks (Motion era)

| Entity type | oId prefix | Notes |
|-------------|------------|-------|
| Motion | `mot_` | Top-level container: offering + motion type (`NET_NEW`, `UPSELL`, `CROSS_SELL`, `CONVERT_FREE_TO_PAID`, `RENEW_AND_RETAIN`, `DISPLACE_INCUMBENT`) |
| Motion Playbook | `mpb_` | Default (auto-generated) or Custom (`THEMATIC` / `MILESTONE` / `ACCOUNT` / `COMPETITIVE`) |
| Motion ICP | `micp_` | One narrative cell per persona × segment intersection inside a Motion Playbook |

Resolve the offering and Motion, select the intended default/custom playbook, and list cells with `playbookOId` when supported. Follow `hasMore`/`nextOffset` for complete coverage. Read selected narratives with `find_motion_icp` and the returned `motionIcpOId`; a missing narrative is missing context, not an empty approved strategy.

Each Motion ICP cell carries a structured narrative: Target ICP overview, Operating landscape, Strategic narrative, Pains and consequences, Benefits and impacts, Methodology, References.

## Other Common oId Prefixes

| Object | oId prefix | Notes |
|--------|------------|-------|
| Agent (all types) | `ca_` | Saved agent configurations |
| Workspace | `wa_` | |
| Organization | `og_` | |
| Revision | `ev_` | Entity audit-trail entries (`list_revisions` / `get_revision`) |

## Legacy (deprecated, still readable)

| Entity type | `entityType` value | oId prefix | Notes |
|-------------|-------------------|------------|-------|
| Playbook | `playbook` | `pb_` | Legacy standalone Playbook — superseded by Motions / Motion Playbooks / Motion ICPs |
| Value Prop | — | `hy_` | Lived on legacy playbooks; superseded by Motion ICP narrative sections |

Prefer the Motion-era primitives for all new work. Legacy playbook tools (`get_playbook`, `list_value_props`, `create_playbook`, `update_playbook`, `add_value_props`, `update_value_props`) exist only for workspaces that have not migrated.
