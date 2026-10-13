#!/usr/bin/env python3
"""Policy-aware source lint. It never certifies rendering or rewrites evidence."""
import argparse
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit


DEFAULT = {'audience': 'internal', 'readiness': 'ready_for_review', 'assets': 'bundled',
           'remoteHosts': [], 'intentionalPlaceholders': [], 'allowedTerms': []}
ENUMS = {'audience': {'internal', 'restricted_external', 'public'},
         'readiness': {'seller_draft', 'ready_for_review', 'buyer_ready', 'published_verified'},
         'assets': {'embedded', 'bundled', 'hosted'}}
WORDS = 'delve robust comprehensive leverage seamless pivotal meticulous utilize holistic synergy tapestry paradigm'.split()


class Document(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.tags = []
        self.text = []
        self.resources = []
        self.links = []
        self.meta = {}
        self.css = []
        self.doctype = False
        self.ids = set()
        self.inert_links = 0

    def handle_decl(self, decl):
        if decl.lower() == 'doctype html':
            self.doctype = True

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get('id'):
            self.ids.add(a['id'])
        if tag == 'a' and not a.get('href') and (a.get('role') == 'button' or 'btn' in a.get('class', '')):
            self.inert_links += 1
        if tag not in {'meta', 'link', 'img', 'br', 'hr', 'input', 'source', 'wbr'}:
            self.tags.append(tag)
        if a.get('style'):
            self.css.append(a['style'])
        if tag == 'meta':
            self.meta[a.get('property', a.get('name', ''))] = a.get('content', '')
        if tag == 'a' and a.get('href'):
            self.links.append(a['href'])
        for attr in ('src', 'poster'):
            if a.get(attr):
                self.resources.append(a[attr])
        if a.get('srcset'):
            self.resources.extend(re.findall(r'(?:https?://|//)[^\s,]+', a['srcset'], re.I))
        if tag in {'image', 'use'}:
            self.resources.extend(a[k] for k in ('href', 'xlink:href') if a.get(k))
        if tag == 'link' and any(r in (a.get('rel') or '').lower().split() for r in ('stylesheet', 'icon', 'preload', 'modulepreload')):
            if a.get('href'):
                self.resources.append(a['href'])

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        self.handle_endtag(tag)

    def handle_endtag(self, tag):
        if tag in self.tags:
            self.tags = self.tags[:len(self.tags) - 1 - self.tags[::-1].index(tag)]

    def handle_data(self, data):
        if 'style' in self.tags:
            self.css.append(data)
        elif not any(t in self.tags for t in ('script', 'template')):
            self.text.append((data, any(t in self.tags for t in ('q', 'blockquote', 'code', 'pre'))))


def read_policy(path):
    policy = dict(DEFAULT)
    if path:
        supplied = json.loads(path.read_text())
        if not isinstance(supplied, dict) or set(supplied) - set(DEFAULT):
            raise ValueError('policy must be an object with documented keys only')
        policy.update(supplied)
    for key, values in ENUMS.items():
        if policy[key] not in values:
            raise ValueError(f'invalid policy {key}')
    for key in ('remoteHosts', 'intentionalPlaceholders', 'allowedTerms'):
        if not isinstance(policy[key], list) or any(not isinstance(x, str) or not x for x in policy[key]):
            raise ValueError(f'{key} must be a list of nonempty strings')
    return policy


def lint(path, policy):
    doc = Document()
    doc.feed(path.read_text())
    errors, warnings = [], []
    if not doc.doctype:
        errors.append('Missing HTML doctype')
    if doc.inert_links:
        errors.append('Actionable anchor is missing its destination')
    for uri in doc.links:
        parsed = urlsplit(unquote(uri))
        if parsed.scheme.lower() in {'javascript', 'data', 'file', 'vbscript'}:
            errors.append('Unsafe link destination scheme')
        if uri.startswith('#') and uri[1:] not in doc.ids:
            errors.append('Missing in-page link target: ' + uri)
    text = ' '.join(t for t, _ in doc.text)
    authored = ' '.join(t for t, quoted in doc.text if not quoted)
    for term in policy['allowedTerms']:
        authored = authored.replace(term, '')
    for word in WORDS:
        if re.search(r'\b' + word + r'\b', authored, re.I):
            warnings.append(f'Review authored wording: {word}; preserve customer terminology')
    if re.search('[—–]', authored):
        warnings.append('Review dash usage in authored prose; range punctuation and exact quotes are allowed')
    placeholders = set(re.findall(r'\[(?:TBD|TODO|NEEDS[^\]]*|INSERT[^\]]*|PRICE|AMOUNT|DATE|OWNER|CTA[^\]]*)\]|\{\{[^}]+\}\}', text, re.I))
    unresolved = placeholders - set(policy['intentionalPlaceholders'])
    if unresolved:
        target = errors if policy['readiness'] in {'buyer_ready', 'published_verified'} else warnings
        target.append('Unresolved inputs: ' + ', '.join(sorted(unresolved)))
    if policy['audience'] != 'internal':
        if any(urlsplit(u).hostname == 'app.octavehq.com' and re.search(r'/(entity|o)/', urlsplit(u).path) for u in doc.links):
            errors.append('External artifact contains internal workspace links')
        if re.search(r'\b(?:evt|ex|crmo|op|pe|sg|uu|oj|rr|wa)_[A-Za-z0-9]{8,}\b', text):
            errors.append('External artifact exposes raw workspace record IDs')
    css = re.sub(r'/\*.*?\*/', '', '\n'.join(doc.css), flags=re.S)
    doc.resources.extend(m[0] or m[1] for m in re.findall(r'''url\(\s*["']?([^\s)'";]+)|@import\s+["']([^"']+)''', css, re.I))
    root = path.parent.resolve()
    for uri in set(doc.resources):
        parsed = urlsplit(uri)
        if uri.startswith('#') or parsed.scheme == 'data':
            continue
        if parsed.scheme in {'http', 'https'} or uri.startswith('//'):
            if policy['assets'] != 'hosted' or parsed.hostname not in policy['remoteHosts']:
                errors.append(f'Undeclared remote asset: {uri}')
        elif parsed.scheme or uri.startswith('/'):
            errors.append(f'Unsupported asset location: {uri}')
        elif policy['assets'] == 'embedded':
            errors.append(f'Embedded artifact references a separate file: {uri}')
        else:
            target = (root / unquote(parsed.path)).resolve()
            if not target.is_relative_to(root) or not target.is_file():
                errors.append(f'Missing or out-of-bundle resource: {uri}')
    if policy['audience'] == 'public':
        for key in ('og:title', 'og:description', 'og:image'):
            if not doc.meta.get(key) or re.search(r'\[[^]]*\]|\{[^}]*\}', doc.meta[key]):
                errors.append(f'Missing/unfilled public share metadata: {key}')
        image = doc.meta.get('og:image', '')
        if image.startswith('data:'):
            errors.append('Public share image cannot be a data URI')
        elif image:
            parsed = urlsplit(image)
            if parsed.scheme not in {'http', 'https'}:
                target = (root / unquote(parsed.path)).resolve()
                if not target.is_relative_to(root) or not target.is_file():
                    errors.append('Public share image file is missing or outside bundle')
                if policy['readiness'] == 'published_verified':
                    errors.append('Served public share image must have an absolute HTTP(S) URL')
    return errors, warnings


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file', type=Path)
    parser.add_argument('--policy', type=Path)
    args = parser.parse_args()
    try:
        errors, warnings = lint(args.file, read_policy(args.policy))
    except (OSError, ValueError) as exc:
        print(f'NOT RUN: {exc}', file=sys.stderr)
        return 2
    for error in errors:
        print('FAIL:', error)
    for warning in warnings:
        print('ADVISORY:', warning)
    print(f'{"FAIL" if errors else "PASS"}: source checks; {len(errors)} failures, {len(warnings)} advisories. Rendering not checked.')
    return int(bool(errors))


if __name__ == '__main__':
    sys.exit(main())
