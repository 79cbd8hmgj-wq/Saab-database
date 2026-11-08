#!/usr/bin/env python3
"""Offline, conservative WIS table candidate extraction for HUMAN REVIEW.

This never fetches pages or writes into the canonical Saab research datasets.
Tables are expanded into a real column grid (colspan/rowspan) and mapped by header
text. Anything not confidently interpretable becomes a ``review_required`` record
that preserves the original cells; it is never reduced to an invented fact.

Information classes on every record:
  A  directly extractable (explicit number + labelled unit, nothing conditional)
  B  needs interpretation (multi-stage/angle procedures, conditional text)
  C  needs human/engineering verification (engine/chassis boundaries, fitment)
"""
import argparse
import hashlib
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit
from wis_indexer import canonical_url

SCHEMA = 'wis-specification-review-v0.2'
TORQUE_NUMBER = re.compile(r'^\d+(?:[.,]\d+)?$')
TORQUE_HEADER_NM = re.compile(r'^(?:torque\s*\(\s*nm\s*\)|nm)$', re.I)
TORQUE_HEADER_LB = re.compile(r'^torque\s*\(\s*lbf\s*ft\s*\)$', re.I)
# Retained for backward compatibility (first match is exposed as applicability_note).
RESTRICTION = re.compile(r'(?:up to and including|from and including)\s+engine\s+no\.\s*\d+', re.I)
_REL = {'up to and including': 'up_to_and_including', 'to and including': 'up_to_and_including',
        'up to': 'up_to_inclusivity_unstated', 'from and including': 'from_and_including',
        'from': 'from_inclusivity_unstated', 'as of': 'from_inclusivity_unstated'}
_REL_RE = r'(up to and including|to and including|up to|from and including|from|as of)'
ENGINE_NO = re.compile(_REL_RE + r'\s+engine\s+(?:no\.?|number)\s*([A-Za-z0-9]+)', re.I)
CHASSIS_NO = re.compile(_REL_RE + r'\s+(?:chassis|vin|vehicle\s+identification)\s*(?:no\.?|number)?\s*([A-Za-z0-9]+)', re.I)
CONFIG_TOKEN = re.compile(r'(?<![\w-])(?:([2-8])\s*-?\s*cyl(?:inder)?s?|(v6)|(diesel)|(petrol)|(manual)|(automatic)|(sedan)|(estate)|(sportcombi)|(convertible))(?![\w])', re.I)
MULTISTAGE = re.compile(r'\d\s*°|\btighten\b|\bfurther\b|\bstage\b|\bthen\b|\bangle\b|^\s*\d+(?:[.,]\d+)?(?:\s+\d+(?:[.,]\d+)?)+\b', re.I)
NUMBER_UNIT = re.compile(r'^\s*[+-]?\d+(?:[.,]\d+)?(?:\s*(?:±|\+/-|–|—|-)\s*\d+(?:[.,]\d+)?)?\s*(°C|°F|kPa|MPa|bar|Nm|N·m|mm|cm|mL|L|rpm|kW|hp|V|A|Ω|ohm|%)\s*$', re.I)
DTC = re.compile(r'\b[PBCU]\d{4}\b')
WARNING_WORD = re.compile(r'^\s*(warning|caution|note|important)\b', re.I)
NM_TO_LBFFT = 0.737562149
MAX_SPAN = 50


class TableReader(HTMLParser):
    """Collect headings and tables (as raw cell lists with spans); tolerant of malformed markup."""

    SKIP = ('script', 'style', 'ins', 'noscript')

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title = ''
        self.heading = ''
        self.section = ''
        self.tables = []          # finished or open tables, in start order
        self.paragraphs = []
        self.images = []
        self.list_items = 0
        self._title = False
        self._head_tag = None
        self._head_text = []
        self._p = None
        self._skip = 0
        self._stack = []          # open tables

    # -- helpers
    def _close_cell(self):
        t = self._stack[-1]
        if t['cell'] is not None:
            raw = ''.join(t['cell']['buf'])
            t['row'].append({'text': ' '.join(raw.split()),
                             'lines': [' '.join(l.split()) for l in raw.split('\n') if l.strip()],
                             'colspan': t['cell']['cs'], 'rowspan': t['cell']['rs']})
            t['cell'] = None

    def _close_row(self):
        t = self._stack[-1]
        self._close_cell()
        if t['row'] is not None:
            t['rows'].append(t['row'])
            t['row'] = None

    def _close_table(self):
        self._close_row()
        self._stack.pop()

    @staticmethod
    def _span(v):
        try:
            return max(1, min(MAX_SPAN, int(v)))
        except (TypeError, ValueError):
            return 1

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in self.SKIP:
            self._skip += 1
            return
        if tag == 'title': self._title = True
        if tag in ('h1', 'h2', 'h3') and not self._stack:
            self._head_tag, self._head_text = tag, []
        if tag == 'p' and not self._stack: self._p = []
        if tag == 'li': self.list_items += 1
        if tag == 'img': self.images.append(attrs.get('src') or '')
        if tag == 'table':
            table = {'section': self.section or self.heading, 'rows': [], 'row': None, 'cell': None,
                     'index': len(self.tables) + 1, 'depth': len(self._stack)}
            self.tables.append(table)
            self._stack.append(table)
        elif self._stack:
            t = self._stack[-1]
            if tag == 'tr':
                self._close_row(); t['row'] = []
            elif tag in ('td', 'th'):
                if t['row'] is None: t['row'] = []
                self._close_cell()
                t['cell'] = {'buf': [], 'cs': self._span(attrs.get('colspan')), 'rs': self._span(attrs.get('rowspan'))}
            elif tag == 'br' and t['cell'] is not None:
                t['cell']['buf'].append('\n')

    def handle_data(self, data):
        if self._skip: return
        if self._title: self.title += data
        if self._head_tag: self._head_text.append(data)
        if self._p is not None: self._p.append(data)
        if self._stack and self._stack[-1]['cell'] is not None:
            self._stack[-1]['cell']['buf'].append(data)

    def handle_endtag(self, tag):
        if tag in self.SKIP:
            if self._skip: self._skip -= 1
            return
        if tag == 'title': self._title = False
        if tag == self._head_tag:
            txt = ' '.join(''.join(self._head_text).split())
            if tag == 'h1' and not self.heading: self.heading = txt
            elif tag != 'h1': self.section = txt
            self._head_tag = None
        if tag == 'p' and self._p is not None:
            txt = ' '.join(''.join(self._p).split())
            if txt: self.paragraphs.append(txt)
            self._p = None
        if self._stack:
            if tag == 'table': self._close_table()
            elif tag == 'tr': self._close_row()
            elif tag in ('td', 'th'): self._close_cell()

    def close(self):
        super().close()
        while self._stack: self._close_table()


def expand_grid(rows):
    """Place cells on a real column grid. Returns, per row, placements sorted by column.

    Each placement: text, c0, c1 (exclusive), inherited (True when a rowspan from an earlier row covers it).
    """
    carried = {}   # col -> (remaining_rows, placement template)
    grid = []
    for row in rows:
        placed, col, created = [], 0, set()
        for cell in row:
            while col in carried and carried[col][0] > 0:
                col += 1
            c0, c1 = col, col + cell['colspan']
            placed.append({'text': cell['text'], 'lines': cell['lines'], 'c0': c0, 'c1': c1, 'inherited': False})
            if cell['rowspan'] > 1:
                for cc in range(c0, c1):
                    carried[cc] = (cell['rowspan'] - 1, {'text': cell['text'], 'lines': cell['lines'], 'c0': c0, 'c1': c1})
                    created.add(cc)
            col = c1
        # rowspan carry-over cells covering this row (decrement after use)
        seen = set()
        for cc, (rem, tpl) in list(carried.items()):
            if rem > 0 and not any(p['c0'] <= cc < p['c1'] and not p['inherited'] for p in placed):
                key = (tpl['c0'], tpl['c1'])
                if key not in seen:
                    placed.append({**tpl, 'inherited': True}); seen.add(key)
        for cc in list(carried):
            if cc in created: continue
            rem, tpl = carried[cc]
            carried[cc] = (rem - 1, tpl)
            if rem - 1 <= 0: del carried[cc]
        grid.append(sorted(placed, key=lambda p: p['c0']))
    return grid


def parse_restrictions(text):
    eng = [{'relation': _REL[m.group(1).lower()], 'boundary': m.group(2), 'source_text': m.group(0)}
           for m in ENGINE_NO.finditer(text)]
    ch = [{'relation': _REL[m.group(1).lower()], 'boundary': m.group(2), 'source_text': m.group(0)}
          for m in CHASSIS_NO.finditer(text)]
    tokens = []
    for m in CONFIG_TOKEN.finditer(text):
        tok = f'{m.group(1)}-cyl' if m.group(1) else m.group(0).lower()
        if tok not in tokens: tokens.append(tok)
    return {'engine_number': eng, 'chassis_number': ch}, tokens



UNIT_BASE = r'(?:°C|°F|kPa|MPa|bar|psi|Nm|N·m|lbf ft|mm|cm|in|L|mL|rpm|kW|hp|V|A|Ohm|Ω|%|km/h|ms|s|g|kg|W|Hz)'
UNIT_CELL = re.compile(rf'^({UNIT_BASE})(?:\s*\(\s*({UNIT_BASE})\s*\))?((?:\s+{UNIT_BASE})*)$')
_NUM = r'[+-]?\d+(?:[.,]\d+)?'
_PRIMARY = rf'(?:{_NUM}\s*[-–—]\s*{_NUM}|{_NUM}(?:\s*(?:±|\+/-)\s*{_NUM}\s*%?)?)'
VALUE_PRIMARY = re.compile(rf'^({_PRIMARY})$')
VALUE_DUAL = re.compile(rf'^({_PRIMARY})\s*\(\s*({_PRIMARY})\s*\)$')
DTC_ROW = re.compile(r'^[PBCU]\d{4}$')
NOTE_WORDS = re.compile(r'^(note|warning|caution|important)$', re.I)


def classify_table(grid):
    """Structure class of one expanded table; 'unclassified' means we do not know how to read it."""
    if not grid: return 'empty'
    texts = [[p['text'] for p in r] for r in grid]
    flat = ' '.join(t for r in texts for t in r)
    if len(grid) == 1:
        first = texts[0]
        if len(first) <= 2 and not re.search(r'\d', flat) and first[0] == '': return 'banner'
        if len(first) == 1 and NOTE_WORDS.match(first[0]): return 'note_box'
        if first and re.fullmatch(r'\d+\.', first[0]): return 'procedure_step'
        if first and first[0] == '•': return 'bullet_item'
        if len(first) == 1 and not re.search(r'\d', first[0]): return 'text_block'
    if len(grid) >= 1 and NOTE_WORDS.match(texts[0][0] if texts[0] else '') and len(texts[0]) == 1:
        return 'note_box'
    if texts and texts[0] and re.match(r'(?i)diagnostic trouble code', texts[0][0]) and all(DTC_ROW.match(r[0]) for r in texts[1:] if r and r[0]):
        return 'dtc_table'
    if len(grid) >= 2 and all(t == 'X' or t == '' for t in texts[-1]) and any(t == 'X' for t in texts[-1]):
        return 'applicability_matrix'
    if any(len(r) >= 3 and UNIT_CELL.fullmatch(r[-2]) and re.search(r'\d', r[-1]) for r in texts):
        return 'label_unit_value'
    return 'unclassified'


def _unit_value_rows(canonical, path, reader, section, table_no, grid, found, seen, review):
    """Interpret a label | [sub-label] | unit | value table. Returns number of rows not promoted."""
    skipped = 0
    group = None
    prev_label = None
    for row_no, placed in enumerate(grid, 1):
        cells = [p['text'] for p in placed]
        if not any(cells): skipped += 1; continue
        if len(placed) < 2: skipped += 1; continue
        unit_p, value_p = placed[-2], placed[-1]
        label_ps = placed[:-2]
        label_lines = (label_ps[0]['lines'] if label_ps else []) or ([label_ps[0]['text']] if label_ps and label_ps[0]['text'] else [])
        label = label_lines[0] if label_lines else ''
        conditions = label_lines[1:]
        subs = label_ps[1:]
        if not unit_p['text'] and not value_p['text'] and len(label_ps) <= 1 and label:
            group = label; prev_label = None; skipped += 1; continue          # group header row
        def rr(reason, cls='B'):
            review.append(_review(table_no, row_no, section, reader.heading, reason, cells, cls))
        if len(subs) > 1: skipped += 1; rr('too_many_label_columns'); continue
        continued = False
        if not label and prev_label and subs:
            label, continued = prev_label, True
        elif not label:
            skipped += 1; rr('missing_label'); continue
        else:
            prev_label = label
        if unit_p['inherited'] or value_p['inherited']: skipped += 1; rr('inherited_value_cell'); continue
        um = UNIT_CELL.fullmatch(unit_p['text'])
        if not um:
            skipped += 1
            if not unit_p['text']:
                if value_p['text']: rr('text_value_no_unit', 'A')
            elif re.search(r'\d', value_p['text']):
                rr('unit_cell_not_recognised')
            continue
        if um.group(3).strip():
            skipped += 1; rr('multi_measure_cell'); continue                     # e.g. "°C (°F) bar" + "131 (268) 1.4"
        vlines = value_p['lines'] or [value_p['text']]
        slines = subs[0]['lines'] if subs else []
        if len(vlines) > 1:
            if not subs or len(slines) != len(vlines): skipped += 1; rr('multiline_value_unpaired'); continue
            pairs = list(zip(slines, vlines)); paired = True
        else:
            if subs and len(slines) > 1: skipped += 1; rr('multiline_value_unpaired'); continue
            pairs = [((subs[0]['text'] if subs else ''), vlines[0])]; paired = False
        has_alt_unit = um.group(2) is not None
        ok = True
        built = []
        for sub, vtext in pairs:
            d, sg = VALUE_DUAL.fullmatch(vtext), VALUE_PRIMARY.fullmatch(vtext)
            if has_alt_unit and d: prim, alt = d.group(1).strip(), d.group(2).strip() + ' ' + um.group(2)
            elif sg: prim, alt = sg.group(1).strip(), None
            else: ok = False; break
            built.append((sub, vtext, prim, alt))
        if not ok:
            skipped += 1; rr('multi_measure_cell' if re.search(r'\d.*\d', value_p['text']) else 'missing_or_non_numeric_value'); continue
        for k, (sub, vtext, prim, alt) in enumerate(built):
            subject = ' / '.join(x for x in (label, sub) if x)
            ctx = ' | '.join(x for x in (group,) if x)
            item = _build(canonical, path, reader, section, table_no, row_no, subject, prim, um.group(1), alt,
                          False, prim + ' ' + um.group(1) + (' @' + ctx if ctx else ''))
            if group:
                gr, gt = parse_restrictions(group)
                item['group_context'] = group
                item['applicability_restrictions']['engine_number'] += gr['engine_number']
                item['applicability_restrictions']['chassis_number'] += gr['chassis_number']
                for t in gt:
                    if t not in item['configuration_tokens']: item['configuration_tokens'].append(t)
                item['warnings'].append('group_context_inferred_from_preceding_header_row')
            item['source_value_text'], item['source_unit_text'] = vtext, unit_p['text']
            if paired: item['locator'] += f' / line {k + 1}'; item['warnings'].append('paired_by_multiline_alignment')
            if continued: item['warnings'].append('label_continued_from_previous_row')
            if conditions:
                item['explicit_conditions'] = conditions
                item['warnings'].append('subject_has_explicit_condition_text')
                item['candidate_id'] = 'wis-review-' + hashlib.sha256(json.dumps([item['candidate_id'], conditions], ensure_ascii=False).encode()).hexdigest()[:20]
            if group or paired or continued or conditions: item['info_class'] = 'B'
            if item['candidate_id'] in seen: continue
            seen.add(item['candidate_id']); found.append(item)
    return skipped


def _covering(placed, col):
    return [p for p in placed if p['c0'] <= col < p['c1']]


def _review(table_no, row_no, section, heading, reason, cells, info_class):
    return {'reason': reason, 'info_class': info_class, 'locator': f'{section or heading} / table {table_no} / row {row_no}',
            'raw_cells': [c[:300] for c in cells], 'promotion': 'review_only'}


def _build(canonical, path, reader, section, table_no, row_no, label, value, unit_text, alt, inherited_label, id_value):
    restrictions, tokens = parse_restrictions(label)
    has_restriction = bool(restrictions['engine_number'] or restrictions['chassis_number'])
    identity = json.dumps([canonical, section, label, id_value], ensure_ascii=False)
    fp = hashlib.sha256(identity.encode('utf-8')).hexdigest()[:20]
    warnings = ['Year path is not verified vehicle applicability', 'Numeric row is not independently validated',
                'Do not interpret as approved part interchange']
    if inherited_label: warnings.append('inherited_label_from_rowspan')
    item = {
        'candidate_id': 'wis-review-' + fp,
        'source_url': canonical,
        'document_heading': reader.heading,
        'document_title': ' '.join(reader.title.split()),
        'subject': label,
        'raw_value': value,
        'unit': unit_text,
        'locator': f'{section or reader.heading} / table {table_no} / row {row_no}',
        'source_section': section or reader.heading,
        'system_path': '/'.join(path[2:-1]),
        'applicability_hint': {'platform_path': path[0], 'model_year': int(path[1])},
        'applicability_restrictions': restrictions,
        'configuration_tokens': tokens,
        'info_class': 'C' if has_restriction else 'A',
        'review_status': 'needs_vehicle_verification',
        'promotion': 'review_only',
        'warnings': warnings,
    }
    if alt: item['alternate_display_value'] = alt
    first = (restrictions['engine_number'] + restrictions['chassis_number'])
    note = RESTRICTION.search(label)
    if note: item['applicability_note'] = note.group(0)
    elif first: item['applicability_note'] = first[0]['source_text']
    return item


def extract_candidates(html, source_url, known_source_urls=None):
    canonical = canonical_url(source_url)
    if canonical is None: raise ValueError('Only official HTTPS SaabWISOnline URLs accepted')
    path = urlsplit(canonical).path.strip('/').split('/')
    if len(path) < 3 or not re.fullmatch(r'(19|20)\d{2}', path[1]):
        raise ValueError('Model, year and WIS document path required')
    reader = TableReader()
    reader.feed(html)
    reader.close()
    found, review, unsupported, diagnostic, table_classes = [], [], [], [], {}
    seen = set()
    skipped = 0
    for table in reader.tables:
        section, table_no = table['section'], table['index']
        rows = table['rows']
        grid = expand_grid(rows)
        header = grid[0] if grid else []
        nm = next((p for p in header if TORQUE_HEADER_NM.fullmatch(p['text'])), None)
        lb = next((p for p in header if TORQUE_HEADER_LB.fullmatch(p['text'])), None)
        torque_table = bool(nm and lb and nm is not lb)
        kind = 'torque_table' if torque_table else classify_table(grid)
        table_classes[kind] = table_classes.get(kind, 0) + 1
        if kind in ('banner', 'empty', 'note_box', 'procedure_step', 'bullet_item', 'text_block', 'applicability_matrix'):
            skipped += len(rows); continue
        if kind == 'dtc_table':
            for row_no, placed in enumerate(grid, 1):
                if row_no > 1 and placed and DTC_ROW.match(placed[0]['text']):
                    diagnostic.append({'code': placed[0]['text'], 'description_verbatim': placed[1]['text'] if len(placed) > 1 else '',
                                       'locator': f'{section or reader.heading} / table {table_no} / row {row_no}',
                                       'promotion': 'review_only', 'info_class': 'A'})
            skipped += len(rows); continue
        if kind == 'label_unit_value':
            skipped += _unit_value_rows(canonical, path, reader, section, table_no, grid, found, seen, review)
            continue
        texts_all = ' '.join(p['text'] for r in grid for p in r)
        if not torque_table and not any(len(r) == 2 for r in grid) and not re.search(r'\d', texts_all):
            skipped += len(rows)
            continue   # layout/banner table: no digits, nothing to interpret
        table_candidates = 0
        for row_no, placed in enumerate(grid, 1):
            cells = [p['text'] for p in placed]
            if torque_table:
                if row_no == 1:
                    skipped += 1
                    continue
                first_val = min(nm['c0'], lb['c0'])
                last_val = max(nm['c1'], lb['c1'])
                label_cells = [p for p in placed if p['c1'] <= first_val]
                label = ' '.join(p['text'] for p in label_cells if p['text'])
                nm_cells, lb_cells = _covering(placed, nm['c0']), _covering(placed, lb['c0'])
                extra = [p for p in placed if p['c0'] >= last_val and p['text']]
                reason = None
                if not any(cells):
                    skipped += 1
                    continue
                if extra: reason = ('unexpected_extra_columns', 'B')
                elif len(nm_cells) != 1 or len(lb_cells) != 1 or nm_cells[0] is lb_cells[0]:
                    reason = ('value_cell_spans_columns', 'B')
                elif not label: reason = ('missing_label', 'B')
                else:
                    nm_text, lb_text = nm_cells[0]['text'], lb_cells[0]['text']
                    if MULTISTAGE.search(nm_text) or MULTISTAGE.search(lb_text):
                        reason = ('multistage_or_angle_procedure', 'B')
                    elif nm_cells[0]['inherited'] or lb_cells[0]['inherited']:
                        reason = ('inherited_value_cell', 'B')
                    elif not TORQUE_NUMBER.fullmatch(nm_text) or not TORQUE_NUMBER.fullmatch(lb_text):
                        reason = ('missing_or_non_numeric_value', 'B')
                    else:
                        n, l = float(nm_text.replace(',', '.')), float(lb_text.replace(',', '.'))
                        expected = n * NM_TO_LBFFT
                        if abs(expected - l) > 0.1 + 0.01 * expected:
                            reason = ('nm_lbfft_inconsistent', 'C')
                if reason:
                    skipped += 1
                    review.append(_review(table_no, row_no, section, reader.heading, reason[0], cells, reason[1]))
                    continue
                value, unit_text, alt = nm_text, 'Nm', lb_text + ' lbf ft'
                id_value = nm_text + ' Nm'
                inherited_label = any(p['inherited'] for p in label_cells)
            else:
                if len(placed) != 2 or not cells[0] or not cells[1]:
                    skipped += 1
                    if len(placed) > 2 and re.search(r'\d', ' '.join(cells[1:])) and row_no > 1:
                        review.append(_review(table_no, row_no, section, reader.heading, 'unsupported_table_shape', cells, 'B'))
                    continue
                m = NUMBER_UNIT.fullmatch(cells[1])
                if not m:
                    skipped += 1
                    if re.search(r'\d', cells[1]):
                        review.append(_review(table_no, row_no, section, reader.heading, 'value_not_numeric_with_unit', cells, 'B'))
                    continue
                label, value, unit_text, alt = cells[0], cells[1], m.group(1), None
                id_value, inherited_label = cells[1], placed[0]['inherited']
            item = _build(canonical, path, reader, section, table_no, row_no, label, value, unit_text, alt,
                          inherited_label, id_value)
            if item['candidate_id'] in seen: continue
            seen.add(item['candidate_id'])
            found.append(item)
            table_candidates += 1
        if not torque_table and table_candidates == 0 and len(rows) > 1:
            unsupported.append({'locator': f'{section or reader.heading} / table {table_no}', 'rows': len(rows),
                                'header': [p['text'][:80] for p in header],
                                'reason': 'no_recognized_specification_columns'})
    # same subject, different value inside ONE document: never pick a winner
    by_subject = {}
    for it in found:
        key = (it['subject'].casefold(), it.get('group_context', ''), json.dumps(it.get('explicit_conditions', [])),
               json.dumps(it['applicability_restrictions'], sort_keys=True))
        by_subject.setdefault(key, []).append(it)
    internal = []
    for subj, items in by_subject.items():
        if len({(i['raw_value'], i['unit']) for i in items}) > 1:
            internal.append({'subject': items[0]['subject'], 'candidate_ids': [i['candidate_id'] for i in items]})
            for i in items: i['warnings'].append('same_subject_different_value_in_document')
    return {
        'schema': SCHEMA,
        'source_url': canonical,
        'document_heading': reader.heading,
        'document_title': ' '.join(reader.title.split()),
        'source_already_recorded': canonical in (known_source_urls or set()),
        'tables_examined': len(reader.tables),
        'skipped_rows': skipped,
        'candidates': found,
        'review_required': review,
        'diagnostic_records': diagnostic,
        'table_classes': table_classes,
        'unsupported_tables': unsupported,
        'internal_conflicts': internal,
        'note': 'Offline review-only extraction; not a factory-verified fact dataset or replacement approval',
    }


def profile_document(html):
    """Structure profile used for coverage reporting (no page text is retained)."""
    r = TableReader()
    r.feed(html)
    r.close()
    text = ' '.join(r.paragraphs)
    return {
        'heading': r.heading,
        'tables': len(r.tables),
        'paragraphs': len(r.paragraphs),
        'list_items': r.list_items,
        'warning_paragraphs': sum(bool(WARNING_WORD.match(p)) for p in r.paragraphs),
        'dtc_codes_seen': sorted(set(DTC.findall(text + ' ' + ' '.join(c['text'] for t in r.tables for row in t['rows'] for c in row)))),
        'image_refs': [s for s in r.images if s],
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
    print(f"Produced {len(result['candidates'])} review-only candidates; "
          f"{len(result['review_required'])} review-required rows; skipped {result['skipped_rows']} rows")

if __name__ == '__main__': main()
