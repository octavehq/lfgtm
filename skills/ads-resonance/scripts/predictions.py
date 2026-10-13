"""Deterministic schema 0.3 ratio evaluator; no query execution or mutations."""
import argparse
from datetime import datetime
import hashlib
import json
import math
from pathlib import Path


def definition_hash(definition):
    return hashlib.sha256(json.dumps(definition, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()).hexdigest()


def evaluate(card, result):
    if card.get('schemaVersion') != '0.3':
        raise ValueError('unsupported prediction schema; bind/migrate legacy cards explicitly')
    definition = card['definition']
    if card['definitionHash'] != definition_hash(definition):
        raise ValueError('prediction definition changed')
    for key in ('workspaceOId', 'platform', 'customerId'):
        if not definition.get(key) or result.get(key) != definition[key]:
            raise ValueError(f'prediction scope mismatch: {key}')
    if sorted(result.get('unitIds', [])) != sorted(definition['unitIds']):
        raise ValueError('population changed')
    def date(s):
        value = datetime.fromisoformat(s.replace('Z', '+00:00'))
        if value.tzinfo is None:
            raise ValueError('timestamps require timezone offsets')
        return value
    window = definition['evaluation_window']
    if result.get('evaluation_window') != window:
        raise ValueError('evaluation source window differs from frozen definition')
    if date(window['start']) >= date(window['end']):
        raise ValueError('invalid evaluation window')
    if result.get('direction', 'unknown') not in ('favorable','unfavorable','neutral','unknown'):
        raise ValueError('invalid descriptive direction')
    bounds = definition['boundaries']
    if not all(isinstance(v, (int,float)) and math.isfinite(v) for v in bounds.values()) or bounds['refuteBelow'] > bounds['confirmAtLeast']:
        raise ValueError('invalid frozen boundaries')
    status, reason, ratio = 'INCONCLUSIVE', 'insufficient or invalid measurements', None
    if date(result['watermark']) < date(window['end']):
        status, reason = 'PENDING', 'evaluation window is incomplete'
    else:
        numerator, denominator = result.get('numerator'), result.get('denominator')
        valid = all(isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v) for v in (numerator, denominator))
        if valid and numerator >= 0 and denominator > 0 and result.get('eligible') is True:
            ratio = numerator / denominator
            status = 'CONFIRMED' if ratio >= bounds['confirmAtLeast'] else 'REFUTED' if ratio < bounds['refuteBelow'] else 'INCONCLUSIVE'
            reason = 'frozen ratio boundaries'
    return {'status': status, 'reason': reason, 'ratio': ratio,
            'tentative': result.get('final') is not True,
            'direction': result.get('direction', 'unknown'), 'watermark': result['watermark'],
            'definitionHash': card['definitionHash']}


def calibration(evaluations):
    final = [e for e in evaluations if not e['tentative'] and e['status'] != 'PENDING']
    hits = sum(e['status'] == 'CONFIRMED' for e in final)
    misses = sum(e['status'] == 'REFUTED' for e in final)
    return {'confirmed': hits, 'refuted': misses, 'final': len(final),
            'hitRate': hits/(hits+misses) if hits+misses else None,
            'evaluability': (hits+misses)/len(final) if final else None,
            'confidenceAdjustment': 'disabled'}


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('card', type=Path); ap.add_argument('result', type=Path)
    args = ap.parse_args()
    print(json.dumps(evaluate(json.loads(args.card.read_text()), json.loads(args.result.read_text())), indent=2, allow_nan=False))
