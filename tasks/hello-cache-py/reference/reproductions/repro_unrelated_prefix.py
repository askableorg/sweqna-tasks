#!/usr/bin/env python3
"""Does an in-flight fetch for `user:42` survive `invalidate("session:")`?

Run from the task root:
    PYTHONPATH=environment/src python3 reference/reproductions/repro_unrelated_prefix.py

The scheduler makes the interleaving explicit, so the result does not depend on
timing: fetch starts, invalidation runs, fetch resumes.
"""

from cachelib import Fetcher, Scheduler, Store


def scenario(invalidated_prefix):
    store = Store()
    fetcher = Fetcher(store, lambda key: f"value-for-{key}")
    scheduler = Scheduler()

    scheduler.start("f1", fetcher.fetch("user:42"))
    generation_at_start = store.generation
    dropped = store.invalidate(invalidated_prefix)
    returned = scheduler.resume("f1")

    return {
        "invalidated_prefix": invalidated_prefix,
        "entries_dropped_by_invalidate": dropped,
        "generation_before": generation_at_start,
        "generation_after": store.generation,
        "value_returned_to_caller": returned,
        "value_in_cache_afterwards": store.get("user:42"),
        "rejected_inserts": store.rejected_inserts,
    }


def main():
    for prefix in ("session:", "user:"):
        print(f"--- invalidate({prefix!r}) while fetch('user:42') is in flight ---")
        for field, value in scenario(prefix).items():
            print(f"  {field}: {value!r}")
        print()


if __name__ == "__main__":
    main()
