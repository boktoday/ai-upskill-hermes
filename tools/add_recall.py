"""Add a recall opener to each lesson: three questions from the previous lesson.

Active recall before new material, and the interleaving comes free because the questions reach back
a lesson rather than repeating the last paragraph.
"""
import pathlib
import shutil

REPO = pathlib.Path('C:/Users/insig/figures/orchestrator-agent-repo/skills/orchestrator-course/references')
PROFILE = pathlib.Path('C:/Users/insig/AppData/Local/hermes/profiles/ai-upskill/skills/build-course/references')

RECALL = {
    1: ('Before you start', [
        'Name the last task you did today that took more than ten minutes.',
        'Which part of it was reading or typing, and which part was deciding?',
        'Who checks your work now, and how do they know it is right?',
    ]),
    2: ('Recall', [
        'How many rows did your task map hold, and which one were you least sure about?',
        'Name one machine-carried row and the input it needs to do its work.',
        'Which human-only reason would a sceptical manager challenge first?',
    ]),
    3: ('Recall', [
        'Which of the four headings on your rules card was hardest to fill in honestly?',
        'What did your redaction pass change, and what did it almost miss?',
        'Where does your employer line come from: policy, a person, or your own reading?',
    ]),
    4: ('Recall', [
        'What are your three commitments, with their dates?',
        'What did you write on the stop-doing line?',
        'Which commitment is most at risk in the next seven days, and why?',
    ]),
    5: ('Recall', [
        'In one line, what is the difference between a prompt and the context around it?',
        'Which three terms from your glossary do you still use loosely?',
        'What does context mean in your own job, in your own words?',
    ]),
    6: ('Recall', [
        'Which two requests triggered the skill you installed?',
        'Which words in the description did the routing?',
        'Where does the key live, and where must it never appear?',
    ]),
    7: ('Recall', [
        'What is your skill description, trigger first?',
        'What failure did the test find, and what did you change?',
        'Which step did you have to rewrite as an imperative?',
    ]),
    8: ('Recall', [
        'What does your mini app do, in one line a stranger would understand?',
        'What broke at phone width, and what did you change?',
        'Has anybody other than you used it, and what did they do with it?',
    ]),
    9: ('Recall', [
        'What single command runs your chore from a clean terminal?',
        'Where is the human step, and what does it block?',
        'What did the log record that you would have missed by hand?',
    ]),
    10: ('Recall', [
        'Which card on your portfolio was hardest to write without adjectives?',
        'Which link did you have to fix, and how did you find it?',
        'What date is on the oldest card, and is it honest?',
    ]),
    11: ('Recall', [
        'Which status code did you see first, and what did it tell you?',
        'Which part of the call was the permission, and which was the address?',
        'What did the failure teach you that the documentation did not?',
    ]),
    12: ('Recall', [
        'What event fired, and what was actually in the body?',
        'Which field did you decide was noise, and why?',
        'What could that trigger have destroyed if it had fired twice?',
    ]),
    13: ('Recall', [
        'Write your schedule in five fields, then in plain English with the timezone.',
        'Which run was on time, and which did you start by hand?',
        'What makes the job safe to run twice?',
    ]),
    14: ('Recall', [
        'Which claim on the portfolio had no row in your verification log?',
        'Which check could a stranger run without asking you anything?',
        'What failure did you record, and what did it change?',
    ]),
    15: ('Recall', [
        'Name the three drills and the symptom of each.',
        'Which fix did you re-test, and did it hold?',
        'What would you deliberately break next?',
    ]),
}


def section(title, questions):
    lines = ['## %s' % title,
             'Answer in a line each, out loud or here, before the new material. Retrieval first, teaching second.',
             '']
    for i, q in enumerate(questions, 1):
        lines.append('%d. %s' % (i, q))
    lines.append('')
    return '\n'.join(lines)


def main():
    for n in range(1, 16):
        f = REPO / ('lesson-%02d.md' % n)
        text = f.read_text(encoding='utf-8')
        if '## Recall' in text or '## Before you start' in text:
            print('skip %02d (already has an opener)' % n)
            continue
        lines = text.splitlines()
        insert_at = 2 if len(lines) > 2 and lines[1].startswith('*') else 1
        block = section(*RECALL[n]).splitlines()
        out = lines[:insert_at] + [''] + block + lines[insert_at:]
        f.write_text('\n'.join(out) + '\n', encoding='utf-8')
        print('%02d +%s' % (n, RECALL[n][0]))
    for n in range(1, 16):
        src = REPO / ('lesson-%02d.md' % n)
        dst = PROFILE / ('lesson-%02d.md' % n)
        if dst.exists():
            shutil.copyfile(src, dst)
    print('profile copies updated')


if __name__ == '__main__':
    main()
