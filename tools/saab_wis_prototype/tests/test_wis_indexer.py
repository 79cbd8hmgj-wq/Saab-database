import sys
import unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import wis_indexer as w

ROOT = "https://saabwisonline.com/9-5-9600/2008/"
INDEX = ROOT + "2-engine/basic-engine-4-cylinder-petrol/technical-data/"
DOC = INDEX + "general-data"
SAMPLE = '<html><head><title>Technical data</title></head><body><h1>Technical data</h1><a href="general-data">General data</a><a href="https://evil.com/x">External</a><a href="/9-5-9600/2009/x">Other year</a><table><tr><td>90</td></tr></table></body></html>'

class FakeResponse:
    def __init__(self, url, content, mime="text/html"):
        self.url, self.content, self.headers = url, content.encode(), {"Content-Type": mime}
    def read(self, amount): return self.content[:amount]
    def __enter__(self): return self
    def __exit__(self, *args): pass

class FakeOpener:
    def __init__(self, robots="User-agent: *\nAllow: /\n"):
        self.robots = robots
        self.calls = []
    def open(self, request, timeout=15):
        url = request.full_url
        self.calls.append(url)
        if url.endswith("robots.txt"):
            return FakeResponse(url, self.robots, "text/plain")
        if url == INDEX: return FakeResponse(url, SAMPLE)
        if url == DOC: return FakeResponse(url, '<h1>General data</h1>')
        raise IOError("unexpected URL")

class IndexerTests(unittest.TestCase):
    def test_parser_links_and_metadata(self):
        d = w.parse_page(SAMPLE, INDEX, "/9-5-9600/2008/")
        self.assertEqual(d["heading"], "Technical data")
        self.assertEqual(d["row_count"], 1)
        self.assertEqual([x["url"] for x in d["child_links"]], [DOC])
    def test_disallow_external_and_traversal(self):
        self.assertIsNone(w.canonical_url("https://evil.com/9-5-9600/2008/"))
        self.assertIsNone(w.canonical_url("http://saabwisonline.com/9-5-9600/2008/"))
        self.assertIsNone(w.canonical_url("https://saabwisonline.com/9-5-9600/2008/../2009/"))
    def test_bounded_crawl(self):
        opener = FakeOpener()
        result = w.index(INDEX, max_pages=2, opener=opener, sleep=lambda x:None)
        self.assertEqual(result["pages_processed"], 2)
        self.assertEqual(result["links_discovered"], 2)
        self.assertTrue(all("body" not in x for x in result["records"]))
        self.assertEqual(opener.calls, [w.ORIGIN + "/robots.txt", INDEX, DOC])
    def test_robots_disallow(self):
        with self.assertRaises(PermissionError):
            w.index(INDEX, opener=FakeOpener("User-agent: *\nDisallow: /\n"))
    def test_network_fail_closed(self):
        class Failed:
            def open(self, *args, **kwargs): raise OSError("no network")
        with self.assertRaises(OSError): w.index(INDEX, opener=Failed())
    def test_limits(self):
        with self.assertRaises(ValueError): w.index(INDEX, max_pages=101)
        with self.assertRaises(ValueError): w.index(INDEX, delay=0)
        with self.assertRaises(ValueError): w.index(w.ORIGIN)

if __name__ == "__main__": unittest.main()
