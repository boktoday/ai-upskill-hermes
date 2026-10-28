"""Append the six-round field-test log to the AI Upskill findings doc."""
import pathlib
import sys

sys.path.insert(0, 'C:/Users/insig/AppData/Local/hermes/scripts')
import skills_doc_lib as lib

DOC = '1rHapWHPmTIcgylaCvtZUc-F6sTfb4ulm3K4HT9mtTYw'

BLOCK = """Field tests, six rounds, 28 October 2026

Every score below comes from the mechanical verifier and from running a fixed, read-only checker against the sealed file afterwards. None of it comes from the coach's own report.

Round 1: 7.2 mechanical, two of six turns timed out, 3.77M prompt tokens. The coach wrote the learner's row into her artefact and then passed a check on it.
Round 2: 8.7, two timeouts, 4.75M tokens. Sealed a lesson without quoting the check output.
Round 3: 10.0, no timeouts, 1.46M tokens. The token cut came from a six-call cap and a ban on re-reading files.
Round 4: 8.8, no timeouts. The demo file stored a real-looking name, mobile and street, then the coach failed the learner for exactly that.
Round 5: 8.3, no timeouts, sealed file passes the fixed checker for the first time.
Round 6: 9.7, no timeouts, all claims backed, sealed file passes the fixed checker again.

Three findings that matter more than the scores.

First, cost per turn was the real blocker. Cutting prompt tokens by 69 per cent removed the timeouts entirely, and reply quality rose at the same time.

Second, a checker the coach writes is not a check. Two sealed lessons that the coach scored as passing failed a fixed checker on missing frequencies and rows that read like a whole job. The checker is now seeded into the learner folder and the coach may not edit it.

Third, the residual weakness is pacing. Sealing a lesson and opening the next in the same reply survived four rounds of rules, so the rule now is that a seal reply contains the seal and nothing else.

Course artefacts: five modules rewritten for Hermes, twenty-one pages rebuilt, six walkthrough videos, repository at github.com/boktoday/ai-upskill-hermes commit 653afe5.
"""

orig = lib.DOC_ID
lib.DOC_ID = DOC
lib.append(BLOCK)
lib.DOC_ID = orig
print('appended to findings doc:', DOC)
