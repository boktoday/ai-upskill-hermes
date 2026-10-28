"""Prove every lesson spec discriminates: a good fixture must PASS, a broken one must FAIL.

For each of the fifteen lessons: write a realistic good artefact, run coach/check.py, expect PASS.
Then break one rule, run again, expect FAIL and record which rule caught it. Also re-run lesson 1
against the four sealed files from the field-test runs, where the verdict is already known.
"""
import json
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile

COURSE = pathlib.Path('C:/Users/insig/figures/upskill-hermes')
PY = sys.executable
CHECK = COURSE / 'coach' / 'check.py'

ROWS1 = """| # | Task | How often | Label | Evidence and reason |
|---|---|---|---|---|
| 1 | Writing the weekly promo email | weekly | machine-drafted, human-checked | I rewrite the opening line and check every price before it goes out. |
| 2 | Chasing suppliers for price lists | weekly | human only | Last Tuesday I rang three suppliers because email was not being answered. |
| 3 | Filing the shared inbox | daily | machine-carried | Machine: the Outlook rule. Input: the shared inbox. I check the leftovers. |
| 4 | Monthly sales summary slide | monthly | machine-drafted, human-checked | Takes half a day and I check every number against the spreadsheet. |
| 5 | Talking the rep through a quote | weekly | human only | The rep only gives straight answers on the phone, and I know which questions to ask. |
| 6 | Sorting supplier invoices | weekly | machine-carried | Machine: the invoice parser. Input: the invoices folder. I approve each one. |
| 7 | Updating the price list sheet | monthly | machine-drafted, human-checked | I check the margins before anyone else sees it. |
| 8 | Negotiating the freight rate | quarterly | human only | It is a relationship call and a machine cannot read the room on cost. |
| 9 | Posting the warehouse notice | fortnightly | machine-drafted, human-checked | I check names and dates before it goes on the board. |
| 10 | Reconciling the card statement | monthly | machine-drafted, human-checked | I still check the odd line myself against receipts. |
"""

GOOD = {}

GOOD[1] = ('position/tasks.md', ROWS1)

GOOD[2] = {
    'position/rules.md': """# My rules card

## Data I never paste
Client names, phone numbers, street addresses, fees and anything from a contract. If it has a person in it, it
does not go into a prompt. I use roles instead of names and ranges instead of numbers.

## What my employer says
No written policy yet, so I follow the strictest reading: nothing client-identifying leaves the building.

## Who owns what I make
The firm owns anything I make in work time on firm equipment. I keep my own course notes separate and write in
my own time for anything personal.

## How I verify
Every output gets checked against the source document before it is sent. If I cannot point to the line the
claim came from, it does not go out.
""",
    'position/redaction-before.md': """Hi, it's Dave from Bunnings on 0412 555 019, we're at 12 Smith Street, can you do the timber quote by Friday
for around $12,000?
""",
    'position/redaction-after.md': """A trade customer, contact by [phone], located in [region], wants a timber quote by Friday in the [amount] range.
""",
}

GOOD[3] = ('position/pathway.md', """# My 90 day plan

One skill I will build by 30 November 2026: writing a prompt library I actually use at work, tested on real
quotes and real customer emails rather than on exercises. I will know it works when I reach for it without
thinking and when a colleague asks me for the wording.

One artefact finished by 15 December 2026: a published portfolio page with three pieces of work on it, each
with a link that opens and a sentence about what I did rather than what I felt.

One person I will show it to by 20 December 2026: my old manager, who will tell me honestly whether it reads
like a professional wrote it. I will send it on that date whether I feel ready or not, because the whole point
is to be told what is wrong while there is still time to fix it.
""")

GOOD[4] = ('language/my-glossary.md', """# My glossary

| Term | In my words |
|---|---|
| Token | A chunk of text the model counts, roughly three quarters of a word. |
| Context | Everything the model can see in one go, prompts plus reply plus files. |
| Sampling | How the model picks the next word, which is why the same prompt differs twice. |
| Temperature | A setting that makes output safer or wilder, not smarter. |
| Hallucination | A confident sentence with nothing behind it, which is why I check claims. |
| Embedding | A list of numbers representing meaning, used for search rather than chat. |
| Tool call | The model asking the harness to do something real, like read a file. |
| Grounding | Pinning an answer to a source document instead of the model's memory. |
| Prompt | The instruction, plus the context, plus the format I want back. |
| Agent | A loop of model, tools and memory that keeps going until the job is done. |
""")

GOOD[5] = ('skills/installed.md', """# Skills I inspected

| Skill | When it fires | Why it exists |
|---|---|---|
| course-pages | When a lesson number is named | Maps lessons to page paths so links never drift |
| knowledge-check | When a learner says they are done | Runs the fixed checks and refuses to mark its own work |
| reminder | When a date is promised | Creates the scheduled job instead of saying it will |
""")

GOOD[6] = {
    'skills/quote-followup/SKILL.md': """---
name: quote-followup
description: Use when a trade quote has had no reply after three days.
---

# Quote follow-up

Read the quote file, find the date it went out, and if three working days have passed without a reply, draft a
short follow-up in the customer's own language, using the wording of the original quote rather than a template.

Never discount and never invent a delivery date. Offer two specific times for a call, leave the decision with
them, and stop after one follow-up: a second chase on the same quote is the salesperson's job, not the agent's.

If the quote file has no date, stop and say so rather than guessing from the filename. If the customer has
already replied, do nothing at all: the skill exists for silence, not for chasing people who answered.
""",
    'skills/quote-followup/test-log.md': """# Test log

2026-10-27: ran on three old quotes. Two drafted correctly. One fired early because the quote date was a Friday,
so the skill now counts working days only.
""",
}

GOOD[7] = ('build/app-url.md', """The quote calculator is live at https://quote-calc.example.com and it is for the two warehouse guys who
currently do the sums on a calculator and get it wrong about once a week.
""")

GOOD[8] = {
    'build/chore/run-log.md': """# Chore run log

2026-10-27 07:00 ran the invoice sorter against 14 invoices. Read 14, filed 13, left one for me because the
supplier name was misspelled. Took 40 seconds against about 25 minutes by hand.
""",
    'build/chore/sorter.md': """# Invoice sorter

Reads the invoices folder, pulls the supplier and the total, files by month. Stops and asks when the supplier
name is not in the list.
""",
}

GOOD[9] = ('build/portfolio-url.md', """Portfolio at https://brendan.example.com. It proves three things: I can build a page, I can write plainly
about my own work, and I finish what I start.
""")

GOOD[10] = ('connect/api-log.md', """# API log

Endpoint: https://api.example.com/v1/quotes

Request: GET with the key in the header, and a query for the last seven days.

Response came back 200 with JSON like {"quotes": [{"id": 41, "total": 1200}]}.

What I learned: the status code tells me whether the request was understood at all, before I read a single word
of the response. 401 means the key is wrong, 404 means the path is wrong, 429 means I asked too often, and 200
with an empty list means the API is fine and my filter is wrong. Two hours went on guessing at the query before
I read the code and found I was sending yesterday's key.
""")

GOOD[11] = ('connect/event-log.md', """# Event log

2026-10-27 09:14 a form submission fired the webhook. The event body carried name, email and message, and the
payload arrived as JSON rather than as form fields, which I had not expected.

I mapped the payload to a row in the sheet and the row appeared within four seconds. A duplicate submission ten
minutes later created a second row, so the event carries no de-duplication and I need to add one before this
touches a client list. Next time I will log the raw body first and map it after.
""")

GOOD[12] = {
    'automate/morning-brief/run-log.md': """# Run log

2026-10-27 daily 06:45 job fired and posted the brief. Second run 07:00 the same day skipped because the job
is set to daily only.
""",
    'automate/morning-brief/job.md': """# Morning brief job

Reads three feeds, drafts five bullets, posts to the channel. Cron set to daily at 06:45 local time.
""",
}

GOOD[13] = ('guardrails/verification.md', """# Verification steps

| Step | How I check it | What failure looks like |
|---|---|---|
| Names and numbers | Read the output against the source line by line | A number that is close but wrong, which is worse than obviously wrong |
| Quotes | Search the source for the exact phrase | A paraphrase presented as a quotation |
| Links | Click every one | A 404 on the one link the reader actually needs |
""")

GOOD[14] = ('guardrails/drills.md', """# Drills

| Drill | What I broke | What happened |
|---|---|---|
| Wrong file | I pointed the agent at last month's sheet on purpose | It summarised the wrong month confidently and only my date check caught it |
| Empty folder | I removed the source file and asked again | It invented three rows rather than saying the folder was empty |
| Bad key | I broke the API key | It reported a 401 honestly instead of retrying forever, which is the one failure it handled well |

Two of three drills failed in a way I would have shipped: a confident wrong month and three invented rows. Both
were caught by a person reading, not by the agent.
""")

GOOD[15] = {
    'build/published.md': """Portfolio: https://brendan.example.com
Agent profile: https://github.com/bokanders/quote-agent
""",
    'build/account.md': """I built a quote calculator and an invoice sorter, and I published the portfolio with three pieces of work on
it, each with a link a stranger can open. The calculator saves about forty minutes a week, measured against my
own timesheet for the four weeks before it existed.

The honest gap is that the sorter still needs a human on misspelled suppliers, which happens about once a
fortnight. Next I am going to add a supplier alias list, run it for a fortnight beside the manual process, and
only then tell anyone it works. I am also going to write the failure notes into the README, because the two
invented rows scare me more than the missing feature.
""",
}

# what to break for the negative test, per lesson
BREAK = {
    1: ('position/tasks.md', lambda t: t.replace('| 9 | Posting the warehouse notice | fortnightly | machine-drafted, human-checked |',
                                                 '| 9 | Posting the warehouse notice |  | machine-drafted, human-checked |')),
    2: ('position/redaction-after.md', lambda t: t + '\nCall me on 0412 555 019.\n'),
    3: ('position/pathway.md', lambda t: t.replace('30 November 2026', '').replace('15 December 2026', '').replace('20 December 2026', '')),
    4: ('language/my-glossary.md', lambda t: '\n'.join(t.splitlines()[:5])),
    5: ('skills/installed.md', lambda t: '| Skill | Notes | Why |\n|---|---|---|\n| course-pages | maps lessons | links |\n'),
    6: ('skills/quote-followup/test-log.md', lambda t: 'no test was run\n'),
    7: ('build/app-url.md', lambda t: 'it is live somewhere soon\n'),
    8: ('build/chore/run-log.md', lambda t: 'done\n'),
    9: ('build/portfolio-url.md', lambda t: 'portfolio coming soon\n'),
    10: ('connect/api-log.md', lambda t: __import__('re').sub(r'\b(200|201|400|401|403|404|429|500)\b', 'code', t)),
    11: ('connect/event-log.md', lambda t: 'something happened\n'),
    12: ('automate/morning-brief/run-log.md', lambda t: 'ran it\n'),
    13: ('guardrails/verification.md', lambda t: '| Step | How I check it | What failure looks like |\n|---|---|---|\n| one | ok | ok |\n'),
    14: ('guardrails/drills.md', lambda t: '| Drill | What I broke | What happened |\n|---|---|---|\n| one | nothing | nothing |\n'),
    15: ('build/account.md', lambda t: 'shipped\n'),
}


def write_tree(root, lesson):
    """Materialise a lesson's good fixture under root."""
    item = GOOD[lesson]
    files = item if isinstance(item, dict) else {item[0]: item[1]}
    for rel, body in files.items():
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(body, encoding='utf-8')
    return files


def run(root, lesson):
    r = subprocess.run([PY, str(CHECK), str(lesson)], cwd=str(root), capture_output=True, text=True,
                       env={k: v for k, v in os.environ.items() if k not in ('PYTHONPATH', 'PYTHONHOME')})
    return r.stdout


def verdict(out):
    if 'RESULT all checks passed' in out:
        return 'PASS'
    if 'RESULT failures' in out:
        return 'FAIL'
    return 'ERROR'


def main():
    tmp = pathlib.Path(tempfile.mkdtemp(prefix='specproof_'))
    results = []
    for lesson in range(1, 16):
        root = tmp / ('good%02d' % lesson)
        root.mkdir()
        files = write_tree(root, lesson)
        out = run(root, lesson)
        v = verdict(out)
        rules = out.count('\nPASS  ') + (1 if out.startswith('PASS') else 0)
        results.append((lesson, 'good', v, rules, ''))

        root2 = tmp / ('bad%02d' % lesson)
        root2.mkdir()
        for rel, body in files.items():
            p = root2 / rel
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(body, encoding='utf-8')
        target, fn = BREAK[lesson]
        p = root2 / target
        p.write_text(fn(p.read_text(encoding='utf-8')), encoding='utf-8')
        out2 = run(root2, lesson)
        caught = [l.split('  ')[1] for l in out2.splitlines() if l.startswith('FAIL')]
        results.append((lesson, 'broken', verdict(out2), 0, caught[0] if caught else 'NOTHING CAUGHT'))

    ok = True
    for lesson, kind, v, rules, extra in results:
        expect = 'PASS' if kind == 'good' else 'FAIL'
        flag = '' if v == expect else '  <-- WRONG'
        if v != expect:
            ok = False
        print('%2d %-7s %-5s %s%s' % (lesson, kind, v, extra, flag))
    print('\nall specs discriminate:', ok)
    shutil.rmtree(tmp, ignore_errors=True)
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
