# Google Ads — CSV Export Format

This reference defines the exact CSV format for bulk upload to Google Ads. The **web UI** (Tools → Bulk Actions → Uploads) uses **separate CSV files per entity type**, each with its own column layout. Generate one file per entity type and upload them in dependency order.

**Before generating**, ask the user for their Google Ads **Customer ID** (the account number in the Google Ads header, e.g., `123-456-7890`). Format it **with dashes** in the CSV: `123-456-7890`. **The Customer ID must match the specific account they'll upload to** — using an MCC/manager account ID instead of the child account ID causes "entity does not exist" errors.

## CSV Quoting Rules (CRITICAL)

**Double-quote EVERY field.** This prevents column shifts from pipes (`|`), apostrophes (`'`), em dashes (`—`), and other special characters. Escape double quotes inside fields by doubling them: `"` → `""`.

## Upload Order

Upload files in this order (each depends on the previous):
1. Campaign CSV
2. Ad group CSV
3. Responsive Search Ad CSV
4. Keyword CSV
5. Negative keyword CSV

Wait for each upload to succeed before uploading the next. If the campaign upload fails, all subsequent uploads will fail with "entity does not exist."

---

## 1. Campaign CSV

**Filename**: `{campaign-name}-campaigns.csv`

### Header
```
Row Type,Action,Campaign status,Customer ID,Campaign ID,Campaign,Campaign type,Networks,Budget,Delivery method,Budget type,Bid strategy type,Bid strategy,Campaign start date,Campaign end date,Language,Location,Exclusion,Devices,Label,Target CPA,Target ROAS,Display URL option,Website description,Target Impression Share,Max CPC Bid Limit for Target IS,Location Goal for Target IS,Tracking template,Final URL suffix,Custom parameter,Inventory type,Campaign subtype,Video ad formats,EU political ads
```

### Required Fields
| Column | Value | Notes |
|--------|-------|-------|
| Row Type | `Campaign` | |
| Action | `Add` | Use `Edit` if campaign already exists |
| Campaign status | `Paused` | Always start paused for review |
| Customer ID | `123-456-7890` | With dashes |
| Campaign | Campaign name | Must be unique in account |
| Campaign type | `Search` | |
| Budget | `50.00` | Daily budget |
| Budget type | `Daily` | |
| Bid strategy type | `Maximize Conversions` | Or `Manual CPC` |
| Language | `en` | |
| Location | `United States` | |
| EU political ads | `No` | **REQUIRED — upload fails without this** |

### Example
```
"Row Type","Action","Campaign status","Customer ID","Campaign ID","Campaign","Campaign type","Networks","Budget","Delivery method","Budget type","Bid strategy type","Bid strategy","Campaign start date","Campaign end date","Language","Location","Exclusion","Devices","Label","Target CPA","Target ROAS","Display URL option","Website description","Target Impression Share","Max CPC Bid Limit for Target IS","Location Goal for Target IS","Tracking template","Final URL suffix","Custom parameter","Inventory type","Campaign subtype","Video ad formats","EU political ads"
"Campaign","Add","Paused","123-456-7890","","Acme | Compliance Automation","Search","Google search","50.00","Standard","Daily","Maximize Conversions","","","","en","United States","","","","","","","","","","","","","","","","","No"
```

---

## 2. Ad Group CSV

**Filename**: `{campaign-name}-ad-groups.csv`

### Header
```
Row Type,Action,Ad group status,Customer ID,Campaign ID,Campaign,Ad group ID,Ad group,Ad group type,Ad rotation,Default max. CPC,CPC%,Max. CPM,Max. CPV,Target CPA,Target CPM,TrueView target CPV,Label,Tracking template,Final URL suffix,Custom parameter,Target ROAS
```

### Required Fields
| Column | Value | Notes |
|--------|-------|-------|
| Row Type | `Ad group` | |
| Action | `Add` | |
| Ad group status | `Enabled` | |
| Customer ID | `123-456-7890` | With dashes |
| Campaign | Campaign name | Must match campaign CSV exactly |
| Ad group | Ad group name | One per persona/segment |
| Default max. CPC | `3.00` | Or appropriate bid |

### Example
```
"Row Type","Action","Ad group status","Customer ID","Campaign ID","Campaign","Ad group ID","Ad group","Ad group type","Ad rotation","Default max. CPC","CPC%","Max. CPM","Max. CPV","Target CPA","Target CPM","TrueView target CPV","Label","Tracking template","Final URL suffix","Custom parameter","Target ROAS"
"Ad group","Add","Enabled","123-456-7890","","Acme | Compliance Automation","","VP Engineering — Mid-Market FinServ","","","3.00","","","","","","","","","","",""
```

---

## 3. Responsive Search Ad CSV

**Filename**: `{campaign-name}-ads.csv`

### Header (first 2 rows are comments, row 3 is the actual header)
```
# Assets can be shown in any order, so make sure that they make sense individually or in combination, and don't violate our policies or local law.
# IMPORTANT: For each responsive search ad, provide at least 5 distinct headlines that do not repeat the same or similar phrases. Providing redundant headlines will restrict our ability to generate combinations.
Row Type,Action,Ad status,Customer ID,Campaign ID,Campaign,Ad group ID,Ad group,Ad ID,Ad type,Label,Headline 1,Headline 2,Headline 3,Headline 4,Headline 5,Headline 6,Headline 7,Headline 8,Headline 9,Headline 10,Headline 11,Headline 12,Headline 13,Headline 14,Headline 15,Description 1,Description 2,Description 3,Description 4,Headline 1 position,Headline 2 position,Headline 3 position,Headline 4 position,Headline 5 position,Headline 6 position,Headline 7 position,Headline 8 position,Headline 9 position,Headline 10 position,Headline 11 position,Headline 12 position,Headline 13 position,Headline 14 position,Headline 15 position,Description 1 position,Description 2 position,Description 3 position,Description 4 position,Path 1,Path 2,Final URL,Mobile final URL,Tracking template,Final URL suffix,Custom parameter
```

### Required Fields
| Column | Value | Notes |
|--------|-------|-------|
| Row Type | `Ad` | |
| Action | `Add` | |
| Ad status | `Enabled` | |
| Customer ID | `123-456-7890` | With dashes |
| Campaign | Campaign name | Must match exactly |
| Ad group | Ad group name | Must match exactly |
| Ad type | `Responsive search ad` | **REQUIRED** |
| Headline 1–5 | Headline text | **Minimum 5 distinct headlines required.** Max 30 chars each. |
| Headline 6–15 | Headline text | Optional. Max 30 chars each. |
| Description 1–2 | Description text | **Minimum 2 required.** Max 90 chars each. |
| Description 3–4 | Description text | Optional. Max 90 chars each. |
| Path 1 | Display path | Optional. Max 15 chars. e.g., `Compliance` |
| Path 2 | Display path | Optional. Max 15 chars. e.g., `Platform` |
| Final URL | Landing page | Full URL with `https://` |

**Headline/Description positions** (optional): Pin a headline to position 1, 2, or 3. Pin a description to position 1 or 2. Leave empty to let Google rotate freely (recommended).

### Example
```
"# Assets can be shown in any order, so make sure that they make sense individually or in combination, and don't violate our policies or local law."
"# IMPORTANT: For each responsive search ad, provide at least 5 distinct headlines that do not repeat the same or similar phrases."
"Row Type","Action","Ad status","Customer ID","Campaign ID","Campaign","Ad group ID","Ad group","Ad ID","Ad type","Label","Headline 1","Headline 2","Headline 3","Headline 4","Headline 5","Headline 6","Headline 7","Headline 8","Headline 9","Headline 10","Headline 11","Headline 12","Headline 13","Headline 14","Headline 15","Description 1","Description 2","Description 3","Description 4","Headline 1 position","Headline 2 position","Headline 3 position","Headline 4 position","Headline 5 position","Headline 6 position","Headline 7 position","Headline 8 position","Headline 9 position","Headline 10 position","Headline 11 position","Headline 12 position","Headline 13 position","Headline 14 position","Headline 15 position","Description 1 position","Description 2 position","Description 3 position","Description 4 position","Path 1","Path 2","Final URL","Mobile final URL","Tracking template","Final URL suffix","Custom parameter"
"Ad","Add","Enabled","123-456-7890","","Acme | Compliance Automation","","VP Engineering — Mid-Market FinServ","","Responsive search ad","","Still Prepping Audits By Hand?","Automate Audit Workflow","See How It Works","Cut Audit Prep By 90%","Book a Demo Today","","","","","","","","","","","Stop spending weeks on manual audit prep. Acme automates the entire workflow.","Join 200+ FinServ teams who eliminated audit fire drills. Book a demo today.","","","","","","","","","","","","","","","","","","","","Compliance","Platform","https://example.com","","","",""
```

---

## 4. Keyword CSV

**Filename**: `{campaign-name}-keywords.csv`

### Header
```
Row Type,Action,Customer ID,Keyword status,Campaign ID,Campaign,Ad group ID,Ad group,Keyword ID,Keyword,Type,Label,Default max. CPC,Max. CPV,Final URL,Mobile final URL,Final URL suffix,Tracking template,Custom parameter
```

### Required Fields
| Column | Value | Notes |
|--------|-------|-------|
| Row Type | `Keyword` | |
| Action | `Add` | |
| Customer ID | `123-456-7890` | With dashes |
| Campaign | Campaign name | Must match exactly |
| Ad group | Ad group name | Must match exactly |
| Keyword | Keyword text | e.g., `compliance automation platform` |
| Type | `Broad match`, `Phrase match`, or `Exact match` | **REQUIRED — full words, not abbreviations** |

### Example
```
"Row Type","Action","Customer ID","Keyword status","Campaign ID","Campaign","Ad group ID","Ad group","Keyword ID","Keyword","Type","Label","Default max. CPC","Max. CPV","Final URL","Mobile final URL","Final URL suffix","Tracking template","Custom parameter"
"Keyword","Add","123-456-7890","","","Acme | Compliance Automation","","VP Engineering — Mid-Market FinServ","","compliance automation platform","Broad match","","","","","","","",""
"Keyword","Add","123-456-7890","","","Acme | Compliance Automation","","VP Engineering — Mid-Market FinServ","","audit preparation software","Broad match","","","","","","","",""
```

---

## 5. Negative Keyword CSV

**Filename**: `{campaign-name}-negative-keywords.csv`

### Header
```
Row Type,Action,Keyword status,Customer ID,Level,Campaign ID,Campaign,Ad group ID,Ad group,Keyword ID,Negative keyword,Type
```

### Required Fields
| Column | Value | Notes |
|--------|-------|-------|
| Row Type | `Negative keyword` | |
| Action | `Add` | |
| Customer ID | `123-456-7890` | With dashes |
| Level | `Ad group` or `Campaign` | Scope of the negative |
| Campaign | Campaign name | Must match exactly |
| Ad group | Ad group name | Required if Level = `Ad group` |
| Negative keyword | Keyword text | e.g., `free` |
| Type | `Broad match`, `Phrase match`, or `Exact match` | **REQUIRED — full words** |

### Example
```
"Row Type","Action","Keyword status","Customer ID","Level","Campaign ID","Campaign","Ad group ID","Ad group","Keyword ID","Negative keyword","Type"
"Negative keyword","Add","","123-456-7890","Ad group","","Acme | Compliance Automation","","VP Engineering — Mid-Market FinServ","","free","Broad match"
"Negative keyword","Add","","123-456-7890","Ad group","","Acme | Compliance Automation","","VP Engineering — Mid-Market FinServ","","tutorial","Broad match"
```

---

## Validation Checklist

Before writing CSV files, verify:

1. **Each entity type is in its own CSV file** with the correct column layout
2. **Every field is double-quoted** to prevent column shifts
3. **Double quotes inside fields are escaped** by doubling: `"` → `""`
4. **Customer ID uses dashes**: `123-456-7890` not `1234567890`
5. **Campaign has `EU political ads` = `No`** — upload fails without this
6. **RSA ads have at least 5 distinct headlines and 2 descriptions** — Google rejects ads with fewer
7. **Ad type is `Responsive search ad`** — not omitted
8. **Keyword Type uses full words**: `Broad match` not `Broad`
9. **Negative keywords have a `Level`**: `Ad group` or `Campaign`
10. **Campaign names match exactly** across all files (including pipes, dashes, spaces)
11. **Headlines ≤ 30 chars, Descriptions ≤ 90 chars, Paths ≤ 15 chars**

## File Encoding

- UTF-8 (with or without BOM)
- Line endings: CRLF or LF both accepted
- File extension: `.csv`
