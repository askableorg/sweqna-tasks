# Cache repopulation after an unrelated invalidation

The `cachelib` package at `/task/src/cachelib` is a small read-through cache. A
`Store` holds entries and a monotonic generation counter; a `Fetcher` performs a
read-through fetch whose slow origin call is modelled as a generator suspension
point, so a `Scheduler` can drive the interleaving deterministically.

A service using this library reports that entries disappear from the cache under
load even when nothing related to them was invalidated. The maintainers want to
understand the mechanism before they change anything.

Consider this interleaving:

1. A fetch for the key `user:42` starts. There is no cached entry, so it proceeds
   towards the origin and suspends at its origin call.
2. While that fetch is suspended, `store.invalidate("session:")` runs. No key in
   the store starts with `session:`.
3. The suspended fetch resumes and completes.

## The question

After step 3, is `user:42` present in the store, and what does the caller of the
fetch receive? Explain the mechanism that produces that outcome.

Your answer must cover:

- **The outcome**, stated directly: what `store.get("user:42")` returns after
  step 3, and what value the fetch returns to its caller.
- **The mechanism**: which values are compared, where each is captured and read,
  and why the comparison resolves the way it does.
- **The role of the prefix**: whether the argument passed to `invalidate` changes
  the outcome for `user:42`, and why.
- **Boundaries**: at least one condition under which the outcome would differ,
  and what your evidence does not establish.

Support every claim with file, symbol, and line references into
`/task/src/cachelib`. Because the question is about runtime behaviour, run at
least one experiment that distinguishes your conclusion from a plausible wrong
one, and report the command you ran and the output you observed.

## Environment

- The package is at `/task/src/cachelib`; `PYTHONPATH` is already set to
  `/task/src`.
- Python 3.12, no network access, no third-party packages required.
- You may add scratch files anywhere under `/task`. Do not edit the files in
  `/task/src/cachelib` — if you want to test a variant, copy it first.
