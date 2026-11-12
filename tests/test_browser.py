"""Offline Chromium checks for executable controllers and brand blocks."""
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]


class BrowserChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pw=sync_playwright().start();cls.browser=cls.pw.chromium.launch()
    @classmethod
    def tearDownClass(cls):cls.browser.close();cls.pw.stop()
    def setUp(self):
        self.context=self.browser.new_context();self.page=self.context.new_page();self.errors=[]
        self.page.on('pageerror',lambda error:self.errors.append(str(error)))
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name).resolve()
    def tearDown(self):
        self.context.close();self.tmp.cleanup();self.assertEqual(self.errors,[])

    def test_lesson_gating_wrong_answer_restart_tabs_and_print(self):
        script=(ROOT/'skills/train/assets/lesson.js').read_text()
        scaffold=(ROOT/'skills/train/references/html-scaffold.md').read_text()
        css=re.search(r'```css\n(.*?)```',scaffold,re.S)[1]
        tabs=''.join(f'<div data-tabset><div class="tabs"><button class="tab">A{i}</button><button class="tab">B{i}</button></div><div class="tpanel active">Panel A{i}</div><div class="tpanel">Panel B{i}</div></div>' for i in range(2))
        self.page.set_content(f'''<!doctype html><style>{css}</style><div id="dots"></div>
          <div class="deck"><section class="slide" data-type="cover"><button data-start>Start</button></section>
          <section class="slide" id="topic" data-type="content"><div class="slide-body">{tabs}
          <div data-checkpoint><button class="cp-opt" data-answer="false">Wrong</button><button class="cp-opt" data-answer="true">Right</button><div class="cp-explain">Reasoning</div></div></div><button data-next>Next</button></section>
          <section class="slide" data-type="done"><div class="score-big"></div><button data-restart>Restart</button></section></div><script>{script}</script>''')
        self.assertFalse(self.page.evaluate('go(2)'))
        self.page.get_by_text('Start',exact=True).click()
        self.assertTrue(self.page.locator('[data-next]').is_disabled())
        self.page.get_by_text('B0',exact=True).click()
        self.assertEqual(self.page.locator('.tpanel.active').all_text_contents(),['Panel B0','Panel A1'])
        self.page.get_by_text('Wrong',exact=True).click();self.assertTrue(self.page.locator('.cp-explain').is_visible())
        self.assertFalse(self.page.locator('[data-next]').is_disabled());self.page.locator('[data-next]').click()
        self.assertEqual(self.page.locator('.score-big').inner_text(),'0 / 1')
        self.page.get_by_text('Restart',exact=True).click();self.page.get_by_text('Start',exact=True).click()
        self.assertTrue(self.page.locator('[data-next]').is_disabled());self.assertFalse(self.page.get_by_text('Wrong',exact=True).is_disabled())
        self.page.emulate_media(media='print')
        self.assertTrue(all(self.page.locator('.slide').nth(i).is_visible() for i in range(3)))
        self.assertTrue(self.page.locator('.cp-explain').is_visible())

    def test_lesson_reports_answers_score_and_topic_results(self):
        script=(ROOT/'skills/train/assets/lesson.js').read_text()
        scaffold=(ROOT/'skills/train/references/html-scaffold.md').read_text()
        css=re.search(r'```css\n(.*?)```',scaffold,re.S)[1]
        form_css=(ROOT/'skills/shared/formats/response-form.css').read_text()
        def topic(sid,title,checks):
            qs=''.join(f'<div data-checkpoint="{key}"><div class="q-text"> {q} </div><button class="cp-opt" data-answer="false">No {key}</button><button class="cp-opt" data-answer="true">Yes {key}</button></div>' for key,q in checks)
            return f'<section class="slide" id="{sid}" data-type="content"><h2>{title}</h2><div class="slide-body">{qs}</div><button data-next>Next {sid}</button></section>'
        def lesson(recorder):
            return f'''<!doctype html><html><head><style>{css}{form_css}</style>{recorder}</head><body><div id="dots"></div>
          <div class="deck"><section class="slide" data-type="cover"><button data-start>Start</button></section>
          {topic('sell','What we sell',[('sell-1','Which problem?'),('sell-2','What does it replace?')])}
          {topic('buy','Who buys',[('buy-1','Who signs?')])}
          <section class="slide gradient" data-type="done" id="done"><div class="slide-inner"><div class="done-grid"><div class="done-score">
            <p class="score-big"></p><p data-score-msg></p>
            <div class="review-menu"><button data-go="sell">What we sell</button><button data-go="buy">Who buys</button></div>
            <p class="record-note">Shared</p><button class="btn-quiet" data-restart>Restart</button></div>
            <div class="done-form"><form class="rf" data-octave-form="lesson-feedback"><textarea name="notes"></textarea><button type="submit">Send note</button></form></div>
          </div></div></section></div><script>{script}</script></body></html>'''
        # Published: a stand-in for Octave's recorder collects what the lesson reports.
        recorder='<script>window.sent=[];window.octave={record:(name,data,key)=>{window.sent.push({name,data,key});return true}};document.documentElement.setAttribute("data-octave-recording","")</script>'
        self.page.set_content(lesson(recorder))
        self.assertEqual(self.page.evaluate('sent'),[])  # opening the lesson reports nothing
        self.page.get_by_text('Start',exact=True).click()
        self.page.get_by_text('No sell-1',exact=True).click();self.page.get_by_text('Yes sell-2',exact=True).click()
        self.page.get_by_text('Next sell',exact=True).click();self.page.get_by_text('Yes buy-1',exact=True).click()
        self.page.get_by_text('Next buy',exact=True).click()
        sent=self.page.evaluate('sent')
        self.assertEqual([(e['name'],e['key']) for e in sent],[('slide','2'),('answer','sell-1'),('answer','sell-2'),('slide','3'),('answer','buy-1'),('slide','4'),('score','final')])
        self.assertEqual(sent[1]['data'],{'question':'Which problem?','choice':'No sell-1','correct':False})
        self.assertEqual(sent[0]['data'],{'type':'content','title':'What we sell','of':4})
        self.assertEqual(sent[-1]['data'],{'correct':2,'total':3})
        self.assertEqual(self.page.locator('[data-score-msg]').inner_text(),'1 to revisit. Those topics are listed first.')
        rows=self.page.locator('.review-menu button')
        self.assertEqual(rows.all_inner_texts(),['What we sell\n1 of 2','Who buys\n1 of 1'])
        self.assertEqual([rows.nth(i).get_attribute('data-result') for i in range(2)],['missed','clear'])
        self.assertTrue(self.page.locator('.done-form').is_visible());self.assertTrue(self.page.locator('.record-note').is_visible())
        # The completion slide reports the score once, however often it is revisited.
        rows.nth(0).click();self.page.evaluate('go(3)')
        self.assertEqual(len([e for e in self.page.evaluate('sent') if e['name']=='score']),1)
        self.page.get_by_text('Restart',exact=True).click()
        self.assertEqual(self.page.evaluate('sent')[-1]['name'],'restart')
        # Opened from disk: no recorder, no errors, and no form that would go nowhere.
        self.page.set_content(lesson(''))
        self.page.get_by_text('Start',exact=True).click()
        self.page.get_by_text('Yes sell-1',exact=True).click();self.page.get_by_text('Yes sell-2',exact=True).click()
        self.page.get_by_text('Next sell',exact=True).click();self.page.get_by_text('Yes buy-1',exact=True).click()
        self.page.get_by_text('Next buy',exact=True).click()
        self.assertEqual(self.page.locator('.score-big').inner_text(),'3 / 3')
        self.assertEqual(self.page.locator('[data-score-msg]').inner_text(),'Every check cleared on the first attempt.')
        self.assertFalse(self.page.locator('.done-form').is_visible());self.assertFalse(self.page.locator('.record-note').is_visible())

    def test_response_form_fits_a_phone_on_light_and_dark(self):
        form_css=(ROOT/'skills/shared/formats/response-form.css').read_text()
        tokens=':root{--brand-bg:#fff;--brand-ink:#14181f;--brand-muted:#5b6472;--brand-border:#d9dee7;--brand-primary:#2f5bea;--brand-band:#101828;--brand-font-body:system-ui;--brand-font-heading:system-ui}'
        form='''<form class="rf" data-octave-form="f"><div class="rf-head"><h3 class="rf-title">Want the pilot plan?</h3></div>
          <div class="rf-fields"><div class="rf-row"><div class="rf-field"><label for="n">Name</label><input id="n" name="name" type="text"></div>
          <div class="rf-field"><label for="e">Work email</label><input id="e" name="email" type="email"></div></div>
          <div class="rf-field"><label for="t">Notes</label><textarea id="t" name="notes"></textarea></div></div>
          <div class="rf-actions"><button class="btn" type="submit">Send</button><p data-octave-notice>Shared with the owner.</p></div></form>'''
        self.page.set_viewport_size({'width':375,'height':812})
        self.page.set_content(f'<!doctype html><style>{tokens}body{{margin:0;padding:16px}}{form_css}</style><div id="light">{form}</div><div id="dark" class="is-dark" style="background:#101828;padding:16px">{form}</div>')
        self.assertFalse(self.page.evaluate('document.documentElement.scrollWidth > innerWidth'))
        for root in ('#light','#dark'):
            boxes=self.page.evaluate(f'''[...document.querySelectorAll("{root} input,{root} textarea")].map(e=>{{const r=e.getBoundingClientRect();return [Math.round(r.left),Math.round(r.height)]}})''')
            self.assertEqual(len({left for left,_ in boxes}),1)  # the two-up row stacks into one column
            self.assertTrue(all(height>=44 for _,height in boxes))
        ink=lambda root:self.page.evaluate(f'getComputedStyle(document.querySelector("{root} input")).color')
        self.assertNotEqual(ink('#light'),ink('#dark'))

    def test_deck_navigation_edit_export_mobile(self):
        script=(ROOT/'skills/deck/assets/presentation.js').read_text()
        css='@media(min-width:721px){.slide{display:none}.slide.active{display:block}}'
        path=self.root/'deck.html';path.write_text(f'''<!doctype html><html data-content-version="fixture-1" data-deck-edit><style>{css}</style><div id="deckStage"><section class="slide"><p data-editable>First</p></section><section class="slide"><p>Second</p></section></div><div id="deckControls"></div><button id="editToggle">Edit</button><button data-export-html>Export</button><script>{script}</script></html>''')
        self.page.goto(path.as_uri());self.page.get_by_text('Next',exact=True).click()
        self.assertEqual(self.page.locator('.slide.active').inner_text(),'Second')
        self.page.get_by_text('Previous',exact=True).click();self.page.get_by_text('Edit',exact=True).click()
        self.page.locator('[data-editable]').fill('Revised')
        with self.page.expect_download() as info:self.page.get_by_text('Export',exact=True).click()
        export=self.root/'export.html';info.value.save_as(export)
        self.assertIn('Revised',export.read_text())
        self.page.goto(export.as_uri());self.assertEqual(self.page.locator('[contenteditable]').count(),0)
        self.assertEqual(self.page.locator('#editToggle,[data-export-html],html[data-deck-edit]').count(),0)  # the export is the shareable file
        self.page.get_by_text('Next',exact=True).click()
        self.assertEqual(self.page.locator('.slide.active').inner_text(),'Second')
        self.page.set_viewport_size({'width':375,'height':812})
        self.page.wait_for_function('document.querySelectorAll(\'.slide[aria-hidden="false"]\').length === 2')
        self.assertEqual(self.page.locator('.slide[aria-hidden="false"]').count(),2)
        shared=self.root/'shared.html';shared.write_text(path.read_text().replace(' data-deck-edit',''))
        self.page.goto(shared.as_uri());self.page.keyboard.press('e')
        self.assertEqual(self.page.locator('#editToggle,[data-export-html],[contenteditable=true]').count(),0)  # no editor chrome without opt-in

    def test_reveal_failure_and_reduced_motion_preserve_content(self):
        script=(ROOT/'skills/microsite/assets/reveal.js').read_text()
        for setup in ('window.IntersectionObserver=undefined;', 'window.IntersectionObserver=function(){throw new Error("unavailable")};'):
            self.page.set_content(f'<main style="margin-top:1000px"><p class="animate-in">Visible</p><a href="#target">Go</a></main><script>{setup}{script}</script>')
            self.assertEqual(self.page.locator('.reveal-pending').count(),0)
            self.assertTrue(self.page.get_by_text('Visible',exact=True).is_visible())

    def test_shared_render_gate_detects_missing_asset(self):
        path=self.root/'gate.html'
        path.write_text('<!doctype html><html><style>body{color:#111;background:white;font-family:Arial}</style><p>Readable content</p></html>')
        command=['node',str(ROOT/'skills/shared/scripts/render-gate.js'),str(path),'--viewports','800x600','--json']
        result=subprocess.run(command,capture_output=True,text=True)
        self.assertEqual(result.returncode,0,result.stderr+result.stdout)
        path.write_text(path.read_text().replace('</html>','<img src="missing.png" alt="Missing"></html>'))
        result=subprocess.run(command,capture_output=True,text=True)
        self.assertEqual(result.returncode,1,result.stderr+result.stdout)
        self.assertIn('asset-load',result.stdout)

    def test_shared_render_gate_contrast_clipping_and_sideways_scroll(self):
        path=self.root/'gate.html';head='<!doctype html><html><style>body{margin:0;padding:16px;color:#111;background:white;font-family:Arial}</style>'
        def gate(body,viewport='800x600'):
            path.write_text(head+body+'</html>')
            result=subprocess.run(['node',str(ROOT/'skills/shared/scripts/render-gate.js'),str(path),'--viewports',viewport,'--json'],capture_output=True,text=True)
            self.assertIn(result.returncode,(0,1),result.stderr);return json.loads(result.stdout)
        checks=lambda report:[p['check'] for p in report['problems']]
        mixed='<div style="background:color-mix(in srgb,#fff 90%,#eee);padding:8px"><p{}>Text on a mixed fill</p></div>'
        self.assertEqual(checks(gate(mixed.format(''))),[])
        self.assertEqual(checks(gate(mixed.format(' style="color:#fafafa"'))),['low-contrast'])
        unknown=gate('<div style="background:oklch(0.97 0.01 250);padding:8px"><p style="color:#fafafa">Unknown fill</p></div>')
        self.assertEqual((checks(unknown),unknown['contrastSkipped']),([],1))
        for fill in ('#000','#f00','#ffcc00'):
            band='<div style="background:%s;padding:8px"><p style="color:{}">Text on an opaque fill with no blue</p></div>'%fill
            self.assertEqual(checks(gate(band.format('#fff'))),[] if fill!='#ffcc00' else ['low-contrast'])
        self.assertEqual(checks(gate('<div style="background:#000;padding:8px"><p style="color:#222">Dark on black</p></div>')),['low-contrast'])
        self.assertEqual(checks(gate('<div style="background:rgba(0,0,0,0.1);padding:8px"><p style="color:#fff">White on a faint tint over white</p></div>')),['low-contrast'])
        self.assertIn('clipped-text',checks(gate('<p style="white-space:nowrap;overflow:hidden;text-overflow:ellipsis;width:120px">A single line that is much too long for its box</p>')))
        deliberate='<div style="max-height:0;overflow:hidden"><p>Collapsed body</p></div><div style="width:200px;overflow:hidden"><div style="display:flex;width:600px"><p style="width:200px;flex:none">One</p><p style="width:200px;flex:none">Two</p></div></div><div style="overflow-x:auto;width:200px"><p style="white-space:nowrap">A wide row that scrolls inside its own container</p></div>'
        self.assertEqual(checks(gate(deliberate,'375x812')),[])
        self.assertIn('page-scroll-x',checks(gate('<div style="width:600px"><p>Fixed wide block</p></div>','375x812')))
        entrance='<style>@keyframes in{from{transform:translateX(60px);opacity:0}}@keyframes spin{to{transform:rotate(1turn)}}</style><p style="animation:in 20s ease both">A headline that slides in from the right</p><i style="display:block;width:8px;height:8px;animation:spin 3s linear infinite"></i>'
        self.assertEqual(checks(gate(entrance,'375x812')),[])

    def test_renderer_blocks_fit_and_og_capture_size(self):
        kit=self.root/'kit';kit.mkdir()
        tokens={'--brand-bg':'#fff','--brand-ink':'#111','--brand-primary':'#124c80','--brand-font-heading':'Arial','--brand-font-body':'Arial','--brand-muted':'#555','--brand-border':'#ddd','--brand-on-dark':'#fff','--brand-band':'#123','--brand-doc-width':'880px'}
        (kit/'manifest.json').write_text(json.dumps({'render':{'tokens':tokens,'hasDarkBand':False,'heroVisual':'none'}}))
        cta={'label':'Learn more','href':'https://example.com'}
        blocks=[{'type':'hero','title':'A clear headline','lead':'A useful explanation.','cta':cta},
                {'type':'stats','items':[{'n':'12','l':'Example units'}]}, {'type':'about','body':'About this example.'},
                {'type':'quote','text':'An illustrative quotation.'},{'type':'section','heading':'Details','paras':['Some details.']},
                {'type':'features','items':[{'title':'Feature','text':'Description'}]}, {'type':'comparison','rows':[['Before','After']]},
                {'type':'checklist','items':['One item']},{'type':'split','heading':'Split','paras':['Supporting text'],'cta':cta},
                {'type':'logos','items':[{'text':'Example'}]}, {'type':'pricing','plans':[{'name':'Example plan','cta':cta}]},
                {'type':'cta','heading':'Continue','cta':cta},{'type':'footer','links':[cta]}]
        spec=self.root/'spec.json';spec.write_text(json.dumps({'title':'Fixture','blocks':blocks}));out=self.root/'output.html'
        subprocess.run([sys.executable,str(ROOT/'skills/get-brand-components/scripts/render_kit.py'),'--kit-dir',str(kit),'--spec',str(spec),'--out',str(out)],check=True,capture_output=True)
        for width in (375,768,1440):
            self.page.set_viewport_size({'width':width,'height':900});self.page.goto(out.as_uri())
            self.assertLessEqual(self.page.evaluate('document.documentElement.scrollWidth'),width+1)
            self.assertEqual(self.page.locator('a:not([href])').count(),0)
        shot=self.root/'nested/og.png'
        subprocess.run([sys.executable,str(ROOT/'skills/get-brand-components/scripts/render.py'),'--file',str(out),'--out',str(shot),'--width','1200','--height','630','--scale','1','--no-full-page','--wait','0'],check=True,capture_output=True)
        from PIL import Image
        with Image.open(shot) as im:self.assertEqual(im.size,(1200,630))


if __name__=='__main__':unittest.main()
