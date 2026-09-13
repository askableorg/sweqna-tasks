# Contributing a SWE Q&A task

This repository is source-available under the `LICENSE`; it is not an open-source
project. Before creating a task, sign the Askable participant agreement, clone
this repository, and do all your work in your own **private** GitHub repository
created from it.

## AI-use policy

You may use AI coding agents to explore the codebase, write scripts, draft prose,
and check your work. We expect you to — fluency with these tools is part of why
you were selected.

Four conditions are absolute:

1. **You own every claim.** Personally verify every substantive claim, every
   citation, and every experimental result, and be able to defend each one in a
   live 30-minute walkthrough. "The agent said so and it sounded right" is a
   failing answer. Work you cannot explain is unverified and returned.
2. **The question is yours.** `instruction.md` must be hand-written, or edited so
   heavily that every requirement is your own. Pasted AI-generated instructions
   have a recognisable signature and are rejected on sight.
3. **The answer is yours.** This is the condition that matters most for SWE Q&A
   and the one with no equivalent in terminal tasks. A model can produce a
   fluent, well-cited, confidently wrong explanation, and you are the only person
   in the process positioned to catch it. Every citation in
   `reference/evidence.json` gets opened and read at the pinned commit. Every
   line range gets checked. Every reproduction gets run by you, on your machine,
   with its output retained.
4. **Disclose your tools.** List every AI tool used in `ai_tools_used` in
   `task.json` (e.g. `["claude-code", "cursor"]`; `[]` if none), and describe what
   each contributed in `AUTHOR_NOTES.md`.

Your private repository's incremental commit history — including the dead ends
and the experiments that went nowhere — is part of how we verify this. A single
giant commit is a red flag regardless of how the work was produced. Preserve
failed experiments in your repository; keep them out of the participant image.

## Third-party material and provenance

Record every third-party dependency, code sample, dataset, binary and fixture in
`provenance.json`. Each item needs a name, source URL or origin, licence, version
or content hash, and an explanation of why its terms permit Askable's intended
AI-training use.

**Which repository you may use** is covered in `AUTHORING.md` §2: `open-source`,
`owned`, or `permissioned`, declared as `source.rights_basis` in
`provenance.json`. For `permissioned`, Askable confirms the grant with the owner
directly before authoring starts. Never send private code inside a proposal, and
never include employer code without written permission obtained beforehand.

**Licence, and why the container is not the question.** Packaging a repository
into a Docker image is redistribution, but so is handing over the source — the
container only bundles it with its dependencies. Every benchmark in this space
ships Docker images of open-source repositories pinned to a commit. What decides
the answer is the licence, not the packaging.

Permissive licences (MIT, Apache-2.0, BSD) are straightforward: redistribute with
the notice intact and record why the terms permit AI-training use. Copyleft needs
a decision before you start, not at submission, because distributing an image
containing GPL code carries the source-provision obligation. **AGPL is out.** If
your candidate repository is copyleft, raise it in the proposal and wait.

Note also that a base image redistributes hundreds of OS packages of its own.
That is normal and expected; it is in the chain, so pin it by digest.

Use an empty `third_party_material` array only when the task genuinely contains
none. Do not include anything whose rights are uncertain, and do not include
employer code or private assets without approval and the authority to contribute
them.

## Separation

Nothing under `reference/`, `evaluation/` or `calibration/` may reach the
participant environment. Use
explicit `COPY` paths in the Dockerfile — never `COPY . /task`. The validator
enforces this, but the rule matters more than the check: a participant who can
see the answer key produces a measurement of nothing.

The same separation applies to your git history inside the image, to comments you
add to the source, and to filenames. Do not name a scratch file `why-the-guard-
rejects-it.py` and copy it in.

## Submission

1. Write the task (`AUTHORING.md`). Confirm every citation resolves and every
   reproduction runs.
2. Run the self-check: at least three agent attempts, every answer graded
   against the rubric you already committed, recorded in
   `calibration/self-check.json` (`DIFFICULTY.md` §5). Harvest a failed answer
   into `grading-examples.json`.
3. Fill `AUTHOR_NOTES.md`, including the contamination probe record.
4. Run `./scripts/validate-task.sh tasks/<task>` and clear every error.
5. Commit task code, provenance and notes. Save that SHA as `TASK_CODE_COMMIT`.
6. Complete the contributor attestation in `attestations/<your-handle>.md`
   against `TASK_CODE_COMMIT`.
7. Send the handoff: private repository URL or ZIP, task ID, the full submission
   commit SHA, the approved proposal reference, and a short summary of the checks
   you performed. For an archive, include a SHA-256 checksum.
8. Add `@xicovarisco` as a read collaborator, or send the archive through your
   assigned Askable channel.

Never include API keys, access tokens, or local credential files.

## Review

1. **Completeness and environment.** Source identity, provenance, container
   setup, smoke results, and separation of participant material from answers and
   grading files.
2. **Independent human solve.** A second engineer receives only `instruction.md`
   and the environment. They must reach a defensible answer without your
   reference. You resolve ambiguities and factual disagreements before the rubric
   is frozen — this is the step that most often changes a task, and it is the
   step worth writing for.
3. **Rubric and judge validation.** Coverage in both directions: every graded
   requirement is in scope of the question, and every essential requested fact is
   graded. Automated judgments are compared with human labels, per criterion.
4. **Difficulty screening and calibration.** See `DIFFICULTY.md`.
5. **Failure review and release decision.** Whether failures reflect reasoning
   limitations, ambiguity, missing context, broken execution, or grading errors.

**During review you must:** attend a 30-minute walkthrough and explain the
conclusion, the evidence, the reproduction, the rubric and the plausible wrong
answers; respond to specific findings with corrected files and an explanation;
and create a new `revision` in `task.json` whenever the question, source,
environment, reference or rubric changes. Do not hide or delete previous model
attempts.

## Time

Plan roughly **9–18 active author hours** for a full task, plus repository
onboarding if the codebase is new to you. Familiar projects take less. This is a
planning estimate, not a quota and not a payment term.

Log time separately for setup, investigation, answer and evidence, rubric, and
revisions, and record independent solve time separately from authoring time.
Agree milestone dates and budget with Askable before starting, and raise access
problems, unclear requirements, or likely overruns early rather than at
submission.
