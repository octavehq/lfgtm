"""Validate RSA creative, preserve attribution, and write quoted web-upload CSV."""
import argparse
import csv
import hashlib
import itertools
import json
from pathlib import Path
import unicodedata
from urllib.parse import urlsplit


def text_length(text):
    return sum(2 if unicodedata.east_asian_width(c) in ('W', 'F') else 1 for c in text)


def validate(ad):
    if not ad.get('customerId') or ad.get('isManager') is not False:
        raise ValueError('bind a verified child advertising account')
    if urlsplit(ad.get('finalUrl', '')).scheme not in ('https', 'http') or not urlsplit(ad['finalUrl']).hostname:
        raise ValueError('finalUrl must be HTTP(S)')
    for field, lower, upper, limit in [('headlines', 3, 15, 30), ('descriptions', 2, 4, 90)]:
        assets = ad[field]
        if not lower <= len(assets) <= upper:
            raise ValueError(f'{field} count must be {lower}–{upper}')
        if len({x['text'] for x in assets}) != len(assets):
            raise ValueError(f'duplicate {field}')
        for item in assets:
            if not item['text'].strip() or text_length(item['text']) > limit:
                raise ValueError(f'{field} exceeds the {limit}-character limit or is empty')
            slots = (1, 2, 3) if field == 'headlines' else (1, 2)
            if item.get('pin') is not None and item['pin'] not in slots:
                raise ValueError('invalid pin position')
    return ad


def fingerprint(ad):
    fields = {k: ad[k] for k in ('customerId', 'finalUrl', 'headlines', 'descriptions')}
    for key in ('headlines', 'descriptions'):
        fields[key] = sorted(fields[key], key=lambda x: (x['text'], x.get('pin') or 0))
    return hashlib.sha256(json.dumps(fields, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def match_creative(ad, cards, workspace):
    candidates = [c for c in cards if c.get('workspaceOId') == workspace
                  and c.get('customerId') == ad['customerId']
                  and c.get('fingerprint') == fingerprint(ad)]
    if ad.get('liveAdId'):
        candidates = [c for c in candidates if c.get('liveAdId') == ad['liveAdId']]
    return candidates[0] if len(candidates) == 1 else None


def previews(ad, limit=12):
    validate(ad)
    def arrangements(assets, slots):
        pools = []
        for position in range(1, slots+1):
            pinned = [a for a in assets if a.get('pin') == position]
            pools.append(pinned or [a for a in assets if not a.get('pin')])
        for combo in itertools.product(*pools):
            if len({a['text'] for a in combo}) == len(combo):
                yield [a['text'] for a in combo]
    # Bounded examples of this RSA's membership, not a prediction of platform serving.
    result = []
    for headlines in arrangements(ad['headlines'], 3):
        for descriptions in arrangements(ad['descriptions'], 2):
            result.append({'headlines': headlines, 'descriptions': descriptions})
            if len(result) >= min(max(limit, 1), 12): return result
    return result


def export_csv(ads, path):
    rows=[]
    for ad in ads:
        validate(ad)
        row={'Campaign':ad['campaign'], 'Ad group':ad['adGroup'], 'Ad type':'Responsive search ad',
             'Customer ID':str(ad['customerId']), 'Ad status':'Paused', 'Final URL':ad['finalUrl']}
        for field, label in [('headlines','Headline'),('descriptions','Description')]:
            for i, item in enumerate(ad[field], 1):
                row[f'{label} {i}']=item['text']
                if item.get('pin'): row[f'{label} {i} position']=str(item['pin'])
        rows.append(row)
    if not rows: raise ValueError('no creative to export')
    headers=list(dict.fromkeys(k for row in rows for k in row))
    with Path(path).open('w',encoding='utf-8',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=headers);writer.writeheader();writer.writerows(rows)
    with Path(path).open(encoding='utf-8',newline='') as f:
        parsed=list(csv.DictReader(f))
    if parsed != [{k: r.get(k,'') for k in headers} for r in rows]: raise ValueError('CSV round-trip failed')


if __name__ == '__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('input',type=Path);ap.add_argument('out',type=Path)
    args=ap.parse_args();export_csv(json.loads(args.input.read_text()),args.out)
