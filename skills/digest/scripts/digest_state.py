#!/usr/bin/env python3
"""Durable digest execution records; no hosting calls or implicit publication."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import sys
import uuid
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'shared/scripts'))
from workspace_state import atomic_json, component, digest_key, read_bound, unsafe_symlink


REQUIRED = {'schemaVersion', 'workspaceOId', 'digestId', 'companyOId', 'name', 'sources',
            'selectionRules', 'timezone', 'window', 'evidenceDepth', 'density', 'format',
            'brandIdentity', 'distribution', 'recurrence'}


def validate_spec(spec, workspace):
    if REQUIRED - spec.keys(): raise ValueError('missing digest specification fields: '+', '.join(sorted(REQUIRED-spec.keys())))
    if spec['schemaVersion'] != 1 or spec['workspaceOId'] != component(workspace): raise ValueError('unsupported or mismatched digest identity')
    component(spec['digestId'])
    if not isinstance(spec['distribution'], dict) or not {'audience','privacy','recipients'} <= spec['distribution'].keys():
        raise ValueError('distribution requires audience, privacy and recipients')
    return spec


def begin(root, workspace, digest, reports):
    directory=Path(root)/component(workspace)/component(digest)
    spec=validate_spec(read_bound(directory/'spec.json',workspace),workspace)
    key=digest_key(spec,reports)
    checkpoint=directory/'checkpoint.json'
    prior=read_bound(checkpoint,workspace) if checkpoint.exists() else None
    if prior and prior['key']==key: return {'status':'already_verified',**prior}
    consumed=set((prior or {}).get('consumedReportRunIds',[]))
    if not reports or set(r['id'] for r in reports)<=consumed: return {'status':'no_new_material'}
    directory.mkdir(parents=True,exist_ok=True)
    if any(unsafe_symlink(p) for p in (directory,*directory.parents)): raise ValueError('symlink in state directory')
    run=uuid.uuid4().hex
    try:
        with (directory/'run.lock').open('x') as f:
            json.dump({'runId':run,'key':key},f); f.flush()
    except FileExistsError:
        raise RuntimeError('active or interrupted run; inspect run.lock and reconcile before retrying')
    record={'schemaVersion':1,'workspaceOId':workspace,'runId':run,'key':key,'status':'drafting',
            'reportRunIds':sorted(set(r['id'] for r in reports)), 'specChecksum':digest_key(spec,[]),
            'createdAt':datetime.now(timezone.utc).isoformat(),'coverage':{},'unresolvedInputs':[]}
    atomic_json(directory/'runs'/f'{run}.json',record)
    return record


def complete(root,workspace,digest,run,verification):
    directory=Path(root)/component(workspace)/component(digest)
    record=read_bound(directory/'runs'/f'{component(run)}.json',workspace)
    lock=json.loads((directory/'run.lock').read_text())
    if lock.get('runId')!=run or lock.get('key')!=record['key']:raise ValueError('run does not own lock')
    spec=validate_spec(read_bound(directory/'spec.json',workspace),workspace)
    if digest_key(spec,[])!=record['specChecksum']:raise ValueError('spec changed; revalidate distribution and output')
    if verification.get('verified') is not True or not verification.get('contentChecksum') or not verification.get('outputPaths'):
        raise ValueError('output verification required before consuming reports')
    if spec['distribution'].get('publish') and not all(verification.get(k) for k in ('artifactId','artifactVersion','accessVerified')):
        raise ValueError('publication readback/access verification required')
    record.update({'status':'verified','verification':verification})
    atomic_json(directory/'runs'/f'{run}.json',record)
    prior=read_bound(directory/'checkpoint.json',workspace) if (directory/'checkpoint.json').exists() else {}
    atomic_json(directory/'checkpoint.json',{'schemaVersion':1,'workspaceOId':workspace,'key':record['key'],
                'consumedReportRunIds':sorted(set(prior.get('consumedReportRunIds',[])+record['reportRunIds'])),
                'verification':verification,'runId':run})
    (directory/'run.lock').unlink()
    return record


if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('action',choices=['begin','complete']);ap.add_argument('--root',type=Path,default=Path('.octave/digests'))
    ap.add_argument('--workspace',required=True);ap.add_argument('--digest',required=True)
    ap.add_argument('--input',type=Path,required=True);ap.add_argument('--run')
    a=ap.parse_args();payload=json.loads(a.input.read_text())
    result=begin(a.root,a.workspace,a.digest,payload) if a.action=='begin' else complete(a.root,a.workspace,a.digest,a.run,payload)
    print(json.dumps(result,indent=2))
