"""Synthetic regressions. No customer data or live service writes."""
import copy
import hashlib
from datetime import datetime, timezone
import importlib.util
import json
import os
import shutil
import subprocess
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'skills/get-brand-components/scripts'))
sys.path.insert(0, str(ROOT/'skills/shared/scripts'))
def module(name, path):
    spec=importlib.util.spec_from_file_location(name,ROOT/path)
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
io=module('artifact_io','skills/asset-manager/scripts/artifact_io.py')
lint=module('html_lint','skills/shared/scripts/html_lint.py')
brand=module('brand','skills/get-brand-components/scripts/render_kit.py')
cache=module('cache','skills/get-brand-components/scripts/brand_cache.py')
logos=module('logos','skills/get-brand-components/scripts/verify_logos.py')
state=module('state','skills/shared/scripts/workspace_state.py')
digest=module('digest','skills/digest/scripts/digest_state.py')
pred=module('pred','skills/ads-resonance/scripts/predictions.py')
creative=module('creative','skills/ads/scripts/creative.py')
rows=module('rows','skills/shared/scripts/analysis_rows.py')


class Reliability(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)
    def tearDown(self):self.tmp.cleanup()

    def test_dotted_ancestors_and_hidden_members(self):
        folder=self.root/'.output'/'a';folder.mkdir(parents=True)
        (folder/'index.html').write_text('ok');(folder/'.private').write_text('private')
        self.assertEqual([n for n,_ in io.files_for(folder)],['index.html'])

    def test_publish_manifest_excludes_notes(self):
        (self.root/'index.html').write_text('public');(self.root/'notes.md').write_text('private')
        manifest=self.root/'approved.json';manifest.write_text('["index.html"]')
        self.assertEqual([n for n,_ in io.files_for(self.root,manifest)],['index.html'])

    def test_paths_reject_escape_and_symlink(self):
        for name in ('../secret','/secret','a/../../secret','a\\b','a//b'):
            with self.subTest(name=name),self.assertRaises(ValueError):io.checked_path(self.root,name)
        (self.root/'link').symlink_to(self.root.parent,target_is_directory=True)
        with self.assertRaises(ValueError):io.checked_path(self.root,'link/secret')

    def test_zip_rejects_traversal(self):
        path=self.root/'bad.zip'
        with zipfile.ZipFile(path,'w') as z:z.writestr('../private','x')
        with self.assertRaises(ValueError):io.checked_zip(path)

    def test_atomic_download_preserves_existing_on_failure(self):
        out=self.root/'saved.txt';out.write_bytes(b'old')
        with self.assertRaises(ValueError):io.atomic_download(self.root,'saved.txt',b'new',True,size=8)
        self.assertEqual(out.read_bytes(),b'old')
        with self.assertRaises(ValueError):io.atomic_download(self.root,'saved.txt',b'new')
        io.atomic_download(self.root,'saved.txt',b'new',True,size=3)
        self.assertEqual(out.read_bytes(),b'new')

    def test_null_previews_and_pretty_json(self):
        raw=json.dumps({'uuid':'artifact-1','previewUrl':None,'description':'He said "hello"'},indent=2).encode()
        for status in ('200','201'):self.assertEqual(io.parse_response(raw,status,True)['uuid'],'artifact-1')

    def test_malformed_success_is_indeterminate(self):
        for raw in (b'not json',b'{}',b'{"uuid":3}'):
            with self.assertRaises(io.Indeterminate):io.parse_response(raw,'201',True)

    def run_upload(self,operation):
        folder=self.root/'.artifact';folder.mkdir(exist_ok=True);(folder/'index.html').write_text('test')
        before={'uuid':'artifact-1','identifier':'example','description':'old','type':'website','privacy':'workspace','status':'published','entryPoint':'index.html','currentVersion':1}
        after={**before,'description':'Quoted "text"','currentVersion':2,'previewUrl':None,'metadata':{'filesMap':[{'path':'index.html','size':4}]}}
        calls=[]
        def request(base,token,route,method='GET',payload=None,archive=None):
            calls.append(method)
            if method!='GET':
                self.assertEqual(payload['description'],'Quoted "text"')
                self.assertEqual(io.checked_zip(archive),['index.html'])
            value=after if method!='GET' or any(c!='GET' for c in calls) else before
            return json.dumps(value,indent=2).encode(),'201' if operation!='update' and method=='POST' else '200'
        argv=['artifact_io',operation,'--src',str(folder),'--identifier','example','--description','Quoted "text"']
        if operation=='update':argv+=['--uuid','artifact-1']
        with patch.object(sys,'argv',argv),patch.dict('os.environ',{'ARTIFACTS_ACCESS_TOKEN':'synthetic'}),patch.object(io,'request',side_effect=request):io.main()
        self.assertEqual(sum(m!='GET' for m in calls),1)

    def test_create_zip_and_update_readback(self):
        for op in ('create','zip','update'):
            with self.subTest(operation=op):self.run_upload(op)

    def test_shell_wrappers_without_jq(self):
        folder=self.root/'.octave-decks/example';folder.mkdir(parents=True)
        (folder/'index.html').write_text('test');(folder/'.notes').write_text('private')
        bins=self.root/'bin';bins.mkdir()
        for command in ('bash','dirname','python3'):
            (bins/command).symlink_to(shutil.which(command))
        fake=bins/'curl'
        fake.write_text('#!'+sys.executable+'\n'+'''import json,os,sys,zipfile
from pathlib import Path
a=sys.argv[1:];method=a[a.index('-X')+1];counter=Path(os.environ['FIXTURE_COUNTER'])
written=counter.exists()
if method!='GET':
    payload=json.loads(a[a.index('--form-string')+1].split('=',1)[1])
    assert payload['description']=='Quoted "text"'
    archive=a[a.index('-F')+1].split('@',1)[1].split(';',1)[0]
    with zipfile.ZipFile(archive) as z:assert z.namelist()==['index.html']
    counter.write_text('written');written=True
assert 'synthetic' in sys.stdin.read()
body={'uuid':'artifact-1','identifier':'example','description':'Quoted "text"','type':'website','privacy':'workspace','status':'published','entryPoint':'index.html','previewUrl':None,'currentVersion':2 if written else 1,'metadata':{'filesMap':[{'path':'index.html','size':4}]}}
Path(a[a.index('-o')+1]).write_text(json.dumps(body,indent=2))
print('201' if method=='POST' else '200',end='')
''');fake.chmod(0o755)
        for script in ('upload-artifact.sh','zip-and-upload-artifact.sh','update-artifact.sh'):
            counter=self.root/'counter';counter.unlink(missing_ok=True)
            args=[str(bins/'bash'),str(ROOT/'skills/asset-manager/scripts'/script),'--src',str(folder),'--identifier','example','--description','Quoted "text"']
            if script=='update-artifact.sh':args+=['--uuid','artifact-1']
            result=subprocess.run(args,capture_output=True,text=True,env={**os.environ,'PATH':str(bins),'ARTIFACTS_ACCESS_TOKEN':'synthetic','FIXTURE_COUNTER':str(counter)})
            self.assertEqual(result.returncode,0,result.stderr);self.assertNotIn('synthetic',result.stdout)

    def test_all_cta_renderers_preserve_links(self):
        ctx={'kitdir':self.root,'render':{},'darkband':False,'icons':{},'slug':'test'}
        link={'label':'Go & learn','href':'https://example.com/?x=1&y=2','target':'_blank'}
        blocks=[(brand.r_hero,{'title':'Title','cta':link,'nav':{'links':[link],'cta':link}}),
                (brand.r_cta,{'heading':'Title','cta':link}), (brand.r_split,{'cta':link}),
                (brand.r_pricing,{'plans':[{'name':'Plan','cta':link}]}),(brand.r_footer,{'links':[link]})]
        for renderer,block in blocks:
            with self.subTest(renderer=renderer.__name__):
                output=renderer(block,ctx);self.assertIn('href="https://example.com/?x=1&amp;y=2"',output);self.assertIn('rel="noopener noreferrer"',output)

    def test_links_and_svg_reject_executable_input(self):
        for href in ('javascript:alert(1)','data:text/html,x','//evil.example','https://example.com/\n'):
            with self.assertRaises(ValueError):brand.render_link({'label':'Go','href':href})
        with self.assertRaises(ValueError):brand.render_link({'label':'Go'})
        with self.assertRaises(ValueError):brand.icon_svg(self.root,{'inner':'<script>alert(1)</script>'},{})
        self.assertIn('&lt;b&gt;',brand.r_cta({'heading':'Title','custLine':'<b>text</b>'},{'darkband':False}))

    def test_logo_spaces_unicode_dimensions(self):
        svg=self.root/'Acme Cloud 图.svg';svg.write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 160 40"><path d="M0 0 L10 10"/></svg>')
        self.assertEqual(logos.dimensions(svg),(160,40))

    def test_missing_font_and_wrong_brand_fail(self):
        man={'canonicalDomain':'example.com','workspaceOId':'workspace-a','render':{'tokens':{},'fonts':[{'file':'absent.woff2'}]}}
        with self.assertRaises(ValueError):brand.validate_manifest(self.root,man)
        man['render']['fonts']=[]
        with self.assertRaises(ValueError):brand.validate_manifest(self.root,man,'example.org','workspace-a')

    def test_failed_refresh_preserves_promoted_brand(self):
        staging=self.root/'staging';staging.mkdir()
        for name in ('tokens.css','brand-kit.md','components.html'):(staging/name).write_text('synthetic visual fixture')
        tokens={'--brand-bg':'#fff','--brand-ink':'#111','--brand-primary':'#124c80','--brand-font-heading':'Arial','--brand-font-body':'Arial'}
        man={'schemaVersion':1,'canonicalDomain':'example.com','workspaceOId':'workspace-a','capturedAt':'2026-01-01T00:00:00Z','sourceUrls':['https://example.com'],'allowedUse':{'text':'synthetic'},'assetChecksums':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in staging.iterdir()},'render':{'tokens':tokens}}
        (staging/'manifest.json').write_text(json.dumps(man))
        target=cache.promote(staging,self.root/'cache','EXAMPLE.COM','workspace-a');before=(target/'current.json').read_text()
        (staging/'tokens.css').write_text('changed without checksum')
        with self.assertRaises(ValueError):cache.promote(staging,self.root/'cache','example.com','workspace-a')
        self.assertEqual((target/'current.json').read_text(),before)
        self.assertEqual(cache.resolve(target,'example.com','workspace-a')[1]['canonicalDomain'],'example.com')

    def test_lint_preserves_quotes_and_draft_inputs(self):
        path=self.root/'a.html';path.write_text('<!DOCTYPE html><html><blockquote>Robust — leverage</blockquote><p>[PRICE]</p></html>')
        policy=dict(lint.DEFAULT);policy['readiness']='seller_draft'
        errors,warnings=lint.lint(path,policy);self.assertFalse(errors);self.assertEqual(len(warnings),1)
        policy['readiness']='buyer_ready';self.assertTrue(lint.lint(path,policy)[0])
        policy['intentionalPlaceholders']=['[PRICE]'];self.assertFalse(lint.lint(path,policy)[0])

    def test_lint_rejects_private_links_and_missing_resource(self):
        path=self.root/'a.html';path.write_text('<!DOCTYPE html><a href="https://app.octavehq.com/entity/abc">source</a><img src="missing.png">')
        policy=dict(lint.DEFAULT);policy['audience']='restricted_external'
        self.assertEqual(len(lint.lint(path,policy)[0]),2)

    def test_workspace_identity_and_interrupted_lock(self):
        path=self.root/'state.json';state.atomic_json(path,{'schemaVersion':1,'workspaceOId':'workspace-a'})
        with self.assertRaises(ValueError):state.read_bound(path,'workspace-b')
        with self.assertRaises(RuntimeError):
            with state.exclusive_lock(self.root,'run-a'):raise RuntimeError('interrupted')
        with self.assertRaises(RuntimeError):
            with state.exclusive_lock(self.root,'run-b'):pass

    def test_digest_once_and_changed_scope(self):
        spec={'schemaVersion':1,'workspaceOId':'workspace-a','digestId':'digest-a','companyOId':'company-a','name':'Digest','sources':[],'selectionRules':{},'timezone':'UTC','window':{},'evidenceDepth':'full','density':'detailed','format':'html','brandIdentity':{},'distribution':{'audience':'internal','privacy':'workspace','recipients':[]},'recurrence':{}}
        directory=self.root/'workspace-a/digest-a';state.atomic_json(directory/'spec.json',spec)
        reports=[{'id':'report-1','status':'completed'}]
        run=digest.begin(self.root,'workspace-a','digest-a',reports)
        with self.assertRaises(RuntimeError):digest.begin(self.root,'workspace-a','digest-a',reports)
        with self.assertRaises(ValueError):digest.complete(self.root,'workspace-a','digest-a',run['runId'],{'verified':False})
        digest.complete(self.root,'workspace-a','digest-a',run['runId'],{'verified':True,'contentChecksum':'synthetic','outputPaths':['output.html']})
        self.assertEqual(digest.begin(self.root,'workspace-a','digest-a',reports)['status'],'already_verified')
        with self.assertRaises(ValueError):digest.begin(self.root,'workspace-a','digest-a',[{'id':'unfinished','status':'running'}])

    def prediction(self):
        definition={'workspaceOId':'workspace-a','platform':'google','customerId':'123','unitIds':['a','b'],'evaluation_window':{'start':'2026-01-01T00:00:00Z','end':'2026-02-01T00:00:00Z','timezone':'UTC'},'boundaries':{'confirmAtLeast':3,'refuteBelow':2}}
        card={'schemaVersion':'0.3','definition':definition,'definitionHash':pred.definition_hash(definition)}
        result={'workspaceOId':'workspace-a','platform':'google','customerId':'123','unitIds':['a','b'],'watermark':'2026-02-02T00:00:00Z','final':True,'numerator':3,'denominator':1,'eligible':True}
        result['evaluation_window']=copy.deepcopy(definition['evaluation_window'])
        return card,result

    def test_ratio_boundaries_and_incomplete_evidence(self):
        card,result=self.prediction()
        for number,status in [(1.9,'REFUTED'),(2,'INCONCLUSIVE'),(2.9,'INCONCLUSIVE'),(3,'CONFIRMED'),(None,'INCONCLUSIVE')]:
            result['numerator']=number;self.assertEqual(pred.evaluate(card,result)['status'],status)
        result['denominator']=0;self.assertEqual(pred.evaluate(card,result)['status'],'INCONCLUSIVE')
        result['watermark']='2026-01-10T00:00:00Z';self.assertEqual(pred.evaluate(card,result)['status'],'PENDING')

    def test_prediction_cannot_change_units_or_definition(self):
        card,result=self.prediction();result['unitIds']=['a','c']
        with self.assertRaises(ValueError):pred.evaluate(card,result)
        result['unitIds']=['a','b'];card['definition']['boundaries']['confirmAtLeast']=2
        with self.assertRaises(ValueError):pred.evaluate(card,result)

    def test_calibration_is_descriptive_and_final_only(self):
        rows=[{'status':'CONFIRMED','tentative':False}]*4+[{'status':'REFUTED','tentative':False}]*6+[{'status':'CONFIRMED','tentative':True}]
        value=pred.calibration(rows);self.assertEqual(value['hitRate'],.4);self.assertEqual(value['confidenceAdjustment'],'disabled')

    def ad(self):
        return {'customerId':'123','isManager':False,'finalUrl':'https://example.com','campaign':'Quoted, "campaign"','adGroup':'Example','headlines':[{'text':x} for x in ['One','Two','Three']],'descriptions':[{'text':x} for x in ['Description one','Description two']]}

    def test_csv_unicode_quotes_and_three_headlines(self):
        ad=self.ad();out=self.root/'ads.csv';creative.export_csv([ad],out)
        self.assertIn('"Quoted, ""campaign"""',out.read_text());self.assertEqual(creative.text_length('界'),2)
        ad['headlines'][0]['text']='界'*16
        with self.assertRaises(ValueError):creative.validate(ad)

    def test_previews_bounded_and_attribution_isolated(self):
        ad=self.ad();ad['headlines']=[{'text':str(i)} for i in range(15)];ad['headlines'][0]['pin']=1
        previews=creative.previews(ad);self.assertLessEqual(len(previews),12);self.assertTrue(all(p['headlines'][0]=='0' for p in previews))
        card={'workspaceOId':'other','customerId':'123','fingerprint':creative.fingerprint(ad)}
        self.assertIsNone(creative.match_creative(ad,[card],'workspace-a'))
        card['workspaceOId']='workspace-a';self.assertIsNone(creative.match_creative(ad,[card,copy.deepcopy(card)],'workspace-a'))

    def test_metrics_preserve_denominator_and_missing_joined_keys(self):
        metric=rows.outcome_metric([{'opportunityId':str(i),'outcome':'won' if i<9 else 'lost'} for i in range(14)])
        self.assertEqual(metric['denominator'],14);self.assertAlmostEqual(metric['winRate'],9/14)
        raw=[{'customerId':'123','campaignId':'c','adGroupId':'g','adId':'a','impressions':500,'clicks':20,'costMicros':3000000,'conversions':1.25}]
        self.assertTrue(rows.reconcile(raw,copy.deepcopy(raw))['reconciled'])
        with self.assertRaises(ValueError):rows.reconcile(raw,[])
        joined=copy.deepcopy(raw);joined[0]['costMicros']+=1
        with self.assertRaises(ValueError):rows.reconcile(raw,joined)

    def test_reopened_opportunity_is_not_counted_twice(self):
        records=[{'opportunityId':'a','outcome':'won','closedAt':'2026-01-05T00:00:00Z','updatedAt':'2026-01-05T00:00:00Z'},
                 {'opportunityId':'a','outcome':'open','updatedAt':'2026-01-07T00:00:00Z'}]
        cohort=rows.closed_cohort(records,'2026-01-01T00:00:00Z','2026-02-01T00:00:00Z','2026-02-02T00:00:00Z')
        self.assertEqual(cohort['rows'],[])


if __name__=='__main__':unittest.main()
