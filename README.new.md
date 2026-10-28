# AI Upskill: the course pack

The reading behind the free AI Orchestrator agent. Five modules, fifteen lessons, twenty-one pages, six short
walkthrough videos and a set of fixed checkers. Read it on a laptop with no internet connection, print it, or
let the agent walk you through it.

Free, and it stays free.

## This pack and the agent

Two repositories, one course.

- **[ai-orchestrator-agent](https://github.com/boktoday/ai-orchestrator-agent)** is the agent. Install that if
  you want to be taught: it demonstrates a task, hands it over, then checks your file against a fixed standard
  before it will mark anything done.
- **This repository** is the material. The same five modules as pages you can read, print or hand to someone
  else, plus the checkers and the build tools.

You do not need this pack to take the course, and you do not need the agent to read it. Most people will want
both.

## What is inside

| Path | What it is |
|---|---|
| `pages/` | Twenty-one self-contained pages: a course map, five module pages, fifteen lesson pages. One stylesheet, no tracking, no network calls. |
| `content/` | The five modules as markdown, if you would rather read plain text or translate it. |
| `video/` | Six silent walkthroughs, one per module plus the course map. |
| `coach/` | The fixed checkers and their specs. This is the part that stops an agent marking its own homework. |
| `tools/` | The renderer, the video builder and the page screenshots. |

## Read it

Open `pages/index.html` in any browser. That is the whole installation. Every page is one file with its styles
inline, so the pack works from a USB stick, on a train, or on a locked-down work laptop with no admin rights.

To keep a copy: print any page to PDF. The pages are set for A4 and use a print stylesheet.

A phone needs a web address rather than a folder, so if you want to read on a phone, host `pages/` anywhere
static (GitHub Pages, Netlify, Vercel, any web server) and open the URL. Nothing in the pages calls home, so
hosting costs nothing beyond the file host.

## The five modules

1. **The agentic revolution.** What a model, a tool, a memory and a loop actually are, and the ability ladder
   from retrieve to act. Artefact: your task map.
2. **AI literacy.** Tokens, context, sampling, and how to write a prompt you can check. Artefact: your prompt
   library.
3. **Building agents.** A profile, a soul, rules, skills, tools, a scheduled job, and three tests before you
   trust any of it. Artefact: your own agent.
4. **Strategy and ethics.** Value in hours and dollars, a risk register, a disclosure rule, and the parts of
   your work that should stay human. Artefact: a business case.
5. **Advanced orchestration.** Four patterns, two handover mechanisms, and an honest failure rate. Artefact:
   a two-agent workflow that runs.

## Why the checks are fixed

An agent that writes its own test will pass it. We watched that happen: two lessons were sealed as complete,
then failed an independent checker on missing detail. So every lesson now has a spec in `coach/specs/` and one
read-only script, `coach/check.py`, that reads your artefact and prints PASS or FAIL per rule. The agent may run
it and quote it. It may not edit it.

Run it yourself at any time:

```
python coach/check.py 1          # checks position/tasks.md against lesson 1
python coach/check.py --list     # every lesson and the artefact it expects
```

Each check names the file, the rule, and what would fix it. No account, no upload, no scoring service: your
work never leaves your machine.

## What it is not

Not a certificate, not an accredited qualification, and not a promise about your job. It is task-level
literacy: what in your work an AI can carry, what it can draft while you check, and what should stay yours.

## Cost

The pack is free. If you use the agent, you pay your own model usage, typically a few dollars a month for
coursework. The agent can run on free model tiers; it is slower and less reliable there, and the course says so
plainly.

## The Saturday

The agent and this pack are free and always will be. The only paid thing is a live Saturday build with Brendan,
capped at fifteen people, where your portfolio gets reviewed by a human and you leave with it published. The
course mentions it once, in the last lesson, and never pushes. Nothing here depends on you buying it.

More at [aiorchestrator.com.au](https://www.aiorchestrator.com.au/).

## Licence

Text and pages: CC BY-SA 4.0, so you may copy, translate and teach it, with credit and under the same terms.
Code in `tools/` and `coach/`: MIT. See [LICENSE.md](LICENSE.md).

## Provenance

Everything in `content/` was written for this Hermes edition in October 2026. What came before it, and what was
replaced, is recorded in [PROVENANCE.md](PROVENANCE.md). The field-test results, including the rounds that
failed, are in [FIELD-TESTS.md](FIELD-TESTS.md).
