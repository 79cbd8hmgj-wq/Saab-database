#!/usr/bin/env python3
"""Offline, conservative WIS table candidate extraction for HUMAN REVIEW.

This never fetches pages or writes into the canonical Saab research datasets.
It deliberately abstains from unlabeled, nonnumeric and complex table rows.
"""
import argparse
import hashlib
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit
from wis_indexer import canonical_url

TORQUE_NUMBER = re.compile(r'^\d+(?:[.,]\d+)?$')
TORQUE_HEADER_NM = re.compile(r'^(?:torque\s*\(\s*nm\s*\)|nm)$', re.I)
TORQUE_HEADER_LB = re.compile(r'^torque\s*\(\s*lbf\s*ft\s*\)$', re.I)
RESTRICTION = re.compile(r'(?:up to and including|from and including)\s+engine\s+no\.\s*\d+', re.I)

NUMBER_UNIT = re.compile(r'^\s*[+-]?\d+(?:[.,]\d+)?(?:\s*(?:±|\+/-|–|—|-)\s*\d+(?:[.,]\d+)?)?\s*(°C|°F|kPa|MPa|bar|Nm|N·m|mm|cm|mL|L|rpm|kW|hp|V|A|Ω|ohm|%)\s*$', re.I)

class TableReader(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.heading = ''
        self.section = ''
        self.tables = []
        self._tag_heading = None
        self._heading_text = []
        self._table = None
        self._row = None
        self._cell = None
        self._table_section = ''

    def handle_starttag(self, tag, attrs):
        if tag in ('h1', 'h2', 'h3') and self._table is None:
            self._tag_heading = tag
            self._heading_text = []
        if tag == 'table':
            self._table = []
            self._table_section = self.section or self.heading
        if tag == 'tr' and self._table is not None:
            self._row = []
        if tag in ('td', 'th') and self._row is not None:
            self._cell = []

    def handle_data(self, data):
        if self._tag_heading is not None:
            self._heading_text.append(data)
        if self._cell is not None:
            self._cell.append(data)

    def handle_endtag(self, tag):
        if tag == self._tag_heading:
            txt = ' '.join(''.join(self._heading_text).split())
            if tag == 'h1': self.heading = txt
            else: self.section = txt
            self._tag_heading = None
        if tag in ('td', 'th') and self._cell is not None:
            self._row.append(' '.join(''.join(self._cell).split()))
            self._cell = None
        if tag == 'tr' and self._row is not None:
            self._table.append(self._row)
            self._row = None
        if tag == 'table' and self._table is not None:
            self.tables.append((self._table_section, self._table))
            self._table = None

def extract_candidates(html, source_url, known_source_urls=None):
    canonical = canonical_url(source_url)
    if canonical is None: raise ValueError('Only official HTTPS SaabWISOnline URLs accepted')
    path = urlsplit(canonical).path.strip('/').split('/')
    if len(path) < 3 or not re.fullmatch(r'(19|20)\d{2}', path[1]):
        raise ValueError('Model, year and WIS document path required')
    reader = TableReader()
    reader.feed(html)
    found = []
    fingerprints = set()
    skipped = 0
    for table_no, (section, rows) in enumerate(reader.tables, 1):
        torque_table = bool(rows and len(rows[0]) == 3
                            and TORQUE_HEADER_NM.fullmatch(rows[0][1])
                            and TORQUE_HEADER_LB.fullmatch(rows[0][2]))
        for row_no, cells in enumerate(rows, 1):
            alternate_display_value = None
            applicability_note = None
            if torque_table and row_no > 1 and len(cells) == 3:
                label, nm, lb = cells
                if not label or not TORQUE_NUMBER.fullmatch(nm) or not TORQUE_NUMBER.fullmatch(lb):
                    skipped += 1
                    continue
                if abs(float(nm.replace(',', '.')) * 0.737562149 - float(lb.replace(',', '.'))) > max(1.0, float(nm.replace(',', '.')) * 0.737562149 * 0.08):
                    skipped += 1
                    continue
                alternate_display_value = lb + ' lbf ft'
                restriction = RESTRICTION.search(label)
                applicability_note = restriction.group(0) if restriction else None
                cells = [label, nm + ' Nm']
            elif torque_table and row_no == 1:
                skipped += 1
                continue
            if len(cells) != 2 or not cells[0] or not cells[1]:
                skipped += 1
                continue
            match = NUMBER_UNIT.fullmatch(cells[1])
            if not match:
                skipped += 1
                continue
            identity = json.dumps([canonical, section, cells[0], cells[1]], ensure_ascii=False)
            fingerprint = hashlib.sha256(identity.encode('utf-8')).hexdigest()[:20]
            if fingerprint in fingerprints: continue
            fingerprints.add(fingerprint)
            item = {
                'candidate_id': 'wis-review-' + fingerprint,
                'source_url': canonical,
                'document_heading': reader.heading,
                'subject': cells[0],
                'raw_value': cells[1],
                'unit': match.group(1),
                'locator': f'{section or reader.heading} / table {table_no} / row {row_no}',
                'applicability_hint': {'platform_path': path[0], 'model_year': int(path[1])},
                'review_status': 'needs_vehicle_verification',
                'promotion': 'review_only',
                'warnings': ['Year path is not verified vehicle applicability', 'Numeric row is not independently validated', 'Do not interpret as approved part interchange'],
            }
            if alternate_display_value:
                item['raw_value'] = nm
                item['alternate_display_value'] = alternate_display_value
            if applicability_note:
                item['applicability_note'] = applicability_note
            found.append(item)
    return {
        'schema': 'wis-specification-review-v0.1',
        'source_url': canonical,
        'document_heading': reader.heading,
        'source_already_recorded': canonical in (known_source_urls or set()),
        'tables_examined': len(reader.tables),
        'skipped_rows': skipped,
        'candidates': found,
        'note': 'Offline review-only extraction; not a factory-verified fact dataset or replacement approval',
    }

def write_review(path, result):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
        f.write('\n')

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--html-file', required=True, type=Path, help='Locally supplied HTML file; no network access')
    p.add_argument('--source-url', required=True)
    p.add_argument('--output', required=True, type=Path)
    p.add_argument('--existing-urls', type=Path, help='Optional JSON array of existing source URLs')
    args = p.parse_args()
    urls = set(json.loads(args.existing_urls.read_text(encoding='utf-8'))) if args.existing_urls else set()
    result = extract_candidates(args.html_file.read_text(encoding='utf-8'), args.source_url, urls)
    write_review(args.output, result)
    print(f"Produced {len(result['candidates'])} review-only candidates; skipped {result['skipped_rows']} rows")

if __name__ == '__main__': main()
