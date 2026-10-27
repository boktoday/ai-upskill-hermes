# Building agents in Hermes

*Module 3 · about 50 minutes · artefact: `build/my-agent/` with a working profile*

## What you are making

A working agent of your own: a profile folder with a soul, operating rules, two skills and a scheduled
job, plus the three tests that prove it does what you claim.

## Why it matters

Anyone can prompt a chat window. Almost nobody can hand another person a folder that behaves like a
competent colleague on Monday morning without them present. That folder is the whole difference between
using AI and orchestrating it.

:::callout note A word about the old edition
Earlier versions of this module taught a different product's four-file agent model. Hermes works
differently: an agent is a profile, its abilities are skills, and its hands are tools. This module is
rewritten for Hermes and every command here runs on the machine you are reading this on.
:::

## The anatomy of an agent

Four things, and only four:

| Part | What it is | Where it lives |
|---|---|---|
| **Profile** | The agent's own world: settings, sessions, memory, skills | `~/AppData/Local/hermes/profiles/<name>` |
| **Soul** | Who it is, how it talks, what it refuses | `SOUL.md` in the profile |
| **Operating rules** | How it works day to day: read this first, never do that | `AGENTS.md` in the profile |
| **Skills** | What it can actually do, one folder each | `skills/<skill-name>/SKILL.md` |

Everything else, memory, cron jobs, model keys, is configuration. If you have those four, you have an
agent. If you are missing any of them, you have a chatbot with a personality.

## The soul is a contract, not a costume

A SOUL that says "you are a friendly assistant" produces exactly the assistant everyone else has.
A SOUL worth writing contains the things that would otherwise be negotiable every session:

- One job, in one sentence. Not five.
- The order it works in: read progress, demo, hand over, check, record.
- What it refuses, and why. "Never mark work complete without running the check" is worth more than
  three paragraphs about being helpful.
- How long a reply is. If you do not say, you get half a page.

:::callout ok Worked example
The free coach in this course refuses to seal a lesson until the learner's file exists and the four
checks pass, and it quotes the check output when it seals. That single rule produced the only
field-test result that mattered: twelve turns, no false completions.
:::

## Skills: how an agent learns a job

A skill is a folder with a `SKILL.md`. The frontmatter decides whether it ever fires:

```
---
name: invoice-triage
description: Use when an invoice needs checking against a purchase order.
---
```

Two rules that decide whether your skill works:

1. **The description is the trigger.** It is the only thing the agent sees before deciding. Write the
   situation, not the topic: "Use when a supplier invoice disagrees with the PO", not "invoice stuff".
2. **The body is a procedure, not an essay.** Numbered steps, exact paths, a check at the end. If a
   step can be skipped without anyone noticing, delete it or make it checkable.

Put long reference material in `references/` and point at it from the body. That keeps the skill cheap
to load and still complete.

## Hands: tools, and the limits you set

Hermes gives the agent a terminal, a file system, a browser, scheduled jobs and memory. You decide how
much of that it gets, per profile and per job.

- Start with the smallest set that does the job. A filing agent needs files, not a browser.
- Keep approvals on for anything that spends money, publishes, deletes or emails a stranger.
- Write the boundary into `AGENTS.md` in plain words, because the agent reads that file every session:
  "never send email without showing me the draft first".

## Memory: what to keep and what to refuse

An agent with memory gets better at your work and worse at protecting you, in the same motion.
The rule that keeps it useful:

- Keep **decisions and preferences**: "uses British spelling", "never quotes scripture from memory".
- Keep **state**: where the project is, what was sealed, what failed.
- Refuse **secrets and third-party personal data**. Memory is a plain file on a disk; treat it that way.

## Schedule it

A cron job turns an agent into a colleague. Three shapes worth knowing:

| Shape | Use it for | Example |
|---|---|---|
| Script only (`no_agent`) | Anything with a fixed output | Print the morning brief |
| Agent run | Anything needing judgement | Review the leads list and draft replies |
| Watcher | Anything you want silence from until it changes | CVE watch, price watch |

The discipline that separates a useful cron from spam: **silence is success**. A job that has nothing
to say should print nothing, and you should notice the quiet.

## Check it, or it is only a claim

Three tests, in this order. If any fails, the agent is not finished.

1. **Routing.** Ask it something that should fire skill A, then skill B. Does it pick correctly and say
   which it opened?
2. **Refusal.** Ask it to do the thing your `AGENTS.md` forbids. Does it decline and offer the allowed
   alternative, or does it comply and apologise?
3. **Verification.** Give it a task with a checkable outcome, and a plausible wrong answer. Does it run
   the check and report the real result, or report what sounds right?

:::callout warn The failure that looks like success
An agent that answers confidently without running the check passes every casual review and fails the
only one that counts. This is why the third test uses a deliberately plausible wrong answer.
:::

## Your turn

- [ ] Create a profile: `hermes profile create my-agent --description "<what it is for>"`
- [ ] Write `SOUL.md` with one job, the work order, two refusals and a length limit
- [ ] Write `AGENTS.md` with the files it may touch and the actions it must ask about
- [ ] Write two skills, each with a trigger-style description and a numbered procedure
- [ ] Add one cron job and make it silent when there is nothing to report
- [ ] Run the three tests and write down what each returned

## The check

The agent reads your profile folder and confirms:

1. `SOUL.md` exists, names one job, and contains at least one explicit refusal and a reply limit.
2. `AGENTS.md` exists and names both a permission and a prohibition.
3. Two skills exist, each with a `description` that starts with "Use when".
4. `hermes --profile my-agent -z "which skill would you open for <your trigger>"` names the right skill.
5. Your three test results are recorded, including any failure.

Failure signs: skills with topic descriptions ("invoices"), a soul with no refusals, or a cron job that
would speak every morning whether or not there is news.

## Sealed when

`build/my-agent/` passes the five checks and the agent has recorded the profile path, the two skill
names and the cron schedule in your progress file.
