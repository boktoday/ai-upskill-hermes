# AI Upskill, Hermes edition

The course, rebuilt so Hermes delivers it and every lesson has a page that looks like it was made on purpose.

## What is here

```
design/course.css        one stylesheet for every page: charcoal, deep pink, warm paper, squared edges
content/                 rewritten module material (module 3 is Hermes-native; the rest is converted)
tools/render.py          markdown -> HTML pages (index, 15 lessons, 5 modules)
tools/shots.py           screenshots and the printable PDF
pages/                   the built course: index.html, lesson-01..15.html, module-1..5.html
shots/                   phone and desktop screenshots, course-index.pdf
```

## Rebuild

```
python tools/render.py     # writes pages/
python tools/shots.py      # screenshots + PDF
```

No build system, no npm, no network. Each page embeds the stylesheet, so a single file is the whole lesson.

## Install the agent

The profile lives at `%LOCALAPPDATA%\hermes\profiles\ai-upskill` and carries the pages in `pages/`:

```
hermes --profile ai-upskill -z "start lesson 1"
```

Nine skills: `agentic-revolution`, `ai-literacy`, `building-agents`, `strategy-ethics`, `advanced-topics`,
`knowledge-check`, `spaced-repetition`, `project-based`, `build-course`, plus `course-pages` which maps
lesson numbers to page paths.

## The teaching contract

- The page is the textbook. The agent names the lesson, gives the page path, and says what to produce.
- The agent demos on its own material, hands over, then runs the checks against the learner's file.
- Nothing is sealed without the artefact existing and the checks passing, and the agent quotes the check output.
- Replies stay under 120 words unless the learner asks for depth.

## What is rewritten, what is converted

- **module 3, building agents**: rewritten for Hermes (profiles, skills, tools, cron). The old edition taught a
  different product's four-file agent model; that material is gone rather than find-and-replaced.
- **modules 1, 2, 4, 5**: converted from the March 2026 OpenClaw edition. Where OpenClaw mechanics remain, the
  page carries a REWRITE NEEDED banner rather than teaching them as Hermes.
- **the fifteen build lessons**: unchanged in substance, now rendered as pages with module, time and artefact chips.

## Five modules, all rewritten

Every module is now Hermes-native writing, not converted OpenClaw text. Each follows the same shape:
what you are making, why it matters, the ideas that actually matter, a warning callout about the standard
failure, a checklist handover, five or six executable checks, and a sealing rule.

| Module | Artefact | The idea it earns |
|---|---|---|
| 1 agentic revolution | `position/agent-map.md` | the ability ladder: retrieve, transform, draft, decide, act |
| 2 ai literacy | `language/prompt-library.md` | tokens, context pressure, sampling, and checkable prompts |
| 3 building agents | `build/my-agent/` | profile, soul, rules, skills, tools, cron, three tests |
| 4 strategy and ethics | `strategy/business-case.md` | value in hours and dollars, a risk register, a disclosure rule |
| 5 advanced orchestration | `build/workflow/` | four patterns, two handover mechanisms, an honest failure rate |

## Videos

`tools/video.py` scroll-captures each page and encodes a walkthrough at `video/`: one per module plus the
course map. Silent, small, and good enough to send to someone deciding whether to take the course.

## Open items

1. Model names and prices in module 2 are deliberately shape-first; refresh the specifics before each cohort.
2. Spaced repetition is specified (scheduler in `skills/spaced-repetition/references/scheduler.py`) but not yet
   wired to a cron job.
3. The pages are local files. Serving them from aiorchestrator.com.au would make them shareable; that is a
   separate publishing decision.

