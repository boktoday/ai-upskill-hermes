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
        {'type': 'absent', 'file': 'position/tasks.md', 'patterns': [r'important to me', r'because it matters'],
         'label': 'no human-only reason is "it matters to me"'},
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
        {'type': 'has_any', 'file': 'position/pathway.md', 'any_of': ['stop doing', 'stop-doing', 'i will stop'],
         'label': 'the plan has a stop-doing line'},
    ]),
    4: ('The words that get work done', 'language/my-glossary.md', [
        {'type': 'rows', 'file': 'language/my-glossary.md', 'min': 20, 'max': 60, 'label': 'twenty terms'},
        {'type': 'col', 'file': 'language/my-glossary.md', 'headers': ['in my words', 'meaning', 'definition', 'what it means'], 'min_chars': 20,
         'label': 'every term has a plain-words definition'},
        {'type': 'words', 'file': 'language/my-glossary.md', 'min': 150, 'label': 'the definitions are written out'},
        {'type': 'has_any', 'file': 'language/my-glossary.md', 'any_of': ['say:', 'say ', 'in my job'],
         'label': 'entries carry a Say line from your own work'},
    ]),
    5: ('What a skill actually is', 'skills/installed.md', [
        {'type': 'rows', 'file': 'skills/installed.md', 'min': 3, 'label': 'at least three skills inspected'},
        {'type': 'col', 'file': 'skills/installed.md', 'headers': ['when', 'trigger', 'fires'], 'min_chars': 15, 'label': 'each skill says when it fires'},
        {'type': 'has_any', 'file': 'skills/installed.md', 'any_of': ['trigger', 'when', 'fires'],
         'label': 'the log talks about triggers'},
        {'type': 'present', 'file': 'skills/installed.md', 'patterns': [r'test', r'(output|outcome|result)'],
         'label': 'both test outcomes are pasted'},
        {'type': 'absent', 'file': 'skills/installed.md', 'patterns': [r'sk-[A-Za-z0-9]{16,}', r'gh[pousr]_[A-Za-z0-9]{20,}'],
         'label': 'no secret pasted into the log'},
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
        {'type': 'present', 'file': 'build/portfolio-url.md', 'patterns': [r'\bI\b'], 'label': 'written in first person'},
    ]),
    10: ('What an API is, and what it is not', 'connect/api-log.md', [
        {'type': 'urls', 'file': 'connect/api-log.md', 'min': 1, 'label': 'the API endpoint is recorded'},
        {'type': 'present', 'file': 'connect/api-log.md', 'patterns': [r'\b(200|201|400|401|403|404|429|500)\b'],
         'label': 'a real status code is recorded'},
        {'type': 'present', 'file': 'connect/api-log.md', 'patterns': [r'(error|fail|wrong|broken)'],
         'label': 'one failure is recorded with its cause'},
        {'type': 'absent', 'file': 'connect/api-log.md', 'patterns': [r'sk-[A-Za-z0-9]{16,}'],
         'label': 'no key value in the log'},
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
        {'type': 'present', 'file': 'connect/event-log.md', 'patterns': [r'(payload|body)'],
         'label': 'the payload is shown, not described'},
        {'type': 'absent', 'file': 'connect/event-log.md', 'patterns': [r'(auto-?send|auto-?delete|auto-?pay)'],
         'label': 'nothing destructive is wired without a human step'},
    ]),
    12: ('Clocks: what a cronjob is', 'automate/<job>/', [
        {'type': 'files', 'glob': 'automate/*/*', 'min': 2, 'label': 'the job folder holds files'},
        {'type': 'files', 'glob': 'automate/*/*log*', 'min': 1, 'label': 'a run log exists'},
        {'type': 'has_any', 'file': 'automate/*/*log*', 'any_of': ['06:', '07:', 'AM', 'PM', 'cron', 'daily'],
         'label': 'the log shows when it ran'},
        {'type': 'has_any', 'file': 'automate/*/*log*', 'any_of': ['UTC', 'AEST', 'AEDT', 'local', 'timezone'],
         'label': 'the timezone is named'},
        {'type': 'dates', 'file': 'automate/*/*log*', 'min': 2, 'label': 'two runs are logged'},
        {'type': 'present', 'file': 'automate/*/*log*', 'patterns': [r'(fail|error|missed|did not run)'],
         'label': 'one deliberate failure is recorded'},
    ]),
    13: ('Verify before you trust', 'guardrails/verification.md', [
        {'type': 'rows', 'file': 'guardrails/verification.md', 'min': 3, 'label': 'at least three verification steps'},
        {'type': 'col', 'file': 'guardrails/verification.md', 'headers': ['how i check', 'how you check', 'check'], 'min_chars': 12,
         'label': 'each step says how you check it'},
        {'type': 'has_any', 'file': 'guardrails/verification.md', 'any_of': ['fail', 'wrong', 'catch'],
         'label': 'the table says what failure looks like'},
        {'type': 'absent', 'file': 'guardrails/verification.md', 'patterns': [r'reviewed by me'],
         'label': 'no check is "reviewed by me"'},
    ]),
    14: ('Failure drills', 'guardrails/drills.md', [
        {'type': 'rows', 'file': 'guardrails/drills.md', 'min': 2, 'label': 'at least two drills run'},
        {'type': 'col', 'file': 'guardrails/drills.md', 'headers': ['what happened', 'result', 'outcome'], 'min_chars': 15, 'label': 'each drill records what happened'},
        {'type': 'words', 'file': 'guardrails/drills.md', 'min': 100, 'label': 'written up, not a tick list'},
        {'type': 'present', 'file': 'guardrails/drills.md', 'patterns': [r'(symptom|cause|check)'],
         'label': 'each drill records symptom, cause and check'},
    ]),
    15: ('Ship and tell', 'build/account.md', [
        {'type': 'urls', 'file': 'build/published.md', 'min': 2, 'label': 'portfolio and profile URLs recorded'},
        {'type': 'words', 'file': 'build/account.md', 'min': 180, 'max': 220, 'label': 'the account is 180 to 220 words'},
        {'type': 'present', 'file': 'build/account.md', 'patterns': [r'(cannot|can not|did not)'],
         'label': 'the cannot line is present'},
        {'type': 'has_any', 'file': 'build/account.md', 'any_of': ['next', 'shipped', 'going to'],
         'label': 'the account looks forward'},
    ]),
}


MANUAL = {
    2: ['The before and after are the same real document, not two invented ones.'],
    3: ['The three dates are in your calendar, not just on the page.'],
    4: ['At least three terms come from the agent section: skill, tool call, verification, guardrail.'],
    5: ['You can say which words in the description did the routing.'],
    6: ['The skill fires on both requests after the fix, tested live.'],
    7: ['The URL loads with no console errors, is usable at 390px, and the one interaction completes a real task.'],
    8: ['The guardrail is a step, not a comment.'],
    9: ['Every card says what you did, in first person, without adjectives, and the page works at phone width.'],
    10: ['Two real calls were made, and you can say which part of the call was permission and which was the address.'],
    11: ['Two fields are identified as meaningful and one as noise, and you know why.'],
    12: ['One run was on time and one started by hand.'],
    13: ['Every claim on the portfolio has a row, and the page now matches the log.'],
    14: ['Each failure was actually caused, not read about, and nothing real was harmed.'],
    15: ['Every claim is supported by a link that loads, and the account is on the portfolio.'],
}


def main():
    for lesson, (title, artefact, checks) in SPECS.items():
        spec = {'lesson': lesson, 'title': title, 'artefact': artefact, 'checks': checks,
                'manual': MANUAL.get(lesson, [])}
        p = OUT / ('lesson-%02d.json' % lesson)
        p.write_text(json.dumps(spec, indent=1), encoding='utf-8')
        print('%2d  %-40s %d rules' % (lesson, artefact, len(checks)))
    print('specs written:', len(SPECS))


if __name__ == '__main__':
    main()
