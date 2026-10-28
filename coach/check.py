#!/usr/bin/env python3
"""Fixed lesson checker.

    python coach/check.py 1            check lesson 1's artefact against coach/specs/lesson-01.json
    python coach/check.py --list       every lesson, its artefact and its rule count
    python coach/check.py 9 --online   also fetch live URLs (off by default, works offline)

Read-only. The specs are the standard, fixed before the learner starts, and the agent may run this
but may not edit it. Output is one PASS or FAIL line per rule, then a RESULT line.

Columns are found by header name, not by position, so a learner who drops the number column or reorders
the table is still checked fairly.
"""
import argparse
import json
import pathlib
import re
import sys
import urllib.error
import urllib.request

HERE = pathlib.Path(__file__).resolve().parent
SPECS = HERE / 'specs'
DATE = re.compile(r'\b(\d{1,2}\s+\w{3,9}\s+\d{4}|\d{4}-\d{2}-\d{2}|\d{1,2}/\d{1,2}/\d{2,4})\b')
URL = re.compile(r'https?://[^\s)\]<>"]+')


def read(path):
    if '*' in path:
        matches = [f for f in sorted(pathlib.Path('.').glob(path)) if f.is_file()]
        if not matches:
            return None
        path = str(matches[0])
    p = pathlib.Path(path)
    return p.read_text(encoding='utf-8', errors='replace') if p.exists() else None


def blocks(text):
    """Every markdown table as (headers, data rows). First row is the header."""
    out, headers, rows, inside = [], [], [], False
    for line in list(text.splitlines()) + ['']:
        s = line.strip()
        if s.startswith('|'):
            cells = [c.strip() for c in s.strip('|').split('|')]
            if set(''.join(cells)) <= set('-: '):
                continue
            if not inside:
                headers, rows, inside = cells, [], True
            else:
                rows.append(cells)
            continue
        if inside:
            out.append((headers, rows))
            headers, rows, inside = [], [], False
    return out


def all_rows(text):
    return [(h, r) for (h, rows) in blocks(text) for r in rows]


def col_index(headers, names):
    for want in names:
        for i, h in enumerate(headers):
            if want.lower() in h.lower():
                return i
    return None


def cell(row, idx):
    return row[idx] if idx is not None and idx < len(row) else ''


def run_check(spec, online):
    kind = spec['type']
    art = spec.get('file', '')

    if kind == 'files':
        found = [f for f in sorted(pathlib.Path('.').glob(spec['glob'])) if f.is_file()]
        ok = len(found) >= spec.get('min', 1)
        return ok, spec['label'], 'found %d: %s' % (len(found), ', '.join(str(f) for f in found[:3]) or 'none')

    text = read(art)
    if text is None:
        return False, spec['label'], 'missing file: %s' % art

    if kind == 'words':
        n = len(text.split())
        lo, hi = spec.get('min', 0), spec.get('max', 10 ** 9)
        return lo <= n <= hi, spec['label'], '%d words' % n

    if kind == 'lines':
        n = len([l for l in text.splitlines() if l.strip()])
        return n >= spec.get('min', 1), spec['label'], '%d non-empty lines' % n

    if kind == 'headings':
        heads = [l.strip('# ').lower() for l in text.splitlines() if l.startswith('#')]
        missing = [h for h in spec['all'] if not any(h.lower() in x for x in heads)]
        return not missing, spec['label'], ('missing: %s' % missing) if missing else 'all present'

    if kind == 'rows':
        n = len(all_rows(text))
        lo, hi = spec.get('min', 0), spec.get('max', 10 ** 9)
        return lo <= n <= hi, spec['label'], '%d data rows' % n

    if kind == 'col':
        names, need = spec.get('headers', []), spec.get('min_chars', 1)
        pairs = all_rows(text)
        if not pairs:
            return False, spec['label'], 'no table found'
        missing_col = [n for n in names if col_index(pairs[0][0], [n]) is None]
        bad = []
        for i, (headers, row) in enumerate(pairs, 1):
            idx = col_index(headers, names)
            if idx is None or len(cell(row, idx)) < need:
                bad.append(i)
        detail = ('thin or missing cells on rows %s' % bad[:6]) if bad else '%d rows pass' % len(pairs)
        if bad and missing_col and len(bad) == len(pairs):
            detail = 'no %s column' % missing_col[0]
        return not bad, spec['label'], detail

    if kind == 'col_any':
        names, any_of = spec.get('headers', []), [a.lower() for a in spec['any_of']]
        need = spec.get('min_rows', 1)
        hits = []
        for i, (headers, row) in enumerate(all_rows(text), 1):
            idx = col_index(headers, names)
            if idx is not None and any(a in cell(row, idx).lower() for a in any_of):
                hits.append(i)
        return len(hits) >= need, spec['label'], '%d matching rows (need %d)' % (len(hits), need)

    if kind == 'has_any':
        present = [w for w in spec['any_of'] if w.lower() in text.lower()]
        return bool(present), spec['label'], ('found: %s' % present[0]) if present else 'none of %s' % spec['any_of']

    if kind == 'absent':
        hits = [p for p in spec['patterns'] if re.search(p, text, re.I)]
        return not hits, spec['label'], ('found: %s' % hits) if hits else 'clean'

    if kind == 'present':
        missing = [p for p in spec['patterns'] if not re.search(p, text, re.I)]
        return not missing, spec['label'], ('missing: %s' % missing) if missing else 'all present'

    if kind == 'dates':
        n = len(DATE.findall(text))
        return n >= spec.get('min', 1), spec['label'], '%d dates' % n

    if kind == 'frontmatter':
        head = text[:600]
        missing = [k for k in spec['keys'] if not re.search(r'^%s\s*:' % re.escape(k), head, re.M)]
        return not missing, spec['label'], ('missing keys: %s' % missing) if missing else 'all present'

    if kind == 'urls':
        found = URL.findall(text)
        if len(found) < spec.get('min', 1):
            return False, spec['label'], 'found %d urls' % len(found)
        if not online:
            return True, spec['label'], '%d urls, liveness not checked (offline)' % len(found)
        for u in found:
            try:
                req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0 check'})
                with urllib.request.urlopen(req, timeout=15) as r:
                    if not (200 <= r.status < 400):
                        return False, spec['label'], '%s returned %s' % (u, r.status)
            except urllib.error.HTTPError as e:
                return False, spec['label'], '%s returned %s' % (u, e.code)
            except Exception as e:
                return False, spec['label'], '%s unreachable (%s)' % (u, type(e).__name__)
        return True, spec['label'], '%d urls live' % len(found)

    return False, spec.get('label', kind), 'unknown check type'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('lesson', nargs='?', type=int)
    ap.add_argument('--list', action='store_true')
    ap.add_argument('--online', action='store_true')
    a = ap.parse_args()

    specs = sorted(SPECS.glob('lesson-*.json'))
    if a.list or not a.lesson:
        for p in specs:
            s = json.loads(p.read_text(encoding='utf-8'))
            print('%2d  %-44s %2d rules  %s' % (s['lesson'], s['artefact'], len(s['checks']), s['title']))
        return 0

    p = SPECS / ('lesson-%02d.json' % a.lesson)
    if not p.exists():
        print('no spec for lesson %d' % a.lesson)
        return 2
    spec = json.loads(p.read_text(encoding='utf-8'))

    print('lesson %d: %s' % (spec['lesson'], spec['title']))
    print('artefact: %s' % spec['artefact'])
    failures = []
    for c in spec['checks']:
        ok, label, detail = run_check(c, a.online)
        print('%s  %s  (%s)' % ('PASS' if ok else 'FAIL', label, detail))
        if not ok:
            failures.append(label)
    print('RESULT %s' % ('all checks passed' if not failures else 'failures: ' + '; '.join(failures)))
    return 0 if not failures else 1


if __name__ == '__main__':
    sys.exit(main())
