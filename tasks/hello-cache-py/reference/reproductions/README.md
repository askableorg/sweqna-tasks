# Reproductions

## repro_unrelated_prefix.py

Builds the interleaving from `instruction.md` — fetch starts, invalidation runs,
fetch resumes — using `Scheduler` so the ordering is explicit and carries no
timing dependence. Runs the scenario twice, with an unrelated prefix
(`"session:"`) and a matching one (`"user:"`).

Run from the task root:

```bash
PYTHONPATH=environment/src python3 reference/reproductions/repro_unrelated_prefix.py
```

Expected for **both** prefixes:

```
entries_dropped_by_invalidate: 0
generation_before: 0
generation_after: 1
value_returned_to_caller: 'value-for-user:42'
value_in_cache_afterwards: None
rejected_inserts: 1
```

Two observations do the discriminating work. Identical output across the two
prefixes rules out "the prefix scopes the invalidation". `rejected_inserts: 1`
alongside `entries_dropped_by_invalidate: 0` rules out eviction, because eviction
would produce the opposite pair.

Retained output: `repro_unrelated_prefix.log`.

Participants do not receive this directory. They have the source, the scheduler,
and a Python interpreter, which is everything needed to derive the result
independently.
