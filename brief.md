## PRevue Review Brief

### 🟡 Medium risk · needs work · 5 gaps

The changes are agent instructions, not data writes, but prospector's default behavior and abm's scope change for every user. These new paths have no recorded run, and the app reads the new catalog fields.

| Does what it says | CI | Tests | Owners |
|---|---|---|---|
| ⚠️ Partly | ✅ passing | ❌ missing | @akash13s, @hayksaryan, @arisrayelyan |

**Needs your attention**

<details><summary><b>🟡 Gap</b> · Battlecard relies on intel tools new here <i>(inferred)</i> · 2 files →</summary>

`list_intel`, `get_intel` and the battlecard option on `get_entity` appear nowhere else in the repo or in the README tool list. The method only covers empty results. It doesn't say what to do if the server lacks these tools. Can the author confirm they ship today, or that they arrive with octave-app#8914?

[`skills/battlecard-doc/references/tool-reference.md:21-23`](https://github.com/octavehq/lfgtm/blob/875d17b3c07d134419169033c595b24571f371f2/skills/battlecard-doc/references/tool-reference.md#L21-L23) · [`skills/battlecard-doc/references/task-method.md:15-19`](https://github.com/octavehq/lfgtm/blob/875d17b3c07d134419169033c595b24571f371f2/skills/battlecard-doc/references/task-method.md#L15-L19)

</details>
<details><summary><b>🟡 Gap</b> · Five changed skills not yet run <i>(inferred)</i> · introduced by this PR · verified 2/2 · 2 files →</summary>

The description says one-pager, microsite, ads, abm's cohort plan and prospector's lookalike route were not run to completion after the change. It says the last two are new behavior and should be run before release. No automated check covers skill prose.

[`skills/prospector/SKILL.md:12`](https://github.com/octavehq/lfgtm/blob/875d17b3c07d134419169033c595b24571f371f2/skills/prospector/SKILL.md#L12) · [`skills/abm/references/cohort-plan.md:1-9`](https://github.com/octavehq/lfgtm/blob/875d17b3c07d134419169033c595b24571f371f2/skills/abm/references/cohort-plan.md#L1-L9)

</details>
<details><summary><b>🟡 Gap</b> · Contact rows still have no score · introduced by this PR · verified 2/2 · 3 files →</summary>

The fix added a score to account rows only. The lookalike method qualifies every person candidate, and the task method says to give the score on every row and rank by it. Contact rows have no score field, and their qualification is optional. A later step that ranks or filters contacts from the data loses the person score. Ask whether contacts should carry a required score and qualification.

[`skills/prospector/output.schema.json:131-142`](https://github.com/octavehq/lfgtm/blob/875d17b3c07d134419169033c595b24571f371f2/skills/prospector/output.schema.json#L131-L142) · [`skills/prospector/output.schema.json:241-253`](https://github.com/octavehq/lfgtm/blob/875d17b3c07d134419169033c595b24571f371f2/skills/prospector/output.schema.json#L241-L253) · [`skills/prospector/references/task-method.md:21`](https://github.com/octavehq/lfgtm/blob/875d17b3c07d134419169033c595b24571f371f2/skills/prospector/references/task-method.md#L21) · [`skills/prospector/references/lookalikes.md:37`](https://github.com/octavehq/lfgtm/blob/875d17b3c07d134419169033c595b24571f371f2/skills/prospector/references/lookalikes.md#L37)

</details>
<details><summary><b>🟡 Gap</b> · Seed customer names now ride in data rows <i>(inferred)</i> · introduced by this PR · verified 2/3 · 2 files →</summary>

The method says seed customers are named only in the internal summary. Now every lookalike account and contact row names its seed in resembles, inside data built so a later step can act on the rows without reading the document. Outreach steps such as generate get the customer name, and only a description note keeps it out of copy. Ask whether downstream consumers drop resembles, or whether it…

[`skills/prospector/output.schema.json:106-112`](https://github.com/octavehq/lfgtm/blob/875d17b3c07d134419169033c595b24571f371f2/skills/prospector/output.schema.json#L106-L112) · [`skills/prospector/output.schema.json:4`](https://github.com/octavehq/lfgtm/blob/875d17b3c07d134419169033c595b24571f371f2/skills/prospector/output.schema.json#L4) · [`skills/prospector/references/lookalikes.md:17`](https://github.com/octavehq/lfgtm/blob/875d17b3c07d134419169033c595b24571f371f2/skills/prospector/references/lookalikes.md#L17) · [`skills/prospector/references/lookalikes.md:39`](https://github.com/octavehq/lfgtm/blob/875d17b3c07d134419169033c595b24571f371f2/skills/prospector/references/lookalikes.md#L39)

</details>
<details><summary><b>🟡 Gap</b> · Seed fields optional and missing from data guide <i>(inferred)</i> · introduced by this PR · verified 2/2 · 2 files →</summary>

resembles and matchedTraits are not required, unlike the other row fields, which must always be present, even as null. The data paragraph the run follows when it returns data doesn't list them either; only the lookalike method does. A lookalike row can leave them out, and a reader can't tell that from a row on another route. matchedTraits must also be 'as the tool reported them'. Can the author…

[`skills/prospector/output.schema.json:15-26`](https://github.com/octavehq/lfgtm/blob/875d17b3c07d134419169033c595b24571f371f2/skills/prospector/output.schema.json#L15-L26) · [`skills/prospector/output.schema.json:113-122`](https://github.com/octavehq/lfgtm/blob/875d17b3c07d134419169033c595b24571f371f2/skills/prospector/output.schema.json#L113-L122) · [`skills/prospector/references/results-output.md:11`](https://github.com/octavehq/lfgtm/blob/875d17b3c07d134419169033c595b24571f371f2/skills/prospector/references/results-output.md#L11)

</details>
<details><summary><b>🔵 Info</b> · Release and sync now gate on catalog fields · 3 files →</summary>

The validator now fails on an unknown kind, pillar or output id, a malformed about list, or a changelog whose first entry isn't the current version. It gates the release ZIP and the downstream sync. The Codex and Cursor builds carry no catalog, so only the root run checks these rules.

[`scripts/build-release.py:11-12`](https://github.com/octavehq/lfgtm/blob/875d17b3c07d134419169033c595b24571f371f2/scripts/build-release.py#L11-L12) · [`scripts/validate.sh:5`](https://github.com/octavehq/lfgtm/blob/875d17b3c07d134419169033c595b24571f371f2/scripts/validate.sh#L5) · [`scripts/validate_package.py:60-77`](https://github.com/octavehq/lfgtm/blob/875d17b3c07d134419169033c595b24571f371f2/scripts/validate_package.py#L60-L77)

</details>

**What the code does:** Implements each listed change. abm's single-company plan also gains new tool steps and a default 7-of-10 fit rule that the description calls unchanged.<details><summary>2 files →</summary>

[`skills/prospector/SKILL.md:12`](https://github.com/octavehq/lfgtm/blob/875d17b3c07d134419169033c595b24571f371f2/skills/prospector/SKILL.md#L12) · [`skills/prospector/references/lookalikes.md:7-19`](https://github.com/octavehq/lfgtm/blob/875d17b3c07d134419169033c595b24571f371f2/skills/prospector/references/lookalikes.md#L7-L19) · [`skills/prospector/references/lookalikes.md:39`](https://github.com/octavehq/lfgtm/blob/875d17b3c07d134419169033c595b24571f371f2/skills/prospector/references/lookalikes.md#L39)

</details>

<sub>The PR says: Add offering fields to the catalog, add document and magazine, reframe deck, one-pager and microsite, deepen battlecard-doc, add abm cohort plans and prospector lookalikes, and fold in #76's structured results. · 37 files · 88 hunks · +1986 −29</sub>

### Themes (10)

**Prospecting starts from lookalikes of won deals** · feature · 8 hunks

<sub>Owners: @akash13s (8 commits to 3 of these files in 6 months), @hayksaryan (5 commits to catalog.json in 6 months)</sub>

With no criteria given, prospector seeds from recent won deals, finds similar companies and buyers, then qualifies them.<details><summary>2 files →</summary>

[`skills/prospector/SKILL.md:12`](https://github.com/octavehq/lfgtm/blob/875d17b3c07d134419169033c595b24571f371f2/skills/prospector/SKILL.md#L12) · [`skills/prospector/references/lookalikes.md:7-19`](https://github.com/octavehq/lfgtm/blob/875d17b3c07d134419169033c595b24571f371f2/skills/prospector/references/lookalikes.md#L7-L19) · [`skills/prospector/references/lookalikes.md:39`](https://github.com/octavehq/lfgtm/blob/875d17b3c07d134419169033c595b24571f371f2/skills/prospector/references/lookalikes.md#L39)

</details>

- **Before:** Prospector built its candidate list from the library's segments, personas and ICP criteria.
- **After:** A bare request reads won deals from the past year, picks a few as seeds, and searches for similar companies and people. Each lookalike row keeps its seed and shared traits in the returned data.

<details><summary>Hunks</summary>

- [H41](https://github.com/octavehq/lfgtm/pull/77/files#diff-efb40728f97cfac4767a2a0cd5f308d3d5c84427f72b9898e02c989a7b37a13bR1753) `catalog.json` +11 −1
- [H42](https://github.com/octavehq/lfgtm/pull/77/files#diff-efb40728f97cfac4767a2a0cd5f308d3d5c84427f72b9898e02c989a7b37a13bR1772) `catalog.json` +6 −0
- [H81](https://github.com/octavehq/lfgtm/pull/77/files#diff-a95a7ac416b67b98eea9cef4a098df217de81e605e57c884f0580adb17a26d28R1) `skills/prospector/SKILL.md` +4 −2
- [H82](https://github.com/octavehq/lfgtm/pull/77/files#diff-a95a7ac416b67b98eea9cef4a098df217de81e605e57c884f0580adb17a26d28R20) `skills/prospector/SKILL.md` +5 −1
- [H84](https://github.com/octavehq/lfgtm/pull/77/files#diff-6c56128c2c308ac7790145103f7c148ee625a9a6c912ac0e5769a47c1b7f5131R1) `skills/prospector/references/lookalikes.md` +52 −0
- [H85](https://github.com/octavehq/lfgtm/pull/77/files#diff-3810fb4dff91188f50f70fcc6d87d0ff23fe6a73a5d51894db6618fca4e785cbR1) `skills/prospector/references/results-output.md` +5 −1
- [H86](https://github.com/octavehq/lfgtm/pull/77/files#diff-4c0e4923e2917128ff890a483a7712709cf615ca35af6973e52c497a3bc619eeR1) `skills/prospector/references/task-method.md` +3 −0
- [H87](https://github.com/octavehq/lfgtm/pull/77/files#diff-4c0e4923e2917128ff890a483a7712709cf615ca35af6973e52c497a3bc619eeR14) `skills/prospector/references/task-method.md` +7 −0

</details>

**Account planning covers a whole segment** · feature · 7 hunks

<sub>Owners: @akash13s (8 commits to 2 of these files in 6 months), @hayksaryan (5 commits to catalog.json in 6 months)</sub>

Asked about a segment or account list, abm writes one cohort plan and leaves per-account committees to separate runs.<details><summary>3 files →</summary>

[`skills/abm/SKILL.md:12`](https://github.com/octavehq/lfgtm/blob/875d17b3c07d134419169033c595b24571f371f2/skills/abm/SKILL.md#L12) · [`skills/abm/references/cohort-plan.md:53-55`](https://github.com/octavehq/lfgtm/blob/875d17b3c07d134419169033c595b24571f371f2/skills/abm/references/cohort-plan.md#L53-L55) · [`skills/abm/references/task-method.md:3-4`](https://github.com/octavehq/lfgtm/blob/875d17b3c07d134419169033c595b24571f371f2/skills/abm/references/task-method.md#L3-L4)

</details>

- **Before:** abm planned one named company: stakeholders, persona matches and outreach.
- **After:** A segment, cohort or list gets a plan covering who is in it, one shared angle from similar won deals, tiers and plays per tier. It names no people at individual accounts.

<details><summary>Hunks</summary>

- [H9](https://github.com/octavehq/lfgtm/pull/77/files#diff-efb40728f97cfac4767a2a0cd5f308d3d5c84427f72b9898e02c989a7b37a13bR2) `catalog.json` +11 −1
- [H10](https://github.com/octavehq/lfgtm/pull/77/files#diff-efb40728f97cfac4767a2a0cd5f308d3d5c84427f72b9898e02c989a7b37a13bR21) `catalog.json` +6 −0
- [H53](https://github.com/octavehq/lfgtm/pull/77/files#diff-2a4fecfd381aec802cdd3d0f89f7f9866ba33a14bf8210eb6e1805182162df99R1) `skills/abm/SKILL.md` +5 −3
- [H54](https://github.com/octavehq/lfgtm/pull/77/files#diff-2a4fecfd381aec802cdd3d0f89f7f9866ba33a14bf8210eb6e1805182162df99R21) `skills/abm/SKILL.md` +3 −0
- [H56](https://github.com/octavehq/lfgtm/pull/77/files#diff-a14ee70926174d5680fda3d96801b43d1033eb9869c5302bb2ede6d23bf9f519R1) `skills/abm/references/cohort-plan.md` +63 −0
- [H57](https://github.com/octavehq/lfgtm/pull/77/files#diff-fac66940b0ef3e1d8a12bc80cea14449c5396368d1199fb63f51b46ba37195c9R1) `skills/abm/references/task-method.md` +3 −0
- [H58](https://github.com/octavehq/lfgtm/pull/77/files#diff-fac66940b0ef3e1d8a12bc80cea14449c5396368d1199fb63f51b46ba37195c9R10) `skills/abm/references/task-method.md` +3 −0

</details>

**Five skills return rows beside the document** · feature · 14 hunks

<sub>Owners: @akash13s (6 commits to catalog.json in 6 months), @hayksaryan (5 commits to catalog.json in 6 months)</sub>

prospector, abm, champion-deal-room, generate and pipeline each declare a data shape and return matching rows when asked.<details><summary>3 files →</summary>

[`skills/prospector/output.schema.json:1-20`](https://github.com/octavehq/lfgtm/blob/875d17b3c07d134419169033c595b24571f371f2/skills/prospector/output.schema.json#L1-L20) · [`skills/abm/references/task-method.md:29-33`](https://github.com/octavehq/lfgtm/blob/875d17b3c07d134419169033c595b24571f371f2/skills/abm/references/task-method.md#L29-L33) · [`skills/pipeline/references/task-method.md:21-23`](https://github.com/octavehq/lfgtm/blob/875d17b3c07d134419169033c595b24571f371f2/skills/pipeline/references/task-method.md#L21-L23)

</details>

- **Before:** These skills produced only a document. A later step had to read the page to act on it.
- **After:** When the host asks for data, each returns the rows its document shows (accounts, people, plays, pieces, risks), with null where a tool returned nothing.

<details><summary>Hunks</summary>

- [H19](https://github.com/octavehq/lfgtm/pull/77/files#diff-efb40728f97cfac4767a2a0cd5f308d3d5c84427f72b9898e02c989a7b37a13bR510) `catalog.json` +10 −1
- [H20](https://github.com/octavehq/lfgtm/pull/77/files#diff-efb40728f97cfac4767a2a0cd5f308d3d5c84427f72b9898e02c989a7b37a13bR528) `catalog.json` +6 −0
- [H26](https://github.com/octavehq/lfgtm/pull/77/files#diff-efb40728f97cfac4767a2a0cd5f308d3d5c84427f72b9898e02c989a7b37a13bR856) `catalog.json` +6 −0
- [H36](https://github.com/octavehq/lfgtm/pull/77/files#diff-efb40728f97cfac4767a2a0cd5f308d3d5c84427f72b9898e02c989a7b37a13bR1471) `catalog.json` +14 −1
- [H37](https://github.com/octavehq/lfgtm/pull/77/files#diff-efb40728f97cfac4767a2a0cd5f308d3d5c84427f72b9898e02c989a7b37a13bR1493) `catalog.json` +6 −0
- [H55](https://github.com/octavehq/lfgtm/pull/77/files#diff-0cf3f58f779a0b0966480e4a76f379fd2f38f4909ddf6c298677068641c5e307R1) `skills/abm/output.schema.json` +222 −0
- [H59](https://github.com/octavehq/lfgtm/pull/77/files#diff-fac66940b0ef3e1d8a12bc80cea14449c5396368d1199fb63f51b46ba37195c9R25) `skills/abm/references/task-method.md` +6 −0
- [H64](https://github.com/octavehq/lfgtm/pull/77/files#diff-172991ccf48d15fb873ba0940c5973701185f51a823d98a082f582dc9302f2aeR1) `skills/champion-deal-room/output.schema.json` +136 −0
- [H65](https://github.com/octavehq/lfgtm/pull/77/files#diff-f03cb13b1b114dbbb97165d2a5b936483510b4d53b7767bcc9e05132fc7083cdR19) `skills/champion-deal-room/references/task-method.md` +4 −0
- [H71](https://github.com/octavehq/lfgtm/pull/77/files#diff-6e449f3b0632ff1bf474999c1d8b67e4c8af64058b6c5a252e611d82a752f955R1) `skills/generate/output.schema.json` +96 −0
- [H72](https://github.com/octavehq/lfgtm/pull/77/files#diff-da385fbe0d122ce11070d44f61c089ec07a716e96d674beecc1bbe1b30c0824aR15) `skills/generate/references/task-method.md` +4 −0
- [H79](https://github.com/octavehq/lfgtm/pull/77/files#diff-75a1932d7e3817372c09a22e00a7bbb6d0b401afa092946da2ca325c64b8d148R1) `skills/pipeline/output.schema.json` +161 −0
- [H80](https://github.com/octavehq/lfgtm/pull/77/files#diff-59aa2ca43ecab808915a7253aa707aecb0cf95634b9e90862278ebea60cc72a7R17) `skills/pipeline/references/task-method.md` +4 −0
- [H83](https://github.com/octavehq/lfgtm/pull/77/files#diff-9bc05748fbb63e4731f1c3f25a77461780e6cb45cc55c61188f5dfea4125f913R1) `skills/prospector/output.schema.json` +297 −0

</details>

**Four output skills shape any subject** · feature · 20 hunks

<sub>Owners: @akash13s (8 commits to 5 of these files in 6 months), @hayksaryan (6 commits to 2 of these files in 6 months)</sub>

New document and magazine skills join deck and one-pager as format-only skills, and microsite becomes a landing-page job.<details><summary>3 files →</summary>

[`catalog.json:809-821`](https://github.com/octavehq/lfgtm/blob/875d17b3c07d134419169033c595b24571f371f2/catalog.json#L809-L821) · [`skills/deck/references/task-method.md:11-24`](https://github.com/octavehq/lfgtm/blob/875d17b3c07d134419169033c595b24571f371f2/skills/deck/references/task-method.md#L11-L24) · [`scripts/validate_package.py:14`](https://github.com/octavehq/lfgtm/blob/875d17b3c07d134419169033c595b24571f371f2/scripts/validate_package.py#L14)

</details>

- **Before:** Document and magazine existed only as shared format guides and couldn't be run by name. Deck, one-pager and microsite opened with their special-case rules.
- **After:** All five open with two ways in (content supplied, or only a subject) and narrative patterns chosen by purpose, and existing rules sit under the matching pattern. The skill count goes to 32.

<details><summary>Hunks</summary>

- [H22](https://github.com/octavehq/lfgtm/pull/77/files#diff-efb40728f97cfac4767a2a0cd5f308d3d5c84427f72b9898e02c989a7b37a13bR655) `catalog.json` +11 −1
- [H23](https://github.com/octavehq/lfgtm/pull/77/files#diff-efb40728f97cfac4767a2a0cd5f308d3d5c84427f72b9898e02c989a7b37a13bR674) `catalog.json` +6 −0
- [H25](https://github.com/octavehq/lfgtm/pull/77/files#diff-efb40728f97cfac4767a2a0cd5f308d3d5c84427f72b9898e02c989a7b37a13bR806) `catalog.json` +41 −1
- [H31](https://github.com/octavehq/lfgtm/pull/77/files#diff-efb40728f97cfac4767a2a0cd5f308d3d5c84427f72b9898e02c989a7b37a13bR1210) `catalog.json` +44 −0
- [H32](https://github.com/octavehq/lfgtm/pull/77/files#diff-efb40728f97cfac4767a2a0cd5f308d3d5c84427f72b9898e02c989a7b37a13bR1315) `catalog.json` +11 −1
- [H33](https://github.com/octavehq/lfgtm/pull/77/files#diff-efb40728f97cfac4767a2a0cd5f308d3d5c84427f72b9898e02c989a7b37a13bR1334) `catalog.json` +6 −0
- [H34](https://github.com/octavehq/lfgtm/pull/77/files#diff-efb40728f97cfac4767a2a0cd5f308d3d5c84427f72b9898e02c989a7b37a13bR1388) `catalog.json` +15 −1
- [H35](https://github.com/octavehq/lfgtm/pull/77/files#diff-efb40728f97cfac4767a2a0cd5f308d3d5c84427f72b9898e02c989a7b37a13bR1414) `catalog.json` +6 −0
- [H51](https://github.com/octavehq/lfgtm/pull/77/files#diff-91091dac2d130b347d2baa431e5947222d9998cade51d52127425086a64c7f3cR11) `scripts/validate_package.py` +1 −1
- [H66](https://github.com/octavehq/lfgtm/pull/77/files#diff-4e34a9a049fe0a1f43a16e2f7ca4cf04206fd1e37f259c6a7a5a34e6b76f1154R9) `skills/deck/SKILL.md` +2 −0
- [H67](https://github.com/octavehq/lfgtm/pull/77/files#diff-539722473333203a7404c7466dc01bb5b4d938568e45eeb1c8b188ca6fd2be8aR1) `skills/deck/references/task-method.md` +22 −1
- [H68](https://github.com/octavehq/lfgtm/pull/77/files#diff-539722473333203a7404c7466dc01bb5b4d938568e45eeb1c8b188ca6fd2be8aR29) `skills/deck/references/task-method.md` +4 −0
- [H69](https://github.com/octavehq/lfgtm/pull/77/files#diff-1bda949ad0868c3f1b6b9cd82a935d5b282f1744bcb4a6ec04afbee01597b719R1) `skills/document/SKILL.md` +39 −0
- [H70](https://github.com/octavehq/lfgtm/pull/77/files#diff-dcf9cc8f64ac1e48294985493353cc5296e0188e6e3f1ea36ac38b9af1bb6e74R1) `skills/document/references/task-method.md` +51 −0
- [H73](https://github.com/octavehq/lfgtm/pull/77/files#diff-4fd20c61997b8e60085e0d6d8e93d269dcae498fea86fb0f97515a1126ea975bR1) `skills/magazine/SKILL.md` +40 −0
- [H74](https://github.com/octavehq/lfgtm/pull/77/files#diff-80e5f8bb0bd64df1222e313b61ed2806ffbb7bc888b4ae9cc497b2897695b677R1) `skills/magazine/references/task-method.md` +51 −0
- [H75](https://github.com/octavehq/lfgtm/pull/77/files#diff-ada07207262372f0d7f921f4923fc13387cb78b9f5ece0cdfdaed8002b98f593R1) `skills/microsite/SKILL.md` +4 −2
- [H76](https://github.com/octavehq/lfgtm/pull/77/files#diff-4afc29752ee01f8abddb08cb4ab3448b5d1f5e1d112a66a11c17edc155faf9bcR1) `skills/microsite/references/task-method.md` +26 −0
- [H77](https://github.com/octavehq/lfgtm/pull/77/files#diff-b096f20437a53d476cb0881e210da0905e489d286850b79d09a6a461764bdb33R9) `skills/one-pager/SKILL.md` +2 −0
- [H78](https://github.com/octavehq/lfgtm/pull/77/files#diff-2a85ce5929cf324a1de23deec0721cbe34741c1b84317d1102fce96be003a7acR1) `skills/one-pager/references/task-method.md` +29 −0

</details>

**Catalog entries say how a skill is offered** · config · 20 hunks

<sub>Owners: @akash13s (6 commits to 2 of these files in 6 months), @hayksaryan (6 commits to 2 of these files in 6 months)</sub>

Every catalog entry gains optional fields: title, kind, about, pillars and outputs. The validator checks them and the changelog order.<details><summary>2 files →</summary>

[`docs/catalog-fields.md:3-11`](https://github.com/octavehq/lfgtm/blob/875d17b3c07d134419169033c595b24571f371f2/docs/catalog-fields.md#L3-L11) · [`docs/catalog-fields.md:28-30`](https://github.com/octavehq/lfgtm/blob/875d17b3c07d134419169033c595b24571f371f2/docs/catalog-fields.md#L28-L30) · [`scripts/validate_package.py:60-77`](https://github.com/octavehq/lfgtm/blob/875d17b3c07d134419169033c595b24571f371f2/scripts/validate_package.py#L60-L77)

</details>

- **Before:** Catalog entries held only release fields: version, runtimes, required tools and changelog.
- **After:** Entries carry a readable title, a job or output kind, likely subjects, GTM areas and formats (default first). Changing only these fields needs no version bump.

<details><summary>Hunks</summary>

- [H13](https://github.com/octavehq/lfgtm/pull/77/files#diff-efb40728f97cfac4767a2a0cd5f308d3d5c84427f72b9898e02c989a7b37a13bR154) `catalog.json` +8 −0
- [H14](https://github.com/octavehq/lfgtm/pull/77/files#diff-efb40728f97cfac4767a2a0cd5f308d3d5c84427f72b9898e02c989a7b37a13bR216) `catalog.json` +5 −0
- [H15](https://github.com/octavehq/lfgtm/pull/77/files#diff-efb40728f97cfac4767a2a0cd5f308d3d5c84427f72b9898e02c989a7b37a13bR299) `catalog.json` +8 −0
- [H18](https://github.com/octavehq/lfgtm/pull/77/files#diff-efb40728f97cfac4767a2a0cd5f308d3d5c84427f72b9898e02c989a7b37a13bR441) `catalog.json` +10 −0
- [H21](https://github.com/octavehq/lfgtm/pull/77/files#diff-efb40728f97cfac4767a2a0cd5f308d3d5c84427f72b9898e02c989a7b37a13bR586) `catalog.json` +10 −0
- [H24](https://github.com/octavehq/lfgtm/pull/77/files#diff-efb40728f97cfac4767a2a0cd5f308d3d5c84427f72b9898e02c989a7b37a13bR726) `catalog.json` +16 −0
- [H27](https://github.com/octavehq/lfgtm/pull/77/files#diff-efb40728f97cfac4767a2a0cd5f308d3d5c84427f72b9898e02c989a7b37a13bR914) `catalog.json` +8 −0
- [H28](https://github.com/octavehq/lfgtm/pull/77/files#diff-efb40728f97cfac4767a2a0cd5f308d3d5c84427f72b9898e02c989a7b37a13bR994) `catalog.json` +13 −0
- [H29](https://github.com/octavehq/lfgtm/pull/77/files#diff-efb40728f97cfac4767a2a0cd5f308d3d5c84427f72b9898e02c989a7b37a13bR1067) `catalog.json` +15 −0
- [H30](https://github.com/octavehq/lfgtm/pull/77/files#diff-efb40728f97cfac4767a2a0cd5f308d3d5c84427f72b9898e02c989a7b37a13bR1142) `catalog.json` +8 −0
- [H38](https://github.com/octavehq/lfgtm/pull/77/files#diff-efb40728f97cfac4767a2a0cd5f308d3d5c84427f72b9898e02c989a7b37a13bR1551) `catalog.json` +9 −0
- [H39](https://github.com/octavehq/lfgtm/pull/77/files#diff-efb40728f97cfac4767a2a0cd5f308d3d5c84427f72b9898e02c989a7b37a13bR1620) `catalog.json` +8 −0
- [H40](https://github.com/octavehq/lfgtm/pull/77/files#diff-efb40728f97cfac4767a2a0cd5f308d3d5c84427f72b9898e02c989a7b37a13bR1682) `catalog.json` +12 −0
- [H43](https://github.com/octavehq/lfgtm/pull/77/files#diff-efb40728f97cfac4767a2a0cd5f308d3d5c84427f72b9898e02c989a7b37a13bR1824) `catalog.json` +8 −0
- [H44](https://github.com/octavehq/lfgtm/pull/77/files#diff-efb40728f97cfac4767a2a0cd5f308d3d5c84427f72b9898e02c989a7b37a13bR1892) `catalog.json` +8 −0
- [H45](https://github.com/octavehq/lfgtm/pull/77/files#diff-efb40728f97cfac4767a2a0cd5f308d3d5c84427f72b9898e02c989a7b37a13bR1954) `catalog.json` +14 −0
- [H46](https://github.com/octavehq/lfgtm/pull/77/files#diff-efb40728f97cfac4767a2a0cd5f308d3d5c84427f72b9898e02c989a7b37a13bR2028) `catalog.json` +12 −0
- [H47](https://github.com/octavehq/lfgtm/pull/77/files#diff-efb40728f97cfac4767a2a0cd5f308d3d5c84427f72b9898e02c989a7b37a13bR2094) `catalog.json` +9 −0
- [H50](https://github.com/octavehq/lfgtm/pull/77/files#diff-a4bfa559753fbf81374c6b751ecf81e97d7f5507ee2c66525d6d498e03b79883R1) `docs/catalog-fields.md` +38 −0
- [H52](https://github.com/octavehq/lfgtm/pull/77/files#diff-91091dac2d130b347d2baa431e5947222d9998cade51d52127425086a64c7f3cR57) `scripts/validate_package.py` +18 −0

</details>

**Battlecards build on Octave's own competitor read** · feature · 4 hunks

<sub>Owners: @akash13s (6 commits to catalog.json in 6 months), @hayksaryan (5 commits to catalog.json in 6 months)</sub>

battlecard-doc reads Octave's generated battlecard, intel and deal outcomes before the library profile, then fills nine weighted parts.<details><summary>2 files →</summary>

[`skills/battlecard-doc/references/task-method.md:11-19`](https://github.com/octavehq/lfgtm/blob/875d17b3c07d134419169033c595b24571f371f2/skills/battlecard-doc/references/task-method.md#L11-L19) · [`skills/battlecard-doc/references/tool-reference.md:21-24`](https://github.com/octavehq/lfgtm/blob/875d17b3c07d134419169033c595b24571f371f2/skills/battlecard-doc/references/tool-reference.md#L21-L24)

</details>

- **Before:** A card was built from the library's competitor profile alone.
- **After:** The generated battlecard is the starting point, with intel and deal results leading the card. A card for one deal ends on one thing to say, show and ask.

<details><summary>Hunks</summary>

- [H16](https://github.com/octavehq/lfgtm/pull/77/files#diff-efb40728f97cfac4767a2a0cd5f308d3d5c84427f72b9898e02c989a7b37a13bR360) `catalog.json` +15 −1
- [H17](https://github.com/octavehq/lfgtm/pull/77/files#diff-efb40728f97cfac4767a2a0cd5f308d3d5c84427f72b9898e02c989a7b37a13bR383) `catalog.json` +6 −0
- [H62](https://github.com/octavehq/lfgtm/pull/77/files#diff-052417090ca0f930e232df2db78dfce19900ff9c50870aa3f29aaa95ffc3334eR8) `skills/battlecard-doc/references/task-method.md` +28 −0
- [H63](https://github.com/octavehq/lfgtm/pull/77/files#diff-5c59c368bd16b1da4c6325089c037df487e524f3375aa71ede82f870be6a2a41R18) `skills/battlecard-doc/references/tool-reference.md` +4 −1

</details>

**Ads gets a per-platform copy guide** · docs · 4 hunks

<sub>Owners: @akash13s (6 commits to catalog.json in 6 months), @hayksaryan (5 commits to catalog.json in 6 months)</sub>

New reference on visible field lengths and reader differences for Google Search, LinkedIn and Meta, linked from the ads method. Version 1.3.0. <sup title="inferred, not fully verified">inferred</sup>

<details><summary>Hunks</summary>

- [H11](https://github.com/octavehq/lfgtm/pull/77/files#diff-efb40728f97cfac4767a2a0cd5f308d3d5c84427f72b9898e02c989a7b37a13bR78) `catalog.json` +10 −1
- [H12](https://github.com/octavehq/lfgtm/pull/77/files#diff-efb40728f97cfac4767a2a0cd5f308d3d5c84427f72b9898e02c989a7b37a13bR96) `catalog.json` +6 −0
- [H60](https://github.com/octavehq/lfgtm/pull/77/files#diff-686c47f956c426f6a3d87898ef31c7c1680f9c6d23ed9bbb9be5d8ceda18901eR1) `skills/ads/references/platform-copy.md` +71 −0
- [H61](https://github.com/octavehq/lfgtm/pull/77/files#diff-be3c033fe360286dd5c319611ca6d399d94714a5d0ddd398d37f428c3f87e0a6R16) `skills/ads/references/task-method.md` +2 −0

</details>

**Win-loss report routes buyer questions to insights** · fix · 3 hunks

<sub>Owners: @akash13s (6 commits to catalog.json in 6 months), @hayksaryan (5 commits to catalog.json in 6 months)</sub>

The description used to send text-only questions back to the skill itself. It now points at insights. Version 1.3.2. <sup title="inferred, not fully verified">inferred</sup>

<details><summary>Hunks</summary>

- [H48](https://github.com/octavehq/lfgtm/pull/77/files#diff-efb40728f97cfac4767a2a0cd5f308d3d5c84427f72b9898e02c989a7b37a13bR2162) `catalog.json` +11 −1
- [H49](https://github.com/octavehq/lfgtm/pull/77/files#diff-efb40728f97cfac4767a2a0cd5f308d3d5c84427f72b9898e02c989a7b37a13bR2181) `catalog.json` +6 −0
- [H88](https://github.com/octavehq/lfgtm/pull/77/files#diff-8c53d9f807a52e213968152dd0866b078a8e4576fac69ff5663e1283e069074eR1) `skills/win-loss-report/SKILL.md` +1 −1

</details>

**Plugin version bump** · mechanical · 2 hunks

<sub>Owners: @akash13s (6 commits to .claude-plugin in 6 months), @arisrayelyan (4 commits to .claude-plugin in 6 months)</sub>

Plugin and marketplace versions both go to 2.22.1, kept equal as the validator requires. <sup title="inferred, not fully verified">inferred</sup>

<details><summary>Hunks</summary>

- [H1](https://github.com/octavehq/lfgtm/pull/77/files#diff-5352ee4067f17e7948e1425843f0a454e045bc8edf338f0bcf75c6804ddabd9aR13) `.claude-plugin/marketplace.json` +1 −1
- [H2](https://github.com/octavehq/lfgtm/pull/77/files#diff-037fda53525563fb89230704794a06db1150204ca28ce80697a637121c3ed3f9R1) `.claude-plugin/plugin.json` +1 −1

</details>

**README and examples describe the new behavior** · docs · 6 hunks

<sub>Owners: @arisrayelyan (6 commits to README.md in 6 months), @akash13s (4 commits to README.md in 6 months)</sub>

Skill table rows and usage examples for lookalike prospecting, cohort abm, document and magazine. <sup title="inferred, not fully verified">inferred</sup>

<details><summary>Hunks</summary>

- [H3](https://github.com/octavehq/lfgtm/pull/77/files#diff-30bf75f8f19e56642c61ecaa902d4d6a0a0126a234b800d76b79a7f1faab8be2R426) `EXAMPLES.md` +4 −0
- [H4](https://github.com/octavehq/lfgtm/pull/77/files#diff-30bf75f8f19e56642c61ecaa902d4d6a0a0126a234b800d76b79a7f1faab8be2R714) `EXAMPLES.md` +3 −0
- [H5](https://github.com/octavehq/lfgtm/pull/77/files#diff-b335630551682c19a781afebcf4d07bf978fb1f8ac04c6bf87428ed5106870f5R93) `README.md` +2 −2
- [H6](https://github.com/octavehq/lfgtm/pull/77/files#diff-b335630551682c19a781afebcf4d07bf978fb1f8ac04c6bf87428ed5106870f5R124) `README.md` +2 −0
- [H7](https://github.com/octavehq/lfgtm/pull/77/files#diff-b335630551682c19a781afebcf4d07bf978fb1f8ac04c6bf87428ed5106870f5R219) `README.md` +3 −0
- [H8](https://github.com/octavehq/lfgtm/pull/77/files#diff-b335630551682c19a781afebcf4d07bf978fb1f8ac04c6bf87428ed5106870f5R279) `README.md` +3 −1

</details>


<sub>Every hunk is covered by a theme.</sub>

### Blast radius

Medium: no data changes, but two skills change their default behavior with no recorded run, and the app reads the new fields.

**Callers and dependents**
- The release ZIP build and the validate workflow (used by publish and sync) now also fail on bad offering fields or a changelog not newest-first. They pass at head.<details><summary>3 files →</summary>

[`scripts/build-release.py:11-12`](https://github.com/octavehq/lfgtm/blob/875d17b3c07d134419169033c595b24571f371f2/scripts/build-release.py#L11-L12) · [`.github/workflows/validate.yml:25`](https://github.com/octavehq/lfgtm/blob/875d17b3c07d134419169033c595b24571f371f2/.github/workflows/validate.yml#L25) · [`scripts/validate.sh:5`](https://github.com/octavehq/lfgtm/blob/875d17b3c07d134419169033c595b24571f371f2/scripts/validate.sh#L5)

</details>

<sub>None found: irreversible, endpoints, jobs and workers, tables and data.</sub>

**Uses of the changed code** · checked 16 of 16 uses of the changed code

<sub>Other repositories: searched octavehq's code for 1 changed name; no other repository uses them. octavehq/ask-octave-skills wasn't searched: git@github.com: Permission denied (publickey). octavehq/demo-warehouse-content wasn't searched: git@github.com: Permission denied (publickey). octavehq/docs wasn't searched: git@github.com: Permission denied (publickey). octavehq/lfgtm-codex wasn't searched: git@github.com: Permission denied (publickey).</sub>

- 🟡 affected · `validate` · 16 sites: The release ZIP build and the validate workflow (used by publish and sync) now also fail on bad offering fields or a changelog not newest-first. They pass at head.<details><summary>3 files →</summary>

[`scripts/build-release.py:11-12`](https://github.com/octavehq/lfgtm/blob/875d17b3c07d134419169033c595b24571f371f2/scripts/build-release.py#L11-L12) · [`.github/workflows/validate.yml:25`](https://github.com/octavehq/lfgtm/blob/875d17b3c07d134419169033c595b24571f371f2/.github/workflows/validate.yml#L25) · [`scripts/validate.sh:5`](https://github.com/octavehq/lfgtm/blob/875d17b3c07d134419169033c595b24571f371f2/scripts/validate.sh#L5)

</details>

### Why this risk level

- With no criteria given, prospector now starts from lookalikes of recent won deals instead of library criteria.<details><summary>2 files →</summary>

[`skills/prospector/SKILL.md:12`](https://github.com/octavehq/lfgtm/blob/875d17b3c07d134419169033c595b24571f371f2/skills/prospector/SKILL.md#L12) · [`skills/prospector/references/task-method.md:3-4`](https://github.com/octavehq/lfgtm/blob/875d17b3c07d134419169033c595b24571f371f2/skills/prospector/references/task-method.md#L3-L4)

</details>
- The validator checks catalog field values and changelog order but doesn't load or check the new data shape files.<details><summary>1 file →</summary>

[`scripts/validate_package.py:54-77`](https://github.com/octavehq/lfgtm/blob/875d17b3c07d134419169033c595b24571f371f2/scripts/validate_package.py#L54-L77)

</details>

### Merge readiness

| | Status | Detail |
|---|---|---|
| CI | ✅ passing | All 1 checks passing. |
| Tests | ❌ missing | 0 of 6 decisions have a test that would fail if it were reverted. |
| Owners | @akash13s, @hayksaryan, @arisrayelyan | From git history: who committed to these files in the 6 months before the PR. |

<details><summary>Brief quality checks</summary>

- Coverage: 88/88 hunks in themes, 0 marked unexplained
- Claims: 13 checked ✓, 8 inferred ~
- Evidence links: 47/47 point at real lines
- Schema: valid
- Investigators: 1 traced the affected uses; 1 new finding, 0 duplicates dropped

</details>

<sub>PRevue · claude-opus-5-5 (high) · 2 turns · 0.9 min · run locally by @jtemps · head 875d17b · ✓ checked against the code, ~ inferred</sub>