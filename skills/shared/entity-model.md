# Octave Entity Model — Canonical Taxonomy and oId Prefixes

The single source of truth for Octave entity types, their `entityType` values, and their oId prefixes. Skills that list, create, update, or audit library entities should use these names and prefixes consistently.

## Library Entities

| Entity type | `entityType` value | oId prefix | Notes |
|-------------|-------------------|------------|-------|
| Persona | `persona` | `pe_` | Buyer roles — who discovers, evaluates, champions |
| Product | `product` | `px_` | An offering (see also Service, Solution) |
| Service | `service` | `px_` | Services share the product prefix |
| Segment | `segment` | `sg_` | Company types where the offering fits differently |
| Use Case | `use_case` | `uu_` | Customer outcomes, not internal processes |
| Competitor | `competitor` | `cp_` | Named rivals encountered in deals |
| Alternative | `alternative` | — | Behavioral patterns — what teams do instead of buying (build internally, status quo) |
| Buying Trigger | `buying_trigger` | — | Organizational moments that create urgency (funding, new hire, key departure) |
| Objection | `objection` | `oj_` | Recurring concerns to pre-handle — distinct from competitors and alternatives |
| Proof Point | `proof_point` | `pp_` | Quantified, pattern-based results — must come from real outcomes |
| Reference | `reference` | `re_` | Customer stories with narrative context — must come from real customers |
| Brand Voice | `brand_voice` | `bv_` | Tone and voice guidelines for generation |
| Writing Style | `writing_style` | `ws_` | Structural writing preferences for generation |

## Motions and Motion Playbooks (Motion era)

| Entity type | oId prefix | Notes |
|-------------|------------|-------|
| Motion | `mo_` | Top-level container: offering + motion type (`NET_NEW`, `UPSELL`, `CROSS_SELL`, `CONVERT_FREE_TO_PAID`, `RENEW_AND_RETAIN`, `DISPLACE_INCUMBENT`) |
| Motion Playbook | `mp_` | Default (auto-generated) or Custom (`THEMATIC` / `MILESTONE` / `ACCOUNT` / `COMPETITIVE`) |
| Motion ICP | `mi_` | One narrative cell per persona × segment intersection inside a Motion Playbook |

Each Motion ICP cell carries a structured narrative: Target ICP overview, Operating landscape, Strategic narrative, Pains and consequences, Benefits and impacts, Methodology, References.

## Other Common oId Prefixes

| Object | oId prefix | Notes |
|--------|------------|-------|
| Agent (all types) | `ca_` | Saved agent configurations |
| Workspace | `wa_` | |
| Organization | `og_` | |
| Revision | `rv_` | Entity audit-trail entries (`list_revisions` / `get_revision`) |

## Legacy (deprecated, still readable)

| Entity type | `entityType` value | oId prefix | Notes |
|-------------|-------------------|------------|-------|
| Playbook | `playbook` | `pb_` | Legacy standalone Playbook — superseded by Motions / Motion Playbooks / Motion ICPs |
| Value Prop | — | `hy_` | Lived on legacy playbooks; superseded by Motion ICP narrative sections |

Prefer the Motion-era primitives for all new work. Legacy playbook tools (`get_playbook`, `list_value_props`, `create_playbook`, `update_playbook`, `add_value_props`, `update_value_props`) exist only for workspaces that have not migrated.
