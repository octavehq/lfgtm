#!/usr/bin/env python3
"""Public changelog: deterministic page render and publish checks.

Octave's release-notes ingestion re-reads the public changelog on a schedule,
converts it to markdown and diffs it as a SET OF LINES: every line it has not
seen before is treated as a newly shipped capability and proposed as a library
update. So the page is rendered from a small state file, never authored by
hand, and a publish is refused unless every line already live survives
byte-identical. The live page is the lock.

  changelog.py init      --title T --dek D --footer F --out changelog.json
  changelog.py bootstrap --html index.html --out changelog.json
  changelog.py add       --state changelog.json --entries new.json --out DIR
                         [--html current/index.html] [--tokens tokens.css]
                         [--logo-light a.png --logo-dark b.png]
                         [--published-at YYYY-MM-DD]
  changelog.py lines     --html index.html [--expect-state changelog.json]

A new entry is fielded (description, use case, problem, novelty). An entry
published as one paragraph before that keeps its shape unless the paste lists
it under `reshape` (its paragraph is replaced by fields) or `remove` (it comes
off the page). Those are the only live lines a publish may change; every other
one must survive.

`add` writes DIR/index.html and DIR/changelog.json (the whole bundle) plus
DIR.manifest.json beside DIR for the public upload. It writes nothing when a
check fails. Exit 0 = ok, 1 = refused or invalid input.
"""
import argparse
import base64
import json
import re
import sys
from datetime import date as Date, datetime, timezone
from html.parser import HTMLParser
from pathlib import Path

# Version 2 added the fielded entry; a version 1 state holds only paragraph
# entries and is read as-is, then written back as version 2.
SCHEMA_VERSION = 2
READABLE_SCHEMA_VERSIONS = {1, 2}
TITLE_MAX_CHARS = 120

# A new entry is fielded: a description, then one labeled line per field. Each
# label is part of the line the crawl reads, so the wording is permanent.
FIELD_LABELS = [('useCase', 'Use case:'), ('problem', 'Problem it solves:')]
TEXT_FIELDS = ['description'] + [key for key, _ in FIELD_LABELS]
# Shown as a badge drawn by the stylesheet, never as page text: "New" on every
# other entry would be a repeated line, which the crawl swallows.
NOVELTY_BADGES = {'net-new': 'New', 'improvement': 'Improvement'}
# Mirrors the ingestion's delta floor and cap. Additions under the floor are
# recorded as a sync and fire no extraction, so they reach readers and never
# reach the library; over the cap the delta is truncated mid-line.
DELTA_MIN_CHARS = 40
DELTA_MAX_CHARS = 100_000
BUNDLE_FILES = ['index.html', 'changelog.json']

# Locale-independent on purpose: a month heading that changes shape between two
# operators' machines is a whole month re-extracted as new.
MONTH_NAMES = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
               'August', 'September', 'October', 'November', 'December']

DATE_RE = re.compile(r'^\d{4}-\d{2}-\d{2}$')
ID_RE = re.compile(r'^[a-z0-9][a-z0-9-]{0,127}$')
HEADING_RE = re.compile(r'^### (\d{4}-\d{2}-\d{2}) — (.+)$')
# Markdown-significant characters at the start of a line. The converter escapes
# these unpredictably, and an escape that changes between converter versions
# re-emits the line as new.
LEAD_HAZARD = re.compile(r'^\s*(#|-|\*|>|\||\d+\.)')
# Text that changes on its own between two crawls of an unchanged page.
VOLATILE = [
    (re.compile(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}'), 'an ISO timestamp'),
    (re.compile('©'), 'a copyright glyph'),
    (re.compile(r'last updated', re.I), '"last updated"'),
    (re.compile(r'generated (on|at)', re.I), '"generated on/at"'),
    (re.compile(r'<script', re.I), 'a <script> tag'),
    (re.compile(r'<iframe', re.I), 'an <iframe> tag'),
    (re.compile(r'<noscript', re.I), 'a <noscript> tag'),
    (re.compile(r'\son[a-z]+\s*=', re.I), 'an inline event handler'),
]
# Links become child Resources under shallow-domain crawling, and anything
# fetched from elsewhere becomes part of what the crawl diffs.
LINK_RE = re.compile(r'\shref\s*=', re.I)
EXTERNAL_FETCH_RE = re.compile(
    r'<link[^>]+rel=["\']?stylesheet|@import|src\s*=\s*["\']?https?:|url\(\s*["\']?(?:https?:)?//', re.I)


class Refused(Exception):
    """A problem the operator has to fix; the message is shown as-is."""


# --------------------------------------------------------------------------
# State
# --------------------------------------------------------------------------

def load_state(path):
    try:
        state = json.loads(Path(path).read_text(encoding='utf-8'))
    except (OSError, ValueError) as error:
        raise Refused(f'Could not read the changelog state at {path}: {error}')
    if not isinstance(state, dict) or state.get('schemaVersion') not in READABLE_SCHEMA_VERSIONS:
        raise Refused(f'{path} is not a changelog state this skill can read (schemaVersion 1 or 2).')
    page = state.get('page')
    if not isinstance(page, dict) or not all(isinstance(page.get(k), str) and page[k].strip() for k in ('title', 'dek', 'footer')):
        raise Refused(f'{path} has no page title, dek and footer.')
    if not isinstance(state.get('entries'), list):
        raise Refused(f'{path} has no entries list.')
    if not isinstance(state.get('removed', []), list):
        raise Refused(f'{path} has a removed list that is not a list.')
    return state


def dump_json(value):
    return json.dumps(value, indent=2, ensure_ascii=False) + '\n'


def slug(text, limit=60):
    value = re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')
    return value[:limit].rstrip('-') or 'entry'


# --------------------------------------------------------------------------
# Render
# --------------------------------------------------------------------------

def escape(value):
    """The same four replacements the page has always used, so re-rendering an
    existing page reproduces its markup byte for byte."""
    return value.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')


def month_heading(date):
    """'2026-08-20' -> 'August 2026', parsed by hand so no timezone can move it."""
    year, month, _ = date.split('-')
    return f'{MONTH_NAMES[int(month) - 1]} {year}'


def is_fielded(entry):
    """Paragraph entries (everything published before the fielded shape) carry
    `body`; fielded ones carry `description`. A live paragraph entry is only
    converted when a reviewer approved its reshape on staging."""
    return 'description' in entry


def entry_lines(entry):
    """The crawl lines one entry yields, after its heading.

      {'body': 'Motion Playbooks let…'}                      -> ['Motion Playbooks let…']
      {'description': 'X does Y.', 'useCase': 'A rep…',
       'problem': 'Reps had to…'}                            -> ['X does Y.', 'Use case: A rep…',
                                                                 'Problem it solves: Reps had to…']
    """
    if not is_fielded(entry):
        return [entry['body']]
    return [entry['description']] + [f'{label} {entry[key]}' for key, label in FIELD_LABELS]


def sorted_entries(state):
    """Newest date first. Python's sort is stable, so entries sharing a date keep
    their stored order and never swap places between renders."""
    return sorted(state['entries'], key=lambda entry: entry['date'], reverse=True)


def render_lines(state):
    """Every line the crawl derives from the page, in order."""
    page = state['page']
    lines = [f'# {page["title"]}', page['dek']]
    current = None
    for entry in sorted_entries(state):
        heading = month_heading(entry['date'])
        if heading != current:
            current = heading
            lines.append(f'## {heading}')
        lines += [f'### {entry["date"]} — {entry["title"]}', *entry_lines(entry)]
    lines.append(page['footer'])
    return lines


def render_html(state, style):
    """The page. Every element is chosen so its markdown equals render_lines():
    the month is a real <h2>, the date stays fused into the <h3>, and the logo is
    a background image on an aria-hidden div, carrying no text and no href."""
    page = state['page']
    body = []
    current = None
    for entry in sorted_entries(state):
        heading = month_heading(entry['date'])
        if heading != current:
            if current is not None:
                body.append('</section>')
            current = heading
            body += ['<section class="cl-group">',
                     f'<div class="cl-group-head"><h2 class="cl-eyebrow">{escape(heading)}</h2></div>']
        if is_fielded(entry):
            # The label is a span, not <strong>: markdown converters render
            # emphasis differently across versions, and a line that changes
            # shape between two crawls is re-read as new.
            body += [f'<article class="cl-entry" data-novelty="{escape(entry["novelty"])}">',
                     f'<h3>{escape(entry["date"])} — {escape(entry["title"])}</h3>',
                     f'<p>{escape(entry["description"])}</p>',
                     *[f'<p class="cl-field"><span class="cl-label">{escape(label)}</span> {escape(entry[key])}</p>'
                       for key, label in FIELD_LABELS],
                     '</article>']
        else:
            body += ['<article class="cl-entry">',
                     f'<h3>{escape(entry["date"])} — {escape(entry["title"])}</h3>',
                     f'<p>{escape(entry["body"])}</p>',
                     '</article>']
    if current is not None:
        body.append('</section>')
    return '\n'.join([
        '<!DOCTYPE html>',
        '<html lang="en">',
        '<head>',
        '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        f'<title>{escape(page["title"])}</title>',
        f'<style>{style}</style>',
        '</head>',
        '<body>',
        '<header class="cl-top"><div class="cl-logo" aria-hidden="true"></div></header>',
        '<section class="cl-hero">',
        f'<h1>{escape(page["title"])}</h1>',
        f'<p class="cl-dek">{escape(page["dek"])}</p>',
        '</section>',
        '<main class="cl-wrap">',
        *body,
        '</main>',
        f'<footer class="cl-foot"><div>{escape(page["footer"])}</div></footer>',
        '</body>',
        '</html>',
        '',
    ])


# The layout for a new page. It reads the workspace brand kit's --brand-*
# tokens (inlined ahead of it) and falls back to a neutral palette without one.
# The stylesheet is not crawled — markdown conversion drops it — so it can be
# replaced wholesale later; what must never move is text between elements.
LAYOUT_CSS = """
:root {
  color-scheme: light;
  --page-bg: var(--brand-bg, #ffffff);
  --ink: var(--brand-ink, #111827);
  --muted: var(--brand-muted, #6b7280);
  --body-ink: var(--brand-body-ink, #374151);
  --accent: var(--brand-primary, #4338ca);
  --line: var(--brand-border, #e5e7eb);
  --band: var(--brand-band, var(--brand-primary, #1f2937));
  --on-band: var(--brand-on-dark, #f9fafb);
  --logo: var(--cl-logo-light, none);
}
@media (prefers-color-scheme: dark) {
  :root {
    color-scheme: dark;
    --page-bg: #0b0d12;
    --ink: #eceef3;
    --muted: #9aa1ae;
    --body-ink: rgba(236, 238, 243, .84);
    --accent: var(--brand-emph-ink-dark, #a5b4fc);
    --line: #2a2f3a;
    --logo: var(--cl-logo-dark, var(--cl-logo-light, none));
  }
}
* { box-sizing: border-box; }
html { -webkit-text-size-adjust: 100%; }
body { margin: 0; background: var(--page-bg); color: var(--ink);
  font-family: var(--brand-font-body, -apple-system, 'Segoe UI', Roboto, sans-serif);
  font-size: 17px; line-height: 1.7; -webkit-font-smoothing: antialiased; }
h1, h2, h3 { font-family: var(--brand-font-heading, var(--brand-font-body, -apple-system, 'Segoe UI', sans-serif));
  font-weight: var(--brand-weight-heading, 600); margin: 0; }
.cl-top { max-width: 880px; margin: 0 auto; padding: 28px 24px 20px; }
.cl-logo { width: 130px; height: 26px; background: var(--logo) left center / contain no-repeat; }
.cl-hero { max-width: 880px; margin: 0 auto; padding: 56px 40px; border-radius: 20px;
  background: var(--band); color: var(--on-band);
  print-color-adjust: exact; -webkit-print-color-adjust: exact; }
.cl-hero h1 { font-size: clamp(30px, 5vw, 44px); line-height: 1.14; color: var(--on-band); text-wrap: balance; }
.cl-hero .cl-dek { margin: 14px 0 0; max-width: 52ch; opacity: .8; font-size: 16px; }
.cl-wrap { max-width: 880px; margin: 0 auto; padding: 0 40px 24px; }
.cl-group { padding-top: 56px; }
.cl-group-head { padding-bottom: 20px; border-bottom: 1px solid var(--line); }
.cl-eyebrow { display: inline-block; padding: 5px 13px; font-size: 12px; font-weight: 600;
  letter-spacing: .06em; text-transform: uppercase; line-height: 1.4; border-radius: 100px;
  font-family: var(--brand-font-body, -apple-system, 'Segoe UI', sans-serif);
  color: var(--accent); border: 1px solid var(--line); }
.cl-entry { padding: 30px 0; border-bottom: 1px solid var(--line); }
.cl-entry:last-child { border-bottom: 0; }
.cl-entry h3 { font-size: 23px; line-height: 1.25; margin-bottom: 10px; font-variant-numeric: tabular-nums; }
.cl-entry p { margin: 0; color: var(--body-ink); }
.cl-foot { max-width: 880px; margin: 0 auto; padding: 0 40px 72px; }
.cl-foot > div { padding-top: 26px; border-top: 1px solid var(--line); color: var(--muted); font-size: 14px; }
@media (max-width: 720px) {
  body { font-size: 16.5px; }
  .cl-hero { padding: 40px 24px; border-radius: 0; }
  .cl-wrap, .cl-foot { padding-left: 24px; padding-right: 24px; }
  .cl-top { padding: 20px 24px 16px; }
}
""".strip()

# The fielded entry's labels and novelty badge. Kept apart from LAYOUT_CSS so a
# page whose stylesheet predates the fielded shape gets it appended on its next
# publish; the stylesheet is not crawled, so appending it moves no line.
FIELDS_CSS = """
/* cl-fields */
.cl-entry .cl-field { margin-top: 12px; }
.cl-entry .cl-label { font-weight: 600; color: var(--ink); }
.cl-entry[data-novelty] h3::after { display: inline-block; vertical-align: middle; margin-left: 10px;
  padding: 3px 10px; font-size: 12px; font-weight: 600; letter-spacing: .06em; text-transform: uppercase;
  line-height: 1.4; border-radius: 100px; border: 1px solid var(--line); color: var(--accent);
  font-family: var(--brand-font-body, -apple-system, 'Segoe UI', sans-serif); }
""".strip() + '\n' + '\n'.join(
    f'.cl-entry[data-novelty="{key}"] h3::after {{ content: "{label}"; }}' for key, label in NOVELTY_BADGES.items())


def ensure_fields_css(style):
    """A carried-over stylesheet, plus the fielded-entry rules if it lacks them."""
    return style if '/* cl-fields */' in style else f'{style}\n{FIELDS_CSS}'


LOGO_MIME = {'.png': 'image/png', '.svg': 'image/svg+xml', '.jpg': 'image/jpeg',
             '.jpeg': 'image/jpeg', '.webp': 'image/webp'}


def data_uri(path):
    path = Path(path)
    mime = LOGO_MIME.get(path.suffix.lower())
    if not mime:
        raise Refused(f'{path.name}: a logo must be png, svg, jpg or webp.')
    return f'data:{mime};base64,{base64.b64encode(path.read_bytes()).decode("ascii")}'


def build_style(tokens_css=None, logo_light=None, logo_dark=None):
    """Brand tokens first, then logo variables, then the layout that reads them.
    Everything is inlined: the page may fetch nothing at render time."""
    parts = []
    if tokens_css:
        parts.append(tokens_css.strip())
    logos = []
    if logo_light:
        logos.append(f'--cl-logo-light: url({data_uri(logo_light)});')
    if logo_dark:
        logos.append(f'--cl-logo-dark: url({data_uri(logo_dark)});')
    if logos:
        parts.append(':root { ' + ' '.join(logos) + ' }')
    parts += [LAYOUT_CSS, FIELDS_CSS]
    return '\n'.join(parts)


def style_of(html):
    match = re.search(r'<style>(.*?)</style>', html, re.S)
    return match[1] if match else None


# --------------------------------------------------------------------------
# Read a page back the way the crawl does
# --------------------------------------------------------------------------

class _PageLines(HTMLParser):
    BLOCKS = {'h1': '# ', 'h2': '## ', 'h3': '### ', 'p': ''}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.lines = []
        self.capture = None
        self.buffer = []
        self.in_footer = False

    def handle_starttag(self, tag, attrs):
        if tag == 'footer':
            self.in_footer = True
        if self.capture is None and (tag in self.BLOCKS or (self.in_footer and tag == 'div')):
            self.capture = tag
            self.buffer = []

    def handle_endtag(self, tag):
        if tag == self.capture:
            text = ''.join(self.buffer).strip()
            if text:
                self.lines.append(self.BLOCKS.get(tag, '') + text)
            self.capture = None
        if tag == 'footer':
            self.in_footer = False

    def handle_data(self, data):
        if self.capture is not None:
            self.buffer.append(data)


def page_lines(html):
    """The text lines a markdown conversion of the page yields, in order."""
    parser = _PageLines()
    parser.feed(html)
    parser.close()
    return parser.lines


def state_from_page(html):
    """Rebuild the state of a page that has none, from its own lines. Refuses a
    page whose shape it does not recognise rather than guessing."""
    lines = page_lines(html)
    if len(lines) < 3 or not lines[0].startswith('# '):
        raise Refused('This page does not look like a changelog rendered by this skill (no title heading).')
    title, dek, footer = lines[0][2:], lines[1], lines[-1]
    entries, ids = [], set()
    index = 2
    while index < len(lines) - 1:
        line = lines[index]
        if line.startswith('## '):
            index += 1
            continue
        match = HEADING_RE.match(line)
        if not match or index + 1 >= len(lines) - 1:
            raise Refused(f'Unrecognised line on the current page, so it cannot be rebuilt safely: {line[:80]!r}')
        entry_date, entry_title = match[1], match[2]
        entry_id = f'{entry_date}-{slug(entry_title)}'
        suffix = 2
        while entry_id in ids:
            entry_id = f'{entry_date}-{slug(entry_title)}-{suffix}'
            suffix += 1
        ids.add(entry_id)
        entries.append({'id': entry_id, 'date': entry_date, 'title': entry_title,
                        'body': lines[index + 1], 'publishedAt': None})
        index += 2
    state = {'schemaVersion': SCHEMA_VERSION, 'page': {'title': title, 'dek': dek, 'footer': footer},
             'entries': entries}
    if render_lines(state) != lines:
        raise Refused('Rebuilding the current page from its own lines did not reproduce it exactly. Stop; publishing on top of it could change live lines.')
    return state


# --------------------------------------------------------------------------
# Validate what is being added
# --------------------------------------------------------------------------

def valid_date(value):
    if not isinstance(value, str) or not DATE_RE.match(value):
        return False
    try:
        Date.fromisoformat(value)
    except ValueError:
        return False
    return True


def read_entries(path):
    """Returns (entries, reshape, remove). Accepts {"entries": [...], "reshape": [...],
    "remove": [...]} (what the staging page copies; the last two only when a
    reviewer decided a live paragraph entry) or a bare list of new entries."""
    try:
        blob = json.loads(Path(path).read_text(encoding='utf-8'))
    except (OSError, ValueError) as error:
        raise Refused(f'Could not read the entries at {path}: {error}')
    parts = blob if isinstance(blob, dict) else {'entries': blob}
    entries, reshape, remove = (parts.get(key, []) for key in ('entries', 'reshape', 'remove'))
    if not all(isinstance(part, list) for part in (entries, reshape, remove)):
        raise Refused('The pasted entries are not lists of entries.')
    if not (entries or reshape or remove):
        raise Refused('The pasted entries contain nothing to publish.')
    return entries, reshape, remove


def validate_entering(entries, state):
    """Returns (entering, already_live). Any problem refuses the whole batch:
    a partial publish would hide an attempt to touch a live entry."""
    errors, entering, already_live, seen = [], [], [], set()
    existing = {entry['id']: entry for entry in state['entries']}
    removed = {gone['id'] for gone in state.get('removed', [])}
    for number, raw in enumerate(entries, 1):
        if not isinstance(raw, dict):
            errors.append(f'Entry {number} is not an object.')
            continue
        title = (raw.get('title') or '').strip() if isinstance(raw.get('title'), str) else ''
        body = (raw.get('body') or '').strip() if isinstance(raw.get('body'), str) else ''
        entry_date = raw.get('date')
        label = f'"{title or f"entry {number}"}"'
        if not valid_date(entry_date):
            errors.append(f'{label} has no valid date (YYYY-MM-DD).')
            continue
        entry_id = raw.get('id') or f'{entry_date}-{slug(title)}'
        if not isinstance(entry_id, str) or not ID_RE.match(entry_id):
            errors.append(f'{label} has an invalid id {entry_id!r}; use lowercase letters, digits and hyphens.')
            continue
        if entry_id in seen:
            errors.append(f'"{entry_id}" appears twice in the pasted entries.')
            continue
        seen.add(entry_id)
        if entry_id in removed:
            errors.append(f'"{entry_id}" was removed from the page; publish it under a new id if it belongs back.')
            continue
        fielded = 'body' not in raw or any(key in raw for key in TEXT_FIELDS)
        fields = {key: (raw.get(key) or '').strip() if isinstance(raw.get(key), str) else '' for key in TEXT_FIELDS}
        novelty = raw.get('novelty')
        if entry_id in existing:
            live = existing[entry_id]
            if is_fielded(live):
                same = fielded and (live['date'], live['title'], live['novelty'], *[live[k] for k in TEXT_FIELDS]) == \
                    (entry_date, title, novelty, *[fields[k] for k in TEXT_FIELDS])
            else:
                same = not fielded and (live['date'], live['title'], live['body']) == (entry_date, title, body)
            if same:
                already_live.append(entry_id)
            else:
                errors.append(f'"{entry_id}" is already live with different text. Published entries are never re-worded (the crawl would read the new wording as a new capability); publish a new entry that supersedes it instead.')
            continue
        if raw.get('availability') != 'ga':
            errors.append(f'{label} is not marked generally available (availability "ga"). Only work every customer can use goes on the public page.')
        if not title:
            errors.append(f'{label} has no title.')
        elif '\n' in title or len(title) > TITLE_MAX_CHARS:
            errors.append(f'{label}: a title is one line of at most {TITLE_MAX_CHARS} characters.')
        if not fielded:
            errors.append(f'{label} is a single paragraph. New entries are fielded: give it a description, a useCase, a problem and a novelty ("net-new" or "improvement") instead of a body.')
            continue
        errors += field_problems(label, fields, novelty)
        entering.append({'id': entry_id, 'date': entry_date, 'title': title, 'novelty': novelty,
                         **{key: fields[key] for key in TEXT_FIELDS}})
    if errors:
        raise Refused(f'Refusing the whole batch ({len(errors)} problem(s)):\n- ' + '\n- '.join(errors))
    return entering, already_live


def field_problems(label, fields, novelty):
    """What is wrong with one entry's fields, as refusal lines; [] when they can publish."""
    errors = []
    for key in TEXT_FIELDS:
        value = fields[key]
        if not value:
            errors.append(f'{label} has no {key}.')
        elif '\n' in value:
            errors.append(f'{label}: its {key} has a line break; each field is one paragraph.')
        elif LEAD_HAZARD.match(value):
            errors.append(f'{label}: its {key} starts with a markdown character (#, -, *, >, |, or "1.").')
    if novelty not in NOVELTY_BADGES:
        errors.append(f'{label} has no novelty; it must be "net-new" or "improvement".')
    return errors


def validate_live_changes(reshape, remove, state, entering_ids):
    """Returns (reshaped, removed): the fields each reshaped entry takes in place
    of its paragraph, keyed by id, and the ids coming off the page. A reshape
    names a live paragraph entry and keeps its date and title, so its heading
    survives; a removal names any live entry. Any problem refuses the whole batch.

      validate_live_changes([{'id': 'a', 'description': 'X does Y.', 'useCase': 'A rep can now…',
                              'problem': 'Reps had to…', 'novelty': 'improvement'}], ['b'], state, set())
      # -> ({'a': {'novelty': 'improvement', 'description': 'X does Y.', …}}, ['b'])
    """
    errors, reshaped, removed = [], {}, []
    live = {entry['id']: entry for entry in state['entries']}
    for number, raw in enumerate(reshape, 1):
        entry_id = raw.get('id') if isinstance(raw, dict) else None
        current = live.get(entry_id) if isinstance(entry_id, str) else None
        if current is None:
            errors.append(f'Reshape {number} ({entry_id!r}) is not live; only an entry already on the page can be reshaped.')
            continue
        label = f'"{current["title"]}"'
        if entry_id in reshaped:
            errors.append(f'"{entry_id}" is reshaped twice in the pasted entries.')
            continue
        if is_fielded(current):
            errors.append(f'{label} is already fielded; its lines are the lock.')
            continue
        for key in ('date', 'title'):
            if key in raw and raw[key] != current[key]:
                errors.append(f'{label}: a reshape keeps the {key} ({current[key]!r}); moving or renaming an entry is a new entry.')
        fields = {key: (raw.get(key) or '').strip() if isinstance(raw.get(key), str) else '' for key in TEXT_FIELDS}
        novelty = raw.get('novelty')
        errors += field_problems(label, fields, novelty)
        reshaped[entry_id] = {'novelty': novelty, **fields}
    for entry_id in remove:
        if not isinstance(entry_id, str) or entry_id not in live:
            errors.append(f'Remove {entry_id!r} is not live; only an entry already on the page can be removed.')
        elif entry_id in removed:
            errors.append(f'"{entry_id}" is removed twice in the pasted entries.')
        elif entry_id in reshaped:
            errors.append(f'"{live[entry_id]["title"]}" is both reshaped and removed; it can only be one.')
        else:
            removed.append(entry_id)
    for entry_id in entering_ids & (set(reshaped) | set(removed)):
        errors.append(f'"{entry_id}" is both a new entry and a change to a live one.')
    if errors:
        raise Refused(f'Refusing the whole batch ({len(errors)} problem(s)):\n- ' + '\n- '.join(errors))
    return reshaped, removed


def apply_live_changes(state, reshaped, removed, changed_at):
    """The state after the reviewer's reshapes and removals, and the live lines
    they retire on purpose: a reshaped entry's paragraph, every line of a removed
    entry, and a month heading no entry is left under. A removed entry leaves
    only its id and date on the record, so its text is gone from the bundle."""
    entries, retiring = [], set()
    for entry in state['entries']:
        if entry['id'] in removed:
            retiring.update([f'### {entry["date"]} — {entry["title"]}', *entry_lines(entry)])
        elif entry['id'] in reshaped:
            retiring.add(entry['body'])
            rest = {key: value for key, value in entry.items() if key not in ('id', 'date', 'title', 'body')}
            entries.append({'id': entry['id'], 'date': entry['date'], 'title': entry['title'],
                            **reshaped[entry['id']], **rest, 'reshapedAt': changed_at})
        else:
            entries.append(entry)
    months_left = {month_heading(entry['date']) for entry in entries}
    retiring.update(f'## {month_heading(entry["date"])}' for entry in state['entries']
                    if entry['id'] in removed and month_heading(entry['date']) not in months_left)
    gone = state.get('removed', []) + [{'id': entry_id, 'removedAt': changed_at} for entry_id in removed]
    return {**state, 'entries': entries, **({'removed': gone} if gone else {})}, retiring


# --------------------------------------------------------------------------
# The invariants
# --------------------------------------------------------------------------

def check(name, ok, detail):
    return {'name': name, 'ok': ok, 'detail': detail}


def run_checks(old_lines, state, style, retiring=frozenset()):
    """The publish checks over the next state. `retiring` is the live lines the
    reviewer's reshapes and removals replace on purpose; every other live line
    must survive."""
    html = render_html(state, style)
    lines = render_lines(state)
    checks = []

    seen, dupes = set(), []
    for line in lines:
        key = line.strip()
        if key in seen:
            dupes.append(key)
        seen.add(key)
    checks.append(check('line-uniqueness', not dupes,
                        f'{len(seen)} unique lines' if not dupes else
                        'the crawl silently swallows repeated lines: ' + ', '.join(repr(d[:60]) for d in dupes[:3])))

    old = {line.strip() for line in old_lines if line.strip()}
    retired = old & {line.strip() for line in retiring}
    missing = sorted(old - seen - retired)
    kept = f'all {len(old)} live lines unchanged' if not retired else \
        f'{len(old) - len(retired)} live lines unchanged, {len(retired)} retired by reshapes and removals'
    checks.append(check('history', not missing,
                        kept if not missing else
                        f'{len(missing)} live line(s) would change or disappear, and the crawl would read the result as new capabilities: '
                        + ', '.join(repr(m[:60]) for m in missing[:3])))

    added = [line for line in lines if line.strip() and line.strip() not in old]
    chars = len('\n'.join(added))
    if chars == 0 and retired:
        checks.append(check('delta', True, f'removes {len(retired)} line(s) and adds none'))
    elif chars == 0:
        checks.append(check('delta', False, 'nothing new to publish'))
    elif chars < DELTA_MIN_CHARS:
        checks.append(check('delta', False, f'only {chars} new characters, under the {DELTA_MIN_CHARS}-character floor below which ingestion fires no extraction'))
    elif chars > DELTA_MAX_CHARS:
        checks.append(check('delta', False, f'{chars} new characters exceeds the {DELTA_MAX_CHARS} cap; the delta would be truncated mid-line'))
    else:
        checks.append(check('delta', True, f'{len(added)} new line(s), {chars} characters'))

    problem = next((label for pattern, label in VOLATILE if pattern.search(html)), None)
    if problem is None and LINK_RE.search(html):
        problem = 'a link; shallow-domain crawling turns each one into its own child resource'
    if problem is None and EXTERNAL_FETCH_RE.search(html):
        problem = 'an external fetch (stylesheet, @import, font or image URL); inline it instead'
    checks.append(check('page-safety', problem is None,
                        'no volatile text, links or external fetches' if problem is None else f'page contains {problem}'))

    checks.append(check('determinism', html == render_html(state, style) and lines == render_lines(state),
                        'two renders byte-identical'))
    return checks, html, added


# --------------------------------------------------------------------------
# Commands
# --------------------------------------------------------------------------

def print_checks(checks):
    for item in checks:
        print(f'  {"✓" if item["ok"] else "✗"} {item["name"]:<16} {item["detail"]}')


def cmd_init(args):
    page = {'title': args.title.strip(), 'dek': args.dek.strip(), 'footer': args.footer.strip()}
    for key, value in page.items():
        if not value or '\n' in value:
            raise Refused(f'The page {key} must be one non-empty line.')
    if page['title'] == page['dek'] or page['dek'] == page['footer'] or page['title'] == page['footer']:
        raise Refused('Title, dek and footer must differ; the crawl swallows repeated lines.')
    Path(args.out).write_text(dump_json({'schemaVersion': SCHEMA_VERSION, 'page': page, 'entries': []}), encoding='utf-8')
    print(f'✓ New changelog state written to {args.out}')


def cmd_bootstrap(args):
    state = state_from_page(Path(args.html).read_text(encoding='utf-8'))
    Path(args.out).write_text(dump_json(state), encoding='utf-8')
    print(f'✓ Rebuilt {len(state["entries"])} live entr{"y" if len(state["entries"]) == 1 else "ies"} from the current page into {args.out}')


def cmd_add(args):
    state = load_state(args.state)
    current_html = Path(args.html).read_text(encoding='utf-8') if args.html else None
    old_lines = page_lines(current_html) if current_html else []
    entries, reshape, remove = read_entries(args.entries)
    entering, already_live = validate_entering(entries, state)
    reshaped, removed = validate_live_changes(reshape, remove, state, {entry['id'] for entry in entering})

    if args.tokens or args.logo_light or args.logo_dark or not current_html:
        tokens = Path(args.tokens).read_text(encoding='utf-8') if args.tokens else None
        style = build_style(tokens, args.logo_light, args.logo_dark)
    else:
        style = style_of(current_html)
        if style is None:
            raise Refused('The current page has no <style> block to carry over; pass --tokens to restyle it.')
        style = ensure_fields_css(style)

    if already_live:
        print(f'  Already live, skipped: {", ".join(already_live)}')
    if not (entering or reshaped or removed):
        print('\n  Nothing new to publish; the page is already up to date.\n')
        return 0

    published_at = args.published_at or datetime.now(timezone.utc).date().isoformat()
    if not valid_date(published_at):
        raise Refused('--published-at must be YYYY-MM-DD.')
    changed, retiring = apply_live_changes(state, reshaped, removed, published_at)
    next_state = {**changed, 'schemaVersion': SCHEMA_VERSION, 'entries': [{**entry, 'publishedAt': published_at} for entry in entering] + changed['entries']}

    if retiring:
        print(f'\n  Live lines the reviewer\'s reshapes and removals retire ({len(retiring)}):')
        for line in sorted(retiring):
            print(f'    - {line if len(line) <= 110 else line[:110] + "…"}')
    checks, html, added = run_checks(old_lines, next_state, style, retiring)
    print()
    print_checks(checks)
    print()
    if not all(item['ok'] for item in checks):
        print('✗ Refusing to publish. Nothing was written.\n')
        return 1

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    (out/'index.html').write_text(html, encoding='utf-8')
    (out/'changelog.json').write_text(dump_json(next_state), encoding='utf-8')
    manifest = out.parent/f'{out.name}.manifest.json'
    manifest.write_text(dump_json(BUNDLE_FILES), encoding='utf-8')

    print(f'  Lines this publish adds ({len(added)}):')
    for line in added:
        print(f'    + {line if len(line) <= 110 else line[:110] + "…"}')
    print(f'\n✓ Bundle ready: {out}/ ({", ".join(BUNDLE_FILES)})')
    print(f'  Upload manifest: {manifest}\n')
    return 0


def cmd_lines(args):
    lines = page_lines(Path(args.html).read_text(encoding='utf-8'))
    if args.expect_state:
        expected = render_lines(load_state(args.expect_state))
        if lines != expected:
            missing = [line for line in expected if line not in lines]
            extra = [line for line in lines if line not in expected]
            print(f'✗ The page does not match the state: {len(missing)} expected line(s) missing, {len(extra)} unexpected.')
            for line in missing[:5]:
                print(f'    - {line[:110]}')
            for line in extra[:5]:
                print(f'    + {line[:110]}')
            return 1
        print(f'✓ The page carries exactly the {len(lines)} lines the state renders.')
        return 0
    for line in lines:
        print(line)
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    commands = parser.add_subparsers(dest='command', required=True)

    init = commands.add_parser('init', help='state for a brand-new changelog')
    init.add_argument('--title', required=True)
    init.add_argument('--dek', required=True)
    init.add_argument('--footer', required=True)
    init.add_argument('--out', required=True)

    bootstrap = commands.add_parser('bootstrap', help='state rebuilt from a live page that has none')
    bootstrap.add_argument('--html', required=True)
    bootstrap.add_argument('--out', required=True)

    add = commands.add_parser('add', help='add entries and render the bundle')
    add.add_argument('--state', required=True)
    add.add_argument('--entries', required=True)
    add.add_argument('--out', required=True)
    add.add_argument('--html', help='the live index.html; its lines are the lock and its style is kept')
    add.add_argument('--tokens', help='brand kit tokens.css, to style a new page or restyle an existing one')
    add.add_argument('--logo-light')
    add.add_argument('--logo-dark')
    add.add_argument('--published-at')

    lines = commands.add_parser('lines', help='print the lines the crawl reads from a page')
    lines.add_argument('--html', required=True)
    lines.add_argument('--expect-state')

    args = parser.parse_args(argv)
    handler = {'init': cmd_init, 'bootstrap': cmd_bootstrap, 'add': cmd_add, 'lines': cmd_lines}[args.command]
    try:
        return handler(args) or 0
    except Refused as error:
        print(f'\n✗ {error}\n', file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
