"""Fetch hardening: redirects, soft 404, retry/backoff, duplicates, output safety."""
import io
import sys
import tempfile
import unittest
from email.message import Message
from pathlib import Path
from urllib.error import HTTPError, URLError
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import wis_indexer as w

ROOT = 'https://saabwisonline.com'
SCOPE = '/9-5-9600/2008/'
DIR = ROOT + '/9-5-9600/2008/2-engine/cooling-system/technical-data'


class Resp:
    def __init__(self, url, body='<h1>x</h1>', mime='text/html'):
        self.url, self.body, self.headers = url, body.encode(), {'Content-Type': mime}
    def read(self, n): return self.body[:n]
    def __enter__(self): return self
    def __exit__(self, *a): pass


def http_error(url, code, location=None, retry_after=None):
    h = Message()
    if location: h['Location'] = location
    if retry_after: h['Retry-After'] = retry_after
    return HTTPError(url, code, 'x', h, io.BytesIO(b''))


class Script:
    """Opener returning scripted outcomes per URL (list of Resp/Exception)."""
    def __init__(self, plan, robots='User-agent: *\nAllow: /\n'):
        self.plan, self.calls, self.robots = {k: list(v) for k, v in plan.items()}, [], robots
    def open(self, request, timeout=15):
        url = request.full_url
        self.calls.append(url)
        if url.endswith('/robots.txt'): return Resp(url, self.robots, 'text/plain')
        step = self.plan[url].pop(0) if len(self.plan[url]) > 1 else self.plan[url][0]
        if isinstance(step, Exception): raise step
        return step


class FetchDocument(unittest.TestCase):
    def fetch(self, plan, url, **kw):
        sleeps = []
        op = Script(plan)
        r = w.fetch_document(op, url, SCOPE, sleep=sleeps.append, delay=2, **kw)
        return r, op, sleeps

    def test_directory_redirect_is_followed_and_recorded(self):
        r, op, _ = self.fetch({DIR: [http_error(DIR, 301, DIR + '/')], DIR + '/': [Resp(DIR + '/')]}, DIR)
        self.assertEqual(r['status'], 'ok')
        self.assertEqual(r['final_url'], DIR + '/')
        self.assertEqual(r['redirect_chain'], [{'from': DIR, 'to': DIR + '/', 'code': 301}])

    def test_soft_404_redirect_to_parent_is_not_a_page(self):
        missing = DIR + '/nope'
        r, op, _ = self.fetch({missing: [http_error(missing, 302, DIR + '/')]}, missing)
        self.assertEqual(r['status'], 'soft_404_redirect')
        self.assertIsNone(r.get('raw'))
        self.assertEqual(op.calls, [missing])  # the parent page was not requested

    def test_off_origin_redirect_is_never_requested(self):
        u = DIR + '/x'
        r, op, _ = self.fetch({u: [http_error(u, 301, 'https://evil.example/x')]}, u)
        self.assertEqual(r['status'], 'redirect_out_of_scope')
        self.assertEqual(op.calls, [u])

    def test_other_model_year_redirect_rejected(self):
        u = DIR + '/x'
        r, op, _ = self.fetch({u: [http_error(u, 302, ROOT + '/9-5-9600/2009/x')]}, u)
        self.assertEqual(r['status'], 'redirect_out_of_scope')

    def test_redirect_loop_detected(self):
        a, b = DIR + '/a', DIR + '/b'
        r, _, _ = self.fetch({a: [http_error(a, 301, b)], b: [http_error(b, 301, a)]}, a)
        self.assertEqual(r['status'], 'redirect_loop')

    def test_404_is_missing_not_error(self):
        u = DIR + '/gone'
        r, op, sleeps = self.fetch({u: [http_error(u, 404)]}, u)
        self.assertEqual(r['status'], 'missing')
        self.assertEqual(len(op.calls), 1)

    def test_429_backoff_honours_retry_after_then_succeeds(self):
        u = DIR + '/doc'
        r, op, sleeps = self.fetch({u: [http_error(u, 429, retry_after='7'), Resp(u)]}, u)
        self.assertEqual(r['status'], 'ok')
        self.assertEqual(r['attempts'], 2)
        self.assertEqual(sleeps, [7])

    def test_5xx_exponential_backoff_and_final_failure_recorded(self):
        u = DIR + '/doc'
        r, op, sleeps = self.fetch({u: [http_error(u, 503)]}, u, max_retries=2)
        self.assertEqual(r['status'], 'error')
        self.assertEqual(r['error_type'], 'http_503')
        self.assertEqual(sleeps, [2, 4])
        self.assertEqual(r['attempts'], 3)

    def test_timeout_is_retried(self):
        u = DIR + '/doc'
        r, _, sleeps = self.fetch({u: [URLError('timed out'), Resp(u)]}, u)
        self.assertEqual(r['status'], 'ok')

    def test_non_html_skipped_with_explicit_status(self):
        u = DIR + '/img'
        r, _, _ = self.fetch({u: [Resp(u, 'x', 'image/png')]}, u)
        self.assertEqual(r['status'], 'non_text_skipped')

    def test_oversize_page_rejected(self):
        u = DIR + '/big'
        r, _, _ = self.fetch({u: [Resp(u, 'x' * (w.MAX_HTML + 5))]}, u)
        self.assertEqual(r['status'], 'error')
        self.assertEqual(r['error_type'], 'too_large')


class CanonicalUrl(unittest.TestCase):
    def test_dedupe_key_ignores_trailing_slash_only(self):
        self.assertEqual(w.dedupe_key(DIR), w.dedupe_key(DIR + '/'))
        self.assertNotEqual(w.dedupe_key(DIR + '/a'), w.dedupe_key(DIR + '/b'))

    def test_encoded_slash_and_backslash_rejected(self):
        self.assertIsNone(w.canonical_url(DIR + '/a%2Fb'))
        self.assertIsNone(w.canonical_url(DIR + '/a%5Cb'))
        self.assertIsNone(w.canonical_url(DIR + '/%2e%2e/x'))
        self.assertIsNone(w.canonical_url(DIR + '/a%00b'))

    def test_userinfo_port_scheme_rejected(self):
        for u in ('https://user@saabwisonline.com/x', 'https://saabwisonline.com:8443/x', 'http://saabwisonline.com/x'):
            self.assertIsNone(w.canonical_url(u))

    def test_query_and_fragment_dropped(self):
        self.assertEqual(w.canonical_url(DIR + '/a?x=1#f'), DIR + '/a')


class IndexDuplicates(unittest.TestCase):
    def test_duplicate_content_and_slash_variant_not_double_counted(self):
        listing = ('<h1>L</h1><p>\U0001F4C4 <a href="a">A</a></p><p>\U0001F4C4 <a href="a/">A2</a></p>'
                   '<p>\U0001F4C4 <a href="b">B</a></p>')
        d = DIR + '/'
        plan = {d: [Resp(d, listing)], d + 'a': [Resp(d + 'a', '<h1>same</h1>')],
                d + 'b': [Resp(d + 'b', '<h1>same</h1>')]}
        res = w.index(d, max_pages=10, opener=Script(plan), sleep=lambda s: None)
        statuses = {r['url']: r['status'] for r in res['records']}
        self.assertEqual(len(res['records']), 3)
        self.assertEqual(statuses[d + 'b'], 'indexed_duplicate_content')
        self.assertEqual([r for r in res['records'] if r['url'] == d + 'b'][0]['duplicate_of'], d + 'a')

    def test_index_records_soft_404_without_indexing_parent(self):
        d = DIR + '/'
        plan = {d: [Resp(d, '<p>\U0001F4C4 <a href="gone">G</a></p>')], d + 'gone': [http_error(d + 'gone', 302, d)]}
        res = w.index(d, max_pages=10, opener=Script(plan), sleep=lambda s: None)
        rec = [r for r in res['records'] if r['url'].endswith('gone')][0]
        self.assertEqual(rec['status'], 'soft_404_redirect')


class OutputSafety(unittest.TestCase):
    def test_write_manifest_refuses_overwrite(self):
        with tempfile.TemporaryDirectory() as t:
            p = Path(t) / 'm.json'
            p.write_text('keep')
            with self.assertRaises(FileExistsError):
                w.write_manifest(p, {'a': 1})
            self.assertEqual(p.read_text(), 'keep')

    def test_unsafe_output_dir_inside_datasets_rejected(self):
        with tempfile.TemporaryDirectory() as t:
            (Path(t) / 'data' / 'datasets').mkdir(parents=True)
            with self.assertRaises(ValueError):
                w.safe_output_path(Path(t) / 'data' / 'datasets' / 'x.json', repo_root=Path(t))
            with self.assertRaises(ValueError):
                w.safe_output_path(Path(t) / 'data' / 'evil' / '..' / 'datasets' / 'x.json', repo_root=Path(t))
            self.assertEqual(w.safe_output_path(Path(t) / 'out' / 'x.json', repo_root=Path(t)), (Path(t) / 'out' / 'x.json').resolve())


if __name__ == '__main__':
    unittest.main()
