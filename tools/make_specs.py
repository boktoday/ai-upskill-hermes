"""Write the fifteen lesson specs: the fixed standard each artefact is checked against."""
import json
import pathlib

OUT = pathlib.Path('C:/Users/insig/figures/upskill-hermes/coach/specs')
OUT.mkdir(parents=True, exist_ok=True)

PHONE = r'\b0\d{3}[\s-]?\d{3}[\s-]?\d{3}\b'
EMAIL = r'[\w.+-]+@[\w-]+\.[\w.]+'

SPECS = {
    1: ('Your work, task by task', 'position/tasks.md', [
        {'type': 'rows', 'file': 'position/tasks.md', 'min': 8, 'max': 12, 'label': 'row count is within 8 to 12'},
        {'type': 'col', 'file': 'position/tasks.md', 'headers': ['how often', 'frequency', 'how regular'], 'min_chars': 4, 'label': 'every row says how often'},
        {'type': 'col_any', 'file': 'position/tasks.md', 'headers': ['label'], 'any_of': ['machine', 'human', 'agent', 'ai'],
         'min_rows': 8, 'label': 'every row carries a label'},
        {'type': 'col_any', 'file': 'position/tasks.md', 'headers': ['label'], 'any_of': ['human only', 'human-only'],
         'min_rows': 3, 'label': 'at least three human-only rows'},
        {'type': 'col', 'file': 'position/tasks.md', 'headers': ['evidence', 'reason'], 'min_chars': 40, 'label': 'each row has a reason in the evidence column'},
        {'type': 'col_any', 'file': 'position/tasks.md', 'headers': ['label'], 'any_of': ['machine'], 'min_rows': 1,
         'label': 'at least one machine-carried row'},
        {'type': 'absent', 'file': 'position/tasks.md',
         'patterns': [r'\b(manager|coordinator|specialist|officer|executive)\b'],
         'label': 'no row reads as a whole job'},
    ]),
    2: ('The rules you work under', 'position/rules.md', [
        {'type': 'headings', 'file': 'position/rules.md',
         'all': ['never paste', 'employer', 'owns', 'verify'],
         'label': 'the card has all four headings'},
        {'type': 'words', 'file': 'position/rules.md', 'min': 120, 'label': 'the card is written out, not a stub'},
        {'type': 'files', 'glob': 'position/redaction-*.md', 'min': 2, 'label': 'a before and after redaction exist'},
        {'type': 'present', 'file': 'position/redaction-after.md',
         'patterns': [r'\[[^\]]+\]|<<[^>]+>>|\{[^}]+\}'],
         'label': 'the after version uses placeholders'},
        {'type': 'absent', 'file': 'position/redaction-after.md', 'patterns': [PHONE, EMAIL],
         'label': 'the after version holds no phone number or email'},
        {'type': 'absent', 'file': 'position/rules.md', 'patterns': [r'(sk-[A-Za-z0-9]{16,}|gh[pousr]_[A-Za-z0-9]{20,})'],
         'label': 'no credentials stored in the card'},
    ]),
    3: ('Your 90 day plan', 'position/pathway.md', [
        {'type': 'headings', 'file': 'position/pathway.md', 'all': ['90 day'], 'label': 'the plan is framed as 90 days'},
        {'type': 'dates', 'file': 'position/pathway.md', 'min': 3, 'label': 'three dated commitments'},
        {'type': 'has_any', 'file': 'position/pathway.md', 'any_of': ['skill', 'artefact', 'person'],
         'label': 'the plan names a skill, an artefact or a person'},
        {'type': 'words', 'file': 'position/pathway.md', 'min': 100, 'label': 'long enough to be useful'},
    ]),
    4: ('The words that get work done', 'language/my-glossary.md', [
        {'type': 'rows', 'file': 'language/my-glossary.md', 'min': 10, 'max': 60, 'label': 'at least ten terms'},
        {'type': 'col', 'file': 'language/my-glossary.md', 'headers': ['in my words', 'meaning', 'definition', 'what it means'], 'min_chars': 20,
         'label': 'every term has a plain-words definition'},
        {'type': 'words', 'file': 'language/my-glossary.md', 'min': 150, 'label': 'the definitions are written out'},
    ]),
    5: ('What a skill actually is', 'skills/installed.md', [
        {'type': 'rows', 'file': 'skills/installed.md', 'min': 3, 'label': 'at least three skills inspected'},
        {'type': 'col', 'file': 'skills/installed.md', 'headers': ['when', 'trigger', 'fires'], 'min_chars': 15, 'label': 'each skill says when it fires'},
        {'type': 'has_any', 'file': 'skills/installed.md', 'any_of': ['trigger', 'when', 'fires'],
         'label': 'the log talks about triggers'},
    ]),
    6: ('Teach your agent once', 'skills/<your-skill>/SKILL.md', [
        {'type': 'files', 'glob': 'skills/*/SKILL.md', 'min': 1, 'label': 'a SKILL.md exists'},
        {'type': 'files', 'glob': 'skills/*/test-log.md', 'min': 1, 'label': 'a test log exists'},
        {'type': 'dates', 'file': 'skills/*/test-log.md', 'min': 1, 'label': 'the test log is dated'},
        {'type': 'words', 'file': 'skills/*/test-log.md', 'min': 25, 'label': 'the test log records what happened'},
        {'type': 'frontmatter', 'file': 'skills/*/SKILL.md', 'keys': ['name', 'description'],
         'label': 'the skill declares a name and a description'},
        {'type': 'words', 'file': 'skills/*/SKILL.md', 'min': 100, 'label': 'the skill has real instructions'},
    ]),
    7: ('Your first mini app', 'build/app-url.md', [
        {'type': 'urls', 'file': 'build/app-url.md', 'min': 1, 'label': 'a live app URL is recorded'},
        {'type': 'words', 'file': 'build/app-url.md', 'min': 25, 'label': 'the note says what it does and who it is for'},
    ]),
    8: ('An agent that does a chore', 'build/chore/', [
        {'type': 'files', 'glob': 'build/chore/*', 'min': 2, 'label': 'the chore folder holds work, not an empty shell'},
        {'type': 'files', 'glob': 'build/chore/*log*', 'min': 1, 'label': 'a run log exists'},
        {'type': 'dates', 'file': 'build/chore/run-log.md', 'min': 1, 'label': 'the log is dated'},
    ]),
    9: ('Your portfolio', 'build/portfolio-url.md', [
        {'type': 'urls', 'file': 'build/portfolio-url.md', 'min': 1, 'label': 'the portfolio URL is recorded'},
        {'type': 'words', 'file': 'build/portfolio-url.md', 'min': 20, 'label': 'the note says what three things it proves'},
    ]),
    10: ('What an API is, and what it is not', 'connect/api-log.md', [
        {'type': 'urls', 'file': 'connect/api-log.md', 'min': 1, 'label': 'the API endpoint is recorded'},
        {'type': 'present', 'file': 'connect/api-log.md', 'patterns': [r'\b(200|201|400|401|403|404|429|500)\b'],
         'label': 'a real status code is recorded'},
        {'type': 'present', 'file': 'connect/api-log.md', 'patterns': [r'\{[^}]*\}'],
         'label': 'a response shape is recorded'},
        {'type': 'has_any', 'file': 'connect/api-log.md', 'any_of': ['request', 'response', 'header'],
         'label': 'the log names the request or the response'},
        {'type': 'words', 'file': 'connect/api-log.md', 'min': 100, 'label': 'written up in your own words'},
    ]),
    11: ('Connected tools and webhooks', 'connect/event-log.md', [
        {'type': 'has_any', 'file': 'connect/event-log.md', 'any_of': ['event', 'payload', 'body'],
         'label': 'the log describes the event that fired'},
        {'type': 'dates', 'file': 'connect/event-log.md', 'min': 1, 'label': 'the event is timestamped'},
        {'type': 'words', 'file': 'connect/event-log.md', 'min': 80, 'label': 'written up in your own words'},
    ]),
    12: ('Clocks: what a cronjob is', 'automate/<job>/', [
        {'type': 'files', 'glob': 'automate/*/*', 'min': 2, 'label': 'the job folder holds files'},
        {'type': 'files', 'glob': 'automate/*/*log*', 'min': 1, 'label': 'a run log exists'},
        {'type': 'has_any', 'file': 'automate/*/*log*', 'any_of': ['06:', '07:', 'AM', 'PM', 'cron', 'daily'],
         'label': 'the log shows when it ran'},
    ]),
    13: ('Verify before you trust', 'guardrails/verification.md', [
        {'type': 'rows', 'file': 'guardrails/verification.md', 'min': 3, 'label': 'at least three verification steps'},
        {'type': 'col', 'file': 'guardrails/verification.md', 'headers': ['how i check', 'how you check', 'check'], 'min_chars': 12,
         'label': 'each step says how you check it'},
        {'type': 'has_any', 'file': 'guardrails/verification.md', 'any_of': ['fail', 'wrong', 'catch'],
         'label': 'the table says what failure looks like'},
    ]),
    14: ('Failure drills', 'guardrails/drills.md', [
        {'type': 'rows', 'file': 'guardrails/drills.md', 'min': 2, 'label': 'at least two drills run'},
        {'type': 'col', 'file': 'guardrails/drills.md', 'headers': ['what happened', 'result', 'outcome'], 'min_chars': 15, 'label': 'each drill records what happened'},
        {'type': 'words', 'file': 'guardrails/drills.md', 'min': 100, 'label': 'written up, not a tick list'},
    ]),
    15: ('Ship and tell', 'build/account.md', [
        {'type': 'urls', 'file': 'build/published.md', 'min': 2, 'label': 'portfolio and profile URLs recorded'},
        {'type': 'words', 'file': 'build/account.md', 'min': 80, 'label': 'the account explains what you built and what is next'},
        {'type': 'has_any', 'file': 'build/account.md', 'any_of': ['next', 'shipped', 'going to'],
         'label': 'the account looks forward'},
    ]),
}


def main():
    for lesson, (title, artefact, checks) in SPECS.items():
        spec = {'lesson': lesson, 'title': title, 'artefact': artefact, 'checks': checks}
        p = OUT / ('lesson-%02d.json' % lesson)
        p.write_text(json.dumps(spec, indent=1), encoding='utf-8')
        print('%2d  %-40s %d rules' % (lesson, artefact, len(checks)))
    print('specs written:', len(SPECS))


if __name__ == '__main__':
    main()
