# hello-cache-py — worked example

A complete, valid SWE Q&A task in miniature. **It is a reference example only:
deliberately small, deliberately easy, and not eligible for submission.** Its job
is to show the shape of every artefact — what an evidence record looks like when
it is real, what a rubric criterion looks like when it is independently
checkable, what a flawed answer looks like when it is plausible rather than a
strawman.

Two things about it are unlike a submittable task, and both are called out in
`AUTHOR_NOTES.md`: the codebase was authored for the example rather than pinned
from an approved repository, and the question is answerable in minutes by a
competent reader.

## Layout

| Path | What it is |
|---|---|
| `instruction.md` | Everything the participant sees |
| `task.json` | Task metadata and environment record |
| `environment/` | `Dockerfile`, the participant's source tree, smoke test |
| `reference/answer.md` | The reference answer |
| `reference/evidence.json` | Four evidence records, E01–E04 |
| `reference/reproductions/` | The experiment, its README, its retained log |
| `evaluation/rubric.json` | Nine criteria, eight required |
| `evaluation/grading-examples.json` | Reference, paraphrase, two flawed answers, fully labelled |
| `provenance.json` | Empty — no third-party material |
| `AUTHOR_NOTES.md` | Investigation summary, wrong answers, contamination probe, effort |
| `attestations/` | Contributor declaration template |

`reference/` and `evaluation/` are never copied into the participant image. The
`Dockerfile` copies `src/` and nothing else.

## Run it

```bash
# from this directory
PYTHONPATH=environment/src python3 reference/reproductions/repro_unrelated_prefix.py
PYTHONPATH=environment/src ./environment/smoke-test.sh

# validate the whole task
../../scripts/validate-task.sh tasks/hello-cache-py   # from the repo root
```

## Build the container

```bash
docker build -t sweqa-hello-cache-py environment/
docker run --rm --network none sweqa-hello-cache-py \
  python3 -c "from cachelib import Store; print(Store().generation)"
```

Reset is `docker rm -f` and re-run: the image carries no mutable state.
