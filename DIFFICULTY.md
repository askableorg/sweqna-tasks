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

**Public availability is not the test.** A public repository is not automatically
contaminated and a niche one is not automatically clean. The probe is the test.
That said, prefer approved, less widely studied projects you know well: they
start further from the training distribution, and the probe is more likely to
come back clean.

## 2. What makes a question hard for the right reasons

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

## 3. What Askable measures, and what you do not have to

Askable supplies the target model, agent, budget, judge and eligibility rules for
each batch, and runs the authoritative calibration. **Those parameters are not in
this repository and are not stable between batches** — the target moved two point
releases in eight days during the terminal-task pilot. Do not hard-code a model
into your task, your rubric, or your notes. Do not copy the terminal-task
calibration pin: a result measured under different conditions is a self-check,
not acceptance evidence.

An exploratory screen of three attempts is a *kill* screen, not a measurement.
Three attempts cannot separate a 20% success rate from a 50% one, which is the
only distinction that matters. Treat 3/3 as "too easy, stop" and treat 0/3 as
"worth measuring properly", and never report either as a difficulty estimate.

**A low success rate is only valuable when the task and the grading are sound.**
Zero passes triggers investigation; it is not automatic acceptance. Failure
review asks which of these produced the failure: a real reasoning limitation,
ambiguity in the question, missing context, broken execution, or a grading error.
Only the first one counts.

## 4. Self-checks

You may run an agentic attempt with whatever you already have — Claude Code,
gemini-cli, Cursor, an API you already pay for. It is genuinely useful and we
encourage it, but it is not required and it is not the acceptance measurement.

If you run one, **the model's answer is worth more than its pass/fail.** Grade it
against your own rubric, criterion by criterion. Two things fall out:

- You find out whether your rubric can actually be applied by someone who is not
  you. Most rubric defects surface here rather than at review.
- An authentic wrong answer is a far better entry in `grading-examples.json` than
  a flawed answer you invented. Real distractors have a texture that strawmen do
  not.

Disclose everything you ran: model and version, task revision, budget, every
answer produced, and your per-criterion scores. Record "not run" explicitly if
you ran nothing. Undisclosed self-checks are treated as concealment, not
oversight.

## 5. Return and rejection

A task comes back for: a missing or incorrect answer; facts the participant
cannot discover; a copied or lightly rewritten question; unresolved source
permissions; a broken environment; answer or rubric leakage into the participant
image; ambiguous or redundant criteria; undisclosed AI assistance; or
insufficient difficulty under the assigned evaluation.

A judge error puts calibration on hold until it is corrected — a task is never
rejected for a grading fault that is ours.

Passing your own checks is submission readiness. It is not acceptance.
