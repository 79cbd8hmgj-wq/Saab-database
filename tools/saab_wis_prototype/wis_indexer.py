#!/usr/bin/env python3
"""Conservative, read-only SaabWISOnline navigation indexer.

This tool creates an index of source URLs and page metadata, NOT a mirror of WIS.
Network requests are blocked unless robots.txt can be fetched and permits access.
"""
import argparse
import hashlib
import json
import re
import time
from collections import deque
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlsplit, urlunsplit, unquote
from urllib.request import Request, build_opener
from urllib.robotparser import RobotFileParser

HOST = "saabwisonline.com"
ORIGIN = "https://" + HOST
USER_AGENT = "SaabDatabaseResearchIndexer/0.1 (metadata-only; contact site owner before bulk collection)"
MAX_HTML = 2_000_000


def canonical_url(url):
    s = urlsplit(url)
    if s.scheme != "https" or (s.hostname or "").lower() != HOST or s.username or s.password or s.port:
        return None
    path = re.sub(r"/+", "/", unquote(s.path))
    if ".." in path.split("/") or "\\" in path or any(ord(c) < 32 for c in path):
        return None
    return urlunsplit(("https", HOST, path or "/", "", ""))


def within_scope(url, prefix):
    parsed = canonical_url(url)
    return bool(parsed and (urlsplit(parsed).path == prefix.rstrip("/") or urlsplit(parsed).path.startswith(prefix)))


class MetadataParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title = ""
        self.heading = ""
        self.links = []
        self.tables = 0
        self.rows = 0
        self.images = 0
        self._in_title = False
        self._in_h1 = False
        self._anchor = None
        self._anchor_text = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "title": self._in_title = True
        if tag == "h1": self._in_h1 = True
        if tag == "a":
            self._anchor = attrs.get("href")
            self._anchor_text = []
        if tag == "table": self.tables += 1
        if tag == "tr": self.rows += 1
        if tag in ("img", "svg"): self.images += 1

    def handle_data(self, data):
        if self._in_title: self.title += data
        if self._in_h1: self.heading += data
        if self._anchor is not None: self._anchor_text.append(data)

    def handle_endtag(self, tag):
        if tag == "title": self._in_title = False
        if tag == "h1": self._in_h1 = False
        if tag == "a" and self._anchor is not None:
            self.links.append((self._anchor, " ".join(" ".join(self._anchor_text).split())))
            self._anchor = None
            self._anchor_text = []


def parse_page(html, page_url, prefix):
    parser = MetadataParser()
    parser.feed(html)
    links = {}
    for href, label in parser.links:
        candidate = canonical_url(urljoin(page_url, href))
        if candidate and within_scope(candidate, prefix):
            links.setdefault(candidate, label)
    return {
        "heading": " ".join(parser.heading.split()),
        "page_title": " ".join(parser.title.split()),
        "table_count": parser.tables,
        "row_count": parser.rows,
        "image_count": parser.images,
        "child_links": [{"url": k, "label": v} for k, v in links.items()],
    }


def fetch(opener, url):
    req = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "text/html, text/plain;q=0.7"})
    with opener.open(req, timeout=15) as response:
        actual = canonical_url(response.url)
        if actual is None:
            raise ValueError("Redirect left authorized origin")
        content_type = response.headers.get("Content-Type", "").lower()
        if "text/html" not in content_type and "text/plain" not in content_type:
            raise ValueError("Non-text response skipped")
        raw = response.read(MAX_HTML + 1)
        if len(raw) > MAX_HTML: raise ValueError("Page exceeds configured size limit")
        return raw, actual, content_type


def robots_policy(opener):
    robots_url = ORIGIN + "/robots.txt"
    raw, _, _ = fetch(opener, robots_url)
    rp = RobotFileParser()
    rp.parse(raw.decode("utf-8", errors="replace").splitlines())
    return rp


def index(start_url, max_pages=10, delay=3.0, opener=None, sleep=time.sleep):
    if max_pages < 1 or max_pages > 100: raise ValueError("max_pages must be within 1..100")
    if delay < 2: raise ValueError("delay must be >= 2 seconds")
    start = canonical_url(start_url)
    if not start: raise ValueError("Start URL must use official HTTPS host")
    parts = urlsplit(start).path.strip("/").split("/")
    if len(parts) < 2 or not re.fullmatch(r"20\d{2}|19\d{2}", parts[1]):
        raise ValueError("Start URL must include exact model and model year")
    prefix = "/" + "/".join(parts[:2]) + "/"
    opener = opener or build_opener()
    robots = robots_policy(opener)
    if not robots.can_fetch(USER_AGENT, start):
        raise PermissionError("robots.txt does not permit the requested starting URL")
    queue = deque([start])
    seen = set()
    records = []
    discovered = set([start])
    while queue and len(records) < max_pages:
        url = queue.popleft()
        if url in seen: continue
        seen.add(url)
        if not robots.can_fetch(USER_AGENT, url):
            records.append({"url": url, "status": "blocked_by_robots"})
            continue
        if records: sleep(delay)
        try:
            raw, actual, content_type = fetch(opener, url)
            if not within_scope(actual, prefix):
                raise ValueError("Redirect left vehicle/year scope")
            if "text/html" not in content_type:
                raise ValueError("Only HTML pages may be indexed")
            data = parse_page(raw.decode("utf-8", errors="replace"), actual, prefix)
            for link in data.pop("child_links"):
                target = link["url"]
                if target not in discovered:
                    discovered.add(target)
                    queue.append(target)
            records.append({"url": actual, "status": "indexed", "html_sha256": hashlib.sha256(raw).hexdigest(), **data})
        except (HTTPError, URLError, ValueError, TimeoutError, OSError) as exc:
            records.append({"url": url, "status": "error", "error_type": type(exc).__name__})
    return {
        "schema": "wis-navigation-manifest-v0.1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "start_url": start,
        "scope_prefix": prefix,
        "pages_processed": len(records),
        "links_discovered": len(discovered),
        "remaining_queue_count": len(queue),
        "records": records,
        "note": "Index only; no full text stored, no part fitment verified, not a coverage certificate",
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--start", default=ORIGIN + "/9-5-9600/2008/2-engine/basic-engine-4-cylinder-petrol/technical-data/")
    p.add_argument("--max-pages", type=int, default=5)
    p.add_argument("--delay", type=float, default=3.0)
    p.add_argument("--output", default="wis-manifest.json")
    args = p.parse_args()
    result = index(args.start, args.max_pages, args.delay)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Indexed {result['pages_processed']} pages, discovered {result['links_discovered']} links; wrote {output}")


if __name__ == "__main__":
    main()
