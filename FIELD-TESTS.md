# Field test log

Written from the harness runs of 28 October 2026. Every number below comes from `verify.py` and from running
`coach/check.py` against the sealed file afterwards, not from the coach's own report.

| Round | Mechanical | Grader | Failed turns | Prompt tokens | Fixed checker on the sealed file |
|---|---|---|---|---|---|
| 1 | 7.2 | 20/20 | 2 | 3.77M | not run (no seal survived) |
| 2 | 8.7 | 19/20 | 2 | 4.75M | fail (row frequency) |
| 3 | 10.0 | 20/20 | 0 | 1.46M | fail (2 rows no frequency, 1 role-like row) |
| 4 | 8.8 | 19/20 | 0 | - | fail (1 row no frequency) |
| 5 | 8.3 | 20/20 | 0 | - | all checks passed |
| 6 | 9.7 | 19/20 | 0 | - | all checks passed |

## What the rounds proved

1. **Cost per turn was the real blocker.** 4.75M prompt tokens per six-turn round produced two timeouts;
   the tool-call cap and the ban on re-reading cut it to 1.46M and the timeouts stopped. A slow model plus
   a chatty profile is a reliability problem long before it is a quality problem.
2. **A checker the coach writes is not a check.** Two seals that the coach scored as passing failed a fixed,
   read-only checker: rows with no frequency, rows that read like a whole job. From round five the checker is
   seeded by the harness and the coach may not touch it.
3. **The demo is the standard.** Round four's demo file contained the exact failure (a stored name, mobile and
   street) that the coach then failed the learner for.
4. **Pacing is the residual weakness.** Sealing a lesson and opening the next in the same reply survived four
   rounds of rules. The rules now say a seal reply contains the seal and nothing else, and one ask per reply.

## How to re-run

```
python harness.py --profile ai-upskill --days 2 --turns 3 --tag <name>
python verify.py runs/<name>
cd runs/<name>/home/<folder> && python coach/check.py
```
