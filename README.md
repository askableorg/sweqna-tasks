# SWE Q&A Tasks

Source-available template for authoring **SWE Q&A** evaluation tasks for Askable:
original questions about real codebases, answered from evidence, graded against a
rubric rather than a test suite. It includes the artefact templates, a worked
example, and a validator that checks structure, citations, rubric consistency and
answer leakage before a reviewer ever opens the task.

**The goal of every SWE Q&A task is to capture a question a skilled engineer can
answer from the code and an AI agent cannot yet answer correctly.** A task earns
its place by isolating one of those gaps. Questions a model answers from general
knowledge are worthless, and so are questions no engineer could settle from the
supplied source.

This is a different product from a terminal task, and the difference is the whole
point. A terminal task asks an agent to *do* something and a verifier decides
whether it worked. A SWE Q&A task asks an agent to *explain* something, and a
rubric written by a human who already established the answer decides whether the
explanation is right. **`Number of Rubrics` is the headline quality metric here,
not `Number of Hidden Test Cases`.**

Use is restricted by the repository licence and the Askable participant
agreement. Do not use this repository to create tasks for another purpose.

## Read these first

1. **`AUTHORING.md`** — what a good question is and how to build one. The core
   document; read it before writing anything.
2. **`DIFFICULTY.md`** — the acceptance bar, the contamination probe, and what
   gets rejected.
3. **`CONTRIBUTING.md`** — process, the AI-use policy, provenance, attestations,
   submission.
4. **`CONTEXT.md`** — the vocabulary (question, reference answer, evidence
   record, criterion, probe) the other documents assume.
5. **`tasks/hello-cache-py/`** — a complete worked example. Read it alongside
   `AUTHORING.md`; between the two, the example is the one that will teach you
   the shape.

## The workflow, end to end

1. **Sign the Askable participant agreement**, then clone this repository.
2. **Create your own private GitHub repository** from your clone. All your work
   lives there, with real incremental commit history — we review that history as
   part of acceptance.
3. **Scaffold a task:** `./scripts/new-task.sh my-task`, or
   `./scripts/new-task.sh --source-only my-task` for a question the participant
   answers by reading rather than running.
4. **Fill `PROPOSAL.md` and send it through Askable.** This is a checkpoint, not
   a formality: it is where the repository and the scope get approved, and it is
   the cheapest place to find out the question does not work. It requires the
   contamination probe (`DIFFICULTY.md`). Do not start substantial authoring
   before approval. One approved task at a time.
5. **Build the environment, investigate, and write the answer** with evidence
   records that cite real paths, symbols and line ranges at the pinned commit.
   Docker is needed only when the question rests on runtime evidence — see
   `AUTHORING.md` §4.
6. **Write the rubric and commit it**, then test it against four answers: your
   reference, a correct paraphrase, and two plausible flawed answers.
7. **Run the self-check:** three agent attempts, every answer graded against that
   rubric (`DIFFICULTY.md` §5). Gemini 3.8 Flash is free in Gemini CLI and
   Antigravity, so this costs time, not money.
8. **Validate:** `./scripts/validate-task.sh tasks/my-task` — clean before you
   submit.
9. **Submit** (`CONTRIBUTING.md`), then either add Askable's reviewer account
   (`@xicovarisco`) as a read collaborator on your private repository, or send an
   archive.

## Validate

```bash
./scripts/validate-task.sh tasks/my-task     # one task
./scripts/validate-all.sh                    # everything under tasks/
./scripts/validate-task.sh tasks/my-task --strict   # warnings fail too
```

The validator checks what a reviewer would otherwise check by hand: every
required file present, every JSON parsing, every cited path and symbol existing
with the line range inside the file, every `evidence_ids` reference resolving,
every rubric criterion labelled in every grading example, each example's
`expected_outcome` agreeing with its own labels, the environment mode matching
the evidence it carries, three graded self-check attempts that are not 3/3, and
the Dockerfile not copying `reference/` or `evaluation/` into the participant
image.

**Green is the precondition for review, not evidence that the task is any good.**
It cannot tell you whether the question is interesting or the answer is right.

## What Askable does, and what you do not have to

Askable runs the authoritative calibration and judge validation against the
designated target for your batch, and handles harness packaging. You do not need
the production judge, paid API access, or the batch's target model.

Two things are on you, and both are free:

- **The contamination probe.** One message, no repository access. Required at
  proposal (`DIFFICULTY.md` §1).
- **The self-check.** Three agent attempts, every answer graded against your
  rubric, recorded in `calibration/self-check.json` (`DIFFICULTY.md` §5). The
  fraction is a kill screen, not a measurement. The grading is the point.

Docker is required only for tasks whose answers rest on runtime evidence.

## Repository layout

| Path | What it is |
|---|---|
| `AUTHORING.md` `DIFFICULTY.md` `CONTRIBUTING.md` `CONTEXT.md` | The documents above |
| `schema/FIELDS.md` | Field-by-field reference for every JSON artefact |
| `scripts/` | `new-task.sh`, `validate-task.sh`, `validate-all.sh`, `validate_task.py` |
| `templates/` | `PROPOSAL.md`, `instruction.md`, `AUTHOR_NOTES.md`, `self-check.json`, `fetch-source.sh`, attestation |
| `tasks/hello-cache-py/` | The worked example — reference only, not eligible |
