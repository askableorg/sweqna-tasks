# Author notes — hello-cache-py

## Investigation summary

The library is 90 lines, so there was no search problem — the work was deciding
which of two outcome-compatible stories is the real one. `invalidate` both
deletes matching entries and bumps the counter, and in this interleaving the
deletion is a no-op while the bump is decisive. An answer that names the wrong
half of that function still predicts the right observable outcome, which is
exactly the failure the rubric has to catch.

The design choice that makes the task gradeable is the `Scheduler`. Threads would
have made the interleaving probabilistic and the evidence unreproducible; a
generator suspension point makes "the invalidation lands during the fetch" a
statement the participant can construct on purpose.

## Wrong conclusions this task is built to distinguish

1. **Prefix scoping.** `invalidate("session:")` does not touch `user:` keys, so
   the insert succeeds. Plausible because that is how a reasonable person would
   design the counter, and because nothing in the naming contradicts it. Killed
   by `store.py:40`: the increment is outside the loop and never reads `prefix`.
   Graded by R05. Example answer: `G03`.
2. **Eviction.** The key is absent because the invalidation cleared it. Reaches
   the correct outcome through a mechanism that is not operating: `invalidate`
   dropped zero entries, and the key was never in the table because the fetch had
   not finished. Graded by R03 and R06. Example answer: `G04`.

Both are the shape an answer takes when the reader stops at the first consistent
story. The two-prefix reproduction separates (1); the `rejected_inserts` counter
separates (2).

## Rubric mapping

| Instruction clause | Criteria |
|---|---|
| "what `store.get(\"user:42\")` returns" | R01 |
| "what value the fetch returns to its caller" | R02 |
| "which values are compared, where each is captured and read" | R03, R04 |
| "whether the argument passed to `invalidate` changes the outcome, and why" | R05, R06 |
| "at least one condition under which the outcome would differ" | R07 |
| "run at least one experiment that distinguishes…" | R08 |
| "what your evidence does not establish" | R09 (optional) |

Every criterion traces to a clause the instruction states outright. Nothing is
graded that the participant was not asked for.

**Nine criteria, below the 10–15 target, deliberately.** The codebase is 90 lines
and supports six substantive facts plus verification and boundaries. Reaching
twelve would have meant splitting R03 into one criterion per compared value, or
adding trivia about `keys()` — both of which make the rubric look thorough and
grade worse. A full task on a real repository should hit the target honestly.

## Source relationship

The `cachelib` package was written for this example, so there is no upstream
project and no contributor relationship to declare.

Authoring about your own code is allowed (`AUTHORING.md` §2). Where it applies,
this section records what the author wrote, plus what they know about it that is
not in the repository — and confirms that none of that private context is needed
to answer the question. Everything E01 to E04 establishes here is read off the
source and the retained log.

## Contamination probe

**Not applicable to this example, and recorded as such rather than skipped.** The
`cachelib` package was authored for the task and has never been public, so a
no-repository probe cannot tell us anything: no model has seen it, and a null
result is not evidence of anything.

A submittable task on a real repository must record a real probe here:

- Model and version, and the date.
- The exact prompt — the question from `instruction.md`, verbatim, with no
  repository access and no attachments.
- The model's full answer.
- Your verdict, graded against the rubric: how many required criteria the
  no-access answer met.

If a no-access model meets the required criteria, the question is answerable from
general knowledge or from memorised source, and the task is dead. Say so and
propose a replacement rather than submitting it.

## Self-check disclosure

**Not run, and exempt.** A submittable task requires `calibration/self-check.json`
with at least three graded attempts; the validator skips that check for
`status: "example"`. This task is deliberately easy and would pass 3/3, which is
the outcome that fails a real submission.

The shape a real one takes is in `templates/self-check.json`: agent, exact model
version, date, task revision, budget, and for every attempt the agent's full
answer plus your per-criterion grading. Commit the rubric before you run it.

## Effort log

| Phase | Hours |
|---|---|
| Environment and source | 1.0 |
| Investigation and reproduction | 0.5 |
| Answer and evidence | 1.0 |
| Rubric and grading examples | 1.5 |
| **Total** | **4.0** |

Independent solve time: not measured — the task is not eligible, so no second
engineer was asked to solve it.

## Known limitations

- The Dockerfile pins a tag, not a digest. A submittable task pins the digest.
- `repo_url` points at this template repository and `repo_commit` is a
  placeholder, because there is no upstream project to pin.
- `environment.mode` is `container` because E04 is executed evidence. Had the
  answer rested entirely on reading `store.py` and `fetcher.py`, this would have
  been a `source-only` task and no Dockerfile would exist.
- The question is answerable in roughly ten minutes by a competent Python reader.
  A submittable task requires investigation across components, and this one does
  not.
