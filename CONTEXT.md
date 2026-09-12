# SWE Q&A vocabulary

What the pieces are. `AUTHORING.md` and `CONTRIBUTING.md` explain how to build
and submit them.

A **task** is one question about one codebase, together with everything needed to
investigate it, the answer, the evidence for that answer, and the rubric that
decides whether someone else's answer is right.

## The product

**SWE_QA**:
The task type. One of four the buyer defines (`SWE_BENCH`, `LONG_HORIZON_SWE`,
`TERMINAL_TASK`, `SWE_QA`). Graded by `RUBRIC`, not `UNITTEST`.
_Avoid_: "Q&A pair", "question bank" — both describe a cheaper product that is
not this one.

**Participant**:
Whoever attempts the task from `instruction.md` and the environment alone: the
model under evaluation, or the second engineer in the independent human solve.
_Avoid_: "user", "candidate".

**Judge**:
The model configuration that scores a participant's answer against the rubric.
Always a different configuration from the model being evaluated. Askable owns it;
authors do not implement it.

## Task anatomy

**Question**:
The uncertainty the participant must resolve, stated in `instruction.md` together
with the scenario, the scope of the answer, and the environment. One central
question; subquestions only when they develop the same investigation.
_Avoid_: prompt.

**Reference answer**:
The author's own answer, in `reference/answer.md`, structured as Conclusion,
Mechanism, Boundaries, Verification. The thing a rubric is written from — never
shown to the participant, and never the definition of correctness by itself. A
different correct explanation is still correct.
_Avoid_: "the solution", "ground truth", "answer key".

**Evidence record**:
One entry in `reference/evidence.json` (`E01`, `E02`, …) tying a specific claim
to a specific source location and a specific verification. Records are the unit
the reference answer and the rubric both cite.

**Reproduction**:
A script under `reference/reproductions/` that produces runtime evidence, with
its retained log. A reproduction must *discriminate*: it separates the correct
conclusion from a plausible wrong one. Output consistent with both explanations
is not evidence.

**Environment**:
What the participant investigates in: source at a pinned commit, configuration,
inputs, and whatever is needed to inspect the relevant behaviour. Always offline,
and it holds nothing from `reference/`, `evaluation/` or `calibration/`.

**Environment mode**:
`container` or `source-only`, set in `task.json`. `container` ships a Dockerfile
pinned by digest and is required for any task carrying executed evidence.
`source-only` ships a fetch script and a checksummed archive, and is allowed only
when every evidence record is source analysis. A runtime claim needs a runtime.

**Smoke test**:
A check that the environment is usable. It deliberately does not exercise the
behaviour the question is about — a passing smoke test is not evidence for the
answer.

## Grading

**Criterion**:
One independently checkable requirement in `evaluation/rubric.json` (`R01`,
`R02`, …), scored met or unmet. Carries a `pass_condition`, a `fail_condition`,
`acceptable_alternatives`, the `evidence_ids` that support it, and whether it is
`required`.
_Avoid_: "rubric item" when you mean one criterion; "points", "score" — criteria
are binary, not weighted.

**Required criterion**:
A criterion covering an essential fact. A task passes when every required
criterion is met and the answer contains no material contradiction of them.
Optional criteria are diagnostic only and never decide the outcome.

**Grading example**:
One labelled answer in `evaluation/grading-examples.json` with every criterion
marked met or unmet: the reference, at least one correct paraphrase, and at least
two plausible flawed answers. The paraphrase proves the rubric accepts a
different correct explanation; the flawed answers prove it rejects for factual
reasons rather than for wording.

**Material contradiction**:
A statement in the answer that contradicts a required criterion, even when some
other passage satisfies it. Grading reads the whole answer, not the best sentence
in it.

## Difficulty and provenance

**Contamination probe**:
The question asked of a frontier chat model with no repository access, no
attachments, no follow-ups. If the model answers it, the question is answerable
from general knowledge or memorised source and the task is dead. Required at
proposal, recorded in `AUTHOR_NOTES.md`. Free.

**Self-check**:
Three or more agent attempts run by the author, with every answer graded against
their own rubric, recorded in `calibration/self-check.json` with
`authoritative: false`. Required before submission. The fraction is a kill screen
(3/3 means too easy); the grading is what the exercise is for. Never the
measurement that decides acceptance.
_Avoid_: calling it calibration.

**Calibration**:
Askable's authoritative fixed-attempt measurement against the designated target,
agent, budget and judge for the batch. Not something authors run.

**Independent human solve**:
A second engineer working from `instruction.md` and the environment alone, who
has not seen the reference answer. They must reach a defensible answer. Their
disagreements are resolved before the rubric is frozen.

**Revision**:
A new `revision` in `task.json`, required whenever the question, source,
environment, reference answer or rubric changes. Askable decides which checks are
repeated.

**Provenance**:
The record (`provenance.json`) of every third-party dependency, sample, dataset,
binary, or fixture, with its licence and why those terms permit Askable's
AI-training use. An empty record asserts the task contains none.

**Attestation**:
A contributor's signed, commit-bound declaration in `attestations/<handle>.md`
affirming hand-written work, personal verification of every claim, the
contamination probe, AI disclosure, authority to contribute, and assignment of
rights to Askable.
