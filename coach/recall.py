#!/usr/bin/env python3
"""Spaced recall for the course: day 1, day 3, week 1, week 2, month 1 after each seal.

    python coach/recall.py            everything scheduled, with dates
    python coach/recall.py --due      only what is due today
    python coach/recall.py --json     machine-readable

The agent writes recall.json when it seals a lesson: one entry per lesson, with the date and the
three questions drawn from that lesson's checks. A daily cron on the learner's own machine runs
`recall.py --due` and asks whatever is due. Nothing leaves the machine.
"""
import argparse
import datetime as dt
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
STATE = HERE.parent / 'recall.json'
OFFSETS = [1, 3, 7, 14, 30]

SAMPLE = {
    'lesson-01': {
        'sealed_on': '2026-10-28',
        'questions': [
            'Name a machine-carried row and the input it needs.',
            'Which human-only reason would a manager challenge?',
            'What does "no row is a whole job" mean in your own list?',
        ],
    }
}


def load():
    if not STATE.exists():
        return {}
    try:
        return json.loads(STATE.read_text(encoding='utf-8'))
    except Exception:
        return {}


def schedule(entry):
    try:
        base = dt.date.fromisoformat(entry['sealed_on'])
    except Exception:
        return []
    return [(base + dt.timedelta(days=d), d) for d in OFFSETS]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--due', action='store_true')
    ap.add_argument('--json', action='store_true')
    ap.add_argument('--init', action='store_true', help='write a sample recall.json')
    a = ap.parse_args()

    if a.init:
        if STATE.exists():
            print('recall.json already exists at %s' % STATE)
            return 0
        STATE.write_text(json.dumps(SAMPLE, indent=1), encoding='utf-8')
        print('wrote sample %s' % STATE)
        return 0

    data = load()
    if not data:
        print('no recall.json yet: the agent writes it when it seals a lesson')
        return 0

    today = dt.date.today()
    rows = []
    for lesson, entry in sorted(data.items()):
        qs = entry.get('questions') or []
        for when, offset in schedule(entry):
            rows.append({'lesson': lesson, 'offset_days': offset, 'due': when.isoformat(),
                         'status': 'due' if when <= today else 'later',
                         'questions': qs})

    if a.json:
        print(json.dumps(rows, indent=1))
        return 0

    due = [r for r in rows if r['status'] == 'due']
    if a.due:
        if not due:
            print('nothing due today')
            return 0
        for r in due:
            print('%s (day %d):' % (r['lesson'], r['offset_days']))
            for i, q in enumerate(r['questions'], 1):
                print('  %d. %s' % (i, q))
        return 0

    print('%d scheduled reviews across %d lessons' % (len(rows), len(data)))
    for r in rows:
        flag = 'due' if r['status'] == 'due' else '   '
        print('  %s  %-10s day %-2d  %s' % (r['due'], r['lesson'], r['offset_days'], flag))
    return 0


if __name__ == '__main__':
    sys.exit(main())
