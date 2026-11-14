# Prospect results

Company-only rows: returned account identity/domain; offering/motion; fit reasoning; actual qualification status and available subscores; hard disqualifiers; unknowns; source/date; next validation/action.

Company-plus-contact adds discovered/enriched person ID/profile, name/title, identity source, and role evidence. Verified identity is distinct from a confirmed buying role. Discover these people before output.

Return unique eligible requested N or a shortfall with searched/returned/qualified counts and applied/unresolved exclusions. Create an actual UTF-8 CSV using a standard CSV writer and round-trip parse it. If files are unavailable, label the result CSV text; do not claim a file exists.

## Data it returns

When the run is asked for data beside its document (the skill's `output.schema.json`), return the same rows the results show, in the same order, as two flat lists. `accounts` has one row per account: name, domain, logo, industry, employee count, founded year, city, country code, the qualification's actual result and score, and one sentence of fit reasoning. `contacts` has one row per person discovered, pointing at their account by `companyDomain`: name, title, profile link, photo, location, an email only when a tool returned one, and one sentence on why this person. Copy each value exactly as a tool returned it; leave out or null what no tool returned. Leave `contacts` empty for company-only results. State a shortfall in `shortfall` in plain words, with the number asked for in `requested`. If the host refuses the data as too large, drop the lowest-ranked rows, say how many in `shortfall`, and keep the document complete.
