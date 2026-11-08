import hashlib
import io
import json
import subprocess
import sys
import tempfile
import unittest
from email.message import Message
from pathlib import Path
from urllib.error import HTTPError
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import wis_pipeline as p
import wis_indexer as wi

FIX = Path(__file__).resolve().parent / 'fixtures'
TD = 'https://saabwisonline.com/9-5-9600/2008/2-engine/cooling-system/technical-data/'
TORQUE = TD + 'tightening-torques'
TOOL_DIR = Path(__file__).resolve().parents[1]


class Resp:
    def __init__(self, url, body, mime='text/html'):
        self.url, self.body, self.headers = url, body.encode('utf-8'), {'Content-Type': mime}
    def read(self, n): return self.body[:n]
    def __enter__(self): return self
    def __exit__(self, *a): pass


def err(url, code, loc=None):
    h = Message()
    if loc: h['Location'] = loc
    return HTTPError(url, code, 'x', h, io.BytesIO(b''))


SUB_LISTING = '<h1>Example folder</h1><p>\U0001F4C4 <a href="prose">Prose</a></p>'
PROSE = '<html><head><title>Prose</title></head><body><div id="content"><h1>Description</h1><p>Warning: hot coolant.</p><p>Fault P0128 is set.</p><img src="/images/x.gif"></div></body></html>'


class Site:
    def __init__(self, robots='User-agent: *\nAllow: /\n', interrupt_after=None):
        self.calls, self.robots, self.interrupt_after = [], robots, interrupt_after
        self.pages = {
            TD: (FIX / 'wis_real_listing_excerpt.html').read_text(encoding='utf-8'),
            TORQUE: (FIX / 'wis_real_tightening_torques_excerpt.html').read_text(encoding='utf-8'),
            TD + 'sub-folder/': SUB_LISTING, TD + 'sub-folder/prose': PROSE,
        }
    def open(self, request, timeout=15):
        url = request.full_url
        self.calls.append(url)
        if url.endswith('/robots.txt'): return Resp(url, self.robots, 'text/plain')
        if self.interrupt_after is not None and len([c for c in self.calls if not c.endswith('robots.txt')]) > self.interrupt_after:
            raise KeyboardInterrupt
        if url == TD + 'coolant': raise err(url, 302, TD)                       # soft 404
        if url == TD + 'sub-folder': raise err(url, 301, TD + 'sub-folder/')    # directory redirect
        if url in self.pages: return Resp(url, self.pages[url])
        raise err(url, 404)


def repo_with_dataset(root, facts=None):
    d = Path(root) / 'data' / 'datasets'
    d.mkdir(parents=True)
    path = d / 'x.json'
    path.write_text(json.dumps({'sources': [{'id': 'src-t', 'url': TORQUE, 'title': 't'}], 'facts': facts or [], 'issues': [], 'parts': [], 'gaps': []}))
    return path


class PipelineTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name) / 'repo'
        self.dataset = repo_with_dataset(self.root, [
            {'id': 'f-pump', 'subject': 'pump:9-5', 'predicate': 'torque', 'value': 22, 'unit': 'Nm', 'locator': 'Coolant pump, 4-cyl.', 'source_ids': ['src-t'], 'applicability': {}},
            {'id': 'f-fan', 'subject': 'fan:9-5', 'predicate': 'torque', 'value': {'nominal': 9}, 'unit': None, 'locator': 'Radiator fan', 'source_ids': ['src-t'], 'applicability': {}}])
        self.state = Path(self.tmp.name) / 'state'
    def tearDown(self): self.tmp.cleanup()

    def collect(self, site=None, **kw):
        site = site or Site()
        cp = p.collect(TD, self.state, self.root, delay=2, opener=site, sleep=lambda s: None, **kw)
        return cp, site

    def test_end_to_end_report_counts_are_measured_and_coverage_not_claimed(self):
        cp, site = self.collect()
        report, outs = p.finalize(self.state, self.root)
        m = report['measured']
        self.assertEqual(cp['status'], 'complete')
        self.assertEqual(m['documents_retrieved'], 2)            # torque + prose; listing pages excluded
        self.assertEqual(m['listing_pages_retrieved'], 2)
        self.assertEqual(m['candidate_specifications_extracted'], 5)
        self.assertEqual(m['existing_source_matches_candidates'], 5)
        self.assertEqual(m['potential_duplicate_facts'], 1)       # pump 22 Nm
        self.assertEqual(m['potential_contradictions']['against_existing_facts'], 1)   # fan 9 vs 8
        self.assertEqual(m['documents_parsed'], 2)
        self.assertEqual([x['status'] for x in m['missing_or_inaccessible_pages']], ['soft_404_redirect'])
        self.assertFalse(report['coverage_claim']['claimed'])
        self.assertFalse(report['inventory']['independent_inventory'])
        self.assertEqual(report['estimated'], {})
        prose = next(d for d in report['documents'] if d['url'].endswith('prose'))
        self.assertEqual((prose['structure'], prose['warning_paragraphs'], prose['dtc_codes_seen']), ('prose_or_diagram_no_tables', 1, ['P0128']))

    def test_soft_404_parent_listing_not_requested_twice(self):
        cp, site = self.collect()
        calls = [c for c in site.calls if not c.endswith('robots.txt')]
        self.assertEqual(calls.count(TD), 1)
        self.assertEqual(len(calls), len(set(calls)))   # nothing requested twice, incl. the soft-404's parent
        self.assertIn(TD + 'sub-folder', calls)

    def test_existing_datasets_are_never_modified(self):
        before = hashlib.sha256(self.dataset.read_bytes()).hexdigest()
        self.collect(); p.finalize(self.state, self.root)
        self.assertEqual(hashlib.sha256(self.dataset.read_bytes()).hexdigest(), before)
        self.assertEqual([x.name for x in (self.root / 'data' / 'datasets').iterdir()], ['x.json'])

    def test_second_run_refuses_to_overwrite_and_outputs_not_replaced(self):
        self.collect(); p.finalize(self.state, self.root, run_name='a')
        with self.assertRaises(FileExistsError): self.collect()
        with self.assertRaises(FileExistsError): p.finalize(self.state, self.root, run_name='a')

    def test_interrupt_then_resume_completes_without_refetching(self):
        site = Site(interrupt_after=2)
        with self.assertRaises(KeyboardInterrupt): self.collect(site)
        cp = json.loads((self.state / 'checkpoint.json').read_text())
        self.assertEqual(cp['status'], 'interrupted')
        done = [r['requested_url'] for r in cp['records']]
        self.assertEqual(len(done), 2)
        cp2, site2 = self.collect(Site(), resume=True)
        self.assertEqual(cp2['status'], 'complete')
        refetched = [c for c in site2.calls if c in done]
        self.assertEqual(refetched, [])
        self.assertEqual(len({r['requested_url'] for r in cp2['records']}), len(cp2['records']))

    def test_resume_with_different_scope_rejected(self):
        self.collect()
        with self.assertRaises(ValueError):
            p.collect(TD + 'sub-folder/', self.state, self.root, delay=2, opener=Site(), sleep=lambda s: None, resume=True)

    def test_bounded_stop_reports_remaining_queue_and_unfetched(self):
        cp, _ = self.collect(max_pages=2)
        self.assertEqual(cp['status'], 'bounded_stop')
        report, _ = p.finalize(self.state, self.root)
        self.assertGreater(report['inventory']['queue_remaining'], 0)
        self.assertTrue(report['inventory']['discovered_but_not_fetched'])

    def test_robots_disallow_fails_closed_before_any_page_request(self):
        site = Site('User-agent: *\nDisallow: /\n')
        with self.assertRaises(PermissionError): self.collect(site)
        self.assertEqual(len(site.calls), 1)

    def test_state_dir_inside_datasets_refused(self):
        with self.assertRaises(ValueError):
            p.collect(TD, self.root / 'data' / 'out', self.root, delay=2, opener=Site(), sleep=lambda s: None)
        self.assertFalse((self.root / 'data' / 'out').exists())

    def test_subtree_excludes_sibling_system_such_as_diesel_cooling(self):
        site = Site()
        site.pages[TD] += '<p>\U0001F4C1 <a href="/9-5-9600/2008/2-engine/cooling-system-diesel/technical-data/">Diesel</a></p>'
        cp, site = self.collect(site)
        self.assertFalse(any('cooling-system-diesel' in c for c in site.calls))

    def test_repeat_analysis_is_deterministic(self):
        self.collect()
        a = p.analyse(self.state, self.root)
        b = p.analyse(self.state, self.root)
        self.assertEqual(json.dumps(a, sort_keys=True), json.dumps(b, sort_keys=True))

    def test_cli_dry_run_makes_no_network_calls_and_writes_nothing(self):
        out = Path(self.tmp.name) / 'dry'
        r = subprocess.run([sys.executable, str(TOOL_DIR / 'wis_pipeline.py'), '--dry-run', '--state-dir', str(out),
                            '--repo-root', str(self.root)], capture_output=True, text=True, cwd=TOOL_DIR)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertTrue(json.loads(r.stdout)['dry_run'])
        self.assertFalse(out.exists())

    def test_cli_rejects_unsafe_state_dir(self):
        r = subprocess.run([sys.executable, str(TOOL_DIR / 'wis_pipeline.py'), '--dry-run', '--state-dir',
                            str(self.root / 'data' / 'datasets' / 'x'), '--repo-root', str(self.root)],
                           capture_output=True, text=True, cwd=TOOL_DIR)
        self.assertNotEqual(r.returncode, 0)

    def test_scope_validation(self):
        with self.assertRaises(ValueError): p.collect('https://evil.example/9-5-9600/2008/x/', self.state, self.root)
        with self.assertRaises(ValueError): p.collect(TD, self.state, self.root, delay=0)
        with self.assertRaises(ValueError): p.collect(TD, self.state, self.root, max_pages=0)


if __name__ == '__main__':
    unittest.main()
