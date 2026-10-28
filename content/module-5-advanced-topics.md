# Advanced orchestration

*Module 5 · about 50 minutes · artefact: `build/workflow/` with a working two-agent run*

## What you are making

A two-agent workflow that produces one real output, with the handover, the check and the failure path all
written down.

## Why it matters

One agent is a tool. Two agents that check each other is a system, and a system is what survives a busy
Tuesday. This module is where the word "orchestrator" stops being a job title and becomes a folder you built.

## The four patterns worth knowing

| Pattern | Shape | Use when | Cost |
|---|---|---|---|
| **Pipeline** | A produces, B checks, C publishes | Quality matters and errors are expensive | Slow, predictable, easiest to audit |
| **Fan-out** | One brief, many workers, one merge | Same job across many items | Cheapest per item, needs a merge rule |
| **Critic** | A drafts, B attacks it, A revises | Writing, decisions, anything persuasive | Two to three times the tokens |
| **Router** | One agent decides which specialist handles it | Mixed intake, different skills | Needs a reliable classifier |

Start with a pipeline. It is the only pattern that is easy to debug at two in the morning.

## How two agents actually talk in Hermes

Three mechanisms, in order of how much machinery they need:

1. **Skill handover**: the same agent switches skill. Cheapest, shares memory, no isolation. Good for a
   pipeline inside one job.
2. **Profile handover**: one profile calls another with `hermes --profile other -z "<brief>"`. Real isolation:
   separate memory, separate rules, separate keys. Good when the second agent must not see everything.
3. **Delegation**: the lead agent spawns subagents for parallel work and receives only their summaries. Good
   for fan-out, useless for anything needing continuity.

Whichever you choose, two things must be explicit or the system will quietly lie to you: **what the receiving
agent is told** (a brief, not the whole transcript) and **what counts as done** (a check, not a claim).

:::callout warn The handover failure that looks fine
Agent A writes a brief that says "improve this", agent B improves something else, and both report success.
The brief is the contract: name the input file, the output file, the format, and the check B must run before
it replies. If B cannot run the check, B must say so rather than approve.
:::

## Memory design, briefly

An orchestrated system fails at memory long before it fails at reasoning:

- **One owner per fact.** If two agents both write "the client is angry", you have two versions and no truth.
- **Summaries beat transcripts** across handovers. Send the decision, the constraint and the artefact path.
- **Write down the failure**, not just the fix. The next run needs to know what went wrong last time.

## Evaluation: how you know it still works

Three levels, cheapest first:

1. **Smoke test**: one prompt per agent, every time you change a rule. Thirty seconds.
2. **Regression battery**: ten fixed inputs with known-good outputs, run monthly. Catches drift after model
   updates, which are the changes nobody tells you about.
3. **Human review**: one real output a week, read properly by a person who would be embarrassed to ship rubbish.

:::callout ok The number that matters
A workflow whose failure rate you have never measured is not a workflow, it is a hope. Ten runs, counted
honestly, tells you more than any benchmark.
:::

## Your turn

- [ ] Choose a pipeline: producer, checker, publisher, in `build/workflow/`
- [ ] Write `brief.md`: what the producer receives, what it must output, where the file goes
- [ ] Write `check.md`: the exact check the checker runs, and what it does on failure
- [ ] Build it with one skill handover or one profile handover, and run it once end to end
- [ ] Run it a second time deliberately broken, and record what the checker did
- [ ] Write ten fixed test inputs for the monthly battery

## The check

The agent reads the folder and confirms:

1. `brief.md` names input, output, format and the check the receiver must run.
2. `check.md` is executable by a machine, or clearly marked as a human step with a name attached.
3. A full run's output exists on disk, from both agents, with timestamps.
4. The deliberately broken run is recorded, including whether the checker caught it.
5. Ten test inputs exist for the regression battery.

Failure signs: a brief that says "make it better", a checker that only agrees, or a broken run quietly
deleted from the folder.

## Sealed when

`build/workflow/` passes the five checks and the pattern name, the agent count and the failure rate from your
two runs are recorded in your progress file.
