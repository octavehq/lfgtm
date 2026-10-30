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


def legacy(entry_id, date, title, **extra):
    """A paragraph entry, the shape everything published before fielded entries has."""
    return {'id': entry_id, 'date': date, 'title': title, 'body': paragraph(title), 'availability': 'ga', **extra}


def entry(entry_id, date, title, **extra):
    """A fielded entry, the shape every new entry takes."""
    return {'id': entry_id, 'date': date, 'title': title, 'novelty': 'net-new', 'availability': 'ga',
            'description': f'{title} plans the next step of a deal from what the buyer said on the last call. '
                           'It reads the call, matches the stated pain to a playbook and drafts the follow-up.',
            'useCase': f'An AE can now close a {title} call with the follow-up already drafted.',
            'problem': f'Reps rebuilt the account story by hand after every {title} call.', **extra}


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
        s = state(legacy('a', '2026-08-20', 'Deal Plans & <Notes>'), legacy('b', '2026-08-20', 'Call Notes'),
                  legacy('c', '2026-07-02', 'Win Rooms'))
        html = cl.render_html(s, cl.build_style())
        rebuilt = cl.state_from_page(html)
        self.assertEqual([e['title'] for e in rebuilt['entries']], ['Deal Plans & <Notes>', 'Call Notes', 'Win Rooms'])
        self.assertEqual(cl.render_html(rebuilt, cl.style_of(html)), html)

    def test_bootstrap_refuses_a_page_it_does_not_recognise(self):
        with self.assertRaises(cl.Refused):
            cl.state_from_page('<h1>Changelog</h1><p>dek</p><p>stray paragraph</p><p>more</p><footer><div>f</div></footer>')

    def test_add_keeps_every_live_line_and_carries_the_style_over(self):
        s = state(legacy('a', '2026-08-20', 'Deal Plans'))
        live = cl.render_html(s, 'body{color:red}')
        code, output = self.add(s, [entry('n', '2026-09-20', 'Pipeline Watch')], html=live)
        self.assertEqual(code, 0, output)
        html = (self.dir/'bundle/index.html').read_text()
        # The live stylesheet is kept, and only gains the fielded-entry rules.
        self.assertIn('<style>body{color:red}\n/* cl-fields */', html)
        self.assertTrue(set(cl.page_lines(live)) <= set(cl.page_lines(html)))
        written = json.loads((self.dir/'bundle/changelog.json').read_text())
        expected = {k: v for k, v in entry('n', '2026-09-20', 'Pipeline Watch').items() if k != 'availability'}
        self.assertEqual(written['entries'][0], {**expected, 'publishedAt': '2026-09-23'})
        self.assertEqual(written['schemaVersion'], 2)
        self.assertEqual(json.loads((self.dir/'bundle.manifest.json').read_text()), ['index.html', 'changelog.json'])

    def test_a_live_line_that_would_change_refuses_the_publish(self):
        s = state(legacy('a', '2026-08-20', 'Deal Plans'))
        live = cl.render_html(s, cl.build_style())
        s['entries'][0]['body'] = paragraph('Deal Plans').replace('blank page', 'empty page')
        code, output = self.add(s, [entry('n', '2026-09-20', 'Pipeline Watch')], html=live)
        self.assertEqual(code, 1)
        self.assertIn('✗ history', output)
        self.assertFalse((self.dir/'bundle').exists())

    def test_rewording_a_live_entry_is_refused_and_an_identical_one_is_skipped(self):
        for make, field in [(legacy, 'body'), (entry, 'problem')]:
            with self.subTest(shape=make.__name__):
                s = state(make('a', '2026-08-20', 'Deal Plans'))
                live = cl.render_html(s, cl.build_style())
                reworded = make('a', '2026-08-20', 'Deal Plans')
                reworded[field] = reworded[field].replace('by hand', 'manually').replace('rep', 'seller')
                code, output = self.add(s, [reworded], html=live)
                self.assertEqual(code, 1)
                self.assertIn('already live with different text', output)
                code, output = self.add(s, [make('a', '2026-08-20', 'Deal Plans')], html=live)
                self.assertEqual(code, 0)
                self.assertIn('Nothing new to publish', output)

    def test_only_generally_available_complete_fielded_entries_enter(self):
        s = state()
        cases = [
            (entry('n', '2026-09-20', 'Gated', availability='beta'), 'generally available'),
            (legacy('n', '2026-09-20', 'Paragraph'), 'is a single paragraph'),
            ({**entry('n', '2026-09-20', 'Empty'), 'useCase': ''}, 'has no useCase'),
            ({**entry('n', '2026-09-20', 'Split'), 'description': 'One line.\nSecond line.'}, 'line break'),
            ({**entry('n', '2026-09-20', 'Bullet'), 'problem': '- a bullet'}, 'markdown character'),
            ({**entry('n', '2026-09-20', 'Unsure'), 'novelty': 'major'}, 'has no novelty'),
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

    def test_a_fielded_entry_reads_as_labeled_lines_and_its_badge_is_not_text(self):
        s = state(entry('a', '2026-08-20', 'Deal Plans'), legacy('b', '2026-07-02', 'Call Notes'))
        html = cl.render_html(s, cl.build_style())
        lines = cl.page_lines(html)
        self.assertEqual(lines, cl.render_lines(s))
        self.assertEqual(lines[3:7], ['### 2026-08-20 — Deal Plans', entry('a', '', 'Deal Plans')['description'],
                                      'Use case: ' + entry('a', '', 'Deal Plans')['useCase'],
                                      'Problem it solves: ' + entry('a', '', 'Deal Plans')['problem']])
        # The badge is drawn by the stylesheet, so two "New" entries never repeat a line.
        self.assertIn('data-novelty="net-new"', html)
        self.assertIn('content: "New"', html)
        self.assertNotIn('New', [line.strip() for line in lines])

    def test_a_version_1_state_is_read_and_written_back_as_version_2(self):
        s = state(legacy('a', '2026-08-20', 'Deal Plans'))
        self.assertEqual(s['schemaVersion'], 1)
        code, output = self.add(s, [entry('n', '2026-09-20', 'Pipeline Watch')], html=cl.render_html(s, cl.build_style()))
        self.assertEqual(code, 0, output)
        self.assertEqual(json.loads((self.dir/'bundle/changelog.json').read_text())['schemaVersion'], 2)

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

    def publish(self, current_state, html, entries=(), reshape=(), remove=()):
        argv = ['add', '--state', self.write('state.json', current_state),
                '--entries', self.write('new.json', {'entries': list(entries), 'reshape': list(reshape), 'remove': list(remove)}),
                '--out', str(self.dir/'bundle'), '--published-at', '2026-10-30', '--html', self.write('live.html', html)]
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = cl.main(argv)
        return code, out.getvalue() + err.getvalue()

    def fields_for(self, entry_id, title):
        fielded = entry(entry_id, '', title)
        return {key: fielded[key] for key in ('id', 'novelty', *cl.TEXT_FIELDS)}

    def test_a_reviewed_reshape_swaps_only_that_paragraph_for_fields(self):
        s = state(legacy('a', '2026-08-20', 'Deal Plans'), legacy('b', '2026-07-02', 'Call Notes'))
        live = cl.render_html(s, 'body{color:red}')
        code, output = self.publish(s, live, reshape=[self.fields_for('a', 'Deal Plans')])
        self.assertEqual(code, 0, output)
        lines = cl.page_lines((self.dir/'bundle/index.html').read_text())
        # The heading stays, the paragraph gives way to the fields, and the other entry is untouched.
        self.assertIn('### 2026-08-20 — Deal Plans', lines)
        self.assertIn('Use case: ' + entry('a', '', 'Deal Plans')['useCase'], lines)
        self.assertEqual(set(cl.page_lines(live)) - set(lines), {paragraph('Deal Plans')})
        written = json.loads((self.dir/'bundle/changelog.json').read_text())
        self.assertEqual(written['entries'][0], {**self.fields_for('a', 'Deal Plans'), 'date': '2026-08-20',
                                                 'title': 'Deal Plans', 'publishedAt': '2026-08-01',
                                                 'reshapedAt': '2026-10-30'})
        self.assertEqual(written['entries'][1]['body'], paragraph('Call Notes'))

    def test_a_removed_entry_leaves_the_page_and_keeps_only_its_id_on_record(self):
        s = state(legacy('a', '2026-08-20', 'Deal Plans'), legacy('b', '2026-07-02', 'Call Notes'))
        live = cl.render_html(s, cl.build_style())
        code, output = self.publish(s, live, remove=['b'])
        self.assertEqual(code, 0, output)
        self.assertIn('removes 3 line(s) and adds none', output)
        lines = cl.page_lines((self.dir/'bundle/index.html').read_text())
        # Its heading, its paragraph and the month heading nothing else sits under all go.
        self.assertEqual(set(cl.page_lines(live)) - set(lines),
                         {'## July 2026', '### 2026-07-02 — Call Notes', paragraph('Call Notes')})
        bundle = (self.dir/'bundle/changelog.json').read_text()
        self.assertNotIn('Call Notes', bundle)
        self.assertEqual(json.loads(bundle)['removed'], [{'id': 'b', 'removedAt': '2026-10-30'}])
        # A removed id cannot come back as a new entry under the same id.
        code, output = self.publish(json.loads(bundle), (self.dir/'bundle/index.html').read_text(),
                                    entries=[entry('b', '2026-10-01', 'Call Notes Again')])
        self.assertEqual(code, 1)
        self.assertIn('was removed from the page', output)

    def test_new_entries_reshapes_and_removals_go_out_in_one_publish(self):
        s = state(legacy('a', '2026-08-20', 'Deal Plans'), legacy('b', '2026-07-02', 'Call Notes'))
        code, output = self.publish(s, cl.render_html(s, cl.build_style()), entries=[entry('n', '2026-10-20', 'Pipeline Watch')],
                                    reshape=[self.fields_for('a', 'Deal Plans')], remove=['b'])
        self.assertEqual(code, 0, output)
        self.assertEqual([e['id'] for e in json.loads((self.dir/'bundle/changelog.json').read_text())['entries']], ['n', 'a'])

    def test_a_reshape_or_removal_of_anything_else_refuses_the_batch(self):
        s = state(legacy('a', '2026-08-20', 'Deal Plans'), entry('f', '2026-07-02', 'Call Notes'))
        live = cl.render_html(s, cl.build_style())
        cases = [
            ({'reshape': [self.fields_for('missing', 'Win Rooms')]}, 'is not live'),
            ({'reshape': [self.fields_for('f', 'Call Notes')]}, 'already fielded'),
            ({'reshape': [{**self.fields_for('a', 'Deal Plans'), 'title': 'Deal Plans 2'}]}, 'keeps the title'),
            ({'reshape': [{**self.fields_for('a', 'Deal Plans'), 'problem': ''}]}, 'has no problem'),
            ({'reshape': [self.fields_for('a', 'Deal Plans')], 'remove': ['a']}, 'both reshaped and removed'),
            ({'remove': ['missing']}, 'is not live'),
        ]
        for parts, message in cases:
            with self.subTest(message=message):
                code, output = self.publish(s, live, **parts)
                self.assertEqual(code, 1)
                self.assertIn(message, output)
                self.assertFalse((self.dir/'bundle').exists())

    def test_a_reshape_still_refuses_a_change_to_any_other_live_line(self):
        s = state(legacy('a', '2026-08-20', 'Deal Plans'), legacy('b', '2026-07-02', 'Call Notes'))
        live = cl.render_html(s, cl.build_style())
        s['entries'][1]['body'] = paragraph('Call Notes').replace('blank page', 'empty page')
        code, output = self.publish(s, live, reshape=[self.fields_for('a', 'Deal Plans')])
        self.assertEqual(code, 1)
        self.assertIn('✗ history', output)

    def test_lines_confirms_a_page_against_its_state(self):
        s = state(entry('a', '2026-08-20', 'Deal Plans'))
        html = self.write('page.html', cl.render_html(s, cl.build_style()))
        with redirect_stdout(io.StringIO()):
            self.assertEqual(cl.main(['lines', '--html', html, '--expect-state', self.write('s.json', s)]), 0)
            s['entries'][0]['title'] = 'Other'
            self.assertEqual(cl.main(['lines', '--html', html, '--expect-state', self.write('s.json', s)]), 1)


if __name__ == '__main__':
    unittest.main()
