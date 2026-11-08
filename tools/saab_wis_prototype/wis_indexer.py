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
from urllib.parse import quote, urljoin, urlsplit, urlunsplit, unquote
from urllib.request import HTTPRedirectHandler, Request, build_opener
from urllib.robotparser import RobotFileParser

HOST = "saabwisonline.com"
ORIGIN = "https://" + HOST
USER_AGENT = "SaabDatabaseResearchIndexer/0.2 (metadata-only; contact site owner before bulk collection)"
MAX_HTML = 2_000_000
REDIRECT_CODES = (301, 302, 303, 307, 308)
RETRY_CODES = (429, 500, 502, 503, 504)
MAX_RETRY_AFTER = 60
FOLDER_MARK, DOCUMENT_MARK = "\U0001F4C1", "\U0001F4C4"


def canonical_url(url):
    s = urlsplit(url)
    if s.scheme != "https" or (s.hostname or "").lower() != HOST or s.username or s.password or s.port:
        return None
    # Encoded separators/NUL would change path meaning after decoding: refuse them outright.
    if re.search(r"%(2f|5c|00)", s.path, re.I):
        return None
    path = re.sub(r"/+", "/", unquote(s.path))
    if ".." in path.split("/") or "\\" in path or any(ord(c) < 32 for c in path):
        return None
    return urlunsplit(("https", HOST, quote(path or "/", safe="/-._~!$&'()*+,;=:@"), "", ""))


def dedupe_key(url):
    """Identity for duplicate detection: canonical URL ignoring a trailing slash only."""
    canon = canonical_url(url)
    if canon is None:
        return None
    return canon.rstrip("/") or "/"


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
        self.images = []
        self.svgs = 0
        self._in_title = False
        self._in_h1 = False
        self._in_crumbs = False
        self._skip = 0
        self._anchor = None
        self._anchor_text = []
        self._anchor_kind = None
        self._recent = ""

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in ("script", "style"): self._skip += 1
        if tag == "title": self._in_title = True
        if tag == "h1" and not self.heading: self._in_h1 = True
        if tag == "div" and attrs.get("id") == "breadcrumbs": self._in_crumbs = True
        if tag == "a":
            self._anchor = attrs.get("href")
            self._anchor_text = []
            recent = self._recent.rstrip()
            self._anchor_kind = ("folder" if recent.endswith(FOLDER_MARK)
                                 else "document" if recent.endswith(DOCUMENT_MARK) else None)
            self._anchor_crumb = self._in_crumbs
        if tag == "table": self.tables += 1
        if tag == "tr": self.rows += 1
        if tag == "img" and "logo-image" not in (attrs.get("class") or ""):
            self.images.append(attrs.get("src") or "")
        if tag == "svg": self.svgs += 1

    def handle_data(self, data):
        if self._skip: return
        if self._in_title: self.title += data
        if self._in_h1: self.heading += data
        if self._anchor is not None: self._anchor_text.append(data)
        if data.strip(): self._recent = data

    def handle_endtag(self, tag):
        if tag in ("script", "style") and self._skip: self._skip -= 1
        if tag == "title": self._in_title = False
        if tag == "h1": self._in_h1 = False
        if tag == "div": self._in_crumbs = False
        if tag == "a" and self._anchor is not None:
            self.links.append((self._anchor, " ".join(" ".join(self._anchor_text).split()),
                               self._anchor_kind, self._anchor_crumb))
            self._anchor = None
            self._anchor_text = []


def parse_page(html, page_url, prefix):
    parser = MetadataParser()
    parser.feed(html)
    links = {}
    for href, label, kind, crumb in parser.links:
        if crumb or not href or href.startswith(("#", "mailto:", "javascript:")):
            continue
        candidate = canonical_url(urljoin(page_url, href))
        if candidate and within_scope(candidate, prefix):
            links.setdefault(dedupe_key(candidate), {"url": candidate, "label": label, "kind": kind or "unknown"})
    image_refs = []
    for src in parser.images:
        full = urljoin(page_url, src)
        if urlsplit(full).hostname == HOST:  # third-party logos/ads are site chrome, not document content
            image_refs.append(full)
    return {
        "heading": " ".join(parser.heading.split()),
        "page_title": " ".join(parser.title.split()),
        "table_count": parser.tables,
        "row_count": parser.rows,
        "image_count": len(image_refs) + parser.svgs,
        "image_refs": image_refs,
        "child_links": list(links.values()),
    }


def decode_html(raw, content_type=""):
    m = re.search(r"charset=([\w-]+)", content_type or "", re.I) or re.search(rb"charset=[\"']?([\w-]+)", raw[:2048], re.I)
    names = [m.group(1).decode() if isinstance(m.group(1), bytes) else m.group(1)] if m else []
    for enc in names + ["utf-8", "cp1252"]:
        try:
            return raw.decode(enc)
        except (UnicodeDecodeError, LookupError):
            continue
    return raw.decode("utf-8", errors="replace")


class _NoRedirect(HTTPRedirectHandler):
    """Surface 3xx responses so every hop can be validated before it is requested."""
    def redirect_request(self, *args, **kwargs):
        return None


def make_opener():
    return build_opener(_NoRedirect)


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


def _is_ancestor(target, current):
    t, c = urlsplit(target).path.rstrip("/"), urlsplit(current).path.rstrip("/")
    return len(t) < len(c) and c.startswith(t + "/")


def _retry_wait(err, attempt, base):
    ra = err.headers.get("Retry-After") if getattr(err, "headers", None) else None
    if ra and str(ra).strip().isdigit():
        return min(int(ra), MAX_RETRY_AFTER)
    return base * (2 ** attempt)


def fetch_document(opener, url, prefix, sleep=time.sleep, delay=3.0, max_retries=3, max_redirects=5, base_backoff=2):
    """Fetch one document without raising for per-document failures.

    Every redirect hop is validated *before* it is requested. A redirect to an ancestor
    directory is reported as ``soft_404_redirect`` (the site answers missing documents
    that way); it is never treated as the requested page.
    """
    current, chain, attempts, seen = url, [], 0, {dedupe_key(url)}
    out = lambda status, **kw: {"status": status, "requested_url": url, "final_url": current,
                                "redirect_chain": chain, "attempts": attempts, **kw}
    hop = 0
    while True:
        attempt = 0
        while True:
            attempts += 1
            try:
                raw, actual, ctype = fetch(opener, current)
                if not within_scope(actual, prefix):
                    return out("redirect_out_of_scope", final_url=actual)
                return out("ok", raw=raw, final_url=actual, content_type=ctype, http_status=200)
            except HTTPError as e:
                if e.code in REDIRECT_CODES:
                    loc = e.headers.get("Location") if e.headers else None
                    target = canonical_url(urljoin(current, loc)) if loc else None
                    if target is None or not within_scope(target, prefix):
                        return out("redirect_out_of_scope", http_status=e.code, redirect_target=loc)
                    if _is_ancestor(target, current):
                        return out("soft_404_redirect", http_status=e.code, redirect_target=target)
                    if dedupe_key(target) in seen and dedupe_key(target) != dedupe_key(current) or hop >= max_redirects:
                        return out("redirect_loop", http_status=e.code)
                    chain.append({"from": current, "to": target, "code": e.code})
                    seen.add(dedupe_key(target))
                    current = target
                    hop += 1
                    sleep(delay)
                    break
                if e.code in (404, 410):
                    return out("missing", http_status=e.code)
                if e.code in RETRY_CODES and attempt < max_retries:
                    sleep(_retry_wait(e, attempt, base_backoff)); attempt += 1; continue
                return out("error", http_status=e.code, error_type=f"http_{e.code}")
            except (URLError, TimeoutError, OSError) as e:
                if attempt < max_retries:
                    sleep(base_backoff * (2 ** attempt)); attempt += 1; continue
                return out("error", error_type=type(e).__name__)
            except ValueError as e:
                msg = str(e)
                status = ("non_text_skipped" if msg.startswith("Non-text") else "redirect_out_of_scope" if "authorized origin" in msg else "error")
                return out(status, error_type="too_large" if "size limit" in msg else "value_error")


def robots_policy(opener):
    robots_url = ORIGIN + "/robots.txt"
    raw, _, _ = fetch(opener, robots_url)
    rp = RobotFileParser()
    rp.parse(raw.decode("utf-8", errors="replace").splitlines())
    return rp


def scope_prefix_for(start_url):
    start = canonical_url(start_url)
    if not start: raise ValueError("Start URL must use official HTTPS host")
    parts = urlsplit(start).path.strip("/").split("/")
    if len(parts) < 2 or not re.fullmatch(r"20\d{2}|19\d{2}", parts[1]):
        raise ValueError("Start URL must include exact model and model year")
    return start, "/" + "/".join(parts[:2]) + "/"


def index(start_url, max_pages=10, delay=3.0, opener=None, sleep=time.sleep, subtree=None):
    """Bounded breadth-first index. ``subtree`` (a path prefix) narrows navigation below model/year."""
    if max_pages < 1 or max_pages > 100: raise ValueError("max_pages must be within 1..100")
    if delay < 2: raise ValueError("delay must be >= 2 seconds")
    start, prefix = scope_prefix_for(start_url)
    nav_prefix = subtree or prefix
    if not within_scope(start, nav_prefix): raise ValueError("Start URL outside requested subtree")
    opener = opener or make_opener()
    robots = robots_policy(opener)
    if not robots.can_fetch(USER_AGENT, start):
        raise PermissionError("robots.txt does not permit the requested starting URL")
    queue = deque([start])
    seen, fetched, hashes = set(), {}, {}
    records = []
    discovered = {dedupe_key(start): start}
    while queue and len(records) < max_pages:
        url = queue.popleft()
        if dedupe_key(url) in seen: continue
        seen.add(dedupe_key(url))
        if not robots.can_fetch(USER_AGENT, url):
            records.append({"url": url, "status": "blocked_by_robots"})
            continue
        if records: sleep(delay)
        res = fetch_document(opener, url, prefix, sleep=sleep, delay=delay)
        base = {"url": res["final_url"] if res["status"] == "ok" else url}
        if res["redirect_chain"]: base["redirect_chain"] = res["redirect_chain"]
        if res["status"] != "ok":
            records.append({**base, "status": res["status"], "http_status": res.get("http_status"),
                            **({"error_type": res["error_type"]} if res.get("error_type") else {})})
            continue
        final_key = dedupe_key(res["final_url"])
        if final_key in fetched and final_key != dedupe_key(url):
            records.append({**base, "status": "duplicate_redirect_target", "duplicate_of": fetched[final_key]})
            continue
        seen.add(final_key)
        fetched[final_key] = res["final_url"]
        if not within_scope(res["final_url"], nav_prefix) and res["final_url"] != start:
            records.append({**base, "status": "outside_subtree"})
            continue
        if "text/html" not in res["content_type"]:
            records.append({**base, "status": "non_text_skipped"}); continue
        raw = res["raw"]
        sha = hashlib.sha256(raw).hexdigest()
        data = parse_page(decode_html(raw, res["content_type"]), res["final_url"], nav_prefix)
        children = data.pop("child_links")
        if sha in hashes:
            records.append({**base, "status": "indexed_duplicate_content", "html_sha256": sha, "duplicate_of": hashes[sha]})
            continue
        hashes[sha] = res["final_url"]
        for link in children:
            key = dedupe_key(link["url"])
            if key not in discovered:
                discovered[key] = link["url"]
                queue.append(link["url"])
        records.append({**base, "status": "indexed", "html_sha256": sha, "bytes": len(raw),
                        "children": [{"url": l["url"], "kind": l["kind"], "label": l["label"]} for l in children], **data})
    return {
        "schema": "wis-navigation-manifest-v0.2",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "start_url": start,
        "scope_prefix": prefix,
        "subtree_prefix": nav_prefix,
        "pages_processed": len(records),
        "links_discovered": len(discovered),
        "remaining_queue_count": len(queue),
        "records": records,
        "note": "Index only; no full text stored, no part fitment verified, not a coverage certificate",
    }


def safe_output_path(path, repo_root=None):
    """Resolve an output path and refuse anything that could touch canonical data."""
    resolved = Path(path).resolve()
    if repo_root is not None:
        root = Path(repo_root).resolve()
        for protected in ("data", "docs", "tests"):
            p = root / protected
            if resolved == p or p in resolved.parents:
                raise ValueError(f"Refusing to write generated output under protected path {p}")
    return resolved


def write_manifest(path, result):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as f:   # never overwrite a previous run
        json.dump(result, f, indent=2, ensure_ascii=False)
        f.write("\n")


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--start", default=ORIGIN + "/9-5-9600/2008/2-engine/cooling-system/")
    p.add_argument("--max-pages", type=int, default=5)
    p.add_argument("--delay", type=float, default=3.0)
    p.add_argument("--output", default="wis-manifest.json")
    p.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[2])
    p.add_argument("--dry-run", action="store_true", help="Validate scope/arguments only; no network, no writes")
    args = p.parse_args()
    start, prefix = scope_prefix_for(args.start)
    output = safe_output_path(args.output, args.repo_root)
    if args.max_pages < 1 or args.max_pages > 100 or args.delay < 2: raise SystemExit("max-pages 1..100 and delay >= 2 required")
    if args.dry_run:
        print(json.dumps({"dry_run": True, "start": start, "scope_prefix": prefix, "max_pages": args.max_pages,
                          "delay": args.delay, "output": str(output), "output_exists": output.exists()}, indent=2))
        return
    result = index(args.start, args.max_pages, args.delay)
    write_manifest(output, result)
    print(f"Indexed {result['pages_processed']} pages, discovered {result['links_discovered']} links; wrote {output}")


if __name__ == "__main__":
    main()
