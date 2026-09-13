# The acceptance bar

Two separate checks decide whether a task is accepted, and passing one does not
help with the other:

- **Technical validity.** The question is original and self-contained, the answer
  is right, the evidence supports it, the rubric grades what the question asked.
- **Measured difficulty.** The task is hard for the designated model under the
  conditions Askable runs.

A beautifully built task that a model answers correctly is rejected. A hard task
whose answer is wrong is rejected faster.

## 1. The contamination probe — do this first, it is free

Paste the question into a frontier chat model. **No repository access, no
attachments, no follow-up turns.** Record the model, its version, the date, and
the model's full answer. Grade that answer against your intended required facts.

If the no-access model gets the required facts, the question is answerable from
general knowledge or from source the model has memorised. **The task is dead.**
Say so in the proposal and propose a different question. Do not argue that the
model was lucky, and do not patch the question by adding formatting requirements
the model happens to miss.

This is the single cheapest filter in the process — one message, no API key, no
container — and it catches the most common way a SWE Q&A task fails. It also
answers the Contamination Risk section the buyer requires, which is why the
record is mandatory rather than advisory.

**Run it for private repositories too.** A model cannot have memorised code it
has never seen, so the probe cannot fail for that reason — but it can still fail,
and when it does it is telling you something worse. If a model answers your
question without the code, the question is about general programming knowledge
rather than about your codebase, and privacy will not save it. That is the more
common failure for owned code, not memorisation.

**Public availability is not the test.** A public repository is not automatically
contaminated and a niche one is not automatically clean. The probe is the test.
That said, prefer approved, less widely studied projects you know well: they
start further from the training distribution, and the probe is more likely to
come back clean.

## 2. Where this bar comes from

Three reference points. The bar below is set against them rather than invented,
and it is worth ten minutes before you spend fifteen hours.

### SWE-QA — Peng et al., September 2025

The first academic benchmark for this task type: 576 question-answer pairs mined
from GitHub issues across 11 repositories. **No container and no execution.** The
agent gets `ReadFile`, `GetRepoStructure`, a RAG-backed search, and `cat`/`grep`.
Answers are scored by a GPT-5 judge across five dimensions — correctness,
completeness, relevance, clarity, reasoning — on a 5-point scale, alongside three
human engineers on a 10-point scale.

*What to take from it:* this is the floor, and its weakness is the judging. A
scalar score across five dimensions cannot tell you whether a specific fact was
established. That is why we grade binary criteria instead.

[arXiv 2509.14635](https://arxiv.org/abs/2509.14635)

### SWE-QA-Pro — Cai et al., March 2026

The same idea rebuilt on long-tail repositories with executable environments
repurposed from SWE-Rebench, which ships a Docker recipe per task. The agent gets
scoped file and directory inspection plus *constrained read-only* command-line
actions. Validation is triple: an agent answering inside the sandbox, human
annotators independently exploring the codebase, then an LLM judge.

*What to take from it:* their difficulty calibration filters out questions
"solvable via memorization or pretraining artifacts", keeping only those that
require genuine codebase interaction. That is §1 of this document, arrived at
independently, and it is why the contamination probe is mandatory rather than
advisory.

[arXiv 2603.16124](https://arxiv.org/abs/2603.16124)

### SWE Atlas Codebase Q&A — Scale

The production benchmark closest to what we are building, and the one that
actually sets the bar.

**Its environments.** Engineers "build a reproducible Docker image pinned to a
specific commit, with all dependencies pre-installed, such that the software can
be built, run, and tested". At evaluation the agent works inside that container
with the repository mounted and standard shell tools, builds and runs the
software, runs experiments, and then answers.

**Its questions.** "Simple codebase exploration is insufficient to solve these."
They "require running the software, tracing execution across multiple files, and
synthesizing findings."

**Its grading.** Human-written rubrics averaging 12.3 criteria, each scored met
or unmet independently by an LLM judge, with three experts reviewing every rubric
before it is used.

[labs.scale.com/leaderboard/sweatlas-qna](https://labs.scale.com/leaderboard/sweatlas-qna)

### What follows, and why this repository looks the way it does

- **Rubrics are binary and hand-written, 10 to 15 criteria.** That is the
  production reference, not the papers. `AUTHORING.md` §8.
- **Execution is a difficulty mechanism, not a verification aid.** The hardest
  questions in this task type are hard because reading is not enough. This is the
  reason `source-only` mode is narrow rather than a general convenience —
  `AUTHORING.md` §4.
- **The frontier sits around 63%.** The best models resolve roughly that share of
  SWE Atlas Codebase Q&A tasks. A question a strong model answers first time is
  worth nothing to us, and building ones a Flash-class model misses is genuinely
  above the public state of the art.

One caveat on that last number, so nobody quotes it loosely. SWE Atlas counts a
task resolved only when the answer meets **every** rubric item. We let a task
pass on its required criteria and treat optional ones as diagnostic, so our pass
rates and theirs are not directly comparable.

## 3. What makes a question hard for the right reasons

Hard because the answer takes investigation:

- It crosses components, execution paths, or dependencies. A single symbol lookup
  or a quotation from the documentation does not settle it.
- The obvious reading is wrong, and the thing that makes it wrong is somewhere
  else in the codebase.
- Two competent engineers could reach different conclusions from a partial read,
  and the source settles it.
- Runtime behaviour contradicts what the names and the structure suggest.

Hard for the wrong reasons — these get returned:

- **Ambiguity.** The question can be read two ways and the rubric grades one of
  them.
- **Arbitrary formatting.** Difficulty manufactured from output shape, length
  limits, or a required phrasing.
- **Withheld context.** Facts the participant cannot discover from the supplied
  environment.
- **Broken environments.** Missing dependencies, an artificially short timeout, a
  container that needs the network.
- **Trivia.** A fact that is hard to find and uninteresting once found.
- **Undocumented intent.** "Why did the author choose this design?" with no
  supplied documentation that answers it.

The test to apply to yourself: if a model fails your task, will the transcript
show it reasoning competently and reaching a wrong conclusion, or will it show it
guessing at what you wanted? Only the first is worth anything.

## 4. What Askable measures, and what you do not have to

Askable supplies the target model, agent, budget, judge and eligibility rules for
each batch, and runs the authoritative calibration. **Those parameters are not in
this repository and are not stable between batches** — the target moved two point
releases in eight days during the terminal-task pilot. Do not hard-code a model
into your task, your rubric, or your notes. Do not copy the terminal-task
calibration pin: a result measured under different conditions is a self-check,
not acceptance evidence.

Your own three attempts (§5) are a kill screen, not a measurement. Askable's run
is the measurement.

**A low success rate is only valuable when the task and the grading are sound.**
Zero passes triggers investigation; it is not automatic acceptance. Failure
review asks which of these produced the failure: a real reasoning limitation,
ambiguity in the question, missing context, broken execution, or a grading error.
Only the first one counts.

## 5. The self-check: three attempts, three graded answers

**Required before submission.** Run the task at least three times with an agentic
coding tool and grade every answer against your own rubric, criterion by
criterion. Record it in `calibration/self-check.json`; the validator will not
pass a task without it.

Gemini 3.8 Flash is currently free in Gemini CLI and Antigravity, which is why
this is a requirement rather than a suggestion. Use whatever you already have —
Claude Code, Cursor, Codex CLI, an API you already pay for. The tool matters less
than the discipline.

### What the three attempts are for, and what they are not for

**They are not a difficulty measurement.** Three attempts cannot separate a 20%
success rate from a 50% one, which is the only distinction that matters, and the
agent you ran is not the harness Askable calibrates with. Never report your
fraction as a difficulty estimate.

They are a kill screen, read like this:

| Attempts passing | What it means |
|---|---|
| 3 of 3 | Too easy. Do not submit. Fix the question or replace it. The validator fails this. |
| 2 of 3 | Probably too easy. Expect it back. Fix it first. |
| 0 or 1 of 3 | Proceed. This is not evidence that the task is hard, only that it is not obviously easy. |

**The real payoff is the grading, not the fraction.** Grading three unfamiliar
answers against your own rubric is the best rubric test available to you, and it
is where most rubric defects surface: a criterion two people read differently, a
`pass_condition` that turns out to be about phrasing, an essential fact nothing
grades. Finding those here costs an hour. Finding them at review costs a round
trip.

And when an attempt fails, **that answer belongs in
`evaluation/grading-examples.json`**, labelled `flawed_agent_<what it got
wrong>`. An authentic wrong answer tests a rubric far better than one you wrote
yourself, because you did not construct it with your own criteria in mind. The
validator warns when a failed attempt has not been harvested this way.

### Write the rubric first

Commit `evaluation/rubric.json` **before** you run the self-check, and let the
commit history show that order. It is the control that keeps this honest: an
author who runs the agent first and writes criteria afterwards will write
criteria the agent happens to fail, which manufactures difficulty rather than
measuring it. We read the commit history.

Changing the rubric after a self-check is fine and often correct — clarify an
ambiguous `pass_condition`, add an `acceptable_alternative` the agent found.
Deleting a criterion the agent met, or adding one because it missed something the
question never asked for, is not.

### Do not tune to a model

The batch target, agent, budget and judge come from Askable and are not stable
between batches — the terminal-task target moved two point releases in eight
days. Do not hard-code a model into your task, your rubric, or your notes, and do
not copy the terminal-task calibration pin. A result measured under different
conditions is a self-check, not acceptance evidence.

### Disclose everything

`calibration/self-check.json` records the agent, the exact model version string
the tool reports, the date, the task revision, the budget, every answer produced
in full, and your per-criterion score for each. `authoritative` is always
`false`.

Record discarded attempts and why. Undisclosed runs are treated as concealment,
not oversight.

## 6. Return and rejection

A task comes back for: a missing or incorrect answer; facts the participant
cannot discover; a copied or lightly rewritten question; unresolved source
permissions; a broken environment; answer or rubric leakage into the participant
image; ambiguous or redundant criteria; undisclosed AI assistance; or
insufficient difficulty under the assigned evaluation.

A judge error puts calibration on hold until it is corrected — a task is never
rejected for a grading fault that is ours.

Passing your own checks is submission readiness. It is not acceptance.
