"""Public changelog render and publish checks. Synthetic data, no service calls."""
import importlib.util
import io
import json
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('changelog', ROOT/'skills/public-changelog/scripts/changelog.py')
cl = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cl)

PAGE = {'title': 'Acme Changelog', 'dek': 'What we shipped, and what it means for Acme teams.',
        'footer': 'Acme, pipeline that plans itself.'}


def paragraph(name):
    return (f'{name} lets a rep plan the next step of a deal from what the buyer said on the last call, '
            'instead of rebuilding the account story by hand. It reads the call, matches the stated pain to a '
            'playbook, and drafts the follow-up against it. Reps stop starting from a blank page.')


def entry(entry_id, date, title, **extra):
    return {'id': entry_id, 'date': date, 'title': title, 'body': paragraph(title), 'availability': 'ga', **extra}


def state(*entries):
    return {'schemaVersion': 1, 'page': dict(PAGE),
            'entries': [{k: v for k, v in e.items() if k != 'availability'} | {'publishedAt': '2026-08-01'} for e in entries]}


class PublicChangelogTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, name, value):
        path = self.dir/name
        path.write_text(value if isinstance(value, str) else json.dumps(value), encoding='utf-8')
        return str(path)

    def add(self, current_state, entries, html=None, **flags):
        argv = ['add', '--state', self.write('state.json', current_state),
                '--entries', self.write('new.json', {'entries': entries}),
                '--out', str(self.dir/'bundle'), '--published-at', '2026-09-23']
        if html is not None:
            argv += ['--html', self.write('live.html', html)]
        for key, value in flags.items():
            argv += [f'--{key.replace("_", "-")}', value]
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = cl.main(argv)
        return code, out.getvalue() + err.getvalue()

    def test_page_lines_match_the_rendered_line_set(self):
        s = state(entry('a', '2026-08-20', 'Deal Plans'), entry('b', '2026-07-02', 'Call Notes'))
        html = cl.render_html(s, cl.build_style())
        self.assertEqual(cl.page_lines(html), cl.render_lines(s))
        self.assertEqual(cl.render_lines(s)[:4], ['# Acme Changelog', PAGE['dek'], '## August 2026', '### 2026-08-20 — Deal Plans'])

    def test_bootstrap_reproduces_a_page_byte_for_byte(self):
        s = state(entry('a', '2026-08-20', 'Deal Plans & <Notes>'), entry('b', '2026-08-20', 'Call Notes'),
                  entry('c', '2026-07-02', 'Win Rooms'))
        html = cl.render_html(s, cl.build_style())
        rebuilt = cl.state_from_page(html)
        self.assertEqual([e['title'] for e in rebuilt['entries']], ['Deal Plans & <Notes>', 'Call Notes', 'Win Rooms'])
        self.assertEqual(cl.render_html(rebuilt, cl.style_of(html)), html)

    def test_bootstrap_refuses_a_page_it_does_not_recognise(self):
        with self.assertRaises(cl.Refused):
            cl.state_from_page('<h1>Changelog</h1><p>dek</p><p>stray paragraph</p><p>more</p><footer><div>f</div></footer>')

    def test_add_keeps_every_live_line_and_carries_the_style_over(self):
        s = state(entry('a', '2026-08-20', 'Deal Plans'))
        live = cl.render_html(s, 'body{color:red}')
        code, output = self.add(s, [entry('n', '2026-09-20', 'Pipeline Watch')], html=live)
        self.assertEqual(code, 0, output)
        html = (self.dir/'bundle/index.html').read_text()
        self.assertIn('<style>body{color:red}</style>', html)
        self.assertTrue(set(cl.page_lines(live)) <= set(cl.page_lines(html)))
        written = json.loads((self.dir/'bundle/changelog.json').read_text())
        self.assertEqual(written['entries'][0], {'id': 'n', 'date': '2026-09-20', 'title': 'Pipeline Watch',
                                                 'body': paragraph('Pipeline Watch'), 'publishedAt': '2026-09-23'})
        self.assertEqual(json.loads((self.dir/'bundle.manifest.json').read_text()), ['index.html', 'changelog.json'])

    def test_a_live_line_that_would_change_refuses_the_publish(self):
        s = state(entry('a', '2026-08-20', 'Deal Plans'))
        live = cl.render_html(s, cl.build_style())
        s['entries'][0]['body'] = paragraph('Deal Plans').replace('blank page', 'empty page')
        code, output = self.add(s, [entry('n', '2026-09-20', 'Pipeline Watch')], html=live)
        self.assertEqual(code, 1)
        self.assertIn('✗ history', output)
        self.assertFalse((self.dir/'bundle').exists())

    def test_rewording_a_live_entry_is_refused_and_an_identical_one_is_skipped(self):
        s = state(entry('a', '2026-08-20', 'Deal Plans'))
        live = cl.render_html(s, cl.build_style())
        reworded = entry('a', '2026-08-20', 'Deal Plans')
        reworded['body'] = reworded['body'].replace('rep', 'seller')
        code, output = self.add(s, [reworded], html=live)
        self.assertEqual(code, 1)
        self.assertIn('already live with different text', output)
        code, output = self.add(s, [entry('a', '2026-08-20', 'Deal Plans')], html=live)
        self.assertEqual(code, 0)
        self.assertIn('Nothing new to publish', output)

    def test_only_generally_available_single_paragraph_entries_enter(self):
        s = state()
        cases = [
            (entry('n', '2026-09-20', 'Gated', availability='beta'), 'generally available'),
            ({**entry('n', '2026-09-20', 'Short'), 'body': 'Too short.'}, 'character paragraph'),
            ({**entry('n', '2026-09-20', 'Split'), 'body': paragraph('Split') + '\nSecond line.'}, 'line break'),
            ({**entry('n', '2026-09-20', 'Bullet'), 'body': '- ' + paragraph('Bullet')}, 'markdown character'),
            (entry('n', '2026-02-30', 'Bad date'), 'valid date'),
        ]
        for raw, message in cases:
            with self.subTest(message=message):
                code, output = self.add(s, [raw])
                self.assertEqual(code, 1)
                self.assertIn(message, output)

    def test_one_bad_entry_refuses_the_whole_batch(self):
        code, output = self.add(state(), [entry('ok', '2026-09-20', 'Fine'), entry('bad', '2026-09-20', 'Gated', availability='gated')])
        self.assertEqual(code, 1)
        self.assertFalse((self.dir/'bundle').exists())

    def test_a_duplicate_line_is_refused(self):
        twin = entry('twin', '2026-09-20', 'Deal Plans')
        code, output = self.add(state(entry('a', '2026-09-20', 'Deal Plans')), [twin])
        self.assertEqual(code, 1)
        self.assertIn('✗ line-uniqueness', output)

    def test_page_safety_refuses_links_scripts_and_external_fetches(self):
        s = state(entry('a', '2026-08-20', 'Deal Plans'))
        for style, label in [('@import url(https://fonts.example/x.css);', 'external fetch'),
                             ('.x{background:url(https://cdn.example/logo.png)}', 'external fetch'),
                             ('</style><script>1</script><style>', '<script>'),
                             ('</style><a href="/pricing">x</a><style>', 'a link')]:
            with self.subTest(label=label):
                checks, _, _ = cl.run_checks([], s, style)
                safety = next(c for c in checks if c['name'] == 'page-safety')
                self.assertFalse(safety['ok'])
                self.assertIn(label, safety['detail'])

    def test_a_new_page_is_self_contained_with_an_inlined_logo(self):
        logo = self.dir/'logo.png'
        logo.write_bytes(b'\x89PNG\r\n\x1a\nfake')
        code, output = self.add(state(), [entry('n', '2026-09-20', 'Pipeline Watch')],
                                tokens=self.write('tokens.css', ':root{--brand-primary:#123456}'), logo_light=str(logo))
        self.assertEqual(code, 0, output)
        html = (self.dir/'bundle/index.html').read_text()
        self.assertIn('--brand-primary:#123456', html)
        self.assertIn('--cl-logo-light: url(data:image/png;base64,', html)

    def test_lines_confirms_a_page_against_its_state(self):
        s = state(entry('a', '2026-08-20', 'Deal Plans'))
        html = self.write('page.html', cl.render_html(s, cl.build_style()))
        with redirect_stdout(io.StringIO()):
            self.assertEqual(cl.main(['lines', '--html', html, '--expect-state', self.write('s.json', s)]), 0)
            s['entries'][0]['title'] = 'Other'
            self.assertEqual(cl.main(['lines', '--html', html, '--expect-state', self.write('s.json', s)]), 1)


if __name__ == '__main__':
    unittest.main()
