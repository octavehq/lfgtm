"""Metrics for normalized, explicitly scoped rows. No inferred causal effects."""
from datetime import datetime
import math


def timestamp(value):
    date=datetime.fromisoformat(value.replace('Z','+00:00'))
    if date.tzinfo is None:raise ValueError('timestamps require timezone offsets')
    return date


def closed_cohort(rows,start,end,as_of):
    start,end,as_of=map(timestamp,(start,end,as_of))
    if start>=end or end>as_of:raise ValueError('invalid cohort boundaries')
    latest={};gaps=[]
    for row in rows:
        if not row.get('opportunityId') or not row.get('updatedAt'):
            gaps.append({'reason':'missing identity or revision timestamp'});continue
        if timestamp(row['updatedAt'])>as_of:continue
        old=latest.get(row['opportunityId'])
        if old and timestamp(old['updatedAt'])==timestamp(row['updatedAt']) and old!=row:
            raise ValueError('conflicting snapshots at the same opportunity revision')
        if old is None or timestamp(row['updatedAt'])>timestamp(old['updatedAt']):latest[row['opportunityId']]=row
    cohort=[]
    for row in latest.values():
        if row.get('outcome') not in ('won','lost','no_decision'):continue
        if not row.get('closedAt'):
            gaps.append({'opportunityId':row['opportunityId'],'reason':'missing close date'});continue
        if start<=timestamp(row['closedAt'])<end:cohort.append(row)
    return {'rows':cohort,'coverageGaps':gaps,'scope':{'start':start.isoformat(),'end':end.isoformat(),'asOf':as_of.isoformat(),'unit':'opportunity'}}


def outcome_metric(rows):
    if len({r['opportunityId'] for r in rows})!=len(rows):raise ValueError('duplicate opportunities in metric input')
    wins=sum(r['outcome']=='won' for r in rows);losses=sum(r['outcome']=='lost' for r in rows)
    denominator=wins+losses
    return {'wins':wins,'losses':losses,'noDecision':sum(r['outcome']=='no_decision' for r in rows),
            'denominator':denominator,'winRate':wins/denominator if denominator else None,
            'definition':'won / (won + lost); no-decision reported separately'}


def reconcile(raw,joined,keys=('customerId','campaignId','adGroupId','adId'),tolerance=1e-6):
    def index(rows):
        out={}
        for row in rows:
            key=tuple(row[k] for k in keys)
            if key in out:raise ValueError('duplicate normalized metric key')
            out[key]=row
        return out
    left,right=index(raw),index(joined)
    if left.keys()!=right.keys():raise ValueError('missing or additional joined metric keys')
    for key,l in left.items():
        r=right[key]
        for field in ('impressions','clicks','costMicros'):
            if not isinstance(l[field],int) or not isinstance(r[field],int) or l[field]!=r[field]:
                raise ValueError(f'joined {field} does not reconcile exactly')
        if not all(isinstance(x,(int,float)) and math.isfinite(x) for x in (l['conversions'],r['conversions'])) or abs(l['conversions']-r['conversions'])>tolerance:
            raise ValueError('joined conversions exceed tolerance')
    return {'keys':len(left),'reconciled':True,'conversionTolerance':tolerance}
