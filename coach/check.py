#!/usr/bin/env python3
"""Lesson 1 checker: reads position/tasks.md and prints PASS/FAIL lines.

Read-only, and the coach may not edit it: the standard is fixed before the work starts.
"""
import pathlib
import re
import sys

work = pathlib.Path.cwd()
f = work / 'position' / 'tasks.md'

if not f.exists():
    print('FAIL  position/tasks.md not found')
    print('RESULT not checked')
    sys.exit(1)

rows = []
for line in f.read_text(encoding='utf-8').splitlines():
    if not line.strip().startswith('|'):
        continue
    cells = [c.strip() for c in line.strip().strip('|').split('|')]
    if len(cells) < 3 or set(''.join(cells)) <= set('-: '):
        continue
    if cells[0].lower().startswith('task') or cells[0].lower().startswith('#'):
        continue
    rows.append(cells)

failures = []
print('rows parsed: %d' % len(rows))

if 8 <= len(rows) <= 12:
    print('PASS  row count %d is within 8 to 12' % len(rows))
else:
    failures.append('row count')
    print('FAIL  row count %d is outside 8 to 12' % len(rows))

LABELS = ('machine', 'human', 'agent', 'ai', 'assist')
human_only, machine_carried, unlabelled, no_freq = [], [], [], []
for i, cells in enumerate(rows, 1):
    # the table is: #, task, how often, label, evidence
    if len(cells) >= 5:
        label_cell, freq_cell = cells[3].lower(), cells[2].lower()
    elif len(cells) == 4:
        label_cell, freq_cell = cells[2].lower(), cells[1].lower()
    else:
        label_cell, freq_cell = cells[-1].lower(), ' '.join(cells).lower()
    joined = ' '.join(cells).lower()
    if not any(k in label_cell for k in LABELS):
        unlabelled.append(i)
    if 'human only' in label_cell or 'human-only' in label_cell:
        human_only.append((i, cells))
    if 'machine' in label_cell or 'agent' in label_cell or 'ai' in label_cell:
        machine_carried.append((i, cells))
    if not re.search(r'day|week|month|daily|weekly|monthly|quarter|each|every|per', freq_cell):
        no_freq.append(i)

if unlabelled:
    failures.append('labels')
    print('FAIL  rows without a label: %s' % unlabelled)
else:
    print('PASS  every row carries a label')

if no_freq:
    failures.append('frequency')
    print('FAIL  rows without a frequency: %s' % no_freq)
else:
    print('PASS  every row carries a frequency')

if len(human_only) < 3:
    failures.append('human-only count')
    print('FAIL  human-only rows: %d, need at least 3' % len(human_only))
else:
    weak = [i for i, cells in human_only if len(' '.join(cells)) < 40]
    if weak:
        failures.append('human-only reason')
        print('FAIL  human-only reason too thin on rows %s' % weak)
    else:
        print('PASS  %d human-only rows, each with a work-based reason' % len(human_only))

if not machine_carried:
    failures.append('machine row')
    print('FAIL  no machine-carried row: the map must show where an agent could take a step')
else:
    good = [i for i, cells in machine_carried
            if re.search(r'\b(input|prompt|source|from|reads|pulls|uses|figures|report)\b', ' '.join(cells).lower())]
    if good:
        print('PASS  machine-carried row %s names its input' % good[0])
    else:
        failures.append('machine input')
        print('FAIL  machine-carried rows name no machine or input')

role_like = [i for i, cells in enumerate(rows, 1)
             if re.search(r'\b(manager|coordinator|specialist|assistant|officer|executive)\b', ' '.join(cells).lower())]
if role_like:
    failures.append('whole job rows')
    print('FAIL  rows that read as a whole job: %s' % role_like)
else:
    print('PASS  no row reads as a whole job')

print('RESULT %s' % ('all checks passed' if not failures else 'failures: ' + ', '.join(failures)))
