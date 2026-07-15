# Google Ads Editor — Import Format

Single-file import format for the Google Ads Editor desktop app. All entity types (campaigns, ad groups, ads, keywords) live in one file with a unified 144-column header.

## Format

- **Encoding**: UTF-16 (with BOM)
- **Delimiter**: Tab-separated (NOT comma-separated, despite `.csv` extension)
- **No Row Type column** — the Editor infers entity type from which columns are populated
- **No Action column** — the Editor determines add/edit from whether the entity exists
- **No Customer ID column** — imports into whatever account is currently open in the Editor

## Key Value Differences from Web UI Format

| Field | Web UI Value | Ads Editor Value |
|-------|-------------|-----------------|
| EU political ads | `No` | `Doesn't have EU political ads` |
| Languages | `en` (same) | `en` |
| Campaign Status | N/A (inferred) | `Paused` or `Enabled` (column 139) |
| Ad Group Status | N/A (inferred) | `Enabled` or `Paused` (column 140) |
| Ad status | N/A (inferred) | `Enabled` or `Paused` (column 141, "Status") |
| Match type | `Broad match` | Keyword column contains the text directly |

## Header (144 columns)

```
Campaign	Labels	Campaign Type	Networks	Budget	Budget type	EU political ads	Standard conversion goals	Custom conversion goal	Customer acquisition	Languages	Bid Strategy Type	Bid Strategy Name	Target CPA	Start Date	End Date	Broad match keywords	Ad Schedule	Ad rotation	Content exclusions	Targeting method	Exclusion method	Audience targeting	Flexible Reach	AI Max	Text customization	Final URL expansion	Tracking template	Ad Group	Max CPC	Max CPM	Max CPV	Target CPV	Percent CPC	Target CPM	Target ROAS	Target CPC	Desktop Bid Modifier	Mobile Bid Modifier	Tablet Bid Modifier	TV Screen Bid Modifier	Display Network Custom Bid Type	Optimized targeting	Strict age and gender targeting	Search term matching	Ad Group Type	Channels	Audience name	Age demographic	Gender demographic	Income demographic	Parental status demographic	Remarketing audience segments	Interest categories	Life events	Custom audience segments	Detailed demographics	Remarketing audience exclusions	Final URL suffix	Custom parameters	ID	Audience segment	Bid Modifier	Final URL	Final mobile URL	Age	Criterion Type	Household income	Location	Reach	Location groups	Radius	Unit	Asset name	Folder	Source	Image Size	File size	Account keyword type	Keyword	First page bid	Top of page bid	First position bid	Quality score	Landing page experience	Expected CTR	Ad relevance	Link source	Business name	Ad type	Headline 1	Headline 1 position	Headline 2	Headline 2 position	Headline 3	Headline 3 position	Headline 4	Headline 4 position	Headline 5	Headline 5 position	Headline 6	Headline 6 position	Headline 7	Headline 7 position	Headline 8	Headline 8 position	Headline 9	Headline 9 position	Headline 10	Headline 10 position	Headline 11	Headline 11 position	Headline 12	Headline 12 position	Headline 13	Headline 13 position	Headline 14	Headline 14 position	Headline 15	Headline 15 position	Description 1	Description 1 position	Description 2	Description 2 position	Description 3	Description 3 position	Description 4	Description 4 position	Path 1	Path 2	Link Text	Description Line 1	Description Line 2	Upgraded extension	Callout text	Account settings	Inventory type	Auto tagging	Campaign Status	Ad Group Status	Status	Approval Status	Ad strength	Comment
```

## Entity Types

The Editor determines what kind of entity each row represents based on which columns are populated. All other columns are left empty (but tabs must still be present).

### Campaign Row

| Column # | Column Name | Value | Notes |
|----------|-------------|-------|-------|
| 1 | Campaign | Campaign name | |
| 3 | Campaign Type | `Search` | |
| 4 | Networks | `Google search` | |
| 5 | Budget | `100.00` | Daily budget |
| 6 | Budget type | `Daily` | |
| 7 | EU political ads | `Doesn't have EU political ads` | **Required — import fails without this** |
| 11 | Languages | `en` | NOT `English` |
| 12 | Bid Strategy Type | `Maximize Conversions` | Or `Manual CPC` |
| 139 | Campaign Status | `Paused` | Always start paused |

### Ad Group Row

| Column # | Column Name | Value | Notes |
|----------|-------------|-------|-------|
| 1 | Campaign | Campaign name | Must match campaign row exactly |
| 29 | Ad Group | Ad group name | |
| 30 | Max CPC | `3.00` | CPC bid |
| 139 | Campaign Status | `Paused` | Must match campaign |
| 140 | Ad Group Status | `Enabled` | |

### Responsive Search Ad Row

| Column # | Column Name | Value | Notes |
|----------|-------------|-------|-------|
| 1 | Campaign | Campaign name | Must match exactly |
| 29 | Ad Group | Ad group name | Must match exactly |
| 64 | Final URL | `https://example.com` | Landing page |
| 90 | Ad type | `Responsive search ad` | **Required** |
| 91 | Headline 1 | Headline text | Max 30 chars |
| 93 | Headline 2 | Headline text | Max 30 chars |
| 95 | Headline 3 | Headline text | Max 30 chars |
| 97 | Headline 4 | Headline text | Max 30 chars |
| 99 | Headline 5 | Headline text | **Minimum 5 headlines required** |
| 121 | Description 1 | Description text | Max 90 chars |
| 123 | Description 2 | Description text | **Minimum 2 descriptions** |
| 129 | Path 1 | Display path | Max 15 chars |
| 130 | Path 2 | Display path | Max 15 chars |
| 139 | Campaign Status | `Paused` | |
| 140 | Ad Group Status | `Enabled` | |
| 141 | Status | `Enabled` | Ad-level status |

**Headline positions** (columns 92, 94, 96, etc.): Leave empty to let Google rotate freely. Set to `1`, `2`, or `3` to pin a headline to that position.

### Keyword Row

| Column # | Column Name | Value | Notes |
|----------|-------------|-------|-------|
| 1 | Campaign | Campaign name | Must match exactly |
| 29 | Ad Group | Ad group name | Must match exactly |
| 80 | Keyword | Keyword text | e.g., `AI GTM platform` |
| 139 | Campaign Status | `Paused` | |
| 140 | Ad Group Status | `Enabled` | |

**Note**: Match type is not a separate column in the Editor format. By default keywords are broad match. For phrase match, wrap in quotes: `"AI GTM platform"`. For exact match, wrap in brackets: `[AI GTM platform]`.

## Row Order

Rows must appear in dependency order:
1. Campaign rows
2. Ad group rows
3. Ad rows
4. Keyword rows

## Generation (CRITICAL)

Claude cannot directly write UTF-16 tab-separated files. **Use a Bash tool call with Python** to generate the file:

```python
python3 << 'PYEOF'
import csv, io

headers = [...]  # Full 144-column header list (see below)

def make_row(data):
    row = [''] * len(headers)
    for col, val in data.items():
        row[headers.index(col)] = val
    return row

rows = []
# ... build rows using make_row({...}) ...

output = io.StringIO()
writer = csv.writer(output, delimiter='\t')
writer.writerow(headers)
for row in rows:
    writer.writerow(row)

with open('campaign-name.csv', 'w', encoding='utf-16') as f:
    f.write(output.getvalue())
PYEOF
```

The full 144-element headers list for use in the Python script:

```python
headers = ['Campaign','Labels','Campaign Type','Networks','Budget','Budget type','EU political ads','Standard conversion goals','Custom conversion goal','Customer acquisition','Languages','Bid Strategy Type','Bid Strategy Name','Target CPA','Start Date','End Date','Broad match keywords','Ad Schedule','Ad rotation','Content exclusions','Targeting method','Exclusion method','Audience targeting','Flexible Reach','AI Max','Text customization','Final URL expansion','Tracking template','Ad Group','Max CPC','Max CPM','Max CPV','Target CPV','Percent CPC','Target CPM','Target ROAS','Target CPC','Desktop Bid Modifier','Mobile Bid Modifier','Tablet Bid Modifier','TV Screen Bid Modifier','Display Network Custom Bid Type','Optimized targeting','Strict age and gender targeting','Search term matching','Ad Group Type','Channels','Audience name','Age demographic','Gender demographic','Income demographic','Parental status demographic','Remarketing audience segments','Interest categories','Life events','Custom audience segments','Detailed demographics','Remarketing audience exclusions','Final URL suffix','Custom parameters','ID','Audience segment','Bid Modifier','Final URL','Final mobile URL','Age','Criterion Type','Household income','Location','Reach','Location groups','Radius','Unit','Asset name','Folder','Source','Image Size','File size','Account keyword type','Keyword','First page bid','Top of page bid','First position bid','Quality score','Landing page experience','Expected CTR','Ad relevance','Link source','Business name','Ad type','Headline 1','Headline 1 position','Headline 2','Headline 2 position','Headline 3','Headline 3 position','Headline 4','Headline 4 position','Headline 5','Headline 5 position','Headline 6','Headline 6 position','Headline 7','Headline 7 position','Headline 8','Headline 8 position','Headline 9','Headline 9 position','Headline 10','Headline 10 position','Headline 11','Headline 11 position','Headline 12','Headline 12 position','Headline 13','Headline 13 position','Headline 14','Headline 14 position','Headline 15','Headline 15 position','Description 1','Description 1 position','Description 2','Description 2 position','Description 3','Description 3 position','Description 4','Description 4 position','Path 1','Path 2','Link Text','Description Line 1','Description Line 2','Upgraded extension','Callout text','Account settings','Inventory type','Auto tagging','Campaign Status','Ad Group Status','Status','Approval Status','Ad strength','Comment']
```

## Validation Checklist

1. **File is UTF-16 encoded** — not UTF-8, not ASCII
2. **Fields are tab-separated** — not comma-separated
3. **Every row has exactly 144 tab-separated fields** (143 tabs per row)
4. **No Row Type or Action columns** — entity type is inferred
5. **EU political ads** = `Doesn't have EU political ads` (not `No`)
6. **Languages** = `en` (not `English`)
7. **RSA ads have at least 5 headlines and 2 descriptions**
8. **Campaign name matches exactly** across campaign, ad group, ad, and keyword rows
9. **Rows are in dependency order**: campaigns → ad groups → ads → keywords
10. **Campaign Status is `Paused`** for all rows (nothing runs until explicitly enabled)
