## PRevue Review Brief

### 🟡 Medium risk · needs work · 1 blocker · 7 gaps

Changes the default behavior of customer-facing skills (prospector, abm, battlecard-doc) that weren't rerun, and adds catalog fields and data shapes that another repo consumes. Everything is prose and JSON, so a revert undoes it.

| Does what it says | CI | Tests | Owners |
|---|---|---|---|
| ✅ Yes | ✅ passing | ❌ missing | @akash13s, @hayksaryan, @arisrayelyan |

**Needs your attention**

<details><summary><b>🔴 Blocker</b> · Cohort plans have no matching data shape · introduced by this PR · verified 2/2 · 3 files →</summary>

abm now writes cohort plans, but its new output schema only fits a single-account plan. It requires `accountName` and stakeholders, and has no place for cohort members, tiers or plays per tier. The cohort method forbids naming contacts for individual accounts. A host that asks a cohort run for data will get an invented account, or rows that fail the schema.

[`skills/abm/output.schema.json:6-11`](https://github.com/octavehq/lfgtm/blob/1d291f6f1c3b600a133c6b1b8ea98d1c2ce2c508/skills/abm/output.schema.json#L6-L11) · [`skills/abm/references/task-method.md:29-31`](https://github.com/octavehq/lfgtm/blob/1d291f6f1c3b600a133c6b1b8ea98d1c2ce2c508/skills/abm/references/task-method.md#L29-L31) · [`skills/abm/references/cohort-plan.md:55`](https://github.com/octavehq/lfgtm/blob/1d291f6f1c3b600a133c6b1b8ea98d1c2ce2c508/skills/abm/references/cohort-plan.md#L55)

</details>
<details><summary><b>🟡 Gap</b> · Six changelogs put the new release last · introduced by this PR · verified 2/2 · 1 file →</summary>

Every other changelog lists the newest release first. For ads, battlecard-doc, deck, microsite, one-pager and win-loss-report, the new entry was added after 1.0.0 instead. Any reader that takes the first entry as the latest will show stale release notes for these six skills.

[`catalog.json:141-152`](https://github.com/octavehq/lfgtm/blob/1d291f6f1c3b600a133c6b1b8ea98d1c2ce2c508/catalog.json#L141-L152) · [`catalog.json:24-29`](https://github.com/octavehq/lfgtm/blob/1d291f6f1c3b600a133c6b1b8ea98d1c2ce2c508/catalog.json#L24-L29) · [`catalog.json:2232-2236`](https://github.com/octavehq/lfgtm/blob/1d291f6f1c3b600a133c6b1b8ea98d1c2ce2c508/catalog.json#L2232-L2236)

</details>
<details><summary><b>🟡 Gap</b> · Deal card order conflicts with section template · introduced by this PR · verified 2/2 · 2 files →</summary>

battlecard-doc's method now sets a nine-part deal card in order of weight. The unchanged sections reference still sets a different layout: strengths/weaknesses grids, watch-outs, trap questions and Our Pitch. Win rates now come from `get_entity` includeUsage and competitive insights, but later in the same file they come from `get_entity_outcome_stats`.

[`skills/battlecard-doc/references/task-method.md:21-35`](https://github.com/octavehq/lfgtm/blob/1d291f6f1c3b600a133c6b1b8ea98d1c2ce2c508/skills/battlecard-doc/references/task-method.md#L21-L35) · [`skills/battlecard-doc/references/single-competitor-sections.md:8`](https://github.com/octavehq/lfgtm/blob/1d291f6f1c3b600a133c6b1b8ea98d1c2ce2c508/skills/battlecard-doc/references/single-competitor-sections.md#L8) · [`skills/battlecard-doc/references/task-method.md:76-79`](https://github.com/octavehq/lfgtm/blob/1d291f6f1c3b600a133c6b1b8ea98d1c2ce2c508/skills/battlecard-doc/references/task-method.md#L76-L79)

</details>
<details><summary><b>🟡 Gap</b> · Fixed pass score of 7 for qualification <i>(inferred)</i> · introduced by this PR · verified 3/3 · 2 files →</summary>

prospector and abm now treat a score of 7 out of 10 as qualified. The same prospector method says to use the configured qualification, and that unknown is not false. A workspace whose agent passes at a different score, or a candidate with unanswered questions, gets labeled not qualified. The description doesn't mention this rule.

[`skills/prospector/references/task-method.md:21`](https://github.com/octavehq/lfgtm/blob/1d291f6f1c3b600a133c6b1b8ea98d1c2ce2c508/skills/prospector/references/task-method.md#L21) · [`skills/prospector/references/task-method.md:15`](https://github.com/octavehq/lfgtm/blob/1d291f6f1c3b600a133c6b1b8ea98d1c2ce2c508/skills/prospector/references/task-method.md#L15) · [`skills/abm/references/task-method.md:13`](https://github.com/octavehq/lfgtm/blob/1d291f6f1c3b600a133c6b1b8ea98d1c2ce2c508/skills/abm/references/task-method.md#L13)

</details>
<details><summary><b>🟡 Gap</b> · Lookalike route skips saved qualification agents · introduced by this PR · verified 3/3 · 3 files →</summary>

The prospector method says to prefer the workspace's saved qualification agent (`run_qualify_company_agent`) and fall back to `qualify_company`. The new lookalike route and the skill entry tell the model to run `qualify_company` and `qualify_person` on every candidate. That conflicts with the description's 'the workspace's own qualification'.

[`skills/prospector/references/lookalikes.md:37`](https://github.com/octavehq/lfgtm/blob/1d291f6f1c3b600a133c6b1b8ea98d1c2ce2c508/skills/prospector/references/lookalikes.md#L37) · [`skills/prospector/SKILL.md:12`](https://github.com/octavehq/lfgtm/blob/1d291f6f1c3b600a133c6b1b8ea98d1c2ce2c508/skills/prospector/SKILL.md#L12) · [`skills/prospector/references/task-method.md:18`](https://github.com/octavehq/lfgtm/blob/1d291f6f1c3b600a133c6b1b8ea98d1c2ce2c508/skills/prospector/references/task-method.md#L18)

</details>
<details><summary><b>🟡 Gap</b> · New catalog fields are never validated · introduced by this PR · verified 2/2 · 2 files →</summary>

The validator checks only that each skill has a catalog key. A typo in a `kind`, pillar, `outputs` id or `about` word would ship unnoticed. The docs list the allowed ids, and the current values all match them.

[`scripts/validate_package.py:54-59`](https://github.com/octavehq/lfgtm/blob/1d291f6f1c3b600a133c6b1b8ea98d1c2ce2c508/scripts/validate_package.py#L54-L59) · [`docs/catalog-fields.md:20-26`](https://github.com/octavehq/lfgtm/blob/1d291f6f1c3b600a133c6b1b8ea98d1c2ce2c508/docs/catalog-fields.md#L20-L26)

</details>
<details><summary><b>🟡 Gap</b> · Seven changed skills not run end to end · introduced by this PR · verified 2/2 · 3 files →</summary>

The description says deck, one-pager, microsite, battlecard-doc, ads, abm and prospector weren't run to completion after their change. These are the riskiest behavior changes: prospector's new default route, abm cohort plans, and battlecard-doc's new sources. No automated test covers skill prose.

[`skills/prospector/references/lookalikes.md:3`](https://github.com/octavehq/lfgtm/blob/1d291f6f1c3b600a133c6b1b8ea98d1c2ce2c508/skills/prospector/references/lookalikes.md#L3) · [`skills/abm/references/cohort-plan.md:3`](https://github.com/octavehq/lfgtm/blob/1d291f6f1c3b600a133c6b1b8ea98d1c2ce2c508/skills/abm/references/cohort-plan.md#L3) · [`skills/battlecard-doc/references/task-method.md:11-19`](https://github.com/octavehq/lfgtm/blob/1d291f6f1c3b600a133c6b1b8ea98d1c2ce2c508/skills/battlecard-doc/references/task-method.md#L11-L19)

</details>
<details><summary><b>🟡 Gap</b> · ads 1.3.0 changelog entry appended last <i>(inferred)</i> · introduced by this PR · verified 3/3 · 2 files →</summary>

If the catalog sync reads the first changelog entry as the latest release, ads 1.3.0 shows the 1.2.1 notes. The 1.3.0 entry sits after 1.0.0, but every other skill lists newest first. validate() never compares version with the changelog, so CI passes and both main workflows publish it. Ask how octave-app orders or picks entries, and move this one to the top.

[`catalog.json:80-81`](https://github.com/octavehq/lfgtm/blob/1d291f6f1c3b600a133c6b1b8ea98d1c2ce2c508/catalog.json#L80-L81) · [`catalog.json:98-104`](https://github.com/octavehq/lfgtm/blob/1d291f6f1c3b600a133c6b1b8ea98d1c2ce2c508/catalog.json#L98-L104) · [`catalog.json:141-153`](https://github.com/octavehq/lfgtm/blob/1d291f6f1c3b600a133c6b1b8ea98d1c2ce2c508/catalog.json#L141-L153) · [`scripts/validate_package.py:54-59`](https://github.com/octavehq/lfgtm/blob/1d291f6f1c3b600a133c6b1b8ea98d1c2ce2c508/scripts/validate_package.py#L54-L59)

</details>

**What the code does:** Implements each listed item as skill prose, catalog entries and JSON schemas. It also adds a fixed qualification pass score and Octave tool lists to abm and prospector.<details><summary>2 files →</summary>

[`skills/abm/output.schema.json:1-11`](https://github.com/octavehq/lfgtm/blob/1d291f6f1c3b600a133c6b1b8ea98d1c2ce2c508/skills/abm/output.schema.json#L1-L11) · [`skills/prospector/references/results-output.md:9-11`](https://github.com/octavehq/lfgtm/blob/1d291f6f1c3b600a133c6b1b8ea98d1c2ce2c508/skills/prospector/references/results-output.md#L9-L11)

</details>

<sub>The PR says: Add offering fields to the catalog, two new output skills, restructured deck/one-pager/microsite methods, a battlecard built from Octave's own competitor data, ads copy guidance, abm cohort plans, lookalike prospecting, and data schemas from #76. · 37 files · 82 hunks · +1852 −29</sub>

### Themes (9)

**Data schemas for five skills' results** · feature · 14 hunks

<sub>Owners: @akash13s (8 commits to 2 of these files in 6 months), @hayksaryan (5 commits to catalog.json in 6 months)</sub>

prospector, abm, champion-deal-room, generate and pipeline each return their rows as JSON beside the document.<details><summary>2 files →</summary>

[`skills/abm/output.schema.json:1-11`](https://github.com/octavehq/lfgtm/blob/1d291f6f1c3b600a133c6b1b8ea98d1c2ce2c508/skills/abm/output.schema.json#L1-L11) · [`skills/prospector/references/results-output.md:9-11`](https://github.com/octavehq/lfgtm/blob/1d291f6f1c3b600a133c6b1b8ea98d1c2ce2c508/skills/prospector/references/results-output.md#L9-L11)

</details>

- **Before:** These skills returned only a document; a later step had to read it to act on the rows.
- **After:** Each ships an output schema, and its method says what rows to return, copying tool values exactly and writing null for anything unknown.

<details><summary>Hunks</summary>

- [H17](https://github.com/octavehq/lfgtm/pull/77/files#diff-efb40728f97cfac4767a2a0cd5f308d3d5c84427f72b9898e02c989a7b37a13bR510) `catalog.json` +10 −1
- [H18](https://github.com/octavehq/lfgtm/pull/77/files#diff-efb40728f97cfac4767a2a0cd5f308d3d5c84427f72b9898e02c989a7b37a13bR528) `catalog.json` +6 −0
- [H23](https://github.com/octavehq/lfgtm/pull/77/files#diff-efb40728f97cfac4767a2a0cd5f308d3d5c84427f72b9898e02c989a7b37a13bR856) `catalog.json` +6 −0
- [H32](https://github.com/octavehq/lfgtm/pull/77/files#diff-efb40728f97cfac4767a2a0cd5f308d3d5c84427f72b9898e02c989a7b37a13bR1493) `catalog.json` +6 −0
- [H49](https://github.com/octavehq/lfgtm/pull/77/files#diff-0cf3f58f779a0b0966480e4a76f379fd2f38f4909ddf6c298677068641c5e307R1) `skills/abm/output.schema.json` +145 −0
- [H53](https://github.com/octavehq/lfgtm/pull/77/files#diff-fac66940b0ef3e1d8a12bc80cea14449c5396368d1199fb63f51b46ba37195c9R25) `skills/abm/references/task-method.md` +4 −0
- [H58](https://github.com/octavehq/lfgtm/pull/77/files#diff-172991ccf48d15fb873ba0940c5973701185f51a823d98a082f582dc9302f2aeR1) `skills/champion-deal-room/output.schema.json` +136 −0
- [H59](https://github.com/octavehq/lfgtm/pull/77/files#diff-f03cb13b1b114dbbb97165d2a5b936483510b4d53b7767bcc9e05132fc7083cdR19) `skills/champion-deal-room/references/task-method.md` +4 −0
- [H65](https://github.com/octavehq/lfgtm/pull/77/files#diff-6e449f3b0632ff1bf474999c1d8b67e4c8af64058b6c5a252e611d82a752f955R1) `skills/generate/output.schema.json` +96 −0
- [H66](https://github.com/octavehq/lfgtm/pull/77/files#diff-da385fbe0d122ce11070d44f61c089ec07a716e96d674beecc1bbe1b30c0824aR15) `skills/generate/references/task-method.md` +4 −0
- [H73](https://github.com/octavehq/lfgtm/pull/77/files#diff-75a1932d7e3817372c09a22e00a7bbb6d0b401afa092946da2ca325c64b8d148R1) `skills/pipeline/output.schema.json` +161 −0
- [H74](https://github.com/octavehq/lfgtm/pull/77/files#diff-59aa2ca43ecab808915a7253aa707aecb0cf95634b9e90862278ebea60cc72a7R17) `skills/pipeline/references/task-method.md` +4 −0
- [H77](https://github.com/octavehq/lfgtm/pull/77/files#diff-9bc05748fbb63e4731f1c3f25a77461780e6cb45cc55c61188f5dfea4125f913R1) `skills/prospector/output.schema.json` +262 −0
- [H79](https://github.com/octavehq/lfgtm/pull/77/files#diff-3810fb4dff91188f50f70fcc6d87d0ff23fe6a73a5d51894db6618fca4e785cbR1) `skills/prospector/references/results-output.md` +5 −1

</details>

**Prospecting starts from lookalikes of won deals** · feature · 9 hunks

<sub>Owners: @akash13s (9 commits to 3 of these files in 6 months), @arisrayelyan (9 commits to 2 of these files in 6 months)</sub>

With no criteria given, prospector seeds from recent won deals and finds similar companies and buyers.<details><summary>2 files →</summary>

[`skills/prospector/references/task-method.md:3-4`](https://github.com/octavehq/lfgtm/blob/1d291f6f1c3b600a133c6b1b8ea98d1c2ce2c508/skills/prospector/references/task-method.md#L3-L4) · [`skills/prospector/references/lookalikes.md:7-19`](https://github.com/octavehq/lfgtm/blob/1d291f6f1c3b600a133c6b1b8ea98d1c2ce2c508/skills/prospector/references/lookalikes.md#L7-L19) · [`skills/prospector/references/task-method.md:17-21`](https://github.com/octavehq/lfgtm/blob/1d291f6f1c3b600a133c6b1b8ea98d1c2ce2c508/skills/prospector/references/task-method.md#L17-L21)

</details>

- **Before:** prospector built its candidate list from the library's segments, personas and ICP criteria.
- **After:** By default it picks a few recent won deals as seeds, finds similar companies and buyers, then qualifies each one. Criteria or a seed company still work, and it can run on a schedule.

<details><summary>Hunks</summary>

- [H4](https://github.com/octavehq/lfgtm/pull/77/files#diff-30bf75f8f19e56642c61ecaa902d4d6a0a0126a234b800d76b79a7f1faab8be2R714) `EXAMPLES.md` +3 −0
- [H8](https://github.com/octavehq/lfgtm/pull/77/files#diff-b335630551682c19a781afebcf4d07bf978fb1f8ac04c6bf87428ed5106870f5R279) `README.md` +3 −1
- [H36](https://github.com/octavehq/lfgtm/pull/77/files#diff-efb40728f97cfac4767a2a0cd5f308d3d5c84427f72b9898e02c989a7b37a13bR1753) `catalog.json` +11 −1
- [H37](https://github.com/octavehq/lfgtm/pull/77/files#diff-efb40728f97cfac4767a2a0cd5f308d3d5c84427f72b9898e02c989a7b37a13bR1772) `catalog.json` +6 −0
- [H75](https://github.com/octavehq/lfgtm/pull/77/files#diff-a95a7ac416b67b98eea9cef4a098df217de81e605e57c884f0580adb17a26d28R1) `skills/prospector/SKILL.md` +4 −2
- [H76](https://github.com/octavehq/lfgtm/pull/77/files#diff-a95a7ac416b67b98eea9cef4a098df217de81e605e57c884f0580adb17a26d28R20) `skills/prospector/SKILL.md` +5 −1
- [H78](https://github.com/octavehq/lfgtm/pull/77/files#diff-6c56128c2c308ac7790145103f7c148ee625a9a6c912ac0e5769a47c1b7f5131R1) `skills/prospector/references/lookalikes.md` +52 −0
- [H80](https://github.com/octavehq/lfgtm/pull/77/files#diff-4c0e4923e2917128ff890a483a7712709cf615ca35af6973e52c497a3bc619eeR1) `skills/prospector/references/task-method.md` +3 −0
- [H81](https://github.com/octavehq/lfgtm/pull/77/files#diff-4c0e4923e2917128ff890a483a7712709cf615ca35af6973e52c497a3bc619eeR14) `skills/prospector/references/task-method.md` +7 −0

</details>

**Account planning also covers a whole cohort** · feature · 10 hunks

<sub>Owners: @akash13s (9 commits to 3 of these files in 6 months), @arisrayelyan (9 commits to 2 of these files in 6 months)</sub>

abm writes a cohort plan for a segment or list, leaving per-account plans to separate runs.<details><summary>2 files →</summary>

[`skills/abm/references/task-method.md:3-4`](https://github.com/octavehq/lfgtm/blob/1d291f6f1c3b600a133c6b1b8ea98d1c2ce2c508/skills/abm/references/task-method.md#L3-L4) · [`skills/abm/references/cohort-plan.md:53-55`](https://github.com/octavehq/lfgtm/blob/1d291f6f1c3b600a133c6b1b8ea98d1c2ce2c508/skills/abm/references/cohort-plan.md#L53-L55)

</details>

- **Before:** abm planned one named company: stakeholders, persona matching and outreach.
- **After:** A segment, cohort or list gets one plan: who is in it, the angle they share, tiers and plays per tier. Tier 1 accounts are listed as ready-to-run single-account plans.

<details><summary>Hunks</summary>

- [H3](https://github.com/octavehq/lfgtm/pull/77/files#diff-30bf75f8f19e56642c61ecaa902d4d6a0a0126a234b800d76b79a7f1faab8be2R426) `EXAMPLES.md` +4 −0
- [H5](https://github.com/octavehq/lfgtm/pull/77/files#diff-b335630551682c19a781afebcf4d07bf978fb1f8ac04c6bf87428ed5106870f5R93) `README.md` +2 −2
- [H7](https://github.com/octavehq/lfgtm/pull/77/files#diff-b335630551682c19a781afebcf4d07bf978fb1f8ac04c6bf87428ed5106870f5R219) `README.md` +3 −0
- [H9](https://github.com/octavehq/lfgtm/pull/77/files#diff-efb40728f97cfac4767a2a0cd5f308d3d5c84427f72b9898e02c989a7b37a13bR2) `catalog.json` +11 −1
- [H10](https://github.com/octavehq/lfgtm/pull/77/files#diff-efb40728f97cfac4767a2a0cd5f308d3d5c84427f72b9898e02c989a7b37a13bR21) `catalog.json` +6 −0
- [H47](https://github.com/octavehq/lfgtm/pull/77/files#diff-2a4fecfd381aec802cdd3d0f89f7f9866ba33a14bf8210eb6e1805182162df99R1) `skills/abm/SKILL.md` +5 −3
- [H48](https://github.com/octavehq/lfgtm/pull/77/files#diff-2a4fecfd381aec802cdd3d0f89f7f9866ba33a14bf8210eb6e1805182162df99R21) `skills/abm/SKILL.md` +3 −0
- [H50](https://github.com/octavehq/lfgtm/pull/77/files#diff-a14ee70926174d5680fda3d96801b43d1033eb9869c5302bb2ede6d23bf9f519R1) `skills/abm/references/cohort-plan.md` +63 −0
- [H51](https://github.com/octavehq/lfgtm/pull/77/files#diff-fac66940b0ef3e1d8a12bc80cea14449c5396368d1199fb63f51b46ba37195c9R1) `skills/abm/references/task-method.md` +3 −0
- [H52](https://github.com/octavehq/lfgtm/pull/77/files#diff-fac66940b0ef3e1d8a12bc80cea14449c5396368d1199fb63f51b46ba37195c9R10) `skills/abm/references/task-method.md` +3 −0

</details>

**Battlecards start from Octave's own competitor data** · feature · 4 hunks

<sub>Owners: @akash13s (6 commits to catalog.json in 6 months), @hayksaryan (5 commits to catalog.json in 6 months)</sub>

battlecard-doc reads the generated battlecard, intel and deal outcomes before the library profile.<details><summary>1 file →</summary>

[`skills/battlecard-doc/references/task-method.md:11-19`](https://github.com/octavehq/lfgtm/blob/1d291f6f1c3b600a133c6b1b8ea98d1c2ce2c508/skills/battlecard-doc/references/task-method.md#L11-L19) · [`skills/battlecard-doc/references/task-method.md:21-35`](https://github.com/octavehq/lfgtm/blob/1d291f6f1c3b600a133c6b1b8ea98d1c2ce2c508/skills/battlecard-doc/references/task-method.md#L21-L35)

</details>

- **Before:** A card was built from the competitor's library profile, plus calls and Ask Octave.
- **After:** It first reads Octave's generated battlecard, recent intel and competitive deal outcomes, then builds a deal card in nine weighted parts.

<details><summary>Hunks</summary>

- [H15](https://github.com/octavehq/lfgtm/pull/77/files#diff-efb40728f97cfac4767a2a0cd5f308d3d5c84427f72b9898e02c989a7b37a13bR360) `catalog.json` +15 −1
- [H16](https://github.com/octavehq/lfgtm/pull/77/files#diff-efb40728f97cfac4767a2a0cd5f308d3d5c84427f72b9898e02c989a7b37a13bR430) `catalog.json` +16 −0
- [H56](https://github.com/octavehq/lfgtm/pull/77/files#diff-052417090ca0f930e232df2db78dfce19900ff9c50870aa3f29aaa95ffc3334eR8) `skills/battlecard-doc/references/task-method.md` +26 −0
- [H57](https://github.com/octavehq/lfgtm/pull/77/files#diff-5c59c368bd16b1da4c6325089c037df487e524f3375aa71ede82f870be6a2a41R18) `skills/battlecard-doc/references/tool-reference.md` +4 −1

</details>

**Catalog says how each skill is offered** · config · 16 hunks

<sub>Owners: @akash13s (6 commits to catalog.json in 6 months), @hayksaryan (5 commits to catalog.json in 6 months)</sub>

Every catalog entry gains a display name, job-or-output kind, subjects, pillars and default formats.<details><summary>2 files →</summary>

[`docs/catalog-fields.md:24-38`](https://github.com/octavehq/lfgtm/blob/1d291f6f1c3b600a133c6b1b8ea98d1c2ce2c508/docs/catalog-fields.md#L24-L38) · [`catalog.json:1242-1258`](https://github.com/octavehq/lfgtm/blob/1d291f6f1c3b600a133c6b1b8ea98d1c2ce2c508/catalog.json#L1242-L1258)

</details>

- **Before:** The catalog held only release fields such as version, changelog and runtimes.
- **After:** Entries carry optional offering fields, documented in a new guide. Changing only these fields needs no version bump.

<details><summary>Hunks</summary>

- [H13](https://github.com/octavehq/lfgtm/pull/77/files#diff-efb40728f97cfac4767a2a0cd5f308d3d5c84427f72b9898e02c989a7b37a13bR216) `catalog.json` +5 −0
- [H14](https://github.com/octavehq/lfgtm/pull/77/files#diff-efb40728f97cfac4767a2a0cd5f308d3d5c84427f72b9898e02c989a7b37a13bR299) `catalog.json` +8 −0
- [H19](https://github.com/octavehq/lfgtm/pull/77/files#diff-efb40728f97cfac4767a2a0cd5f308d3d5c84427f72b9898e02c989a7b37a13bR586) `catalog.json` +10 −0
- [H24](https://github.com/octavehq/lfgtm/pull/77/files#diff-efb40728f97cfac4767a2a0cd5f308d3d5c84427f72b9898e02c989a7b37a13bR914) `catalog.json` +8 −0
- [H25](https://github.com/octavehq/lfgtm/pull/77/files#diff-efb40728f97cfac4767a2a0cd5f308d3d5c84427f72b9898e02c989a7b37a13bR994) `catalog.json` +13 −0
- [H26](https://github.com/octavehq/lfgtm/pull/77/files#diff-efb40728f97cfac4767a2a0cd5f308d3d5c84427f72b9898e02c989a7b37a13bR1067) `catalog.json` +15 −0
- [H27](https://github.com/octavehq/lfgtm/pull/77/files#diff-efb40728f97cfac4767a2a0cd5f308d3d5c84427f72b9898e02c989a7b37a13bR1142) `catalog.json` +8 −0
- [H33](https://github.com/octavehq/lfgtm/pull/77/files#diff-efb40728f97cfac4767a2a0cd5f308d3d5c84427f72b9898e02c989a7b37a13bR1551) `catalog.json` +9 −0
- [H34](https://github.com/octavehq/lfgtm/pull/77/files#diff-efb40728f97cfac4767a2a0cd5f308d3d5c84427f72b9898e02c989a7b37a13bR1620) `catalog.json` +8 −0
- [H35](https://github.com/octavehq/lfgtm/pull/77/files#diff-efb40728f97cfac4767a2a0cd5f308d3d5c84427f72b9898e02c989a7b37a13bR1682) `catalog.json` +12 −0
- [H38](https://github.com/octavehq/lfgtm/pull/77/files#diff-efb40728f97cfac4767a2a0cd5f308d3d5c84427f72b9898e02c989a7b37a13bR1824) `catalog.json` +8 −0
- [H39](https://github.com/octavehq/lfgtm/pull/77/files#diff-efb40728f97cfac4767a2a0cd5f308d3d5c84427f72b9898e02c989a7b37a13bR1892) `catalog.json` +8 −0
- [H40](https://github.com/octavehq/lfgtm/pull/77/files#diff-efb40728f97cfac4767a2a0cd5f308d3d5c84427f72b9898e02c989a7b37a13bR1954) `catalog.json` +14 −0
- [H41](https://github.com/octavehq/lfgtm/pull/77/files#diff-efb40728f97cfac4767a2a0cd5f308d3d5c84427f72b9898e02c989a7b37a13bR2028) `catalog.json` +12 −0
- [H42](https://github.com/octavehq/lfgtm/pull/77/files#diff-efb40728f97cfac4767a2a0cd5f308d3d5c84427f72b9898e02c989a7b37a13bR2094) `catalog.json` +9 −0
- [H45](https://github.com/octavehq/lfgtm/pull/77/files#diff-a4bfa559753fbf81374c6b751ecf81e97d7f5507ee2c66525d6d498e03b79883R1) `docs/catalog-fields.md` +38 −0

</details>

**Four output skills, microsite becomes a job** · feature · 20 hunks

<sub>Owners: @akash13s (9 commits to 6 of these files in 6 months), @arisrayelyan (10 commits to 4 of these files in 6 months)</sub>

Adds document and magazine, restructures deck and one-pager by purpose, and offers microsite as a job.<details><summary>2 files →</summary>

[`skills/document/references/task-method.md:11-30`](https://github.com/octavehq/lfgtm/blob/1d291f6f1c3b600a133c6b1b8ea98d1c2ce2c508/skills/document/references/task-method.md#L11-L30) · [`skills/deck/references/task-method.md:3-24`](https://github.com/octavehq/lfgtm/blob/1d291f6f1c3b600a133c6b1b8ea98d1c2ce2c508/skills/deck/references/task-method.md#L3-L24)

</details>

- **Before:** Document and magazine existed only as shared format guides and couldn't be run by name; deck, one-pager and microsite opened on their specific rules.
- **After:** Each output method opens with two ways in and a table of narrative patterns by purpose, with the existing rules filed under their pattern. Microsite is offered as a landing-page job.

<details><summary>Hunks</summary>

- [H6](https://github.com/octavehq/lfgtm/pull/77/files#diff-b335630551682c19a781afebcf4d07bf978fb1f8ac04c6bf87428ed5106870f5R124) `README.md` +2 −0
- [H20](https://github.com/octavehq/lfgtm/pull/77/files#diff-efb40728f97cfac4767a2a0cd5f308d3d5c84427f72b9898e02c989a7b37a13bR655) `catalog.json` +11 −1
- [H21](https://github.com/octavehq/lfgtm/pull/77/files#diff-efb40728f97cfac4767a2a0cd5f308d3d5c84427f72b9898e02c989a7b37a13bR715) `catalog.json` +22 −0
- [H22](https://github.com/octavehq/lfgtm/pull/77/files#diff-efb40728f97cfac4767a2a0cd5f308d3d5c84427f72b9898e02c989a7b37a13bR806) `catalog.json` +41 −1
- [H28](https://github.com/octavehq/lfgtm/pull/77/files#diff-efb40728f97cfac4767a2a0cd5f308d3d5c84427f72b9898e02c989a7b37a13bR1210) `catalog.json` +44 −0
- [H29](https://github.com/octavehq/lfgtm/pull/77/files#diff-efb40728f97cfac4767a2a0cd5f308d3d5c84427f72b9898e02c989a7b37a13bR1315) `catalog.json` +11 −1
- [H30](https://github.com/octavehq/lfgtm/pull/77/files#diff-efb40728f97cfac4767a2a0cd5f308d3d5c84427f72b9898e02c989a7b37a13bR1381) `catalog.json` +21 −1
- [H31](https://github.com/octavehq/lfgtm/pull/77/files#diff-efb40728f97cfac4767a2a0cd5f308d3d5c84427f72b9898e02c989a7b37a13bR1461) `catalog.json` +20 −1
- [H46](https://github.com/octavehq/lfgtm/pull/77/files#diff-91091dac2d130b347d2baa431e5947222d9998cade51d52127425086a64c7f3cR11) `scripts/validate_package.py` +1 −1
- [H60](https://github.com/octavehq/lfgtm/pull/77/files#diff-4e34a9a049fe0a1f43a16e2f7ca4cf04206fd1e37f259c6a7a5a34e6b76f1154R9) `skills/deck/SKILL.md` +2 −0
- [H61](https://github.com/octavehq/lfgtm/pull/77/files#diff-539722473333203a7404c7466dc01bb5b4d938568e45eeb1c8b188ca6fd2be8aR1) `skills/deck/references/task-method.md` +22 −1
- [H62](https://github.com/octavehq/lfgtm/pull/77/files#diff-539722473333203a7404c7466dc01bb5b4d938568e45eeb1c8b188ca6fd2be8aR29) `skills/deck/references/task-method.md` +4 −0
- [H63](https://github.com/octavehq/lfgtm/pull/77/files#diff-1bda949ad0868c3f1b6b9cd82a935d5b282f1744bcb4a6ec04afbee01597b719R1) `skills/document/SKILL.md` +39 −0
- [H64](https://github.com/octavehq/lfgtm/pull/77/files#diff-dcf9cc8f64ac1e48294985493353cc5296e0188e6e3f1ea36ac38b9af1bb6e74R1) `skills/document/references/task-method.md` +51 −0
- [H67](https://github.com/octavehq/lfgtm/pull/77/files#diff-4fd20c61997b8e60085e0d6d8e93d269dcae498fea86fb0f97515a1126ea975bR1) `skills/magazine/SKILL.md` +40 −0
- [H68](https://github.com/octavehq/lfgtm/pull/77/files#diff-80e5f8bb0bd64df1222e313b61ed2806ffbb7bc888b4ae9cc497b2897695b677R1) `skills/magazine/references/task-method.md` +51 −0
- [H69](https://github.com/octavehq/lfgtm/pull/77/files#diff-ada07207262372f0d7f921f4923fc13387cb78b9f5ece0cdfdaed8002b98f593R1) `skills/microsite/SKILL.md` +4 −2
- [H70](https://github.com/octavehq/lfgtm/pull/77/files#diff-4afc29752ee01f8abddb08cb4ab3448b5d1f5e1d112a66a11c17edc155faf9bcR1) `skills/microsite/references/task-method.md` +26 −0
- [H71](https://github.com/octavehq/lfgtm/pull/77/files#diff-b096f20437a53d476cb0881e210da0905e489d286850b79d09a6a461764bdb33R9) `skills/one-pager/SKILL.md` +2 −0
- [H72](https://github.com/octavehq/lfgtm/pull/77/files#diff-2a85ce5929cf324a1de23deec0721cbe34741c1b84317d1102fce96be003a7acR1) `skills/one-pager/references/task-method.md` +29 −0

</details>

**Ads platform copy guide** · docs · 4 hunks

<sub>Owners: @akash13s (6 commits to catalog.json in 6 months), @hayksaryan (5 commits to catalog.json in 6 months)</sub>

Adds a guide to Google, LinkedIn and Meta field lengths, a pointer to it from the ads method, and the ads 1.3.0 catalog entry. <sup title="inferred, not fully verified">inferred</sup>

<details><summary>Hunks</summary>

- [H11](https://github.com/octavehq/lfgtm/pull/77/files#diff-efb40728f97cfac4767a2a0cd5f308d3d5c84427f72b9898e02c989a7b37a13bR78) `catalog.json` +10 −1
- [H12](https://github.com/octavehq/lfgtm/pull/77/files#diff-efb40728f97cfac4767a2a0cd5f308d3d5c84427f72b9898e02c989a7b37a13bR143) `catalog.json` +14 −0
- [H54](https://github.com/octavehq/lfgtm/pull/77/files#diff-686c47f956c426f6a3d87898ef31c7c1680f9c6d23ed9bbb9be5d8ceda18901eR1) `skills/ads/references/platform-copy.md` +71 −0
- [H55](https://github.com/octavehq/lfgtm/pull/77/files#diff-be3c033fe360286dd5c319611ca6d399d94714a5d0ddd398d37f428c3f87e0a6R16) `skills/ads/references/task-method.md` +2 −0

</details>

**Win-loss report routes text questions to insights** · fix · 3 hunks

<sub>Owners: @akash13s (6 commits to catalog.json in 6 months), @hayksaryan (5 commits to catalog.json in 6 months)</sub>

Its description pointed text-only questions back at itself; it now points at insights. Version 1.3.2. <sup title="inferred, not fully verified">inferred</sup>

<details><summary>Hunks</summary>

- [H43](https://github.com/octavehq/lfgtm/pull/77/files#diff-efb40728f97cfac4767a2a0cd5f308d3d5c84427f72b9898e02c989a7b37a13bR2162) `catalog.json` +11 −1
- [H44](https://github.com/octavehq/lfgtm/pull/77/files#diff-efb40728f97cfac4767a2a0cd5f308d3d5c84427f72b9898e02c989a7b37a13bR2228) `catalog.json` +6 −0
- [H82](https://github.com/octavehq/lfgtm/pull/77/files#diff-8c53d9f807a52e213968152dd0866b078a8e4576fac69ff5663e1283e069074eR1) `skills/win-loss-report/SKILL.md` +1 −1

</details>

**Plugin version bump** · mechanical · 2 hunks

<sub>Owners: @akash13s (6 commits to .claude-plugin in 6 months), @arisrayelyan (4 commits to .claude-plugin in 6 months)</sub>

Plugin and marketplace go from 2.21.0 to 2.22.1 together; the validator checks they match. <sup title="inferred, not fully verified">inferred</sup>

<details><summary>Hunks</summary>

- [H1](https://github.com/octavehq/lfgtm/pull/77/files#diff-5352ee4067f17e7948e1425843f0a454e045bc8edf338f0bcf75c6804ddabd9aR13) `.claude-plugin/marketplace.json` +1 −1
- [H2](https://github.com/octavehq/lfgtm/pull/77/files#diff-037fda53525563fb89230704794a06db1150204ca28ce80697a637121c3ed3f9R1) `.claude-plugin/plugin.json` +1 −1

</details>


<sub>Every hunk is covered by a theme.</sub>

### Blast radius

All changes are skill prose and JSON, but default behavior shifts for several customer-facing skills that weren't rerun, and another repo consumes the new fields and schemas.

**Endpoints**
- New route `/octave:document` <sup title="inferred, not fully verified">inferred</sup>
- New route `/octave:magazine` <sup title="inferred, not fully verified">inferred</sup>
- Changed route `/octave:abm --segment / --accounts` <sup title="inferred, not fully verified">inferred</sup>
- Changed route `/octave:prospector (no arguments)` <sup title="inferred, not fully verified">inferred</sup>
- Changed route `/octave:battlecard-doc` <sup title="inferred, not fully verified">inferred</sup>
- Changed route `/octave:microsite` <sup title="inferred, not fully verified">inferred</sup>

<sub>None found: irreversible, callers and dependents, jobs and workers, tables and data.</sub>

**Uses of the changed code** · checked 16 of 16 uses of the changed code

<sub>Other repositories: searched octavehq's code for 1 changed name; no other repository uses them. octavehq/ask-octave-skills wasn't searched: git@github.com: Permission denied (publickey). octavehq/demo-warehouse-content wasn't searched: git@github.com: Permission denied (publickey). octavehq/docs wasn't searched: git@github.com: Permission denied (publickey). octavehq/lfgtm-codex wasn't searched: git@github.com: Permission denied (publickey).</sub>

- ✓ not affected · `validate` · 16 sites: The workflows and validate.sh still pass: the repo, the Codex build and the Cursor build each hold 32 skill folders now that document and magazine exist.<details><summary>1 file →</summary>

[`scripts/validate.sh:5`](https://github.com/octavehq/lfgtm/blob/1d291f6f1c3b600a133c6b1b8ea98d1c2ce2c508/scripts/validate.sh#L5) · [`scripts/validate.sh:13-14`](https://github.com/octavehq/lfgtm/blob/1d291f6f1c3b600a133c6b1b8ea98d1c2ce2c508/scripts/validate.sh#L13-L14)

</details>

### Why this risk level

- With no arguments, prospector now starts from lookalikes of recent won deals instead of library criteria.<details><summary>1 file →</summary>

[`skills/prospector/references/task-method.md:3-4`](https://github.com/octavehq/lfgtm/blob/1d291f6f1c3b600a133c6b1b8ea98d1c2ce2c508/skills/prospector/references/task-method.md#L3-L4)

</details>
- The only automated check touched is the validator's skill count, raised from 30 to 32 for the two new skills.<details><summary>1 file →</summary>

[`scripts/validate_package.py:14`](https://github.com/octavehq/lfgtm/blob/1d291f6f1c3b600a133c6b1b8ea98d1c2ce2c508/scripts/validate_package.py#L14)

</details>
- Five skills gain an output schema; the abm one describes only a single-account plan.<details><summary>1 file →</summary>

[`skills/abm/output.schema.json:1-11`](https://github.com/octavehq/lfgtm/blob/1d291f6f1c3b600a133c6b1b8ea98d1c2ce2c508/skills/abm/output.schema.json#L1-L11)

</details>

### Merge readiness

| | Status | Detail |
|---|---|---|
| CI | ✅ passing | All 1 checks passing. |
| Tests | ❌ missing | 0 of 6 decisions have a test that would fail if it were reverted. |
| Owners | @akash13s, @hayksaryan, @arisrayelyan | From git history: who committed to these files in the 6 months before the PR. |

<details><summary>Brief quality checks</summary>

- Coverage: 82/82 hunks in themes, 0 marked unexplained
- Claims: 17 checked ✓, 13 inferred ~
- Evidence links: 50/50 point at real lines
- Schema: valid
- Investigators: 1 traced the affected uses; 1 new finding, 0 duplicates dropped

</details>

<sub>PRevue · claude-opus-5-5 (high) · 31 turns · 5.1 min · run locally by @jtemps · head 1d291f6 · ✓ checked against the code, ~ inferred</sub>