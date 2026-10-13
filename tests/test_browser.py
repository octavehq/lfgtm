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

    def test_deck_navigation_edit_export_mobile(self):
        script=(ROOT/'skills/deck/assets/presentation.js').read_text()
        css='@media(min-width:721px){.slide{display:none}.slide.active{display:block}}'
        path=self.root/'deck.html';path.write_text(f'''<!doctype html><html data-content-version="fixture-1"><style>{css}</style><div id="deckStage"><section class="slide"><p data-editable>First</p></section><section class="slide"><p>Second</p></section></div><div id="deckControls"></div><button id="editToggle">Edit</button><button data-export-html>Export</button><script>{script}</script></html>''')
        self.page.goto(path.as_uri());self.page.get_by_text('Next',exact=True).click()
        self.assertEqual(self.page.locator('.slide.active').inner_text(),'Second')
        self.page.get_by_text('Previous',exact=True).click();self.page.get_by_text('Edit',exact=True).click()
        self.page.locator('[data-editable]').fill('Revised')
        with self.page.expect_download() as info:self.page.get_by_text('Export',exact=True).click()
        export=self.root/'export.html';info.value.save_as(export)
        self.assertIn('Revised',export.read_text())
        self.page.goto(export.as_uri());self.assertEqual(self.page.locator('[contenteditable]').count(),0)
        self.page.get_by_text('Next',exact=True).click()
        self.assertEqual(self.page.locator('.slide.active').inner_text(),'Second')
        self.page.set_viewport_size({'width':375,'height':812})
        self.page.wait_for_function('document.querySelectorAll(\'.slide[aria-hidden="false"]\').length === 2')
        self.assertEqual(self.page.locator('.slide[aria-hidden="false"]').count(),2)

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
