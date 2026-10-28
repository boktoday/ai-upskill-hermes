# AI literacy that survives contact with work

*Module 2 · about 45 minutes · artefact: `language/prompt-library.md`*

## What you are making

A prompt library of five reusable prompts for your own work, each with a note on which model you would use
and what would make the answer untrustworthy.

## Why it matters

You do not need to understand how a model works to use one badly. You do need three ideas, and they fit on
a card: tokens, context and sampling. Everything else you will hear this year is either a product name or
a sales claim.

## Three ideas, properly understood

**Tokens.** Models read in chunks of roughly four characters. That is why long documents get truncated, why
counting words is not the same as counting cost, and why "it forgot what I said" usually means the start of
the conversation fell out of the window rather than the model being stupid.

**Context window.** The whole working memory of one turn: your system prompt, the conversation, files,
tool output, and the answer it is writing. Everything competes for the same space. When the window fills,
the oldest material gets dropped or compressed, which is exactly when an agent starts contradicting itself.

| Window pressure | What you see | What to do |
|---|---|---|
| Comfortable | Fast, specific answers | Nothing |
| Half full | Slightly repetitive | Trim old turns, restate the goal |
| Full | Forgets constraints, invents detail | Start a fresh session with a summary |

**Sampling.** The model picks likely next words. Temperature and similar settings decide how adventurous
that picking is. Low is consistent and dull; high is varied and drifts. For work you will check, low is
better than interesting.

:::callout pink Hallucination, honestly explained
A model that has never seen your invoice has no way to know it says something false. It fills the gap with
what such documents usually contain. It is not lying, because it has no concept of a truth it could betray.
This is why every task at rung 4 or 5 needs a check that does not depend on the model's confidence.
:::

## How to ask so the answer is checkable

The shape that works, and that you can teach a colleague in two minutes:

1. **Context**: what this is, who it is for, what already exists.
2. **Objective**: one job, in one sentence.
3. **Style and tone**: three adjectives, or paste an example of the voice you want.
4. **Audience**: who reads it, and what they already know.
5. **Response format**: the shape you want back, exactly. A table with these columns. Under 200 words. No preamble.
6. **Guardrails**: what it must not do. "Do not invent figures. If a number is missing, write MISSING."

Two additions that pay for themselves immediately: ask for **the check** ("list the three claims most
likely to be wrong"), and ask for **sources** where sources are possible.

## Choosing a model in the here and now

Specific models and prices move every few months, so learn the shape, then check the current numbers:

| Job | What you need | What to avoid |
|---|---|---|
| Reading and summarising long documents | Large context, cheap input | Paying premium rates for bulk work |
| Drafting in your voice | Strong writing, your examples in the prompt | One-shotting a whole document with no example |
| Tool use and agent loops | Reliable structured output, supports tool calls | Models that invent tool names |
| Anything private | A provider whose terms you have read, or a local model | Assuming a free tier is private |

:::callout warn The dated-material warning
Any table of model names in any course is out of date within a quarter, including this one. Rewrite it with
current numbers before you teach it to anyone else.
:::

## Your turn

- [ ] Write five prompts you would genuinely reuse, in `language/prompt-library.md`
- [ ] Give each one a name, the job it does, the model you would use, and the format you expect back
- [ ] For each, write the specific thing that would make the answer untrustworthy
- [ ] Run one of them twice, once vague and once with the six-part shape, and paste both answers side by side
- [ ] Write one sentence on the difference you can actually see

## The check

The agent reads your library and confirms:

1. Five prompts, each doing a different job, each named so you could find it in six months.
2. Each has the six parts, or an explicit choice about which ones do not apply and why.
3. Each names the model and the output format.
4. Each has a real failure mode, not "it might be wrong".
5. The two-version comparison is in the file, with the vague version kept rather than quietly deleted.

Failure signs: five prompts that are the same prompt reworded, missing output formats, or a comparison whose
"before" version was written after the "after".

## Sealed when

`language/prompt-library.md` passes the five checks and the prompt names are recorded in your progress file.
