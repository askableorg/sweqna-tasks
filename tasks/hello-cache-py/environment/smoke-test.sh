#!/usr/bin/env bash
# Proves the environment is usable. It deliberately does not exercise the
# behaviour the question is about — a passing smoke test is not evidence for the
# answer.
set -euo pipefail

python3 -c "
from cachelib import Store, Fetcher, Scheduler
store = Store()
assert store.generation == 0
assert store.get('anything') is None
Fetcher(store, lambda k: k)
Scheduler()
print('smoke: cachelib importable, store empty at generation 0')
"
