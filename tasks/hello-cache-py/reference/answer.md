# Reference answer — cache repopulation after an unrelated invalidation

## Conclusion

After step 3, `user:42` is **not** in the store: `store.get("user:42")` returns
`None`. The caller of the fetch nonetheless receives the fetched value
(`"value-for-user:42"` with the origin used here). The insert is rejected, not
the fetch.

The prefix passed to `invalidate` is irrelevant to this outcome. `invalidate`
bumps a single store-wide generation counter regardless of which prefix it was
given and regardless of whether it dropped any entries, so any invalidation that
overlaps an in-flight fetch discards that fetch's insert. This holds whenever the
interleaving is: fetch observes the generation → an invalidation runs → the fetch
inserts. [E01, E02, E03, E04]

## Mechanism

Two values are compared: the generation the fetch captured before suspending, and
the store's generation at the moment of insert.

`Fetcher.fetch` reads `self.store.generation` into `observed_generation`
(`fetcher.py:19`) *before* it suspends at the origin call (`fetcher.py:20`). When
it resumes it calls `self.store.insert(key, value, observed_generation)`
(`fetcher.py:22`), passing the stale reading. [E01]

`Store.insert` compares that argument with the live counter and returns early on
any mismatch, incrementing `rejected_inserts` and writing nothing
(`store.py:29–31`). Only an exact match reaches the assignment at `store.py:32`.
[E02]

`Store.invalidate` does two separate things (`store.py:35–41`): it deletes the
entries whose keys match `prefix` (`store.py:37–39`), and it increments
`self._generation` (`store.py:40`). The increment is unconditional — it is outside
the loop, is not guarded by whether `doomed` is empty, and does not consult
`prefix`. This is what makes the prefix irrelevant: `invalidate("session:")` with
no matching keys still moves the counter from 0 to 1. [E03]

So the sequence is: `observed_generation = 0` → `invalidate` makes
`_generation = 1` → `insert(..., 0)` sees `0 != 1` and returns `False`. The value
is still returned to the caller because `fetch` returns `value` at `fetcher.py:23`
independently of what `insert` returned; `insert`'s boolean is discarded at
`fetcher.py:22`. [E01, E04]

The guard is therefore correct but conservative. It cannot produce a stale entry,
and the cost of that guarantee is that an invalidation of one key space discards
concurrent work in every other key space.

## Boundaries

- **The entry was never evicted.** `invalidate("session:")` dropped zero entries
  and `user:42` was not in the store to begin with — the fetch was still in
  flight. Attributing the absence to eviction is wrong even though it reaches the
  right outcome. [E04]
- **The caller is unaffected.** This is a cache-effectiveness problem, not a
  correctness problem at the call site: the value is returned, the next fetch
  simply misses again.
- **Interleaving-dependent.** If the invalidation lands entirely before
  `fetcher.py:19` or entirely after `fetcher.py:22`, the generations match and the
  insert succeeds. The claim is about overlap, not about invalidation in general.
- **Cache-hit path is not involved.** A fetch that finds a cached entry returns at
  `fetcher.py:17` and never reads the generation or inserts.
- **Not established by this evidence:** how the library behaves under real
  threading. `Scheduler` is cooperative and single-threaded by construction, and
  `Store` has no locking; nothing here shows whether `_generation` reads and
  writes are safe under genuine concurrency. The failing insert is a design
  consequence visible in the source, not an artefact of the test harness.

## Verification

`reference/reproductions/repro_unrelated_prefix.py` builds the interleaving from
the instruction with the deterministic scheduler and prints the observable state
after step 3. It runs the scenario twice — once with the unrelated prefix
`"session:"` and once with the matching prefix `"user:"` — so the output
discriminates the correct conclusion from the plausible wrong one that the prefix
matters.

```
PYTHONPATH=environment/src python3 reference/reproductions/repro_unrelated_prefix.py
```

Both cases print `entries_dropped_by_invalidate: 0`, `generation_after: 1`,
`value_returned_to_caller: 'value-for-user:42'`, `value_in_cache_afterwards: None`
and `rejected_inserts: 1`. Identical results across the two prefixes is the
positive evidence that the outcome is prefix-independent; `rejected_inserts: 1`
identifies the generation guard rather than eviction as the mechanism, since
eviction would leave that counter at 0. Full output is retained at
`reference/reproductions/repro_unrelated_prefix.log`. [E04]
